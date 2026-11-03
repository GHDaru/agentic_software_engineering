#!/usr/bin/env bash
# rodar.sh — o exemplo do capítulo 6 de ponta a ponta. Só Python 3 (biblioteca padrão).
# Uso:  bash rodar.sh                                 imprime a saída
#       bash rodar.sh | diff - saida-esperada.txt     confere contra a saída esperada
# Alguns passos SAEM 1 de propósito (o corte que colide, o paralelo que não compensa).
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

passo "1. corte por tela: o mesmo conceito ganha três donos"
rodar "$PY" dividir.py colisao planos/por-tela.json

passo "2. corte por quantidade: dois agentes no mesmo arquivo, e um contrato que ninguém escreve"
rodar "$PY" dividir.py colisao planos/por-quantidade.json

passo "3. corte por fronteira: cada arquivo e cada conceito com um dono"
rodar "$PY" dividir.py colisao planos/por-fronteira.json

passo "4. a ordem sai dos contratos: o dono antes de quem consome"
rodar "$PY" dividir.py ondas planos/por-fronteira.json

passo "5. quanto custa: o corte por tela e o por quantidade não pagam a coordenação"
rodar "$PY" dividir.py custo planos/por-tela.json
rodar "$PY" dividir.py custo planos/por-quantidade.json

passo "6. o corte por fronteira paga ... enquanto a passagem for barata"
rodar "$PY" dividir.py custo planos/por-fronteira.json
rodar "$PY" dividir.py custo planos/por-fronteira.json --handoff 4

passo "7. a menor autonomia que resolve, caso a caso"
rodar "$PY" dividir.py autonomia casos.json

passo "8. numerar em duas linhas paralelas: colisão de endereço e recusa"
rodar "$PY" dividir.py numerar linhas.json
