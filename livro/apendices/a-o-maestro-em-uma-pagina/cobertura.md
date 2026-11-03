# Cobertura do inventário — apêndice A

## Itens principais (16/16)

| id | seção onde está coberto |
|---|---|
| CICLOS-B-014 | «A falha real: o resumo que afirmava o que o disco não tinha» (ciclo 053, oito grupos de defeito, check-retro vermelho por dívida do 047); «Por que este resumo também envelhece» |
| LIVRO-METODO-002 | «A página», parágrafo «Dois detalhes evitam confusão» (12 elementos, 13 capítulos, rótulo ≠ número do capítulo, ordem = dependência) |
| LIVRO-METODO-149 | «As outras formas do mesmo desenho», «O deck executivo» (10 slides, dois extremos, 12 elementos em 5 camadas, seis pilares, prova viva e sua fraqueza como evidência) |
| LIVRO-METODO-164 | «A página», parágrafo sobre o caderno de desenvolvimento (três coisas a guardar; norma que ninguém confere vira `check-*.sh`) |
| LIVRO-METODO-165 | «As outras formas do mesmo desenho», «Os prompts de imagem» (direção de arte única, sem texto, espaço negativo; o prompt é o artefato) |
| LIVRO-METODO-198 | «A página», «O nome» (partitura, compasso, músicos; um rege, muitos executam) |
| LIVRO-METODO-199 | «A página», «Três ideias costuram o resto» |
| LIVRO-METODO-201 | «O ciclo, com quem executa cada passo» (tabela com Steward, agentes, gates) |
| LIVRO-METODO-204 | «O processo em sete raias» (tabela das raias, caixas navegáveis, losangos na raia humana) |
| LIVRO-METODO-213 | «As outras formas do mesmo desenho», «A planta gerada» (Archify, cinco raias, retrato de 22/10 `39a86ba`, sem os portões do ADR 0030) |
| LIVRO-METODO-214 | «As outras formas do mesmo desenho», «As peças numeradas» e «O código de cores» (render-pdf.mjs, Playwright, conflito com a 06) |
| LIVRO-METODO-231 | «A página», tabela «O sistema, em 12 elementos e 5 camadas» e a leitura de cima para baixo |
| LIVRO-METODO-232 | «Como ler o Maestro» (quatro paradas e glossário) |
| LIVRO-METODO-239 | «Como ler o Maestro», parágrafo das cinco trilhas e da cadência de estudo |
| LIVRO-METODO-304 | «O processo em sete raias» (BPMN do OMG, versão 2.0.2); Referências |
| LIVRO-METODO-308 | «A planta gerada»; Referências |

## Itens secundários usados

| id | seção |
|---|---|
| CICLOS-A-028 | «O processo em sete raias», tabela (raia de distribuição em três camadas) |
| CICLOS-A-063 / DECISOES-012 / GOV-012 | «O processo em sete raias» (raia de portões e gatilho da retro no ciclo 035; regra argumentada contra os axiomas) |
| GOV-001 | «A página» (governança: constituição que só se emenda) |
| GOV-038 / LIVRO-METODO-004 | «A página», leitura da camada fundamento |
| GOV-039 / LIVRO-METODO-026 | «O ciclo, com quem executa cada passo» (raias leve/plena/infra) |
| LIVRO-METODO-054 | «A página», camada estrutura (RACI, Accountable sempre humano) |
| LIVRO-METODO-007 | «A página», terceira ideia (reversibilidade compra velocidade) |
| LIVRO-METODO-200 | «O deck executivo» (os dois extremos que falham) |

## Seções acrescentadas na correção da crítica (02/11/2026)

| seção | o que cobre | claims |
|---|---|---|
| «De onde vêm as três ideias» | axiomas A1–A5, derivação das três ideias (T1, T2, T3, C4), C7 e C1; o resumo dos axiomas na constituição defasado (seis/dez × sete/treze) | CLAIM-91-026 |
| «Em que o Maestro difere das alternativas» | Spec Kit adotado, OpenSpec, BMAD, Kiro, Superpowers, prompt sem spec; Scrum com agentes × artefatos e portões; limite do fichamento sem uso | CLAIM-91-027, CLAIM-91-028 |
| «Quando este resumo atrapalha» | custo do resumo sem consumidor (C9), do claim por número, da revisão que refuta; o Maestro inteiro como excesso | CLAIM-91-016, CLAIM-91-026, CLAIM-91-028 |
| «O ciclo, com quem executa cada passo» (passo zero) | o passo zero no caderno de desenvolvimento, ausente do `03-fluxo.md`; C6 | CLAIM-91-025 |
| «As outras formas do mesmo desenho» (caderno) | os slides «1 de 4» a «3 de 4», sem «4 de 4» | CLAIM-91-023 |
| «A falha real» (comando que devolvia três) | lacuna 02 do qa-report do 053 | CLAIM-91-024 |
| «Evidência» | claims por estado (13 medido, 15 observado); hipóteses H1, H2, H8, H10 marcadas como hipótese; o que o exemplo reproduz e quanto demora | — |

## Correção da segunda crítica (03/11/2026)

| seção | o que cobre | claims |
|---|---|---|
| «Se você só tem uma página» (novo, antes de «A página») | a página de verdade: definição, três ideias, o que fazer na segunda-feira (instalar, ciclo leve, medir o tempo); o resto marcado como aprofundamento | CLAIM-91-001, CLAIM-91-025, CLAIM-91-029 |
| «Em que o Maestro difere das alternativas», «Critério de adoção para um tech lead» | custos conferíveis (13 agentes, 12 comandos, 6 skills, 12 moldes, 19 scripts; instalação ~5 min; tempo por ciclo não publicado), três perguntas de decisão, primeiro passo | CLAIM-91-018, CLAIM-91-028, CLAIM-91-029 |
| «Checklist para quem avalia adotar o Maestro» | checklist de decisão, ao lado do checklist de quem resume o próprio método | — |
| «Evidência» | 29 claims: 13 medido, 16 observado; tempo do exemplo como faixa (11 s a ~80 s) | — |
