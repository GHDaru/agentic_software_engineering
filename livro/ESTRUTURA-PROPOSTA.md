# Proposta de estrutura do livro (rascunho para decisão — 02/11/2026)

> Proposta, não decisão. Responde à primeira tarefa do `PROMPT-RESTAURAR.md`: a árvore de
> pastas, o sumário final e o mapa do que reaproveitar do handbook do Maestro. Nenhum capítulo
> foi escrito. As perguntas que são decisão do Darú estão no fim (§5).
>
> Fontes lidas: `pesquisa/base-de-pesquisa.md`; `maestro-handbook/handbook/` (README, os 13
> capítulos e 3 apêndices, pelos títulos de seção); no Maestro (somente leitura),
> `docs/governance/axioms.md`, `docs/livro/guia-editorial.md`, a lista de ADRs 0004–0033 e de
> skills.

## 1. Três escolhas que moldam o resto

1. **Pasta por capítulo, não arquivo solto.** A anatomia exige *exemplo executável*; código
   que roda precisa de casa ao lado do texto, com o mesmo número.
2. **O livro cita o Maestro por versão, não copia.** O padrão Maestro de cada capítulo aponta
   para o handbook/governança numa tag do Maestro (`maestro@vX.Y`). O handbook continua sendo a
   referência por versão (corpus 2); o livro guarda o argumento (corpus 3).
3. **A espinha lógica são os axiomas do Maestro.** Os cinco axiomas (A1–A5) e sete teoremas
   (T1–T7) de `docs/governance/axioms.md` já são um argumento independente de ferramenta. Cada
   capítulo declara de qual teorema deriva; capítulo que não deriva de nenhum é sinal de que
   ou falta axioma, ou o capítulo é ferramenta (e vai para o handbook).

## 2. Estrutura de pastas

```text
470_LIVRO_ESOA/
├── README.md                       mapa (já existe)
├── livro/                          CORPUS 3 — o argumento durável
│   ├── README.md                   estado de cada capítulo (rascunho/revisão/pronto)
│   ├── sumario.yaml                FONTE ÚNICA: ordem, parte, slug, título, estado, teorema,
│   │                               claims citados — o build e os portões leem daqui
│   ├── guia-editorial.md           anatomia de 11 seções, regra de evidência, siglas, voz
│   ├── glossario.md
│   ├── referencias.bib             (ou .md — ver §5, pergunta 3)
│   ├── 00-prefacio/
│   ├── 01-a-mudanca-de-unidade-de-trabalho/
│   │   ├── capitulo.md
│   │   ├── figuras/
│   │   └── exemplo/                o exemplo executável (script, fixture, saída esperada)
│   ├── 02-.../  …  16-.../
│   └── apendices/
│       ├── a-o-maestro-em-uma-pagina/      resumo por versão, com link ao handbook
│       ├── b-aseg-bench/                   o benchmark de governança GOV-001…010
│       ├── c-pacote-de-replicacao/         como reproduzir cada CLAIM
│       └── d-estudos-de-campo/             ex-apêndices A/B/C do handbook, datados
├── pesquisa/                       CORPUS 4 — evidência
│   ├── base-de-pesquisa.md         (já existe)
│   ├── CLAIMS.md                   uma linha por claim: id, afirmação, estado, evidência
│   ├── hipoteses.md                H1–H10, cada uma com a métrica e o desenho que a testa
│   ├── protocolo.md                baselines A/B/C × tratamento, congelamento do ambiente
│   ├── runs/                       um diretório por run, schema imutável (append-only)
│   ├── datasets/ciclos-maestro/    extração sanitizada dos 76 ciclos (specs, retros, decisões)
│   └── leituras/                   fichamento das referências-base
├── maestro-handbook/               cópia congelada de 19823c2 — SOMENTE LEITURA
├── publicar/                       build do livro (derivado de maestro-handbook/publicar)
└── scripts/                        portões: anatomia, claim sem id, sigla nua, links
```

Os portões mínimos (o livro é governado pelo próprio método — "instrução não é enforcement"):

| Portão | Falha quando |
|---|---|
| `check-anatomia` | capítulo sem uma das 11 seções |
| `check-claims` | número no texto sem `[CLAIM-NNN]`, ou claim citado que não existe em `CLAIMS.md` |
| `check-siglas` | sigla sem forma por extenso na primeira ocorrência do capítulo (Princípio VIII) |
| `check-links` | link relativo ou referência que não resolve |
| `check-sumario` | `sumario.yaml` × pastas divergem nos dois sentidos |

## 3. Sumário final (16 capítulos em 4 partes)

Mantenho os 16 da base de pesquisa, agrupo em partes e proponho três ajustes (marcados ✎).

**Parte I — Por que agentes mudam a engenharia**

| # | Título | Pergunta central | Deriva de |
|---|---|---|---|
| 1 | A mudança de unidade de trabalho | Se gerar código ficou barato, o que ficou caro? | A5 |
| 2 | O problema da confiança | Quem responde pelo que um agente fez? | A2 · T2 |
| 3 | Um humano, muitos agentes | Qual é o gargalo quando a capacidade deixa de ser? | A1 · A3 |

**Parte II — Especificar e dar contexto**

| # | Título | Pergunta central | Deriva de |
|---|---|---|---|
| 4 | A spec como partitura | Por que a spec gera o código em vez de descrevê-lo? | T1 |
| 5 | Engenharia de contexto | Como selecionar, comprimir, persistir e transferir o que o agente sabe? | A3 · T5 |
| 6 | Como dividir o trabalho | Onde cortar para que agentes em paralelo não colidam? | A3 |
| 7 | ✎ Papéis e skills | Como dar a um agente um modo de trabalho, e não só um prompt? | T2 |
| 8 | DDD para agentes | Como impedir que N agentes criem N nomes para a mesma coisa? | A4 |

**Parte III — Provar e conter**

| # | Título | Pergunta central | Deriva de |
|---|---|---|---|
| 9 | Arquitetura que se defende | Como a arquitetura recusa a mudança errada sem um revisor? | T4 |
| 10 | Quality Gates que provam fatos | O que acontece quando o check mede o proxy, e não o fato? | T4 · T7 |
| 11 | Risco, reversibilidade e autonomia | Quanta autonomia dar a cada ação? | T3 |
| 12 | ✎ Ferramentas, MCP e o ecossistema | O que muda quando o agente age no mundo por ferramentas? | T3 |

**Parte IV — Medir e aprender**

| # | Título | Pergunta central | Deriva de |
|---|---|---|---|
| 13 | Observabilidade e economia | Quanto custa uma tarefa aceita, e onde o custo se perde? | A5 · T7 |
| 14 | ✎ A organização que aprende | Como uma correção vira regra sem a governança inchar? | T6 · T5 |
| 15 | Validando o Maestro | Como testar uma metodologia, e não só um software? | T7 |
| 16 | O futuro da engenharia agêntica | O que deste livro sobrevive à próxima geração de modelos? | — |

Os três ajustes:

- **7 e 12 dividiam "ferramentas".** Proponho: o 7 fica com papéis e skills (o modo de
  trabalho); o 12 fica com ferramentas, MCP (Model Context Protocol) e o risco de agir no mundo
  (excessive agency, prompt injection — do OWASP GenAI Top 10).
- **Artefatos vivos e rastreabilidade não tinham casa.** São dois capítulos do handbook (08 e
  11). Vão para o 14 (artefato vive se é consumido; governança que aprende sem inchar) e para o
  5 (a rastreabilidade é a memória que sobrevive ao reset do contexto).
- **DORA não tinha casa.** DevOps Research and Assessment (DORA) e SPACE entram no 1 (a economia
  muda) e no 13 (as cinco métricas como bússola).

## 4. Mapa de reaproveitamento do handbook

Anatomia: o handbook usa o esqueleto v2 de 9 seções; o livro usa 11. O mapa de seções:

| Handbook (v2) | Livro | Como reaproveitar |
|---|---|---|
| 1 Objetivos | resultado de aprendizagem | reescrever sem nome de ferramenta |
| 2 O problema | **falha real antes da regra** | só serve se virar falha datada, com ciclo e commit do Maestro |
| 3 A ideia central | pergunta central + teoria | aproveitar a ideia, não o texto |
| 4 A regra vigente | padrão Maestro | **citar por versão**, nunca copiar |
| 5 Fundamentos (5.1–5.3) | teoria | maior reaproveitamento de argumento |
| 5.4 Frameworks avaliados | alternativas | atualizar (LangGraph, CrewAI, ADK, Agent Framework, Agents SDK) |
| 6 Na prática — o ciclo real | exemplo executável | a narrativa vira script que roda em `exemplo/` |
| 7 Erros e anti-padrões | contraexemplo | direto, com a skill `anti-patterns` |
| 8 Verificação | checklist | direto |
| 9 O que roubar | — | funde no checklist |
| — | evidência | **novo**: claims com id em `pesquisa/CLAIMS.md` |
| — | referências | 7 Fontes do v1 + referências-base |

O que cada capítulo do livro aproveita (H = handbook; R = receita; D = diagrama; ADR e
ciclos estão no Maestro):

| Cap. | Do handbook | Do Maestro (evidência e falhas reais) | Lacuna (escrever do zero) |
|---|---|---|---|
| 1 | H02 §5.3 (tamanho de lote); H01 §5.3 (reversibilidade) | axioma A5 | a economia do custo de gerar × verificar |
| 2 | **H01** (quem decide o quê); H06 §5.1–5.3 | T2; ADR 0026 (gate por delegação de política) | confiança como problema de engenharia, não de modelo |
| 3 | H07 §5.3 (WIP = atenção humana); H05 §5.1; D01, D02 | painel de regência (ciclos 066/075) | o limite humano medido |
| 4 | **H03**; H13 §5.1, §5.2, §5.12 (EARS); R `abrir-um-ciclo` | T1; ADR 0005 (raias) | comparação com Spec Kit sem depender dele |
| 5 | **H04**; **H11** | A3; ADR 0013 (instrução como fonte única) | as 4 operações: seleção, compressão, persistência, transferência |
| 6 | **H05**; H13 §5.6 (corte por fronteira) | ADR 0018 (fronteira interna) | quando multiagente piora (H4) |
| 7 | **H06**; H13 §5.14 (Iron Laws); apêndice B (Superpowers) | `.claude/agents/`, skills, `check-roles.sh` | papel × modelo × custo |
| 8 | H13 §5.6 | ADR 0023 (modelo de domínio no plan), ADR 0029; ciclo 076 (glossário gerado) | **quase tudo**: REUSE/EXTEND/ALIAS/CREATE |
| 9 | H13 §5.5 (fitness functions), §5.6 | `check-boundary.sh`; ADR 0028 (hexagonal) | arquitetura como portão, não diagrama |
| 10 | **H09**; R `escrever-criterio-verificavel`; H13 §5.4 | T4; skill `verifiable-dod`; achado 063 (anti-padrão 21 sobreviveu a 7 fechamentos) | teste de mutação do gate |
| 11 | **H10**; H01 §5.3; H13 §5.7 | T3; `promote-main.sh`; ADR 0009 | autonomia como função contínua |
| 12 | apêndice C (panorama) | ADR 0025 (hooks de terceiro) | **quase tudo**: MCP, superfície de ferramenta, OWASP |
| 13 | H02 §5.1–5.2; apêndice A §2 (auditoria com custo) | ADR 0033 (OpenTelemetry), ledger de tokens | custo por tarefa aceita |
| 14 | **H12**; **H08**; H07 §5.2 (retro); R `rodar-a-retro` | T6; ADR 0021; `check-retro.sh`; decisoes.jsonl | — |
| 15 | — | T7; ADR 0016 (evals), ADR 0019 (conformidade executável) | **quase tudo**: protocolo, ASEG-Bench, H1–H10 |
| 16 | apêndice C | — | **quase tudo** |

Fica **fora do livro** (é referência por versão, mora no handbook): H13 §5.2 (uma ferramenta de
spec só), §5.9 (changelog), §5.11 (registro por máquina), §5.13 (vendorização); as apresentações
HTML; o diagrama 06 (proposta de fluxo v5). Os diagramas 03 (fluxo) e 05 (BPMN) entram no
apêndice A.

Leitura do mapa: os capítulos 1–7, 10, 11 e 14 têm base forte no handbook; 8, 12, 15 e 16 são
essencialmente novos e dependem da agenda de pesquisa — são os que mais demoram.

## 5. Perguntas que são decisão do Darú

1. **Leitor e formato de publicação.** Quem é o leitor-alvo — tech lead/engenheiro sênior
   (livro de prática), academia (o pacote de replicação sugere isso) ou os dois? E o destino:
   site próprio, PDF, editora? Muda o tom, o tamanho do capítulo e o build.
2. **Os três ajustes do sumário (§3)** e o agrupamento em quatro partes: aprova, ou mantém os
   16 títulos como estão?
3. **Referências em BibTeX ou em Markdown?** BibTeX se houver destino acadêmico ou editora;
   Markdown se for só o site. Depende da resposta 1.
4. **O livro é escrito pelo próprio Maestro?** Isto é: cada capítulo é um ciclo (spec →
   rascunho → revisão em contexto fresco → seu gate), com os portões do §2. Recomendo que sim —
   o livro vira, ele mesmo, um caso de estudo para o capítulo 15 —, mas o custo de cerimônia é
   seu de aceitar.
