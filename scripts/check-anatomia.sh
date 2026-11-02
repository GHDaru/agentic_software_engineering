#!/usr/bin/env bash
# check-anatomia.sh — todo capitulo.md dos capítulos 01..16 (o prefácio fica de fora) tem
# as 11 seções "## " da anatomia, com os títulos e na ordem de livro/guia-editorial.md,
# e nenhuma outra seção de nível 2. Também confere a abertura "# NN — Título".
# A lista das 11 seções é LIDA do guia (fonte única), não copiada aqui.
#
# Uso: scripts/check-anatomia.sh [--estrito]
#   --estrito  capítulo do sumário ainda sem capitulo.md também reprova
#              (sem a flag, aparece como "em escrita" e não reprova).
# Saída: 0 = conforme · 1 = desvio · 2 = erro de ambiente/guia.
set -euo pipefail
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
cd "$RAIZ"

PY=""
for c in "${PYTHON:-}" python py python3; do
  [ -n "$c" ] && "$c" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)' >/dev/null 2>&1 && { PY="$c"; break; }
done
[ -n "$PY" ] || { echo "✗ python 3.8+ não encontrado (no Git Bash, python3 é stub: use 'python')" >&2; exit 2; }
export PYTHONUTF8=1 PYTHONIOENCODING=utf-8

"$PY" - "$@" <<'PYEOF'
import re, sys
from pathlib import Path

estrito = "--estrito" in sys.argv[1:]
guia = Path("livro/guia-editorial.md").read_text(encoding="utf-8")
secoes = re.findall(r"^\s*\d+\.\s+`## ([^`]+)`", guia, re.M)
if len(secoes) != 11:
    print(f"✗ guia-editorial.md: esperava 11 seções na anatomia, achei {len(secoes)}: {secoes}")
    sys.exit(2)

def titulos(texto):
    """(nível, título) dos cabeçalhos ATX fora de bloco de código cercado."""
    out, cerca = [], None
    for linha in texto.splitlines():
        m = re.match(r"^\s{0,3}(`{3,}|~{3,})", linha)
        if m:
            marca = m.group(1)
            if cerca is None: cerca = marca[0] * len(marca)
            elif marca[0] == cerca[0] and len(marca) >= len(cerca): cerca = None
            continue
        if cerca: continue
        h = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", linha)
        if h: out.append((len(h.group(1)), h.group(2).strip()))
    return out

caps = sorted(p for p in Path("livro").glob("[0-9][0-9]-*") if p.is_dir() and p.name[:2] != "00")
falhas, ok, pendentes = [], 0, []
for d in caps:
    n = d.name[:2]
    if not (1 <= int(n) <= 16): continue
    arq = d / "capitulo.md"
    if not arq.exists():
        pendentes.append(d.name); continue
    hs = titulos(arq.read_text(encoding="utf-8"))
    erros = []
    h1 = [t for nv, t in hs if nv == 1]
    if not h1 or not re.match(rf"^{n} — \S", h1[0]):
        erros.append(f"abertura deve ser '# {n} — Título' (achei: {h1[0] if h1 else 'nenhum # título'})")
    h2 = [t for nv, t in hs if nv == 2]
    if h2 != secoes:
        faltam = [x for x in secoes if x not in h2]
        sobram = [x for x in h2 if x not in secoes]
        repetidas = sorted({x for x in h2 if x in secoes and h2.count(x) > 1})
        comuns = [x for x in h2 if x in secoes]
        if faltam: erros.append("faltam: " + "; ".join(faltam))
        if sobram: erros.append("seções '## ' fora da anatomia (use '###'): " + "; ".join(sobram))
        if repetidas: erros.append("seção repetida: " + "; ".join(repetidas))
        if not repetidas and comuns != [x for x in secoes if x in comuns]:
            erros.append("ordem errada: " + " → ".join(comuns))
    if erros:
        falhas.append((str(arq).replace("\\", "/"), erros))
    else:
        ok += 1

for arq, erros in falhas:
    print(f"✗ {arq}")
    for e in erros: print(f"    {e}")
print(f"anatomia: {ok} conforme(s), {len(falhas)} com desvio, {len(pendentes)} em escrita"
      + (f" ({', '.join(pendentes)})" if pendentes and estrito else ""))
if falhas or (estrito and pendentes):
    sys.exit(1)
print("✓ anatomia OK")
PYEOF
