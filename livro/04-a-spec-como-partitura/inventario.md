# Inventário do capítulo 4

Gerado de `pesquisa/inventario/itens.json` (02/11/2026).

## Itens PRINCIPAIS (61) — cada um tem de estar coberto neste capítulo

| id | fonte | resumo | falha real |
|---|---|---|---|
| CICLOS-B-044 | maestro:specs/070-conferidor-ordem-veredito/00-chamado.md | Evidência importada do Hindiana: chamado rodado com gates G0–G3 e requisitos EARS; isenta pela forma no check-conformance.sh. |  |
| CICLOS-A-009 | maestro:specs/009-vendorizar-spec-kit/spec.md @ e32023f | Ciclo 009: o Spec Kit é vendorizado seletivamente — templates adaptados (raias, EARS, Constitution Check real, gate humano no fim), comando converge trazido do fork e .specify/UPSTREAM.md registrando a proveniência; upstream só entra por spec. |  |
| CICLOS-A-038 | maestro:specs/023-capitulo-03-padrao-v2/spec.md @ ba9c1c4 | Ciclo 023: capítulo 03 (Spec-Driven) no padrão v2, explicando EARS com frase real do repositório e o caminho spec → executável → primeira execução, com todo número reproduzível por comando. |  |
| CICLOS-A-039 | maestro:specs/023-capitulo-03-padrao-v2/qa-report.md @ ba9c1c4 | Falha real: a primeira versão da seção 6 afirmava que correções de texto entravam como raia leve; o comando mostrou 19 plena contra 2 leve e todas com spec própria — afirmação plausível e falsa sobre o próprio método (anti-padrão 7 aplicado à prosa). | sim |
| CICLOS-A-040 | maestro:specs/023-capitulo-03-padrao-v2/qa-report.md @ ba9c1c4, 7264fe6 | Falha real: a régua de raias não era aplicada (19 de 22 specs 'plena'); registrado com pergunta objetiva e só convertido em portão (justificativa por três fatores no check-cycle.sh) na retro do ciclo 034. | sim |
| CICLOS-A-074 | maestro:specs/041-retro-dos-quatro-achados-de-eval/qa-report.md @ 4f6ec0e, 0873e40 | Falha real: trabalho feito sem spec, plano, tarefas nem relatório e commitado duas vezes como 'ciclo 040', número sem artefato — violação do Princípio I pega pelo check-cycle.sh; os commits não foram reescritos (histórico compartilhado). | sim |
| CICLOS-A-086 | maestro:specs/044-speckit-plan-defere-a-declaracao/spec.md @ 73cd3e5 | Ciclo 044: o /speckit.plan vendorizado passa a gerar só os artefatos declarados =yes na tabela do plano, resolvendo duas ordens contraditórias entregues pelo instalador (e o quickstart.md, sexto artefato fora do catálogo). |  |
| DECISOES-002 | maestro:docs/adr/0005-raias-de-trabalho-e-specs-de-infra.md | ADR 0005: três raias (leve/delta: o PR é o artefato e bug exige teste que reproduz; plena: Spec Kit completo; infra: sempre plena com bloco obrigatório para irreversíveis — backup, dry-run, staging). Desempate: na dúvida é plena; infra/migração nunca é leve. |  |
| DECISOES-036 | maestro:docs/records/decisoes.jsonl#achado-023-regua-de-raias · commit 7264fe6 | Régua de raias não aplicada: 19 specs plena contra 2 leve; fechado no check-cycle.sh. | sim |
| DECISOES-046 | maestro:docs/records/decisoes.jsonl#achado-041-ciclo-040-sem-spec · commit 2d3504f | Commits citando ciclo 040 sem specs/040-*: violação do Princípio I pelo próprio agente, pega pelo check-cycle. | sim |
| DECISOES-098 | maestro:docs/roadmap.md#F4 | F4: Spec Kit vendorizado com raias, EARS, Constitution Check, converge e UPSTREAM.md. |  |
| DECISOES-125 | maestro:docs/ecosystem/ideias/001-ears.md | Ideia 001 (Kiro): EARS — absorver em verifiable-dod. |  |
| DECISOES-129 | maestro:docs/ecosystem/ideias/005-raia-leve-delta.md | Ideia 005 (OpenSpec): mudança como delta — absorver como raia leve. |  |
| DECISOES-140 | maestro:docs/ecosystem/ideias/016-spec-como-artefato-executavel.md | Ideia 016 (Tessl): spec executável — observar. |  |
| DECISOES-144 | maestro:docs/ecosystem/ideias/020-fluxo-spec-em-comandos.md | Ideia 020 (Pimzino): fluxo em comandos — descartar. |  |
| DECISOES-145 | maestro:docs/ecosystem/ideias/021-baixa-cerimonia-para-mudanca-simples.md | Ideia 021 (GSD, OpenSpec): baixa cerimônia — descartar. |  |
| DECISOES-155 | maestro:docs/ecosystem/ideias/031-spec-kit.md | Ideia 031: spec-kit — a única adotar do catálogo. |  |
| DECISOES-160 | maestro:docs/ecosystem/ideias/036-formato-mission-roadmap-techstack.md | Ideia 036 (Agent OS): mission/roadmap/tech-stack — absorver no roadmap. |  |
| DECISOES-163 | maestro:docs/ecosystem/ideias/039-piramide-prd-epico-historia.md | Ideia 039 (BMAD): pirâmide PRD/épico/história — descartar. |  |
| LIVRO-METODO-022 | livro:maestro-handbook/handbook/03-spec-driven.md §5.1 | Inversao de dependencia aplicada a documento: a spec passa de descricao a jusante para input a montante que gera o codigo, e por isso nao apodrece. |  |
| LIVRO-METODO-023 | livro:maestro-handbook/handbook/03-spec-driven.md §2 | Com agentes, prompt vago gera codigo que compila, passa no teste e erra a intencao, o modo de falha mais caro porque parece sucesso. |  |
| LIVRO-METODO-024 | livro:maestro-handbook/handbook/03-spec-driven.md §5.2 | EARS: QUANDO <condicao> O SISTEMA DEVE <comportamento observavel>; condicao e comportamento observaveis fazem do requisito um teste quase 1:1. |  |
| LIVRO-METODO-025 | livro:maestro-handbook/handbook/03-spec-driven.md §4 | A spec diz o que e por que; o plano diz como; misturar os dois e o comeco do amontoado. |  |
| LIVRO-METODO-026 | livro:maestro-handbook/handbook/03-spec-driven.md §5.3 | Raias leve/plena/infra decididas por ambiguidade x raio x irreversibilidade; na leve o PR e o artefato e bug exige teste que reproduz. |  |
| LIVRO-METODO-027 | livro:maestro-handbook/handbook/03-spec-driven.md §4 | Regra de desempate: na duvida, plena; infraestrutura e migracao nunca sao leves. |  |
| LIVRO-METODO-028 | livro:maestro-handbook/handbook/03-spec-driven.md §5.4 | GitHub Spec Kit adotado como base unica do fluxo spec-driven, casando com constituicao e ciclos numerados. |  |
| LIVRO-METODO-029 | livro:maestro-handbook/handbook/03-spec-driven.md §5.4 | OpenSpec (Fission-AI) descartado como segunda ferramenta; a ideia do delta foi absorvida como raia leve (ADR 0005). |  |
| LIVRO-METODO-030 | livro:maestro-handbook/handbook/03-spec-driven.md §5.4 | Kiro, Tessl e 'specs as source of truth' observados sem adocao (ADR 0008); prompt ad-hoc rejeitado. |  |
| LIVRO-METODO-031 | livro:maestro-handbook/handbook/03-spec-driven.md §6 | 14 de 22 specs com requisitos em EARS (padrao entrou no ciclo 008); FR3 do ciclo 021 virou laco em check-install.sh, mostrando a frase da spec virando comando. |  |
| LIVRO-METODO-033 | livro:maestro-handbook/handbook/03-spec-driven.md §6; maestro commit ba9c1c4 | Regua de raias mal aplicada: das 22 specs, 19 plena e 2 leve, registrado como dado desconfortavel a espera da retro. | sim |
| LIVRO-METODO-034 | livro:maestro-handbook/handbook/03-spec-driven.md §7 | Anti-padroes de spec: spec que descreve solucao, criterio nao verificavel, spec escrita depois, raia plena para tudo, raia leve por conveniencia. |  |
| LIVRO-METODO-083 | livro:maestro-handbook/handbook/09-definition-of-ready-done.md §4 | Definition of Ready: spec e plano completos o bastante para o agente executar sem adivinhar. |  |
| LIVRO-METODO-140 | livro:maestro-handbook/handbook/apendice-b-superpowers.md | Tensao HARD-GATE universal x raias: o Superpowers exige design para tudo; o Maestro mantem a raia leve (ADR 0005) e absorve so o aviso 'na duvida, plena'. |  |
| LIVRO-METODO-152 | livro:maestro-handbook/handbook/apresentacao-desenvolvimento-maestro.html | Caderno de desenvolvimento (v0.2.0): o ciclo do ponto de vista de quem executa, de intencao a retro, sem daily, planning ou grooming. |  |
| LIVRO-METODO-177 | livro:maestro-handbook/receitas/abrir-um-ciclo.md | Receita de abrir ciclo: classificar a raia em 30 s, scripts/new-cycle.sh NNN slug cria specs/NNN-slug com os quatro artefatos sem sobrescrever. |  |
| LIVRO-METODO-178 | livro:maestro-handbook/receitas/abrir-um-ciclo.md §3 | Ordem de escrita da spec: Origem, O que e por que, FR, Fora de escopo, Criterios, Clarify; nao inventar requisito nao dito, ambiguidade vira pergunta. |  |
| LIVRO-METODO-179 | livro:maestro-handbook/receitas/abrir-um-ciclo.md §4 | Gate de prontidao (DoR) humano antes do plano: criterios testaveis, ambiguidades resolvidas, fora de escopo explicito e apetite definido. |  |
| LIVRO-METODO-180 | livro:maestro-handbook/receitas/abrir-um-ciclo.md §5 | Constitution Check com uma linha por principio (oito), violacao reformulada ou registrada em Complexity Tracking (skill constitution-check). |  |
| LIVRO-METODO-306 | livro:pesquisa/base-de-pesquisa.md §Referencias | GitHub Spec Kit. |  |
| GOV-002 | maestro:docs/governance/principles.md | Princípio I, spec-driven: nenhum código nasce sem especificação; a spec é o insumo que gera o código (por isso não apodrece) e mudança de escopo volta à spec antes de virar código. |  |
| GOV-018 | maestro:docs/governance/axioms.md | T1 (A1+A4), spec precede código; evidência: 34 ciclos abertos por spec.md e o FR3 do ciclo 021 que, escrito antes do código, virou laço em check-install.sh e pegou deriva de três ciclos na primeira execução. |  |
| GOV-030 | maestro:docs/governance/axioms.md | Corolário C6: quanto processo uma mudança recebe é função de ambiguidade x raio x irreversibilidade (as três raias; check-cycle.sh). |  |
| GOV-039 | maestro:docs/governance/operating-model.md | Raias de trabalho (§3, ADR 0005): leve (o PR é o artefato), plena (spec completa) e infra (sempre plena + gates de reversibilidade); o valor da spec escala com ambiguidade x raio x irreversibilidade. |  |
| GOV-040 | maestro:docs/governance/operating-model.md | Regras da raia leve: na dúvida é plena; infra e migração nunca são leves; a raia leve não afrouxa revisão independente nem testes, e bug exige teste que o reproduza falhando antes. |  |
| GOV-047 | maestro:docs/governance/operating-model.md | Definition of Ready (§7) para a raia plena: spec com critérios testáveis, ambiguidades resolvidas, Constitution Check aprovado, ux-design se houver tela e apetite definido. |  |
| GOV-056 | maestro:docs/governance/artifacts.md | Os quatro artefatos que sempre existem (spec.md, plan.md, tasks.md, qa-report.md); tasks.md pesa mais que o tamanho sugere porque é o que o agente executor segue e o que sobrevive à compactação. |  |
| GOV-058 | maestro:docs/governance/artifacts.md | Cinco artefatos condicionais sempre declarados no plan.md por token legível por máquina (ART:research=, ART:data-model=, ART:contracts=, ART:checklist=, ART:ux-design=); ux-design não é opcional quando toca tela. |  |
| GOV-076 | maestro:docs/governance/glossary.md; maestro:.specify/templates/spec-template.md | EARS ('WHEN <condição> THE SYSTEM SHALL <comportamento observável>'): requisito que vira teste quase 1:1, absorvido do Kiro no ciclo 007 (ADR 0008); vive em verifiable-dod e no template de spec. |  |
| GOV-105 | maestro:skills/anti-patterns/SKILL.md | Anti-padrão 10. Mudança de escopo silenciosa: o agente 'aproveita' para refatorar; diff pequeno e problema maior vira registro. |  |
| GOV-134 | maestro:.claude/commands/speckit.specify.md | Comando /speckit.specify (Spec Kit vendorizado): cria ou atualiza a spec a partir da descrição em linguagem natural. |  |
| GOV-135 | maestro:.claude/commands/speckit.clarify.md | Comando /speckit.clarify: até 5 perguntas de esclarecimento dirigidas, com as respostas gravadas de volta na spec. |  |
| GOV-136 | maestro:.claude/commands/speckit.plan.md @ 73cd3e5 | Comando /speckit.plan: gera o plano a partir do template; desde o ciclo 044 defere à tabela de declaração de artefatos condicionais em vez de exigir os quatro artefatos. |  |
| GOV-137 | maestro:.claude/commands/speckit.tasks.md | Comando /speckit.tasks: gera tasks.md ordenado por dependência a partir dos artefatos de design. |  |
| GOV-138 | maestro:.claude/commands/speckit.implement.md | Comando /speckit.implement: executa o plano processando as tarefas de tasks.md. |  |
| GOV-139 | maestro:.claude/commands/speckit.analyze.md | Comando /speckit.analyze: análise não destrutiva de consistência entre spec.md, plan.md e tasks.md. |  |
| GOV-143 | maestro:.claude/commands/speckit.converge.md | Comando /speckit.converge (do fork da casa, ciclo 009): compara o repositório real com spec/plan/tasks e ANEXA o trabalho faltante como tarefas novas, nunca reescreve. |  |
| GOV-144 | maestro:.specify/UPSTREAM.md | Proveniência do Spec Kit vendorizado (ciclo 009): upstream github/spec-kit 0.4.3 e fork GHDaru/spec-kit; cada peça marcada com estado (UP:state=adapted); vendorizar faz do conteúdo fonte própria, consultando o upstream por decisão. |  |
| GOV-154 | maestro:scripts/new-cycle.sh | new-cycle.sh: cria specs/NNN-slug/ com os quatro artefatos esqueleto; nunca sobrescreve; os templates vendorizados prevalecem em divergência. |  |
| GOV-159 | maestro:scripts/check-cycle.sh @ 7264fe6 | check-cycle.sh: exige raia declarada E justificada pelos três fatores, mostra a distribuição de raias e exige commit citando o ciclo; nasceu de 19 de 22 specs 'plena' (ciclo 023) e da citação mantida 28 commits só por hábito (ciclo 031); admite que não julga a resposta. | sim |
| GOV-188 | maestro:.specify/templates/spec-template.md | Template de spec adaptado (ciclo 009): raia, comportamento em forma EARS, fora de escopo, clarify e gates. |  |
| GOV-189 | maestro:.specify/templates/plan-template.md | Template de plano: Constitution Check I-VIII, tabela de declaração ART: dos condicionais (=no por padrão, com motivo) e tabela DOM: do modelo de domínio. |  |

## Itens SECUNDÁRIOS (36) — o capítulo principal é outro; cite ou remeta quando servir ao argumento

| id | fonte | resumo | principal |
|---|---|---|---|
| CICLOS-B-039 | maestro:specs/067-trava-de-dominio-no-plan/spec.md | Ciclo 067 (retroativo): plan.md exige modelo de domínio declarado (linguagem ubíqua, agregados, invariantes), nunca omitido; o painel mostra quem pulou o plano. | 8 |
| CICLOS-B-046 | maestro:specs/070-workflow-sqlite/spec.md · commit b63c2fe | Integrado como parcial: FR2 ausente, FR3 invertido, FR1 sem branch/hash; o cabeçalho dizia 'Spec 064 / DRAFT' e o painel lia isso. Resto virou dívida declarada. | 10 |
| CICLOS-B-056 | maestro:specs/076-padroes-de-engenharia-e-react/spec.md | Ciclo 076: padrões de engenharia, tipos de mudança, contexto para a IA e frontend em React; o protótipo do 074 vira especificação visual. | 9 |
| CICLOS-A-030 | maestro:specs/020-bpmn-navegavel-no-livro/spec.md @ 0021b20 | Ciclo 020 (raia leve): o BPMN vira índice navegável do livro — cada caixa linka a referência — e o motor de publicação passa a copiar imagens e a falhar o build com <img> sem arquivo ou href .md não reescrito. | 14 |
| CICLOS-A-059 | maestro:specs/034-retro-dos-quatro-achados/spec.md @ 7264fe6 | Ciclo 034: retrospectiva dos achados abertos (o mais velho com 11 ciclos) vira portão — check-retro.sh (≥4 abertos ou ≥6 ciclos), check-cycle.sh (raia justificada por ambiguidade, raio e irreversibilidade + commit citando o ciclo), check-links.sh e check-chapters.sh; anti-padrões 17 e 18. | 14 |
| CICLOS-A-065 | maestro:specs/036-pesquisa-upstream-decomposicao/spec.md @ 01ccea1 | Ciclo 036: pesquisa do upstream (decompor projeto grande em ciclos) — 20 de 34 specs nasceram de pedido pontual, o Spec Kit não tem upstream (confirmado comando a comando), proposta em 'um objeto, um verbo e um portão' e recomendação de não construir sem dor real. | 6 |
| CICLOS-A-089 | maestro:specs/045-fechar-v0-1-0/spec.md @ 8b0ced3 | Ciclo 045: critérios de aceite sem caixas de marcação — a spec declara critérios e o qa-report diz se valeram (Princípio VI) — e fechamento da v0.1.0, primeira tag em 44 ciclos, como linha de base e não como marco de completude. | 15 |
| DECISOES-005 | maestro:docs/adr/0008-avaliacao-ecossistema-sdd.md | ADR 0008: mantém o Spec Kit como ferramenta SDD única; BMAD descartado, Kiro descartado como ferramenta (lock-in de IDE), Superpowers não adotado por atacado; absorve EARS e outras ideias com destino concreto. | 12 |
| DECISOES-048 | maestro:docs/records/decisoes.jsonl#achado-042-speckit-plan-contraditorio · commit d6ffbb2 | speckit.plan vendorizado contradizia a tabela de declaração; fechado com UPSTREAM.md regra 2 (divergência declarada). | 12 |
| DECISOES-051 | maestro:docs/records/decisoes.jsonl#spec-045-fecha-044 | Resolução por forma: critérios da spec perdem a caixa; a spec diz o que deve valer, o qa-report diz se valeu. | 10 |
| DECISOES-101 | maestro:docs/roadmap.md#F8-F9 | F8–F9: método instalável (ux-semantics, living-journey, três camadas) e BPMN navegável. | 7 |
| DECISOES-113 | maestro:docs/roadmap.md#upstream-outcome | Gatilho: outcome + skill de corte + check-outcomes.sh só na primeira intenção grande real. | 6 |
| DECISOES-136 | maestro:docs/ecosystem/ideias/012-contexto-de-codebase-na-spec.md | Ideia 012 (PRP): contexto na spec — observar até reger código de produção. | 5 |
| DECISOES-146 | maestro:docs/ecosystem/ideias/022-decomposicao-em-tres-passadas.md | Ideia 022 (Product-Manager-Skills): três passadas — observar. | 6 |
| DECISOES-162 | maestro:docs/ecosystem/ideias/038-tecnicas-de-descoberta.md | Ideia 038: técnicas de descoberta e fronteira de domínio — observar. | 8 |
| DECISOES-169 | maestro:docs/research/resultado-pesquisa-praticas-desenvolvimento-avaliacao.md | Avaliação da pesquisa (base do ADR 0004): spec-driven, sem Scrum, DORA, gate humano + revisão independente. | 1 |
| DECISOES-170 | maestro:docs/research/upstream-decomposicao.md | Pesquisa do upstream (036): gap medido e proposta outcome/slice-outcome/check-outcomes adiada por gatilho. | 6 |
| LIVRO-METODO-065 | livro:maestro-handbook/handbook/07-cerimonias-cadencia.md §4 | Apetite (Shape Up): tempo fixo, escopo variavel; quando o tempo acaba corta-se escopo, ilustrado pela migracao de capitulos um por ciclo. | 3 |
| LIVRO-METODO-093 | livro:maestro-handbook/handbook/10-gates-classes-de-risco.md §5.3 | Dois eixos, mesma fisica: ambiguidade x raio x irreversibilidade decide o processo (raia); irreversibilidade x impacto decide o gate. | 11 |
| LIVRO-METODO-142 | livro:maestro-handbook/handbook/apendice-c-panorama-templates.md §A | claude-code-spec-workflow (Pimzino): trilhas feature e bug-fix validam externamente as raias e o Analyze antes do Fix; observar. | D |
| LIVRO-METODO-145 | livro:maestro-handbook/handbook/apendice-c-panorama-templates.md §B | PRP (Product Requirement Prompt, Wirasm): contexto de codebase empacotado na spec; hands-on com gatilho do primeiro ciclo regendo codigo de produto. | D |
| LIVRO-METODO-153 | livro:maestro-handbook/handbook/apresentacao-desenvolvimento-maestro.html | Marcas ART:x=yes\|no no plan.md declaram os cinco artefatos opcionais (research, data-model, contracts, checklist, ux-design) e sao lidas por check-conformance.sh; silencio nao e decisao. | 10 |
| LIVRO-METODO-155 | livro:maestro-handbook/handbook/apresentacao-desenvolvimento-maestro.html | 12 comandos do motor (/speckit.specify, clarify, plan, tasks, implement, analyze, checklist, constitution, converge, taskstoissues, /dod, /eval). | 12 |
| LIVRO-METODO-175 | livro:maestro-handbook/handbook/apresentacao-desenvolvimento-maestro.html | check-cycle (consultivo): raia justificada e commit citando o ciclo, o elo antes so convencional. | 5 |
| LIVRO-METODO-181 | livro:maestro-handbook/receitas/escrever-criterio-verificavel.md | A pergunta que resolve: 'que comando prova isto?'; comportamento em EARS, estrutura ou invariante como par (comando, esperado). | 10 |
| LIVRO-METODO-250 | livro:pesquisa/base-de-pesquisa.md §Agenda H1 | H1: spec reduz retrabalho. | 15 |
| LIVRO-METODO-265 | livro:pesquisa/base-de-pesquisa.md §Agenda GOV-001 | GOV-001: feature sem spec. | B |
| LIVRO-METODO-282 | livro:pesquisa/base-de-pesquisa.md §Agenda metricas | Metrica: retrabalho. | 13 |
| GOV-013 | maestro:docs/governance/axioms.md | A1, a intenção é humana: o agente propõe, escreve e verifica, mas não quer; sem A1 não há razão para a spec existir. | 2 |
| GOV-044 | maestro:docs/governance/operating-model.md | Apetite (Shape Up): ciclo de tempo fixo e escopo variável; quando o apetite acaba corta-se escopo, não se estende prazo. | 3 |
| GOV-077 | maestro:docs/governance/glossary.md | BMAD-METHOD avaliado e rejeitado no ciclo 007 (ADR 0008): uma metodologia concorrente inteira criaria uma segunda fonte de verdade. | D |
| GOV-089 | maestro:skills/constitution-check/SKILL.md | Skill constitution-check: Iron Law 'nenhum plano sem as oito linhas, uma por princípio, nenhuma vazia'; decide quando um princípio conta como violado; nasceu de reescrita manual nos ciclos 003 e 004. | 7 |
| GOV-090 | maestro:skills/verifiable-dod/SKILL.md | Skill verifiable-dod: Iron Law 'nenhum critério de aceite sem o comando que o prova'; transforma critério vago em fitness function (grep, ls, teste) e recomenda EARS. | 10 |
| GOV-097 | maestro:skills/anti-patterns/SKILL.md | Anti-padrão 2. Contexto tribal: intenção que só existe na cabeça do operador; se não está na spec, o agente não sabe. | 5 |
| GOV-119 | maestro:.claude/agents/spec-agent.md | Agente spec-agent: escreve ou refina spec.md a partir da intenção (o quê e por quê, critérios testáveis) e levanta ambiguidades; não decide arquitetura nem implementa. | 7 |
| GOV-190 | maestro:.specify/templates/tasks-template.md | Template de tasks: verificação primeiro, doc viva no mesmo PR e as quatro linhas TAIL:review/security/mutation/gate da closing tail. | 10 |
