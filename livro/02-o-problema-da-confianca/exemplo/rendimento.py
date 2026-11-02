#!/usr/bin/env python3
"""rendimento.py — quanto a revisão independente mudou o resultado, ciclo a ciclo.

Lê veredictos-042-063.csv, uma linha por ciclo do Maestro (042–063, em maestro@19823c2):

  veredito_no_cabecalho  o que o cabeçalho do qa-report.md diz (escrito por quem executou)
  linha_tail_review      a linha do qa-report.md onde está a evidência de TAIL:review
  revisao                quando a revisão independente rodou, lido naquela evidência:
                         antes-do-gate | depois-da-promocao
  resultado              o que o parecer fez: reprovou | nao-mudou

A classificação vem do CORPO (a evidência de TAIL:review), não do cabeçalho. O cabeçalho
"aguardando parecer" é um estado transitório: o script conta quantas vezes ele contradiz o
corpo, para o leitor ver por que não serve de medida. Como reproduzir: README.md.

Rendimento = reprovou / revisões antes do gate. Cobertura = revisões antes do gate / total.
Só biblioteca padrão; Python 3.8+.
"""
import csv
import sys
from collections import Counter
from pathlib import Path

AQUI = Path(__file__).resolve().parent


def main():
    linhas = list(csv.DictReader((AQUI / "veredictos-042-063.csv").open(encoding="utf-8")))
    c = Counter()
    cabecalho_engana = []
    for l in linhas:
        c[(l["revisao"], l["resultado"])] += 1
        if "aguardando parecer" in l["veredito_no_cabecalho"].lower():
            cabecalho_engana.append(l["ciclo"][:3])
        print(f"  {l['ciclo'][:3]}  {l['revisao']:<18}  {l['resultado']:<9}  "
              f"(qa-report.md:{l['linha_tail_review']})")
    total = len(linhas)
    antes = c[("antes-do-gate", "reprovou")] + c[("antes-do-gate", "nao-mudou")]
    depois = c[("depois-da-promocao", "reprovou")] + c[("depois-da-promocao", "nao-mudou")]
    reprovou_antes = c[("antes-do-gate", "reprovou")]
    reprovou = reprovou_antes + c[("depois-da-promocao", "reprovou")]
    print(f"\nciclos: {total} · revisão antes do gate: {antes} · revisão só depois da promoção: {depois}")
    print(f"rendimento da revisão antes do gate: {reprovou_antes}/{antes} = {100 * reprovou_antes / antes:.1f}%")
    print(f"cobertura da revisão antes do gate: {antes}/{total} = {100 * antes / total:.1f}%")
    print(f"ciclos reprovados por um parecer, em qualquer momento: {reprovou}/{total} = {100 * reprovou / total:.1f}%")
    print(f"cabeçalho 'aguardando parecer' com parecer no corpo: {len(cabecalho_engana)} "
          f"({', '.join(cabecalho_engana)})")
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
