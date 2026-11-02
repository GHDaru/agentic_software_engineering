#!/usr/bin/env bash
# check-sumario.sh — livro/sumario.yaml × pastas do livro, nos DOIS sentidos:
#   1. todo slug do sumário (prefácio, capítulos, apêndices) tem pasta em livro/ (caixa exata);
#   2. toda pasta livro/NN-* e livro/apendices/* está no sumário;
#   3. coerência interna: slug sem repetição, capítulos numerados 1..N sem buraco, slug do
#      capítulo começa com o número (01-…), prefácio é 00-…, apêndice começa com a letra (a-…)
#      e as letras seguem A, B, C…
#   4. nenhuma chave desconhecida ou vazia numa entrada — pega o título com vírgula sem aspas
#      dentro de {...}: "titulo: Um humano, muitos agentes" vira titulo "Um humano" + chave
#      "muitos agentes" nula, e o título sai truncado sem erro nenhum.
# O sumário é a fonte única da ordem: o build (publicar/build.mjs) lê dele.
#
# Uso: scripts/check-sumario.sh      Saída: 0 = conforme · 1 = desvio · 2 = erro de ambiente.
set -euo pipefail
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
cd "$RAIZ"

PY=""
for c in "${PYTHON:-}" python py python3; do
  [ -n "$c" ] && "$c" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)' >/dev/null 2>&1 && { PY="$c"; break; }
done
[ -n "$PY" ] || { echo "✗ python 3.8+ não encontrado (no Git Bash, python3 é stub: use 'python')" >&2; exit 2; }
export PYTHONUTF8=1 PYTHONIOENCODING=utf-8

# YAML -> JSON: PyYAML se houver; senão o js-yaml do motor (publicar/node_modules).
if "$PY" -c 'import yaml' >/dev/null 2>&1; then
  JSON="$("$PY" -c 'import json,yaml; print(json.dumps(yaml.safe_load(open("livro/sumario.yaml",encoding="utf-8"))))')"
elif [ -d publicar/node_modules/js-yaml ]; then
  JSON="$(cd publicar && node -e 'const y=require("js-yaml"),f=require("fs");process.stdout.write(JSON.stringify(y.load(f.readFileSync("../livro/sumario.yaml","utf8"))))')"
else
  echo "✗ sem leitor de YAML: 'pip install pyyaml' ou 'cd publicar && npm install'" >&2; exit 2
fi

SUMARIO_JSON="$JSON" "$PY" - <<'PYEOF'
import json, os, re, sys
from pathlib import Path

s = json.loads(os.environ["SUMARIO_JSON"])
erros = []
declarados = []  # (slug, de onde)
CHAVES = {"prefácio": {"slug", "titulo"}, "capítulo": {"n", "slug", "titulo", "deriva"}, "apêndice": {"letra", "slug", "titulo"}}
def chaves(entrada, tipo, onde):
    for k, v in entrada.items():
        if k not in CHAVES[tipo]:
            erros.append(f"{onde}: chave desconhecida '{k}'" + (" (vírgula sem aspas no título? use titulo: \"…, …\")" if v is None else ""))
        elif v is None:
            erros.append(f"{onde}: '{k}' vazio")

pref = s.get("prefacio") or {}
if not pref.get("slug"): erros.append("sumário sem prefacio.slug")
else:
    declarados.append((pref["slug"], "prefácio")); chaves(pref, "prefácio", "prefácio")
    if not pref["slug"].startswith("00-"): erros.append(f"prefácio deveria ser 00-…: {pref['slug']}")

ns = []
for parte in s.get("partes") or []:
    caps = parte.get("capitulos") or []
    if not caps: erros.append(f"parte sem capítulos: {parte.get('nome')}")
    for c in caps:
        n, slug = c.get("n"), c.get("slug")
        if not isinstance(n, int) or not slug or not c.get("titulo"):
            erros.append(f"capítulo incompleto (n, slug, titulo): {c}"); continue
        ns.append(n); chaves(c, "capítulo", f"capítulo {n}")
        declarados.append((slug, f"capítulo {n}"))
        if not re.match(rf"^{n:02d}-[a-z0-9-]+$", slug):
            erros.append(f"capítulo {n}: slug deveria ser '{n:02d}-…' em minúsculas: {slug}")
if ns != list(range(1, len(ns) + 1)):
    erros.append(f"capítulos fora de sequência 1..{len(ns)}: {ns}")

for i, a in enumerate(s.get("apendices") or []):
    letra, slug = a.get("letra"), a.get("slug")
    if not letra or not slug or not a.get("titulo"):
        erros.append(f"apêndice incompleto (letra, slug, titulo): {a}"); continue
    declarados.append((slug, f"apêndice {letra}")); chaves(a, "apêndice", f"apêndice {letra}")
    if letra != chr(ord("A") + i): erros.append(f"apêndice {letra}: esperava a letra {chr(ord('A') + i)}")
    if not re.match(rf"^apendices/{letra.lower()}-[a-z0-9-]+$", slug):
        erros.append(f"apêndice {letra}: slug deveria ser 'apendices/{letra.lower()}-…': {slug}")

vistos = {}
for slug, onde in declarados:
    if slug in vistos: erros.append(f"slug repetido: {slug} ({vistos[slug]} e {onde})")
    vistos[slug] = onde

# Sentido 1: sumário -> pasta (comparação de nomes = caixa exata, mesmo no Windows).
pastas = {p.name for p in Path("livro").iterdir() if p.is_dir() and re.match(r"^\d{2}-", p.name)}
ap = Path("livro/apendices")
pastas |= {f"apendices/{p.name}" for p in ap.iterdir() if p.is_dir()} if ap.is_dir() else set()
for slug, onde in declarados:
    if slug not in pastas: erros.append(f"no sumário e SEM pasta: livro/{slug} ({onde})")
# Sentido 2: pasta -> sumário.
for p in sorted(pastas - set(vistos)):
    erros.append(f"pasta FORA do sumário: livro/{p}")

for e in erros: print(f"✗ {e}")
print(f"sumário: {len(declarados)} entrada(s) declaradas, {len(pastas)} pasta(s), {len(erros)} desvio(s)")
if erros: sys.exit(1)
print("✓ sumário OK")
PYEOF
