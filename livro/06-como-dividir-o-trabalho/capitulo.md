# 06 — Como dividir o trabalho

> *Fatiar é fácil. Juntar de volta é o trabalho, e o corte decide quanto ele vai custar.*

Com agentes de Inteligência Artificial (IA), abrir mais uma frente de trabalho custa um
comando. A tentação é óbvia: cinco agentes terminam em um quinto do tempo. Não terminam. Cada
fatia volta verde no próprio teste, e o conjunto chega contraditório, porque duas fatias
resolveram o mesmo problema de dois jeitos ou porque uma esperava um contrato que a outra nunca
escreveu. Este capítulo mostra onde cortar para que agentes em paralelo não colidam, como
medir se o paralelo pagou a coordenação que exigiu e, sobretudo, quando não dividir. É o
capítulo que separa o time que ganha velocidade com agentes do time que só multiplica o
retrabalho.

## Pergunta central

Onde cortar o trabalho para que agentes em paralelo não colidam, e como saber quando é melhor
não cortar?

## Resultado de aprendizagem

Ao final do capítulo, você consegue:

1. **Derivar** do limite de contexto por que o trabalho precisa ser fatiado e por que a junção
   das fatias é julgamento, não colagem, e explicar a quem esse julgamento pertence.
2. **Diagnosticar** um plano de divisão apontando os três defeitos que o corte cria: arquivo
   com dois escritores, conceito com mais de um dono e contrato consumido sem dono.
3. **Ordenar** fatias em ondas a partir dos contratos (o dono antes de quem consome) e calcular
   se o tempo paralelo, somado ao custo de coordenação, fica abaixo do tempo de um agente só.
4. **Escolher** o padrão de orquestração de cada situação pela regra da menor autonomia que
   resolve e dizer que evidência você exigiria antes de subir um degrau.
5. **Escrever** gatilhos observáveis para as práticas de paralelismo (isolamento por
   *worktree*, grafo de dependências, contrato por fatia), em vez de adotá-las por antecipação
   ou esquecê-las depois que o gatilho dispara.

## A falha real

Entre 29 e 30 de outubro de 2026, o ciclo 074 do Maestro fechava um protótipo navegável do
painel de regência, a tela em que o humano acompanha o time de agentes. O trabalho corria com
um time de verdade: uma sessão Gerente e Workers numerados, cada um na sua própria cópia de
trabalho do repositório, entregando por *cherry-pick* que o Gerente integrava na linha
principal. O ciclo fora cortado por **peça de tela**: seis podas, de P1 a P6, cada uma com o
seu Worker ou o seu par de Workers [CLAIM-06-006]. Parecia um corte limpo. Cada Worker tinha a
sua tela, os seus arquivos, a sua sonda.

O problema era um número. A pergunta "quem precisa de mim agora?" era uma das seis peças que o
ciclo tinha escolhido redesenhar [CLAIM-06-006], e a resposta aparecia em três lugares: no item do menu, no chip da tela de entrada e no
filtro da tela de andares. Cada tela tinha dono. O **conceito** não tinha. Cada Worker calculou
o número do seu jeito, e cada cálculo passava no teste da própria peça. Com os dados de exemplo do
protótipo, o chip da tela de entrada contava as linhas do time no ar e mostrava **1**; a união
de pedidos de decisão aguardando com sessões esperando o humano, que é o que o operador queria
saber, dava **4** [CLAIM-06-001]. Verde em cada fatia, contraditório no conjunto.

Ninguém descobriu isso lendo o código com atenção. Descobriu-se porque dois Workers, sem
combinar, levantaram a mesma pergunta pelo canal de pendências: o Worker01 numa declaração
sobre qual número o menu deveria mostrar, o Worker04 numa análise da costura do contador nos
andares. A fila de decisões do Gerente registrou as duas como "a mesma decisão", que "viajam
juntas" [CLAIM-06-005]. Nenhum dos dois podia decidir sozinho, porque a resposta não estava em
nenhuma das peças: estava no conceito que atravessava as três.

A correção não foi um agente a mais para "consolidar". Foi uma decisão de quem tinha o
contexto global e um corte novo. Decidiu a **regente**, a sessão que conduz o time acima do
Gerente e a quem o mantenedor do Maestro tinha delegado por escrito os seus portões, sob uma
política dele e com crítico independente em contexto fresco, decisão registrada num
*Architecture Decision Record* (ADR), o 0026, cinco dias antes
[CLAIM-06-027]. Em 29/10, a regente fixou que haveria **um número só**, saído de **um predicado
só**:
pedidos aguardando unidos às sessões em "aguardando humano" sem pedido, sem contar a mesma
sessão duas vezes. E o Gerente redistribuiu o trabalho pela fronteira do conceito, não pela
tela [CLAIM-06-003]:

- o **Worker01** passou a ser dono do contrato público do predicado (`quemPrecisaDeVoce`) e
  entregaria **primeiro**; os consumidores esperariam por ele;
- o **Worker02**, em paralelo, abriria na casca da aplicação uma porta para recontar o menu,
  **inerte**: sem ninguém chamá-la, o comportamento seria o de antes;
- o **Worker05** trocaria o chip da entrada para ler o mesmo predicado e ligaria a porta,
  **depois** do Worker01;
- a fatia do Worker04 nos andares foi **cancelada** no mesmo dia, desta vez por decisão do
  próprio mantenedor, que transferiu os andares para o ciclo seguinte.

As três entregas pousaram nessa ordem: a porta inerte às 08h08 de 29/10, o predicado às 12h12
do mesmo dia, o chip e a chamada às 09h06 de 30/10, cada uma integrada por cherry-pick
[CLAIM-06-002]. O commit do Worker05 trouxe ainda um segundo defeito, consertado no mesmo
commit e da mesma família: uma ação portada de outra tela procurava a sessão pelo nome nu,
`Worker04`, quando a rota casava a linha pela identidade completa (`nome [ref] · projeto`). A
sonda pegou o painel abrindo a ficha de **outra** sessão [CLAIM-06-004]. Dois defeitos no
mesmo dia, e os dois eram de divisão: um conceito sem dono e um endereço ambíguo.

O que torna esta falha útil para um tech lead é que ela não tinha cara de falha. Os arquivos
eram diferentes, os Workers não pisaram uns nos outros, nenhum *merge* conflitou. A regra mais
comum para decidir se duas tarefas podem correr em paralelo, "arquivos diferentes e nenhuma
dependência pendente", teria aprovado o corte por tela. O defeito não estava no arquivo. Estava
no conceito.

## Teoria

### Por que dividir: o axioma do contexto

O Maestro deriva este capítulo de um axioma, o A3: **o contexto é finito e degrada ao
encher**. A janela que um agente lê tem limite, e o desempenho cai à medida que ela se enche de
ruído. É uma propriedade física da ferramenta, não um hábito de quem a opera. O próprio texto
do axioma diz o que acontece se você o retirar: deixa de haver razão para fatiar o trabalho,
resetar o contexto ou manter o agente estreito
([axiomas](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/axioms.md)).

Daí sai a primeira metade da regra: um trabalho grande demais para caber limpo numa janela
precisa ser cortado. O [capítulo 5](../05-engenharia-de-contexto/capitulo.md) trata das
operações sobre o contexto de **um** agente. Este trata do passo seguinte: quando o trabalho
vira várias janelas, cada uma com um agente.

### O custo que o axioma esconde: o *reduce*

A segunda metade é menos óbvia. Quando você divide, distribui o contexto. Cada agente vê a sua
fatia e não vê o todo, e é justamente por isso que ele trabalha bem. Mas alguém precisa juntar
as fatias, e juntar exige o contexto **global**, que é o que a divisão acabou de espalhar. O
handbook do Maestro chama isso de *map-reduce* cognitivo: o *reduce* não é concatenação, é
julgamento com contexto global, e por isso pertence a quem tem esse contexto, o orquestrador
humano
([handbook, cap. 5 §3](https://github.com/GHDaru/maestro/blob/19823c2/docs/handbook/05-orquestracao.md)).
"Humano", aqui, quer dizer quem responde pela política: no ciclo 074 o julgamento foi de uma
sessão regente agindo sob delegação escrita do mantenedor, que continuou responsável pela
delegação e podia revogá-la. O [capítulo 11](../11-risco-reversibilidade-e-autonomia/capitulo.md)
trata de quando essa delegação é segura; o que importa aqui é que o *reduce* foi para **um**
ponto com o contexto global, e não para um agente consolidador ao lado dos Workers.

A tentação, quando as fatias voltam inconsistentes, é pôr um agente para consolidar. Ele não
tem o contexto global; recebe cinco opiniões e devolve a média delas. No ciclo 074, o "reduce"
foi uma decisão sobre o que o operador precisa ver, coisa que nenhum Worker, nem um sexto, podia
tomar a partir das peças.

### O corte é mais traiçoeiro que o *reduce*

O map-reduce clássico pressupõe partes independentes. Em software elas quase nunca são: porta
e adaptador dividem um contrato, tela e serviço dividem um formato, três telas dividem um
número. O handbook formula a consequência sem rodeio: paralelize por **fronteira** (contexto
delimitado, contrato, camada), nunca por **quantidade**, e nenhuma reconciliação salva uma
fatia cortada fora da costura
([handbook, cap. 5 §5.1](https://github.com/GHDaru/maestro/blob/19823c2/docs/handbook/05-orquestracao.md)).

Essa ideia é velha e tem dono. Em 1972, David Parnas comparou duas decomposições do mesmo
programa e mostrou que a decomposição pelos **passos do processamento**, a mais natural,
produzia módulos que mudavam todos juntos, enquanto a decomposição por **decisões de projeto
que cada módulo esconde** produzia módulos que mudavam sozinhos. O critério de Parnas é
exatamente o que faltou no ciclo 074: a decisão "o que conta como precisar do humano" não
estava escondida em módulo nenhum; estava espalhada por três telas. Cortar por tela é cortar
pelos passos que o usuário vê; cortar pelo conceito é cortar pela decisão que pode mudar.

Daí a regra operacional que este capítulo defende, em três partes:

1. **Cada arquivo tem um escritor** por vez. É a parte que todo mundo já conhece.
2. **Cada conceito tem um dono**. Quem consome o conceito não o recalcula; lê o contrato do
   dono.
3. **Cada contrato é escrito antes de ser consumido**. A ordem de execução sai daí: o dono
   antes de quem consome.

A primeira parte pega colisões de texto. As outras duas pegam colisões de significado, que são
as que passam pelos testes.

### Duas leis clássicas que valem dobrado com agentes

**Conway** (1968) observou que um sistema reproduz a estrutura de comunicação de quem o
desenhou. Com pessoas, a estrutura de comunicação é dada pela organização; com agentes, **você**
a desenha a cada plano de tarefas. O corte vira arquitetura: se três agentes calculam o mesmo
número em três lugares, o sistema terá três cálculos. A lei de Conway deixa de ser uma
observação sobre organizações e vira uma decisão sua, refeita a cada ciclo.

**Brooks** (1975) mostrou que a comunicação cresce mais rápido que o time: entre *n*
participantes há *n*(*n*−1)/2 canais possíveis. Um Gerente com seis Workers, a formação que o
Maestro usou nos ciclos 066 em diante, tem sete sessões e, portanto, 21 canais possíveis
[CLAIM-06-024]. O método não deixa os 21 abertos: as tarefas descem do Gerente e as entregas
sobem para ele, de modo que a comunicação passa por um ponto só. É deliberado, e tem preço: o
Gerente vira a parte serial.

E aí entra **Amdahl** (1967): o ganho de paralelizar é limitado pela parte que não paraleliza.
No trabalho com agentes, a parte serial tem nome: o *reduce* humano, o portão de revisão, a
integração. Se cada fatia exige uma passagem pelo Gerente e uma decisão da regente, dobrar o
número de Workers não dobra a vazão; aumenta a fila na frente do humano. O
[capítulo 3](../03-um-humano-muitos-agentes/capitulo.md) trata desse limite pelo lado da
atenção humana; aqui ele aparece pelo lado do corte.

### Overhead de coordenação: a métrica que decide

Se o corte tem custo, ele pode ser medido. O livro chama de **overhead de coordenação** a
fração do tempo (ou dos *tokens*) de um trabalho paralelo que foi gasta em passagens entre
fatias e em reconciliação, e não em produzir as fatias. A pergunta "vale paralelizar?" vira uma
desigualdade: o caminho crítico das fatias, somado à coordenação, precisa ficar abaixo do tempo
de um agente fazendo tudo em sequência.

O exemplo deste capítulo calcula essa conta num modelo de brinquedo. Com o Maestro real, ela
**não foi medida**: o método registra tokens por tarefa etiquetada, mas não separa o que foi
produção do que foi coordenação. Fica como hipótese a medir, e o
[capítulo 13](../13-observabilidade-e-economia/capitulo.md) discute a instrumentação. Uma
consequência, porém, já se vê sem medir: corte errado aparece como retrabalho, e o retrabalho
do ciclo 074 foram três entregas a mais, de três Workers, para chegar a um número
[CLAIM-06-002].

### O espectro fluxo ↔ agente e a menor autonomia que resolve

Dividir o trabalho também é escolher **quem decide a divisão**. Num extremo, você fixa o
caminho: os passos estão escritos, o agente executa cada um. No outro, o modelo decide o corte
na hora. A Anthropic, no texto *Building effective agents*, chama o primeiro lado de
*workflows* e o segundo de *agents*, e descreve seis padrões ao longo desse espectro
[CLAIM-06-007]:

| Padrão | O que é | Lado do espectro |
|---|---|---|
| Encadeamento | passos fixos em sequência, cada um consome a saída do anterior | fluxo |
| Roteamento | classifica a entrada e escolhe um tratamento fixo | fluxo |
| Paralelização | fatias independentes, ou várias tentativas da mesma tarefa | fluxo |
| Orquestrador-trabalhadores | um orquestrador corta na hora e junta | agente |
| Avaliador-otimizador | gera, critica, refina até passar | fluxo com laço |
| Autônomo | o modelo decide os passos, com guarda-corpos | agente |

A recomendação do texto, que o Maestro adota como princípio, é **começar pelo mais simples e
só acrescentar autonomia quando o simples comprovadamente falhar**, não quando parecer
limitado. Fluxo fixo é barato, previsível e depurável; autonomia é flexível e paga em variância.
O handbook acrescenta um corolário de arquitetura: quanto melhores as fronteiras, mais trabalho
cabe no lado barato do espectro, porque o corte deixa de precisar de inteligência quando já está
desenhado
([handbook, cap. 5 §5.2–5.3](https://github.com/GHDaru/maestro/blob/19823c2/docs/handbook/05-orquestracao.md)).

### A hipótese que este capítulo sustenta, e não prova

A agenda de pesquisa do livro registra a hipótese H4: **multiagente só ajuda com cortes
independentes**. O ciclo 074 é um caso a favor (o corte dependente custou retrabalho) e o
exemplo deste capítulo é uma ilustração, não uma prova. A H4 continua hipótese até o protocolo
do [capítulo 15](../15-validando-o-maestro/capitulo.md) compará-la em tarefas controladas.

## Alternativas

Há duas famílias de alternativas: os *frameworks* que **executam** a divisão e as técnicas que
ensinam a **cortar**. Elas respondem a perguntas diferentes, e misturá-las é o erro mais comum.

### Frameworks de orquestração

**LangGraph** modela o trabalho como um grafo de nós com estado compartilhado e arestas
explícitas, com persistência de estado entre passos e pontos de interrupção para um humano
aprovar. É uma boa casa para encadeamento e roteamento: o fluxo fica em código, versionado e
testável. O que ele não faz é decidir onde cortar; um grafo com três nós calculando o mesmo
número é um grafo válido. **Veredito**: adote como execução de fluxo fixo quando o seu fluxo
precisar viver fora do *harness*; não espere dele o critério de corte.

**CrewAI** organiza agentes por **papel** (pesquisador, redator, revisor) e executa as tarefas
num processo sequencial ou hierárquico, este com um agente gerente que delega e consolida. O
corte por papel é um corte por **quem**, não por **qual conceito**; e o processo hierárquico
põe o *reduce* num modelo, que é o que a seção anterior desaconselha. **Veredito**: o processo
sequencial é encadeamento e serve; o hierárquico só depois de o sequencial falhar com
evidência, e com o julgamento final num humano.

**MetaGPT** (Hong et al.) codifica procedimentos operacionais padrão (*standard operating
procedures*, SOPs) de uma empresa de software em papéis que trocam **artefatos estruturados**
(documento de requisitos, desenho, código), não conversa livre. É encadeamento com artefato
como interface, e confirma de fora a tese do Maestro de que a passagem entre agentes deve ser
um documento, não um chat. **Veredito**: observe a ideia do artefato tipado; o elenco fixo de
papéis é cerimônia para quem rege sozinho.

Dois relatos públicos de 2025 ajudam a calibrar. A Anthropic descreveu o seu sistema de
pesquisa multiagente, do tipo orquestrador-trabalhadores, e relatou que ele gasta muito mais
*tokens* do que uma conversa simples (cerca de 15 vezes) e que a maior parte das tarefas de
programação tem menos partes verdadeiramente paralelizáveis do que pesquisa [CLAIM-06-025]. A
Cognition, no texto *Don't Build Multi-Agents*, defendeu o oposto do paralelismo ingênuo:
subagentes que não compartilham o contexto inteiro tomam decisões implícitas conflitantes. Os
dois relatos convergem com o ciclo 074: paralelismo em código é caro e só compensa com fatias
que não precisam decidir a mesma coisa.

### Ferramentas de decomposição

**Spec Kit**, o motor que o Maestro vendorizou, gera a lista de tarefas e marca com `[P]` as
que podem correr em paralelo. O critério está escrito no comando: **arquivos diferentes e
nenhuma dependência de tarefa incompleta** [CLAIM-06-023]. É a primeira parte da regra deste
capítulo e só ela; o corte por tela do ciclo 074 passaria. O Spec Kit também não tem nada **a
montante** da spec: nenhum comando decompõe uma intenção grande em várias specs, o que a
pesquisa do ciclo 036 conferiu comando a comando [CLAIM-06-011]. **Veredito**: use; acrescente
o dono por conceito.

**Taskmaster** transforma um documento de requisitos em tarefas com grafo de dependências,
pontuação de complexidade e detecção de dependência circular. Resolve a ordenação de muitas
tarefas; cobra por isso um conjunto grande de ferramentas carregadas no contexto (o Maestro
estimou cerca de 21 mil *tokens* de sobrecarga) [CLAIM-06-016]. **Veredito**: observe, com o
gatilho que a seção seguinte descreve.

**Superpowers** executa cada tarefa num subagente fresco e numa *worktree* do Git isolada,
com revisão por tarefa. O isolamento resolve a primeira parte da regra (um escritor por
arquivo) de forma mecânica. **Veredito**: adote a worktree quando houver dois agentes escrevendo
no mesmo repositório ao mesmo tempo, não antes.

**Skills de decomposição** (a skill comunitária `decompose`, que quebra uma funcionalidade em
*issues* do tamanho de um agente; a coleção `Product-Manager-Skills`, que inclui três passadas
sobre uma spec: superfície, jornada e risco). A primeira corta **abaixo** da spec, onde a lista
de tarefas já opera, e amarra o resultado a uma plataforma de issues; a segunda corta **acima**,
entre specs, que é a lacuna real. **Veredito**: descarte a primeira; observe a segunda, com a
ressalva de licença (a coleção usa a licença Creative Commons BY-NC-SA, que proíbe o reempacotamento comercial:
a ideia atravessa, o texto não).

### Técnicas de corte

O conhecimento mais preciso sobre **como** cortar não está em ferramenta nenhuma; está na
literatura ágil. Os **padrões de fatiamento** de Richard Lawrence listam formas nomeadas de
cortar (por passo do fluxo, por operação, por variação de regra, por variação de dado, por
interface, adiando desempenho, isolando a investigação) e duas regras de desempate: prefira o
corte que permite jogar fora uma das fatias e o que produz fatias de tamanho parecido. O
**SPIDR** de Mike Cohn resume cinco linhas de corte (*Spike, Path, Interface, Data, Rules*). E
o **INVEST** (*Independent, Negotiable, Valuable, Estimable, Small, Testable*), com a ideia de
fatia vertical, proíbe cortar por camada técnica quando a fatia precisa entregar valor sozinha.

Aqui há uma tensão que o tech lead precisa resolver, e a resolução é de nível:

- **Entre ciclos** (o que se entrega ao usuário), valem a fatia vertical e o INVEST: cada
  entrega atravessa da interface ao dado e vale sozinha.
- **Dentro de um ciclo** (quem escreve o quê, ao mesmo tempo), vale o dono por conceito: o
  predicado tem um dono, a casca tem outro, e a tela consome os dois.

O ciclo 074 mostra as duas: a entrega ("um número só no menu e na entrada") era uma fatia
vertical; a divisão entre Workers foi por fronteira, com o domínio de um lado e a casca do
outro.

### Comparação

| Alternativa | Decide onde cortar? | Executa a divisão? | Veredito |
|---|---|---|---|
| LangGraph | não | sim (grafo com estado) | adotar para fluxo fixo fora do harness |
| CrewAI | por papel | sim (sequencial ou hierárquico) | sequencial sim; hierárquico só com evidência |
| MetaGPT | por fase, com artefato | sim | observar o artefato tipado |
| Spec Kit `[P]` | só por arquivo | não | usar, e acrescentar dono por conceito |
| Taskmaster | por dependência | sim | observar, com gatilho |
| Superpowers (worktree) | não; isola | sim | adotar quando houver escrita paralela |
| Lawrence, SPIDR, INVEST | sim, entre ciclos | não | absorver como conhecimento |

## O padrão Maestro

O Maestro resolve a divisão em três alturas: **dentro do ciclo** (a lista de tarefas e o fluxo
fixo), **entre sessões** (o time de Workers e o seu protocolo) e **acima do ciclo** (a
decomposição de uma intenção grande, que ele deliberadamente ainda não construiu). Em cada
altura, vale separar o que é regra escrita, o que é script e o que é *hook*.

### A regra: Princípio V e o anti-padrão 4

A constituição do método diz, no Princípio V, que a janela de contexto é finita e degrada ao
encher, que se deve **paralelizar por contexto delimitado** (porque bons cortes são o que torna
a orquestração segura) e usar **a menor autonomia que resolve o problema**, fluxo fixo antes de
agente autônomo
([princípios](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/principles.md)).
O catálogo de anti-padrões nomeia o erro simétrico, o número 4: **multiagente para um problema
de um agente**, porque orquestração cobra passagens e reconciliação
([anti-padrões](https://github.com/GHDaru/maestro/blob/19823c2/skills/anti-patterns/SKILL.md)).
O template de tarefas carrega a regra para onde ela é usada: ordenar por dependência, "cortar
por fronteira é o que torna o trabalho paralelo seguro", e escrever cada tarefa para quem tem
**zero contexto** do repositório
([tasks-template](https://github.com/GHDaru/maestro/blob/19823c2/.specify/templates/tasks-template.md)).

Isso é regra: texto que o agente lê. Nenhum script confere hoje se um conceito tem dois donos
num `tasks.md`; o exemplo deste capítulo mostra que a checagem é simples de escrever, e a
ausência dela no Maestro é a razão de o ciclo 074 ter precisado de dois Workers levantando a
mão.

### Dentro do ciclo: o encadeamento fixo é o padrão dominante

O ciclo 025 do Maestro reescreveu o capítulo de orquestração do handbook com uma exigência
nova: dizer **quais padrões foram usados**, e não só listá-los
([spec 025](https://github.com/GHDaru/maestro/blob/19823c2/specs/025-capitulo-05-padrao-v2/spec.md)).
O resultado, depois de 25 ciclos, foi que o padrão dominante era o mais barato do espectro. O
encadeamento fixo vivia em 11 comandos versionados na pasta de comandos do harness (`specify`,
`clarify`, `plan`, `tasks`, `implement` e os seus vizinhos, mais o comando de *Definition of
Done*, DoD); hoje são 12 [CLAIM-06-008]. Cada ciclo percorre a mesma sequência, e por isso
começar um ciclo custa pouco: ninguém decide **como** trabalhar, só **o que** fazer.

O avaliador-otimizador foi o padrão que mais rendeu, na forma de portão **provado falhando**
antes de ser aceito: quatro relatórios de qualidade (ciclos 017, 018, 020 e 021) documentam o
laço "escrever o check, tentar refutá-lo, só então confiar" [CLAIM-06-009]. E o dado negativo
informa tanto quanto o positivo: em 25 ciclos, **zero** uso do padrão autônomo, e quase nenhuma
paralelização de subagentes [CLAIM-06-010]. O trabalho coube num encadeamento com
verificação. É a regra da menor autonomia sendo obedecida, e o custo evitado é real.

O roteamento também está lá: são as raias (leve, plena, infra) que o
[capítulo 4](../04-a-spec-como-partitura/capitulo.md) descreve, cada uma um tratamento fixo
escolhido pela classificação da mudança.

A partir do ciclo 070, o encadeamento ganhou um registro mecânico. Uma **rodada** é uma
execução do fluxo gravada passo a passo num banco SQLite; cada **passo** é gravado na entrada,
no resumo e na saída, e **um passo sem saída bloqueia a entrada do seguinte**. A mensagem entre
sessões da mesma máquina vai por uma fila no mesmo banco (a *outbox*, em modo de registro
antecipado, o *write-ahead log*, WAL), sem servidor de mensageria
([glossário](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/glossary.md)). Aqui
há hook: `workflow_session_start.py` e `workflow_stop.py` gravam a entrada e cobram o resumo e a
evidência ao fim do turno
([hooks](https://github.com/GHDaru/maestro/tree/19823c2/painel/hooks)). O hook de fim cobra; não
impede. O próprio código diz que o objetivo é cobrar, não bloquear a sessão.

Um último comando merece menção porque mostra uma divisão que o Maestro **não** quer. O
`/speckit.taskstoissues`, herdado do Spec Kit, converte a lista de tarefas em *issues* do
GitHub ordenadas por dependência, e só prossegue se o repositório remoto for do GitHub
([comando](https://github.com/GHDaru/maestro/blob/19823c2/.claude/commands/speckit.taskstoissues.md)).
Ele está instalado porque veio com o motor. A ideia equivalente vinda de fora, a skill
`decompose`, foi **descartada** na pesquisa do ciclo 036 por dois motivos: a lista de tarefas
já faz esse corte, e amarrar a rastreabilidade a issues de uma plataforma é acoplamento que o
método recusa
([cartão 037](https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/ideias/037-decompose-feature-em-issues.md)).

### Entre sessões: o time, a worktree e o endereço

O paralelismo real chegou ao Maestro por fora. Entre 29/09 e 01/10/2026, o projeto Hindiana,
que usava o método, rodou 16 sessões simultâneas, com cerca de 160 worktrees, e registrou 52
desvios de método em três dias e 28 decisões numa única noite [CLAIM-06-019]. Dessa escala
nasceu uma **linha paralela** de desenvolvimento do próprio Maestro, num clone separado, com 42
branches publicadas em 19/10 [CLAIM-06-017].

Integrar essa linha virou um ciclo próprio, o 066, que o plano descreve como **guarda-chuva**:
uma pasta de coordenação que não entrega código além do lançador de sessões, e cujos filhos
entregam o resto
([plano 066](https://github.com/GHDaru/maestro/blob/19823c2/specs/066-painel-de-regencia/plan.md)).
O corte foi por fronteira histórica: **um ciclo filho por linhagem de commits**, cada um com a
própria cauda de verificação, integrado por *merge* `--no-ff` para preservar a história (sem
*rebase*, que reescreveria hashes de que outro projeto dependia; sem *squash*, que apagaria os
pares vermelho-verde dos testes). O mapa aprovado previa seis ciclos de integração, do 066 ao
071; em `19823c2` há pastas do 066 ao 070, e nenhuma do 071 [CLAIM-06-017]. O
mapa de integração registra a única colisão real de código: duas linhagens irmãs, separadas num
commit comum, que tocavam os mesmos três arquivos do painel; o conflito foi arbitrado pelos
testes da linhagem que os tinha [CLAIM-06-021].

O **lançador multissessão** (`scripts/multi-session.py`) é o script que torna o time
repetível: abre uma sessão Gerente e seis Workers, cada um com o seu modelo, e cria **uma
worktree por Worker**, de modo que as edições de um não aparecem na cópia do outro
[CLAIM-06-018]. A decisão que o autorizou, tomada por consenso de três pareceres em contexto
fresco, fixou também que **só o Gerente faz push, e só depois do portão humano**
([decisões](https://github.com/GHDaru/maestro/blob/19823c2/docs/records/decisoes.jsonl), linha
`decisao-066-sessoes-via-gateway`). Repare na forma: o isolamento por worktree resolve a
primeira parte da regra (um escritor por arquivo) mecanicamente; o Gerente como único ponto de
integração resolve o *reduce*; a segunda e a terceira partes (dono por conceito, contrato antes
do consumo) continuam dependendo do plano. O ciclo 074 rodou exatamente sobre esse arranjo, e
foi por isso que a colisão foi de conceito, não de arquivo.

**A colisão que não é de código: a numeração.** Duas linhas que trabalham em paralelo sem um
alocador comum colidem também nos **nomes**. A linha principal já tinha os ciclos 064 e 065
quando a linha paralela trouxe os seus próprios 064, 065, 066, 067 e 070. O registro de
decisões guarda a renumeração de um deles: o ciclo do "livro de ponto", aberto como 064, virou
065 porque 064 já existia [CLAIM-06-020]. O mapa de integração renumerou os demais em ordem
aprovada pelo humano (o antigo 064 virou 070, o 065 virou 071, o 070 virou 069) [CLAIM-06-022].
E o retrato de hoje ainda mostra as marcas: em `specs/` há duas pastas com o prefixo 066, duas
com o prefixo 070 e uma pasta com número pendente, `NNN-painel-de-coordenacao-v0`, cuja spec
diz "número do ciclo pendente da decisão" [CLAIM-06-020]. Até a branch de origem tinha um nome,
`067-painel-chamados`, sem pasta de spec correspondente [CLAIM-06-021].

Renumerar resolve a colisão e quebra referências. Todo texto que dizia "ciclo 064" antes da
renumeração passou a apontar para outra coisa. O Maestro tirou disso uma invariante, registrada
no glossário como **colisão de endereço**: o mesmo identificador apontando para duas sessões, ou
para nenhuma, e a regra de que **endereço ambíguo é recusado, nunca resolvido**, porque uma
entrega ao par errado não se desfaz
([glossário](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/glossary.md)). O
nome nu `Worker04` do ciclo 074 foi uma violação dessa invariante.

O ciclo 075 levou a invariante ao canal de mensagens. A spec mediu quatro defeitos do canal
entre sessões; o primeiro era que **a mensagem se perde ao reiniciar**, porque o endereço era o
identificador da sessão no harness, e ele muda quando a sessão reinicia [CLAIM-06-015]. O
protocolo novo separa as duas coisas: a **identidade** é `nome · projeto`, estável; o *ref* é só
**localizador**, resolvido na entrega; e o identificador de contexto do protocolo *Agent2Agent*
(A2A) existe só na borda, no mapa de conversão, nunca no envelope interno
([spec 075](https://github.com/GHDaru/maestro/blob/19823c2/specs/075-protocolo-entre-sessoes/spec.md)).
Para o tech lead, a lição é geral: dividir o trabalho entre agentes cria endereços (de tarefa,
de sessão, de ciclo), e endereço é parte do corte. Se dois agentes podem ser chamados pelo
mesmo nome, o corte não terminou.

### Acima do ciclo: a lacuna medida e o gatilho

A divisão que o Maestro não faz é a de cima: ir de uma intenção grande até o conjunto de
ciclos. O ciclo 036 pesquisou isso a pedido do mantenedor e começou por medir o próprio
repositório: das 34 specs de então, 20 tinham nascido de um pedido pontual, não de um corte
planejado; nenhum agente, skill ou template cobria decomposição [CLAIM-06-011]
([pesquisa do upstream](https://github.com/GHDaru/maestro/blob/19823c2/docs/research/upstream-decomposicao.md)).
Funcionava porque o dono do escopo estava na sala, e a pesquisa diz com todas as letras que é
isso que não escala para um produto com terceiros.

A proposta coube, por exigência da própria spec, em **um objeto, um verbo e um portão**
([spec 036](https://github.com/GHDaru/maestro/blob/19823c2/specs/036-pesquisa-upstream-decomposicao/spec.md)):

- o objeto `outcome`, um resultado observável com métrica e dono, no lugar de "épico";
- o verbo, uma skill `slice-outcome` com as três passadas e os padrões de fatiamento, e uma lei
  de ferro: nenhuma fatia sem critério de aceite próprio e contrato declarado;
- o portão, um `check-outcomes.sh` que confere se toda spec cita o resultado que serve e se toda
  fatia tem contrato, sem julgar se o corte está certo (isso fica com o humano).

E a recomendação foi **não construir**: registrar um gatilho e esperar a primeira intenção
grande real. O roteiro do Maestro guarda o item com esse gatilho: "primeira intenção grande
**real** que não caiba em um ciclo, ou primeiro projeto com usuários externos"
([roadmap](https://github.com/GHDaru/maestro/blob/19823c2/docs/roadmap.md)).

As ideias de fora seguiram o mesmo destino. A pesquisa registrou como **absorver**, em
06/08/2026, a decomposição em três passadas, os padrões de fatiamento, a fatia vertical como lei
e o contrato por fatia. Quatro dias depois, o ciclo 047 (o catálogo do ecossistema) as
reclassificou para **observar**, com nota explícita: tinham sido registradas como absorvidas com
destino numa skill que nunca foi escrita [CLAIM-06-012]. O cartão do contrato por fatia ganhou
um gatilho diferente dos outros, e o mais relevante para este capítulo: "dois ou mais agentes
trabalhando em fatias da mesma intenção ao mesmo tempo"
([cartão 035](https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/ideias/035-contrato-por-fatia.md)).

### Gatilhos que disparam, e catálogos que não ficam sabendo

Os gatilhos são a parte mais inteligente desse desenho e também a mais frágil. Três casos, em
`19823c2`:

- **Worktree por tarefa** (cartão 003, vindo do Superpowers): em 10/08/2026, estado
  **observar**, porque "nunca rodamos dois agentes escrevendo em paralelo", com o gatilho "dois
  ou mais agentes escrevendo no mesmo repositório ao mesmo tempo, com conflito observado" (o
  estudo de campo do Superpowers, no apêndice B do handbook, já tinha mantido a ideia em
  observação, com o gatilho de dor de paralelismo inalterado). Em
  outubro, o lançador do ciclo 066 passou a criar uma worktree por Worker. A última linha do
  índice de estado do catálogo, porém, ainda diz **observar**, com a data de agosto
  [CLAIM-06-013]. O gatilho disparou; o catálogo não registrou.
- **Grafo de dependências** (cartão 011, do Taskmaster): gatilho "um ciclo com mais de 20
  tarefas paralelas, ou vários projetos simultâneos, e a ordenação manual doer (registrado em
  retro)". Hoje, 8 das 74 listas de tarefas passam de 20 caixas, e a do ciclo 074 tem 85
  [CLAIM-06-014]. Quantas eram paralelas e se a ordenação doeu, ninguém mediu; o gatilho tem
  três condições e só a contagem é automática.
- **Contrato por fatia** (cartão 035): o gatilho "dois ou mais agentes em fatias da mesma
  intenção ao mesmo tempo" descreve o ciclo 074 palavra por palavra. O campo de contrato que a
  pesquisa propôs teria nomeado o dono de `quemPrecisaDeVoce` antes de três Workers o
  calcularem.

Nada disso é escândalo; é o [teorema T5](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/axioms.md)
aplicado ao próprio catálogo: um artefato sobrevive por consumo ou por imutabilidade, e um
gatilho escrito só é consumido se alguma coisa o lê quando o mundo muda. O cartão é imutável
(certo); o índice de estado depende de alguém lembrar de acrescentar a linha nova (frágil). O
[capítulo 14](../14-a-organizacao-que-aprende/capitulo.md) trata de como uma correção vira
regra; aqui basta a consequência prática: **gatilho sem leitor é decisão adiada sem data**.

### Resumo do que é regra, script e hook

| Mecanismo | Tipo | O que garante |
|---|---|---|
| Princípio V; anti-padrão 4; template de tarefas | regra | corte por fronteira, menor autonomia, tarefa para contexto zero |
| Comandos do fluxo (`specify` … `implement`, DoD) | comando versionado | encadeamento fixo, igual em todo ciclo |
| `scripts/multi-session.py` | script | uma worktree por Worker; um modelo por sessão |
| Gerente como único integrador, push só após portão | regra (decisão registrada) | um ponto de *reduce* |
| `workflow_session_start.py`, `workflow_stop.py` | hook | passo registrado; resumo e evidência cobrados |
| Colisão de endereço; identidade `nome · projeto` | regra (glossário) e protocolo (075) | endereço ambíguo recusado |
| `outcome`, `slice-outcome`, `check-outcomes.sh` | proposta com gatilho | nada ainda: deliberadamente não construído |

## Exemplo executável

O exemplo em [`exemplo/`](exemplo/README.md) refaz, em miniatura, o ciclo 074: o mesmo trabalho
(um número só para "quem precisa de mim", em domínio, casca, entrada e sonda) cortado de três
jeitos. Python 3, só biblioteca padrão. Para rodar:

```bash
cd livro/06-como-dividir-o-trabalho/exemplo
bash rodar.sh | diff - saida-esperada.txt   # nenhuma linha de diferença
```

São oito passos [CLAIM-06-026]:

1. **Corte por tela.** `dividir.py colisao` acusa o conceito `contagem-precisa-de-mim` com três
   donos. Os arquivos são todos diferentes: a regra `[P]` do Spec Kit aprovaria.
2. **Corte por quantidade.** Duas mudanças para cada agente, na ordem da lista: dois agentes
   escrevem `casca.js`, e um terceiro consome um contrato que ninguém escreve.
3. **Corte por fronteira.** Cada arquivo e cada conceito com um dono só.
4. **A ordem sai dos contratos.** `ondas` põe o dono do predicado, a casca e a sonda na
   primeira onda e o consumidor na segunda, como o Gerente fez com os Workers 01, 02 e 05.
5. **Quanto custa o corte errado.** `custo` soma o caminho crítico das ondas, as passagens e o
   retrabalho das colisões. Os cortes por tela e por quantidade ficam **mais caros** que um
   agente só.
6. **Quando o corte certo paga.** O corte por fronteira cai de 14 para 9 unidades com a
   passagem custando 1; com a passagem custando 4, deixa de pagar. O mesmo corte, outro
   veredito: o custo da coordenação decide.
7. **A menor autonomia que resolve.** `autonomia` classifica seis situações. O ciclo inteiro é
   encadeamento com avaliador; a triagem é roteamento; "metade dos arquivos para cada agente"
   volta para encadeamento até haver fronteira; integrar 42 branches de outra linha é
   orquestrador-trabalhadores com *reduce* humano; o agente que "descobre sozinho o que
   refatorar" é recusado por falta de evidência.
8. **Numerar em paralelo.** `numerar` reproduz as colisões de 064 e 065 entre duas linhas,
   recusa resolver "ciclo 064" (dois destinos) e mostra que a renumeração, ao consertar a
   colisão, muda o destino de uma referência que antes estava certa.

O README traz a saída completa, três exercícios e um script opcional, `medir_maestro.py`, que
reproduz num clone do Maestro os números deste capítulo.

## Contraexemplo

A regra deste capítulo tem custo, e há situações em que ela atrapalha.

**Quando o trabalho cabe num agente.** Toda a discussão de corte pressupõe que vale dividir. Na
maior parte do tempo, não vale. O dado mais forte do Maestro é negativo: 25 ciclos sem padrão
autônomo e quase sem paralelismo de subagentes [CLAIM-06-010]. Um tech lead que importa a
regra "dono por conceito, contrato antes do consumo" para um trabalho que um agente faz sozinho
em uma tarde acrescenta cerimônia sem comprar nada. O passo 6 do exemplo mostra o limite: com
passagem cara, até o corte certo perde para um agente só.

**Quando a fronteira ainda não existe.** Cortar por contexto delimitado exige que o contexto
esteja delimitado. Num protótipo, numa investigação, num domínio que ninguém modelou, a
fronteira é o que se está descobrindo. Paralelizar ali é escolher uma fronteira por chute e
pagar o retrabalho quando ela se mostrar errada. O caminho é sequencial até o modelo de domínio
aparecer; o [capítulo 8](../08-ddd-para-agentes/capitulo.md) trata de como desenhá-lo.

**Quando o dono vira gargalo.** Dar um dono a cada conceito serializa os consumidores atrás
dele. No ciclo 074, o Worker05 esperou o Worker01 [CLAIM-06-003]. Se o conceito é central e o
dono demora, o paralelo vira fila. A porta inerte do Worker02 é a técnica que alivia isso:
publique cedo um contrato que não muda o comportamento, e deixe os consumidores trabalharem
contra ele. Mas ela só funciona quando o contrato é estável; contrato que muda depois de
publicado é o pior dos mundos.

**Quando o gatilho vira desculpa.** Esperar dor real antes de construir é bom conselho (o
Maestro recusou a skill de decomposição por isso). Mas o caso da worktree mostra o outro lado: o
gatilho disparou e o registro não acompanhou [CLAIM-06-013]. Um time que usa "observar com
gatilho" e não tem ninguém lendo os gatilhos está, na prática, dizendo "não" sem data.

**Quando o corte por camada é o certo.** A fatia vertical é a regra entre entregas, mas dentro
de um ciclo o corte do ciclo 074 foi, sim, por camada: domínio, casca, tela. Quem lê INVEST
como proibição absoluta de cortar por camada vai rejeitar exatamente o corte que resolveu o
problema. A distinção de nível (entre ciclos × dentro do ciclo) não é detalhe; sem ela as duas
regras se contradizem.

**O custo da regra, resumido.** Escrever o contrato antes custa tempo antes de qualquer código
aparecer. Ordenar por ondas custa paralelismo. Recusar endereço ambíguo custa conveniência
("é óbvio que Worker04 é aquele"). O ganho só aparece quando há colisão, e colisão não avisa
antes.

## Evidência

O que sustenta este capítulo, com o estado de cada afirmação. O registro completo, com o
caminho ou comando que reproduz cada número, está em [claims.md](claims.md).

**Medido** (reproduzível por comando no Maestro em `19823c2`, ou pelo exemplo):

- Os commits da costura do ciclo 074, com datas, autores das pontas e cherry-picks na linha
  [CLAIM-06-002].
- Os comandos versionados no ciclo 025 e hoje [CLAIM-06-008]; os quatro relatórios com portão
  provado falhando [CLAIM-06-009].
- As pastas de `specs/` com prefixo repetido e a pasta sem número; a decisão de renumeração do
  065 [CLAIM-06-020].
- O estado corrente das ideias de divisão no catálogo e a worktree por Worker no lançador
  [CLAIM-06-012, CLAIM-06-013]; o tamanho das listas de tarefas [CLAIM-06-014].
- A conta de canais de Brooks para sete sessões [CLAIM-06-024].
- A saída do exemplo executável [CLAIM-06-026].

**Observado** (o Maestro registra; o livro leu o registro, não refez o experimento):

- O chip em 1 contra a união em 4, a decisão da regente e o despacho em ondas
  [CLAIM-06-001, CLAIM-06-003]; a delegação dos portões à regente [CLAIM-06-027]; o endereço pelo nome nu [CLAIM-06-004]; as duas pendências como
  a mesma decisão [CLAIM-06-005]; o corte do ciclo em seis podas [CLAIM-06-006].
- O uso dos padrões em 25 ciclos [CLAIM-06-010]; a lacuna a montante medida no ciclo 036
  [CLAIM-06-011]; o custo estimado do Taskmaster [CLAIM-06-016].
- A escala do Hindiana, a linha paralela e a integração em seis ciclos [CLAIM-06-017,
  CLAIM-06-019]; o lançador e a decisão de só o Gerente fazer push [CLAIM-06-018]; o conflito
  das linhagens irmãs e a branch sem spec [CLAIM-06-021]; o mapa de renumeração [CLAIM-06-022].
- O defeito de endereço do canal entre sessões [CLAIM-06-015].
- O critério `[P]` do Spec Kit [CLAIM-06-023]; os seis padrões da Anthropic [CLAIM-06-007].
- O relato público de custo de *tokens* de um sistema multiagente [CLAIM-06-025]: número da
  fonte, não reproduzido.

**Hipótese** (não medido):

- **H4**, multiagente só ajuda com cortes independentes: o capítulo traz um caso a favor e um
  modelo de brinquedo, não um experimento.
- O overhead de coordenação no Maestro real: definido aqui, nunca medido lá.
- Que uma checagem automática de "conceito com mais de um dono" no plano de tarefas teria
  evitado o retrabalho do ciclo 074: plausível pelo exemplo, não testado no método.

## Checklist

Para aplicar no seu time, antes de distribuir trabalho entre agentes:

- [ ] O trabalho **precisa** ser dividido? Estime o tempo de um agente só e compare com o
      caminho crítico mais a coordenação; se não houver ganho claro, não divida.
- [ ] Cada arquivo tem **um** escritor por vez (worktree por agente, ou lista de arquivos por
      tarefa sem interseção).
- [ ] Cada **conceito** que aparece em mais de uma fatia tem **um** dono nomeado no plano, e as
      outras fatias o consomem em vez de recalcular.
- [ ] Cada contrato consumido tem dono no plano ou já existe no repositório; nenhum "a gente
      combina na hora".
- [ ] A ordem de execução saiu dos contratos (dono antes de consumidor), e uma dependência
      circular é motivo para recortar, não para "rodar junto".
- [ ] Quando o dono atrasar os consumidores, há uma porta inerte publicada cedo, com
      comportamento inalterado até ser chamada.
- [ ] O *reduce* tem um dono com o contexto global (o humano, ou quem age sob política escrita
      dele), e nenhum agente "consolidador" ao lado das fatias decide o que elas discordam.
- [ ] Cada fluxo começa no padrão mais simples (encadeamento); subir para orquestrador ou
      autônomo exige evidência escrita de que o simples falhou.
- [ ] Todo identificador que um agente usa para endereçar outro (tarefa, sessão, ciclo) é único
      e estável; endereço ambíguo é recusado, não adivinhado.
- [ ] Numeração de ciclos ou tarefas vem de **um** alocador, mesmo com linhas paralelas.
- [ ] Toda prática de paralelismo adiada tem gatilho observável **e** um leitor: um script ou
      uma cerimônia que confere o gatilho e registra quando ele dispara.

## Referências

Fontes do Maestro, todas na versão `19823c2`:

- Axiomas, teoremas e corolários (A3, T5):
  <https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/axioms.md>
- Constituição, Princípio V:
  <https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/principles.md>
- Glossário (rodada, passo, outbox, colisão de endereço):
  <https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/glossary.md>
- Catálogo de anti-padrões (anti-padrão 4):
  <https://github.com/GHDaru/maestro/blob/19823c2/skills/anti-patterns/SKILL.md>
- Template de tarefas:
  <https://github.com/GHDaru/maestro/blob/19823c2/.specify/templates/tasks-template.md>
- Comandos `speckit.tasks` e `speckit.taskstoissues`:
  <https://github.com/GHDaru/maestro/tree/19823c2/.claude/commands>
- Handbook, capítulo 5 (orquestração):
  <https://github.com/GHDaru/maestro/blob/19823c2/docs/handbook/05-orquestracao.md>
- Spec 025 (capítulo de orquestração no padrão v2):
  <https://github.com/GHDaru/maestro/blob/19823c2/specs/025-capitulo-05-padrao-v2/spec.md>
- Spec 036 e a pesquisa do upstream:
  <https://github.com/GHDaru/maestro/blob/19823c2/specs/036-pesquisa-upstream-decomposicao/spec.md> ·
  <https://github.com/GHDaru/maestro/blob/19823c2/docs/research/upstream-decomposicao.md>
- Cartões do ecossistema 003, 011, 022, 033, 034, 035 e 037, e o índice de estado:
  <https://github.com/GHDaru/maestro/tree/19823c2/docs/ecosystem/ideias> ·
  <https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/estado.jsonl>
- Roadmap (item "Upstream" e o seu gatilho):
  <https://github.com/GHDaru/maestro/blob/19823c2/docs/roadmap.md>
- Plano do ciclo 066 e o mapa de integração da linha paralela:
  <https://github.com/GHDaru/maestro/blob/19823c2/specs/066-painel-de-regencia/plan.md> ·
  <https://github.com/GHDaru/maestro/blob/19823c2/specs/066-painel-de-regencia/plano-integracao-linha-paralela.md>
- Spec com número pendente do painel de coordenação v0:
  <https://github.com/GHDaru/maestro/blob/19823c2/specs/NNN-painel-de-coordenacao-v0/spec.md>
- Lançador multissessão:
  <https://github.com/GHDaru/maestro/blob/19823c2/scripts/multi-session.py>
- Hooks do fluxo (ciclo 070):
  <https://github.com/GHDaru/maestro/tree/19823c2/painel/hooks>
- Ciclo 074, lista de tarefas (bloco `costura-um-numero`) e o fechamento do gauntlet:
  <https://github.com/GHDaru/maestro/blob/19823c2/specs/074-prototipo-navegavel/tasks.md> ·
  <https://github.com/GHDaru/maestro/blob/19823c2/specs/074-prototipo-navegavel/done-074-gauntlet-fechado.md>
- Spec 075 (protocolo entre sessões):
  <https://github.com/GHDaru/maestro/blob/19823c2/specs/075-protocolo-entre-sessoes/spec.md>
- ADR 0026 (portão humano por delegação de política):
  <https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0026-gate-humano-por-delegacao-de-politica.md>
- Índice de decisões (`ciclo-065-renumerado`, `ciclo-066-integra-painel-controle`,
  `decisao-066-sessoes-via-gateway`, `decisao-072-gates-delegados`):
  <https://github.com/GHDaru/maestro/blob/19823c2/docs/records/decisoes.jsonl>

Literatura e fontes externas (citadas de memória bibliográfica ou a partir do registro do
Maestro em `19823c2`; os endereços web não foram reacessados para esta edição):

- Parnas, D. L. *On the criteria to be used in decomposing systems into modules*.
  Communications of the ACM, 15(12), 1972.
- Conway, M. E. *How do committees invent?* Datamation, abr. 1968.
- Brooks, F. P. *The Mythical Man-Month*. Addison-Wesley, 1975.
- Amdahl, G. M. *Validity of the single processor approach to achieving large scale computing
  capabilities*. AFIPS Spring Joint Computer Conference, 1967.
- Evans, E. *Domain-Driven Design*. Addison-Wesley, 2003.
- Anthropic. *Building effective agents*, dez. 2024.
  <https://www.anthropic.com/engineering/building-effective-agents>
- Anthropic. *How we built our multi-agent research system*, jun. 2025.
  <https://www.anthropic.com/engineering/multi-agent-research-system>
- Cognition. *Don't Build Multi-Agents*, jun. 2025. <https://cognition.ai/blog/dont-build-multi-agents>
- Hong, S. et al. *MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework*.
  arXiv:2308.00352, 2023.
- LangGraph, documentação. <https://langchain-ai.github.io/langgraph/>
- CrewAI, documentação (processos sequencial e hierárquico). <https://docs.crewai.com/>
- GitHub Spec Kit. <https://github.com/github/spec-kit>
- Taskmaster. <https://github.com/eyaltoledano/claude-task-master>
- Superpowers. <https://github.com/obra/superpowers>
- Product-Manager-Skills. <https://github.com/deanpeters/Product-Manager-Skills>
- Lawrence, R. *The Humanizing Work Guide to Splitting User Stories*.
  <https://www.humanizingwork.com/the-humanizing-work-guide-to-splitting-user-stories/>
- SPIDR (Mike Cohn), resumo. <https://blogs.itemis.com/en/spidr-five-simple-techniques-for-a-perfectly-split-user-story>
