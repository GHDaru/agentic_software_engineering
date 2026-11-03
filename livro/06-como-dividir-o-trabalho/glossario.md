# Glossário do capítulo 6

| termo | definição |
|---|---|
| Fatia | Parte de um trabalho entregue a um agente (ou a uma sessão) para ser feita sem olhar as outras. |
| Corte | A decisão de onde separar as fatias. Pode ser por fronteira (contexto delimitado, contrato, camada), por quantidade (N itens para cada um) ou por tela/papel. |
| Corte por fronteira | Corte que dá a cada conceito um dono e a cada contrato um escritor; as fatias se tocam só por contratos declarados. |
| Corte por quantidade | Corte que reparte o trabalho por número de itens ou de arquivos, sem olhar o que eles compartilham. Produz colisões. |
| *Map-reduce* cognitivo | Leitura do trabalho com agentes como *map* (as fatias, em paralelo) e *reduce* (a junção). O *reduce* não é concatenação: é julgamento com contexto global. |
| *Reduce* | A junção das fatias. Exige o contexto global que a divisão espalhou; pertence a quem responde pelo resultado (o humano, ou quem age sob política escrita dele). |
| Dono do conceito | A única fatia que calcula ou define um conceito; as outras o consomem pelo contrato, sem recalcular. |
| Contrato | O que uma fatia publica para as outras: função, formato, porta. Escrito antes de ser consumido. |
| Porta inerte (*seam* inerte) | Contrato publicado cedo que não muda o comportamento enquanto ninguém o chama; deixa os consumidores trabalharem sem esperar o dono terminar. |
| Onda | Grupo de fatias que podem correr ao mesmo tempo porque nenhuma consome contrato de outra do mesmo grupo. A ordem das ondas sai dos contratos. |
| Passagem (*handoff*) | Cada vez que uma fatia depende de algo produzido por outra. Custa tempo e contexto. |
| Overhead de coordenação | Fração do tempo (ou dos tokens) de um trabalho paralelo gasta em passagens e reconciliação, e não em produzir as fatias. |
| Colisão | Defeito do corte: arquivo com dois escritores, conceito com mais de um dono ou contrato consumido sem dono. |
| Colisão de endereço | O mesmo identificador apontando para dois destinos, ou para nenhum. Invariante do Maestro: endereço ambíguo é recusado, nunca resolvido. |
| Espectro fluxo ↔ agente | Eixo entre o caminho fixado por você (*workflow*) e o caminho decidido pelo modelo na hora (*agent*). |
| Regra da menor autonomia | Começar pelo padrão mais simples do espectro e só subir quando o simples comprovadamente falhar. |
| Encadeamento | Padrão de passos fixos em sequência, cada um consumindo a saída do anterior. |
| Roteamento | Padrão que classifica a entrada e escolhe um tratamento fixo. |
| Paralelização | Padrão de fatias independentes (ou várias tentativas da mesma tarefa) executadas ao mesmo tempo. |
| Orquestrador-trabalhadores | Padrão em que um orquestrador corta o trabalho na hora e junta as respostas. |
| Avaliador-otimizador | Padrão de laço: gerar, criticar contra um critério, refinar até passar. |
| Gerente / Worker | No Maestro, a sessão que distribui e integra (Gerente) e as sessões que executam fatias, cada uma na sua worktree (Workers). |
| Regente | No Maestro, a sessão que conduz o time acima do Gerente e decide portões sob delegação escrita do humano (ADR 0026). |
| *Worktree* | Cópia de trabalho adicional de um repositório Git, com branch própria; isola as edições de um agente das de outro. |
| Ciclo guarda-chuva | Ciclo que só coordena: abre ciclos filhos e registra as decisões, sem entregar código próprio. |
| Rodada / passo | Uma execução do fluxo gravada passo a passo; cada passo tem entrada, resumo e saída, e um passo sem saída bloqueia o seguinte (Maestro, ciclo 070). |
| *Outbox* | Fila local (SQLite em modo WAL) por onde sessões da mesma máquina trocam mensagens sem servidor de mensageria. |
| Gatilho de reavaliação | Condição observável escrita junto de uma decisão adiada ("observar"), que diz quando a decisão deve ser revista. |
| Fatia vertical | Fatia que atravessa da interface ao dado e entrega valor sozinha. Regra entre entregas, não entre agentes dentro de um ciclo. |
| INVEST | *Independent, Negotiable, Valuable, Estimable, Small, Testable*: os atributos de uma boa história de usuário. |
| SPIDR | *Spike, Path, Interface, Data, Rules*: cinco linhas de corte de uma história, de Mike Cohn. |
