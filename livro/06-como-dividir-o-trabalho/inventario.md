# Inventário do capítulo 6

Gerado de `pesquisa/inventario/itens.json` (02/11/2026).

## Itens PRINCIPAIS (28) — cada um tem de estar coberto neste capítulo

| id | fonte | resumo | falha real |
|---|---|---|---|
| CICLOS-B-037 | maestro:specs/066-painel-de-regencia/plan.md | Ciclo 066 guarda-chuva: coordenação da integração da linha paralela Hindiana (filhos 066 v0, 067–070, 072) e o lançador multi-sessão com Gerente e Worker01–06. |  |
| CICLOS-B-038 | maestro:specs/NNN-painel-de-coordenacao-v0/spec.md | Spec com número pendente da mesma entrega do 066 v0; com as pastas gêmeas 066 e 070 e a renumeração 064→065, mostra a colisão de numeração em linhas paralelas. |  |
| CICLOS-B-054 | maestro:specs/075-protocolo-entre-sessoes/spec.md | Ciclo 075: protocolo próprio entre sessões (envelope interno, identidade nome · projeto, ref como localizador, contextId só na borda A2A, SSE), redesenhado pela V2 das bancas. |  |
| CICLOS-A-043 | maestro:specs/025-capitulo-05-padrao-v2/spec.md @ c47ea48 | Ciclo 025: capítulo 05 (orquestração) no padrão v2 dizendo quais padrões foram usados — encadeamento fixo dominante, avaliador-otimizador em 4 ciclos, padrão autônomo nunca usado em 25 ciclos (regra da menor autonomia). |  |
| CICLOS-A-065 | maestro:specs/036-pesquisa-upstream-decomposicao/spec.md @ 01ccea1 | Ciclo 036: pesquisa do upstream (decompor projeto grande em ciclos) — 20 de 34 specs nasceram de pedido pontual, o Spec Kit não tem upstream (confirmado comando a comando), proposta em 'um objeto, um verbo e um portão' e recomendação de não construir sem dor real. |  |
| DECISOES-081 | maestro:docs/records/decisoes.jsonl#ciclo-066-integra-painel-controle | 066 inicia seis ciclos de integração da linha paralela (42 branches), merge --no-ff preservando histórico. |  |
| DECISOES-113 | maestro:docs/roadmap.md#upstream-outcome | Gatilho: outcome + skill de corte + check-outcomes.sh só na primeira intenção grande real. |  |
| DECISOES-127 | maestro:docs/ecosystem/ideias/003-worktree-por-task.md | Ideia 003 (Superpowers): worktree por task — observar com gatilho de conflito real. |  |
| DECISOES-135 | maestro:docs/ecosystem/ideias/011-grafo-de-dependencias-de-tasks.md | Ideia 011 (Taskmaster): grafo de dependências — observar. |  |
| DECISOES-146 | maestro:docs/ecosystem/ideias/022-decomposicao-em-tres-passadas.md | Ideia 022 (Product-Manager-Skills): três passadas — observar. |  |
| DECISOES-157 | maestro:docs/ecosystem/ideias/033-padroes-de-fatiamento.md | Ideia 033 (Lawrence, SPIDR): padrões de fatiamento — observar. |  |
| DECISOES-158 | maestro:docs/ecosystem/ideias/034-fatia-vertical-invest.md | Ideia 034 (INVEST): fatia vertical — observar. |  |
| DECISOES-159 | maestro:docs/ecosystem/ideias/035-contrato-por-fatia.md | Ideia 035: contrato por fatia — observar. |  |
| DECISOES-161 | maestro:docs/ecosystem/ideias/037-decompose-feature-em-issues.md | Ideia 037 (skill decompose): issues do tamanho de um agente — descartar. |  |
| DECISOES-170 | maestro:docs/research/upstream-decomposicao.md | Pesquisa do upstream (036): gap medido e proposta outcome/slice-outcome/check-outcomes adiada por gatilho. |  |
| LIVRO-METODO-045 | livro:maestro-handbook/handbook/05-orquestracao.md §3 | Map-reduce cognitivo: o reduce nao e concatenacao, e julgamento com contexto global, e pertence ao orquestrador (humano). |  |
| LIVRO-METODO-046 | livro:maestro-handbook/handbook/05-orquestracao.md §5.1 | O corte e mais traicoeiro que o reduce: paralelizar por fronteira (contexto delimitado, contrato, camada), nunca por quantidade; nenhuma reconciliacao salva fatia cortada fora da costura. |  |
| LIVRO-METODO-047 | livro:maestro-handbook/handbook/05-orquestracao.md §5.2 | Espectro fluxo <-> agente e regra da menor autonomia que resolve: comecar pelo fluxo fixo e so adicionar autonomia quando o simples comprovadamente falhar. |  |
| LIVRO-METODO-049 | livro:maestro-handbook/handbook/05-orquestracao.md §5.4 | Seis padroes (Anthropic, Building effective agents) mapeados no metodo: encadeamento=fluxo specify..implement, roteamento=raias, paralelizacao=subagentes, orquestrador-trabalhadores, avaliador-otimizador=escritor/revisor, autonomo=evitado. |  |
| LIVRO-METODO-050 | livro:maestro-handbook/handbook/05-orquestracao.md §6 | Encadeamento fixo vive em 11 comandos versionados em .claude/commands (speckit.* e dod): ninguem decide como trabalhar, so o que fazer. |  |
| LIVRO-METODO-052 | livro:maestro-handbook/handbook/05-orquestracao.md §6 | Em 25 ciclos, zero uso do padrao autonomo e quase nenhuma paralelizacao massiva de subagentes: o trabalho coube num encadeamento com verificacao. |  |
| LIVRO-METODO-138 | livro:maestro-handbook/handbook/apendice-b-superpowers.md §7 | Worktrees por task mantidas em observacao com gatilho de dor de paralelismo. |  |
| LIVRO-METODO-280 | livro:pesquisa/base-de-pesquisa.md §Agenda metricas | Metrica: overhead de coordenacao. |  |
| LIVRO-METODO-310 | livro:pesquisa/base-de-pesquisa.md §Referencias | LangGraph. |  |
| LIVRO-METODO-311 | livro:pesquisa/base-de-pesquisa.md §Referencias | CrewAI. |  |
| GOV-070 | maestro:docs/governance/glossary.md | Rodada, passo e outbox (ciclo 070): execução do workflow gravada passo a passo em SQLite; passo sem saída bloqueia o próximo; fila SQLite (WAL) para mensagens entre sessões sem broker. |  |
| GOV-099 | maestro:skills/anti-patterns/SKILL.md | Anti-padrão 4. Multiagente para problema de um agente: orquestração custa handoffs e reconciliação; use a menor autonomia que resolve. |  |
| GOV-142 | maestro:.claude/commands/speckit.taskstoissues.md | Comando /speckit.taskstoissues: converte tarefas em issues do GitHub ordenadas por dependência. |  |

## Itens SECUNDÁRIOS (35) — o capítulo principal é outro; cite ou remeta quando servir ao argumento

| id | fonte | resumo | principal |
|---|---|---|---|
| CICLOS-B-057 | maestro:specs/076-padroes-de-engenharia-e-react/sintese-das-bancas.md | Síntese das bancas de arquitetura e UX (A1–A15) e a V2 do estudo de Agent Control Plane; síntese prevalece sobre briefing e V2 sobre v1. | 7 |
| DECISOES-014 | maestro:docs/adr/0017-divisao-em-dois-repositorios.md | ADR 0017: propôs dividir em toolkit (máquina, 282 arquivos) e guia (pessoa, 79 arquivos), memória no toolkit; superado pelo 0018 antes de qualquer execução. | 9 |
| DECISOES-015 | maestro:docs/adr/0018-fronteira-interna-em-vez-de-divisao.md | ADR 0018: a medição (20% de acoplamento substantivo, 0 arquivos do guia no instalador, 0 tags) reverteu o corte; fronteira interna em boundary.json com gatilhos observáveis para reabrir. | 9 |
| DECISOES-029 | maestro:docs/adr/0032-dono-do-processo-fora-do-servidor-web.md | ADR 0032: o dono do processo das sessões nunca é o servidor web; job object que mata é proibido; prova = matar o servidor e ver as sessões vivas. | 9 |
| DECISOES-077 | maestro:docs/records/decisoes.jsonl#decisao-066-sessoes-via-gateway | Construtores do 066 via gateway por consenso de três pareceres; token fora do repositório, sem copiar permissions/hooks do Hindiana. | 12 |
| DECISOES-095 | maestro:docs/records/decisoes.jsonl#decisao-076-control-plane-v2 | Cinco análises de control plane (Paperclip, CompozyOS, AgentConnect, ACP, A2A): construir, padrões nas bordas, nenhum produto como base. | 12 |
| DECISOES-142 | maestro:docs/ecosystem/ideias/018-frota-de-agentes.md | Ideia 018 (claude-flow): frota de agentes — observar até a atenção humana governar. | 3 |
| DECISOES-148 | maestro:docs/ecosystem/ideias/024-assuma-zero-contexto.md | Ideia 024 (Superpowers): assuma zero contexto — absorver no tasks-template. | 5 |
| DECISOES-150 | maestro:docs/ecosystem/ideias/026-gates-em-nivel-de-task.md | Ideia 026 (maestro-02): gates em nível de task — absorver. | 11 |
| LIVRO-METODO-036 | livro:maestro-handbook/handbook/04-fluxo-agentic-contexto.md §5.1 | Quatro praticas, uma restricao: explorar-planejar-codar comprime, subagente le em janela propria, /clear descarta ruido, revisor fresco comeca com orcamento inteiro. | 5 |
| LIVRO-METODO-037 | livro:maestro-handbook/handbook/04-fluxo-agentic-contexto.md §5.2 | Reset demais e amnesia e delegar tudo produz otimo local; o contexto certo preserva objetivo, invariantes e contratos (a spec e o contexto integrador). | 5 |
| LIVRO-METODO-038 | livro:maestro-handbook/handbook/04-fluxo-agentic-contexto.md §4 | Economia de contexto medida, nao afirmada: economia consistentemente baixa ao fatiar e sinal de corte errado, nao de contexto pequeno. | 5 |
| LIVRO-METODO-044 | livro:maestro-handbook/handbook/04-fluxo-agentic-contexto.md §5.4 | Um agente generalista gigante rejeitado (janela cheia degrada, prompt cresce sem limite); revisao adversarial do diff adotada como gate antes do merge. | 7 |
| LIVRO-METODO-048 | livro:maestro-handbook/handbook/05-orquestracao.md §5.3 | Boa arquitetura empurra o trabalho para o lado barato e previsivel do espectro: investir em fronteira e comprar previsibilidade. | 9 |
| LIVRO-METODO-051 | livro:maestro-handbook/handbook/05-orquestracao.md §6; maestro commit 0021b20 | Avaliador-otimizador como portao provado falhando: qa-reports dos ciclos 017, 018, 020 e 021; no ciclo 020 o laco rodou quatro vezes e cada volta achou um formato de link que o portao ignorava. | 10 |
| LIVRO-METODO-064 | livro:maestro-handbook/handbook/07-cerimonias-cadencia.md §4 | Paralelize dentro de uma feature ja decidida, nao entre features ambiguas; para escalar, barateie o gate em vez de abrir frentes. | 3 |
| LIVRO-METODO-095 | livro:maestro-handbook/handbook/10-gates-classes-de-risco.md §4 | Fases com gate valem em qualquer granularidade, do ciclo a tarefa de minutos. | 10 |
| LIVRO-METODO-116 | livro:maestro-handbook/handbook/13-decisoes-de-engenharia.md §5.6 | Corte por fronteira (DDD / arquitetura hexagonal): paralelizar por bounded context gera independencia; cortar bem e dificil e corte ruim aparece como economia baixa ou retrabalho. | 8 |
| LIVRO-METODO-127 | livro:maestro-handbook/handbook/apendice-a-maestro-02.md §4 | Wave-engine (map -> validate -> scaffold -> test com ValidationResult entre fases) confirma que fases com gate convergem em qualquer granularidade. | D |
| LIVRO-METODO-135 | livro:maestro-handbook/handbook/apendice-b-superpowers.md §4 | Review por task alem do review por ciclo: absorvido em parte como checkpoint leve na raia plena com mais de tres tasks. | 2 |
| LIVRO-METODO-136 | livro:maestro-handbook/handbook/apendice-b-superpowers.md §5 | 'Assuma zero contexto' nos planos (tasks autossuficientes de 2-5 min) absorvido no tasks-template. | 5 |
| LIVRO-METODO-147 | livro:maestro-handbook/handbook/apendice-c-panorama-templates.md §C | claude-flow (orquestracao pesada) fora por ora pela menor autonomia que resolve; Google ADK/Gemini observado so se houver nuvem gerenciada. | D |
| LIVRO-METODO-253 | livro:pesquisa/base-de-pesquisa.md §Agenda H4 | H4: multiagente so ajuda com cortes independentes. | 15 |
| LIVRO-METODO-299 | livro:pesquisa/base-de-pesquisa.md §Referencias | MetaGPT (Hong et al.). | 7 |
| GOV-006 | maestro:docs/governance/principles.md | Princípio V, economia de contexto e corte por fronteira: preservar o contexto integrador (a spec), paralelizar por bounded context e usar a menor autonomia que resolve (fluxo fixo antes de agente autônomo). | 5 |
| GOV-015 | maestro:docs/governance/axioms.md | A3, o contexto é finito e degrada ao encher: propriedade física da ferramenta, que justifica fatiar, resetar contexto e manter o agente estreito. | 5 |
| GOV-064 | maestro:docs/governance/glossary.md | Colisão de endereço: o mesmo identificador apontando para duas sessões ou nenhuma; invariante de que endereço ambíguo é recusado, nunca resolvido, porque entrega ao par errado não se desfaz. | 8 |
| GOV-080 | maestro:docs/governance/task-ledger.md | Protocolo de tags [[TASK ...]] / [[DONE ...]]: tag sozinha na linha; contam o primeiro TASK e o último DONE da mensagem; auditoria carrega target e verdict; é o contrato entre sessão gerente e workers. | 3 |
| GOV-105 | maestro:skills/anti-patterns/SKILL.md | Anti-padrão 10. Mudança de escopo silenciosa: o agente 'aproveita' para refatorar; diff pequeno e problema maior vira registro. | 4 |
| GOV-137 | maestro:.claude/commands/speckit.tasks.md | Comando /speckit.tasks: gera tasks.md ordenado por dependência a partir dos artefatos de design. | 4 |
| GOV-138 | maestro:.claude/commands/speckit.implement.md | Comando /speckit.implement: executa o plano processando as tarefas de tasks.md. | 4 |
| GOV-143 | maestro:.claude/commands/speckit.converge.md | Comando /speckit.converge (do fork da casa, ciclo 009): compara o repositório real com spec/plan/tasks e ANEXA o trabalho faltante como tarefas novas, nunca reescreve. | 4 |
| GOV-167 | maestro:scripts/check-boundary.sh | check-boundary.sh: a fronteira entre os dois domínios do repositório é decidível (cada arquivo com exatamente um domínio, caminho compartilhado com dono, nada chega ao site por caminho não declarado), cobrindo todo canal de publicação. | 9 |
| GOV-181 | maestro:scripts/multi-session.py | Lançador multissessão (ciclo 066): abre as sessões do ciclo no Windows Terminal com --model por sessão (gerente num modelo, workers noutro), uma git worktree por worker para isolar edições, e nenhum segredo no repositório. | 3 |
| GOV-200 | maestro:boundary.json | Fronteira interna entre dois domínios num repositório só: toolkit (lido por máquina) e guide (o livro, lido por gente), com caminhos compartilhados declarados; ADR 0018 superou o ADR 0017 depois de medir que só 20% dos commits acoplam as duas metades. | 9 |
