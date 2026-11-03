#!/usr/bin/env python3
"""economia.py — quanto custa uma tarefa ACEITA, e onde o custo se perde.

Lê um livro de ponto de tarefas (JSON Lines, um evento por linha: assigned, start, stop,
verdict — o formato do task ledger do Maestro) e deriva, NA LEITURA, as métricas de economia
do capítulo 13. Nada é gravado: o livro é só-acréscimo e toda métrica nasce aqui.

Regras que o script impõe (são as do capítulo, não enfeite):
  * custo é por tentativa (stop.cost_usd); stop sem medida é "não medido", nunca zero;
  * veredito só conta se quem o deu (`by`) é uma tarefa de kind review/audit deste livro —
    quem executa ou gerencia não aprova (revisão independente);
  * "tarefa aceita" = tarefa cujo ÚLTIMO veredito válido é approved/approved_with_notes;
    sem veredito válido, a métrica responde "n/a" e diz por quê, em vez de inventar;
  * retrabalho é medido de DOIS jeitos, para mostrar que a definição muda o número:
      (a) por tentativa: tentativas com attempt >= 2;
      (b) por linhagem: tudo que começou depois da primeira reprovação e até a aceitação.

Uso:   python3 economia.py [livro.jsonl]     (padrão: tarefas-064.jsonl, ao lado deste arquivo)
Saída: 0 = livro lido · 2 = livro ilegível. Só biblioteca padrão; Python 3.8+.
"""
import json
import os
import sys
from datetime import datetime

APROVADO = {"approved", "approved_with_notes"}
JUIZES = {"review", "audit"}


def ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def ler(caminho):
    eventos, invalidas = [], 0
    with open(caminho, encoding="utf-8") as f:
        for linha in f:
            if not linha.strip():
                continue
            try:
                e = json.loads(linha)
                ts(e["ts"]), e["event"], e["task_id"]
                eventos.append(e)
            except (ValueError, KeyError, TypeError):
                invalidas += 1
    eventos.sort(key=lambda e: ts(e["ts"]))
    return eventos, invalidas


def tokens(stop):
    return sum(stop.get(k, 0) or 0 for k in
               ("tokens_in", "tokens_out", "tokens_cache_read", "tokens_cache_write"))


def main():
    aqui = os.path.dirname(os.path.abspath(__file__))
    caminho = sys.argv[1] if len(sys.argv) > 1 else os.path.join(aqui, "tarefas-064.jsonl")
    try:
        eventos, invalidas = ler(caminho)
    except OSError as erro:
        print(f"livro ilegível: {erro}", file=sys.stderr)
        return 2

    kind = {}                                   # task_id -> kind
    for e in eventos:
        if e["event"] in ("assigned", "start") and "kind" in e:
            kind.setdefault(e["task_id"], e["kind"])
    starts = [e for e in eventos if e["event"] == "start"]
    stops = [e for e in eventos if e["event"] == "stop"]
    medidos = [s for s in stops if num(s.get("cost_usd"))]
    nao_medidos = [f'{s["task_id"]}#{s.get("attempt", "?")}' for s in stops if not num(s.get("cost_usd"))]
    total = sum(s["cost_usd"] for s in medidos)

    print(f"livro: {os.path.basename(caminho)} · {len(eventos)} eventos · {invalidas} linha(s) inválida(s)")
    print(f"tentativas: {len(stops)} com stop ({len(medidos)} medidas, {len(nao_medidos)} sem medida: "
          f"{', '.join(nao_medidos) or '-'})")

    # 1. Para onde foi o dinheiro: custo por kind
    print("\n1. Custo por tipo de tarefa (só tentativas medidas)")
    por_kind = {}
    for s in medidos:
        k = s.get("kind", "?")
        c, n = por_kind.get(k, (0.0, 0))
        por_kind[k] = (c + s["cost_usd"], n + 1)
    for k, (c, n) in sorted(por_kind.items(), key=lambda x: -x[1][0]):
        print(f"   {k:<10} {n:>2} tentativa(s)  US$ {c:7.4f}  {100 * c / total:5.1f} %")
    print(f"   {'total':<10} {len(medidos):>2}               US$ {total:7.4f}")

    # 2. Tokens por tentativa: o total engana quando o cache domina
    print("\n2. Tokens por tentativa medida")
    tot_tok = sum(tokens(s) for s in medidos)
    novos = sum((s.get("tokens_in", 0) or 0) + (s.get("tokens_out", 0) or 0) for s in medidos)
    cache = sum(s.get("tokens_cache_read", 0) or 0 for s in medidos)
    entrada = sum((s.get("tokens_in", 0) or 0) + (s.get("tokens_cache_read", 0) or 0)
                  + (s.get("tokens_cache_write", 0) or 0) for s in medidos)
    print(f"   média total: {tot_tok / len(medidos):,.0f} tokens · média sem cache (entrada+saída): "
          f"{novos / len(medidos):,.0f} tokens")
    print(f"   taxa de cache (lido / entrada total): {100 * cache / entrada:.1f} %")

    # 3. Vereditos: quem pode aprovar
    juizes_validos = {e["task_id"] for e in starts if kind.get(e["task_id"]) in JUIZES}
    sessao_do_juiz = {}
    for e in starts:
        if e["task_id"] in juizes_validos:
            sessao_do_juiz.setdefault(e["task_id"], set()).add(e.get("session"))
    validos, descartados = [], []
    for e in eventos:
        if e["event"] != "verdict":
            continue
        ok = e.get("by") in juizes_validos and e.get("session") in sessao_do_juiz.get(e.get("by"), set())
        (validos if ok else descartados).append(e)
    print("\n3. Vereditos")
    print(f"   válidos (dados por tarefa review/audit, na sessão que a executou): {len(validos)}")
    print(f"   descartados (dados por quem não julga): {len(descartados)} -> "
          f"{', '.join(sorted({e['task_id'] + '<-' + str(e.get('by')) for e in descartados})) or '-'}")

    # 4. Custo por tarefa aceita
    ultimo = {}
    for e in validos:
        ultimo[e["task_id"]] = e
    aceitas_tarefa = [t for t, e in ultimo.items() if not t.endswith("-cycle") and e["verdict"] in APROVADO]
    aceitos_ciclo = [t for t, e in ultimo.items() if t.endswith("-cycle") and e["verdict"] in APROVADO]
    print("\n4. Custo por tarefa aceita")
    executadas = sorted({e["task_id"] for e in starts if kind.get(e["task_id"]) not in JUIZES})
    print(f"   ingênuo (custo ÷ tarefas executadas, sem juízes): {len(executadas)} tarefa(s), "
          f"US$ {total / len(executadas):.4f} — não diz nada sobre o que foi aceito")
    if aceitas_tarefa:
        print(f"   {len(aceitas_tarefa)} tarefa(s) aceita(s): US$ {total / len(aceitas_tarefa):.4f} por tarefa aceita "
              f"(custo total do livro ÷ tarefas aceitas)")
    else:
        print("   n/a: nenhuma TAREFA tem veredito válido — o número não é calculado, para não ser inventado")
    for c in aceitos_ciclo:
        print(f"   ciclo aceito ({c}, por {ultimo[c]['by']}): custo do ciclo inteiro US$ {total:.4f}")

    # 5. Retrabalho de dois jeitos
    print("\n5. Retrabalho")
    a = [s for s in medidos if (s.get("attempt") or 1) >= 2]
    print(f"   (a) por tentativa (attempt >= 2): {len(a)} medida(s), US$ {sum(s['cost_usd'] for s in a):.4f}")
    reprov = [e for e in validos if e["verdict"] == "rejected"]
    aceite = [e for e in validos if e["verdict"] in APROVADO]
    if reprov:
        t0 = ts(reprov[0]["ts"])
        t1 = min((ts(e["ts"]) for e in aceite if ts(e["ts"]) > t0), default=None)
        linhagem = {e["task_id"] + "#" + str(e.get("attempt")) for e in starts
                    if ts(e["ts"]) > t0 and (t1 is None or ts(e["ts"]) < t1)}
        b = [s for s in medidos if s["task_id"] + "#" + str(s.get("attempt")) in linhagem]
        sem = sorted(x for x in linhagem if x in {n for n in nao_medidos})
        cb = sum(s["cost_usd"] for s in b)
        print(f"   (b) por linhagem (da 1ª reprovação até a aceitação): {len(linhagem)} tentativa(s), "
              f"US$ {cb:.4f} medidos = {100 * cb / total:.1f} % do total"
              + (f" (+{len(sem)} sem medida: {', '.join(sem)})" if sem else ""))
        depois = sorted({e["task_id"] for e in starts if t1 and ts(e["ts"]) > t1})
        if depois:
            print(f"   iniciadas depois dessa aceitação (fora da conta): {', '.join(depois)}")
    else:
        print("   (b) por linhagem: nenhuma reprovação válida no livro")

    # 6. Tempo de ciclo e órfãos
    print("\n6. Tempo de ciclo e órfãos")
    inicio = ts(eventos[0]["ts"])
    if aceite:
        print(f"   do primeiro evento à aceitação: {(ts(aceite[-1]['ts']) - inicio).total_seconds() / 60:.1f} min")
    print(f"   do primeiro ao último evento: {(ts(eventos[-1]['ts']) - inicio).total_seconds() / 60:.1f} min")
    abertos = {}
    for e in eventos:
        chave = (e["task_id"], e.get("session"), e.get("attempt"))
        if e["event"] == "start":
            abertos[chave] = abertos.get(chave, 0) + 1
        elif e["event"] == "stop" and abertos.get(chave):
            abertos[chave] -= 1
    orfaos = sorted(f"{k[0]}#{k[2]}" for k, n in abertos.items() if n)
    print(f"   órfãos (start sem stop = trabalho pago e não entregue): {len(orfaos)} {' '.join(orfaos)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
