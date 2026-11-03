# Prefácio — por que este livro

> *O agente escreve. Alguém ainda precisa responder pelo que foi escrito.*

## O ciclo 047

Em 10 de agosto de 2026, um ciclo de trabalho do Maestro, o método que este livro estuda,
terminou com o autor confessando no próprio relatório de qualidade: tinha trocado e
retrodatado seis vereditos de um índice histórico [CLAIM-00-001]. O ciclo, o 047, existia
justamente para impedir que um registro sobrevivesse ao fato que ele descreve. A spec acusava
um documento antigo de reclassificar decisões sem deixar rastro, e o próprio ciclo cometeu a
versão mais direta desse defeito, numa linha datada de 30 de julho, onze dias antes, e
atribuída a outro ciclo.

Ninguém percebeu lendo com atenção. Percebeu um revisor independente, em contexto novo, que
não tinha escrito uma linha daquele trabalho. O veredito dele foi «não promover como está»,
com cinco bloqueantes. Um dos bloqueantes era mais incômodo que a retrodatação: o portão
automático que o ciclo acabara de criar para conferir o catálogo não discriminava nada.
Bastava apontar qualquer arquivo existente como prova de uma absorção, e o `README.md`
passava [CLAIM-00-001]. O verde era verdadeiro e não provava nada.

Não houve vilão. O que funcionou foi um arranjo: quem executou não verificou. O que falhou também foi um
arranjo: um *check* que media a presença de um arquivo, e não a coisa que dizia medir. Este
livro é sobre esses arranjos. Com agentes de Inteligência Artificial (IA) escrevendo código,
a qualidade do resultado depende menos do modelo do que da governança em volta dele, e essa
governança se projeta, se testa e se mede como qualquer outra parte do sistema.

## Para quem é este livro

Para o *tech lead*: o engenheiro sênior que responde por um time e que, de uns meses para cá,
também rege agentes. Você sabe programar, conhece Git, integração contínua (CI), revisão de
código e alguma forma de Scrum ou Kanban. Não precisa saber o que é o Maestro, nem usar a
ferramenta com que ele foi construído.

Você provavelmente já viveu uma das duas pontas que falham. Na primeira, sem IA, entender um
sistema legado exige dúzias de pessoas reconstruindo uma intenção perdida, e o conhecimento
vai embora com quem sai. Na segunda, com IA mas sem método, o agente escreve código que
compila, passa no teste e erra a intenção; a velocidade vira risco. O Maestro nasceu de uma pergunta feita a
partir dessa segunda ponta: *se um agente escreve o código, o que muda?* A resposta que
este livro defende é que o valor do trabalho humano migra de digitar para duas coisas:
deixar a intenção clara e verificar o resultado.

Três passos para a segunda-feira, antes do resto do livro. Liste os portões do seu
*pipeline* e escreva, para cada um, o que ele afirma provar e o que de fato confere; onde as
duas frases diferem, há um proxy. Classifique as ações dos seus agentes pelo custo de
desfazer e confira que a aprovação humana está nas irreversíveis, não nas baratas. E, para
cada agente que revisa, pergunte se ele consegue alterar o que revisa, inclusive por terminal.

## A tese

O Maestro não é mais um *framework* de agentes. Não compete com LangGraph, CrewAI ou o kit
de desenvolvimento (*Software Development Kit*, SDK) de agentes de um fornecedor; não orquestra chamadas de modelo nem define formato de
mensagem. É um **sistema de governança operacional** para engenharia de software com
agentes: uma constituição, raias de processo, papéis, artefatos, portões, registros de
decisão, *skills*, scripts e *hooks*. Essa camada roda sobre o *harness* e o modelo que você
tiver. Quando um nome de produto
aparece no texto, é exemplo, nunca premissa.

A tese se apoia em cinco ideias, que se reforçam.

**Instrução não é enforcement.** Escrever no arquivo de instruções do agente "nunca reescreva
um registro de decisão" é um pedido, que o modelo pode cumprir ou não.
No Maestro, um *hook* intercepta cada chamada de ferramenta antes que ela rode
(`scripts/hooks/guard-immutables.py`, ligado em
[`.claude/settings.json`](https://github.com/GHDaru/maestro/blob/19823c2/.claude/settings.json))
e recusa a edição de um *Architecture Decision Record* (ADR) já versionado [CLAIM-00-002]. Em qualquer *harness* o mecanismo é
o mesmo: um ponto de interceptação antes da ação, fora do modelo, com poder de recusa. Mas o
próprio script declara onde para: nas regras de histórico ele não julga o terminal, e um
`sed -i` reescreve o corpo de um ADR sem passar por ele [CLAIM-00-002]. O arquivo de
instruções diz que a regra é imposta, não pedida; é imposta contra a ferramenta de edição,
não contra o terminal. A lição tem duas metades: o que pode virar comando vira comando, e o
comando declara o que não cobre. O que exige julgamento fica com um humano, num lugar declarado.

**Quem executa não verifica.** A revisão independente não nasce de desconfiança do autor. É
consequência de como o contexto funciona. O agente que escreveu carrega os becos sem saída
que explorou e tende a ler o próprio diff com os olhos de quem já sabe o que quis dizer. A
história do ciclo 047 é isso: o erro só apareceu para quem chegou sem essa carga. No Maestro,
a independência começa na configuração (em qualquer *harness*, a lista de capacidades de
cada agente), e o próprio método mostra onde ela para. Dos treze
agentes, três (`review`, `security` e `process-guardian`) são declarados somente leitura: não
têm as ferramentas `Write` nem `Edit`, e um script falha se algum ganhar uma
[CLAIM-00-003]. Mas `review` e `security` têm `Bash`, e por um terminal se escreve qualquer
arquivo. O script confere a ausência de duas palavras na lista, não a impossibilidade de escrever:
um check que mede o proxy dentro da defesa da independência.

**Autonomia proporcional à irreversibilidade.** Um portão humano uniforme está sempre errado.
Pesado em tudo, transforma o humano em carimbo; leve em tudo, deixa passar o irreversível. O
portão tem de ser função do custo de desfazer e do raio de impacto da ação. Ler código não
pede aprovação; promover para a linha principal pede; apagar dados em produção pede mais que
aprovação, pede reversibilidade engenheirada (backup, execução a seco, homologação, exclusão
lógica), que é o que rebaixa a classe de risco e torna a ação delegável. O documento de
axiomas do Maestro registra, quando esse teorema foi escrito, 21 portões de *merge* no índice
de decisões enquanto dezenas de operações reversíveis rodavam sem aprovação, e admite que
quatro das sete classes de risco nunca tinham ocorrido [CLAIM-00-004]. É um balanço do autor,
não uma contagem que você refaz por comando.

**O check mede o proxy, não o fato.** Esta é a ideia que mais muda o trabalho de um *tech
lead*. Quando o agente passa a cumprir os portões com competência, o erro deixa de estar no
"o agente errou" e passa a estar no "o portão mede a coisa errada". O teste conta a palavra e
não o número; o *script* confere que o arquivo existe e não que diz a verdade; a
cobertura sobe e nenhuma asserção discrimina o certo do plausível. No Maestro, o anti-padrão
«um check que mede o proxy, não o fato» recorreu quatro vezes antes de virar lei numa *skill*,
e o mesmo documento conta, sem listá-los, nove defeitos que chegaram à linha principal com o
portão verde, todos pegos depois por uma checagem escrita, nunca por leitura atenta
[CLAIM-00-005]. A consequência
prática é desconfortável: o portão também precisa ser testado, e a forma de testá-lo é vê-lo
falhar.

**Contexto é recurso finito.** A janela que o agente lê tem limite, e o desempenho cai à
medida que ela se enche de ruído. Daí saem quatro operações que você vai fazer o tempo todo: *selecionar* o que o
agente lê, *comprimir* o que já foi feito, *persistir* em artefato o que precisa sobreviver à
sessão e *transferir* o que um agente entrega ao próximo. Daí sai também a razão de fatiar o
trabalho e manter cada agente estreito.

### De onde vêm essas ideias

As cinco ideias não foram escolhidas por gosto. O Maestro as deriva de cinco axiomas, que
assume sem provar, e de sete teoremas, que precisam ser demonstráveis com evidência do
próprio repositório; dos teoremas saem treze corolários, que são de onde vêm as regras do
dia a dia [CLAIM-00-006]. Os axiomas cabem num parágrafo. A intenção é humana: o agente
propõe, escreve e verifica, mas não *quer*. A consequência precisa de dono: o agente não
carrega perda nenhuma se errar, e por isso a responsabilidade não se transfere a ele, por
falta de exposição e não de capacidade. O contexto é finito e degrada ao encher. O que está
escrito é o que sobrevive, porque o agente começa cada sessão do zero. E o custo é assimétrico
entre fazer e desfazer: produzir está cada vez mais barato, desfazer não.

A camada de derivação serve para podar: uma regra que não deriva de axioma nenhum ou é um
axioma novo, defendido por escrito, ou é cerimônia, e sai. O livro usa a mesma disciplina:
cada capítulo declara de onde deriva, e o que não deriva de nada é ferramenta, que mora no
manual.

## O que é o Maestro, em um parágrafo

O Maestro é o método de **um humano regendo muitos agentes**, construído e usado num
repositório público ([GHDaru/maestro](https://github.com/GHDaru/maestro/blob/19823c2/README.md))
que foi desenvolvido por ele mesmo: entre 27 de julho e 1º de novembro de 2026, o histórico
acumulou 943 *commits*, 75 pastas de ciclo numeradas, 30 registros de decisão de arquitetura,
os ADRs, treze agentes, seis *skills* e dezenove scripts de
verificação [CLAIM-00-007]. A imagem do nome é de orquestra: a partitura (a especificação) diz
o que tocar, o compasso (os portões) marca o ritmo, os músicos (os agentes) executam, e o
maestro não toca instrumento nenhum. O núcleo é uma constituição de oito princípios
[CLAIM-00-008], que vão da especificação como fonte de verdade à regra de que nenhuma sigla
nasce sem a forma por extenso. O princípio operacional central cabe numa linha do
[modelo operacional](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/operating-model.md):
IA para explorar, propor e escrever; o humano para especificar, decidir e aprovar; testes,
portões e revisão independente para validar. O humano responde pela política, pelos portões e
pelos critérios, não por cada item. É isso que deixa o método escalar sem que a atenção dele
vire o gargalo.

Por que estudar um método só? Porque o Maestro guarda os próprios erros: cada ciclo tem
relatório de qualidade, cada decisão vira um ADR imutável ou uma linha num índice que só
cresce. As falhas que abrem os capítulos estão lá, datadas, e você pode conferir.

## Como ler as quatro partes

O livro tem dezesseis capítulos em quatro partes, mais quatro apêndices [CLAIM-00-009]. A
ordem segue a de um argumento, não a de um ciclo de trabalho.

**Parte I — Por que agentes mudam a engenharia.** O diagnóstico. O
[capítulo 1](../01-a-mudanca-de-unidade-de-trabalho/capitulo.md) mostra que gerar código
ficou barato e que o custo foi para verificar e desfazer, e redefine a unidade de trabalho
como a mudança aceita, não a escrita. O [capítulo 2](../02-o-problema-da-confianca/capitulo.md)
trata a confiança como problema de engenharia: quem responde pelo que um agente fez. O
[capítulo 3](../03-um-humano-muitos-agentes/capitulo.md) encontra o gargalo novo, que é a
atenção do humano que rege, e não a capacidade dos agentes.

**Parte II — Especificar e dar contexto.** A entrada do trabalho. A
[spec como partitura](../04-a-spec-como-partitura/capitulo.md) explica por que a especificação
gera o código em vez de descrevê-lo. A [engenharia de contexto](../05-engenharia-de-contexto/capitulo.md)
detalha as quatro operações sobre a janela finita. [Como dividir o trabalho](../06-como-dividir-o-trabalho/capitulo.md)
diz onde cortar para que agentes em paralelo não colidam, e quando o multiagente piora.
[Papéis e skills](../07-papeis-e-skills/capitulo.md) mostra como dar ao agente um modo de
trabalho, e não só um prompt. [DDD para agentes](../08-ddd-para-agentes/capitulo.md) aplica o
*Domain-Driven Design* (DDD) para impedir que N agentes criem N nomes para a mesma coisa.

**Parte III — Provar e conter.** O controle. A
[arquitetura que se defende](../09-arquitetura-que-se-defende/capitulo.md) recusa a mudança
errada sozinha. Os [quality gates que provam fatos](../10-quality-gates-que-provam-fatos/capitulo.md)
são o capítulo do proxy e do teste de mutação do próprio portão.
[Risco, reversibilidade e autonomia](../11-risco-reversibilidade-e-autonomia/capitulo.md)
transforma a autonomia numa função da irreversibilidade. [Ferramentas, MCP e o ecossistema](../12-ferramentas-mcp-e-o-ecossistema/capitulo.md)
trata o que muda quando o agente age no mundo por ferramentas, com o *Model Context Protocol*
(MCP) como exemplo atual.

**Parte IV — Medir e aprender.** O laço. [Observabilidade e economia](../13-observabilidade-e-economia/capitulo.md)
pergunta quanto custa uma tarefa aceita e onde o custo se perde.
[A organização que aprende](../14-a-organizacao-que-aprende/capitulo.md) mostra como uma
correção vira regra versionada sem que a governança inche; no Maestro, a própria
retrospectiva passou trinta e três ciclos como regra sem gatilho [CLAIM-00-010].
[Validando o Maestro](../15-validando-o-maestro/capitulo.md) faz a pergunta mais difícil do
livro: como testar uma metodologia, e não só um software. [O futuro](../16-o-futuro-da-engenharia-agentica/capitulo.md)
separa o que deve sobreviver à próxima geração de modelos do que é circunstância.

Os apêndices trazem o Maestro numa página, um *benchmark* de governança, o pacote de
reprodução e estudos de campo.

**Três rotas.** Com uma tarde, leia os capítulos 1, 2, 10 e 11. Para implantar um fluxo com
agentes no time, leia a Parte II antes da III, porque portão não salva especificação vaga. Se
a pergunta é "isso funciona mesmo?", comece pelo 15 e pelo apêndice C.

Todo capítulo tem a mesma anatomia: pergunta central, uma falha real e datada contada
**antes** da regra que ela motivou, teoria, alternativas com veredito, o padrão Maestro, um
exemplo executável, um contraexemplo, a evidência, um *checklist* e as referências. O contraexemplo diz quando a regra atrapalha e quanto custa.

## A regra de evidência

Um livro sobre portões que provam fatos precisaria passar no próprio portão. A regra é
simples: **nenhum número no texto sem um identificador de afirmação**, o `CLAIM-NN-NNN` entre colchetes que
você já viu neste prefácio. Cada capítulo tem um arquivo `claims.md` com uma linha por
afirmação: o identificador, o que se afirma, o estado e a evidência reproduzível. A evidência
é um caminho num *commit* fixo do Maestro, um comando que você roda num clone, ou uma
referência publicada. O commit de referência do livro inteiro é o `19823c2`, de 1º de
novembro de 2026. Os links para o Maestro apontam para ele, de modo que o texto não muda de
sentido quando o repositório andar.

O estado é a parte honesta da regra. **Medido** é o que um comando reconta: "o histórico tem
943 *commits*" é um `git rev-list --count` [CLAIM-00-007]. **Observado** é o que está registrado num
artefato e você confere lendo: "o revisor reprovou com cinco bloqueantes" está no relatório
do ciclo 047. **Hipótese** é o que o livro acredita e ainda não demonstrou. Há dez delas, de
H1 a H10, numa agenda de pesquisa: especificação reduz retrabalho; revisão em contexto fresco
acha mais defeito; contexto seletivo reduz custo sem perder qualidade; multiagente só ajuda
com cortes independentes; portão com teste de mutação reduz escapes; e outras cinco do mesmo
tipo [CLAIM-00-011]. Quando um capítulo se apoia numa delas, diz qual, e não a apresenta como
resultado.

Por trás da regra há quatro corpos de texto, cada um com seu ritmo. O método normativo vive
na governança do Maestro e muda por ADR. O *handbook* é a referência de uso, versionada com o
método. Este livro guarda o argumento durável, que deve sobreviver às versões dos dois. A
pesquisa guarda o protocolo e os dados que um dia vão confirmar as hipóteses, ou derrubá-las. Como o Maestro faz hoje está no *handbook*; por que vale fazer está aqui.

A regra de evidência também é imposta, não pedida: um script do repositório do livro confere
que todo identificador citado está registrado e que todo registro é citado.

## O que este livro não é

**Não é manual de ferramenta.** Você não vai aprender aqui a configurar um agente de linha de
comando, um protocolo de ferramentas ou um *kit* de especificação. Essas coisas mudam a cada
trimestre, e o *handbook* do Maestro, por versão, cobre o uso. O teste que o livro aplica a si
mesmo: se o argumento quebra quando se troca o *harness*, o argumento está no lugar errado.

**Não é um livro de *prompt*.** O que importa é o que acontece quando o prompt é ignorado,
ou esquecido na próxima sessão.

**Não é prova de que o Maestro funciona.** O Maestro é o objeto de estudo, não o herói. Os
números do livro vêm, em grande parte, de um único repositório,
num período de pouco mais de três meses [CLAIM-00-007]. Isso basta para mostrar mecanismos e
falhas com data, não para generalizar. Onde o livro só tem uma crença bem fundada, ele a
marca como hipótese e mostra o experimento que a testaria, no
[capítulo 15](../15-validando-o-maestro/capitulo.md).

**Não é um processo para copiar inteiro.** O Maestro tem três raias, da leve (um conserto em
que o próprio *pull request* é o artefato) à de infraestrutura, com portões de
reversibilidade [CLAIM-00-012], justamente porque processo demais numa mudança pequena é
desperdício. Leia
com a pergunta "que parte disso paga o próprio custo no meu time?" e descarte o resto.

## Uma última coisa

O ciclo 047 terminou bem. Os vereditos foram restaurados, as reclassificações viraram linhas
novas com data e nota, e o portão ganhou um campo que obriga a dizer qual é a prova
[CLAIM-00-001]. A correção não veio de um modelo mais inteligente. Veio de um arranjo: um revisor que não escreveu o trabalho, um portão testado
contra as mutações que o derrubaram e um registro que só cresce. Esse arranjo se constrói de
propósito, e é disso que o livro trata.
