# Glossário do capítulo 2

| termo | definição |
|---|---|
| Accountability | O dever de responder pelas consequências de um resultado. Diferente de capacidade: um agente pode raciocinar bem e não ter o que perder (axioma A2). |
| Accountable (A) | Na matriz RACI, a única pessoa que responde pelo resultado. Neste livro, sempre humano, e responsável pela política, pelos gates e pelos critérios, não por cada item. |
| Armadilha do funil | Quando o humano é Accountable e também confere à mão cada saída de agente: recria o trabalho de fazer tudo sozinho, com uma etapa a mais de leitura, e vira o gargalo. |
| Autor como revisor | Anti-padrão em que o agente (ou pessoa) que escreveu aprova o próprio trabalho. |
| Caixa marcada sem testemunha | Item de checklist marcado como feito sem a evidência existir; no Maestro, a caixa da cauda de fechamento marcada antes da revisão. |
| Cauda de fechamento | As caixas `TAIL:review`, `TAIL:security`, `TAIL:mutation` e `TAIL:gate` no fim do `tasks.md` de um ciclo do Maestro, cada uma exigindo evidência escrita no relatório de qualidade. |
| Constitution Check | Tabela, dentro do plano de um ciclo do Maestro, que confere o plano contra cada princípio da constituição do método antes de implementar; aprovar o plano com ela é um dos gates humanos. |
| Contexto fresco | Sessão de agente iniciada sem o histórico de quem executou: recebe o diff, a spec e o plano, e nada da conversa. |
| Crítica às cegas | Forma de revisão em que o juiz compara o resultado com uma referência externa sem saber qual é qual, e decide qual atende melhor à pergunta do usuário. |
| Definition of Done (DoD) | Definição de pronto: o conjunto de verificações executáveis (testes, portões, build) que um ciclo tem de passar para ser dado como feito. |
| Gate humano | Ponto do fluxo em que um humano decide, com nome e registro, se o trabalho avança (spec, plano, merge, deploy ou migração). |
| Gate por delegação de política | Gate humano decidido por um agente regente que não executou o trabalho, sob delegação escrita e revogável do humano, depois do parecer de um crítico em contexto fresco (ADR 0026 do Maestro). |
| Harness | O programa que roda o agente de IA em volta do modelo (por exemplo, um CLI de agente de código): entrega as ferramentas à sessão, aplica permissões e executa hooks. É ele que impõe a configuração de quem pode escrever. |
| Hook | Gancho do harness: um comando que roda automaticamente antes ou depois de um evento (uma chamada de ferramenta, o fim de um turno) e pode bloquear a ação. |
| Human-in-the-loop | Arranjo em que um humano confere ou aprova cada saída de um sistema automatizado. Aqui se distingue o humano em cada item (rejeitado como regra geral) do humano nos gates. |
| Iniciativa mista | Princípio de Horvitz para interfaces com agentes: humano e máquina alternam a iniciativa, e o humano entra no ponto de decisão das ações consequentes, não em cada passo. |
| Juiz com caneta | Papel que julga e também tem permissão de escrita; viola o corolário C3, porque o revisor que conserta vira coautor. |
| Matriz RACI | Responsible, Accountable, Consulted, Informed: quem executa, quem responde, quem é consultado, quem é informado, por tarefa. |
| Parecer | O veredito escrito de uma revisão independente (aprovar, aprovar com condições, reprovar), com os achados que o sustentam. |
| Prova por mutação | Introduzir de propósito o defeito que um portão deveria acusar (uma mutação) e conferir que ele acusa; a contraprova é o caso legítimo que ele deve deixar passar. Prova que o portão sabe reprovar, não que mede a coisa certa. |
| Raia (regra de raia) | No Maestro, a classe de rigor de um ciclo, declarada no início: leve (o pull request é o artefato), plena (spec completa) ou infra (plena mais reversibilidade). A regra de raia fixa que cerimônia cada classe exige. |
| Regente | Sessão de agente que coordena outras sessões e não executa o trabalho que distribui. |
| Rendimento da revisão independente | Fração das revisões independentes, feitas antes do gate, que mudaram o resultado (reprovaram ou exigiram correção), lida no corpo do parecer e não no título ou no cabeçalho do relatório. Métrica da agenda de pesquisa do livro. |
| Segregação de funções | Princípio de controle em que quem executa, quem confere e quem aprova são posições diferentes; aqui aplicado a agentes. |
