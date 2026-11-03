# Glossário do capítulo 16

| termo | definição |
|---|---|
| axioma (no Maestro) | Verdade assumida sem prova, da qual o método deriva teoremas e regras; o Maestro tem cinco (A1–A5), em `docs/governance/axioms.md`. |
| teorema (no Maestro) | Consequência dos axiomas, com evidência no próprio repositório (T1–T7); cada um declara de quais axiomas deriva. |
| corolário (no Maestro) | Regra do dia a dia derivada de um teorema ou axioma (C1–C13). |
| premissa sobre a ferramenta | Axioma que descreve uma limitação do modelo ou do *harness* de hoje (A3, contexto finito; parte de A4, sessão que começa do zero); pode enfraquecer com a próxima geração. |
| regra exposta | No mapa da fragilidade deste livro, regra que deriva de pelo menos uma premissa que enfraqueceu num cenário. |
| regra sem apoio | Regra cujas premissas enfraqueceram todas num cenário; precisa de outro motivo ou vira cerimônia. |
| mapa da fragilidade | Leitura deste livro (hipótese) que cruza teoremas e axiomas para dizer quais regras dependem só da ferramenta. |
| catálogo do ecossistema | No Maestro, o registro do que foi visto fora do projeto, com a **ideia** como unidade: fontes, cartões datados e imutáveis, e um índice de estado que só cresce. |
| veredito (absorver, adotar, descartar, observar) | Os quatro estados de uma ideia no catálogo: absorvida no método, adotada como ferramenta, descartada, ou em observação com gatilho. |
| gatilho de reavaliação | Condição escrita que, quando acontece, obriga a reabrir uma decisão adiada. |
| gatilho de evento / de relógio | De evento: dispara quando algo observável acontece (um pedido, um conflito, uma medida). De relógio: dispara numa data; certo quando quem publica a data é externo. |
| registro de eventos | Proposta do livro: arquivo anexável com uma linha por gatilho tocado (ideia, data, prova), conferido por um portão contra o estado corrente. |
| portão antigo / portão novo | No exemplo do capítulo: o antigo confere que todo "observar" tem gatilho; o novo, que nenhum gatilho disparou sem reavaliação. |
| vigília do futuro | O conjunto catálogo + gatilhos + portão + cadência com que um time percebe, sem depender de memória, que uma premissa mudou. |
| aplicação escalonada | Entrada em vigor de uma lei em marcos datados diferentes por tipo de obrigação, como no art. 113 do Regulamento Europeu de Inteligência Artificial. |
| plano de controle de agentes (*agent control plane*) | Camada que coordena, observa e governa vários agentes; no Maestro, decidiu-se construí-la com protocolos nas bordas. |
| Agent2Agent (A2A) | Protocolo aberto para conversa entre agentes; no Maestro, só os nomes de estado entram no envelope das mensagens. |
| Agent Client Protocol (ACP) | Protocolo aberto para a conversa entre editor e agente; no Maestro, um dos modos da porta de *harness*, com versão fixada. |
| *lock-in* | Dependência de um fornecedor que torna cara a saída; mede-se na dimensão de reversibilidade do cartão. |
| letramento em IA (*AI literacy*) | Obrigação do art. 4 do *AI Act*: desde o Regulamento (UE) 2026/1744, fornecedores e quem implanta sistemas de IA tomam medidas que apoiem o letramento da equipe, sem garantir nível individual. |
| modelo de IA de uso geral (*general-purpose AI model*, GPAI) | No *AI Act*, modelo treinado para servir a muitas tarefas e ser integrado por terceiros; o fornecedor tem os deveres dos arts. 53 e 55. |
| *Digital Omnibus on AI* | Nome do Regulamento (UE) 2026/1744, que alterou o *AI Act* (datas do alto risco, proibições novas, transições). |
| conferência com validade | Data em que um dado externo (como um calendário regulatório) foi comparado com a fonte oficial, mais o prazo depois do qual o dado não responde sem nova conferência. |
