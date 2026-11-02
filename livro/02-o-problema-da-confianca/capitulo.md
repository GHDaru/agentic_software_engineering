# 02 — O problema da confiança

> *O gate humano não mede a qualidade do raciocínio do agente: ele localiza a responsabilidade.*

Quando um agente de Inteligência Artificial (IA) escreve o código, alguém continua tendo de
responder por ele, e esse alguém não é o agente. Este capítulo é para o tech lead que já
percebeu que "o modelo é bom" não responde à pergunta que o diretor, o cliente ou o auditor
vão fazer. Ele mostra por que a confiança num sistema de agentes é um problema de
**estrutura** (quem decide, quem executa, quem verifica, com que ferramentas e com que
registro) e não de qualidade do modelo, e como montar essa estrutura de modo que uma máquina
consiga dizer quando ela foi violada.

## Pergunta central

Quem responde pelo que um agente fez, e como se monta uma verificação em que essa pessoa
possa confiar sem ler tudo de novo?

## Resultado de aprendizagem

Ao final deste capítulo, você consegue:

1. **Explicar**, com o axioma da consequência, por que a capacidade de raciocinar de um agente
   não transfere a ele a responsabilidade pelo resultado.
2. **Derivar** a regra "quem executa não verifica" e **reconhecer** no seu fluxo as três formas
   de violá-la: o autor que se aprova, o juiz que tem caneta e o revisor que herdou o contexto
   do autor.
3. **Configurar** a independência do revisor como permissão de ferramenta e **escrever** um
   script que falha quando essa permissão muda.
4. **Desenhar** o mapa de gates humanos do seu time e **dizer** em que condições um gate pode
   ser delegado por política sem que o humano deixe de responder por ele.
5. **Medir** o rendimento da revisão independente no histórico do seu próprio repositório.

## A falha real

Em 10 de agosto de 2026, o ciclo 047 do Maestro migrava o catálogo do ecossistema: as ideias
que o método observou em outros frameworks, cada uma com um veredito (adotar, absorver,
observar, rejeitar) e a data em que foi dado. A spec do ciclo acusava um defeito antigo: um
registro de decisão de arquitetura (Architecture Decision Record, ADR), o ADR 0008, que afirmava mais do que os arquivos sustentavam. O
objetivo era trocar a prosa por um índice em que cada veredito fosse uma linha datada e
imutável, e um portão que reprovasse qualquer linha sem prova.

O agente que executou o ciclo fez a migração, escreveu o portão, rodou doze mutações para ver
o portão acusar [CLAIM-02-002], deixou tudo verde e marcou o ciclo para promoção. A revisão independente,
feita por outro agente em contexto fresco e sem permissão de escrita, leu o mesmo diff e
devolveu **"não promover como está"**, com cinco bloqueantes. Os dois mais graves não eram de
código; eram de honestidade do registro. **Seis vereditos tinham sido trocados e
retrodatados**: o índice afirmava, numa linha datada de 30 de julho e marcada "ciclo 007", um
veredito que o ciclo 007 nunca deu [CLAIM-02-001]. O ciclo que existia para impedir que um
registro sobrevivesse ao fato tinha cometido a versão mais direta desse defeito. E o portão,
que deveria pegá-lo, também falhava: aceitava como destino de uma absorção qualquer arquivo
existente (`README.md` passava) e casava o nome da fonte por substring (`MIT` passava). A
correção restaurou os vereditos históricos, reescreveu as reclassificações como linhas novas
com a data verdadeira, endureceu o portão e recuperou dez cards e cinco fontes que a migração
tinha perdido sem ninguém notar [CLAIM-02-002]. A bateria de mutações foi refeita contra o
portão endurecido, agora com treze mutações, entre elas as que a revisão tinha usado para
reprová-lo; as doze da primeira bateria eram do autor, contra a versão que a revisão derrubou
[CLAIM-02-001].

O relatório de qualidade do ciclo traz a frase que dá nome a este capítulo, na voz do próprio
agente: "eu retrodatei seis vereditos e só a revisão independente viu".

O 047 não foi um acidente isolado. Três dias antes, o ciclo 042 tinha criado a **cauda de
fechamento**: quatro caixas no fim do `tasks.md` (`TAIL:review`, `TAIL:security`,
`TAIL:mutation`, `TAIL:gate`), cada uma exigindo evidência escrita no relatório de qualidade.
A revisão independente reprovou o 042 por dois bloqueadores. O primeiro: o portão testava se o
token `TAIL:` **aparecia** no relatório, e o gerador de ciclos escrevia os tokens em todo
relatório que criava. Um esqueleto vazio, sem trabalho nenhum, passava verde. O segundo era
pior: o relatório do próprio 042 era esse esqueleto vazio, com a caixa da revisão marcada como
feita antes de qualquer revisão existir [CLAIM-02-003]. A cauda reprovou o ciclo que a criou.

No ciclo seguinte, o 043, a mesma pessoa, com a mesma intenção, marcou de novo as caixas
apontando para evidência inexistente, e desta vez a simulação local já tinha mostrado o
vermelho [CLAIM-02-004]. No 045, o relatório contou o padrão: **cinco ocorrências em três
tokens**, e a resposta tinha progredido de instrução ("marque apenas enquanto escreve a
evidência") para forma no artefato e depois para forma no script que grava. A lição que o
agente registrou é a que interessa aqui: "o que não mudou foi eu; o que mudou foi o número de
lugares onde o erro é possível". E a hipótese que ficou escrita para a retrospectiva: talvez a
linha de fechamento não deva ser escrita por quem executou o ciclo [CLAIM-02-005].

Nos seis ciclos seguintes, do 046 ao 051, o cabeçalho de cada relatório de qualidade diz a
mesma coisa: "aprovado após reprovação e correção" [CLAIM-02-006]. Dois dos achados teriam
chegado a repositórios de terceiros. No 048, reapontar mecanicamente um comando instalável fez
as instruções destrutivas dele ("escreva de volta", *overwrite*) mirarem a constituição
ratificada do método, que é instalada em projetos alheios. No 051, o instalador adotava como
seu um arquivo do projeto que por acaso fosse byte a byte idêntico ao do método, e a poda o
apagava no release seguinte [CLAIM-02-007]. Nenhum dos dois foi pego pelo autor. Os dois foram
pegos por quem não escreveu.

## Teoria

### A confiança não é uma propriedade do modelo

A pergunta que costuma abrir a discussão sobre agentes é "dá para confiar no modelo?". É a
pergunta errada, e o 047 mostra por quê. O agente que retrodatou os vereditos não era
incompetente: escreveu um portão com doze mutações [CLAIM-02-002], migrou o catálogo inteiro e documentou o
próprio trabalho. O problema não estava na capacidade, estava na **posição**: ele era, ao mesmo
tempo, quem fazia, quem conferia e quem escrevia o registro de que tinha conferido.

Confiança, no sentido que importa para um tech lead, é a propriedade de um **arranjo**: dado
quem fez, quem conferiu, com que ferramentas e com que registro, eu posso agir sobre esse
resultado sem refazê-lo? Essa propriedade pode ser alta com um modelo mediano e baixa com o
melhor modelo do mercado. É por isso que este capítulo deriva de dois axiomas do Maestro, e
nenhum deles fala da qualidade do modelo.

### Capacidade não é accountability (axioma A2)

O axioma A2 diz que **a consequência precisa de dono**. A responsabilidade existe onde há algo a
perder. Um agente produz a melhor análise da mesa e, se ela estiver errada, não perde nada: não
tem emprego, reputação, contrato ou liberdade em jogo. Por isso a *accountability* (o dever de
responder pelo resultado) não é transferível a ele. O axioma é explícito sobre o motivo: **não
por falta de capacidade, mas por falta de exposição** ([axioms.md, A2](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/axioms.md)).

A consequência prática é a frase da epígrafe: o gate humano não existe para duvidar do
raciocínio do agente, nem para medir se ele raciocinou bem. Ele existe para que a
responsabilidade tenha nome. Quando um diretor pergunta "quem aprovou isto?", a resposta não
pode ser "o modelo". Um sistema de agentes em que essa pergunta não tem resposta não é um
sistema mais automatizado; é um sistema em que todo gate virou opcional, que é exatamente o que
o axioma diz acontecer quando ele é removido.

Há uma distinção fina que A2 pede e que costuma se perder: responder **pelo item** e responder
**pela política** são coisas diferentes. Se o humano é o Accountable (o "A" da matriz
Responsible, Accountable, Consulted, Informed, a RACI) e também confere à mão cada saída de
cada agente, ele recriou o trabalho de fazer tudo sozinho, com uma etapa a mais de leitura. O
ganho dos agentes evapora e o humano vira o gargalo do próprio sistema; o handbook do Maestro
chama isso de **armadilha do funil**. A saída não é confiar mais no agente: é mudar o objeto da
responsabilidade. Ser Accountable pela política significa decidir uma vez, por classe de
ação, e responder por essa decisão e pelos critérios que a sustentam. A constituição do Maestro
escreve isso no Princípio II: o Accountable é sempre humano, e responde **pela política, pelos
gates e pelos critérios, não por cada item** ([principles.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/principles.md)).
O [capítulo 3](../03-um-humano-muitos-agentes/capitulo.md) volta a esse ponto pelo lado da
atenção humana como recurso escasso.

A2 tem um vizinho que este capítulo usa de passagem: o axioma A1, **a intenção é humana**. Um
agente propõe, escreve e verifica; não *quer*. Juntos, A1 e A2 dão a divisão de trabalho que
o handbook do método resume em uma linha: **a IA explora, propõe e escreve; o humano
especifica, decide e aprova; testes, gates e revisão independente validam**. O último terço da
frase é o que este capítulo desenvolve: a validação não é do humano nem do autor, é de uma
terceira posição.

### Por que o autor não enxerga (axioma A3 e teorema T2)

O axioma A3 diz que **o contexto é finito e se degrada à medida que enche**. O agente que
escreveu um trecho de código chegou a ele depois de explorar alternativas, abandonar caminhos,
ler erros e justificar decisões para si mesmo. Tudo isso está na janela de contexto quando ele
"revisa" o próprio trabalho. Ele lê o diff com a justificativa de cada linha já carregada, e é
justamente a justificativa que esconde o defeito. O revisor em contexto fresco não tem essa
justificativa, e por isso enxerga o que ela estava cobrindo.

Some A2 (alguém tem de responder) a A3 (quem executou carrega os becos sem saída) e sai o
teorema T2: **quem executa não verifica**. O texto do teorema é cuidadoso: verificação
independente **não é desconfiança do autor**; é uma consequência do contexto
([axioms.md, T2](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/axioms.md)).
Isso tira a regra do terreno moral, onde ela soaria como "o agente mente", e a coloca no
terreno físico: o autor não consegue ver o que o próprio contexto esconde, por melhor que
seja.

A ideia não é nova em engenharia, e o tech lead já a pratica com pessoas. A segregação de
funções em controles financeiros, o princípio dos quatro olhos, as inspeções formais de código
que Fagan descreveu na IBM nos anos 1970 e a revisão de código moderna (que Bacchelli e Bird
estudaram na Microsoft e que, segundo eles, entrega tanto transferência de conhecimento quanto
defeitos encontrados) partem da mesma premissa: o autor é o pior leitor do próprio trabalho. O
que muda com agentes são duas coisas. A primeira é o volume: um humano regendo vários agentes
produz mais diff por dia do que consegue reler. A segunda é a facilidade de esquecer o
contrapeso: num time de pessoas, o revisor é outra pessoa por construção; com agentes, o
mesmo humano opera todos eles, e a separação entre quem decide, quem executa e quem verifica
**some em silêncio** se ninguém a escrever.

A literatura sobre fatores humanos dá um aviso complementar. Bainbridge, em *Ironies of
Automation*, mostrou que automatizar a execução e deixar o humano como monitor cria um papel
para o qual o humano é especialmente ruim: vigiar com atenção algo que quase sempre funciona.
Parasuraman e Riley chamaram de *misuse* a confiança excessiva na automação, quando o operador
deixa de conferir porque o sistema costuma acertar. Os dois trabalhos são anteriores aos
modelos de linguagem e valem com mais força para eles: o agente produz texto fluente e
justificado, que convida à leitura confiante. A resposta do Maestro a esses avisos não é pedir
mais atenção ao humano; é tirar dele a tarefa de vigiar cada item e dar a vigilância a uma
posição estruturalmente independente.

### Independência é configuração, não promessa (corolário C3)

"O revisor deve ser imparcial" é uma intenção. Tirar do revisor a capacidade de editar é uma
estrutura. O corolário C3 do Maestro diz isso numa linha: **o papel que julga não recebe
permissão de escrita**. A razão é simples e prática: um revisor que pode consertar o que aponta
deixa de ser revisor e vira coautor. Ele conserta, o conserto entra no diff, e quem confere o
conserto? A independência se sustenta em duas coisas verificáveis: **contexto fresco** (o
revisor não viveu os becos do autor) e **ferramentas restritas** (o revisor só consegue apontar).

O ponto que dá força ao corolário é que ambas são verificáveis **por máquina**. Contexto fresco
é uma propriedade da sessão: o revisor foi iniciado sem a conversa do autor, só com o diff, a
spec e o plano. Ferramentas restritas são uma linha num arquivo de configuração. Nenhuma das
duas depende de o agente "se comportar". E, sendo verificáveis, podem ter um teste que falha.
O teorema T2 traz essa evidência no próprio texto: os agentes que julgam não têm `Write` nem
`Edit`, e um script falha se ganharem. **Independência é configuração, não promessa.**

### Duas posições, não duas pessoas

Juntando as três ideias, o problema da confiança se decompõe em duas posições que nunca podem
coincidir com a de quem executa:

| Posição | Quem ocupa | O que a torna confiável | Axioma |
|---|---|---|---|
| **Verificar** | um agente que julga, em contexto fresco, sem escrita | estrutura: sessão nova, ferramentas restritas | A3 → T2 |
| **Responder** | um humano | exposição: ele perde se der errado | A2 |
| Executar | um agente (ou humano) que escreve | nada: é o objeto da verificação | — |

Repare que a tabela não diz que o humano verifica. Essa é a distinção que separa o modelo
deste livro do *human-in-the-loop* ingênuo. Horvitz, ao propor os princípios das interfaces de
iniciativa mista, colocou o humano no ponto de decisão das ações consequentes, não em cada
passo. O Maestro adota essa espinha e a leva um passo adiante: o humano decide nos gates
(aprovar a spec, aprovar o plano, aprovar o merge, autorizar deploy ou migração) e responde
pela política; a verificação de cada item fica com um agente independente, e o registro dessa
verificação é o que permite ao humano decidir sem refazer.

### O verde mecânico não é o certo

Há um limite que a teoria precisa declarar antes que o tech lead conclua que basta montar o
revisor independente. Em 27 de outubro de 2026, o protótipo navegável do ciclo 074 do Maestro
estava verde: o relatório da tarefa registrava todos os 18 elementos da tela alcançados no
navegador e 63 de 63 botões com o efeito declarado, e a caminhada da sessão regente tinha
aprovado os cinco contextos. O gate humano reprovou a usabilidade: "um amontoado de texto, sem
uma história clara em cada tela, não sei o que faço, por onde começo" [CLAIM-02-014]. A
decisão registrada aponta a causa: a caminhada da regente **conferiu efeito, não história**.

O caso não contradiz T2; ele mostra o que T2 não cobre. A verificação independente pega o que
**diverge do critério**. Ela não pega um critério que mede a coisa errada, e não decide se o
critério certo é o que o usuário quer. Isso fica com o humano, porque é intenção (A1), e com
os capítulos que tratam do critério: o [capítulo 4](../04-a-spec-como-partitura/capitulo.md)
(a spec como fonte da intenção) e o [capítulo 10](../10-quality-gates-que-provam-fatos/capitulo.md)
(o gate que mede o proxy em vez do fato).

## Alternativas

O tech lead tem várias formas de responder à pergunta da confiança. Elas não são excludentes,
mas cada uma resolve uma parte diferente do problema, e algumas resolvem a parte errada.

| Alternativa | O que oferece | Onde falha | Veredito |
|---|---|---|---|
| **Confiar no modelo** (autorrevisão, "reflita e corrija", modelo maior) | barato, sem cerimônia | o autor revê com o próprio contexto (A3); Huang e coautores mostraram que modelos de linguagem não corrigem o próprio raciocínio de forma confiável sem sinal externo; não há a quem atribuir a consequência (A2) | **Rejeitado** como verificação; útil como passo do autor antes de entregar |
| **Juiz de IA no mesmo contexto** (o mesmo agente, ou outro que recebe a conversa inteira) | barato, rápido | herda as justificativas do autor; Zheng e coautores documentaram vieses de juízes de modelo, entre eles o de favorecer respostas parecidas com as próprias | **Rejeitado**; o juiz só serve em contexto fresco |
| **Humano revisa tudo** (*human-in-the-loop* por item) | a responsabilidade e a verificação ficam na mesma pessoa | armadilha do funil; o monitor humano é ruim em vigiar o que quase sempre funciona (Bainbridge) | **Rejeitado** como regra geral; vale para a classe irreversível |
| **Proteção de branch na plataforma** (revisão obrigatória antes do merge, autor não aprova o próprio pull request, aprovação invalidada a cada novo *push*) | enforcement fora do modelo, auditável, barato | garante que **alguém** aprovou, não que esse alguém leu em contexto fresco; se o mesmo humano opera o agente e aprova, a separação é nominal | **Adotado** como camada de baixo; não basta sozinho |
| **Pausa para aprovação nos frameworks de orquestração** (as interrupções do LangGraph, o `human_input` das tarefas do CrewAI, aprovações de ferramenta nos kits de desenvolvimento de agentes (Software Development Kits, SDKs)) | o fluxo para e pede um humano no ponto certo | resolve **onde** parar, não **quem** verifica nem **com que registro**; tende a virar aprovação por item | **Adotado** como mecanismo; a política de onde parar continua sua |
| **Avaliador-otimizador** (um agente gera, outro avalia e devolve, em laço) | separa gerar de avaliar | se o avaliador recebe o histórico do gerador, a separação é só de nome; não localiza a responsabilidade | **Adotado** desde que o avaliador seja fresco e sem escrita |
| **Norma externa** (supervisão humana no art. 14 do Regulamento Europeu de Inteligência Artificial, o AI Act; função *Govern* do AI Risk Management Framework do National Institute of Standards and Technology, o NIST AI RMF) | exige que a supervisão e a responsabilidade existam e sejam documentadas | diz **o quê**, não **como**; a conformidade no papel não impede a caixa marcada sem testemunha | **Adotado** como requisito; o método deste capítulo é uma forma de cumpri-lo |

A leitura da tabela: nenhuma alternativa isolada resolve as duas posições. A proteção de branch
e as pausas dos frameworks resolvem o **mecanismo** do gate humano; a separação gerador/avaliador
resolve parte da **verificação**; a norma externa exige que ambas existam. O que falta em todas
é a amarração: o verificador é estruturalmente independente (contexto e ferramentas), o humano
responde pela política e não pelo item, e há um registro que uma máquina confere. É essa
amarração que o padrão a seguir oferece, e ela é independente de ferramenta: qualquer
harness que permita restringir as ferramentas de uma sessão e iniciar outra sem histórico
consegue reproduzi-la.

## O padrão Maestro

O Maestro resolve o problema em três camadas, e vale distinguir o que é **regra** (texto que
alguém tem de seguir), o que é **configuração** (o harness impõe) e o que é **script** (uma
máquina confere e falha). Tudo abaixo é citado em `maestro@19823c2`.

### A regra

- **Princípio II** da constituição: papéis são **modos de trabalho** numa matriz RACI;
  Responsible, Consulted e Informed são delegáveis a agentes; o Accountable é sempre humano e
  responde pela política, pelos gates e pelos critérios; a verificação é feita por um agente
  independente em contexto fresco ([principles.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/principles.md)).
- **ADR 0004**, o registro de decisão que criou o modelo
  operacional em 22 de julho de 2026: papéis viram modos de trabalho com RACI por etapa; quem
  decide, quem executa e quem verifica são posições diferentes; o "verifica" passa a um agente
  revisor em contexto fresco; o Accountable é fixo e humano em toda linha de risco
  ([ADR 0004](https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0004-modelo-operacional.md)).
  O mesmo ADR adota uma cadência leve (Shape Up com Kanban, uma tarefa em andamento por vez,
  retrospectiva individual, sem *daily* nem *sprint planning*), coerente com um humano que rege
  agentes em vez de um time de pessoas.
- **Mapa de gates humanos inegociáveis** no modelo operacional, §8: aprovar a spec, aprovar o
  plano (com o Constitution Check), aprovar o merge, autorizar deploy ou migração
  [CLAIM-02-016]. A mesma seção gradua os demais gates por classe de risco, assunto do
  [capítulo 11](../11-risco-reversibilidade-e-autonomia/capitulo.md)
  ([operating-model.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/operating-model.md)).
- **Anti-padrão 6, "autor como revisor"**, no catálogo da skill `anti-patterns`: o agente que
  escreveu aprovando o próprio trabalho; a revisão acontece em contexto fresco, sempre
  ([SKILL.md](https://github.com/GHDaru/maestro/blob/19823c2/skills/anti-patterns/SKILL.md)).

### A configuração

Os agentes do Maestro são arquivos curtos em `.claude/agents/`, cada um com uma linha `tools:`
que o harness lê e impõe. Dos treze agentes, os três que julgam (`review`, `security` e
`process-guardian`) são exatamente os três sem `Write` nem `Edit` [CLAIM-02-009]. O contrato
do `review` diz o resto: revisão independente do diff **contra o plano**, em contexto fresco,
"você não escreveu este código"; somente leitura; julga, não conserta; aponta só lacunas de
correção ou de requisito, não preferência de estilo, porque um revisor que caça tudo induz
excesso de engenharia; e lembra que "verde localmente não é certo globalmente", passando essa
decisão ao humano ([review.md](https://github.com/GHDaru/maestro/blob/19823c2/.claude/agents/review.md)).
O `dev-implementer`, do outro lado, tem `Write` e `Edit` e um contrato que diz que ele não
revisa nem aprova o próprio trabalho.

Essa separação é o que o harness impõe: o `review` não consegue editar um arquivo, ainda que
"queira". É uma propriedade da sessão, não do prompt.

### Os scripts

- **`scripts/check-agents.sh`** lista os papéis somente-leitura e falha se algum deles ganhar
  `Write` ou `Edit` na linha `tools:`. É o corolário C3 virando teste: se alguém, numa edição
  inocente, der caneta ao juiz, a verificação local e a integração contínua ficam vermelhas
  ([check-agents.sh](https://github.com/GHDaru/maestro/blob/19823c2/scripts/check-agents.sh)).
- **A cauda de fechamento e o `check-conformance.sh`**: todo ciclo carrega no `tasks.md` as
  caixas `TAIL:review`, `TAIL:security`, `TAIL:mutation` e `TAIL:gate`, com a evidência no
  `qa-report.md`. Depois dos ciclos 042 a 045, o portão rejeita o esqueleto do gerador, o
  marcador vazio e, desde o ciclo 063, a palavra "pendente" usada como se fosse evidência
  [CLAIM-02-020]. O `TAIL:gate` é sempre do humano.
- **`scripts/promote-main.sh`**, o gate de merge. O comentário de abertura diz a fronteira com
  todas as letras: "o gate é humano; este script só executa o passo mecânico depois da sua
  decisão; ele não decide nada". O script aborta com árvore suja, aborta se não há o que
  promover, **recusa promover com a conformidade vermelha** (a cauda incompleta não chega à
  linha principal), mostra os commits, pede confirmação explícita e, depois do "sim", registra
  a decisão sozinho no índice como `gate-main-<hash>` antes de empurrar
  ([promote-main.sh](https://github.com/GHDaru/maestro/blob/19823c2/scripts/promote-main.sh)).
  Automatizar a execução do ritual é economia de atenção; automatizar a decisão violaria o
  Princípio II. O resultado é um rastro: no índice de decisões em `19823c2`, 50 das 199 linhas
  são gates de merge, cada uma com hash e data [CLAIM-02-011].

### E o hook?

Neste tema, nenhum. A independência do revisor no Maestro **não** depende de um *hook* que
intercepte a chamada de ferramenta: depende da lista de ferramentas que o harness entrega à
sessão (configuração) e de um script que confere essa lista (verificação). Os hooks do Maestro
guardam outra coisa: por exemplo, recusam a reescrita do corpo de um ADR ou do índice de
decisões, que só aceitam acréscimo. A distinção importa para quem leva o padrão a outro
harness: se ele não tem hooks, este capítulo continua inteiro; se ele não permite restringir
ferramentas por sessão, a independência volta a ser promessa e tem de ser compensada por
processo.

### Gate humano por delegação de política

O desenho acima tem um custo: o humano ausente para a linha. Em 22 e 24 de outubro de 2026, o
dono do método passou a conduzir ciclos por uma sessão regente que não executa (distribui o
trabalho a outras sessões e subagentes), e a espera pelo "sim" dele em cada gate chegou a
horas. Em 24 de outubro, ele delegou por escrito: "Peço que os 'meus' gates sejam assumidos por
você. Chame um subagente par seu para ajudar a criticar e tomar a decisão. E prossiga sem
parar." O crítico do gate
seguinte, o `process-guardian` em contexto fresco, apontou que a delegação contradizia a letra
do §8 do modelo operacional e pediu base escrita. A base virou o **ADR 0026**
([ADR 0026](https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0026-gate-humano-por-delegacao-de-politica.md)).

O ADR permite que a sessão regente decida um gate humano **quando, e só quando**, cinco
condições valem juntas [CLAIM-02-015]:

1. o humano delegou por escrito, a delegação está no índice de decisões e não foi revogada;
2. a regente **não executou** o trabalho julgado;
3. um crítico independente em contexto fresco, somente leitura, deu parecer antes da decisão,
   registrado no relatório de qualidade com as condições que impôs;
4. cada gate aberto por delegação gera sua própria linha no índice, com o veredito do crítico
   e o hash julgado;
5. a promoção para a linha principal continua exigindo a delegação explícita para aquele ciclo.

O primeiro uso está registrado como `gate-070-delegado`: o `TAIL:gate` do ciclo 070 foi aberto
pela regente depois do parecer `APPROVE_WITH_CONDITIONS` do crítico, com cinco condições
fechadas no relatório [CLAIM-02-017]. Este é o ponto conceitual mais fino do capítulo: a
delegação **não** transfere o Accountable. O humano continua respondendo pela política (a
delegação), pelos critérios (as cinco condições) e pode revogá-la com uma linha. O que ele deixa
de fazer é responder **por item**, que é exatamente o que o Princípio II pedia desde o começo.
T2 continua de pé em dobro: quem decide não executou, e alguém de contexto fresco leu antes.

### Revisão por tarefa e a crítica às cegas

Dois refinamentos completam o padrão. O primeiro veio de fora: o catálogo do ecossistema
avaliou a prática do Superpowers de revisar **cada tarefa** em contexto fresco, e não só o
ciclo. O veredito foi **absorver em parte**: na raia plena com mais de três tarefas, um
checkpoint leve por tarefa; em toda mudança, seria cerimônia desproporcional na raia leve
[CLAIM-02-018] ([ideia 025](https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/ideias/025-review-por-task.md)).

O segundo nasceu dentro do ciclo 076 e mostra até onde a independência pode ir. Em 1º de
novembro de 2026, a tarefa T035b entregou uma seção de documentação gerada a partir do modelo
de domínio. A mecânica funcionava, os testes passavam. O juiz em contexto fresco reprovou por
três motivos medidos: a integração contínua regerava da projeção gravada e não do modelo (uma
projeção adulterada passava verde com a tela afirmando o contrário do modelo), o texto visível
carregava referências internas e o termo pedido não tinha virado a palavra da tela. E acrescentou
uma **crítica às cegas**: leu sem rótulo o começo do nosso texto e o da descrição de domínio do
projeto público `ddd-by-examples/library`, e decidiu qual um operador novo entenderia mais
rápido. Perdemos [CLAIM-02-012]. A rodada seguinte (T035c com T036) consertou a mecânica e
foi reprovada de novo: a pergunta do operador ("o que é uma Sessão e quem manda nela?") seguia
sem resposta, o cego perdeu outra vez, e o job de portões da integração contínua estava
vermelho na árvore intacta por causa de comentários em português num script instalável. O juiz
ainda notou que o teste escrito para a crítica anterior media **obediência à crítica**, não a
resposta [CLAIM-02-013]. A crítica às cegas é a forma mais forte de contexto fresco: o juiz não
sabe nem qual dos textos é o nosso.

## Exemplo executável

O exemplo em [`exemplo/`](exemplo/README.md) transforma as regras deste capítulo num portão que
roda em qualquer máquina com Python 3.8 ou mais novo, sem dependência e sem modelo de IA. Ele
não julga o código de ninguém: julga a **estrutura** de um fechamento de ciclo.

Há três entradas. `papeis.json` descreve os papéis de um time humano com agentes: quem julga,
que ferramentas cada um tem, que delegações escritas existem. `registros/` traz dez fechamentos
de ciclo [CLAIM-02-019], um correto e os outros com um defeito cada, todos tirados deste capítulo: o autor que
se revisa, a caixa marcada sem testemunha (042), a palavra "pendente" aceita como prova (061 e
062), o juiz com caneta, o revisor que leu a conversa do autor, o merge aprovado por um agente
sem delegação, o gate delegado sem crítico e a regente que abre o gate do trabalho que ela
mesma fez. Cada registro declara o veredito esperado.

O `verifica.py` aplica seis regras, de R0 a R5, cada uma com a origem no texto: R0 confere a
configuração (papel que julga sem escrita, o C3); R1 a R3 conferem a revisão (outra posição,
um papel que julga, contexto fresco, o T2); R4 confere a evidência da caixa marcada; R5
confere o dono do gate (humano, ou delegação escrita com as condições do ADR 0026, o A2).
Depois, ele **prova o próprio portão por mutação**: dá `Edit` ao revisor e revoga a delegação,
e confere que as duas violações são acusadas. Um portão que nunca foi visto falhar é uma
crença, não um portão.

```bash
cd livro/02-o-problema-da-confianca/exemplo
python verifica.py
```

As últimas linhas da saída:

```text
== prova por mutação: o portão acusa quando a regra é violada?
  revisor ganha Edit -> R0 acusa
  delegação revogada -> 08-gate-delegado reprova

resultado: 10/10 registros com o veredito esperado; mutações acusadas: 2/2
✓ verificação de confiança OK
```

Repare em duas linhas que aparecem no topo da saída: `aviso R0 'revisor' julga e tem Bash: o
shell também escreve`. O exemplo não reprova esse caso, mas avisa, e o
[Contraexemplo](#contraexemplo) explica por quê.

O segundo script, `rendimento.py`, mede o que a revisão independente fez no Maestro. A entrada
é uma linha por ciclo, do 042 ao 063, tirada de `maestro@19823c2` por dois comandos que o
`README.md` do exemplo reproduz: o veredito do cabeçalho do relatório de qualidade e a
evidência de `TAIL:review` no corpo do mesmo relatório. Da evidência saem duas colunas, lidas à
mão: quando a revisão rodou (antes do gate ou só depois da promoção) e o que ela fez (reprovou
ou não mudou nada). O script só conta.

```text
ciclos: 22 · revisão antes do gate: 20 · revisão só depois da promoção: 2
rendimento da revisão antes do gate: 19/20 = 95.0%
cobertura da revisão antes do gate: 20/22 = 90.9%
ciclos reprovados por um parecer, em qualquer momento: 21/22 = 95.5%
cabeçalho 'aguardando parecer' com parecer no corpo: 3 (061, 062, 063)
```

Em 19 dos 20 ciclos em que a revisão independente rodou antes do gate, ela reprovou e o
resultado mudou; o único que passou sem mudança foi o 052, cuja evidência cita o parecer do
051 como origem do ciclo e não relata reprovação [CLAIM-02-008]. Os dois ciclos em que a
revisão não rodou antes do gate, o 061 e o 062, são os que o portão deixou passar com
"pendente." no lugar da evidência, com o humano avisado da ausência antes de decidir
[CLAIM-02-020]. Quando a revisão enfim rodou, depois da
promoção, um parecer só reprovou os dois com 18 achados; o 063 nasceu para fechar o buraco, e a
revisão do próprio 063, feita antes do gate dele, o reprovou com 18 defeitos, cinco deles
introduzidos pelo próprio ciclo [CLAIM-02-022].

A última linha da saída está ali por um erro deste livro. A primeira versão do exemplo
classificava os ciclos pelo cabeçalho do relatório, e o cabeçalho dos três últimos dizia "DoD
verde; aguardando parecer e portão humano" (DoD é a Definition of Done, a definição de pronto
verificável do ciclo). Lido como fato, isso dava três ciclos sem revisão e
um rendimento de 18 em 19. Mas o cabeçalho é escrito por quem executou, num momento do ciclo, e
ninguém voltou para atualizá-lo; o corpo do 063 registra a revisão e o gate que vieram depois.
A lição é a do capítulo em miniatura: o resumo que o autor escreve de si não é testemunha.

O script de rendimento é a métrica que a agenda de pesquisa do livro chama de **rendimento da
revisão independente**, aplicada ao seu repositório: troque o arquivo de valores separados por
vírgula (Comma-Separated Values, CSV) pelos pareceres dos seus últimos pull requests (lidos no
corpo da revisão, não no título) e veja o número.

## Contraexemplo

A regra "quem executa não verifica" tem custo, tem furos e tem lugares onde atrapalha. Um tech
lead que a adote sem esta seção vai descobrir os três na prática.

**O custo em mudança pequena.** Uma revisão em contexto fresco custa uma sessão nova, a leitura
do diff, da spec e do plano, e o tempo de tratar os achados. Para corrigir um erro de digitação
no README, é cerimônia. O próprio Maestro reconhece isso duas vezes: na raia leve, o pull
request é o artefato e não há spec nem plano; e, ao avaliar a revisão por tarefa, absorveu-a
só em parte, porque aplicá-la a toda mudança violaria o princípio de governança leve
[CLAIM-02-018]. A regra prática é proporcional: a revisão independente é obrigatória no
fechamento do ciclo e onde há risco; por tarefa, só quando o ciclo é grande o bastante para
que o erro cedo economize retrabalho.

**O furo do shell.** O `check-agents.sh` procura `Write` e `Edit` na linha `tools:`. O `review`
e o `security` têm `Bash`, e um shell escreve arquivo com um redirecionamento [CLAIM-02-010].
A independência por configuração é tão boa quanto a lista que ela confere. O Maestro aceita o
furo porque o revisor precisa rodar os portões para julgar (as críticas do 076 rodaram ataques
em cópias temporárias e escreveram o próprio parecer), e a defesa passa a ser o contrato do
papel e o fato de que qualquer escrita do revisor aparece no diff. É por isso que o exemplo
emite aviso em vez de reprovar. Se o seu harness permitir um shell somente leitura, ou se
o revisor puder rodar numa cópia descartável do repositório, feche o furo.

**Independência não conserta o critério.** O caso do 074 mostra que um protótipo verde em
todas as verificações pode ser reprovado pelo humano, porque o critério media efeito e não
história [CLAIM-02-014]. A crítica da T035c mostra o mesmo fenômeno dentro da própria
verificação: o teste escrito para atender o juiz anterior media se os trechos citados estavam
presentes, e não se a pergunta do operador era respondida [CLAIM-02-013]. Revisor fresco
contra um critério errado produz um "não" ou um "sim" confiável sobre a coisa errada. O
[capítulo 10](../10-quality-gates-que-provam-fatos/capitulo.md) trata desse defeito.

**Mesmo modelo, mesmos pontos cegos.** O revisor em contexto fresco não herda a conversa do
autor, mas, se for o mesmo modelo, herda o treinamento. Defeitos que o modelo tende a não ver
podem escapar dos dois lados. É uma hipótese plausível, não medida aqui; quem tem orçamento
pode variar o modelo do revisor e comparar o rendimento.

**A delegação tensiona a letra.** Em `19823c2`, o §8 do modelo operacional ainda diz que nenhum
dos gates inegociáveis é delegável a um agente, enquanto o ADR 0026, de 24 de outubro, emenda
esse parágrafo e promete incorporar o texto na próxima revisão [CLAIM-02-015]. Quem lê só o
modelo operacional conclui uma coisa; quem lê o índice de decisões, outra. É o custo de uma
governança que evolui por acréscimo: a regra viva está em dois lugares até a revisão
acontecer. E a delegação só é segura enquanto as cinco condições são conferidas; sem o crítico
e sem a linha por gate, ela vira o agente aprovando a si mesmo com um ADR na mão.

**Quando não aplicar.** Em exploração descartável (um *spike* que vai para o lixo, um protótipo
de uma tarde), a verificação independente custa mais do que o erro. O critério é a
reversibilidade: se o resultado não vai sair da sua máquina, não há consequência a que
alguém responda. No momento em que ele vai para a linha principal, para um repositório alheio
ou para o usuário, a regra volta.

## Evidência

Os claims abaixo estão registrados em [`claims.md`](claims.md), com o caminho no Maestro
fixado em `19823c2` ou o comando que os reproduz.

**Medido** (um comando reproduz o número):

- os seis ciclos de 046 a 051 têm no cabeçalho "aprovado após reprovação e correção"
  [CLAIM-02-006];
- os três agentes sem `Write` nem `Edit` são os três que julgam, entre treze [CLAIM-02-009];
- o índice de decisões tem 50 gates de merge em 199 linhas [CLAIM-02-011];
- o exemplo deste capítulo acerta o veredito dos dez registros e acusa as duas mutações
  [CLAIM-02-019].

**Observado** (lido nos artefatos; quando há contagem, o script conta, mas a classificação
de cada caso é leitura humana): dos 22 ciclos entre 042 e 063, a revisão independente rodou
antes do gate em 20 e reprovou 19 deles; 061 e 062 passaram pelo gate sem revisão
[CLAIM-02-008]; a revisão do 063 reprovou o próprio ciclo com 18 defeitos [CLAIM-02-022]; a retrodatação do 047 e o que a
correção recuperou [CLAIM-02-001, CLAIM-02-002]; a cauda que reprovou o ciclo que a criou
[CLAIM-02-003]; a recorrência da caixa marcada sem testemunha no 043 e no 045 [CLAIM-02-004,
CLAIM-02-005]; os dois achados do 048 e do 051 que chegariam a terceiros [CLAIM-02-007]; o furo
do shell [CLAIM-02-010]; as duas críticas reprovadas no 076 [CLAIM-02-012, CLAIM-02-013]; o
gate humano do 074 [CLAIM-02-014]; o ADR 0026 e o primeiro gate delegado [CLAIM-02-015,
CLAIM-02-017]; os quatro gates inegociáveis [CLAIM-02-016]; a absorção parcial da revisão por
tarefa [CLAIM-02-018]; e os ciclos 061 e 062 promovidos com "pendente." [CLAIM-02-020].

**Hipótese.** O número de 19 em 20 é forte, mas não é a prova de que a revisão em contexto
fresco acha mais defeito que a autorrevisão; essa é a hipótese H2 da agenda de pesquisa do
livro, e ela continua hipótese [CLAIM-02-021]. Três motivos. Não há grupo de controle: nenhum
ciclo foi revisado pelo próprio autor com o mesmo esforço para comparação. A classificação é
leitura humana da evidência de `TAIL:review`, escrita por quem executou, e "reprovou" pode
incluir parecer cujo achado era menor; o 052 foi contado como "não mudou" porque a evidência
dele não relata parecer próprio, a leitura que menos favorece a revisão. E há viés de
seleção: a revisão foi instruída a refutar e a executar ataques, o que aumenta a chance de achar algo. O desenho que testa H2 (o mesmo conjunto de diffs, revisão pelo
autor contra revisão fresca, defeitos plantados conhecidos) está no
[capítulo 15](../15-validando-o-maestro/capitulo.md).

## Checklist

Aplique no seu time. Cada item tem uma forma de conferir que não depende de opinião.

- [ ] **Existe um nome por gate.** Para cada um dos gates que você considera inegociáveis
  (spec, plano, merge, deploy ou migração), o registro diz quem aprovou e quando. Conferência:
  abra o último merge na linha principal e ache o nome.
- [ ] **O agente que julga não tem caneta.** As sessões de revisão e segurança são iniciadas
  sem ferramenta de escrita. Conferência: um script, na integração contínua, que falha se a
  configuração mudar (o `verifica.py` do exemplo é um ponto de partida).
- [ ] **O revisor começa do zero.** A revisão recebe o diff, a spec e o plano, e não a conversa
  de quem executou. Conferência: o comando ou o template que inicia a revisão, versionado.
- [ ] **O autor não fecha a própria caixa sem evidência.** A caixa de revisão só fica marcada se
  houver um parecer escrito por outra posição, e "pendente", "ok" ou o marcador do gerador não
  contam. Conferência: um portão que rejeita placeholder, visto falhar ao menos uma vez.
- [ ] **O merge é um passo mecânico depois de uma decisão humana.** O script ou a proteção de
  branch executam; não decidem. Conferência: tente promover com a cauda incompleta e veja
  recusar.
- [ ] **Delegação de gate é escrita, revogável e tem crítico.** Se você delega gates a um
  agente regente, a delegação está registrada, quem decide não executou, um crítico fresco
  opinou antes e cada gate aberto deixa uma linha. Conferência: as condições do ADR 0026 como
  lista no seu registro de decisões.
- [ ] **Você mede o rendimento da revisão.** De cada dez revisões independentes, quantas mudaram
  o resultado? Conferência: o `rendimento.py` rodando sobre os seus últimos vereditos. Se o
  número for próximo de zero, ou a revisão é cerimônia, ou o autor é excepcional; descubra
  qual antes de cortar.

## Referências

- Axiomas, teoremas e corolários do Maestro (A1, A2, A3, T2, C3).
  https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/axioms.md
- Constituição do Maestro, Princípio II.
  https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/principles.md
- Modelo operacional do Maestro, §2 (princípio operacional central) e §8 (gates).
  https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/operating-model.md
- ADR 0004 — Modelo operacional.
  https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0004-modelo-operacional.md
- ADR 0026 — Gate humano por delegação de política, com crítico independente.
  https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0026-gate-humano-por-delegacao-de-politica.md
- Índice de decisões (`gate-070-delegado`, `decisao-074-usabilidade-reprovada`,
  `achado-047-vereditos-retrodatados`).
  https://github.com/GHDaru/maestro/blob/19823c2/docs/records/decisoes.jsonl
- Agentes `review`, `security`, `process-guardian` e `dev-implementer`.
  https://github.com/GHDaru/maestro/blob/19823c2/.claude/agents/review.md
- Scripts `check-agents.sh` e `promote-main.sh`.
  https://github.com/GHDaru/maestro/blob/19823c2/scripts/check-agents.sh ·
  https://github.com/GHDaru/maestro/blob/19823c2/scripts/promote-main.sh
- Skill `anti-patterns`, item 6.
  https://github.com/GHDaru/maestro/blob/19823c2/skills/anti-patterns/SKILL.md
- Ideia 025 do catálogo do ecossistema — revisão por tarefa.
  https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/ideias/025-review-por-task.md
- Relatórios de qualidade dos ciclos 042, 043, 045, 047, 048, 051 e 074; spec do ciclo 063;
  críticas da T035b e da T035c+T036 no ciclo 076, todos em
  https://github.com/GHDaru/maestro/tree/19823c2/specs
- Handbook do Maestro, capítulos 01 (o princípio central), 04 §6 e 06 (papéis e RACI) e
  apêndice B (Superpowers), na cópia congelada em `maestro-handbook/` deste repositório.
- L. Bainbridge. *Ironies of Automation*. Automatica, 19(6), 1983.
- R. Parasuraman e V. Riley. *Humans and Automation: Use, Misuse, Disuse, Abuse*. Human
  Factors, 39(2), 1997.
- M. E. Fagan. *Design and Code Inspections to Reduce Errors in Program Development*. IBM
  Systems Journal, 15(3), 1976.
- A. Bacchelli e C. Bird. *Expectations, Outcomes, and Challenges of Modern Code Review*.
  International Conference on Software Engineering (ICSE), 2013.
- E. Horvitz. *Principles of Mixed-Initiative User Interfaces*. Conference on Human
  Factors in Computing Systems (CHI), 1999.
  https://www.microsoft.com/en-us/research/publication/principles-mixed-initiative-user-interfaces/
  (acesso em 02/11/2026).
- J. Huang et al. *Large Language Models Cannot Self-Correct Reasoning Yet*. International
  Conference on Learning Representations (ICLR), 2024.
- L. Zheng et al. *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*. Conference on
  Neural Information Processing Systems (NeurIPS), 2023, Datasets and Benchmarks.
- Anthropic. *Building effective agents* (padrão avaliador-otimizador).
  https://www.anthropic.com/engineering/building-effective-agents (acesso em 02/11/2026).
- GitHub Docs. *About protected branches*.
  https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
  (acesso em 02/11/2026).
- LangChain. *LangGraph — human-in-the-loop*.
  https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/ (acesso em 02/11/2026).
- Regulamento da União Europeia (UE) 2024/1689 (AI Act), art. 14 — supervisão humana.
  https://eur-lex.europa.eu/eli/reg/2024/1689/oj (acesso em 02/11/2026).
- NIST. *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*, NIST AI 100-1, 2023.
  https://doi.org/10.6028/NIST.AI.100-1 (acesso em 02/11/2026).
- `ddd-by-examples/library`, README, seção *Domain description*.
  https://github.com/ddd-by-examples/library (acesso em 02/11/2026).
