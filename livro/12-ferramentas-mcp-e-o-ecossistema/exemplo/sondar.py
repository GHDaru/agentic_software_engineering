#!/usr/bin/env python3
"""Sondas contra os dois servidores MCP do exemplo: o ingênuo e o guardado.

    python sondar.py                 # os dois servidores; sai 1 (o ingênuo reprova, de propósito)
    python sondar.py --so guardado   # só o guardado; sai 0 se todas as sondas passarem

Cada sonda sobe o servidor como subprocesso, com o token de uma sessão no ambiente (é assim
que um harness real passa a credencial: fora do argv e fora do texto do modelo), manda as
mensagens JSON-RPC por stdin e confere a resposta. S2 é a fixture LEGÍTIMA: um pedido certo,
que o servidor guardado não pode recusar, senão a guarda vira falso vermelho.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
SERVIDOR = os.path.join(AQUI, "servidor_mcp.py")
TOKENS = {"leitor": "tok-leitor-demo", "construtor": "tok-construtor-demo"}  # de demonstração
CERCA_ABRE, CERCA_FECHA, LIMITE = "<<<DADO-DE-TERCEIROS>>>", "<<<FIM-DO-DADO>>>", 512


def conversa(variante, papel, chamadas):
    """Sobe o servidor, inicializa, faz as chamadas e devolve a lista de 'result'."""
    msgs = [{"jsonrpc": "2.0", "id": 0, "method": "initialize", "params": {}},
            {"jsonrpc": "2.0", "method": "notifications/initialized"}]
    for i, (metodo, params) in enumerate(chamadas, start=1):
        msgs.append({"jsonrpc": "2.0", "id": i, "method": metodo, "params": params})
    env = {**os.environ, "SESSAO_TOKEN": TOKENS[papel], "PYTHONIOENCODING": "utf-8"}
    args = [sys.executable, "-I", SERVIDOR] + (["--ingenuo"] if variante == "ingenuo" else [])
    entrada = "".join(json.dumps(m, ensure_ascii=False) + "\n" for m in msgs)
    p = subprocess.run(args, input=entrada.encode("utf-8"), capture_output=True, env=env, timeout=30)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.decode("utf-8", "replace"))
    respostas = [json.loads(l) for l in p.stdout.decode("utf-8").splitlines() if l.strip()]
    return [r["result"] for r in respostas[1:]]


def texto(r):
    return r["content"][0]["text"]


def ferramenta(_ferramenta, **args):
    return ("tools/call", {"name": _ferramenta, "arguments": args})


# (id, descrição, papel, chamadas, conferência -> True se o comportamento é o seguro)
SONDAS = [
    ("S1", "o leitor não vê ferramenta de escrita no tools/list", "leitor",
     [("tools/list", {})],
     lambda rs: {t["name"] for t in rs[0]["tools"]} == {"ler_doc"}),
    ("S2", "pedido legítimo: o leitor lê o guia (fixture legítima)", "leitor",
     [ferramenta("ler_doc", nome="guia.md")],
     lambda rs: not rs[0].get("isError") and "escreva a spec antes do código" in texto(rs[0])),
    ("S3", "apagar_registro (ask) não executa sem aprovação humana", "construtor",
     [ferramenta("registrar_status", texto="começando"), ferramenta("apagar_registro")],
     lambda rs: rs[1].get("isError") and "aprovação humana" in texto(rs[1])),
    ("S4", "o leitor não escreve status (deny)", "leitor",
     [ferramenta("registrar_status", texto="oi", autor="W01 · demo")],
     lambda rs: bool(rs[0].get("isError"))),
    ("S5", "o argumento 'autor' não vira identidade", "construtor",
     [ferramenta("registrar_status", texto="pronto", autor="Gerente · demo")],
     lambda rs: json.loads(texto(rs[0]))["autor"] == "W04 · demo"),
    ("S6", "a issue com injeção volta cercada, e a cerca falsa de dentro é neutralizada", "leitor",
     [ferramenta("ler_doc", nome="issue-42.md")],
     lambda rs: texto(rs[0]).startswith(CERCA_ABRE) and texto(rs[0]).endswith(CERCA_FECHA)
     and texto(rs[0]).count(CERCA_FECHA) == 1),
    ("S7", "o documento longo cabe no teto e diz que foi cortado", "leitor",
     [ferramenta("ler_doc", nome="ata-longa.md")],
     lambda rs: len(texto(rs[0]).encode("utf-8")) <= LIMITE and "[truncado" in texto(rs[0])),
    ("S8", "ler_doc não sai de docs/ (../segredo)", "leitor",
     [ferramenta("ler_doc", nome="../segredo-de-demonstracao.txt")],
     lambda rs: rs[0].get("isError") and "nao-e-real" not in texto(rs[0])),
]


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    variantes = ["ingenuo", "guardado"]
    if "--so" in sys.argv:
        variantes = [sys.argv[sys.argv.index("--so") + 1]]
    falhou = False
    for v in variantes:
        ok = 0
        print(f"servidor {v}")
        for sid, desc, papel, chamadas, confere in SONDAS:
            try:
                passou = bool(confere(conversa(v, papel, chamadas)))
            except (KeyError, ValueError, IndexError, TypeError):
                passou = False
            ok += passou
            print(f"  {'✓' if passou else '✗'} {sid} {desc}")
        veredito = "GUARDADO" if ok == len(SONDAS) else "EXPOSTO"
        print(f"  {ok}/{len(SONDAS)} sondas  →  {veredito}")
        falhou |= ok != len(SONDAS)
    sys.exit(1 if falhou else 0)


if __name__ == "__main__":
    main()
