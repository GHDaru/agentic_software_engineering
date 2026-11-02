#!/usr/bin/env bash
# check-claims.sh — regra de evidência do guia editorial, nos dois sentidos, por capítulo
# (livro/NN-*/ e livro/apendices/*/):
#   1. todo [CLAIM-NN-NNN] citado no capitulo.md está registrado no claims.md da MESMA pasta;
#   2. todo claim registrado no claims.md (1ª coluna da tabela) é citado no capitulo.md;
#   3. id bem formado (CLAIM-NN-NNN), sem registro duplicado, e NN = número do capítulo
#      (nas pastas NN-*; apêndices não têm número).
# Citação = qualquer id dentro de colchetes: [CLAIM-03-001] ou [CLAIM-03-001, CLAIM-03-002].
# Blocos de código cercados (```) são ignorados no capitulo.md.
#
# Uso: scripts/check-claims.sh      Saída: 0 = conforme · 1 = desvio · 2 = erro de ambiente.
set -euo pipefail
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
cd "$RAIZ"

PY=""
for c in "${PYTHON:-}" python py python3; do
  [ -n "$c" ] && "$c" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)' >/dev/null 2>&1 && { PY="$c"; break; }
done
[ -n "$PY" ] || { echo "✗ python 3.8+ não encontrado (no Git Bash, python3 é stub: use 'python')" >&2; exit 2; }
export PYTHONUTF8=1 PYTHONIOENCODING=utf-8

"$PY" - <<'PYEOF'
import re, sys
from pathlib import Path

ID = re.compile(r"^CLAIM-(\d{2})-(\d{3})$")
TOKEN = re.compile(r"CLAIM-[A-Za-z0-9-]*[A-Za-z0-9]")

def sem_codigo(texto):
    out, cerca = [], None
    for linha in texto.splitlines():
        m = re.match(r"^\s{0,3}(`{3,}|~{3,})", linha)
        if m:
            marca = m.group(1)
            if cerca is None: cerca = marca
            elif marca[0] == cerca[0] and len(marca) >= len(cerca): cerca = None
            continue
        if cerca is None: out.append(linha)
    return "\n".join(out)

def citados(texto):
    ids = []
    for grupo in re.findall(r"\[([^\[\]]*CLAIM-[^\[\]]*)\]", sem_codigo(texto)):
        ids += TOKEN.findall(grupo)
    return ids

def registrados(texto):
    ids = []
    for linha in texto.splitlines():
        if not linha.lstrip().startswith("|"): continue
        celulas = linha.strip().strip("|").split("|")
        ids += TOKEN.findall(celulas[0]) if celulas else []
    return ids

pastas = sorted([p for p in Path("livro").glob("[0-9][0-9]-*") if p.is_dir()]
                + [p for p in Path("livro/apendices").glob("*") if p.is_dir()])
falhas, total_cit, total_reg, vistas = [], 0, 0, 0
for d in pastas:
    cap, cla = d / "capitulo.md", d / "claims.md"
    if not cap.exists() and not cla.exists(): continue
    vistas += 1
    nome = str(d).replace("\\", "/")
    erros = []
    c = citados(cap.read_text(encoding="utf-8")) if cap.exists() else []
    r = registrados(cla.read_text(encoding="utf-8")) if cla.exists() else []
    total_cit += len(set(c)); total_reg += len(r)
    for x in sorted(set(c) | set(r)):
        if not ID.match(x): erros.append(f"id malformado (esperado CLAIM-NN-NNN): {x}")
    nn = d.name[:2] if d.parent.name == "livro" else None
    if nn:
        for x in sorted(set(c) | set(r)):
            m = ID.match(x)
            if m and m.group(1) != nn: erros.append(f"{x}: NN deveria ser {nn} (número do capítulo)")
    dup = sorted({x for x in r if r.count(x) > 1})
    if dup: erros.append("registrado mais de uma vez no claims.md: " + ", ".join(dup))
    if c and not cla.exists(): erros.append("capitulo.md cita claims, mas não há claims.md")
    if r and not cap.exists(): erros.append("claims.md registra claims, mas não há capitulo.md que os cite")
    if cla.exists() and cap.exists():
        for x in sorted(set(c) - set(r)): erros.append(f"citado e NÃO registrado no claims.md: {x}")
        for x in sorted(set(r) - set(c)): erros.append(f"registrado e NÃO citado no capitulo.md: {x}")
    if erros: falhas.append((nome, erros))

for nome, erros in falhas:
    print(f"✗ {nome}")
    for e in erros: print(f"    {e}")
print(f"claims: {vistas} pasta(s) com texto, {total_cit} id(s) citado(s), {total_reg} registro(s), {len(falhas)} com desvio")
if falhas: sys.exit(1)
print("✓ claims OK")
PYEOF
