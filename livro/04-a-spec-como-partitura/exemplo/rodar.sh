#!/usr/bin/env bash
# rodar.sh — o exemplo do capítulo 4 de ponta a ponta. Só Python 3 (biblioteca padrão).
# Uso:  bash rodar.sh                 imprime a saída
#       bash rodar.sh | diff - saida-esperada.txt   confere contra a saída esperada
# Alguns passos SAEM 1 de propósito (a spec vaga, a spec que andou); o script não para neles.
set -uo pipefail
cd "$(dirname "$0")"

PY=""
for c in "${PYTHON:-}" python3 python py; do
  [ -n "$c" ] && "$c" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)' >/dev/null 2>&1 && { PY="$c"; break; }
done
[ -n "$PY" ] || { echo "✗ python 3.8+ não encontrado" >&2; exit 2; }
export PYTHONUTF8=1 PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1

passo() { echo; echo "== $1"; }
rodar() { "$@"; echo "(exit $?)"; }

passo "1. a spec aprovada passa no lint (todo requisito é verificável)"
rodar "$PY" partitura.py lint spec.md

passo "2. a mesma intenção escrita como prompt: três desejos e um requisito"
rodar "$PY" partitura.py lint casos/spec-vaga.md

passo "3. cada requisito tem teste, e nenhum teste existe sem requisito"
rodar "$PY" partitura.py rastreio spec.md test_frete.py

passo "4. os testes leem o limite DA SPEC e passam"
SPEC=spec.md rodar "$PY" test_frete.py

passo "5. a spec muda primeiro (v2): o rastreio acusa o requisito novo sem teste"
rodar "$PY" partitura.py rastreio casos/spec-v2.md test_frete.py

passo "6. ... e os testes ficam vermelhos até o código seguir a spec"
SPEC=casos/spec-v2.md rodar "$PY" test_frete.py

passo "7. quanto processo cada mudança merece (ambiguidade × raio × irreversibilidade)"
rodar "$PY" partitura.py raia mudancas.json
