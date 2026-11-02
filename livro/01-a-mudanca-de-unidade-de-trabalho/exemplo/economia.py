#!/usr/bin/env python3
"""economia.py - custo por mudanca ACEITA quando gerar fica barato.

Modelo de valor esperado (deterministico, sem sorteio), por mudanca:
  gerar     = g * (1 + p*d)        # gera de novo o que a verificacao recusou
  verificar = v * (1 + p*d)        # e verifica de novo
  desfazer  = p * (1 - d) * u * b  # o erro que escapou arrasta o lote inteiro
  total     = gerar + verificar + desfazer

Uso:
  python economia.py                 imprime a tabela
  python economia.py --conferir      compara com saida-esperada.txt (0 = bate, 1 = diverge)
  python economia.py --cenarios X    usa outro arquivo de parametros
So biblioteca padrao. Python 3.8+.
"""
import json
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent


def custo(c):
    refaz = 1 + c["p"] * c["d"]
    gerar = c["g"] * refaz
    verificar = c["v"] * refaz
    desfazer = c["p"] * (1 - c["d"]) * c["u"] * c["b"]
    return gerar, verificar, desfazer, gerar + verificar + desfazer


def relatorio(dados):
    linhas = []
    linhas.append("CUSTO POR MUDANCA ACEITA (horas-equivalentes; parametros ilustrativos)")
    linhas.append("")
    linhas.append(f"{'':2} {'cenario':40} {'gerar':>6} {'verif':>6} {'desf':>6} {'total':>6} {'%gerar':>7}")
    tot = {}
    for c in dados["cenarios"]:
        g, v, u, t = custo(c)
        tot[c["id"]] = t
        linhas.append(f"{c['id']:2} {c['nome']:40} {g:6.2f} {v:6.2f} {u:6.2f} {t:6.2f} {100*g/t:6.1f}%")
    linhas.append("")
    a, d = dados["cenarios"][0], next(c for c in dados["cenarios"] if c["id"] == "D")
    linhas.append(f"gerar ficou {a['g']/d['g']:.0f}x mais barato (A -> D); "
                  f"o total caiu {tot['A']/tot['D']:.1f}x.")
    linhas.append(f"sem verificacao (B) o total e {tot['B']/tot['A']:.1f}x o do humano digitando (A).")
    linhas.append("")
    s = dados["sensibilidade"]
    base = next(c for c in dados["cenarios"] if c["id"] == s["base"])
    linhas.append(f"SENSIBILIDADE: o cenario {s['base']} com g variando")
    for g in s["g"]:
        c = dict(base, g=g)
        _, _, _, t = custo(c)
        linhas.append(f"  g = {g:5.2f}  ->  total = {t:5.2f}")
    piso = custo(dict(base, g=0.0))[3]
    linhas.append(f"  piso (g = 0) = {piso:.2f}: o que sobra e verificar e desfazer.")
    return "\n".join(linhas) + "\n"


def main(argv):
    arq = AQUI / "cenarios.json"
    if "--cenarios" in argv:
        arq = Path(argv[argv.index("--cenarios") + 1])
    dados = json.loads(arq.read_text(encoding="utf-8"))
    saida = relatorio(dados)
    if "--conferir" in argv:
        esperado = (AQUI / "saida-esperada.txt").read_text(encoding="utf-8")
        if saida == esperado:
            print("OK: a saida bate com saida-esperada.txt")
            return 0
        print("DIVERGE de saida-esperada.txt:")
        for i, (x, y) in enumerate(zip(saida.splitlines(), esperado.splitlines()), 1):
            if x != y:
                print(f"  linha {i}\n    obtido:   {x}\n    esperado: {y}")
        return 1
    sys.stdout.write(saida)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
