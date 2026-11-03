#!/usr/bin/env bash
# rodar.sh — o exemplo do capítulo 5 de ponta a ponta. Só Python 3.8+ (biblioteca padrão).
# Uso:  bash rodar.sh                               imprime a saída
#       bash rodar.sh | diff - saida-esperada.txt   confere contra a saída esperada
# Vários passos SAEM 1 de propósito: são as falhas que o capítulo descreve. O script segue.
# Nada no projeto/ é alterado: o registro de decisão e a correção da instrução rodam em cópias
# temporárias.
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

passo "1. seleção: uma tarefa cortada pela fronteira carrega pouco do repositório"
rodar "$PY" contexto.py selecionar projeto 007 T2

passo "2. seleção: a tarefa que atravessa o código inteiro — economia baixa é sinal de corte errado"
rodar "$PY" contexto.py selecionar projeto 007 T4

passo "3. seleção: a tarefa que não cita nada manda o executor procurar sozinho"
rodar "$PY" contexto.py selecionar projeto 007 T3

passo "4. compressão: a janela compacta e só o tasks.md fica — a cauda morava na spec e na conversa"
rodar "$PY" contexto.py compactar projeto 007 --conversa casos/conversa.md

passo "5. compressão: a mesma janela, com a cauda como token no tasks.md"
rodar "$PY" contexto.py compactar projeto 007 --tasks casos/tasks-com-cauda.md --conversa casos/conversa.md

passo "6. persistência: acrescentar uma decisão (numa cópia do índice)"
cp projeto/registros/decisoes.jsonl "$TMP/decisoes.jsonl"
rodar "$PY" contexto.py registrar "$TMP/decisoes.jsonl" '{"id": "achado-007-fecha-006", "fecha": "achado-006-mensagem-sem-data", "data": "2026-09-06", "titulo": "Fechado: a mensagem traz a data", "status": "fechada", "registro": "specs/007-cupom-de-desconto/qa-report.md"}'

passo "7. persistência: o mesmo id de novo, e um registro que aponta para um marcador"
rodar "$PY" contexto.py registrar "$TMP/decisoes.jsonl" '{"id": "achado-006-mensagem-sem-data", "data": "2026-09-06", "titulo": "corrigido", "status": "fechada", "registro": "specs/007-cupom-de-desconto/qa-report.md"}'
rodar "$PY" contexto.py registrar "$TMP/decisoes.jsonl" '{"id": "achado-007-x", "data": "2026-09-06", "titulo": "x", "status": "aberta", "registro": "<pendente>"}'

passo "8. persistência: o índice com uma linha acrescentada × o índice com uma linha reescrita"
rodar "$PY" contexto.py historico projeto/registros/decisoes.jsonl "$TMP/decisoes.jsonl"
rodar "$PY" contexto.py historico projeto/registros/decisoes.jsonl casos/decisoes-reescrito.jsonl

passo "9. transferência: CLAUDE.md e AGENTS.md escritos à mão, contra as skills do disco"
rodar "$PY" contexto.py transferir projeto

passo "10. transferência: fonte única e bloco gerado do disco (numa cópia temporária)"
rodar "$PY" contexto.py transferir projeto --corrigir

passo "11. rastreabilidade: do gate ao porquê, de trás para frente"
rodar "$PY" contexto.py rastrear projeto gate-main-b7e41c2

passo "12. o quadro: as quatro operações do ciclo 007 numa tela"
rodar "$PY" contexto.py inspecionar projeto 007
