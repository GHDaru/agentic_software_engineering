# Glossário do capítulo 9

| termo | definição |
|---|---|
| *fitness function* (de arquitetura) | Verificação objetiva e executável de uma característica de arquitetura, rodada de forma contínua (em geral na integração contínua). Termo de Ford, Parsons e Kua. |
| fronteira decidível | Fronteira em que uma máquina responde, para qualquer arquivo, a qual domínio ele pertence, sem julgamento: nenhum órfão, nenhuma dupla reivindicação, empate tratado como erro. |
| fronteira interna | Separação entre domínios declarada e verificada dentro de um único repositório, em vez de repositórios separados (ADR 0018 do Maestro). |
| domínio (de repositório) | No sentido do capítulo, uma das metades do repositório definidas pelo leitor: o que é lido por máquina (toolkit) e o que é lido por gente (guia). Não confundir com o domínio do DDD. |
| caminho compartilhado | Caminho possuído por um domínio e lido (ou publicado) por outro; declarado para que quem o edita saiba que a edição é pública. |
| canal de publicação | Cada via pela qual um arquivo chega ao leitor final (itens do sumário, materiais, anexos). Um portão de fronteira precisa ler todos. |
| prefixo mais longo | Regra de resolução de dono: entre as declarações que casam com um caminho, vence a mais específica; empate no mesmo comprimento é ambiguidade e falha. |
| regra da dependência | O código-fonte só aponta para dentro, em direção ao domínio: o domínio não conhece porta nem adaptador; a porta não conhece o adaptador. |
| porta / adaptador | Na arquitetura hexagonal, a porta é a interface que o núcleo define para falar com o mundo; o adaptador é a implementação que fala com o mundo real (banco, rede) ou o substitui em teste (o falso). |
| teste de contrato | Uma única bateria de casos rodada contra todos os adaptadores de uma porta, inclusive o falso, para que o dublê não seja mais frouxo que a produção. |
| append-only mecânico | Garantia de que um registro só cresce imposta por mecanismo (modo de abertura verificado, gatilho no banco), e não por convenção. |
| prova destrutiva | Verificação de uma propriedade de ciclo de vida provocando a falha de propósito (matar o servidor) e observando o que sobrevive. |
| porta nova, guarda antiga (anti-padrão 23) | Um ciclo abre um canal ou concede um poder novo e o portão que vigiava o canal velho continua lendo metade do mundo; o verde passa a significar "não olhei para lá". |
| gatilho de reabertura | Condição observável, escrita na decisão, que manda reavaliá-la (por exemplo, "mais de 30 rotas"); substitui a data de revisão e a decisão eterna. |
