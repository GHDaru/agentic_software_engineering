# Inventário do capítulo 1

Gerado de `pesquisa/inventario/itens.json` (02/11/2026).

## Itens PRINCIPAIS (12) — cada um tem de estar coberto neste capítulo

| id | fonte | resumo | falha real |
|---|---|---|---|
| CICLOS-B-061 | maestro:specs/076-padroes-de-engenharia-e-react/tasks.md · commit 3719cbd | Corte da v1 (Darú, 01/11): o crítico às cegas sai do caminho de cada fatia e fica um só no fim da v1, mais o gate humano; entram T040, T045 e T047. |  |
| DECISOES-167 | maestro:docs/research/jornada-aprendizado-modelo-operacional.md | Diário de aprendizado dos 12 elementos do modelo operacional, com síntese e meta-insights. |  |
| DECISOES-169 | maestro:docs/research/resultado-pesquisa-praticas-desenvolvimento-avaliacao.md | Avaliação da pesquisa (base do ADR 0004): spec-driven, sem Scrum, DORA, gate humano + revisão independente. |  |
| LIVRO-METODO-015 | livro:maestro-handbook/handbook/02-dora-space.md §5.3 | Tamanho de lote e a alavanca unica que move as quatro metricas; analogia da linha de producao cognitiva, que ao contrario da de Ford tem desfazer barato. |  |
| LIVRO-METODO-150 | livro:maestro-handbook/handbook/apresentacao-executiva-maestro.html | Legado como territorio de maior ROI: economia de contexto, paralelizacao por bounded context e rastreabilidade; comparacao antes x depois declarada direcional. |  |
| LIVRO-METODO-200 | livro:maestro-handbook/diagramas/02-problema-solucao.md | Problema-solucao: sem IA o legado exige duzias de pessoas; com IA sem metodo o agente compila e erra a intencao; o Maestro e o metodo no meio. |  |
| LIVRO-METODO-215 | maestro:docs/jornada/README.md | A Jornada como trilha tutorial: 12 paradas, cada uma com tensao, pergunta que destravou e regra que nasceu, reconstruindo o metodo na ordem em que foi descoberto. |  |
| LIVRO-METODO-229 | maestro:docs/comece-por-aqui.md | A dor em dois extremos (sem IA lento e caro; com IA sem metodo, erra a intencao e apodrece) e a pergunta de origem: se um agente escreve o codigo, o que muda? |  |
| LIVRO-METODO-230 | maestro:docs/comece-por-aqui.md | Quando a maquina executa, o valor migra de digitar para duas coisas humanas: deixar a intencao clara e verificar o resultado. |  |
| LIVRO-METODO-241 | livro:pesquisa/base-de-pesquisa.md §Tese | Tese: o Maestro nao e mais um framework de agentes, e um sistema de governanca operacional (constituicao, raias, papeis, artefatos, gates, ADRs, skills, scripts, hooks) que roda sobre diferentes harnesses e modelos. |  |
| LIVRO-METODO-300 | livro:pesquisa/base-de-pesquisa.md §Referencias | He / Treude / Lo (TOSEM 2025). |  |
| GOV-038 | maestro:docs/governance/operating-model.md | Princípio operacional central (§2): IA para explorar, propor e escrever; humano para especificar, decidir e aprovar; testes, gates e revisão independente para validar. |  |

## Itens SECUNDÁRIOS (9) — o capítulo principal é outro; cite ou remeta quando servir ao argumento

| id | fonte | resumo | principal |
|---|---|---|---|
| CICLOS-A-019 | maestro:specs/016-capitulo-01-padrao-v2/spec.md @ 73c78d6 | Ciclo 016: capítulo 01 migrado ao padrão editorial v2 ('reescrever a forma, preservar o fato'), com o promover-main.sh como exemplo real e a fitness function que falha se uma página do livro não estiver no corpus do companion. | 14 |
| LIVRO-METODO-004 | livro:maestro-handbook/handbook/01-principio-central.md | Principio operacional central: IA explora, propoe e escreve; humano especifica, decide e aprova; testes, gates e revisao independente validam. | 2 |
| LIVRO-METODO-007 | livro:maestro-handbook/handbook/01-principio-central.md §5.3 | Reversibilidade como alavanca: backup, dry-run, homologacao e soft-delete mudam a classe de risco e tornam a acao delegavel; reversibilidade compra velocidade. | 11 |
| LIVRO-METODO-022 | livro:maestro-handbook/handbook/03-spec-driven.md §5.1 | Inversao de dependencia aplicada a documento: a spec passa de descricao a jusante para input a montante que gera o codigo, e por isso nao apodrece. | 4 |
| LIVRO-METODO-023 | livro:maestro-handbook/handbook/03-spec-driven.md §2 | Com agentes, prompt vago gera codigo que compila, passa no teste e erra a intencao, o modo de falha mais caro porque parece sucesso. | 4 |
| LIVRO-METODO-063 | livro:maestro-handbook/handbook/07-cerimonias-cadencia.md §5.3 | WIP e limitado pela atencao humana, nao pela capacidade dos agentes: frentes paralelas funilam pelos mesmos gates humanos. | 3 |
| LIVRO-METODO-149 | livro:maestro-handbook/handbook/apresentacao-executiva-maestro.html | Deck executivo de 10 slides: dois extremos que falham, 12 elementos em 5 camadas, seis pilares e o metodo construido por ele mesmo. | A |
| LIVRO-METODO-198 | livro:maestro-handbook/diagramas/01-definicao.md | Metafora do nome: a partitura (spec) diz o que tocar, o compasso (gates) marca o ritmo, os musicos (agentes) executam; um humano rege, muitos agentes executam. | A |
| GOV-017 | maestro:docs/governance/axioms.md | A5, custo assimétrico entre fazer e desfazer: produzir é barato e cada vez mais; apagar dados, deployar, migrar e publicar não; sem A5 todo ato mereceria o mesmo gate. | 11 |
