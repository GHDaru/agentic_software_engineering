# Estado do livro — v1 (03/11/2026)

Primeira versão completa: prefácio, 16 capítulos e 4 apêndices, escritos por agentes e julgados
por um crítico independente em contexto fresco (o mesmo princípio que o livro defende).

| Portão | Resultado |
|---|---|
| `scripts/check-anatomia.sh` | 16 capítulos com as 11 seções, na ordem |
| `scripts/check-claims.sh` | 641 claims citados = 641 registrados |
| `scripts/check-sumario.sh` | 21 entradas do sumário = 21 pastas |
| `scripts/consolidar.py` | cobertura do inventário: **841/841** itens; glossário de 429 termos |
| `publicar/build.mjs` | site em `docs/`, links internos OK |

## Veredito do crítico por texto

| Texto | Veredito |
|---|---|
| Capítulos 1–13, apêndice D | **aprovado** pelo crítico independente |
| Prefácio, capítulos 14, 15, 16, apêndices A e C | reprovado na 1ª crítica; **revisado** contra cada lacuna, sem 2ª crítica (limite de créditos) |
| Apêndice B (ASEG-Bench) | reprovado; lacunas declaradas no texto — nenhum caso foi rodado contra um agente real, e GOV-007 tem origem fraca |

## Pendências conhecidas

- **Links para o Maestro em `19823c2`** não resolvem no GitHub: esse commit existe só na branch
  local `066-painel-de-regencia` do Maestro (o remoto está em `566bca5`). Resolve com um push
  daquela branch no repositório do Maestro.
- **Apêndice B** precisa de execuções reais dos dez casos para virar evidência, não só instrumento.
- **Segunda crítica** dos textos revisados (prefácio, 14, 15, 16, A, C).

Inventário de cobertura: `pesquisa/inventario/` · evidências: `pesquisa/CLAIMS.md` ·
contrato de escrita: `guia-editorial.md` · ordem: `sumario.yaml`.
