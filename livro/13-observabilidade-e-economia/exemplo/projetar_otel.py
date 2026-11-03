#!/usr/bin/env python3
"""projetar_otel.py — o livro de ponto PROJETADO no formato OpenTelemetry, com minimização.

A tese do capítulo 13: telemetria é projeção do log, não dependência. Este script lê o mesmo
livro de ponto que economia.py e devolve spans no formato de dados do OpenTelemetry (OTel),
SEM biblioteca e SEM coletor:

    trace  = o ciclo (o "chamado")         trace_id = sha256(ciclo)[:32]
    span   = uma tentativa (start → stop)  span_id  = sha256(tarefa#tentativa)[:16]
    evento = o veredito, pendurado no span da tentativa julgada

Os nomes de uso de modelo seguem as convenções semânticas GenAI do OTel (gen_ai.*); o resto
fica num espaço próprio (esoa.*). A MINIMIZAÇÃO é uma lista de permissão: só sai o que está
nela. Texto livre (reason, note), identificador de sessão e destinatário NUNCA saem — e o
script diz quantos de cada ficaram para trás.

Portão: depois de projetar, `vazou()` procura qualquer atributo fora da lista. Com
--sem-filtro o script copia tudo (a mutação de propósito) e o portão tem de reprovar.

Uso:   python3 projetar_otel.py [livro.jsonl] [--sem-filtro] [--json]
Saída: 0 = projeção minimizada · 1 = vazou campo fora da lista · 2 = livro ilegível.
"""
import hashlib
import json
import os
import sys
from collections import Counter

# o que PODE sair — e com que nome
PERMITIDOS_STOP = {
    "tokens_in": "gen_ai.usage.input_tokens",
    "tokens_out": "gen_ai.usage.output_tokens",
    "tokens_cache_read": "esoa.usage.cache_read_tokens",
    "tokens_cache_write": "esoa.usage.cache_write_tokens",
    "cost_usd": "esoa.cost_usd",
    "outcome": "esoa.task.outcome",
    "duration_s": "esoa.task.duration_s",
    "requests": "esoa.task.requests",
}
PERMITIDOS_START = {"model": "gen_ai.request.model", "kind": "esoa.task.kind", "attempt": "esoa.task.attempt"}
PERMITIDOS_VEREDITO = {"verdict": "esoa.verdict", "by": "esoa.verdict.by"}
NOMES_OK = (set(PERMITIDOS_STOP.values()) | set(PERMITIDOS_START.values())
            | set(PERMITIDOS_VEREDITO.values()) | {"gen_ai.operation.name"})
ESTRUTURA = {"ts", "event", "task_id", "cycle"}   # vira trace/span/tempo, não atributo
JA_PROJETADOS = set(PERMITIDOS_STOP) | set(PERMITIDOS_START) | set(PERMITIDOS_VEREDITO)


def h(texto, n):
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()[:n]


def projetar(eventos, filtrar=True):
    spans, abertos, descartados = [], {}, Counter()
    ciclo_da_tarefa = {}

    def copia(e, mapa):
        attrs = {}
        for k, v in e.items():
            if k in ESTRUTURA:
                continue
            if k in mapa:
                attrs[mapa[k]] = v
            elif filtrar:
                if k not in JA_PROJETADOS:      # repetição de campo já projetado não conta
                    descartados[k] += 1
            else:
                attrs[k] = v                    # a mutação: sem lista de permissão
        return attrs

    for e in eventos:
        if e.get("cycle"):
            ciclo_da_tarefa.setdefault(e["task_id"], e["cycle"])
        chave = (e["task_id"], e.get("attempt"))
        if e["event"] == "start":
            attrs = copia(e, PERMITIDOS_START)
            attrs["gen_ai.operation.name"] = "invoke_agent"
            abertos[chave] = {"start": e["ts"], "attrs": attrs}
        elif e["event"] == "stop" and chave in abertos:
            a = abertos.pop(chave)
            ciclo = e.get("cycle") or "?"
            attrs = a["attrs"]
            attrs.update(copia(e, PERMITIDOS_STOP))
            spans.append({
                "trace_id": h(ciclo, 32), "span_id": h(f"{e['task_id']}#{e.get('attempt')}", 16),
                "name": f"{e['task_id']}#{e.get('attempt')}",
                "start": a["start"], "end": e["ts"], "attributes": attrs, "events": []})
        elif e["event"] == "verdict":
            alvo = [s for s in spans if s["name"].startswith(e["task_id"] + "#")]
            ev = {"name": "verdict", "time": e["ts"], "attributes": copia(e, PERMITIDOS_VEREDITO)}
            if alvo:
                alvo[-1]["events"].append(ev)
            else:                               # veredito do ciclo inteiro: span próprio, sem duração
                spans.append({"trace_id": h(e["task_id"].replace("-cycle", ""), 32),
                              "span_id": h(e["task_id"] + e["ts"], 16), "name": e["task_id"],
                              "start": e["ts"], "end": e["ts"], "attributes": {}, "events": [ev]})
        elif e["event"] == "assigned":
            for k in e:
                if k not in ESTRUTURA and k not in JA_PROJETADOS and filtrar:
                    descartados[k] += 1         # a atribuição não vira span: tudo fica
    return spans, descartados


def vazou(spans):
    fora = Counter()
    for s in spans:
        for k in s["attributes"]:
            if k not in NOMES_OK:
                fora[k] += 1
        for ev in s["events"]:
            for k in ev["attributes"]:
                if k not in NOMES_OK:
                    fora[k] += 1
    return fora


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    aqui = os.path.dirname(os.path.abspath(__file__))
    caminho = args[0] if args else os.path.join(aqui, "tarefas-064.jsonl")
    try:
        with open(caminho, encoding="utf-8") as f:
            eventos = [json.loads(l) for l in f if l.strip()]
    except (OSError, ValueError) as erro:
        print(f"livro ilegível: {erro}", file=sys.stderr)
        return 2
    eventos.sort(key=lambda e: e["ts"])
    spans, descartados = projetar(eventos, filtrar="--sem-filtro" not in sys.argv)
    if "--json" in sys.argv:
        print(json.dumps(spans, ensure_ascii=False, indent=1))
    else:
        traces = {s["trace_id"] for s in spans}
        com_ev = sum(1 for s in spans if s["events"])
        print(f"{len(eventos)} eventos -> {len(traces)} trace(s), {len(spans)} span(s), {com_ev} com veredito")
        print("ficaram para trás (minimização): "
              + (", ".join(f"{k}×{n}" for k, n in sorted(descartados.items())) or "nada"))
        exemplo = next(s for s in spans if s["events"] and s["attributes"])
        print("um span, por exemplo:")
        print(json.dumps(exemplo, ensure_ascii=False, indent=1))
    fora = vazou(spans)
    if fora:
        print("✗ VAZOU atributo fora da lista de permissão: "
              + ", ".join(f"{k}×{n}" for k, n in sorted(fora.items())))
        return 1
    print("✓ nenhum atributo fora da lista de permissão")
    return 0


if __name__ == "__main__":
    sys.exit(main())
