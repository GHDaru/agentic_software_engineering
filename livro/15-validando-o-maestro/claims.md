# Claims do capítulo 15

Regra do guia editorial: todo número do texto leva um id; cada id tem estado e evidência
reproduzível. Caminhos sem outra indicação são do Maestro em `19823c2`
(`git -C <maestro> show 19823c2:<caminho>`).

| id | afirmação | estado | evidência reproduzível |
|---|---|---|---|
| CLAIM-15-001 | Durante 36 ciclos, 13 agentes operaram sem linha de base de avaliação. | observado | `docs/governance/axioms.md`, teorema T7, bloco "Evidence"; `specs/037-evals-linha-de-base/spec.md` |
| CLAIM-15-002 | O ciclo 037 (06/08/2026) entregou `check-evals.sh` vermelho de propósito, com os dois casos-semente nunca executados. | observado | `docs/records/decisoes.jsonl` id `achado-037-linhas-de-base-pendentes`; `specs/037-evals-linha-de-base/qa-report.md` |
| CLAIM-15-003 | Em 07/08/2026 o caso 001 passou com 6 de 6 asserções no alvo real (uma marcada "borderline"; dois defeitos de redação achados no próprio caso) e o alvo ablado — sem a instrução de comparar com o plano **e com o plano retido** — reprovou o caso. | observado | `evals/001-review-drops-a-requirement/baseline.md` (campos `Verdict`, `Ablation`, `First-red`; tabela do "Run 1", linha MUST-NOT-CLAIM #3 "borderline"; "Run 2", frase "and with the plan withheld"; "What running it changed in the case") |
| CLAIM-15-004 | O caso 002 foi escrito duas vezes e rodado quatro vezes; o alvo ablado passou nas duas fixtures. | observado | `evals/002-guardian-accepts-a-wrong-lane/baseline.md` ("Why this stays pending", campo `Ablation`); `decisoes.jsonl` id `achado-040-caso-002-nao-discrimina` |
| CLAIM-15-005 | Duas fixtures escritas à mão, dois defeitos achados pelos agentes avaliados (conclusão no enunciado; premissa falsa). | observado | `decisoes.jsonl` id `achado-040-fixtures-com-defeito`; `evals/002-guardian-accepts-a-wrong-lane/baseline.md`, "The defect the ablated target found in the fixture" |
| CLAIM-15-006 | As rodadas de avaliação foram commitadas citando o ciclo 040, sem pasta `specs/040-*`; o `check-cycle.sh` pegou. | observado | `decisoes.jsonl` id `achado-041-ciclo-040-sem-spec`; `ls specs/ \| grep ^040` (vazio) |
| CLAIM-15-007 | A retro do ciclo 041 fechou quatro achados: anti-padrões 19 e 20, campos `Axis`, `Ablation` e `Premise-checked`, caso 002 aposentado. | observado | `decisoes.jsonl` ids `retro-041-fecha-037`, `retro-041-fecha-040a`, `retro-041-fecha-040b`; `specs/041-retro-dos-quatro-achados-de-eval/qa-report.md`; `skills/anti-patterns/SKILL.md` itens 19–20 |
| CLAIM-15-008 | A única ocorrência de *judge* em `scripts/` era o comentário de `check-cycle.sh:8` admitindo que o portão não julga a resposta. | observado | `docs/governance/axioms.md`, teorema T7, bloco "Evidence" (afirmação datada do ciclo 037; não remedida em `19823c2`) |
| CLAIM-15-009 | A agenda de pesquisa do livro tem dez hipóteses (H1–H10) e quatro níveis de tratamento (A prompt, B spec, C spec + gates, Maestro completo). | observado | livro: `pesquisa/base-de-pesquisa.md`, seção "Agenda de pesquisa" (linhas 39–47) |
| CLAIM-15-010 | No ciclo 042, 35 de 40 `tasks.md` tinham perdido o gate humano que o template carregava. | observado | `specs/042-conformidade-executavel/spec.md` linha 23 (tabela de medição); `skills/anti-patterns/SKILL.md` item 22 |
| CLAIM-15-011 | Em quatro ciclos seguidos (057–060) as caixas `TAIL` foram marcadas sem `qa-report.md`, e só a revisão humana pegou. | observado | `.github/workflows/ci.yml` comentário do passo "A ticked box has its evidence (blocking)"; `scripts/check-conformance.sh` cabeçalho ("Why --ticked-only exists") |
| CLAIM-15-012 | O exemplo do capítulo, rodado em 02/11/2026, reporta 3 casos, 1 saudável, 0 aposentados, e sai com código 1. | medido | `cd livro/15-validando-o-maestro/exemplo && python avaliar.py; echo $?` |
| CLAIM-15-013 | Na primeira execução (ciclo 021), o `check-install.sh` achou três derivas com uma causa: listas escritas à mão que ninguém comparava com o disco. | observado | `specs/021-maestro-instalado-no-maestro/qa-report.md`, "Achados" item 1; `docs/roadmap.md` linha F10 |
| CLAIM-15-014 | No ciclo 016 as nove seções do capítulo 01 do guia foram contadas à mão; o `check-chapters.sh` nasceu disso (ciclo 022). | observado | `scripts/check-chapters.sh`, cabeçalho (linhas 1–9) |
| CLAIM-15-015 | Com 28 ciclos, 26 tinham os quatro artefatos completos; os dois restantes eram os ciclos abertos. | observado | livro: `maestro-handbook/handbook/08-entregaveis-artefatos.md` §6 (linhas ~128–131) |
| CLAIM-15-016 | No ciclo 042, zero de quarenta ciclos tinha produzido artefato condicional (research, data-model, contracts, checklist, ux-design) com registro de por quê. | observado | `docs/governance/artifacts.md` @ `d6ffbb2`, linha 16 ("Zero of forty cycles") |
| CLAIM-15-017 | A v0.1.0 (09/08/2026) foi a primeira versão após zero versões e zero tags em 44 ciclos: 13 agentes, 6 skills, 22 anti-padrões, 11 portões executáveis, um caso de avaliação provado por ablação. | observado | `CHANGELOG.md`, seção `[0.1.0]` (linhas 1434–1446) |
| CLAIM-15-018 | Caixa marcada antes da evidência teve cinco ocorrências em três *tokens* (`TAIL:`, critérios de aceite, campo `registro` do índice de decisões); a spec do 045, escrita antes, dizia quatro em dois. | observado | `specs/045-fechar-v0-1-0/qa-report.md` @ `8b0ced3`, seções "A quinta ocorrência, num log que não se retira" e "Lição para a retrospectiva"; contraste: `specs/045-fechar-v0-1-0/spec.md` @ `8b0ced3`, "O quê e por quê" |
| CLAIM-15-019 | Em 22/08/2026 o remoto não tinha tag nenhuma; v0.1.0 e v0.2.0 nunca publicadas; quatro tentativas de push da v0.3.0 falharam. | observado | `docs/records/decisoes.jsonl` id `achado-062-nenhuma-tag-existe-no-remoto` |
| CLAIM-15-020 | Em 23/08/2026 a revisão independente achou o fechamento do achado do 055 afirmado falso. | observado | `docs/records/decisoes.jsonl` ids `achado-063-fechamento-do-055-foi-afirmado-falso` e `retro-063-achado-063-055` |
| CLAIM-15-021 | O gauntlet do 074 teve seis peças contra o Maestri; a P3 perdeu quatro rodadas às cegas e foi transferida ao 076 (29/10/2026). | observado | `docs/records/decisoes.jsonl` ids `decisao-074-gauntlet-maestri` e `decisao-074-p3-transferida-076` |
| CLAIM-15-022 | A redundância da instrução de raia apareceu em 2 fixtures e 2 ablações; foi fechada como gatilho, a reavaliar com um terceiro dado. | observado | `docs/records/decisoes.jsonl` ids `achado-040-raia-sobredeterminada` e `retro-041-fecha-040c` |
| CLAIM-15-023 | A proposta de fluxo v5 (ciclo 053) comparou o ciclo de vida com um externo de 13 passos; seis das dezesseis caixas mudariam. | observado | livro: `maestro-handbook/diagramas/06-fluxo-v5-proposta.md`, linhas 5 e 8 |
| CLAIM-15-024 | A fase F13 (ciclo 037) foi entregue vermelha, com linhas de base pendentes. | observado | `docs/roadmap.md` linha F13 |
| CLAIM-15-025 | A base de pesquisa propõe sumário de 16 capítulos, anatomia de 11 seções e quatro corpora; o guia do Maestro tinha esqueleto de 9 seções. | observado | livro: `pesquisa/base-de-pesquisa.md` ("Quatro corpora", "Sumário proposto"); Maestro `docs/livro/guia-editorial.md` §2 |
| CLAIM-15-026 | O prompt de pesquisa profunda que originou o modelo operacional foi gerado em 22/07/2026. | observado | `docs/research/prompt-pesquisa-praticas-desenvolvimento.md`, linha 3 ("Gerado em 2026-07-22") |
| CLAIM-15-027 | O SWE-Bench Pro tira suas tarefas de 41 repositórios ativamente mantidos. | observado | Deng et al., arXiv:2509.16941, resumo (https://arxiv.org/abs/2509.16941, acesso em 02/11/2026) |
| CLAIM-15-028 | O README do exemplo traz cinco exercícios numerados. | medido | `grep -c '^[0-9]\. \*\*' livro/15-validando-o-maestro/exemplo/README.md` → `5` |

## Como conferir um claim "observado"

"Observado" quer dizer: o número está escrito num artefato datado do Maestro, e qualquer um
o lê com um comando, sem confiar no livro. Com `M=<caminho do clone do Maestro>`:

```bash
# 003 — veredito, ablação (com o plano retido) e a asserção limítrofe do caso 001
git -C $M show 19823c2:evals/001-review-drops-a-requirement/baseline.md | grep -nE 'Verdict|Ablation|First-red|borderline|plan withheld'
# 004 / 005 — o caso 002: rodadas, ablação e o defeito de fixture
git -C $M show 19823c2:evals/002-guardian-accepts-a-wrong-lane/baseline.md | grep -nE 'Ablation|pending|defect'
# 002, 006, 007, 019, 020, 021, 022 — linhas do índice de decisões, por id
git -C $M show 19823c2:docs/records/decisoes.jsonl | grep -E 'achado-037-linhas-de-base-pendentes|achado-041-ciclo-040-sem-spec|retro-041-fecha|achado-062-nenhuma-tag|achado-063-fechamento|decisao-074-|achado-040-raia|retro-041-fecha-040c'
# 010 — 35 de 40
git -C $M show 19823c2:specs/042-conformidade-executavel/spec.md | sed -n 15,30p
# 017 — a nota da v0.1.0
git -C $M show 19823c2:CHANGELOG.md | grep -n -A12 '^## \[0.1.0\]'
# 018 — cinco ocorrências, três tokens (e o "quatro" da spec, anterior)
git -C $M show 8b0ced3:specs/045-fechar-v0-1-0/qa-report.md | grep -n 'Cinco ocorrências'
git -C $M show 8b0ced3:specs/045-fechar-v0-1-0/spec.md | grep -n 'quatro vezes'
# 024 — F13 entregue vermelha
git -C $M show 19823c2:docs/roadmap.md | grep -n 'F13'
# 026 — data do prompt de pesquisa
git -C $M show 19823c2:docs/research/prompt-pesquisa-praticas-desenvolvimento.md | sed -n 3p
```

Os claims marcados "livro:" leem-se direto neste repositório. O 027 depende de fonte externa e
é o único que não se reproduz offline.
