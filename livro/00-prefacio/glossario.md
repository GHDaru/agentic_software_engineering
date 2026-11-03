# Glossário do prefácio

| termo | definição |
|---|---|
| Governança operacional | A camada de regras, papéis, artefatos, portões, registros de decisão e automações que decide o que um agente pode fazer, quem verifica e quem aprova. Roda sobre qualquer *harness* e modelo. |
| *Harness* | O programa que executa o agente: dá a ele ferramentas, contexto e permissões (um agente de linha de comando, um SDK, um orquestrador). O livro é independente dele. |
| Instrução × enforcement | Instrução é o que se pede ao agente em texto; enforcement é o mecanismo (*hook*, script, permissão) que recusa a ação errada independentemente de o agente ter lido o pedido. |
| *Hook* | Comando que o *harness* executa em um ponto fixo do ciclo do agente (por exemplo, antes de cada chamada de ferramenta) e que pode recusar a ação. |
| Revisão em contexto fresco | Verificação feita por um agente ou pessoa que não executou o trabalho e não carrega o histórico da sessão que o produziu. |
| Proxy (de um check) | O que um portão de fato mede quando não mede o fato que diz medir: a presença de um arquivo, a ocorrência de uma palavra, a cobertura sem asserção que discrimine. |
| Reversibilidade engenheirada | Mecanismos (backup, execução a seco, homologação, exclusão lógica) que barateiam desfazer e rebaixam a classe de risco de uma ação. |
| Axioma / teorema / corolário | Na camada de derivação do Maestro: verdade assumida; regra derivada e demonstrável com evidência do repositório; consequência imediata que muda uma decisão. |
| CLAIM | Afirmação quantitativa ou factual do livro, com identificador `CLAIM-NN-NNN`, estado (medido, observado, hipótese) e evidência reproduzível registrada no `claims.md` do capítulo. |
| Medido / observado / hipótese | Estados de um claim: um comando reconta; um artefato registra e se confere lendo; o livro acredita e ainda não demonstrou. |
| Raia | Quanto processo uma mudança recebe (leve, plena, infra), em função de ambiguidade, raio de impacto e irreversibilidade. |
| Quatro corpos de texto | Método normativo, *handbook* por versão, livro (argumento durável) e pesquisa (protocolo, execuções, dados). |
