# 05 — Engenharia de contexto

> *O agente não esquece aos poucos. Ele esquece de uma vez, e esquece exatamente o que você
> não escreveu.*

Seu time já sabe que um agente de Inteligência Artificial (IA) "fica burro" na terceira hora
de sessão, e já aprendeu o remédio de corredor: limpar a conversa e começar de novo. O
remédio funciona até o dia em que, junto com o ruído, vai embora a regra que segurava o
merge. Este capítulo trata o contexto do agente como o que ele é, um recurso finito que se
gasta, e mostra as quatro operações que um tech lead precisa governar sobre ele: **selecionar**
o que entra, **comprimir** o que já entrou, **persistir** o que precisa sobreviver e
**transferir** para a próxima sessão o que esta aprendeu. Nenhuma das quatro depende da
ferramenta que você usa; todas dependem de onde a informação está escrita.

## Pergunta central

Se a janela de contexto do agente é finita e zera a cada sessão, como decidir o que ele lê,
o que ele descarta e o que tem de sobreviver fora dele?

## Resultado de aprendizagem

Ao final do capítulo, você consegue:

1. **Derivar** de duas premissas (o contexto é finito e degrada; só o escrito sobrevive) por
   que um artefato só se mantém vivo se algo o consome ou se ele é imutável, e usar isso para
   decidir onde cada regra do seu time tem de morar.
2. **Classificar** uma prática de trabalho com agentes (subagente, plano, limpar a sessão,
   revisor novo, memória de sessão, índice de decisões) em uma das quatro operações:
   seleção, compressão, persistência ou transferência.
3. **Medir** a economia de contexto de uma tarefa (o que ela carrega ÷ o que o repositório
   tem) e ler uma economia baixa como sinal de corte errado, e não de janela pequena.
4. **Escrever** uma tarefa que sobrevive à compactação: autossuficiente, com arquivo e
   critério, e com os passos de fechamento em forma que uma máquina confere.
5. **Montar** a cadeia de rastreabilidade de trás para frente (registro do gate → commit →
   ciclo → decisão) e apontar qual elo do seu repositório ainda vive de hábito.

## A falha real

Em 7 de agosto de 2026, uma agente que trabalhava num repositório vizinho ao do Maestro foi
perguntada, ao fim de um ciclo, se tinha seguido o método. Respondeu com honestidade que não
[CLAIM-05-001]. O diagnóstico que ela mesma fez virou a especificação do ciclo 042 do Maestro
([spec 042](https://github.com/GHDaru/maestro/blob/19823c2/specs/042-conformidade-executavel/spec.md)).

O plano dela, o `plan.md`, listava a ordem de implementação e parava em "docs e fitness
verdes". O resto do fechamento, que o método exige (revisão independente em contexto
fresco, revisão de segurança, gate humano), estava escrito na spec e estava, sobretudo, na
memória de trabalho da agente, porque tinha sido conversado. Então a janela encheu e o
*harness* compactou o contexto. A compactação não estraga a informação aos poucos: ela
escolhe o que fica. Ficou o plano, que era o que a agente estava seguindo. A conversa virou
resumo, e o resumo não trazia a cauda. A partir daí, a versão truncada passou a ser a fonte
de verdade, e a agente dirigiu até o *pull request* (PR) obedecendo a ela com fidelidade.
Nenhum passo foi desobedecido. Os passos que faltavam simplesmente tinham deixado de existir
para quem executava.

O Maestro foi medir se aquilo era acidente do vizinho. Não era. Em 35 dos 40 ciclos que o
próprio Maestro tinha rodado até ali, o `tasks.md` (a lista que o executor segue) tinha
perdido o gate humano que o template carregava [CLAIM-05-002]. O método instalado era uma
cópia com perda do método, e o executor seguia a cópia. Nada acusava a perda, porque omissão
não viola nada visível: a checagem de constituição perguntava se o plano *violava* um
princípio, nunca se ele *omitia* um passo.

A segunda falha é cinco dias mais velha e mostra o mesmo defeito do outro lado: não o que se
perde dentro da sessão, mas o que se perde entre uma sessão e a próxima. Em 2 de agosto, o
ciclo 021 instalou o Maestro no próprio Maestro, como teste mais barato possível: se o método
não passa no seu instalador, ninguém deveria confiar nele nos outros. Não passou. A
auto-instalação achou três derivas silenciosas [CLAIM-05-003]. O `AGENTS.md`, o arquivo de
instrução que a maioria dos assistentes lê, estava sem a regra "skills primeiro", que o
`CLAUDE.md` tinha desde o ciclo 011. A skill de jornada viva, criada no ciclo 018, existia no
disco e não era citada na instrução: três ciclos invisível para a IA. E a checagem de
constituição da skill e de dois agentes dizia "I–VII", quando a constituição tinha oito
princípios desde o ciclo 013: oito ciclos de planos sem onde marcar o princípio novo. O
verificador escrito no ciclo saiu com código 1 na primeira execução, com dois achados reais
[CLAIM-05-004] ([relatório do ciclo 021](https://github.com/GHDaru/maestro/blob/19823c2/specs/021-maestro-instalado-no-maestro/qa-report.md)).

O relatório do ciclo nomeou a causa comum: **lista escrita à mão que ninguém compara com o
disco**. Nada daquilo quebrava o build. A IA apenas seguia menos método do que o repositório
declarava ter. A correção foi estrutural e virou o ADR 0013 (o *Architecture Decision
Record*, registro de decisão de arquitetura): `AGENTS.md` passou a ser link simbólico para
`CLAUDE.md`, e o bloco de instrução passou a ser gerado lendo as skills do disco
([ADR 0013](https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0013-instrucao-para-ia-gerada-e-fonte-unica.md)).

As duas histórias são o capítulo em miniatura. Na primeira, a informação certa foi apagada
porque não estava no artefato que o executor consumia. Na segunda, ela existia no disco e não
chegava à próxima sessão porque o canal era uma cópia escrita à mão. Não faltou inteligência
ao agente. Faltou engenharia sobre o que ele lê.

## Teoria

### Dois axiomas, um teorema

O capítulo deriva de duas verdades assumidas, sem prova, na camada de axiomas do Maestro
([axiomas](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/axioms.md)):

- **A3 — o contexto é finito e degrada ao encher.** A janela que o agente lê é limitada, e o
  desempenho cai à medida que ela se enche de ruído. É propriedade física da ferramenta, não
  hábito do operador. Tire A3 e não há razão para fatiar trabalho, limpar contexto ou manter
  um agente estreito.
- **A4 — o que está escrito é o que sobrevive.** O agente começa cada sessão do zero. O que
  não está num artefato não existe para a próxima execução, inclusive o motivo de uma
  decisão. Tire A4 e a documentação vira opcional, porque a memória moraria em outro lugar
  que não o repositório.

Dos dois sai o teorema T5: **um artefato sobrevive por consumo ou por imutabilidade.** Manter
um documento atualizado custa atenção, que é o recurso escasso (A3). Então só dois tipos
sobrevivem: o que alguma coisa a jusante consome e que falha alto quando envelhece, e o que
descreve um momento e por isso nunca envelhece (A4). O Maestro dá a evidência dos dois: o
registro de mudanças vive porque a integração contínua falha sem ele, e os ADRs vivem porque
são imutáveis, nove de dez com um único commit desde que nasceram [CLAIM-05-020].

Dois corolários traduzem isso para o dia a dia de quem rege agentes. O C12 diz que **o que
sobrevive à compactação é o que está num artefato consumido; o resto é apagado, e não
degradado**. É a falha do ciclo 042 enunciada como lei: a cauda não ficou "mais fraca" na
memória da agente, ela sumiu. O C13 diz que **pergunta que se responde de memória será
respondida de memória, e memória relata intenção**. "Estou seguindo o método?" respondido
pelo agente devolve o que ele pretendia fazer, não o que os artefatos mostram. O antídoto do
C13 é trocar a pergunta por um comando, assunto que volta no padrão Maestro.

### Contexto é orçamento, não depósito

A intuição manda alimentar mais: "cole o repositório inteiro, assim ele entende". É o
contrário. Cada beco sem saída, arquivo irrelevante ou tentativa abandonada continua
ocupando lugar e afogando o sinal. Depois de horas de sessão, o agente que começou preciso
repete o que já tentou e esquece a regra dada no começo. Não ficou pior. Ficou cheio.

Há literatura para a parte de A3 que não é intuição. Liu e colegas mostraram, em 2023, que
modelos de linguagem usam mal a informação posta no meio de um contexto longo: o desempenho
é melhor quando o dado relevante está no começo ou no fim, e cai quando está no meio
(*lost in the middle*). Relatórios de engenharia posteriores, como o da Chroma sobre
*context rot* e o da Anthropic sobre engenharia de contexto para agentes, descrevem o mesmo
fenômeno de outro ângulo: mais *tokens* na entrada não significam mais compreensão, e a
atenção do modelo é um orçamento que se gasta. A conclusão prática é a mesma do handbook do
Maestro: **o inimigo não é a falta de contexto, é o acúmulo**.

Para o tech lead, a consequência é de gestão, não de *prompt*: toda prática de trabalho com
agentes é uma decisão de gasto.

### As quatro operações

Há quatro coisas que se fazem com um orçamento de contexto, e cada prática conhecida é uma
delas:

| Operação | A pergunta que responde | Práticas que a realizam |
|---|---|---|
| **Seleção** | O que entra na janela desta tarefa? | agente estreito; subagente que lê em janela própria; tarefa que cita os arquivos de que precisa |
| **Compressão** | O que já entrou pode virar menos? | explorar → planejar → codar (o plano é a exploração destilada); compactação; resumo de subagente |
| **Persistência** | O que precisa existir depois que a janela fechar? | spec, plano, tarefas, relatório; índice de decisões; ADR |
| **Transferência** | Como a próxima sessão recebe o que esta sabia? | arquivo de instrução lido no início; carga de estado no início da sessão; revisor que começa do zero com o diff e o critério |

O handbook do Maestro chegou a essa leitura por um caminho mais curto: quatro práticas que
parecem soltas, explorar-planejar-codar, subagentes, limpar a sessão e revisor em contexto
fresco, contornam a mesma restrição física. Explorar-planejar-codar **comprime** a exploração
no essencial antes de gastar janela com código. O subagente **seleciona**: lê em janela
própria e devolve ao principal só o resultado. Limpar a sessão descarta ruído entre tarefas
não relacionadas. O revisor fresco começa com o orçamento inteiro e vê só o diff e o
critério, o que é uma **transferência** deliberadamente estreita. A taxonomia de quatro
operações vem da base de pesquisa deste livro; ela converge com a que a LangChain publicou em
2025 para agentes (escrever, selecionar, comprimir e isolar contexto), e a diferença de
nomes importa pouco. O que importa é que, com as quatro na cabeça, o tech lead para de
discutir "boas práticas" uma a uma e passa a perguntar qual das quatro operações está mal
feita.

Seleção e compressão acontecem dentro de uma sessão; persistência e transferência
atravessam o corte entre sessões, onde A4 morde. A falha do ciclo 042 foi de compressão; a do
021, de transferência. A raiz foi a mesma: a informação estava escrita, mas não no lugar que
o consumidor seguinte lia.

### O que não se descarta: o contexto integrador

A primeira reação a A3 é cortar. Cortar demais tem nome: **amnésia**. Limpar a sessão a cada
turno esquece o básico; delegar tudo a subagentes produz **ótimo local**, em que cada fatia é
perfeita e o conjunto quebra, porque nenhum executor viu o todo. A disciplina madura não é
"menos contexto", é **contexto certo**: o objetivo, os invariantes e os contratos ficam; os
caminhos abandonados vão embora.

O Princípio V da constituição do Maestro diz isso numa frase: preserve o **contexto
integrador**, a spec, e descarte o ruído
([princípios](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/principles.md)).
O mesmo princípio acrescenta duas regras que pertencem à seleção: paralelizar por contexto
delimitado (*bounded context*), porque é o corte certo que torna a orquestração segura, e usar
a menor autonomia que resolve, com fluxo fixo antes de agente autônomo. A primeira é assunto
do [capítulo 6](../06-como-dividir-o-trabalho/capitulo.md); aqui basta registrar que
**fronteira importa mais que tamanho**. Fatiar por quantidade ("metade dos arquivos para cada
agente") produz duas fatias que não se encaixam. Fatiar por fronteira produz fatias que se
encaixam por construção.

O gatilho de limpar a sessão segue a mesma lógica: é a **troca de papel**, não o turno.
Quem acabou de implementar e vai revisar começa do zero; quem só mudou de arquivo, não.

### Economia medida, não afirmada

A economia que um corte produz pode ser medida: quanto a tarefa carrega dividido por quanto
o repositório tem. Quando a economia sai **consistentemente baixa** ao
fatiar, o diagnóstico quase nunca é "a janela é pequena". É que o corte atravessou uma
costura em vez de segui-la, e o remédio é replanejar o corte, não pedir um modelo com janela
maior.

A ideia veio de um estudo anterior do mesmo autor, o maestro-02, cujo *context-slicer*
reportava a estimativa de *tokens* da fatia ao lado da estimativa do contexto cheio. O Maestro
absorveu o conceito e não a ferramenta, e o próprio cartão de absorção admite que é a absorção
mais fraca das seis vindas daquele estudo: existe texto, não existe portão [CLAIM-05-021]
([cartão 027](https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/ideias/027-economia-de-contexto-medida.md)).
Princípio sem medida é adjetivo.

O próprio handbook caiu nisso antes de corrigir. Até o ciclo 024, o capítulo sobre contexto
tinha uma seção chamada "economia de contexto medida" que não media nada: era a recomendação
de medir, escrita como se fosse prática [CLAIM-05-017]. O ciclo trocou a recomendação por um
número que se reproduz: os agentes do repositório, contados em linhas, com a permissão de
escrita negada por arquivo
([relatório do ciclo 024](https://github.com/GHDaru/maestro/blob/19823c2/specs/024-capitulo-04-padrao-v2/qa-report.md)).
O mesmo ciclo registrou um limite honesto: nem todo papel é acionado em todo ciclo. O
inventário de janelas separadas é maior que o uso, e isso é a regra funcionando, não
desperdício.

### A memória que sobrevive ao reset

Num time humano, parte da memória do projeto fica nas pessoas. Com agentes, **não fica em
lugar nenhum**: cada sessão começa do zero, por desenho, e a rastreabilidade deixa de ser boa
prática de auditoria para ser o único mecanismo de continuidade.

Rastreabilidade tem dois sentidos. **Para frente**, ela responde se a intenção foi construída
e verificada: esta spec virou código, este código tem teste? É cobertura de intenção.
**Para trás**, ela responde de onde veio um sintoma: este comportamento vem de qual mudança,
que atendia qual requisito, decidido por quê? É recuperação, e é o sentido que se otimiza,
porque é o que encurta o incidente. Gotel e Finkelstein já apontavam, em 1994, que o problema
da rastreabilidade de requisitos é sobretudo o do sentido para trás, até a origem da
intenção; com agentes, a origem da intenção é a única coisa que o executor não tem como
reconstruir sozinho.

A forma barata de ter rastreabilidade é por **convenção**, não por ferramenta: a spec
numera, o commit cita o número, o teste nomeia o requisito, o ADR guarda o porquê. Nenhuma
matriz de rastreabilidade, porque matriz que ninguém mantém morre, e rastreabilidade que vira
projeto próprio já morreu. O elo emerge do fluxo quando cada artefato cita o próximo e algum
portão força a citação. O modelo operacional do Maestro escreve a cadeia inteira: intenção →
spec → plano → desenho de interface → tarefas → implementação → testes → revisão →
documentação viva → PR → gate humano, sem ferramenta pesada
([modelo operacional, §9](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/operating-model.md)).

### O regente também tem janela

Há um leitor de contexto que os textos sobre agentes esquecem: o humano que rege. A atenção
dele também é finita, e um documento que mistura tutorial, explicação, receita e referência
gasta o orçamento de quem lê como um *prompt* despejado gasta o do agente. Por isso o guia
editorial do Maestro adota o Diátaxis, de Daniele Procida (quatro tipos de texto que nunca se
misturam na mesma página: tutorial, explicação, como-fazer e referência), e a teoria da carga
cognitiva, de John Sweller, com o modelo *Four-Component Instructional Design* (4C/ID), de van Merriënboer (uma ideia nova por vez,
exemplo resolvido antes do exercício, a tarefa inteira como fio condutor)
([guia editorial do Maestro, §1](https://github.com/GHDaru/maestro/blob/19823c2/docs/livro/guia-editorial.md)).

O ciclo 014 aplicou isso à navegação: cinco trilhas tipadas pelo Diátaxis, quatro percursos
escolhidos pelo tempo que o leitor tem, nenhum link de conteúdo saindo do livro
[CLAIM-05-023]
([spec 014](https://github.com/GHDaru/maestro/blob/19823c2/specs/014-navegacao-cinco-trilhas/spec.md)).
É seleção feita para o humano: quem escreve decide o que o próximo leitor carrega, e o
próximo leitor, agente ou pessoa, paga a conta do que não foi selecionado.

## Alternativas

O ecossistema oferece muitas respostas para "o agente esquece". A tabela compara as que o
Maestro avaliou com fonte primária, mais duas da literatura, pela operação que realizam e
pelo veredito. O veredito do Maestro é um momento datado: cada cartão do ecossistema traz um
gatilho de reavaliação, e mudar de ideia gera linha nova, nunca reescrita do cartão.

| Alternativa | Operação | O que oferece | Veredito |
|---|---|---|---|
| **Despejo de contexto** (colar o repositório; janela maior) | seleção (ausente) | simplicidade aparente | **Rejeitar**. É o anti-padrão 1 do catálogo; A3 diz que mais janela cheia é pior, não melhor |
| **Geração aumentada por recuperação** (*Retrieval-Augmented Generation*, RAG) | seleção | busca o trecho relevante por similaridade | **Útil para corpus grande e alheio**; não substitui o contexto integrador, que não é "o trecho mais parecido" com a pergunta |
| **Memória de sessão em arquivos** (Cline Memory Bank; na pesquisa, MemGPT) | persistência + transferência | um banco que o agente lê no início e atualiza no fim | **Observar**. Duplica a função dos artefatos do ciclo, e carregar memória a cada sessão gasta contexto onde ele falta |
| **Scaffolding de contexto** (context-forge: *command-line interface* (CLI) que gera `CLAUDE.md` por questionário) | transferência | começar rápido | **Descartar**. Produz lista escrita à mão, que é o defeito do ciclo 021 |
| **Contexto do codebase na spec** (*Product Requirement Prompt*, PRP) | seleção + compressão | a spec leva os arquivos, convenções e exemplos de que o agente vai precisar | **Observar**, com gatilho: o primeiro ciclo que rege código de produto alheio |
| **Standards por camada** (Agent OS: standards, produto, specs em arquivos separados) | seleção | reduz deriva em código legado | **Observar**. Para o porte atual, a instrução única já injeta padrão; a pasta prevista nunca existiu |
| **Rastreabilidade pelas *issues*** (Claude Code Project Manager, CCPM) | persistência | o estado mora na plataforma, visível a todos | **Observar**, com gatilho: mais de um humano coordenando por *issues* |
| **"Assuma zero contexto"** (Superpowers) | compressão + transferência | toda tarefa escrita para quem não viu a conversa | **Absorver**. Uma linha no template de tarefas, de maior retorno por caractere |
| **Economia de contexto medida** (maestro-02, *context-slicer*) | seleção | número em vez de adjetivo | **Absorver o conceito**; a ferramenta não veio, e falta portão |
| **Arquivo de instrução do agente** (`AGENTS.md`; template de arquivo de agente do Spec Kit) | transferência | um lugar fixo que o agente lê primeiro | **Adotar**, com uma condição: fonte única e conteúdo gerado do disco |
| **Workflow registrado em banco** (cada passo grava entrada, resumo e saída) | persistência | estado do ciclo consultável por máquina | **Promissor e parcial** no Maestro; ver o padrão abaixo |

Três leituras atravessam a tabela.

A primeira é que **memória de sessão e artefato de ciclo disputam a mesma função**. O cartão
do Memory Bank reconhece o problema (é o C12) e responde que spec, plano, tarefas e relatório
**são** a memória, com um comando que mede se ela sobreviveu; uma segunda camada seria função
duplicada, a menos que a dor apareça medida em sessões de vários dias
([cartão 017](https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/ideias/017-memoria-persistente-de-sessao.md)).
O mesmo raciocínio derrubou o *scaffolding* por questionário, que produz lista escrita à mão
quando o Maestro já gera a instrução lendo o disco
([cartão 019](https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/ideias/019-scaffolding-de-contexto.md)).
O próprio cartão 019 mostra persistência bem feita: o veredito de agosto ("observar") ficou
intacto, e o de hoje ("descartar") entrou numa linha nova de um arquivo de estado. Mudar de
ideia é legítimo; apagar o registro de que se pensava diferente, não.

A segunda é que **duas ideias são genuinamente novas e esperam a dor certa**: o contexto do
codebase empacotado na spec (PRP) e a rastreabilidade pelas *issues* (CCPM). As duas foram
deixadas em "observar" com gatilho explícito, e o motivo é honesto: o Maestro ainda rege o
próprio repositório, que o agente conhece inteiro, e tem um humano só. Num codebase grande e
alheio, descobrir o contexto é a maior parte do custo; com dois humanos, o estado precisa de
um lugar que os dois vejam
([cartão 012](https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/ideias/012-contexto-de-codebase-na-spec.md),
[cartão 014](https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/ideias/014-rastreabilidade-via-issues.md)).
Quem já está nessa situação deve ler o "observar" como "adotar". Os standards por camada do
Agent OS ficaram na mesma posição, e o cartão registra que a pasta prevista nunca existiu
([cartão 004](https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/ideias/004-standards-por-camada.md)).

A terceira é que **o arquivo de instrução é unânime e frágil**. Todo harness moderno lê um
arquivo fixo no início da sessão (`CLAUDE.md`, `AGENTS.md`, regras de projeto), e o Spec Kit
traz um template de arquivo de agente gerado dos planos, que o Maestro mantém sem alteração
desde a versão vendorizada
([template](https://github.com/GHDaru/maestro/blob/19823c2/.specify/templates/agent-file-template.md)).
A fragilidade não está no formato, e sim em ter **duas** cópias, ou uma cópia escrita à mão,
de um fato que já existe no disco.

## O padrão Maestro

O Maestro resolve as quatro operações com uma mistura deliberada de **regra** (texto que o
agente lê), **script** (comando que mede e recusa) e **hook** (gatilho do harness que dispara
sem ninguém pedir). Tudo abaixo é citado na versão `maestro@19823c2`.

### Regra: o princípio, os anti-padrões e a instrução lida antes de tudo

A regra é o Princípio V, já descrito: preservar o contexto integrador, cortar por fronteira,
usar a menor autonomia que resolve. Ela é operada por quatro anti-padrões do catálogo, cada
um com o antídoto
([skill `anti-patterns`](https://github.com/GHDaru/maestro/blob/19823c2/skills/anti-patterns/SKILL.md)):

- **1. Despejo de contexto**: colar a base inteira no *prompt*. Fatie por papel ou tarefa e,
  quando der, reporte a economia.
- **2. Contexto tribal**: intenção que só existe na cabeça do operador. Se não está na spec, o
  agente não sabe, e o próximo humano também não.
- **3. Reset preguiçoso**: o gatilho de limpar a sessão é a troca de papel, não o turno.
- **5. Repetição cega**: rodar o mesmo *prompt* esperando outro resultado. Falhou duas vezes,
  o problema é o *prompt*, o contexto ou a tarefa; mude um deles antes de tentar de novo.

O quinto é o mais subestimado: repetir o pedido numa janela que já contém a tentativa errada
é tentar com mais ruído. A operação certa é selecionar ou comprimir, não insistir.

O veículo da regra é o arquivo de instrução, o `CLAUDE.md`, que a IA lê antes de trabalhar.
Ele importa a constituição, manda consultar as skills antes de agir, descreve o fluxo e as
raias, exige o fechamento do ciclo em `tasks.md` e traz a frase que responde ao C13: se
perguntarem "você está seguindo o método?", **não responda de memória, rode o comando de
conformidade**
([`CLAUDE.md`](https://github.com/GHDaru/maestro/blob/19823c2/CLAUDE.md)). Essa instrução,
mais a constituição que ela importa, é o contexto que toda sessão paga de entrada: 125 linhas
de um e 106 do outro [CLAIM-05-008]. É o custo fixo do método, e por isso ele é curto.

### Seleção: agentes estreitos e skills com gatilho

A seleção no Maestro virou **formato de arquivo**. Cada papel de agente é um arquivo curto,
com escopo, ferramentas e saída declarados. Em `19823c2` são 13 arquivos e 285 linhas, o menor
com 18 e o maior com 36; na primeira medida, no ciclo 024, eram 267 linhas, o menor com 17
[CLAIM-05-006]. Um papel que cabe numa tela não gasta janela com o que não vai usar; o
corolário C8 diz que um agente estreito é mais barato que um capaz. O desenho dos papéis é
assunto do [capítulo 7](../07-papeis-e-skills/capitulo.md).

As skills seguem a mesma economia, com gatilho escrito para quando ela deixar de bastar: o
roadmap deixa em observação o *progressive disclosure* (carregar o corpo da skill só quando
ela se aplica) até o orçamento do que é instalado passar de umas 600 linhas. Quando a linha
foi escrita, as seis skills somavam 419; em `19823c2` somam 472 [CLAIM-05-007]
([roadmap](https://github.com/GHDaru/maestro/blob/19823c2/docs/roadmap.md)). Não adotar
mecanismo de seleção antes que o número peça também é decisão de contexto: cada camada a
mais é algo que alguém precisa carregar para entender o sistema.

### Compressão: o plano, a tarefa de contexto zero e a cauda como token

A compressão começa no fluxo. Na raia plena, a exploração vira **plano** antes de virar
código, e o plano é a exploração destilada no que importa. Depois o plano vira **tarefas**, e
é aqui que a falha do ciclo 042 ensinou mais.

O template de tarefas do Maestro traz a regra que veio do Superpowers: **contexto zero**.
Cada tarefa é escrita para quem não tem contexto nenhum do repositório; tudo de que ela
precisa está nela ou é apontado (arquivo, comando, critério). O Superpowers fala em tarefas
de dois a cinco minutos; o template do Maestro admite de dois a quinze [CLAIM-05-024]
([template de tarefas](https://github.com/GHDaru/maestro/blob/19823c2/.specify/templates/tasks-template.md);
[cartão 024](https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/ideias/024-assuma-zero-contexto.md)).
A tarefa que depende da conversa morre com ela; a regra antecipou o C12.

A resposta do ciclo 042 foi transformar a cauda em **token legível por máquina**. Todo
`tasks.md` passou a carregar, uma linha cada e "nunca apagar", os passos `TAIL:review`,
`TAIL:security`, `TAIL:mutation` e `TAIL:gate`; e o relatório do ciclo tem de trazer a
evidência de cada passo que não for declarado "não se aplica". Os artefatos condicionais
passaram a ser **declarados** (`ART:<nome>=yes|no` com a razão), nunca apenas ausentes. E
um script, `check-conformance.sh`, responde à pergunta "estou seguindo o método?" pelos
artefatos ([ADR 0019](https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0019-conformidade-executavel-e-catalogo-de-artefatos.md)).
Uma nota "lembre da revisão" pode ser resumida pela compactação; um token `TAIL:review`
que um script procura, não.

### Persistência: o índice que só cresce, mantido por script

O Maestro tem dois tipos de memória persistente, e os dois obedecem a T5. A **consumida** é a
pasta do ciclo: spec, plano, tarefas e relatório, que o próximo passo do fluxo lê e que os
scripts conferem. A **imutável** é o registro de decisões: os ADRs e um índice em *JSON Lines*
(*JavaScript Object Notation* (JSON), um objeto por linha, uma decisão cada), em `docs/records/decisoes.jsonl`, com 199 linhas em `19823c2`
[CLAIM-05-009].

O índice existe para a máquina. O agente consulta "as últimas cinco decisões" sem carregar os
ADRs inteiros, o que é seleção a serviço da persistência; a regra que evita a duplicidade
aparente é que **o ADR é a fonte e o índice é o ponteiro**. E o índice é barato de manter
porque ninguém o mantém à mão. O script de promoção para a linha principal escreve a linha do
gate sozinho. O `record-decision.sh` valida que a linha é JSON válido, que tem os campos obrigatórios, que o id é único e que o registro não
aponta para um arquivo ainda cheio de marcadores de pendência, antes de acrescentar
([`record-decision.sh`](https://github.com/GHDaru/maestro/blob/19823c2/scripts/record-decision.sh)).
Corrigir é acrescentar uma linha nova que "fecha" a anterior, nunca reescrever. O
`CLAUDE.md` acrescenta que um *hook* de pré-uso de ferramenta recusa a reescrita do índice,
dos ADRs e dos cartões datados: não é pedido, é imposto.

Duas histórias mostram por que a imutabilidade importa.

Em 12 de outubro de 2026, um ciclo aberto como 064 numa linha paralela foi renumerado para
065 ao entrar na linha de desenvolvimento, porque o 064 já existia. O livro de ponto das
tarefas, também só-acréscimo, já tinha os eventos gravados com o número antigo. Ninguém os
reescreveu: 45 das 52 linhas seguem com o ciclo 064, e uma linha nova no índice de decisões
faz a ponte para o 065 [CLAIM-05-012]
([commit `dda2225`](https://github.com/GHDaru/maestro/commit/dda2225)). Reescrever teria
deixado o arquivo "certo" e destruído a prova de que um dia ele foi outra coisa.

A segunda é o contrário: persistência que falhou por um nome de arquivo. Na jornada do ciclo
072, a captura de 24 de outubro registrava um defeito real, um banner com o horário
impossível "1H60M". Corrigido o defeito, a captura foi refeita no dia 25, e o script grava em
**nome fixo**: a foto nova sobrescreveu a foto do defeito, que hoje sobrevive só no texto
[CLAIM-05-013]
([jornada 072](https://github.com/GHDaru/maestro/blob/19823c2/docs/jornada/072-painel-de-regencia.md)).
A jornada seguinte, a do ciclo 074, escreveu a regra que faltava: correção futura usa nome
novo, nunca sobrescreve a foto que registra o defeito. É a regra do índice aplicada a
imagens.

O passo seguinte ainda está em curso. O ciclo 070 propôs registrar cada rodada como
execução de *workflow* em SQLite, com o *hook* da sessão gravando entrada, resumo e saída de
cada passo. A spec admite implementação parcial: o requisito que recusaria um passo sem a
evidência do anterior está ausente, e o que cobraria o resumo no fim do turno saiu invertido
[CLAIM-05-027]
([spec 070](https://github.com/GHDaru/maestro/blob/19823c2/specs/070-workflow-sqlite/spec.md)).

### Transferência: fonte única, bloco gerado e estado carregado

A transferência tem três mecanismos, um de cada tipo.

A **regra estrutural** é a do ADR 0013: uma instrução só. Em `19823c2`, o `AGENTS.md` é um
link simbólico para o `CLAUDE.md` [CLAIM-05-005]. O ADR pesou e descartou as alternativas:
manter duas cópias e revisar na retrospectiva (foi o que estava valendo, e falhou nas três
derivas [CLAIM-05-003]), um ponteiro de
uma linha "veja o `CLAUDE.md`" (custa um salto de leitura e falha em ferramenta que não segue
referência), gerar o arquivo inteiro por script (tira do humano a parte que é dele). Ficou o
link, com o custo aceito e escrito: no navegador do GitHub, quem abre o `AGENTS.md` vê um
ponteiro, não o texto. Quem lê `AGENTS.md` é máquina, e máquina segue o link.

O **script** é a geração e a conferência. O instalador monta o bloco de instrução lendo
`skills/` (nome e primeira frase de cada skill), e o `check-install.sh` falha se uma skill do
disco não aparece na instrução. Skill invisível passou a ser impossível, e o mesmo comando
roda em todo projeto que recebe o método.

O **hook** é a carga de estado no início da sessão. O harness usado pelo Maestro dispara um
*hook* `SessionStart`, e a saída dele vira contexto que o agente vê. O
`session-state.sh` imprime fatos medidos naquele instante, pelos mesmos scripts que um humano
rodaria: em que branch se está, qual ciclo está aberto, se ele está conforme, que achados
estão em aberto e há quanto tempo. O comentário do script diz por que ele existe: a forma de
falha que o repositório insistia em produzir era o agente respondendo "estou seguindo o
método?" de memória, e respondendo intenção. Nada ali é informação nova. É a mesma
informação, **carregada em vez de lembrada**. O detalhe que importa para este capítulo está
na configuração: o *hook* dispara no início, na retomada, na limpeza e na **compactação** da
sessão [CLAIM-05-018]
([`.claude/settings.json`](https://github.com/GHDaru/maestro/blob/19823c2/.claude/settings.json)).
É o C12 virado mecanismo: depois de cada compactação, o estado do método volta à janela por
um caminho que não depende do resumo.

O *hook* tem sua própria falha. A revisão independente do ciclo 056 achou que, num
repositório sem nenhum commit, o script concatenava um valor e um erro ao ler a branch: um
fato quebrado em duas linhas, injetado em toda sessão de todo repositório novo [CLAIM-05-019]
([`session-state.sh` em `813a469`](https://github.com/GHDaru/maestro/blob/813a469/scripts/hooks/session-state.sh)).
Transferir um fato errado é pior que não transferir, porque ele chega com a autoridade de
"medido agora".

Transferência também é para a pessoa que chega ao projeto, e três ciclos seguidos de agosto
mostram a mesma falha nesse canal. No ciclo 058, medir a documentação para responder "como eu
instalo?" achou três mentiras: uma opção com nome errado na receita, a promessa de "não
sobrescrever" num instalador que passara a atualizar, e um texto de uso que omitia três
opções aceitas. Nenhum portão pegava isso, e a revisão independente reprovou a primeira
entrega com 19 achados [CLAIM-05-014]
([spec 058](https://github.com/GHDaru/maestro/blob/19823c2/specs/058-a-porta-da-frente/spec.md)).
No 059, quem conduz o repositório leu a instrução e não soube o que fazer: faltava escrever a
distinção entre a ferramenta (o clone) e o projeto (o alvo), e faltava instrução para uma IA
que abre o repositório. O ciclo escreveu as duas e criou um portão contra subcomando anunciado
e inexistente, provado com mutações e uma contraprova [CLAIM-05-015]
([spec 059](https://github.com/GHDaru/maestro/blob/19823c2/specs/059-clonei-e-agora/spec.md)).
No 060, a árvore de arquivos pós-instalação foi para um lugar só, no livro, com uma asserção
que a compara com uma instalação feita na hora, provada com oito mutações [CLAIM-05-016]
([spec 060](https://github.com/GHDaru/maestro/blob/19823c2/specs/060-a-arvore-que-nao-mente/spec.md)).

As três têm a anatomia do ciclo 021: **um fato dito em dois lugares sem nada comparando**.

### Rastreabilidade: quatro saltos e o elo que vivia de hábito

O exemplo de rastreabilidade do Maestro percorre a cadeia de trás para frente, sem
ferramenta, e qualquer leitor pode refazê-lo com um clone. Começa por uma linha do índice, o
gate `gate-main-0021b20`. A linha aponta o commit. O commit `12332c3` cita no assunto a spec
021 e o ADR 0013. A spec abre a pasta do ciclo, com os quatro artefatos. E o ADR guarda o
porquê, com as alternativas descartadas e o custo aceito [CLAIM-05-022]
([spec 031](https://github.com/GHDaru/maestro/blob/19823c2/specs/031-capitulo-11-padrao-v2/spec.md)).
Quatro saltos, e cada elo existe porque algum passo do fluxo o obriga: o script de promoção
escreve a linha, o gerador de ciclo cria a pasta, a definição de pronto exige o relatório.

Todos, menos um. Quando o ciclo 031 reescreveu o capítulo de rastreabilidade do handbook, em
2 de agosto, ele nomeou o elo mais frágil: a citação do número da spec no assunto do commit,
o elo mais usado do repositório, era **convenção**. Tinha se mantido por 28 commits só por
hábito, e nenhum portão a exigia [CLAIM-05-011]. O relatório acrescentou uma observação que
vale para qualquer time: nenhum elo tinha se perdido até ali, o que era bom e enganoso, porque
eram 28 commits em sete dias, com o mesmo operador; ausência de falha não é evidência de
robustez quando a amostra é curta e homogênea
([relatório do ciclo 031](https://github.com/GHDaru/maestro/blob/19823c2/specs/031-capitulo-11-padrao-v2/qa-report.md)).
O achado entrou no índice em aberto e foi fechado no dia seguinte pela retrospectiva do ciclo
034, que o transformou em portão: o `check-cycle.sh` passou a exigir a citação em todo commit
à frente da linha principal
([commit `7264fe6`](https://github.com/GHDaru/maestro/commit/7264fe6)). O portão é
consultivo na integração contínua, e seu próprio cabeçalho admite o limite: ele força a
citação, não julga se a citação está certa
([`check-cycle.sh`](https://github.com/GHDaru/maestro/blob/19823c2/scripts/check-cycle.sh)).
No histórico até `19823c2`, 810 dos 943 assuntos de commit citam um ciclo, uma spec ou um ADR
[CLAIM-05-010]. Os que não citam são, em boa parte, anteriores ao portão; o número é o
retrato de uma convenção que virou regra no meio do caminho, e não uma meta.

### O que é regra, o que é script e o que é hook

| Operação | Regra (o agente lê) | Script (mede e recusa) | Hook (dispara sozinho) |
|---|---|---|---|
| Seleção | Princípio V; anti-padrões 1 e 4; agentes estreitos | `check-agents.sh` (forma e permissões dos papéis) | — |
| Compressão | contexto zero no template de tarefas; cauda `TAIL:` | `check-conformance.sh` | `Stop`: confere o ciclo aberto quando o agente vai entregar |
| Persistência | ADR imutável; índice só-acréscimo | `record-decision.sh`; `promote-main.sh` | `PreToolUse`: recusa reescrever o que é histórico |
| Transferência | `CLAUDE.md` como fonte única; "não responda de memória" | `check-install.sh`; bloco gerado do disco; portões de documentação | `SessionStart` (também após compactar): carrega o estado medido |
| Rastreabilidade | spec numerada, commit que cita, ADR que guarda o porquê | `check-cycle.sh` | — |

A base de pesquisa deste livro propõe um comando que ainda não existe no Maestro, um
`inspect-context <ciclo>` que mostraria, para um ciclo, o que cada tarefa carrega, o que
sobreviveria a uma compactação e o que não está ligado a nada. Em `19823c2`, o despachante
`maestro` tem `init`, `check`, `cycle`, `conformance`, `retro`, `promote`, `agents` e
`version`, e nenhum `inspect-context`. O exemplo deste capítulo implementa uma versão de
brinquedo, para mostrar o que um comando assim teria de medir.

## Exemplo executável

O exemplo está em [`exemplo/`](exemplo/README.md) e roda com Python 3 e bash, sem rede. É uma
loja de brinquedo que ganha um cupom de desconto no ciclo 007, com spec, plano, tarefas,
código, índice de decisões, commits e duas cópias da instrução para a IA, passada pelas
quatro operações em doze passos:

```bash
cd livro/05-engenharia-de-contexto/exemplo
bash rodar.sh | diff - saida-esperada.txt   # nenhuma linha de diferença
```

O que a saída mostra [CLAIM-05-025]:

- **Seleção.** A tarefa T2, cortada pela fronteira do cupom e do carrinho, tem economia de
  90% sobre o repositório inteiro. A T4, "renomear `desconto` para `abatimento` em todo o
  código", tem 18%, e o script a reprova com a leitura certa: reveja o corte, não aumente a
  janela. A T3, "ajustar a mensagem do jeito que combinamos na conversa", não cita arquivo.
- **Compressão.** A janela compacta e só o `tasks.md` fica. Somem a revisão em contexto
  fresco, a de segurança e o gate humano (que estavam na spec e na conversa) e o formato da
  data (que só estava na conversa). Com a cauda como token `TAIL:` e a T3 autossuficiente,
  o mesmo cenário passa.
- **Persistência.** O índice aceita a linha nova, recusa id repetido e registro que aponta
  para `<pendente>`, e o comparador reprova a linha 2 editada de "aberta" para "fechada".
- **Transferência.** `CLAUDE.md` e `AGENTS.md` escritos à mão somam quatro derivas contra as
  skills do disco, a anatomia do ciclo 021; com bloco gerado e fonte única, ficam verdes.
- **Rastreabilidade e quadro.** Do gate ao ADR em quatro saltos, com 3 de 4 commits citando
  ciclo ou ADR; e as quatro operações do ciclo numa tela.

A régua de *tokens* é declaradamente grosseira (caracteres divididos por quatro). Ela serve
para a razão entre o selecionado e o total, que é o que o capítulo argumenta, e não para
prever o custo de um modelo. Troque `projeto/` pelo seu repositório e a régua pelo contador
do seu modelo, e o `contexto.py` vira um ponto de partida para o seu próprio
`inspect-context`.

## Contraexemplo

A engenharia de contexto tem custo, e há situações em que ela atrapalha.

**Repositório pequeno, tarefa curta.** Se o repositório cabe com folga na janela e a sessão
dura minutos, selecionar arquivo por arquivo é cerimônia: a degradação só morde quando a
janela enche. O sinal de que passou do ponto é o agente repetindo tentativas já descartadas.

**Reset demais.** Limpar a sessão a cada turno produz amnésia, e o operador passa a colar de
volta, à mão, o contexto que jogou fora: despejo com outro nome. Se você cola o mesmo
parágrafo depois de cada limpeza, ele pertence a um artefato, não à conversa.

**Fatiar demais.** Subagentes com janelas limpas produzem ótimo local: o revisor que só vê o
diff não vê o invariante que o diff quebrou em outro módulo. Um corte que deixa a spec de fora
economiza no lugar errado.

**Memória que duplica artefato.** Um banco de memória de sessão ao lado de spec, plano e
tarefas cria duas fontes para o mesmo fato, e duas fontes divergem. Antes de adotá-lo,
confira se a dor não é um artefato que não está sendo consumido.

**Matriz de rastreabilidade.** A planilha requisito × teste × commit vira projeto próprio,
ninguém a mantém e no primeiro mês ela mente. A convenção barata com portão rastreia melhor;
o custo é admitir quais elos ainda dependem de hábito.

**Economia que não se mede.** O Maestro escreveu "meça a economia de contexto" no seu
princípio e no seu handbook e, até `19823c2`, não tem portão que a meça. Isso não invalida a
ideia; mostra o limite de adotá-la por texto. Se o seu time vai medir economia de contexto,
decida antes o que acontece quando ela sai baixa (quem replaneja o corte, com que gatilho);
sem isso, o número é decorativo.

**Instrução que cresce sem limite.** O arquivo de instrução é o contexto que toda sessão paga
de entrada. Cada regra boa acrescentada a ele é custo fixo multiplicado por todas as sessões.
Quando a instrução passar de uma tela, a pergunta não é "o que mais falta dizer", é "o que
aqui é skill (carregada quando se aplica) e não regra (carregada sempre)".

## Evidência

O que sustenta este capítulo, separado por força.

**Medido** (o comando reproduz o número em `19823c2`): a fonte única da instrução
[CLAIM-05-005], o tamanho de agentes, skills e instrução [CLAIM-05-006, CLAIM-05-007,
CLAIM-05-008], o índice de decisões [CLAIM-05-009], a citação de ciclo nos commits
[CLAIM-05-010], o livro de ponto do ciclo renumerado [CLAIM-05-012], o *hook* após a
compactação [CLAIM-05-018], a cadeia de quatro saltos [CLAIM-05-022] e a saída do exemplo
[CLAIM-05-025].

**Observado** (o Maestro registra; o livro leu o registro): as duas falhas de abertura
[CLAIM-05-001, CLAIM-05-002, CLAIM-05-003, CLAIM-05-004], o elo de commit [CLAIM-05-011], a
captura sobrescrita [CLAIM-05-013], as mentiras e mutações dos ciclos 058 a 060
[CLAIM-05-014, CLAIM-05-015, CLAIM-05-016], a seção que não media [CLAIM-05-017], o fato
quebrado do *hook* [CLAIM-05-019], a base de T5 [CLAIM-05-020], a absorção sem portão
[CLAIM-05-021], as trilhas do ciclo 014 [CLAIM-05-023], o tamanho de tarefa [CLAIM-05-024] e o
estado parcial do ciclo 070 [CLAIM-05-027].

**Hipótese (não medido neste livro).** A hipótese H3 da base de pesquisa diz que **contexto
seletivo reduz custo sem perder qualidade** [CLAIM-05-026]. Ela é a promessa econômica deste
capítulo e não está demonstrada: o Maestro mede o tamanho dos papéis e conta derivas, mas
nunca comparou, com a mesma tarefa, um agente com contexto selecionado e outro com contexto
despejado, medindo custo e taxa de aceitação. O desenho para testá-la está na agenda de
pesquisa do livro (linhas de base com só *prompt*, com spec, com spec e portões, e o método
completo), e é assunto do [capítulo 15](../15-validando-o-maestro/capitulo.md). A literatura
externa citada na Teoria sustenta a degradação com contexto longo (A3), não o ganho líquido de
um método de seleção específico.

Há também uma limitação de amostra que o próprio Maestro declara: um humano, um repositório
que o agente conhece inteiro, e a maior parte dos ciclos regendo o próprio método. As duas
alternativas deixadas em "observar" (contexto na spec e rastreio por *issues*) são exatamente
as que só um codebase alheio e um time maior testariam.

## Checklist

Aplique no seu time, item por item. Cada um se confere por comando ou por inspeção de um
artefato.

- [ ] Existe **um** arquivo de instrução para agentes no repositório. Se a sua ferramenta lê
      mais de um nome (`CLAUDE.md`, `AGENTS.md`, regras de projeto), os outros são links ou
      gerados, e um script falha se o conteúdo divergir.
- [ ] A lista de skills, comandos ou papéis que a instrução cita é **gerada do disco**, e um
      script falha se algo existe no disco e não aparece na instrução.
- [ ] O arquivo de instrução cabe numa tela, e você sabe quantas linhas ele custa a toda
      sessão.
- [ ] Toda tarefa do plano cita os arquivos que toca e tem um critério de pronto. Uma tarefa
      que diz "como combinamos" é reescrita antes de ser executada.
- [ ] Os passos de fechamento (revisão independente, segurança, gate humano) estão **no
      artefato que o executor segue**, em forma que um script encontra, e não só na spec ou
      na conversa.
- [ ] Para as tarefas de um ciclo, você mediu ao menos uma vez a razão entre o que cada uma
      carrega e o que o repositório tem; a de economia mais baixa foi discutida como possível
      corte errado.
- [ ] Limpar a sessão tem gatilho escrito (troca de papel), e quem revisa começa sem o
      contexto de quem implementou.
- [ ] Quando um *prompt* falhou duas vezes, o que muda antes da terceira tentativa é o
      *prompt*, o contexto ou a tarefa, nunca nada.
- [ ] Decisões vivem num registro só-acréscimo, mantido por script que valida o formato e
      recusa id repetido; corrigir é acrescentar.
- [ ] Evidência gerada por script (captura, relatório) nunca é regravada no mesmo caminho;
      cada geração tem nome ou data própria.
- [ ] O estado do processo (ciclo aberto, conformidade, achados) é **carregado** no início da
      sessão por um mecanismo do harness, inclusive depois de compactar, e não lembrado.
- [ ] A pergunta "estamos seguindo o processo?" tem um comando que a responde pelos
      artefatos.
- [ ] Todo commit cita a unidade de trabalho que o originou, e um script cobra isso.
- [ ] Você consegue ir de uma linha de gate até o porquê (commit → ciclo → decisão) em poucos
      saltos, e sabe qual elo do seu repositório ainda vive de hábito.

## Referências

Fontes do Maestro, todas na versão `19823c2` salvo indicação:

- Axiomas, teoremas e corolários (A3, A4, T5, C8, C12, C13):
  <https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/axioms.md>
- Constituição, Princípio V:
  <https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/principles.md>
- Modelo operacional, §9 (rastreabilidade ponta a ponta):
  <https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/operating-model.md>
- Instrução para a IA e link simbólico:
  <https://github.com/GHDaru/maestro/blob/19823c2/CLAUDE.md> ·
  <https://github.com/GHDaru/maestro/blob/19823c2/AGENTS.md>
- ADR 0013 (instrução gerada e fonte única):
  <https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0013-instrucao-para-ia-gerada-e-fonte-unica.md>
- ADR 0019 (conformidade executável e catálogo de artefatos):
  <https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0019-conformidade-executavel-e-catalogo-de-artefatos.md>
- Skill `anti-patterns` (1, 2, 3, 5):
  <https://github.com/GHDaru/maestro/blob/19823c2/skills/anti-patterns/SKILL.md>
- Templates de tarefas e de arquivo de agente:
  <https://github.com/GHDaru/maestro/tree/19823c2/.specify/templates>
- Configuração dos *hooks* e o script de estado de sessão:
  <https://github.com/GHDaru/maestro/blob/19823c2/.claude/settings.json> ·
  <https://github.com/GHDaru/maestro/blob/813a469/scripts/hooks/session-state.sh>
- Scripts `record-decision.sh`, `check-cycle.sh`, `check-install.sh`, `check-conformance.sh`:
  <https://github.com/GHDaru/maestro/tree/19823c2/scripts>
- Índice de decisões e livro de ponto:
  <https://github.com/GHDaru/maestro/blob/19823c2/docs/records/decisoes.jsonl> ·
  <https://github.com/GHDaru/maestro/blob/19823c2/docs/records/tarefas.jsonl>
- Specs e relatórios dos ciclos 014, 021, 024, 031, 042, 058, 059, 060 e 070:
  <https://github.com/GHDaru/maestro/tree/19823c2/specs>
- Jornada do ciclo 072: <https://github.com/GHDaru/maestro/blob/19823c2/docs/jornada/072-painel-de-regencia.md>
- Roadmap (gatilhos de *progressive disclosure*, PRP e CCPM):
  <https://github.com/GHDaru/maestro/blob/19823c2/docs/roadmap.md>
- Cartões do ecossistema 004, 012, 014, 017, 019, 024 e 027:
  <https://github.com/GHDaru/maestro/tree/19823c2/docs/ecosystem/ideias>
- Guia editorial do livro do Maestro, §1:
  <https://github.com/GHDaru/maestro/blob/19823c2/docs/livro/guia-editorial.md>
- Handbook do método, capítulos 04 (fluxo e contexto) e 11 (rastreabilidade), apêndice B
  (Superpowers): cópia congelada em `maestro-handbook/handbook/` deste repositório.

Fontes externas (os endereços não foram reacessados para esta edição; conferir antes de
publicar):

- ANTHROPIC. *Effective context engineering for AI agents*. Engineering blog, set. 2025.
  <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>
- ANTHROPIC. *Building effective agents*. Engineering blog, dez. 2024.
  <https://www.anthropic.com/engineering/building-effective-agents>
- ANTHROPIC. *Claude Code: best practices*. <https://code.claude.com/docs/en/best-practices>
- HONG, K.; TROYNIKOV, A.; HUBER, J. *Context Rot: How Increasing Input Tokens Impacts LLM
  Performance*. Chroma Research, jul. 2025. <https://research.trychroma.com/context-rot>
- MARTIN, L. *Context Engineering for Agents*. LangChain blog, 2025.
  <https://blog.langchain.com/context-engineering-for-agents/>
- AGENTS.md, formato aberto de instrução para agentes. <https://agents.md>
- Cline, documentação do Memory Bank. <https://docs.cline.bot>
- Superpowers. <https://github.com/obra/superpowers>
- Agent OS. <https://github.com/buildermethods/agent-os>
- PRPs (Wirasm). <https://github.com/Wirasm/PRPs-agentic-eng>
- GitHub Spec Kit. <https://github.com/github/spec-kit>
- Diátaxis. <https://diataxis.fr>

Literatura:

- LIU, N. F. et al. *Lost in the Middle: How Language Models Use Long Contexts*. Transactions
  of the Association for Computational Linguistics, v. 12, 2024 (arXiv:2307.03172, 2023).
- LEWIS, P. et al. *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*.
  Advances in Neural Information Processing Systems (NeurIPS), 2020.
- PACKER, C. et al. *MemGPT: Towards LLMs as Operating Systems*. arXiv:2310.08560, 2023.
- GOTEL, O. C. Z.; FINKELSTEIN, A. C. W. *An Analysis of the Requirements Traceability
  Problem*. Proceedings of the First International Conference on Requirements Engineering
  (ICRE), 1994.
- SWELLER, J. *Cognitive Load During Problem Solving: Effects on Learning*. Cognitive
  Science, v. 12, n. 2, 1988.
- VAN MERRIËNBOER, J. J. G.; KIRSCHNER, P. A. *Ten Steps to Complex Learning*. Routledge
  (4C/ID).
