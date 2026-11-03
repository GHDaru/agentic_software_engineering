#!/usr/bin/env bash
# medir_maestro.sh — opcional: reproduz, num clone do Maestro, os números do capítulo 8.
# Só lê (git show / git ls-tree); não escreve nada no clone.
# Uso: bash medir_maestro.sh /caminho/do/clone/maestro [versão]   (versão padrão: 19823c2)
set -euo pipefail
M="${1:?informe o caminho do clone do Maestro}"; V="${2:-19823c2}"
g() { git -C "$M" "$@"; }
mod() { g show "$V:painel/servidor/dominio/model.yaml"; }

echo "== versão $V"
echo "-- plans com os quatro DOM:* (ciclos 067 em diante)"
for d in $(g ls-tree -d --name-only "$V" specs/ | grep -E 'specs/0(6[7-9]|7[0-9])-'); do
  if g cat-file -e "$V:$d/plan.md" 2>/dev/null; then
    n=$(g show "$V:$d/plan.md" | grep -oE 'DOM:(aggregate|invariants|glossary|ports)=' | sort -u | wc -l | tr -d ' ')
    echo "   $d: $n de 4"
  else
    echo "   $d: sem plan.md"
  fi
done
echo "-- piso do portão de domínio"
g show "$V:scripts/check-conformance.sh" | grep -E '^DOM_FLOOR(_DEFAULT)?=' | sed 's/^/   /'
echo "-- model.yaml"
echo "   contextos delimitados: $(mod | sed -n '/^contextos:/,/^invariantes:/p' | grep -cE '^  [a-z-]+:$')"
echo "   palavras proibidas na tela: $(mod | sed -n '/^proibidos:/,/^# ---/p' | grep -c '{termo:')"
echo "   linhas de mapa nas bordas: $(mod | grep -c 'um_para_um:') ($(mod | grep -c 'um_para_um: false') não 1:1)"
echo "   termos de agregado: $(mod | sed -n '/^  agregados:/,/^  conceitos:/p' | grep -c '{tela:') · conceitos: $(mod | sed -n '/^  conceitos:/,/^  papeis:/p' | grep -c '{tela:') · papéis de tela: $(mod | sed -n '/^  papeis:/,/^# ---/p' | grep -c '{tela:')"
echo "-- glossário da governança"
echo "   verbetes: $(g show "$V:docs/governance/glossary.md" | grep -c '^| \*\*')"
echo "-- achado 055 (linguagem ubíqua prometida e ausente)"
g show "$V:docs/records/decisoes.jsonl" | grep -oE '"id":"(achado-055-linguagem-ubiqua-prometida-e-ausente|retro-061-achado-055)","data":"[0-9-]+"' | sed 's/^/   /'
