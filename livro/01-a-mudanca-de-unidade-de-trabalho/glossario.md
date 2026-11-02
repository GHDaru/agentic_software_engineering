# Glossário do capítulo 1

| termo | definição |
|---|---|
| Unidade de trabalho | O que um time conta como "uma coisa feita" e usa para planejar e medir. Com agentes, desloca-se da mudança escrita para a mudança aceita. |
| Mudança aceita | Alteração que alguém especificou, um mecanismo independente verificou e um humano (ou política escrita por um humano) aceitou integrar. A unidade de trabalho deste livro. |
| Custo por mudança aceita | Soma esperada de gerar, verificar e desfazer, dividida pelas mudanças aceitas. Versão do capítulo para a métrica "custo por tarefa aceita" da agenda de pesquisa. |
| Gerar / verificar / desfazer | Os três termos de custo de uma mudança: produzi-la; estabelecer que ela faz o que devia, inclusive a intenção; e reverter o erro que escapou. |
| Piso de custo | O custo por mudança aceita quando gerar tende a zero; só verificação e reversibilidade o movem. |
| Tamanho de lote (*batch size*) | Quantas mudanças são integradas juntas. Lote menor reduz o custo de desfazer e move as métricas do DevOps Research and Assessment (DORA) na mesma direção. |
| Reversibilidade engenheirada | Mecanismos (backup, execução a seco, homologação, exclusão lógica) que barateiam desfazer e, com isso, baixam a classe de risco de uma ação. |
| Crítico às cegas | Agente em contexto fresco que compara duas versões sem saber qual é a do time e aponta a melhor e a maior lacuna. |
| *Gauntlet* | Laço construtor × crítico às cegas contra uma barra, repetido até a versão do time vencer. |
| Corte | Decisão humana de reduzir escopo ou realocar verificação para fechar uma versão; no Maestro, registrada com data e o que entra e sai. |
| Governança operacional | Conjunto de regras, papéis, artefatos, gates, registros de decisão, scripts e hooks que decide quem faz, verifica e aprova o quê, independentemente do *harness*. |
| *Harness* | O ambiente que executa o agente e lhe dá ferramentas (por exemplo, uma ferramenta de linha de comando para agentes de código); trocável sem mudar o método. |
| Assimetria fazer × desfazer (A5) | Axioma do Maestro: produzir é barato e fica mais barato; desfazer (apagar, publicar, migrar, fazer deploy) não. |
