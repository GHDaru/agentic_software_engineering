# Inventário do capítulo D

Gerado de `pesquisa/inventario/itens.json` (02/11/2026).

## Itens PRINCIPAIS (30) — cada um tem de estar coberto neste capítulo

| id | fonte | resumo | falha real |
|---|---|---|---|
| CICLOS-B-003 | maestro:specs/047-catalogo-do-ecossistema/spec.md | Ciclo 047: catálogo do ecossistema com a ideia absorvida como unidade (não a ferramenta) e o momento da observação separado do estado vigente; portão check-ecosystem.sh. |  |
| CICLOS-B-049 | maestro:specs/073-area-administrativa/qa-report.md | Ciclo 073: pesquisa sem software da área administrativa; matriz 25 plataformas × 26 funcionalidades (650 células) e confronto: ENTRA 13, NÃO PRECISA 8, DEPOIS 5. |  |
| CICLOS-A-006 | maestro:specs/007-avaliacao-ecossistema-sdd/spec.md @ 2a1177e | Ciclo 007: avaliação do ecossistema de Spec-Driven Development (Superpowers, BMAD, Kiro, Taskmaster, Agent OS, GSD, Tessl) com veredito adotar/absorver/descartar/observar consolidado no ADR 0008, para não re-litigar 'isso foi avaliado?'. |  |
| CICLOS-A-010 | maestro:specs/010-estudo-superpowers/spec.md @ 080dced | Ciclo 010: estudo hands-on do Superpowers (fork em 44c9b2d) que vira o Apêndice B, com vereditos propostos e a tensão HARD-GATE universal × raias; cumpre a reavaliação prevista no ADR 0008 quando o gatilho disparou. |  |
| CICLOS-A-012 | maestro:specs/012-panorama-templates/spec.md @ 53c71dc | Ciclo 012: Apêndice C, panorama exploratório de templates com triagem (hands-on com gatilho / observar / fora do problema), formalizando o funil de avaliação exploratório → gatilho → hands-on → absorção por gate. |  |
| DECISOES-034 | maestro:docs/records/decisoes.jsonl#gate-010-vereditos | Tema absorções aprovadas: o Steward aprova as absorções do estudo do maestro-02 e os vereditos do Apêndice B (Superpowers: 5 absorções + 2 descartes). |  |
| DECISOES-085 | maestro:docs/records/decisoes.jsonl#decisao-073-gauntlet-area-administrativa | Gauntlet do 073: 25 plataformas × 26 funcionalidades, confronto 16/5/11, wireframes e três juízes em contexto fresco. |  |
| DECISOES-100 | maestro:docs/roadmap.md#F7 | F7: estudos de campo — apêndices A (maestro-02), B (Superpowers) e C (panorama). |  |
| DECISOES-123 | maestro:docs/ecosystem/fontes.md | Fontes avaliadas com licença e data; licenças não permissivas são citáveis, não copiáveis. |  |
| DECISOES-156 | maestro:docs/ecosystem/ideias/032-workflow-de-comandos-generico.md | Ideia 032 (catlog22): workflow genérico — descartar. |  |
| DECISOES-166 | maestro:docs/research/avaliacao-ecossistema-sdd.md | Pesquisa do ecossistema SDD com quadro de vereditos — base do ADR 0008. |  |
| LIVRO-METODO-123 | livro:maestro-handbook/handbook/apendice-a-maestro-02.md | Estudo de campo de 2026-07-31 do maestro-02 (fork de sharpdeveye/maestro, v2.0.0, MIT): instrumento instalavel em 10 providers, sem papeis nem gates humanos; adocao integral descartada. |  |
| LIVRO-METODO-124 | livro:maestro-handbook/handbook/apendice-a-maestro-02.md §1 | Memoria persistente como camada explicita (.maestro/ com context.md, decisions.jsonl, audit.jsonl, sessions/), absorvida como registro consultavel por agente. |  |
| LIVRO-METODO-125 | livro:maestro-handbook/handbook/apendice-a-maestro-02.md §2 | Trilha de auditoria com custo por invocacao (command, duration_ms, cost_estimate_usd, exit_status) em JSONL, observada como primeiro degrau da telemetria. |  |
| LIVRO-METODO-126 | livro:maestro-handbook/handbook/apendice-a-maestro-02.md §3 | /reflect como retro executavel (scorecard de skills, taxa de conclusao, custo), absorvido como scripts/retro.sh. |  |
| LIVRO-METODO-127 | livro:maestro-handbook/handbook/apendice-a-maestro-02.md §4 | Wave-engine (map -> validate -> scaffold -> test com ValidationResult entre fases) confirma que fases com gate convergem em qualquer granularidade. |  |
| LIVRO-METODO-128 | livro:maestro-handbook/handbook/apendice-a-maestro-02.md §5 | Context-slicer reporta tokenEstimate vs fullTokenEstimate: absorvido o conceito de medir a economia de contexto. |  |
| LIVRO-METODO-129 | livro:maestro-handbook/handbook/apendice-a-maestro-02.md §6 | Catalogo de anti-padroes de execucao ('workflow slop') absorvido como skill anti-patterns alimentada por retros (spec 008). |  |
| LIVRO-METODO-131 | livro:maestro-handbook/handbook/apendice-b-superpowers.md | Estudo hands-on do Superpowers (obra/superpowers v6.2.0, MIT): 14 skills, bootstrap por hooks, forca linguistica; adocao integral descartada como segunda fonte de verdade. |  |
| LIVRO-METODO-141 | livro:maestro-handbook/handbook/apendice-c-panorama-templates.md | Funil de avaliacao do ecossistema: exploratorio -> gatilho -> estudo hands-on -> absorcao por gate, com triagem candidato/observar/fora do problema. |  |
| LIVRO-METODO-142 | livro:maestro-handbook/handbook/apendice-c-panorama-templates.md §A | claude-code-spec-workflow (Pimzino): trilhas feature e bug-fix validam externamente as raias e o Analyze antes do Fix; observar. |  |
| LIVRO-METODO-143 | livro:maestro-handbook/handbook/apendice-c-panorama-templates.md §A | CCPM (Claude Code Project Manager): rastreabilidade via GitHub Issues e execucao paralela; hands-on com gatilho de projeto multi-dev. |  |
| LIVRO-METODO-144 | livro:maestro-handbook/handbook/apendice-c-panorama-templates.md §A | Claude-Code-Workflow (catlog22): orquestracao multi-CLI, fora do problema. |  |
| LIVRO-METODO-145 | livro:maestro-handbook/handbook/apendice-c-panorama-templates.md §B | PRP (Product Requirement Prompt, Wirasm): contexto de codebase empacotado na spec; hands-on com gatilho do primeiro ciclo regendo codigo de produto. |  |
| LIVRO-METODO-146 | livro:maestro-handbook/handbook/apendice-c-panorama-templates.md §B | Cline Memory Bank e context-forge observados: retro.sh, registro e new-cycle.sh ja cobrem; reavaliar se sessoes multi-dia doerem. |  |
| LIVRO-METODO-147 | livro:maestro-handbook/handbook/apendice-c-panorama-templates.md §C | claude-flow (orquestracao pesada) fora por ora pela menor autonomia que resolve; Google ADK/Gemini observado so se houver nuvem gerenciada. |  |
| LIVRO-METODO-148 | livro:maestro-handbook/handbook/apendice-c-panorama-templates.md §D | Colecoes e marketplaces tratados como fonte de garimpo por dor especifica (via research-curator), nao como framework. |  |
| GOV-077 | maestro:docs/governance/glossary.md | BMAD-METHOD avaliado e rejeitado no ciclo 007 (ADR 0008): uma metodologia concorrente inteira criaria uma segunda fonte de verdade. |  |
| GOV-168 | maestro:scripts/check-ecosystem.sh @ e73ee0d | check-ecosystem.sh: catálogo de terceiros com a ideia como unidade, momento separado de estado, e absorção exigindo destino real; nasceu porque duas ideias do ADR 0008 ficaram 39 ciclos registradas como absorvidas sem existir no disco. | sim |
| GOV-194 | maestro:.specify/templates/evaluation-template.md | Template do cartão de avaliação de ideia de FORA do projeto (docs/ecosystem/ideias/, lido por check-ecosystem.sh): a unidade é a ideia, não a ferramenta; absorver exige destino concreto. |  |

## Itens SECUNDÁRIOS (38) — o capítulo principal é outro; cite ou remeta quando servir ao argumento

| id | fonte | resumo | principal |
|---|---|---|---|
| CICLOS-B-036 | maestro:specs/066-painel-de-coordenacao-v0/spec.md | Ciclo 066 v0: painel localhost que projeta os arquivos, spec retroativa do código Hindiana (16 sessões, ~160 worktrees, 52 desvios em três dias); supera em parte o dashboard YAGNI. | 3 |
| CICLOS-B-044 | maestro:specs/070-conferidor-ordem-veredito/00-chamado.md | Evidência importada do Hindiana: chamado rodado com gates G0–G3 e requisitos EARS; isenta pela forma no check-conformance.sh. | 4 |
| CICLOS-A-065 | maestro:specs/036-pesquisa-upstream-decomposicao/spec.md @ 01ccea1 | Ciclo 036: pesquisa do upstream (decompor projeto grande em ciclos) — 20 de 34 specs nasceram de pedido pontual, o Spec Kit não tem upstream (confirmado comando a comando), proposta em 'um objeto, um verbo e um portão' e recomendação de não construir sem dor real. | 6 |
| CICLOS-A-066 | maestro:specs/036-pesquisa-upstream-decomposicao/qa-report.md @ 01ccea1 | Falha real (evitada por pouco): o catálogo mais útil encontrado (70 skills de produto) era CC BY-NC-SA, incompatível com a distribuição; virou regra verificar licença antes de propor uso. | 12 |
| CICLOS-A-080 | maestro:specs/042-conformidade-executavel/spec.md @ d6ffbb2 | Falha real de campo: uma agente num repositório vizinho admitiu não ter seguido o Maestro — o plan.md parava em 'docs e fitness verdes', a compactação de contexto promoveu a versão truncada e ela obedeceu com fidelidade; o método instalado era cópia com perda. | 5 |
| DECISOES-005 | maestro:docs/adr/0008-avaliacao-ecossistema-sdd.md | ADR 0008: mantém o Spec Kit como ferramenta SDD única; BMAD descartado, Kiro descartado como ferramenta (lock-in de IDE), Superpowers não adotado por atacado; absorve EARS e outras ideias com destino concreto. | 12 |
| DECISOES-058 | maestro:docs/records/decisoes.jsonl#achado-047-cinco-absorcoes-sem-destino · commit e73ee0d | Cinco ideias registradas como absorver nunca chegaram a arquivo; reclassificadas para observar com gatilho. | 12 |
| DECISOES-090 | maestro:docs/records/decisoes.jsonl#decisao-074-gauntlet-maestri | Barra do redesenho por gauntlet-loop contra um produto real (Maestri), seis peças, crítico às cegas. | 15 |
| DECISOES-095 | maestro:docs/records/decisoes.jsonl#decisao-076-control-plane-v2 | Cinco análises de control plane (Paperclip, CompozyOS, AgentConnect, ACP, A2A): construir, padrões nas bordas, nenhum produto como base. | 12 |
| DECISOES-107 | maestro:docs/roadmap.md#F22 | F22: catálogo do ecossistema (30 cards, 18 fontes, check-ecosystem.sh) achou duas absorções fantasma. | 12 |
| DECISOES-122 | maestro:docs/ecosystem/README.md | Catálogo do ecossistema: ideia como unidade, momento separado de estado, vocabulário fechado com prova/gatilho, check-ecosystem.sh. | 12 |
| DECISOES-124 | maestro:docs/ecosystem/estado.jsonl | Veredito corrente por ideia: 52 linhas append-only; a última de cada id manda. | 14 |
| DECISOES-127 | maestro:docs/ecosystem/ideias/003-worktree-por-task.md | Ideia 003 (Superpowers): worktree por task — observar com gatilho de conflito real. | 6 |
| DECISOES-128 | maestro:docs/ecosystem/ideias/004-standards-por-camada.md | Ideia 004 (Agent OS): standards por camada — observar. | 5 |
| DECISOES-133 | maestro:docs/ecosystem/ideias/009-ide-proprietaria-spec-first.md | Ideia 009 (Kiro): IDE proprietária — descartar. | 12 |
| DECISOES-134 | maestro:docs/ecosystem/ideias/010-adocao-integral-de-metodologia.md | Ideia 010 (BMAD): metodologia inteira — descartar. | 7 |
| DECISOES-139 | maestro:docs/ecosystem/ideias/015-skills-de-gestao-de-produto.md | Ideia 015: skills de produto — descartar pela licença CC BY-NC-SA. | 12 |
| DECISOES-144 | maestro:docs/ecosystem/ideias/020-fluxo-spec-em-comandos.md | Ideia 020 (Pimzino): fluxo em comandos — descartar. | 4 |
| DECISOES-145 | maestro:docs/ecosystem/ideias/021-baixa-cerimonia-para-mudanca-simples.md | Ideia 021 (GSD, OpenSpec): baixa cerimônia — descartar. | 4 |
| LIVRO-METODO-029 | livro:maestro-handbook/handbook/03-spec-driven.md §5.4 | OpenSpec (Fission-AI) descartado como segunda ferramenta; a ideia do delta foi absorvida como raia leve (ADR 0005). | 4 |
| LIVRO-METODO-030 | livro:maestro-handbook/handbook/03-spec-driven.md §5.4 | Kiro, Tessl e 'specs as source of truth' observados sem adocao (ADR 0008); prompt ad-hoc rejeitado. | 4 |
| LIVRO-METODO-130 | livro:maestro-handbook/handbook/apendice-a-maestro-02.md | Servidor MCP do maestro-02 (25 prompts, 10 tools, 8 resources) distribui skills como servico, arquitetura fonte-unica -> adaptadores. | 12 |
| LIVRO-METODO-132 | livro:maestro-handbook/handbook/apendice-b-superpowers.md §1 | Enforcement linguistico 'Iron Law' com 'violar a letra e violar o espirito' absorvido nas skills do Maestro (spec 011). | 7 |
| LIVRO-METODO-133 | livro:maestro-handbook/handbook/apendice-b-superpowers.md §2 | TDD para skills: rodar subagente sem a skill (RED), escrever a skill (GREEN), fechar brechas (REFACTOR); absorvido como protocolo no skill-author. | 7 |
| LIVRO-METODO-134 | livro:maestro-handbook/handbook/apendice-b-superpowers.md §3 | systematic-debugging ('no fixes without root cause') absorvido como skill diagnose-before-fix, lacuna real do Maestro. | 7 |
| LIVRO-METODO-135 | livro:maestro-handbook/handbook/apendice-b-superpowers.md §4 | Review por task alem do review por ciclo: absorvido em parte como checkpoint leve na raia plena com mais de tres tasks. | 2 |
| LIVRO-METODO-136 | livro:maestro-handbook/handbook/apendice-b-superpowers.md §5 | 'Assuma zero contexto' nos planos (tasks autossuficientes de 2-5 min) absorvido no tasks-template. | 5 |
| LIVRO-METODO-137 | livro:maestro-handbook/handbook/apendice-b-superpowers.md §6 | Continuous execution (nao perguntar 'continuo?') validada: atencao humana se gasta em gates, nao em progresso. | 3 |
| LIVRO-METODO-138 | livro:maestro-handbook/handbook/apendice-b-superpowers.md §7 | Worktrees por task mantidas em observacao com gatilho de dor de paralelismo. | 6 |
| LIVRO-METODO-139 | livro:maestro-handbook/handbook/apendice-b-superpowers.md §8 | Bootstrap por hook de sessao inspirou o paragrafo 'skills primeiro' no CLAUDE.md (enforcement estrutural de consulta as skills). | 12 |
| LIVRO-METODO-140 | livro:maestro-handbook/handbook/apendice-b-superpowers.md | Tensao HARD-GATE universal x raias: o Superpowers exige design para tudo; o Maestro mantem a raia leve (ADR 0005) e absorve so o aviso 'na duvida, plena'. | 4 |
| LIVRO-METODO-172 | livro:maestro-handbook/handbook/apresentacao-desenvolvimento-maestro.html | check-ecosystem: ideia 'absorvida' aponta o arquivo que prova, e veredito 'observar' sem gatilho e recusado. | 14 |
| LIVRO-METODO-312 | livro:pesquisa/base-de-pesquisa.md §Referencias | Google ADK. | 12 |
| GOV-053 | maestro:docs/governance/operating-model.md | O que NÃO adotamos (§10): Scrum completo, backlog formal, segundo toolkit spec-driven (OpenSpec avaliado e descartado, absorvido o modelo delta), RFC pesado, diagramas formais e estimativa de prazo. | 14 |
| GOV-076 | maestro:docs/governance/glossary.md; maestro:.specify/templates/spec-template.md | EARS ('WHEN <condição> THE SYSTEM SHALL <comportamento observável>'): requisito que vira teste quase 1:1, absorvido do Kiro no ciclo 007 (ADR 0008); vive em verifiable-dod e no template de spec. | 4 |
| GOV-088 | maestro:CLAUDE.md @ 2534eaa | Iron Law como forma: toda skill traz a regra inegociável com as brechas fechadas ('violar a letra viola o espírito'), absorvida do Superpowers no ciclo 011; e 'skills primeiro' como enforcement: havendo chance razoável, a skill comanda. | 7 |
| GOV-129 | maestro:.claude/agents/research-curator.md | Agente research-curator: pesquisa boa prática com FONTES CITADAS e traz evidência externa às decisões; não decide arquitetura. | 7 |
| GOV-144 | maestro:.specify/UPSTREAM.md | Proveniência do Spec Kit vendorizado (ciclo 009): upstream github/spec-kit 0.4.3 e fork GHDaru/spec-kit; cada peça marcada com estado (UP:state=adapted); vendorizar faz do conteúdo fonte própria, consultando o upstream por decisão. | 4 |
