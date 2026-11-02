# Inventário do capítulo 13

Gerado de `pesquisa/inventario/itens.json` (02/11/2026).

## Itens PRINCIPAIS (31) — cada um tem de estar coberto neste capítulo

| id | fonte | resumo | falha real |
|---|---|---|---|
| CICLOS-B-033 | maestro:specs/065-o-metodo-se-cobra-e-bate-o-ponto/spec.md · commit dda2225 | Ciclo 065: autocobrança por hook Stop e ponto de tarefas ([[TASK]]/[[DONE]] com tokens e custo); renumerado de 064, mantendo ids 064-* no livro só-acréscimo. |  |
| CICLOS-B-034 | maestro:docs/records/tarefas.jsonl | Livro de ponto append-only: eventos assigned/start/stop com tentativa, redoes, desfecho, duração, tokens por modelo e cost_usd; 52 linhas do ciclo 064/065. |  |
| CICLOS-A-036 | maestro:specs/022-capitulo-02-padrao-v2/spec.md @ bf90f63 | Ciclo 022: capítulo 02 (DORA/SPACE) no padrão v2 com as quatro métricas DORA lidas do próprio repositório, incluindo a ruim (change fail rate), e a Iron Law editorial vira executável em verificar-capitulos.sh. |  |
| DECISOES-030 | maestro:docs/adr/0033-opentelemetry-como-projecao-do-log.md | ADR 0033: OpenTelemetry é projeção do log, não dependência; só nomes de campos de custo GenAI agora; exportador OTLP só com primeiro consumidor real, nunca o conteúdo da mensagem. |  |
| DECISOES-080 | maestro:docs/records/decisoes.jsonl#decisao-066-d4-custo-privacidade | custo.py grava só contagens de tokens em SQLite local ignorado pelo git; nada chega ao HTTP. |  |
| DECISOES-087 | maestro:docs/records/decisoes.jsonl#decisao-073-teto-60 | Teto de consumo elevado de 40% para 60% do semanal após a rodada de juízes chegar a 39%. |  |
| DECISOES-153 | maestro:docs/ecosystem/ideias/029-trilha-de-auditoria-com-custo.md | Ideia 029 (maestro-02): trilha com custo — observar. |  |
| LIVRO-METODO-013 | livro:maestro-handbook/handbook/02-dora-space.md §5.1 | As quatro metricas DORA so informam aos pares (throughput: frequencia, lead time; estabilidade: change fail rate, tempo de recuperacao). |  |
| LIVRO-METODO-014 | livro:maestro-handbook/handbook/02-dora-space.md §5.2 | Outcome nao e acionavel, capacidade e: lead time cai mudando CI, trunk-based, testes, revisao e deploys pequenos, nao cobrando o numero. |  |
| LIVRO-METODO-016 | livro:maestro-handbook/handbook/02-dora-space.md §4 | DORA e bussola, nao painel: instrumentar metricas foi adiado por YAGNI porque sem base de comparacao o painel e debito. |  |
| LIVRO-METODO-017 | livro:maestro-handbook/handbook/02-dora-space.md §5.4 | SPACE adotado como referencia e DX Core 4 observado (gameabilidade de 'PRs por pessoa'); painel instrumentado de DORA rejeitado agora. |  |
| LIVRO-METODO-018 | livro:maestro-handbook/handbook/02-dora-space.md §6 | Frequencia de entrega lida do proprio repositorio: 17 gate-main em decisoes.jsonl em tres dias (31/07-02/08), cada ciclo entrando em um commit no mesmo dia. |  |
| LIVRO-METODO-020 | livro:maestro-handbook/handbook/02-dora-space.md §6 | Tempo de recuperacao: zero reversoes no historico; todo defeito foi corrigido avancando no ciclo seguinte. |  |
| LIVRO-METODO-021 | livro:maestro-handbook/handbook/02-dora-space.md §7 | Metrica virando meta (Goodhart) e medir um par so sao os anti-padroes de medicao; ataque a capacidade, nao o numero. |  |
| LIVRO-METODO-197 | livro:maestro-handbook/receitas/instalar-o-maestro.md | Livro de ponto opcional (mod maestro-ledger): registra inicio e fim das tarefas [[TASK]]/[[DONE]] com tokens por requisicao em livro append-only, com limites declarados. |  |
| LIVRO-METODO-211 | livro:maestro-handbook/diagramas/06-fluxo-v5-proposta.md; maestro commit 9be9c3f | Lacuna 3: aprendizados sim, metricas nao; o qa-report fecha com narrativa e sem numero por escolha declarada (metrics dashboard YAGNI). | sim |
| LIVRO-METODO-275 | livro:pesquisa/base-de-pesquisa.md §Agenda metricas | Metrica: custo por tarefa aceita. |  |
| LIVRO-METODO-276 | livro:pesquisa/base-de-pesquisa.md §Agenda metricas | Metrica: custo do retrabalho. |  |
| LIVRO-METODO-277 | livro:pesquisa/base-de-pesquisa.md §Agenda metricas | Metrica: tokens por tarefa. |  |
| LIVRO-METODO-278 | livro:pesquisa/base-de-pesquisa.md §Agenda metricas | Metrica: tempo de ciclo. |  |
| LIVRO-METODO-282 | livro:pesquisa/base-de-pesquisa.md §Agenda metricas | Metrica: retrabalho. |  |
| LIVRO-METODO-285 | livro:pesquisa/base-de-pesquisa.md §Agenda metricas | Metricas DORA (cinco) como camada de entrega da agenda de pesquisa. |  |
| LIVRO-METODO-290 | livro:pesquisa/base-de-pesquisa.md §No repositorio | Telemetria compativel com OpenTelemetry, com minimizacao de dados (LGPD). |  |
| LIVRO-METODO-295 | livro:pesquisa/base-de-pesquisa.md §Riscos | LGPD e sandbox regulatorio da ANPD. |  |
| LIVRO-METODO-296 | livro:pesquisa/base-de-pesquisa.md §Riscos | Regra: tracing nao e retencao indiscriminada. |  |
| LIVRO-METODO-305 | livro:pesquisa/base-de-pesquisa.md §Referencias | DORA 2025. |  |
| GOV-072 | maestro:docs/governance/glossary.md | Limite de orçamento e emissor do aviso (ciclo 073): teto de consumo executável lido como 'declarar teto + avisar'; a ingestão de uso enfileira aviso ao cruzar o limiar ('aviso tardio, nunca perdido'); o corte fica para depois. |  |
| GOV-074 | maestro:docs/governance/glossary.md | Consumo por agente e custo por sessão (ciclos 068/073): tokens lidos incrementalmente dos transcripts, só contagens e nunca conteúdo, no grão de agente e não só de sessão ou modelo. |  |
| GOV-081 | maestro:docs/governance/task-ledger.md; maestro:scripts/record-task.py | Task ledger docs/records/tarefas.jsonl (ciclo 065): um evento por linha, só anexado, validado contra vocabulários fechados (kinds spec/plan/implement/test/review/audit/fix/docs/research; outcomes delivered/blocked/failed/interrupted/superseded). |  |
| GOV-082 | maestro:docs/governance/task-ledger.md | Limite declarado: no Windows o O_APPEND do Python não é atômico entre processos (no Linux/macOS, 30 linhas de ~2 KB simultâneas intactas); rode um escritor por vez ou aceite linha danificada contada como inválida. |  |
| GOV-084 | maestro:scripts/report-tasks.py | Relatório do ledger: tokens e custo por kind e ciclo, tokens por modelo, aprovação de primeira (só de tarefas audit/review), custo de retrabalho (tentativas >= 2), taxa de cache e órfãos (start sem stop). |  |

## Itens SECUNDÁRIOS (34) — o capítulo principal é outro; cite ou remeta quando servir ao argumento

| id | fonte | resumo | principal |
|---|---|---|---|
| CICLOS-B-036 | maestro:specs/066-painel-de-coordenacao-v0/spec.md | Ciclo 066 v0: painel localhost que projeta os arquivos, spec retroativa do código Hindiana (16 sessões, ~160 worktrees, 52 desvios em três dias); supera em parte o dashboard YAGNI. | 3 |
| CICLOS-B-041 | maestro:specs/068-chamados-gate-a-gate/spec.md | Ciclo 068 (retroativo): um chamado, uma pasta; cada gate, um entregável — a tela deriva o estado dos arquivos e mostra custo por sessão; o estado digitado envelhecia em horas. | 3 |
| CICLOS-B-045 | maestro:specs/070-workflow-sqlite/spec.md | Ciclo 070: cada rodada vira execução de workflow em SQLite, com o hook da sessão gravando entrada, resumo e saída de cada passo. | 5 |
| DECISOES-018 | maestro:docs/adr/0021-o-metodo-se-cobra-e-bate-o-ponto.md | ADR 0021: hook Stop mede conformance --ticked-only e bloqueia uma vez, depois avisa o humano; livro de ponto tarefas.jsonl alimentado por [[TASK]]/[[DONE]] via maestro-ledger. | 10 |
| DECISOES-019 | maestro:docs/adr/0022-painel-de-coordenacao-como-projecao-dos-arquivos.md | ADR 0022: painel de coordenação (stdlib, localhost) com DORA com fonte; SQLite é projeção reconstruída a cada ingestão, única escrita direta é eventos. Não há linha adr-0022 em decisoes.jsonl. | 3 |
| DECISOES-022 | maestro:docs/adr/0025-hooks-de-terceiro-gravando-sqlite.md | ADR 0025 (aceito com ressalva): hooks SessionStart/Stop gravam em tabelas próprias do workflow, nunca nas derivadas; append-only ainda por convenção; hooks são ferramenta, não método. | 12 |
| DECISOES-110 | maestro:docs/roadmap.md#F32-F33 | F32–F33: chamados gate a gate e conferidor pela data. | 10 |
| DECISOES-111 | maestro:docs/roadmap.md#F34-F35 | F34–F35: workflow em SQLite (parcial) e painel de regência rodada 1. | 3 |
| DECISOES-121 | maestro:CHANGELOG.md#Unreleased | [Unreleased] (~1000 linhas) acumula os ciclos 065–076 sem versão fechada desde a v0.3.0. | 14 |
| DECISOES-151 | maestro:docs/ecosystem/ideias/027-economia-de-contexto-medida.md | Ideia 027 (maestro-02): economia de contexto medida — absorver. | 5 |
| DECISOES-169 | maestro:docs/research/resultado-pesquisa-praticas-desenvolvimento-avaliacao.md | Avaliação da pesquisa (base do ADR 0004): spec-driven, sem Scrum, DORA, gate humano + revisão independente. | 1 |
| LIVRO-METODO-015 | livro:maestro-handbook/handbook/02-dora-space.md §5.3 | Tamanho de lote e a alavanca unica que move as quatro metricas; analogia da linha de producao cognitiva, que ao contrario da de Ford tem desfazer barato. | 1 |
| LIVRO-METODO-019 | livro:maestro-handbook/handbook/02-dora-space.md §6; maestro commit bf90f63 | Change fail rate ruim: nove defeitos escaparam para main em 17 promocoes, todos com verificacao verde; nenhum foi pego por revisao, todos quando alguem escreveu um check. | 10 |
| LIVRO-METODO-035 | livro:maestro-handbook/handbook/04-fluxo-agentic-contexto.md §3 | Contexto e orcamento, nao deposito: a janela e finita e degrada enquanto enche; o inimigo e o acumulo, nao a falta. | 5 |
| LIVRO-METODO-038 | livro:maestro-handbook/handbook/04-fluxo-agentic-contexto.md §4 | Economia de contexto medida, nao afirmada: economia consistentemente baixa ao fatiar e sinal de corte errado, nao de contexto pequeno. | 5 |
| LIVRO-METODO-097 | livro:maestro-handbook/handbook/10-gates-classes-de-risco.md §6 | Commits pequenos numa branch mantem quase toda mudanca na classe criacao reversivel: 17 promocoes em tres dias sem dupla aprovacao porque a acao e de classe baixa. | 11 |
| LIVRO-METODO-101 | livro:maestro-handbook/handbook/11-rastreabilidade.md §5.2 | Dois sentidos: para frente e cobertura de intencao, para tras (sintoma -> causa -> porque) e recuperacao, o sentido a otimizar. | 5 |
| LIVRO-METODO-125 | livro:maestro-handbook/handbook/apendice-a-maestro-02.md §2 | Trilha de auditoria com custo por invocacao (command, duration_ms, cost_estimate_usd, exit_status) em JSONL, observada como primeiro degrau da telemetria. | D |
| LIVRO-METODO-128 | livro:maestro-handbook/handbook/apendice-a-maestro-02.md §5 | Context-slicer reporta tokenEstimate vs fullTokenEstimate: absorvido o conceito de medir a economia de contexto. | D |
| LIVRO-METODO-219 | maestro:docs/jornada/072-painel-de-regencia.md | Anti-regras do painel conferidas: vazio e informacao, '-' com motivo nunca valor padrao, nada marcado conferido que foi calculado a mao, veredito original ao lado do normalizado. | 3 |
| LIVRO-METODO-220 | maestro:docs/jornada/072-painel-de-regencia.md; maestro commit 02e434f | R1: derivacao preguicosa sem estado 'carregando' faz o painel frio mostrar vazio que nao e o estado do projeto; o script contorna com aquecimento, a tela nao. | 3 |
| LIVRO-METODO-222 | maestro:docs/jornada/072-painel-de-regencia.md; maestro commit bbfab80 | R8: banner de leitura velha com floor nas horas e round nos minutos gerava '1h60m'; fechado no T16 com o banner vindo pronto do servidor. | 10 |
| LIVRO-METODO-258 | livro:pesquisa/base-de-pesquisa.md §Agenda H9 | H9: modelo menor basta em tarefa estruturada. | 15 |
| LIVRO-METODO-279 | livro:pesquisa/base-de-pesquisa.md §Agenda metricas | Metrica: espera humana. | 3 |
| LIVRO-METODO-280 | livro:pesquisa/base-de-pesquisa.md §Agenda metricas | Metrica: overhead de coordenacao. | 6 |
| LIVRO-METODO-281 | livro:pesquisa/base-de-pesquisa.md §Agenda metricas | Metrica: aceitacao na primeira passada. | 10 |
| LIVRO-METODO-283 | livro:pesquisa/base-de-pesquisa.md §Agenda metricas | Metrica: escape de gate. | 10 |
| LIVRO-METODO-284 | livro:pesquisa/base-de-pesquisa.md §Agenda metricas | Metrica: rendimento da revisao independente. | 2 |
| LIVRO-METODO-291 | livro:pesquisa/base-de-pesquisa.md §No repositorio | Comando maestro inspect-context <ciclo> para inspecionar o contexto de um ciclo. | 5 |
| GOV-032 | maestro:docs/governance/axioms.md | Corolário C8: agente estreito é mais barato que agente capaz: 13 agentes em 267 linhas, de T2 e T5. | 7 |
| GOV-080 | maestro:docs/governance/task-ledger.md | Protocolo de tags [[TASK ...]] / [[DONE ...]]: tag sozinha na linha; contam o primeiro TASK e o último DONE da mensagem; auditoria carrega target e verdict; é o contrato entre sessão gerente e workers. | 3 |
| GOV-083 | maestro:docs/governance/task-ledger.md | Mod maestro-ledger: plugin do Claude Code que assina eventos do motor e transforma as tags no registro de tokens, dinheiro e tentativas; instalado por 'claude plugin install', nunca pelo instalador do método. | 12 |
| GOV-085 | maestro:scripts/check-ledger.sh | Gate hermético do ledger: gravador, relatório, hook de Stop e merge de settings testados em fixtures escritas num diretório temporário, com números esperados calculados à mão; mutação roda numa cópia. | 10 |
| GOV-181 | maestro:scripts/multi-session.py | Lançador multissessão (ciclo 066): abre as sessões do ciclo no Windows Terminal com --model por sessão (gerente num modelo, workers noutro), uma git worktree por worker para isolar edições, e nenhum segredo no repositório. | 3 |
