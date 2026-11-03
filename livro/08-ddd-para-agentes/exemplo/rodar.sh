#!/usr/bin/env bash
# rodar.sh — o exemplo do capítulo 8 de ponta a ponta. Só Python 3 (biblioteca padrão) e bash.
# Uso:  bash rodar.sh                               imprime a saída
#       bash rodar.sh | diff - saida-esperada.txt   confere contra a saída esperada
# Vários passos SAEM 1 de propósito (é o vermelho que o capítulo descreve); o script não para neles.
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
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

passo "1. três sessões nomeiam a mesma tarefa: cada nome recebe REUSE, ALIAS, EXTEND ou CREATE"
rodar "$PY" catalogo.py decidir modelo.json propostas.json

passo "2. o texto de tela que a sessão A escreveu sem o catálogo"
rodar "$PY" catalogo.py lint modelo.json casos/tela-ruim.md

passo "3. o mesmo texto depois do catálogo"
rodar "$PY" catalogo.py lint modelo.json casos/tela-boa.md

passo "4. o plano que pulou o domínio (só diz 'usar DDD')"
rodar "$PY" catalogo.py plano casos/plan-sem-dom.md

passo "5. o plano que pôs uma regra na borda sem dizer por quê"
rodar "$PY" catalogo.py plano casos/plan-edge-sem-motivo.md

passo "6. o plano com as quatro declarações e o motivo da borda"
rodar "$PY" catalogo.py plano casos/plan-ok.md

passo "7. endereço: ambíguo ou morto é recusado, nunca adivinhado"
rodar "$PY" catalogo.py endereco sessoes.json "Gerente" "Gerente · loja" "Revisor · loja" "Revisor [0a0a0a] · loja"

passo "8a. o glossário gerado confere com o modelo"
rodar "$PY" catalogo.py glossario conferir modelo.json glossario-gerado.md

passo "8b. alguém 'corrige' o glossário à mão"
sed 's/Quem abre o chamado e recebe a resposta./Quem paga o contrato./' glossario-gerado.md > "$TMP/glossario-gerado.md"
rodar "$PY" catalogo.py glossario conferir modelo.json "$TMP/glossario-gerado.md"

passo "8c. alguém muda o modelo e não regera o glossário"
mkdir -p "$TMP/m"
sed 's/Data limite para pagar a fatura sem multa./Data limite para pagar sem juros./' modelo.json > "$TMP/m/modelo.json"
rodar "$PY" catalogo.py glossario conferir "$TMP/m/modelo.json" glossario-gerado.md

passo "9. as réguas discriminam? (fixture boa limpa, fixture ruim pega)"
rodar "$PY" catalogo.py mutacao modelo.json
