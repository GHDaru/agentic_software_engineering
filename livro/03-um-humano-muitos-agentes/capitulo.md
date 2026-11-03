# 03 — Um humano, muitos agentes

> *Mais agentes não alargam o gargalo; alargam a fila na frente dele.*

Todo tech lead que experimenta agentes de Inteligência Artificial (IA) chega ao mesmo ponto:
um agente rende bem, dois rendem o dobro, e a tentação é abrir o terceiro, o quarto, o
décimo. Este capítulo é sobre o que acontece depois disso. Ele mostra, com registros datados
de um método que passou de uma frente de trabalho para dezessete sessões simultâneas em
poucas semanas [CLAIM-03-005], que o recurso que acaba primeiro não é a máquina, e sim a atenção da pessoa
que responde pelo resultado. E mostra como se rege dentro desse limite: o que se corta, o
que se mede, o que se torna visível e o que nunca se delega.

## Pergunta central

Quando a capacidade de executar deixa de ser o limite, qual passa a ser o gargalo de um time
de agentes, e como um humano rege muitos agentes sem virar a fila do próprio sistema?

## Resultado de aprendizagem

Ao final deste capítulo, você consegue:

1. **Derivar**, a partir dos axiomas da intenção humana e do contexto finito, por que a vazão
   de um time de agentes satura na atenção de quem decide, e **calcular** essa saturação com
   uma fila simples.
2. **Medir** o trabalho em curso do seu time em decisões humanas pendentes, e não em tarefas
   abertas, e **distinguir** paralelismo que rende (dentro de uma feature decidida) de
   paralelismo que só multiplica gates (entre features ambíguas).
3. **Escolher** que cerimônias manter perguntando pela função de cada uma, e **aplicar**
   apetite (tempo fixo, escopo variável) no lugar de estimativa de prazo.
4. **Desenhar** uma fila de decisões com prazo, recomendação e destino, cujo estado é
   derivado de um registro só-acréscimo, e **recusar** endereço ambíguo de sessão em vez de
   adivinhá-lo.
5. **Reconhecer** no seu fluxo a armadilha do funil e as falhas típicas de escala (estado
   digitado que envelhece, mensagem no destinatário errado, sessão que renasce sem contexto) e
   **escrever** o controle que as torna visíveis.

## A falha real

Em agosto de 2026, o Maestro (o método de governança que este livro usa como objeto de
estudo) operava com uma regra simples de trabalho em curso (*work in progress*, WIP): uma
feature de cada vez. O capítulo de cerimônias do handbook, revisto em 17 de agosto, mostrava
a prova por comando: depois de vinte e seis ciclos, `git branch -a` devolvia duas branches,
`dev` e `main`, e nenhuma frente paralela tinha sido aberta [CLAIM-03-001]. Duas decisões
coerentes com essa escala estavam registradas. A primeira: a ideia de orquestrar uma frota de
agentes, observada num projeto de código aberto, foi triada em 1º de agosto como "por ora,
não", e reclassificada em 10 de agosto para "observar" com um gatilho escrito: "existir
trabalho paralelo real que a atenção de **um** humano consiga governar" [CLAIM-03-002]. A
segunda: o catálogo de artefatos do modelo operacional listava um painel de métricas como
"Later / YAGNI" (*you aren't gonna need it*, não vai precisar), com o argumento de que, sem
a quem comparar, instrumentar era débito prematuro [CLAIM-03-003].

Havia, já então, uma lacuna declarada. Em 14 de agosto, um diagrama que comparava o fluxo do
Maestro com o de um arquiteto externo registrou que a fila de trabalho existia (o roadmap,
ordenado por dependência, com gatilhos) mas não tinha **dono por item nem critério de
elegibilidade**: "por que este ciclo e não aquele" continuava sendo julgamento não
registrado [CLAIM-03-004]. Com uma frente só, isso custava pouco: a fila cabia na cabeça de
uma pessoa.

Seis semanas depois, a escala mudou. Entre 29 de setembro e 1º de outubro, o método foi
usado num projeto de produto, o Hindiana, com dezessete sessões de agente simultâneas (duas
de coordenação, dois gerentes e treze workers; a fonte escreve "16 sessões", mas a lista que
ela mesma dá soma dezessete, e é a lista que este livro segue), cerca de cento e sessenta *worktrees* do
Git, cinquenta e dois desvios de método registrados em três dias e vinte e oito decisões
tomadas numa única noite [CLAIM-03-005]. Nenhuma dessas sessões estava ociosa por falta de
capacidade. O que falhou foi tudo o que passava pela pessoa que regia o time.

O **estado** falhou primeiro. Cada sessão mantinha um "Estado atual" digitado pelo próprio
agente, e ele envelhecia em horas; o controle se espalhou por dez arquivos e pelas mensagens
entre sessões. O desvio mais perigoso daqueles dias, dez branches com *upstream* apontando
para a linha de produção, só apareceu quando alguém procurou à mão, em 1º de outubro
[CLAIM-03-005] [CLAIM-03-006]. O primeiro painel construído para isso, instalado no próprio
projeto, mostrava em 19 de outubro tabelas derivadas com dez dias de defasagem: o status dos
workers tinha parado de ser registrado em 6 de outubro [CLAIM-03-006].

O **endereço** falhou em seguida. As sessões se acham pelo nome, e o nome não é identidade:
havia uma sessão de coordenação registrada sob três referências, duas delas fora do ar. Em
13 e 14 de outubro, mensagens de gerentes caíram em sessões de outro projeto; num desses
dias, um gerente mandou dez mensagens a uma sessão que tratava de um assunto alheio
[CLAIM-03-007].

E a **espera** falhou por último, e foi a mais cara. Em 10 de outubro, uma pergunta feita às
08:45 ficou vinte e quatro horas sem resposta. Em 16 de outubro, uma decisão escalada ao
humano às 07:04 ficou sem resposta até a tarde e estourou dois prazos; no mesmo dia, uma
sessão de coordenação caiu duas vezes [CLAIM-03-008]. Ninguém estava parado por falta de
agente. Os agentes estavam parados esperando a única pessoa que podia responder, e essa
pessoa não tinha um lugar onde ver o que esperava por ela.

A resposta do Maestro veio em 20 de outubro: integrar a linha paralela que o projeto tinha
produzido (quarenta e duas branches) em ciclos numerados a partir do 066, o primeiro deles um
painel de coordenação que deriva o estado dos arquivos, e superar em parte o "YAGNI" do
painel com um registro de decisão de arquitetura (*Architecture Decision Record*, ADR), o ADR
0022 [CLAIM-03-009]. A falha não terminou aí, e é isso que a torna instrutiva. O painel de
regência do ciclo 072, que devia dizer ao regente "o que me espera" em cinco segundos, tinha
dois defeitos registrados na própria jornada de uso em 24 e 25 de outubro. Aberto com o
servidor frio, ele mostrava uma lista vazia enquanto calculava, e vazio "que não é o estado
do projeto" é a pior leitura possível às sete da manhã; o script de captura contornava o
problema esperando a derivação estabilizar, a tela não [CLAIM-03-010]. E o quadro por gate,
que devia mostrar dez colunas lado a lado, empilhava todas numa faixa de 232 pixels numa
janela de 1440 × 900 [CLAIM-03-011].

Em 29 de outubro o time inteiro caiu. Cada painel do lançador de sessões reabriu uma sessão
**nova**, e o contexto vivo de cada agente se perdeu; a regente retomou as sessões à mão. No
dia seguinte, o lançador ganhou uma opção para retomar cada sessão pelo nome, mantendo o
mesmo endereço, porque uma sessão renascida com outro nome é uma sessão que os pares não
acham [CLAIM-03-012]. Em 31 de outubro, a retomada pelo nome abriu o seletor com nomes
duplicados e o time ficou parado dez horas; a correção passou a retomar pelo identificador
da sessão [CLAIM-03-013]. Este episódio é o único do capítulo que vem de depois da versão de
referência do Maestro (`19823c2`): está na mensagem do commit `8c79331`, de 1º de novembro,
e por isso não tem link fixado como os demais.

Nenhuma dessas falhas foi de capacidade de modelo. Todas aconteceram na interface entre
muitos agentes e um humano: o estado que ele lê, o endereço pelo qual ele fala, a fila em
que ele decide. O resto deste capítulo explica por que é ali que a coisa quebra, e o que se
põe no lugar.

## Teoria

### A fonte da intenção não se paraleliza (axioma A1)

O primeiro axioma do Maestro diz que a **intenção é humana**: um agente propõe, escreve e
verifica, mas não *quer*; o que construir e por que vale a pena não tem outra fonte além de
uma pessoa ([axioms.md, A1](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/axioms.md)).
Lido como engenharia de capacidade, o axioma tem uma consequência direta. Todo trabalho de um
time de agentes começa numa intenção e termina num aceite, e as duas pontas passam pela
mesma fonte. Dá para multiplicar quem executa; não dá para multiplicar quem quer.

Isso transforma o time num sistema com um recurso compartilhado. Cada agente que se
acrescenta produz mais itens que precisam de uma decisão humana: aprovar uma spec, escolher
entre duas opções, aceitar um merge, responder "por item ou por pedido?". Enquanto o humano
tem folga, mais agentes significam mais vazão. Quando a folga acaba, mais agentes significam
**mais fila**, e a vazão do sistema inteiro fica presa ao ritmo de quem decide. O
[capítulo 1](../01-a-mudanca-de-unidade-de-trabalho/capitulo.md) chegou a esse limite pelo
lado da economia (a mudança aceita é escassa porque consome atenção); este capítulo chega
pelo lado do fluxo.

O [capítulo 2](../02-o-problema-da-confianca/capitulo.md) somou um segundo motivo: a
consequência precisa de dono (axioma A2). A1 devolve ao humano a decisão de *o quê*; A2
devolve a resposta *por isso*. Tirar o humano das duas pontas não deixa o sistema mais
rápido: deixa-o sem objetivo e sem responsável.

### O contexto finito obriga a fatiar, e cada fatia cria uma junção (axioma A3)

O terceiro axioma diz que **o contexto é finito e degrada quando enche**: a janela que um
agente lê é limitada e o desempenho cai com o ruído ([axioms.md, A3](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/axioms.md)).
Por causa dele, o trabalho grande não vai inteiro para um agente: ele é cortado em fatias
estreitas, cada uma com o contexto que lhe basta. É isso que torna possível ter muitos
agentes, e é também o que gera o custo de coordenação. Cada corte cria uma junção: alguém
precisa saber que a fatia terminou, que ela encaixa nas outras, que a pergunta que ela
levantou foi respondida. O [capítulo 5](../05-engenharia-de-contexto/capitulo.md) trata do
que vai em cada janela; o [capítulo 6](../06-como-dividir-o-trabalho/capitulo.md), de onde
cortar. Aqui interessa a soma: N fatias produzem N pontos em que o trabalho volta a quem
integra.

O axioma fala da janela do agente, mas a mesma física vale, por analogia, para quem rege:
a atenção do humano também é finita e também degrada com ruído. Essa extensão é uma hipótese
deste livro, não um axioma do método, e o argumento não depende dela. Basta A1 para que as
decisões convirjam numa pessoa, e basta A3 para que o número de junções cresça com o número
de fatias. Juntos, eles dizem que o custo de coordenação cresce com o time e que esse custo
cai sempre no mesmo lugar.

### O gargalo é uma fila, e fila tem matemática

Um humano que decide itens que chegam de vários agentes é, para efeito de cálculo, uma fila
com um servidor só. Três resultados clássicos de teoria das filas e de fluxo bastam para o
tech lead.

O primeiro é a **Lei de Little** (Little, 1961) [CLAIM-03-032]: num sistema estável, o número médio de itens
em curso é igual à taxa de chegada vezes o tempo médio que cada item passa no sistema. Lida
ao contrário, ela diz que, para a mesma vazão, mais itens em curso significam mais tempo de
espera de cada um. Abrir frentes não acelera nada que passe pelo mesmo servidor: só aumenta o
estoque na frente dele.

O segundo é a relação entre ocupação e espera. Em filas com variabilidade, a espera cresce
de forma não linear quando a ocupação do servidor se aproxima de cem por cento: a aproximação
de Kingman (1961) põe a espera proporcional a ocupação ÷ (1 − ocupação). Um humano ocupado em
oitenta por cento ainda responde a tempo; ocupado em cem, não responde mais nada a tempo,
mesmo trabalhando o dia inteiro. Reinertsen (2009) lembra por que isso passa despercebido: o
estoque do desenvolvimento é informação, não caixas no chão.

O terceiro é a **Teoria das Restrições** (*Theory of Constraints*, TOC) de Goldratt (1984):
a vazão de um sistema é a vazão da sua restrição, e otimizar fora dela não muda o resultado.
Num time de agentes, a restrição é a decisão humana. Toda melhoria que acelera os agentes sem
tocar nela é, para a vazão, irrelevante; toda melhoria que barateia a decisão, ou que tira da
fila o que não precisava estar lá, é a que conta.

O exemplo executável calcula isso num caso simples: com oito horas de atenção e doze minutos
por decisão, o teto é de quarenta decisões por dia. Quatro agentes ocupam o humano em oitenta
por cento e ninguém espera; oito dobram a produção, mas as decisões param em quarenta e vinte e
quatro fatias dormem na fila [CLAIM-03-026]. Com dezesseis, continuam sendo quarenta.

### O trabalho em curso se mede em decisões, não em tarefas

Daí a primeira regra prática: o limite de trabalho em curso de um time de agentes não é a
capacidade dos agentes, é a **atenção humana**. O handbook do método formula isso dizendo que
cinco features sem dependência entre si ainda funilam pelos mesmos gates humanos (aprovar
spec, aprovar plano, aprovar merge); abrir frentes multiplica gates, e o humano vira a fila
([handbook 07 §5.3](https://github.com/GHDaru/maestro/blob/19823c2/docs/handbook/07-cerimonias-cadencia.md)). A unidade
certa para medir o trabalho em curso é, portanto, o número de **decisões que o humano segura
com qualidade**, e não o número de tarefas abertas ou de agentes ativos.

Duas consequências seguem. A primeira é onde paralelizar: **dentro** de uma feature já
decidida, e não **entre** features ambíguas. Dentro da feature, a intenção já foi fixada na
spec e o plano já foi aprovado; as fatias paralelas não pedem gate novo, só a integração no
fim. Entre features ambíguas, cada frente traz suas próprias perguntas, sua spec, seu plano e
seu merge, e cada uma dessas coisas passa pela mesma pessoa. O exemplo mostra o efeito: os
mesmos oito agentes, se as fatias de quatro deles fecham uma decisão só sobre o lote, liberam
todas as sessenta e quatro fatias do dia com o humano ocupado em dois terços do tempo
[CLAIM-03-026].

A segunda consequência é como escalar: **barateando o gate**, e não abrindo frentes. Um gate
fica barato quando o critério é verificável por máquina (o humano lê uma evidência, não
refaz o raciocínio; ver o [capítulo 10](../10-quality-gates-que-provam-fatos/capitulo.md)) e
quando a ação é reversível (errar custa um *revert*, e o gate pode ser mais leve; ver o
[capítulo 11](../11-risco-reversibilidade-e-autonomia/capitulo.md)). No exemplo, baixar o
custo de cada decisão de doze para seis minutos tira as vinte e quatro fatias da fila sem
mexer em agente nenhum [CLAIM-03-026].

### A armadilha do funil

Existe uma forma de "baratear o gate" que piora tudo: o humano decide continuar responsável
por cada item e, para dar conta, passa a ler cada saída na diagonal. O handbook chama isso de
**armadilha do funil**: se o humano é o Accountable da matriz Responsible, Accountable,
Consulted, Informed (RACI) **e** confere à mão cada saída de agente, ele recriou "fazer tudo
sozinho", com uma etapa a mais de leitura; o ganho evapora e ele vira o gargalo do próprio
sistema ([handbook 06 §5.2](https://github.com/GHDaru/maestro/blob/19823c2/docs/handbook/06-papeis-raci.md)).

A saída não é confiar mais no agente, é **mudar o objeto da responsabilidade**. Ser
Accountable pela política significa decidir uma vez por *classe* de ação ("toda mudança na
raia leve com testes verdes entra sem mim"; "toda migração de dados passa por mim") e
responder por essa decisão. Ser Accountable por item significa decidir N vezes e não
responder direito por nenhuma. Na linguagem da fila: a política tira itens da fila; a
leitura na diagonal só reduz o tempo por item, à custa da qualidade da decisão, que era a
única razão de o item estar ali. O [capítulo 2](../02-o-problema-da-confianca/capitulo.md)
mostra como essa responsabilidade pela política se torna verificável; aqui o que importa é o
efeito no fluxo.

### Cerimônia é função, não reunião

As cerimônias que um tech lead herdou do Scrum resolvem problemas de coordenação entre
pessoas. Quando o time é uma pessoa e N agentes, metade dessas funções deixa de existir. A
regra que o método adotou é perguntar pela função, não pelo evento: "essa função ainda
existe no meu contexto?". O planejamento continua, mas vira **dar forma e especificar**: a
spec é o planejamento real. A revisão vira **checkpoint de ciclo**. A reunião diária é
cortada, porque não há entre quem sincronizar, e o refinamento de backlog também, porque não
há backlog formal ([handbook 07 §5.1](https://github.com/GHDaru/maestro/blob/19823c2/docs/handbook/07-cerimonias-cadencia.md)).
A retrospectiva, ao contrário, ganha valor: com agentes, a correção que sai dela vira
instrução versionada e é aplicada no ciclo seguinte por quem não estava lá (o
[capítulo 14](../14-a-organizacao-que-aprende/capitulo.md) trata disso).

Na leitura de fila, toda cerimônia consome a mesma atenção que os gates: uma reunião diária
com agentes não sincroniza ninguém, só ocupa a restrição.

### Apetite: o tempo é fixo, o escopo é a variável

A segunda ferramenta de cadência vem do Shape Up (Singer, 2019): o **apetite**. Em vez de
estimar quanto uma feature vai levar, decide-se quanto tempo ela merece, e o escopo se ajusta
dentro desse tempo. Quando o apetite acaba, corta-se escopo; o prazo não se estende. Com
agentes, a regra ganha um motivo: o que o tech lead controla não é a velocidade do agente,
é quanto da própria atenção a aposta vai consumir. O exemplo mais visível no
histórico do método é a migração dos capítulos do handbook: um capítulo por ciclo, treze
ciclos, em vez de um mutirão de documentação que nunca termina [CLAIM-03-015].

### Não pergunte "continuo?": gaste atenção em gates, não em progresso

Há um último desperdício de atenção que é fácil de não ver: o agente que interrompe o humano
para perguntar se pode seguir. O método avaliou essa prática num estudo do Superpowers (um
conjunto de skills de código aberto) e registrou validação mútua com a regra de execução
contínua: o agente executa o plano até um bloqueio, uma ambiguidade real ou o fim, sem pedir
licença a cada passo ([handbook, apêndice B §6](https://github.com/GHDaru/maestro/blob/19823c2/docs/handbook/apendice-b-superpowers.md)).
Um "posso continuar?" é um item na fila que não carrega decisão nenhuma.

O par dessa regra é a **fila de decisões**: se o agente não pergunta à toa, a pergunta que
ele faz merece um lugar próprio, com prazo, opções, recomendação e destino da resposta.
Pergunta jogada no meio de uma conversa, como as de 10 e 16 de outubro, não tem idade visível
e não tem quem a cobre.

### Espera humana: a métrica que falta

Se o gargalo é a decisão humana, a métrica que importa é quanto tempo o trabalho espera por
ela. A agenda de pesquisa do livro lista a **espera humana** entre as métricas a medir, ao
lado do tempo de ciclo e do overhead de coordenação ([base de pesquisa](../../pesquisa/base-de-pesquisa.md)).
É o intervalo entre um pedido de decisão ficar pronto e a decisão ser registrada. Sem um
registro em que pedido e resposta tenham carimbo de tempo, a espera não existe como dado, só
como irritação; por isso o padrão deste capítulo começa por um registro, e não por um painel.

## Alternativas

O tech lead tem à mão dois tipos de alternativa: cadências de trabalho herdadas de times
humanos, e arquiteturas de coordenação vindas dos frameworks de agentes. A tabela compara as
duas famílias pelo critério deste capítulo: o que cada uma faz com a fila na frente do humano.

| Alternativa | O que traz | O que faz com a fila humana | Veredito |
|---|---|---|---|
| **Scrum** | papéis, sprint, cinco eventos | mantém eventos de sincronização entre pessoas que não existem; acrescenta cerimônia à restrição | **Parcial**: sobrevivem o planejamento (como spec) e a retrospectiva |
| **Kanban** (Anderson, 2010) | fluxo contínuo, limite explícito de trabalho em curso | dá o instrumento certo, desde que o limite seja medido em decisões humanas | **Adotado** |
| **Shape Up** (Singer, 2019) | apetite, ciclo com folga, sem backlog | fixa o tempo de atenção por aposta; corta escopo em vez de estender | **Adotado como esqueleto** |
| **Scrumban** | híbrido de Scrum e Kanban | herda o overhead de eventos do Scrum | **Observado** |
| **Frota de agentes** (enxames com topologia, filas e supervisão automática) | dezenas de agentes coordenados por máquina | produz mais trabalho do que um humano consegue julgar; trabalho não julgado é dívida com cara de velocidade | **Observar**, com gatilho: trabalho paralelo que a atenção de um humano consiga governar |
| **Supervisor hierárquico** (um agente gerente que distribui e recolhe, como o padrão *supervisor* do LangGraph ou o processo hierárquico do CrewAI) | roteamento e consolidação por modelo | tira da fila o trabalho de despacho, mas não o de decidir; quando o supervisor "aprova", a pergunta de quem responde fica sem resposta | **Útil como camada de despacho**, nunca como dono do gate |
| **"Aprovo tudo" / "aprovo nada"** | a escolha binária de confiar ou conferir | o primeiro esvazia a fila e o gate; o segundo é a armadilha do funil | **Rejeitado** em favor de responsabilidade pela política |
| **Painel de métricas clássico** | números de produtividade sobre código e produção | instrumenta antes de saber a quem comparar; frequentemente mede o proxy | **Recusado em escala pequena**; substituído por painel que projeta os arquivos quando a escala chegou |

A linha da frota merece um comentário, porque é a alternativa mais sedutora e a mais
diretamente oposta ao argumento deste capítulo. A ficha que o Maestro escreveu sobre ela não
diz "é cedo demais"; diz que a escolha é de fundo: a frota alarga a capacidade de execução, e
o gargalo é o julgamento humano, que ela não alarga ([ideia 018](https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/ideias/018-frota-de-agentes.md)).
O gatilho que reabre a questão não fala da máquina; fala do humano. É a forma certa de
registrar uma recusa: dizer o que teria de mudar para ela deixar de valer.

O supervisor hierárquico está do lado oposto: ele é útil. O próprio Maestro usa uma sessão
gerente que despacha tarefas a workers (ver o padrão adiante). O erro não é ter um agente
coordenador; é deixar que ele ocupe a posição de quem aceita. O despacho é responsabilidade
delegável; o aceite, pelos axiomas A1 e A2, não é.

Por fim, uma alternativa de interface observada em outubro: um diagrama vivo do time, em que
cada agente é um nó e o clique mostra o que ele faz ([ideia 041](https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/ideias/041-diagrama-vivo-do-time.md)).
Veredito: "observar", como linguagem visual, desde que seja projeção do estado e não decida
nada. É a condição que separa uma boa visualização de um segundo lugar onde o estado é
digitado.

## O padrão Maestro

O Maestro responde à pergunta deste capítulo em quatro camadas: uma regra de cadência, um
protocolo de coordenação entre sessões, uma identidade de sessão que não se adivinha e um
painel que projeta o estado sem decidir. Em cada uma, vale separar o que é **regra** (texto
que o agente lê), o que é **script** (executável que alguém roda) e o que é **hook**
(executável que o *harness* dispara sozinho).

### Cadência: uma feature, apetite fixo, cerimônias por função (regra)

O modelo operacional adota um esqueleto de Shape Up com Kanban, sem Scrum: reunião diária e
planejamento de sprint cortados, trabalho em curso limitado a uma feature ou spec por vez,
ciclos com apetite fixo, e cinco cerimônias com função declarada (dar forma e especificar,
execução, checkpoint de ciclo, período de folga, retrospectiva)
([operating-model.md §5](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/operating-model.md))
[CLAIM-03-014]. A retrospectiva é a única com saída obrigatória: erro recorrente vira regra
versionada. O princípio que sustenta a camada é o II da constituição: o Accountable é sempre
humano e responde pela política, pelos gates e pelos critérios, não por cada item
([principles.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/principles.md)).

Essa camada é **regra**, a mais frágil das quatro: nada a executa. O WIP de um sobreviveu
vinte e seis ciclos porque a escala não o testou [CLAIM-03-001]; diante de dezessete sessões
em paralelo [CLAIM-03-005], não tinha como recusar nada. As outras três camadas nasceram daí.

### Coordenação: o protocolo de tarefas entre gerente e workers (regra + script + hook)

Quando há uma sessão gerente e várias sessões worker, o contrato entre elas é um protocolo
de duas *tags* textuais ([task-ledger.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/task-ledger.md)).
Quem despacha começa a mensagem com uma tag `[[TASK ...]]` sozinha na linha, com
identificador, tipo, tentativa e ciclo; quem entrega termina com `[[DONE ...]]`, com o
desfecho. Uma auditoria nomeia a tarefa julgada (`target`) e o veredito (`verdict`). Contam a
**primeira** `[[TASK]]` e a **última** `[[DONE]]` da mensagem, para que um exemplo do
protocolo citado no meio do texto não seja confundido com despacho real.

A regra vira dado por um **script** (`scripts/record-task.py`, que valida cada linha contra
vocabulários fechados e a acrescenta a `docs/records/tarefas.jsonl`) e por um **mod** do
harness que lê as tags no momento em que acontecem. O livro de ponto resultante é
só-acréscimo e guarda tentativa, retrabalho, desfecho, tokens e custo por tarefa; em
`19823c2` ele tinha cinquenta e duas linhas [CLAIM-03-017]. O que importa aqui não é o
custo (tema do [capítulo 13](../13-observabilidade-e-economia/capitulo.md)), mas o contrato:
"quem está fazendo o quê" deixa de ser pergunta feita no chat. O relato
do projeto Hindiana registra que esse protocolo **não** era usado lá [CLAIM-03-017], e o
estado do time vivia em texto digitado por cada agente.

### Identidade: nome · ref · projeto, e o lançador que preserva o endereço (regra + script)

A falha de roteamento de outubro virou regra de glossário. Uma sessão é identificada por
três partes, `nome · ref · projeto`, porque o nome se repete e a referência (o `[xxxxxx]` que
o harness mostra ao lado do nome) é o único campo que distingue duas sessões homônimas, e
também o único que **expira**: muda quando a sessão reinicia
([glossary.md, "Ref de sessão" e "Endereçar por ref"](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/glossary.md)).
Daí a invariante: endereço ambíguo é **recusado**, nunca resolvido pelo "mais provável",
porque uma entrega no par errado não se desfaz.

O **script** que monta o time é o lançador multissessão
([scripts/multi-session.py](https://github.com/GHDaru/maestro/blob/19823c2/scripts/multi-session.py)),
adaptado do projeto Hindiana no ciclo 066. Ele abre um gerente e seis workers num terminal,
cada sessão com o seu modelo (o gerente num, os workers noutro), e dá a cada worker uma
*worktree* própria do Git, para que as edições e os commits de um não toquem os arquivos de
outro; nenhum segredo fica no repositório [CLAIM-03-016]. A opção de retomar o time caído
nasceu da queda de 29 de outubro e tem um teste que a mede rodando o lançador em modo de
ensaio, nunca lendo o código
([scripts/test_multi_session_retomar.py](https://github.com/GHDaru/maestro/blob/19823c2/scripts/test_multi_session_retomar.py))
[CLAIM-03-012]. A evolução posterior, de retomar pelo nome para retomar pelo identificador
da sessão, é a mesma regra do glossário aplicada ao próprio lançador: o nome não é
identidade [CLAIM-03-013].

### Estado: o painel que projeta os arquivos e nunca promove (script + hook)

O ADR 0022 decidiu que o Maestro passa a ter um **painel de coordenação**, com Python da
biblioteca padrão e uma página HTML (*HyperText Markup Language*), servido só em localhost
([ADR 0022](https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0022-painel-de-coordenacao-como-projecao-dos-arquivos.md)).
Três decisões dele são o coração do padrão:

1. **O banco local é projeção, nunca fonte.** O painel guarda o que lê num SQLite, mas toda
   tabela derivada é apagada e reconstruída a cada ingestão a partir dos arquivos que o método
   já obriga a escrever (specs, ADRs, vereditos, Git). É a separação entre escrita e leitura
   (*Command Query Responsibility Segregation*, CQRS) aplicada ao controle de um time.
2. **A única escrita direta é uma tabela de eventos só-acréscimo**, para fatos que não existem
   em arquivo nenhum (status de sessão, transição de peça, deploy, incidente); gatilhos no
   banco recusam alteração e remoção [CLAIM-03-020].
3. **O painel nunca promove nada sozinho.** Todo evento tem autor humano ou de sessão
   identificada, e transição de estado sem evidência parseável é recusada.

O ADR explica por que isso não é o débito que o YAGNI temia: o painel não instrumenta código
nem produção, e descartá-lo custa apagar um diretório. Em `19823c2`, o catálogo de artefatos do modelo operacional já trazia o painel como essencial
desde o ciclo 066, no lugar da linha "Later / YAGNI" [CLAIM-03-003]. Detalhe honesto: o
índice de decisões tem linhas para os ADRs vizinhos, mas não para o 0022, registrado só sob o
id do ciclo [CLAIM-03-025].

O ciclo 068 levou o princípio um passo adiante com o padrão "um chamado, uma pasta; cada
gate, um entregável": cada gate de uma unidade de trabalho deixa um arquivo com cabeçalho
(gate, objeto, veredito, quem julgou, data), e o estado **é** a leitura desses arquivos sob
regras fixas ([spec 068](https://github.com/GHDaru/maestro/blob/19823c2/specs/068-chamados-gate-a-gate/spec.md)).
A motivação está escrita na spec: o estado digitado mente; o estado calculado não. O mesmo
ciclo pôs o custo em tokens de cada sessão ao lado de cada passo, rotulado como estimativa.
O **hook** que sustenta essa camada é de pre-commit: ele recusa o commit de um arquivo de
veredito sem carimbo de tempo verificável, para que a data que o painel lê não seja digitada.

### Regência: a fila de decisões e o portão que só o humano registra (script)

O ciclo 072 construiu sobre isso o **painel de regência**, rodada 1: um quadro por gate e uma
fila de decisões ([spec 072](https://github.com/GHDaru/maestro/blob/19823c2/specs/072-painel-de-regencia/spec.md)).
O quadro tem dez colunas, de G0 a G9, derivadas dos arquivos de veredito; o cartão de cada
chamado mora no último gate aprovado e mostra o dono do gate atual, a idade no gate, o
veredito normalizado **ao lado** do original e um marcador de independência entre quem fez e
quem julgou [CLAIM-03-018]. A fila tem uma fonte nova, um registro só-acréscimo de pedidos e
respostas. O glossário do método fixa os termos
([glossary.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/glossary.md)):

- **pedido de decisão**: pergunta escalada ao humano com id, quem pediu, opções,
  recomendação, prazo, o que destrava e destino da resposta;
- **ruling**: a resposta registrada, com autor humano, data, destinatário e ligação ao merge
  ou ADR que a cita; ruling sem autor ou sem destinatário é recusado;
- **portão do regente**: os gates que só o humano registra (o aceite G7, a ordem de produção
  G8 e o fechamento `TAIL:gate`); para um agente, eles aparecem como item da fila em modo
  somente leitura.

O objetivo da tela foi escrito como frase de usuário: "em 5 segundos, saber o que me espera e
quem morreu; em 5 minutos, decidir" [CLAIM-03-019]. E a tela foi desenhada com anti-regras
verificáveis, que são a parte mais transferível do padrão
([jornada 072](https://github.com/GHDaru/maestro/blob/19823c2/docs/jornada/072-painel-de-regencia.md);
[desenho de interface do ciclo 066, §4](https://github.com/GHDaru/maestro/blob/19823c2/specs/066-painel-de-regencia/ux-design.md)):

- **vazio é informação**: "fila vazia — nenhuma decisão registrada", com contador zero, e não
  uma tela que some;
- **"—" com motivo, nunca valor padrão**: fonte ausente aparece como travessão acompanhado do
  motivo, e não como `0` ou `n/a`;
- **nada é marcado "conferido" se foi calculado à mão**: sem o script que confere, o marcador
  diz "não conferido", nunca verde;
- **o veredito original fica ao lado do normalizado**: normalizar é traduzir, não apagar a
  palavra do arquivo;
- **não há "dispensar"**: pergunta sem ruling fica na fila até ser respondida ou devolvida.

O mesmo ciclo mostrou a política de gates em funcionamento: o gate de pronto para executar
(*Definition of Ready*, DoR) da spec do 072 foi decidido pela sessão regente com parecer de
um crítico em contexto fresco, sob a delegação escrita que o humano deu em 24 de outubro e que
o ADR 0026 formalizou ([decisoes.jsonl, `decisao-072-gates-delegados`](https://github.com/GHDaru/maestro/blob/19823c2/docs/records/decisoes.jsonl))
[CLAIM-03-021]. É a armadilha do funil resolvida na prática: o humano respondeu pela
política, uma vez, e não por cada spec.

O roadmap registra o estado honesto dessa camada em `19823c2`: o workflow do ciclo em SQLite
(fase F34) está **parcial**, com requisitos ausentes ou invertidos que passaram ao escopo do
072, e o painel de regência (F35) está na rodada 1, com a rodada 2 declarada como raia de
infraestrutura [CLAIM-03-024].

### A tela que o regente lê: frase-chave e navegação curta

Os ciclos seguintes trataram a atenção do regente como requisito de interface. O ciclo 074
abriu em 26 de outubro um protótipo navegável do painel, organizado por contexto delimitado,
com um contrato para as ações simuladas (cada botão declara o que faria, quem autoriza e o
efeito) e uma definição de pronto executável, um verificador de navegação que anda pelo
protótipo ([decisoes.jsonl, `decisao-074-prototipo-navegavel`](https://github.com/GHDaru/maestro/blob/19823c2/docs/records/decisoes.jsonl))
[CLAIM-03-022]. Dele saíram dois termos que o glossário guarda. A **frase-chave** é a frase
de abertura da tela inicial ("você tem 3 decisões esperando, a mais antiga há 7 h") e é
**derivada** da fila, nunca digitada; **registrar ruling** é a ação humana que tira o pedido
da fila e faz o contador baixar. A frase traduz a fila numa leitura de cinco segundos e põe
a espera humana na primeira linha da tela.

O ciclo 076 reduziu a navegação: o ADR 0031 registra que a regra de uma trilha de contexto
no rodapé tinha nascido com vinte telas e, com a navegação reduzida a sete itens e um botão
global, as vistas irmãs viraram abas no topo e a regra antiga deixou de valer, com a dívida
das telas antigas declarada ([ADR 0031](https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0031-abas-de-contexto-no-topo.md))
[CLAIM-03-023]. Menos tela é menos atenção gasta em achar onde se está.

### O que fica com o humano, e o que o script faz

A tabela resume o padrão; em nenhuma linha o executável decide. O índice de scripts do método
formula isso como princípio: os scripts tiram o passo mecânico da atenção do orquestrador, que é o gargalo, sem tirar dele
a decisão; cada um nasceu de dor real numa retrospectiva
([scripts/README.md](https://github.com/GHDaru/maestro/blob/19823c2/scripts/README.md)).

| Peça | Tipo | O que faz | O que não decide |
|---|---|---|---|
| WIP de uma feature, apetite, cerimônias por função | regra | limita a fila na origem | nada é recusado por máquina |
| `[[TASK]]` / `[[DONE]]` | regra + script + mod | registra despacho, entrega e veredito | se a tarefa foi bem feita |
| `nome · ref · projeto` | regra | define endereço; ambíguo é recusado | — |
| `multi-session.py` | script | sobe o time com modelo por sessão e worktree por worker; retoma o time caído | quem trabalha em quê |
| painel de coordenação | script (servidor local) | projeta os arquivos; eventos só-acréscimo | nunca promove |
| hook de veredito | hook (pre-commit) | recusa veredito sem carimbo verificável | o mérito do veredito |
| painel de regência | script (servidor local) | kanban por gate, fila de decisões, frase-chave | ruling, G7, G8 e `TAIL:gate` são do humano |

## Exemplo executável

A pasta [`exemplo/`](exemplo/README.md) tem dois scripts, só com a biblioteca padrão do
Python 3.8 ou superior. Nenhum chama modelo de IA: o primeiro mede a fila que se forma na
frente do humano; o segundo constrói a fila de decisões a partir de um registro, do jeito que
o padrão descreve.

```bash
cd livro/03-um-humano-muitos-agentes/exemplo
python gargalo.py
python fila.py
```

**`gargalo.py`** simula, sem sorteio, um dia de oito horas de um humano que decide as fatias
entregues por N agentes (uma por agente por hora, doze minutos por decisão). Três blocos: mais
agentes com o mesmo gate (a vazão para em quarenta a partir de cinco agentes; com dezesseis,
oitenta e oito fatias dormem e a espera máxima chega a 330 minutos); o gate mais barato (com
seis minutos, a fila de oito agentes zera); e paralelizar dentro da feature (uma decisão de
vinte minutos por lote de quatro fatias libera as sessenta e quatro do dia, com o humano
ocupado em 67% do tempo) [CLAIM-03-026].

```text
A  mais agentes, mesmo gate
  cenário                      prod decid  fila  esp.méd  esp.máx   ocup
   4 agente(s)                   32    32     0      0.0      0.0    80%
   5 agente(s)                   40    40     0      0.0      0.0   100%
   8 agente(s)                   64    40    24     87.8    180.0   100%
  16 agente(s)                  128    40    88    160.9    330.0   100%
```

**`fila.py`** lê um roster de sessões e um registro só-acréscimo de eventos e aplica as
regras do padrão: endereço `nome · ref · projeto` resolvido para uma sessão viva; pedido sem
prazo, opções ou recomendação recusado; ruling só com autor humano e destino; nada de
"dispensar". Deriva a frase-chave em três instantes, mede a espera humana (média de 4 h 34
min, máxima de 8 h 16 min, dois de quatro pedidos respondidos depois do prazo) e prova, por
mutação, que reescrever uma linha do registro é acusado. Sai com código 0 quando os dezesseis
eventos têm o veredito esperado e a mutação é acusada [CLAIM-03-027].

```text
== frase-chave (derivada da fila, nunca digitada)
  14:00  você tem 3 decisões esperando; a mais antiga (D-01) há 6 h 56 min
  14:35  você tem 2 decisões esperando; a mais antiga (D-01) há 7 h 31 min
  16:00  você tem 1 decisão esperando; a mais antiga (D-08) há 55 min
```

Os dados são fictícios, mas imitam os casos de outubro: um pedido às 07:04 com prazo às
09:00, respondido às 15:20; uma sessão homônima em outro projeto; uma sessão caída. O
exercício útil é pôr no `gargalo.py` os números do seu time e descobrir a partir de quantos
agentes você vira a fila. As saídas de referência estão em `saida-esperada-*.txt`.

## Contraexemplo

**Quando o WIP de um é conservador demais.** O limite de uma feature de cada vez é uma
consequência da restrição, não um valor em si. Se as decisões que um trabalho exige são
poucas e baratas (correções na raia leve, com testes verdes e reversão trivial), a fila não
se forma, e manter uma frente só deixa o humano ocioso enquanto os agentes esperam a próxima
aposta. No exemplo, com quatro agentes e doze minutos por decisão, o humano está ocupado em
oitenta por cento e ninguém espera [CLAIM-03-026]: ainda cabe trabalho. A regra correta não é
"uma frente", é "não passe da capacidade de decisão", e uma frente é só o jeito mais simples de
garantir isso quando ninguém mede.

**Quando o painel é débito.** O argumento do YAGNI contra o painel era bom enquanto a escala
era pequena, e o próprio ADR 0022 diz que ele valia sem escala. Um humano com um ou dois
agentes lê o estado nos arquivos e no Git sem esforço; construir servidor, ingestão e tela
para isso é instrumentar antes de ter a quem comparar. Ele também cobra disciplina (sem
registrar status e deploy, o quadro mostra "—", risco que o ADR aceita por escrito). E pode
mentir, como mostrou a tela fria do 072
[CLAIM-03-010]: uma projeção que exibe "vazio" enquanto calcula é pior que nenhuma, porque
tem crédito. Painel só vale quando a dor de coordenação é medida, e só se ele declarar os
próprios estados (carregando, defasado, erro de fonte).

**Quando a fila de decisões vira depósito.** Uma fila com prazo e recomendação convida os
agentes a escalarem tudo, e uma fila em que tudo é escalado é a armadilha do funil com outra
roupa. A regra "não existe dispensar" agrava o risco, porque nada sai da fila sem ruling ou
devolução. A fila só funciona se a política tirar dela as classes de decisão que não precisam
do humano; caso contrário, a frase-chave vira um contador que só cresce e o humano aprende a
não olhar.

**Quando a execução contínua passa do ponto.** "Não pergunte se pode continuar" pressupõe que
o agente reconhece uma ambiguidade real. Quando ele não reconhece, a regra transforma uma
pergunta barata numa correção cara depois. O antídoto não é voltar a pedir licença a cada
passo; é a spec fixar a intenção antes (o [capítulo 4](../04-a-spec-como-partitura/capitulo.md))
e o agente tratar silêncio da spec como bloqueio.

**Quando a delegação de gate é o atalho.** A delegação por política com crítico independente
resolveu o funil no 072, mas ela tem custo: o humano deixa de ver os itens. Três dias depois
dessa delegação, o gate humano de usabilidade reprovou um protótipo que verificadores e a
regente tinham aprovado (o [capítulo 2](../02-o-problema-da-confianca/capitulo.md) conta o
caso) [CLAIM-03-031]. Baratear o gate não é eliminá-lo: há perguntas, como "isto tem uma história clara
para quem usa?", que ainda não têm crítico que as substitua.

**Quando o caso de origem não generaliza.** As falhas de outubro vêm de um projeto, um
harness e um humano. A saturação na decisão humana é matemática de fila e vale em geral; os
números (dezessete sessões [CLAIM-03-005], dez horas paradas [CLAIM-03-013]) não. Meça o
próprio limite antes de adotar o de outro.

## Evidência

O que sustenta o capítulo, separado pelo grau de confiança. Todos os claims estão em
[`claims.md`](claims.md), com a evidência reproduzível.

**Medido (um comando reproduz):** a saturação da vazão na capacidade de decisão e o efeito
de baratear o gate e de paralelizar dentro da feature, no modelo determinístico do exemplo
[CLAIM-03-026]; as regras da fila e a frase-chave derivada [CLAIM-03-027]; o tamanho do livro
de ponto de tarefas [CLAIM-03-017]; a ausência de linha para o ADR 0022 no índice de decisões
[CLAIM-03-025]; os sete nomes de sessão do lançador [CLAIM-03-016].

**Observado (lido no artefato citado, com data):** o WIP de um em agosto [CLAIM-03-001]; a
ficha da frota e o painel recusado por YAGNI [CLAIM-03-002] [CLAIM-03-003]; a lacuna da fila
sem dono [CLAIM-03-004]; a escala do projeto Hindiana e as falhas de estado, endereço e espera
[CLAIM-03-005] a [CLAIM-03-008]; a integração da linha paralela e o ADR 0022 [CLAIM-03-009];
os dois defeitos do painel de regência, achados R1 e R7 da jornada de uso [CLAIM-03-010] [CLAIM-03-011]; a queda do time e as
duas correções do lançador [CLAIM-03-012] [CLAIM-03-013]; o padrão de cadência, de painel e
de fila [CLAIM-03-014] a [CLAIM-03-024].

**Hipótese (plausível, não testada aqui):**

- A extensão do axioma A3 à atenção de quem rege (a atenção humana degrada com ruído como a
  janela do agente) é um argumento por analogia [CLAIM-03-028].
- A hipótese H4 da agenda de pesquisa, "multiagente só ajuda com cortes independentes", é
  compatível com o que este capítulo mostra, mas o histórico do Maestro não a testa: não há
  grupo de controle, e o caso Hindiana mistura escala com mudança de projeto [CLAIM-03-029].
- A **espera humana** não é medida de forma sistemática no Maestro em `19823c2`: os casos de
  sete e vinte e quatro horas [CLAIM-03-008] vêm de relato escrito, não de registro com carimbo; a fila do
  072 cria a fonte, mas não há série histórica [CLAIM-03-030]. O
  [capítulo 15](../15-validando-o-maestro/capitulo.md) descreve como medi-la.

O que a recomendação deste capítulo deve a essas hipóteses fica dito. A regra central (medir o
trabalho em curso em decisões humanas e escalar barateando o gate) se apoia na matemática de
fila, medida no exemplo [CLAIM-03-026], e não nelas. O que depende delas é a **calibragem**:
quanto custa uma decisão, a partir de que ocupação a atenção de quem rege começa a errar,
que espera é tolerável. Como o Maestro ainda não tem série histórica de espera
[CLAIM-03-030], nenhum desses números é transferível; o primeiro passo de segunda-feira é
registrar a própria fila (o `fila.py` do exemplo basta) por duas semanas antes de fixar
limite algum. Se a analogia do A3 [CLAIM-03-028] estiver errada, o limite de decisões por dia
fica mais alto, mas continua existindo.

Dois limites do argumento ficam registrados. Primeiro, o modelo de fila do exemplo é
determinístico; filas reais têm variabilidade, e com ela a espera começa a crescer **antes**
de cem por cento de ocupação, o que torna o argumento mais forte, não mais fraco. Segundo, os
números de outubro são de um relato da sessão de coordenação do projeto, preservado como
insumo do ciclo 066; eles são consistentes com o ADR 0022, que os cita, mas não foram
recontados a partir das fontes primárias, que estão fora do repositório do método. E a própria
fonte tem uma inconsistência aritmética: o ADR 0022 e a spec 066 falam em "16 sessões", mas a
lista do ADR (duas de coordenação, dois gerentes, treze workers) soma dezessete, e o banco do
painel do projeto, no mesmo insumo, registra dezessete sessões. Este capítulo usa dezessete e
trata o número como observado com discrepância declarada [CLAIM-03-005]. Terceiro, a parada
de dez horas [CLAIM-03-013] é o único fato posterior à versão de referência `19823c2`: vem
da mensagem do commit `8c79331`, de 1º de novembro.

## Checklist

Itens que você aplica no próprio time, cada um com uma verificação.

- [ ] **Capacidade de decisão medida.** Você sabe quantas decisões por dia consegue tomar com
  qualidade e quanto custa cada uma. Verificação: rode `gargalo.py` com os seus números e
  anote a partir de quantos agentes a fila aparece.
- [ ] **WIP medido em decisões.** O quadro do time mostra quantas decisões humanas estão
  pendentes, e não só quantas tarefas estão abertas. Verificação: a resposta a "o que espera
  por mim agora?" sai de um comando ou de uma tela, não da memória.
- [ ] **Paralelismo dentro, não entre.** Toda frente paralela aberta neste mês tem spec e
  plano aprovados antes de os agentes começarem. Verificação: liste as branches ativas e
  confira, para cada uma, a data do aceite da spec.
- [ ] **Responsabilidade pela política.** Existe uma lista escrita de classes de decisão que
  **não** passam por você, e uma das que sempre passam. Verificação: a lista está num arquivo
  versionado e tem data.
- [ ] **Cerimônias com função nomeada.** Cada cerimônia que o time mantém tem a função escrita
  ao lado. Verificação: nenhuma linha diz "porque sempre fizemos".
- [ ] **Apetite no lugar de prazo.** Cada aposta tem o tempo que merece, e o que não coube foi
  cortado em escopo, não estendido. Verificação: o último ciclo que estourou tem um registro
  do que foi cortado.
- [ ] **Pedido de decisão estruturado.** Toda pergunta ao humano tem id, quem pediu, opções,
  recomendação, prazo, o que destrava e destino da resposta. Verificação: um pedido sem prazo
  é recusado por script, como no `fila.py`.
- [ ] **Estado derivado, não digitado.** O "onde está cada coisa" é calculado de arquivos ou
  de eventos com carimbo, e nenhum agente escreve o próprio status à mão. Verificação: apague
  o painel e reconstrua; a projeção sai igual.
- [ ] **Endereço não se adivinha.** Mensagens entre sessões usam um identificador que
  distingue homônimos, e endereço ambíguo é recusado. Verificação: crie duas sessões com o
  mesmo nome e confira que a entrega falha em vez de escolher uma.
- [ ] **Queda prevista.** Existe um jeito testado de retomar o time inteiro com o contexto de
  cada sessão. Verificação: o teste roda em modo de ensaio, sem abrir sessão real.
- [ ] **O painel declara os próprios estados.** Vazio, carregando, defasado e erro de fonte têm
  cara própria, e fonte ausente aparece como "—" com motivo. Verificação: abra a tela com o
  servidor frio e veja o que ela diz.
- [ ] **Espera humana medida.** Você sabe a espera média e a máxima da última semana, e
  quantos pedidos estouraram o prazo. Verificação: o número sai do registro, como no
  `fila.py`.

## Referências

- Axiomas, teoremas e corolários do Maestro (A1, A2, A3).
  https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/axioms.md
- Constituição do Maestro, Princípio II.
  https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/principles.md
- Modelo operacional do Maestro, §5 (cerimônias e cadência) e §6 (catálogo de artefatos).
  https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/operating-model.md
- Glossário do Maestro ("Ref de sessão", "Endereçar por ref", "Painel de regência", "Pedido de
  decisão", "Ruling", "Portão do regente", "Frase-chave", "Registrar ruling").
  https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/glossary.md
- Protocolo de tags e livro de ponto de tarefas.
  https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/task-ledger.md
- Índice de scripts do Maestro.
  https://github.com/GHDaru/maestro/blob/19823c2/scripts/README.md
- Lançador multissessão e o teste da retomada.
  https://github.com/GHDaru/maestro/blob/19823c2/scripts/multi-session.py ·
  https://github.com/GHDaru/maestro/blob/19823c2/scripts/test_multi_session_retomar.py
- ADR 0022 — Painel de coordenação como projeção dos arquivos.
  https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0022-painel-de-coordenacao-como-projecao-dos-arquivos.md
- ADR 0031 — Abas de contexto no topo.
  https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0031-abas-de-contexto-no-topo.md
- Specs dos ciclos 066 (painel v0), 068 (chamados gate a gate) e 072 (painel de regência), e o
  insumo do ciclo 066.
  https://github.com/GHDaru/maestro/blob/19823c2/specs/066-painel-de-coordenacao-v0/spec.md ·
  https://github.com/GHDaru/maestro/blob/19823c2/specs/068-chamados-gate-a-gate/spec.md ·
  https://github.com/GHDaru/maestro/blob/19823c2/specs/072-painel-de-regencia/spec.md ·
  https://github.com/GHDaru/maestro/blob/19823c2/specs/066-painel-de-regencia/insumo-hindiana.md
- Desenho de interface do painel de regência (jornada às 07:00, anti-regras).
  https://github.com/GHDaru/maestro/blob/19823c2/specs/066-painel-de-regencia/ux-design.md
- Jornada viva do painel de regência, com a heurística datada (R1–R8).
  https://github.com/GHDaru/maestro/blob/19823c2/docs/jornada/072-painel-de-regencia.md
- Índice de decisões (`ciclo-066-integra-painel-controle`, `decisao-072-gates-delegados`,
  `decisao-074-prototipo-navegavel`).
  https://github.com/GHDaru/maestro/blob/19823c2/docs/records/decisoes.jsonl
- Roadmap do Maestro, fases F34 e F35.
  https://github.com/GHDaru/maestro/blob/19823c2/docs/roadmap.md
- Catálogo do ecossistema: ideias 018 (frota de agentes) e 041 (diagrama vivo do time).
  https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/ideias/018-frota-de-agentes.md ·
  https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/ideias/041-diagrama-vivo-do-time.md
- Handbook do Maestro, capítulos 06 (papéis e RACI, §5.2) e 07 (cerimônias e cadência), apêndice
  B (Superpowers, §6) e diagrama 06 (fluxo v5, lacuna 1), na cópia congelada em
  `maestro-handbook/` deste repositório.
- Base de pesquisa do livro (agenda de métricas e hipóteses H1–H10), em
  `pesquisa/base-de-pesquisa.md` deste repositório.
- J. D. C. Little. *A Proof for the Queuing Formula: L = λW*. Operations Research, 9(3), 1961.
- J. F. C. Kingman. *The single server queue in heavy traffic*. Mathematical Proceedings of the
  Cambridge Philosophical Society, 57(4), 1961.
- E. M. Goldratt e J. Cox. *The Goal: A Process of Ongoing Improvement*. North River Press, 1984.
- D. G. Reinertsen. *The Principles of Product Development Flow*. Celeritas Publishing, 2009.
- D. J. Anderson. *Kanban: Successful Evolutionary Change for Your Technology Business*. Blue Hole
  Press, 2010.
- Commit `8c79331` do Maestro (01/11/2026, ciclo 075, descendente de `19823c2`), cuja
  mensagem registra a parada de dez horas de 31/10; integrado como `3c94811` na linha da v1.
  Reproduzir num clone do Maestro: `git log -1 8c79331`.
- R. Singer. *Shape Up: Stop Running in Circles and Ship Work that Matters*. Basecamp, 2019.
  https://basecamp.com/shapeup (acesso em 02/11/2026).
