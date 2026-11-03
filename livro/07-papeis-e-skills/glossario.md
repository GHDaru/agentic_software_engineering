# Glossário do capítulo 7

| termo | definição |
|---|---|
| Ablação | Técnica de avaliação em que o mesmo caso roda contra o agente real e contra o agente menos uma instrução. Se o ablado falha onde o real passa, a instrução paga o contexto que custa; se os dois passam, ela é suspeita de redundância. |
| Agente (perfil) | O par descrição ↔ arquivo executável de um papel (no Maestro, `.claude/agents/<nome>.md`), com escopo, ferramentas e contrato. Não tem identidade de execução; ocupa sessões. |
| Bootstrap de enforcement | O parágrafo, na instrução que o agente lê primeiro, que manda consultar as skills antes de agir. No Maestro, gerado do disco pelo instalador e conferido por script. |
| Contrato do papel | A parte do perfil que diz o que o papel faz, o que não faz, o que consome, o que produz e a quem entrega. É o que distingue um papel de um prompt. |
| Custo fixo de contexto | O que um papel carrega para a janela a cada invocação: o próprio perfil, as skills que consome e o que a instrução do projeto importa por padrão. |
| Desculpa fechada | Racionalização listada e recusada explicitamente numa lei de ferro ("isto NÃO é desculpa: …"), para que o agente não a use. |
| Faixa de modelo | A classe de modelo (por exemplo pequeno, médio, grande) em que um papel roda, declarada no perfil com motivo e gatilho de revisão. Recomendação deste livro; ausente no Maestro na versão citada. |
| Gatilho (de skill) | O trecho da `description` de uma skill que diz quando ela se aplica ("Use quando…"); é o que o harness lê para decidir carregá-la. |
| Handoff | A passagem de trabalho de um papel ao seguinte, feita por artefato (spec, plano, diff, veredito), e não por conversa. |
| Lei de ferro (*Iron Law*) | Regra inegociável que abre uma skill, em bloco de código, com a fórmula "violar a letra é violar o espírito" e as desculpas fechadas. Estreita: uma por skill. |
| Linha de base (de skill) | Registro de um cenário de pressão em que o agente falha sem a skill (vermelho) e cumpre com ela (verde), exigido antes de publicar uma skill original. |
| Meta-agente | Agente cujo trabalho é construir ou evoluir o próprio método: projetar papéis, escrever skills, curar pesquisa, revisar a didática. |
| Modo de trabalho | Papel entendido como forma de trabalhar (decidir, executar, verificar), exercida por humano, agente ou ambos com um gate, e não como cargo. |
| Norma × executável | O par formado pelo documento que prescreve um papel ou artefato e pelo arquivo que o entrega. O defeito típico mora na distância entre os dois. |
| Papel de ocasião | Especialista convocado para uma decisão (por exemplo, uma banca em contexto fresco), consultado e descartado, sem perfil permanente. |
| Papel órfão | Perfil executável que entrega um papel que a norma não prescreve; o espelho do papel prescrito sem executável. |
| Sessão de agente | Uma execução de um perfil, que o humano sobe, observa e derruba; a unidade de administração. |
| Skill | Procedimento recorrente empacotado como `SKILL.md` (nome, descrição com gatilho, passos), que dispara pelo contexto. Diferente de comando (invocação explícita) e de agente (quem faz). |
| Skill órfã | Skill que nenhum papel consome (ou, na versão editorial do problema, que nenhum capítulo ensina). |
| Teste de pressão | Cenário escrito para que o agente tenha motivo para desobedecer a regra (pressa, conserto "óbvio"); é a fixture da linha de base de uma skill. |
