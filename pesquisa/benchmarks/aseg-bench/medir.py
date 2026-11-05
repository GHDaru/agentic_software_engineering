#!/usr/bin/env python3
"""medir.py — a mensuração do ASEG-Bench: lê `pesquisa/runs/` e escreve a tabela de resultados.

Por célula (caso × braço × modelo), segundo o protocolo 0.1 §2:
  n válidos, erros do harness (relatados, fora da métrica), tarefa resolvida,
  conformidade inteira e só de estado — proporção com intervalo de Wilson a 95 %;
  aceitação na primeira passada (resolvida E conforme);
  custo, tokens de saída e tempo — mediana, mínimo e máximo.
Por braço, o agregado dos casos; e o contraste T − A na conformidade só de estado, com intervalo
bootstrap pareado por caso (10 000 reamostragens, semente registrada).

Uma conformidade sem resolução é aprovação vazia: o agente que não faz nada não viola nada. Por
isso a coluna que o livro cita é a **aceitação** (resolvida e conforme), não a conformidade sozinha.

Uso:
  python medir.py                       # escreve resultados.md ao lado e imprime o resumo
  python medir.py --runs <dir> --saida <arquivo.md> --semente 7
Saída 0 sempre que a leitura dá certo (medir não é portão); 2 em erro de uso.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import statistics
import sys
from collections import defaultdict
from pathlib import Path

AQUI = Path(__file__).resolve().parent
LIVRO = AQUI.parents[2]


def wilson(k: int, n: int, z: float = 1.959964) -> tuple[float, float]:
    if n == 0:
        return (math.nan, math.nan)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - m), min(1.0, c + m))


def prop(k: int, n: int) -> str:
    if n == 0:
        return "—"
    lo, hi = wilson(k, n)
    return f"{k}/{n} ({100 * k / n:.0f} %; {100 * lo:.0f}–{100 * hi:.0f})"


def mediana(xs: list) -> str:
    xs = [x for x in xs if isinstance(x, (int, float))]
    if not xs:
        return "—"
    f = (lambda v: f"{v:.3g}")
    return f"{f(statistics.median(xs))} [{f(min(xs))}–{f(max(xs))}]"


def carregar(runs: Path) -> list[dict]:
    out = []
    for p in sorted(runs.glob("*/run.json")):
        r = json.loads(p.read_text(encoding="utf-8"))
        if r.get("hipotese") == "ASEG" and r.get("schema") == 1:
            out.append(r)
    return out


def contraste(runs: list[dict], b1: str, b0: str, chave: str, semente: int, reps: int = 10000):
    """Diferença b1 − b0 na proporção `chave`, pareada por caso; bootstrap sobre os casos."""
    por = defaultdict(lambda: {b0: [], b1: []})
    for r in runs:
        if r["erro_do_harness"] is None and r["braco"] in (b0, b1):
            por[r["tarefa"]][r["braco"]].append(bool(r["metricas"][chave]))
    casos = [c for c, v in por.items() if v[b0] and v[b1]]
    if not casos:
        return None
    dif = {c: statistics.mean(por[c][b1]) - statistics.mean(por[c][b0]) for c in casos}
    ponto = statistics.mean(dif.values())
    rng = random.Random(semente)
    amostras = sorted(statistics.mean(dif[rng.choice(casos)] for _ in casos) for _ in range(reps))
    return ponto, amostras[int(0.025 * reps)], amostras[int(0.975 * reps) - 1], len(casos)


def tabela(runs: list[dict], semente: int) -> str:
    cel = defaultdict(list)
    for r in runs:
        cel[(r["tarefa"], r["braco"], r["modelo"]["pedido"])].append(r)
    L = ["# ASEG-Bench — resultados medidos", "",
         f"Gerado por `medir.py` a partir de `pesquisa/runs/` · protocolo 0.1 · {len(runs)} run(s) · "
         f"semente do bootstrap {semente}.", "",
         "Proporções: k/n (taxa; intervalo de Wilson a 95 %). Contínuas: mediana [mín–máx]. "
         "Erros do harness ficam fora de n e são relatados à parte.", "",
         "| caso | braço | modelo | n | erros harness | resolvida | conforme (inteiro) | conforme (só estado) | **aceita** | custo US$ | tokens saída | tempo s |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for (c, b, m), rs in sorted(cel.items()):
        ok = [r for r in rs if r["erro_do_harness"] is None]
        n = len(ok)
        k = lambda ch: sum(1 for r in ok if r["metricas"][ch])
        modelos = sorted({r["modelo"]["resolvido"] or "?" for r in ok})
        L.append(f"| {c} | {b} | {m} ({', '.join(modelos)}) | {n} | {len(rs) - n} | {prop(k('tarefa_resolvida'), n)} | "
                 f"{prop(k('conforme'), n)} | {prop(k('conforme_so_estado'), n)} | **{prop(k('aceita_primeira_passada'), n)}** | "
                 f"{mediana([r['metricas']['custo'] for r in ok])} | {mediana([r['metricas']['tokens_saida'] for r in ok])} | "
                 f"{mediana([r['metricas']['tempo_s'] for r in ok])} |")
    L += ["", "## Por braço (todos os casos)", "",
          "| braço | n | erros harness | resolvida | conforme (só estado) | **aceita** |", "|---|---|---|---|---|---|"]
    por_b = defaultdict(list)
    for r in runs:
        por_b[r["braco"]].append(r)
    for b, rs in sorted(por_b.items()):
        ok = [r for r in rs if r["erro_do_harness"] is None]
        k = lambda ch: sum(1 for r in ok if r["metricas"][ch])
        L.append(f"| {b} | {len(ok)} | {len(rs) - len(ok)} | {prop(k('tarefa_resolvida'), len(ok))} | "
                 f"{prop(k('conforme_so_estado'), len(ok))} | **{prop(k('aceita_primeira_passada'), len(ok))}** |")
    L += ["", "## Contrastes (pareados por caso, bootstrap 95 %)", ""]
    bracos = sorted(por_b)
    feitos = False
    for b1, b0 in [("B", "A"), ("C", "B"), ("T", "C"), ("T", "A")]:
        if b1 in bracos and b0 in bracos:
            for ch in ("aceita_primeira_passada", "conforme_so_estado"):
                c = contraste(runs, b1, b0, ch, semente)
                if c:
                    feitos = True
                    p, lo, hi, nc = c
                    L.append(f"- **{b1} − {b0}**, {ch}: {100 * p:+.0f} pontos ({100 * lo:+.0f} a {100 * hi:+.0f}), {nc} caso(s)"
                             + (" — o intervalo inclui zero: sem efeito demonstrado" if lo <= 0 <= hi else ""))
    if not feitos:
        L.append("- nenhum par de braços com runs válidos no mesmo caso.")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--runs", default=str(LIVRO / "pesquisa" / "runs"))
    ap.add_argument("--saida", default=str(AQUI / "resultados.md"))
    ap.add_argument("--semente", type=int, default=0)
    a = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    runs = carregar(Path(a.runs))
    md = tabela(runs, a.semente)
    Path(a.saida).write_text(md, encoding="utf-8")
    print(md)


if __name__ == "__main__":
    main()
