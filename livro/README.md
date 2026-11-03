# Estado do livro — v1 (03/11/2026)

Primeira versão completa: prefácio, 16 capítulos e 4 apêndices, escritos por agentes e julgados
por um crítico independente em contexto fresco (o mesmo princípio que o livro defende).

| Portão | Resultado |
|---|---|
| `scripts/check-anatomia.sh` | 16 capítulos com as 11 seções, na ordem |
| `scripts/check-claims.sh` | 646 claims citados = 646 registrados |
| `scripts/check-sumario.sh` | 21 entradas do sumário = 21 pastas |
| `scripts/consolidar.py` | cobertura do inventário: **841/841** itens; glossário de 429 termos |
| `publicar/build.mjs` | site em `docs/`, links internos OK |

## Veredito do crítico por texto

| Texto | Veredito |
|---|---|
| Capítulos 1–13, apêndice D | **aprovado** pelo crítico independente |
| Prefácio, capítulos 14, 15, 16, apêndices A e C | reprovado na 1ª crítica, revisado e **aprovado na 2ª crítica** (03/11; 15, 16 e A após mais uma revisão); lacunas menores apontadas corrigidas à mão |
| Apêndice B (ASEG-Bench) | reprovado; lacunas declaradas no texto — nenhum caso foi rodado contra um agente real, e GOV-007 tem origem fraca |

## Pendências conhecidas

- **Links para o Maestro em `19823c2`**: resolvidos em 03/11 — o *commit* foi publicado na branch `livro-ref-19823c2` do Maestro. Uma *tag* anotada seria âncora mais firme.
- **Apêndice B** precisa de execuções reais dos dez casos para virar evidência, não só instrumento.
- **Folga de tamanho**: capítulos 14 e 15 estão no teto de 8.000 palavras; nenhum portão mede isso.

Inventário de cobertura: `pesquisa/inventario/` · evidências: `pesquisa/CLAIMS.md` ·
contrato de escrita: `guia-editorial.md` · ordem: `sumario.yaml`.
