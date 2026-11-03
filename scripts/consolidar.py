"""Consolida o livro: glossário único, CLAIMS.md único e relatório de cobertura do inventário.

Uso: python scripts/consolidar.py   (da raiz do repositório)
Saídas: livro/glossario.md, pesquisa/CLAIMS.md, pesquisa/inventario/cobertura.md
Sai com 1 se algum item do inventário não estiver em nenhum cobertura.md.
"""
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
LIVRO = RAIZ / "livro"
PASTAS = sorted([p for p in LIVRO.iterdir() if p.is_dir() and p.name[:2].isdigit()]) + sorted(
    p for p in (LIVRO / "apendices").iterdir() if p.is_dir())


def linhas_de_tabela(texto):
    for linha in texto.splitlines():
        linha = linha.strip()
        if linha.startswith("|") and not re.match(r"^\|[\s:|-]+\|$", linha):
            yield [c.strip() for c in linha.strip("|").split("|")]


def rotulo(pasta):
    return pasta.name if pasta.parent == LIVRO else "apêndice " + pasta.name[0].upper()


# Glossário: termo -> (definição, onde nasceu); a primeira definição vence.
termos = {}
for pasta in PASTAS:
    g = pasta / "glossario.md"
    if not g.exists():
        continue
    for cel in linhas_de_tabela(g.read_text(encoding="utf-8")):
        if len(cel) < 2 or cel[0].lower() in ("termo", "sigla"):
            continue
        chave = re.sub(r"[*_`]", "", cel[0]).strip()
        if chave and chave.lower() not in {k.lower() for k in termos}:
            termos[chave] = (cel[1], rotulo(pasta))
out = ["# Glossário", "", f"Consolidado dos glossários dos capítulos ({len(termos)} termos). "
       "Gerado por `scripts/consolidar.py` — não edite à mão.", "",
       "| Termo | Definição | Nasce em |", "|---|---|---|"]
for t in sorted(termos, key=str.lower):
    d, onde = termos[t]
    out.append(f"| {t} | {d} | {onde} |")
(LIVRO / "glossario.md").write_text("\n".join(out) + "\n", encoding="utf-8")

# Claims: concatena as tabelas, preservando o cabeçalho de cada capítulo.
claims = ["# Evidências (CLAIMS)", "",
          "Toda afirmação quantitativa do livro tem um id aqui. Estados: `medido`, `observado`, "
          "`hipótese`. Gerado por `scripts/consolidar.py` a partir de `livro/*/claims.md`.", ""]
total = 0
for pasta in PASTAS:
    c = pasta / "claims.md"
    if not c.exists():
        continue
    linhas = [l for l in c.read_text(encoding="utf-8").splitlines() if l.strip().startswith("|")]
    n = sum(1 for l in linhas if "CLAIM-" in l)
    total += n
    claims += [f"## {rotulo(pasta)} ({n})", ""] + linhas + [""]
claims.insert(4, f"Total: {total} claims.\n")
(RAIZ / "pesquisa" / "CLAIMS.md").write_text("\n".join(claims) + "\n", encoding="utf-8")

# Cobertura: todo item do inventário aparece em algum cobertura.md (ou no texto).
itens = json.loads((RAIZ / "pesquisa/inventario/itens.json").read_text(encoding="utf-8"))
coberto = {}
for pasta in PASTAS:
    blob = ""
    for nome in ("cobertura.md", "capitulo.md"):
        f = pasta / nome
        if f.exists():
            blob += f.read_text(encoding="utf-8")
    for i in itens:
        if re.search(rf"\b{re.escape(i['id'])}\b", blob):
            coberto.setdefault(i["id"], []).append(rotulo(pasta))
faltam = [i for i in itens if i["id"] not in coberto]
rel = ["# Cobertura do inventário", "", f"{len(itens) - len(faltam)} de {len(itens)} itens cobertos "
       f"({100 * (len(itens) - len(faltam)) / len(itens):.1f}%). Gerado por `scripts/consolidar.py`.", ""]
if faltam:
    rel += ["## Itens sem cobertura", "", "| id | capítulo principal | resumo |", "|---|---|---|"]
    rel += [f"| {i['id']} | {i['capitulos'][0]} | {i['resumo'][:140].replace('|', '/')} |" for i in faltam]
(RAIZ / "pesquisa/inventario/cobertura.md").write_text("\n".join(rel) + "\n", encoding="utf-8")

print(f"glossário: {len(termos)} termos · claims: {total} · cobertura: "
      f"{len(itens) - len(faltam)}/{len(itens)}")
sys.exit(1 if faltam else 0)
