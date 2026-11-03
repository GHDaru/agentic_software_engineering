# Glossário do capítulo 3

| termo | definição |
|---|---|
| Apetite | O tempo que uma aposta merece, fixado antes de começar (Shape Up). O escopo varia dentro dele; quando o apetite acaba, corta-se escopo e o prazo não se estende. |
| Armadilha do funil | Quando o humano é o Accountable e também confere à mão cada saída de agente: recria o trabalho de fazer tudo sozinho, com uma etapa a mais de leitura, e vira o gargalo do próprio sistema. A saída é responder pela política, não por item. |
| Capacidade de decisão | Quantas decisões por dia o humano consegue tomar com qualidade; o teto da vazão de um time de agentes. No exemplo do capítulo, 480 minutos ÷ 12 minutos por decisão = 40. |
| Cerimônia por função | Critério para manter ou cortar uma cerimônia: perguntar que função ela cumpre no contexto de um humano com N agentes. Sem função, sem cerimônia. |
| Endereço de sessão | A identidade de uma sessão de agente escrita em três partes, `nome · ref · projeto`. O nome se repete; a ref distingue homônimos e expira quando a sessão reinicia. Endereço ambíguo é recusado, nunca adivinhado. |
| Espera humana | O intervalo entre um pedido de decisão ficar pronto e a decisão ser registrada. Métrica do gargalo; só existe como dado se pedido e resposta tiverem carimbo de tempo. |
| Estado derivado | Estado calculado a partir de arquivos ou de eventos com carimbo, sob regras fixas, em vez de digitado por quem trabalha. O oposto do "Estado atual" que cada agente escrevia e que envelhecia em horas. |
| Execução contínua | Regra de o agente executar o plano até um bloqueio, uma ambiguidade real ou o fim, sem pedir licença a cada passo; a atenção humana se gasta em gates, não em acompanhar progresso. |
| Fila de decisões | Lista dos pedidos de decisão abertos, ordenada por prazo, derivada de um registro só-acréscimo. Não tem "dispensar": um pedido sai só com ruling ou devolução. |
| Frase-chave | A frase de abertura da tela do regente ("você tem N decisões esperando, a mais antiga há X"), derivada da fila e nunca digitada; o contador baixa quando um ruling é registrado. |
| Lei de Little | Num sistema estável, itens em curso = taxa de chegada × tempo no sistema (Little, 1961). Para a mesma vazão, mais itens em curso significam mais espera. |
| Painel de coordenação | Servidor local que projeta o estado de um time a partir dos arquivos do método; o banco é projeção reconstruível, a única escrita direta é uma tabela de eventos só-acréscimo, e o painel nunca promove. |
| Painel de regência | A vista do painel feita para o humano que rege: quadro por gate e fila de decisões. Lê e registra; não decide. |
| Paralelizar dentro, não entre | Abrir trabalho paralelo só dentro de uma feature cuja spec e plano já foram aprovados; entre features ambíguas, cada frente multiplica os gates que passam pela mesma pessoa. |
| Pedido de decisão | Pergunta escalada ao humano com id, quem pediu, opções, recomendação, prazo, o que destrava e destino da resposta. Sem prazo, é recusado. |
| Portão do regente | Os gates que só o humano registra (no Maestro, o aceite G7, a ordem de produção G8 e o fechamento `TAIL:gate`); para um agente, aparecem como somente leitura. |
| Projeção | Modelo de leitura que se apaga e se reconstrói a partir da fonte (arquivos, eventos). Pode ser descartada sem perda; nunca é a fonte. |
| Ruling | A resposta registrada a um pedido de decisão: autor humano, data, destinatário e ligação ao que a cita. Sem autor ou sem destino, é recusada. |
| Teoria das Restrições (TOC) | *Theory of Constraints* (Goldratt): a vazão de um sistema é a vazão da sua restrição; melhorar fora dela não muda o resultado. Num time de agentes, a restrição é a decisão humana. |
| Trabalho em curso (WIP) | *Work in progress*. Neste capítulo, medido em decisões humanas pendentes, e não em tarefas abertas ou agentes ativos. |
