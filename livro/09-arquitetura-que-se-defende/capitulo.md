# 09 — Arquitetura que se defende

> "Um portão que lê um de dois canais não distingue 'nada vazou' de 'não olhei'."
> — spec 054 do Maestro, sexto requisito funcional

Com um time de pessoas, a arquitetura se defendia de um jeito caro e confiável: alguém sênior
lia o pull request e dizia "isso não vai no domínio". Com agentes, o volume de mudança cresce
mais rápido do que qualquer revisor consegue ler, e cada agente começa a sessão sem lembrar o
diagrama que você desenhou no mês passado. Este capítulo é sobre transformar as regras de
arquitetura em coisas que **recusam** a mudança errada sozinhas: uma fronteira declarada num
arquivo, uma seta de dependência medida pela árvore do código, um registro que não aceita ser
reescrito. E sobre o defeito que sobra mesmo assim, que é o portão que não percebeu que o mundo
dele cresceu.

## Pergunta central

Como a arquitetura recusa a mudança errada sem depender de um revisor que leia o diff, e como
saber que ela continua recusando quando o sistema ganha uma porta nova?

## Resultado de aprendizagem

Ao final, você consegue:

1. **Declarar** uma fronteira interna como dado (um arquivo, uma fonte), com invariantes que uma
   máquina decide: cada arquivo tem exatamente um dono, todo caminho compartilhado tem dono, nada
   sai publicado por caminho que ninguém declarou.
2. **Escrever** uma *fitness function* que mede a direção das dependências pela árvore sintática
   do código, e não pelo texto, e **provar** que ela reprova as formas de violação que o texto
   esconde.
3. **Tornar mecânica** uma propriedade que hoje é convenção (só acrescentar, nunca reescrever;
   sessão que sobrevive à queda do servidor), escolhendo entre teste estático, gatilho no banco e
   prova destrutiva.
4. **Perguntar**, a cada ciclo que abre um canal ou um poder novo, quais portões guardavam a porta
   velha, e estendê-los no mesmo ciclo.
5. **Decidir** quando uma fronteira física (outro repositório, outro serviço) se paga, medindo o
   acoplamento antes de mover qualquer arquivo.

## A falha real

Em 14 de agosto de 2026, o operador do Maestro pediu uma coisa pequena: "coloque esta
apresentação no livro, como material" [CLAIM-09-004]. O livro do método é publicado por um
motor próprio, que lê um sumário em JavaScript Object Notation (JSON), converte cada capítulo
Markdown em página e reprova o build se um link interno não resolver. Uma apresentação é um
arquivo HyperText Markup Language (HTML) de tela cheia; não cabia no molde. O ciclo 054 criou
então um terceiro tipo de conteúdo, ao lado de "parte" e "item": o **material**, uma página
autocontida que o livro publica e indexa sem renderizar
([spec 054](https://github.com/GHDaru/maestro/blob/19823c2/specs/054-material-de-apresentacao-no-livro/spec.md)).

O implementador escreveu o canal novo, provou que o build reprovava material ausente e material
colidindo com página gerada, viu o build verde e entregou. A revisão independente, rodada em
contexto fresco com a instrução de refutar, reprovou o ciclo com quatro achados numerados
[CLAIM-09-001]. Dois deles são o assunto deste capítulo.

O primeiro: um material chamado `index.html` **substituía a capa do site**, mantida à mão, e o
build imprimia uma linha de sucesso com a contagem de páginas. O revisor provou comparando o
*hash* do arquivo antes e depois [CLAIM-09-002]. O mapa de colisões do motor só conhecia itens e
materiais; a capa e o sumário nunca tinham sido itens, então nunca estiveram no mapa. Antes do
ciclo, o buraco não existia, porque nenhum arquivo que não fosse Markdown chegava à raiz do
site. O canal novo abriu a porta.

O segundo é pior, porque atinge um portão que existia exatamente para isso. O Maestro tem um
script, `check-boundary.sh`, que garante que nenhum documento voltado para máquina saia no site
voltado para gente sem que alguém o tenha declarado público. Ele lia as páginas publicadas da
lista de partes do sumário. O material era um segundo canal. O revisor publicou
`scripts/interno.html`, um arquivo do lado instalável do repositório, como material: o site
recebeu o arquivo, e o portão disse que estava tudo certo [CLAIM-09-001]. Nas palavras do
relatório, era a falha que aquele script existe para impedir, entrando pela porta que ele não
vigiava
([qa-report 054](https://github.com/GHDaru/maestro/blob/19823c2/specs/054-material-de-apresentacao-no-livro/qa-report.md)).

Nenhum dos dois portões estava errado no dia em que nasceu. O mapa de colisões cobria todas as
páginas que o motor publicava; o portão de fronteira lia o único canal de publicação que existia.
Os dois ficaram errados **sem que ninguém mexesse neles**: o mundo que eles guardavam cresceu e
eles continuaram olhando para a metade antiga. O verde passou a significar "não olhei para lá".

A correção foi estrutural. O mapa de colisões passou a incluir tudo o que existe na raiz do site,
inclusive a capa e o sumário. O portão de fronteira passou a ler os dois canais, com um
comentário no código explicando por que, e seis mutações foram rodadas numa cópia do repositório
e vistas reprovando, uma por modo de falha [CLAIM-09-003]. E o catálogo de anti-padrões do método
ganhou o item 23, "porta nova, guarda antiga não avisada", com um antídoto em forma de pergunta:
*qual era o mundo deste portão, e ele acabou de crescer?*
([anti-patterns](https://github.com/GHDaru/maestro/blob/19823c2/skills/anti-patterns/SKILL.md)).

A falha tem um parente mais antigo, que mostra o mesmo defeito em escala de método. No ciclo 018,
em 1º de agosto, o relatório de qualidade registrou que o modelo operacional do Maestro
prescrevia um agente de experiência de uso (UX, de *user experience*), um artefato
`ux-design.md` e um documento de jornada havia **catorze ciclos**, sem que nada no toolkit os
entregasse [CLAIM-09-005]. Nenhum relatório tinha pegado, porque os checks olhavam sempre para
dentro do ciclo, nunca para a distância entre o que a norma manda e o que o repositório tem. A
arquitetura do método estava desenhada num documento. Não estava em lugar nenhum que recusasse
alguma coisa.

## Teoria

### Uma regra de arquitetura é um critério, e critério sem comando é desejo

O livro deriva este capítulo do teorema T4 do Maestro: *um critério sem comando não é um
critério*. O teorema nasce de dois axiomas. A consequência precisa de dono (A2), e só o que está
escrito sobrevive à sessão seguinte (A4). Logo, "pronto" precisa produzir uma evidência que uma
máquina confirme, ou significa o que o leitor supôs
([axioms.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/axioms.md)).

Uma regra de arquitetura é um critério como outro qualquer. "O domínio não fala com o banco" é
uma afirmação sobre todo commit futuro. Se ela vive num diagrama, num documento de arquitetura ou
na cabeça do tech lead, vale enquanto alguém lembra de olhar. Com agentes, dois axiomas pioram a
situação. O contexto é finito e se degrada conforme enche (A3): o documento de arquitetura pode
simplesmente não estar na janela do agente que está escrevendo o código. E cada sessão começa do
zero (A4): o que o agente "entendeu" na conversa de ontem não existe hoje. A regra que só existe
como prosa depende de três coisas que o trabalho com agentes torna improváveis: o documento ser
lido, ser lembrado e ser comparado com o diff por alguém com tempo.

A literatura de arquitetura já tinha um nome para a alternativa. Neal Ford, Rebecca Parsons e
Patrick Kua chamaram de *fitness function* a verificação objetiva de uma característica de
arquitetura, executada de forma contínua, para que a arquitetura possa evoluir sem perder o que
importa (*Building Evolutionary Architectures*, 2017). O handbook do Maestro resume o efeito em
três linhas: regra de arquitetura que vive só em documento é violada em silêncio; transformada em
teste executável na integração contínua (CI, de *continuous integration*), ela se defende
sozinha; e o preço é um falso senso de segurança, porque a função testa o que foi codificado,
não o que foi esquecido
([handbook, cap. 13, §5.5](../../maestro-handbook/handbook/13-decisoes-de-engenharia.md)).
Guarde a terceira linha. A falha do ciclo 054 é ela, com data.

A evidência que o Maestro registra para T4 não é a de que portões pegam tudo. É o contrário:
**nove defeitos escaparam para a linha principal com o portão verde**, e cada um foi achado
depois por um check que alguém escreveu, nunca por leitura atenta [CLAIM-09-007]. A arquitetura
que se defende não é a que nunca deixa passar nada. É a que transforma cada coisa que passou num
check novo, e por isso não deixa passar a mesma coisa duas vezes.

### Fronteira não é pasta: fronteira é decidível

O primeiro tipo de regra de arquitetura é a fronteira: o que pertence a qual parte do sistema.
A forma usual de declarar fronteira é a estrutura de pastas, e ela tem um defeito que só aparece
com o tempo. Pasta descreve onde o arquivo está, não a quem ele pertence nem quem pode lê-lo.
Quando um arquivo novo nasce num lugar que ninguém previu, a estrutura de pastas não reclama.

O Maestro tratou o problema com uma palavra precisa: a fronteira tem de ser **decidível**. Para
qualquer arquivo rastreado, uma máquina tem de responder, sem julgamento, a qual domínio ele
pertence. O script que verifica isso diz no próprio cabeçalho o que ele não mede: não mede se os
arquivos estão em pastas bonitas; mede que a fronteira é decidível, e lista as três maneiras pelas
quais uma fronteira apodrece sem ninguém perceber
([check-boundary.sh](https://github.com/GHDaru/maestro/blob/19823c2/scripts/check-boundary.sh)):

1. **Arquivo órfão.** Nenhum domínio o reivindica, então ele vai derivar para a metade errada.
2. **Caminho compartilhado sem dono.** Um caminho que dois leitores usam, e que ninguém possui,
   é uma bifurcação com outro nome: as duas cópias divergem.
3. **Publicação sem origem declarada.** Algo chega ao leitor por um caminho que ninguém declarou
   público.

Duas decisões de desenho tornam isso decidível de verdade. A resolução de dono é por **prefixo
mais longo**, o que permite exceções aninhadas sem lista de exceções. E o empate no mesmo
comprimento não é resolvido por ordem de declaração: é marcado como ambíguo e **falha**, porque,
nas palavras do registro de decisão que criou a regra, ambiguidade silenciosa é pior que erro.

Há um efeito colateral que vale mais que o portão. Quando a fronteira é um arquivo que um script
consome, toda pasta nova na raiz do repositório exige uma linha nesse arquivo, no mesmo commit.
O arquivo de fronteira do Maestro mudou oito vezes entre agosto e outubro de 2026, e cada mudança
é uma decisão de arquitetura pequena, registrada no lugar onde ela vale: o painel de coordenação
entrou como domínio de máquina, o protótipo navegável também, a licença e as notas de terceiros
ganharam dono [CLAIM-09-014]. Nenhuma dessas decisões precisou de reunião. Todas precisaram ser
tomadas.

### A seta aponta para dentro

O segundo tipo de regra é a direção das dependências. Alistair Cockburn descreveu a arquitetura
hexagonal, ou de portas e adaptadores, com uma ideia simples: o núcleo da aplicação fala com o
mundo por portas (interfaces que ele define) e o mundo se conecta por adaptadores (implementações
que dependem da porta, nunca o contrário). Robert C. Martin chamou a mesma ideia de regra da
dependência: o código-fonte só aponta para dentro, em direção à política. O *Domain-Driven
Design* (DDD) de Eric Evans acrescenta onde moram as invariantes: no domínio, dentro do agregado,
não na tela, não na rota, não no gatilho.

Para agentes, essa regra tem um valor que ela não tinha para times humanos. O agente escreve onde
for mais curto escrever. Se a rota HTTP (*HyperText Transfer Protocol*) já tem a conexão com o
banco aberta, a validação do pedido vai para a rota. O resultado compila, passa nos testes de
comportamento e espalha a regra de negócio por um lugar onde o próximo agente não vai procurar.
A direção da dependência é o que impede que "mais curto" vire "certo".

E a regra é inteiramente mecânica. Saber se `dominio/pedido.py` importa `sqlite3` não exige
julgamento: exige ler a árvore sintática abstrata (AST, de *abstract syntax tree*) do arquivo.
A versão ingênua, procurar a linha `import sqlite3` no texto, mede o proxy: deixa passar
`from sqlite3 import connect`, deixa passar o import relativo do adaptador, deixa passar
`__import__("sqlite3")`. O [capítulo 10](../10-quality-gates-que-provam-fatos/capitulo.md) trata
essa família de defeitos em detalhe; aqui basta a consequência prática. O teste de arquitetura
tem de ler a estrutura do código, não a sua superfície.

### Mecanismo em vez de convenção

O terceiro tipo de regra é uma propriedade de comportamento que a arquitetura promete: um
registro que só cresce, uma sessão que sobrevive à queda do servidor. Essas promessas costumam
viver como convenção ("ninguém faz `UPDATE` nessa tabela"). A convenção é verdade até o dia em
que o agente, com a melhor das intenções, corrige um registro errado editando-o.

O Maestro registra a passagem de convenção para mecanismo com franqueza, em dois registros de
decisão de arquitetura. O Architecture Decision Record (ADR) é o registro imutável de uma
decisão, com contexto, opções e consequências. O ADR 0025, de 22 de outubro de 2026, aceitou que
ganchos de terceiros gravassem tabelas de fluxo de trabalho com o append-only ainda garantido
por convenção. Dois dias depois, o ADR 0027 tornou a mesma regra mecânica, com duas provas
independentes [CLAIM-09-033]. É a esse tipo de troca que este capítulo chama de arquitetura que
se defende.

A escolha do mecanismo segue uma escada. O mais barato é o **teste estático**: ler o código e
recusar a forma proibida (um `open` em modo de escrita). Depois vem o **mecanismo no próprio
substrato**: um gatilho no banco que aborta o `UPDATE`, independente de quem escreveu o código. E
há propriedades que só se provam por **destruição deliberada**: matar o processo e ver o que
sobrevive. O ADR 0032 do Maestro é desse terceiro tipo, e diz a prova na própria decisão: matar o
servidor e ver as sessões vivas [CLAIM-09-023].

### Boa arquitetura empurra para o lado barato

O handbook do Maestro tem uma observação sobre orquestração que muda o lugar da arquitetura num
time com agentes. Há um espectro entre fluxo fixo (você decide o caminho, previsível, fácil de
depurar) e agente autônomo (o modelo decide na hora, flexível e variável). Quanto melhores as
fronteiras, mais trabalho cabe no lado previsível: investir em fronteira é comprar
previsibilidade, porque o corte deixa de precisar de inteligência quando já está desenhado
([handbook, cap. 05, §5.3](../../maestro-handbook/handbook/05-orquestracao.md)).

A mesma lógica vale para a verificação. Uma fronteira declarada e uma seta de dependência medida
por AST são verificações determinísticas, de custo quase zero, que rodam em cada commit. A
alternativa, pedir a um modelo de linguagem que revise "se a arquitetura foi respeitada", é cara,
variável e, pelo teorema T7 do Maestro, nem chega a ser critério enquanto não tiver uma linha de
base registrada. A arquitetura que se defende tira da revisão humana e da revisão por agente
tudo o que pode ser decidido por máquina, e devolve a elas só o que é julgamento.

### O mundo do portão cresce

A teoria até aqui produz portões que funcionam no dia em que nascem. O que o ciclo 054 mostra é
como eles deixam de funcionar sem que ninguém os toque. O corolário C5 do Maestro diz que um
portão cobre a família inteira ou não cobre nada. O anti-padrão 23 acrescenta o tempo: a família
cresce. Um ciclo concede um poder novo ou abre um canal novo, e o portão que vigiava o canal velho
continua lendo metade do mundo.

A pergunta prática é onde o portão obtém o seu mundo. O portão de fronteira do Maestro, depois da
correção, enumera os canais de publicação **pelo nome**: lê as partes e lê os materiais. Isso
fecha a porta do ciclo 054 e deixa a pergunta aberta para a próxima: se um terceiro canal nascer,
o mesmo portão volta a dizer verde sem olhar. O [exemplo executável](#exemplo-executável) deste
capítulo mostra as três gerações lado a lado e uma quarta forma, que lê o mundo pelo fato (todo
campo que aponta para um arquivo publicado, em qualquer canal) e não pelo nome do canal. Não é a
forma do Maestro; é uma resposta possível à pergunta que o Maestro deixou escrita.

## Alternativas

Há várias maneiras de defender uma arquitetura. Elas não são excludentes, e o veredito abaixo é
sobre o que cada uma resolve quando quem escreve o código é um agente.

| Alternativa | O que resolve | O que não resolve | Veredito |
|---|---|---|---|
| Revisão humana de arquitetura (o sênior lê o diff, ou um comitê aprova) | julgamento: se a fronteira está no lugar certo | não escala com o volume de mudança dos agentes; não lembra o que viu no mês passado | indispensável para desenhar a fronteira, péssima para guardá-la |
| Documento de arquitetura e ADR (Michael Nygard, 2011) | memória: por que a fronteira é assim | não recusa nada; o agente pode não ter lido | necessário; vira forte quando cada ADR aponta para o portão que o executa |
| Instrução ao agente (arquivo de instruções do *harness*: "não importe o banco no domínio") | intenção dita onde o agente lê | instrução não é *enforcement*; some na compactação do contexto | útil como explicação, nunca como guarda |
| Regras de dependência por linguagem: ArchUnit (Java), import-linter (Python), dependency-cruiser (JavaScript/TypeScript), a regra de fronteiras de módulo do Nx, pacotes `internal/` do Go, Packwerk (Ruby) | direção de dependência entre módulos, com mensagens boas e manutenção de terceiros | dono de arquivo, canal de publicação, propriedades de comportamento | adote se a sua linguagem tem; não substitui a fronteira decidível |
| `CODEOWNERS` do GitHub | quem revisa cada caminho | não falha em arquivo órfão nem em dupla reivindicação; roteia revisão, não decide fronteira | complementar; é fronteira de pessoas, não de artefatos |
| Fronteira física (repositórios ou serviços separados) | isolamento forte, ritmos independentes | custa atomicidade, cobertura de link e evidência; só se paga com acoplamento baixo medido | meça antes (ver o padrão Maestro); quase sempre comece pela fronteira interna |
| Revisão de arquitetura por modelo de linguagem (*LLM-as-judge*, de *large language model*) | casos que exigem leitura de intenção | não é determinística; sem linha de base, não é critério | use para o que é julgamento, depois de esgotar o que é mecânico |

Duas observações sobre a tabela. Primeiro, as ferramentas de regra de dependência são o caminho
mais curto para a seta: se você tem Java, uma regra do ArchUnit substitui o portão de
dependências do exemplo deste capítulo, com manutenção de terceiros. O que nenhuma delas faz é a fronteira decidível de arquivos e canais,
que é uma propriedade do repositório, não do grafo de módulos. Segundo, a fronteira física é a
alternativa que mais parece "arquitetura séria" e a que mais custa desfazer. A lei de Conway
(1968) lembra que a estrutura do sistema tende a copiar a estrutura de comunicação de quem o
constrói; num time de um humano regendo muitos agentes, essa estrutura raramente justifica dois
repositórios. O Maestro mediu isso, e é a história mais instrutiva do capítulo.

## O padrão Maestro

O Maestro resolve a pergunta deste capítulo em camadas: **regra** (o que está escrito),
**script** (o que a máquina roda), **gancho** (o que roda queira o agente ou não) e **prova** (a
mutação ou a destruição que mostram que o portão acusa). Todas as citações são da versão
`maestro@19823c2`.

### Regra: a fronteira deriva do leitor

A fronteira interna do Maestro deriva do corolário C10: *o que é instalado é lido por máquinas; o
que é publicado é lido por pessoas*
([axioms.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/axioms.md)). O
repositório serve aos dois leitores desde a fundação: agentes leem o método instalável (agentes,
skills, scripts, templates, governança) e pessoas leem o livro. Os dois domínios estão declarados
num arquivo só,
[`boundary.json`](https://github.com/GHDaru/maestro/blob/19823c2/boundary.json): `toolkit`
(leitor: máquina) e `guide` (leitor: humano), mais uma lista de caminhos **compartilhados** que o
toolkit possui e o site do livro publica. O próprio arquivo explica o que a declaração compra:
quem edita esses caminhos sabe que a edição é pública.

A regra de pilha e camadas está no
[ADR 0028](https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0028-react-no-front-e-back-hexagonal.md),
aceito em 29 de outubro: React com TypeScript no front, Python hexagonal no back (domínio,
aplicação, portas, adaptadores), servidor HTTP da biblioteca padrão com tabela de rotas,
invariantes no domínio e nunca na rota nem no gatilho, e **nenhuma pasta nova de primeiro nível**.
O ADR escreve os gatilhos para rever a decisão, em vez de deixá-la eterna: mais de 30 rotas,
validação repetida em três ou mais rotas, um segundo cliente da interface de programação (API, de
*application programming interface*) ou uma *thread* presa no teste de caos levam ao FastAPI, e
**só no adaptador HTTP**; mais de oito rotas consumidas pelo React levam a um gerador de contrato
[CLAIM-09-016]. A regra do quando reabrir é parte da arquitetura.

Essas decisões não saíram de uma pessoa. Em 28 de outubro, seis especialistas em contexto
fresco, três de experiência de uso e três de arquitetura de backend, com réplica cruzada,
fecharam a síntese do ciclo 076 [CLAIM-09-017]. Algumas linhas dessa síntese são regras de
arquitetura que um tech lead pode copiar quase literalmente: porta só onde há dois adaptadores
hoje, **contando o falso de teste**; cada porta com um teste de contrato que roda contra o falso e
contra o real; relógio como argumento, nunca lido do ambiente; migrações numeradas com um único
ponto de migração para servidor, ganchos e ferramentas
([síntese das bancas](https://github.com/GHDaru/maestro/blob/19823c2/specs/076-padroes-de-engenharia-e-react/sintese-das-bancas.md)).
A primeira regra é You Aren't Gonna Need It (YAGNI) aplicado a portas: porta com um adaptador só
é cerimônia, e a regra diz como contar.

E por que o ciclo 076 precisou de padrões? Porque o protótipo do ciclo 074 provou o caminho em
HTML e JavaScript soltos, e a banca mediu o resultado: vinte telas, três números diferentes para
a mesma pergunta ("o que precisa de mim": 3, 1 e 4) e nove desenhos diferentes de "em que estado
está" [CLAIM-09-018]. Em 30 de outubro, o crítico que anda pelo build real reprovou o fecho do 074
com seis jornadas falhando e uma causa única: telas e avisos afirmavam um efeito que o estado não
tinha registrado, porque cada tela lia a sua fixture, e não um estado único [CLAIM-09-019]. É uma
falha de arquitetura que aparece como falha de usabilidade. A decisão foi corrigir no protótipo só
o que era local e **transferir** a coerência de estado entre telas para o 076, onde ela ganharia
o lugar certo: o domínio, com o número nascendo uma vez
([decisoes.jsonl](https://github.com/GHDaru/maestro/blob/19823c2/docs/records/decisoes.jsonl),
`decisao-074-fecho-corte-e-transferencia`).

O ciclo 076 respondeu em três frentes que a
[spec](https://github.com/GHDaru/maestro/blob/19823c2/specs/076-padroes-de-engenharia-e-react/spec.md)
trata como uma só. Escrever **como se constrói aqui**, em documentos instaláveis de padrões de
engenharia, de tipos de mudança e de carregamento de contexto para a inteligência artificial, para
que nenhum agente precise deduzir a pilha lendo o código. Dar nome ao **tipo de mudança**, um eixo
ortogonal à raia (que mede só o risco): tela, regra de domínio, adaptador, esquema de dados,
infraestrutura, documentação, refatoração ou correção. O tipo decide o que o agente carrega: quem
mexe em adaptador recebe o contrato da porta; quem mexe em domínio, o mapa do domínio. E passar a superfície para React, com **um componente por papel semântico** do catálogo
em vez de N desenhos do mesmo cartão. O protótipo do 074 não é tocado: vira especificação visual.
É a mesma lição da fronteira, aplicada à tela. O padrão que vive no olho de quem escreve volta a
se espalhar no ciclo seguinte; o padrão que vive num componente único e num documento que o
agente carrega não precisa ser lembrado.

### Script: o que a máquina roda

**A fronteira decidível.**
[`check-boundary.sh`](https://github.com/GHDaru/maestro/blob/19823c2/scripts/check-boundary.sh)
lê `boundary.json`, lista os arquivos rastreados pelo Git e verifica as três invariantes:
todo arquivo com exatamente um domínio; todo caminho compartilhado possuído pelo toolkit; toda
página publicada vinda do guia ou de um caminho compartilhado declarado. Na versão citada, o
portão classifica 1.235 arquivos rastreados, 1.139 do toolkit e 96 do guia, com seis caminhos
compartilhados e 39 páginas publicadas, 29 do guia e 10 compartilhadas [CLAIM-09-013]. Ele roda
na CI no laço bloqueante de quinze scripts estruturais [CLAIM-09-015]. O comentário no meio do
código conta a história do ciclo 054 para quem for mexer nele depois: o canal de materiais ficou
invisível ao portão por exatamente um ciclo.

**A seta de dependência.** O teste
[`test_import_fronteira.py`](https://github.com/GHDaru/maestro/blob/19823c2/painel/tests/test_import_fronteira.py)
nasceu na primeira tarefa do ciclo 075, em 29 de outubro, e se descreve como "a fronteira medida
por AST, não por leitura". Ele percorre todo módulo do domínio, recusa qualquer import de uma
lista de doze módulos de entrada e saída (I/O) — sistema de arquivos, banco, rede, subprocesso — e
recusa que os dois contextos delimitados do domínio, Comunicação e Coordenação, importem um ao
outro [CLAIM-09-020]. Um segundo teste,
[`test_esqueleto.py`](https://github.com/GHDaru/maestro/blob/19823c2/painel/tests/test_esqueleto.py),
verifica a direção das camadas (o domínio não conhece o adaptador, a porta também não) e que
nenhuma pasta nova nasceu na raiz, com a mensagem de erro dizendo o custo: pasta na raiz custa
uma linha em `boundary.json`. Os dois portões se conhecem.

**O contrato da porta.** O teste da porta `Transporte` é uma única bateria de casos que roda
**contra os dois adaptadores**, o SQLite real e o falso de teste. O cabeçalho do arquivo diz por
quê: se o falso for mais frouxo que o real, o teste mente [CLAIM-09-021]. É a regra da síntese
virando executável, e é a resposta a uma armadilha comum dos testes com dublês: o dublê aceita o
que a produção recusa, e a suíte verde descreve um sistema que não existe.

**O registro que só cresce.** O
[ADR 0027](https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0027-registro-da-fila-e-append-only-mecanico.md),
de 24 de outubro, decidiu que o registro da fila de decisões do painel é append-only **mecânico**,
com duas provas. No arquivo: o adaptador sempre abre em modo de acréscimo, sob uma trava, e um
teste estático lê a AST do adaptador e recusa qualquer `open` que reescreva ou trunque. No banco:
gatilhos em linguagem SQL (*Structured Query Language*) que abortam `UPDATE` e `DELETE` nas
tabelas de fluxo, com uma exceção estreita (o fechamento de um passo só pode preencher as colunas
de saída, e só quando estão vazias). A emenda do próprio ADR registra o que a implementação
ensinou: eram oito gatilhos, não quatro, porque o banco exige um gatilho por evento por tabela, e
a fila também precisava da exceção estreita para não quebrar três testes de um ciclo anterior
[CLAIM-09-022]. A emenda foi acrescentada abaixo do texto original, que não foi reescrito.

**Os papéis que julgam não escrevem.**
[`check-agents.sh`](https://github.com/GHDaru/maestro/blob/19823c2/scripts/check-agents.sh)
verifica invariantes estruturais dos subagentes: a contagem esperada, o campo de nome e, a parte
de segurança, que os três agentes somente-leitura (revisão, segurança e guardião do processo) não
tenham ferramentas de escrita [CLAIM-09-026]. É arquitetura no sentido mais literal: a separação
entre quem executa e quem verifica é configuração, e a configuração é verificada. No ciclo 018,
quando um papel novo elevou os agentes a treze, esse script falhou sozinho, porque esperava doze;
o relatório chama isso de efeito colateral bem-vindo, a fitness function anterior funcionando como
projetada [CLAIM-09-006]. Repare no tipo de alarme: não acusou um erro, acusou uma **mudança de
mundo** que ninguém tinha anunciado ao portão. Foi o oposto do ciclo 054, e é o comportamento que
se quer.

**A norma comparada com o disco.** A resposta do ciclo 018 à falha dos catorze ciclos foi um
portão que compara a norma com o toolkit: todo papel prescrito tem agente, todo artefato essencial
tem template. A do ciclo 021, em 2 de agosto, foi instalar o Maestro no próprio Maestro. Não
passou: três derivas silenciosas da mesma família, listas escritas à mão que ninguém comparava com
o disco, entre elas o princípio VIII da constituição sem onde ser marcado no plano havia oito
ciclos; e, num repositório vazio, a instalação recém-copiada falhava o check com sete achados até
receber o bloco de instruções gerado das skills do disco [CLAIM-09-024]. Nasceu ali um verificador de instalação e a fonte única das instruções:
o arquivo lido por um *harness* e o lido pelos outros passaram a ser um só, com o segundo como
link simbólico. Cópia escrita à mão diverge, diz o registro; a pergunta não é se, é quando.

### Gancho: o que roda queira o agente ou não

Scripts rodam quando alguém os chama, na CI ou à mão. A camada de ganchos do *harness* roda antes
da ação. No Maestro, um gancho `PreToolUse` recusa a reescrita do que o método guarda como
história (o corpo de um ADR, o índice de decisões, os cartões de ideia datados). É a forma mais
forte de arquitetura que se defende, porque recusa **antes do dano**, e tem um limite declarado
pelo próprio método: comandos de shell não são guardados para essas regras, e uma edição em massa
por `sed` alcança o que a guarda não vê. O [capítulo 12](../12-ferramentas-mcp-e-o-ecossistema/capitulo.md)
trata a camada de ganchos; aqui basta a lição: diga o que o guarda não vê, para que ninguém
confunda o silêncio dele com proteção.

### Prova: medir antes de mover

A história que mais ensina sobre fronteiras no Maestro é a de uma divisão que não aconteceu.

Em 6 de agosto, o operador decidiu dividir o projeto em dois repositórios: o instalável e o livro.
O corte tinha derivação pronta no corolário C10. O ciclo 038 foi declarado na raia de
infraestrutura, a de irreversibilidade alta, e por isso **não moveu nenhum arquivo**
([spec 038](https://github.com/GHDaru/maestro/blob/19823c2/specs/038-divisao-em-dois-repositorios/spec.md)).
Primeiro mediu: o site publicava 37 páginas, nove nascidas do lado instalável; o livro
atravessava a fronteira em 35 links; e citava 22 caminhos de código como evidência
[CLAIM-09-008]. O
[ADR 0017](https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0017-divisao-em-dois-repositorios.md)
registrou o corte: 282 arquivos para o toolkit, 79 para o guia [CLAIM-09-009]. A fatia 1 entregou
só o critério: `boundary.json` e `check-boundary.sh`, escrito **antes** da classificação e visto
falhando em cada uma das três invariantes, com 361 arquivos classificados [CLAIM-09-012]. O
custo de desfazer, registrado no relatório, era apagar dois arquivos [CLAIM-09-032].

Antes do gate da fatia 2, o operador pediu a comparação com prós e contras, e a medição mudou a
decisão. Só 18 de 86 commits, 20%, tocavam substância dos dois lados; o número bruto dava 40%, mas
changelog, roadmap, registros e specs são tocados por toda entrega por obrigação, não por
acoplamento. O instalador copiava zero arquivos do lado do livro. O histórico tinha zero versões
fechadas e zero tags, ou seja, o argumento "cada um libera no seu ritmo" descrevia algo que nunca
tinha acontecido [CLAIM-09-010]. Contra os ganhos reais (contexto do agente, peso de clone,
dependências isoladas), quatro perdas mensuráveis: a atomicidade dos commits acoplados; 252 links
relativos verificados caindo para 35 externos sem verificação; a evidência de código do livro
ficando sem portão possível; e um mecanismo de espelho novo, com defasagem própria
[CLAIM-09-011].

O [ADR 0018](https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0018-fronteira-interna-em-vez-de-divisao.md)
datado do mesmo 6 de agosto, superou o 0017 sem editar o corpo dele [CLAIM-09-010]: um repositório, com a fronteira
**interna**. O arquivo de fronteira deixou de descrever dois repositórios e passou a declarar dois
domínios. As três invariantes continuaram, e a terceira mudou de razão, não de valor: deixou de
proteger contra perder páginas no dia da mudança e passou a proteger contra o site publicar um
documento de máquina que ninguém declarou público. Foi exatamente essa invariante que o ciclo 054
quebrou, oito dias depois, pelo canal novo [CLAIM-09-004]. E o ADR escreveu três gatilhos observáveis para
reabrir a questão: o guia ganhar ciclo de vida próprio, aparecer quem contribua só com o livro,
ou alguém reclamar do peso da instalação [CLAIM-09-031].

Há três lições nesse par de ADRs. A fronteira valia **independentemente** da divisão: o ganho
principal da fatia 1 não dependia da fatia 2. A medição que reverte uma decisão é o comportamento
que se quer, e o par 0017 → 0018 fica no repositório para mostrar isso. E a ordem importa: quem
move primeiro e conserta os links depois aposta numa operação de irreversibilidade alta sem
reversibilidade engenheirada. O próprio ADR 0017 cita o precedente menor: no ciclo 033, uma troca
de texto em massa para renomear um arquivo casou também dentro do nome de um registro de decisão
que não foi renomeado e criou um caminho inexistente em catorze arquivos, achado pelo portão de
links, não pela leitura [CLAIM-09-025]. Daí o anti-padrão 18 e a regra de checar links no
repositório inteiro depois de qualquer renome, não só nas páginas publicadas.

### Prova destrutiva: o dono do processo

O
[ADR 0032](https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0032-dono-do-processo-fora-do-servidor-web.md)
decide uma propriedade de arquitetura que nenhum teste estático pega: quem é o dono do processo
das sessões de agente. Se o servidor web do painel for o dono, um `Ctrl+C` mata todas as sessões.
O ADR rejeita o servidor como dono, rejeita um daemon próprio (um segundo produto para manter) e
decide por um hospedeiro separado, destacado do grupo de processos, que conversa com o painel pelo
banco. O mecanismo que mataria a sessão junto com o pai fica **proibido** no texto, e a primeira
prova é escrita na decisão: matar o servidor e ver as sessões vivas [CLAIM-09-023]. Para o tech
lead, a forma vale mais que o caso: quando a propriedade é de ciclo de vida, o portão é um teste de
caos pequeno e explícito, não uma leitura de código.

## Exemplo executável

A pasta [`exemplo/`](exemplo/README.md) traz um projeto de brinquedo com dois leitores (um
servidor em camadas e um livro publicado) e sete portões de arquitetura em Python 3, sem
dependência externa. Um harness prova cada portão por mutação: roda no projeto como está (tem de
ficar verde), em três fixtures legítimas (o mundo certo de um jeito incômodo, que nenhum portão
pode reprovar) e em quinze mutações divididas por família (o mundo quebrado de propósito, que o
portão da família tem de reprovar) [CLAIM-09-027]. Cada mutação roda numa cópia temporária; o projeto nunca é
alterado.

| Família | Portões | O que as mutações quebram |
|---|---|---|
| fronteira | um canal (a forma anterior ao ciclo 054), dois canais (a correção pelo nome), fato (todo campo `arquivo`, em qualquer canal) | arquivo órfão, dupla reivindicação, compartilhado sem dono, arquivo do toolkit publicado pelo 1º, 2º e 3º canais |
| dependências | texto (procura `import <módulo>`), fato (lê a AST) | `import sqlite3`, `from sqlite3 import connect`, import relativo do adaptador, `__import__`, porta importando adaptador |
| registro | fato | modo `"w"`, `mode="w"` por palavra-chave, `truncate()` |
| portas | fato | a porta perde o adaptador falso |

Rode:

```bash
cd livro/09-arquitetura-que-se-defende/exemplo
python3 provar.py     # no Git Bash do Windows, use python
```

O resultado [CLAIM-09-027]: sete portões provados, quatro portões e três decorações, e o script
sai com código 0, porque é exatamente isso que o capítulo afirma. O que observar:

- No projeto como está, os sete ficam verdes. Rodados só no caminho feliz, o portão de um canal e
  o de dois canais são indistinguíveis do portão bom.
- O portão de um canal mata quatro de seis mutações e deixa viver o arquivo do toolkit publicado
  como material. É o ciclo 054, reproduzido.
- O portão de dois canais, a correção pontual, mata cinco de seis e deixa viver o terceiro canal.
  Corrigir a porta que foi arrombada não fecha a próxima.
- O portão de dependência por texto mata uma de cinco mutações: só a forma literal
  `import sqlite3`. O import relativo do adaptador e o import do adaptador pela porta passam.
- A fixture legítima `"a+"` (ler e acrescentar) fica verde no portão do registro. Um portão que a
  reprovasse seria mais estrito do que a regra, e portão de falso vermelho se aprende a ignorar.

O exercício do [README](exemplo/README.md) pede para você acrescentar um canal novo ao sumário do
projeto e rodar de novo, antes e depois de mudar o portão. É o anti-padrão 23 em cinco minutos.

## Contraexemplo

Arquitetura que se defende tem custo, e há lugares onde ela atrapalha.

**A fronteira cobra pedágio em cada pasta nova.** As oito mudanças de `boundary.json`
[CLAIM-09-014] são oito momentos em que alguém criou uma pasta e o portão ficou vermelho até a
declaração entrar. Num repositório de exploração, com pastas nascendo e morrendo toda semana, esse
pedágio pode custar mais do que protege. Se o seu repositório tem um leitor só e nada é publicado
a partir dele, a terceira invariante não tem o que guardar, e as outras duas são uma estrutura de
pastas com burocracia.

**A porta com um adaptador.** A síntese do ciclo 076 é explícita: porta só onde há dois
adaptadores hoje, contando o falso. O erro inverso, hexagonal como estética, produz interfaces com
uma implementação, contêineres de injeção e classes de caso de uso que ninguém troca. É
complexidade além do necessário, e o princípio VII do Maestro manda justificar por escrito ou
remover.

**O protótipo que tinha o direito de ser solto.** O protótipo do ciclo 074 foi escrito em HTML e
JavaScript soltos de propósito, para provar o caminho rápido, e provou. A falta de estado único
virou falha só quando o protótipo foi julgado como produto [CLAIM-09-019]. Pôr hexagonal,
contratos e teste de AST num protótipo de descarte seria pagar a defesa de algo que ninguém ia
manter. A regra útil não é "defenda sempre"; é "defenda a partir do momento em que o código vai
sobreviver à semana", e transfira o que o protótipo aprendeu, como o 074 fez.

**O falso senso de segurança.** O portão testa o que foi codificado, não o que foi esquecido. O
portão de dependência do exemplo pega `__import__("sqlite3")`, mas não pega
`importlib.import_module("sqlite3")`, nem uma função do domínio que recebe uma conexão aberta por
argumento e a usa. Fitness function verde não é arquitetura correta; é ausência das violações que
alguém pensou em proibir. A única defesa contra isso é a que o capítulo inteiro descreve: cada
escape vira mutação nova no portão.

**O portão mais estrito que a regra.** Se o portão do registro reprovasse `"a+"`, ele estaria
certo pela letra (o `+` permite leitura e escrita) e errado pelo fato (em modo de acréscimo, toda
escrita vai para o fim). O resultado seria um portão contornado por quem precisa ler e acrescentar
no mesmo arquivo. O Maestro registrou a mesma lição no changelog do ciclo 074, sobre outra régua: régua mais
estrita que o requisito acusa o produto
([CHANGELOG.md](https://github.com/GHDaru/maestro/blob/19823c2/CHANGELOG.md)).

**A cerimônia que a fronteira não eliminou.** O ADR 0018 lista as perdas de não dividir e uma
delas é honesta: o verificador de idioma continua existindo como fronteira interna, uma cerimônia
que a separação teria eliminado. Escolher a fronteira interna não é de graça; é trocar uma perda
maior por uma menor, com o gatilho para reabrir escrito.

## Evidência

O que sustenta o capítulo, separado pelo estado de cada afirmação. A tabela completa, com a
evidência reproduzível de cada claim, está em [`claims.md`](claims.md).

**Medido** (reproduzível por comando na versão citada): a classificação atual da fronteira, com
1.235 arquivos e 39 páginas [CLAIM-09-013]; as oito mudanças do arquivo de fronteira, cada uma
declarando um caminho novo [CLAIM-09-014]; o laço bloqueante de quinze scripts na CI
[CLAIM-09-015]; a lista de doze módulos de I/O proibidos no domínio [CLAIM-09-020]; os três agentes
somente-leitura e a contagem esperada de treze [CLAIM-09-026]; e a saída do exemplo executável
[CLAIM-09-027].

**Observado** (registrado em relatório, spec, ADR ou índice de decisões do Maestro): a falha do
ciclo 054 e a sua prova por mutação [CLAIM-09-001 a CLAIM-09-004]; a norma sem executor por
catorze ciclos [CLAIM-09-005] e o alarme de contagem [CLAIM-09-006]; os nove escapes com verde
[CLAIM-09-007]; a medição e a reversão da divisão [CLAIM-09-008 a CLAIM-09-012, CLAIM-09-031,
CLAIM-09-032]; as decisões de arquitetura do 076 e a falha que as motivou [CLAIM-09-016 a
CLAIM-09-019]; o teste de contrato contra dois adaptadores [CLAIM-09-021]; o append-only mecânico
[CLAIM-09-022]; o dono do processo [CLAIM-09-023]; a auto-instalação [CLAIM-09-024]; e o renome em
massa [CLAIM-09-025].

Uma divergência de fonte, registrada para não se perder: o handbook do Maestro atribui ao ciclo
019 o alarme do `check-agents.sh` quando os agentes passaram de doze para treze; o relatório de
qualidade do ciclo 018 é quem registra o fato. O livro segue o relatório, que é a fonte primária
[CLAIM-09-006].

**Hipótese** (não medida; agenda da pesquisa). Duas hipóteses da base de pesquisa do livro tocam
este capítulo. A H4 diz que multiagente só ajuda com cortes independentes [CLAIM-09-028]; a
fronteira decidível e a seta de dependência são o que torna um corte independente verificável, mas
o Maestro não mediu o efeito delas sobre o retrabalho de agentes paralelos. E o benchmark de
governança proposto na agenda (o ASEG-Bench) tem um caso exatamente deste capítulo, o GOV-003,
"dependência proibida" [CLAIM-09-029]: dar ao agente uma tarefa cujo caminho mais curto viola a
seta, com e sem o portão, e contar quantas vezes a violação chega ao merge. O desenho está no
[capítulo 15](../15-validando-o-maestro/capitulo.md). Até lá, o que os casos acima mostram com
segurança é qualitativo: portões de arquitetura que não foram provados por mutação, ou que não
foram estendidos quando o mundo cresceu, deixaram passar exatamente o que existiam para barrar.

O limite habitual vale aqui também. São casos de um repositório e de um operador, muitos achados
por agentes que ele rege. Estão datados e com commit; servem como estudo de caso, não como
estimativa de frequência.

## Checklist

Aplique no seu repositório, portão por portão.

- [ ] A fronteira entre as partes do repositório está declarada num arquivo só, consumido por um
      script; nenhum script carrega lista própria de caminhos.
- [ ] Todo arquivo rastreado tem exatamente um dono; arquivo órfão e dupla reivindicação reprovam,
      e empate na resolução de dono é erro, não ordem de declaração.
- [ ] Todo caminho lido por dois públicos está declarado como compartilhado, com dono.
- [ ] Toda página publicada (site, pacote, imagem de contêiner) vem de um caminho declarado
      público, e o portão lê **todos** os canais de publicação, de preferência pelo fato e não
      pelo nome.
- [ ] A direção das dependências é verificada pela estrutura do código (AST ou ferramenta da sua
      linguagem), não por busca de texto, e o portão foi visto reprovando import relativo e
      import dinâmico.
- [ ] O domínio não importa I/O nem relógio; quem precisa de hora recebe a hora por argumento.
- [ ] Toda porta tem dois adaptadores hoje, contando o falso de teste, e um teste de contrato
      roda a mesma bateria contra os dois.
- [ ] Toda propriedade "só acrescenta" é mecânica (modo de abertura verificado, gatilho no banco),
      não convenção.
- [ ] Toda propriedade de ciclo de vida (sobrevive à queda, reinicia sem perder) tem uma prova
      destrutiva escrita na decisão e executada.
- [ ] Cada portão de arquitetura tem fixture legítima incômoda que ele deixa passar, e uma mutação
      por modo de falha que ele reprova.
- [ ] Quando um ciclo abre um canal, um formato ou um poder novo, a revisão pergunta em voz alta:
      quais portões guardavam a porta velha, e o mundo deles cresceu?
- [ ] Os portões que guardam o que não pode ser reescrito (ADR, índice de decisões) dizem o que
      não veem.
- [ ] Antes de dividir repositório ou serviço, alguém mediu o acoplamento substantivo e escreveu
      os gatilhos para reabrir a decisão.
- [ ] Cada ADR de arquitetura aponta para o portão que o executa, e cada portão cita o ADR de que
      deriva.

## Referências

**Maestro** (versão `19823c2`, salvo indicação):

- Axiomas, teorema T4, corolários C5, C7 e C10 —
  https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/axioms.md
- Fronteira interna — https://github.com/GHDaru/maestro/blob/19823c2/boundary.json e
  https://github.com/GHDaru/maestro/blob/19823c2/scripts/check-boundary.sh
- ADR 0017 (superado) e ADR 0018 —
  https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0017-divisao-em-dois-repositorios.md e
  https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0018-fronteira-interna-em-vez-de-divisao.md
- ADR 0027, 0028 e 0032 — https://github.com/GHDaru/maestro/tree/19823c2/docs/adr
- Specs e relatórios dos ciclos 018, 021, 033, 038, 039, 054 e 076 —
  https://github.com/GHDaru/maestro/tree/19823c2/specs
- Síntese das bancas do ciclo 076 —
  https://github.com/GHDaru/maestro/blob/19823c2/specs/076-padroes-de-engenharia-e-react/sintese-das-bancas.md
- Crítica que anda do ciclo 074 —
  https://github.com/GHDaru/maestro/blob/19823c2/specs/074-prototipo-navegavel/critica-que-anda.md
- Índice de decisões (`decisao-074-fecho-corte-e-transferencia`,
  `decisao-076-bancas-e-decisoes-do-daru`) —
  https://github.com/GHDaru/maestro/blob/19823c2/docs/records/decisoes.jsonl
- Testes de arquitetura do painel —
  https://github.com/GHDaru/maestro/blob/19823c2/painel/tests/test_import_fronteira.py,
  https://github.com/GHDaru/maestro/blob/19823c2/painel/tests/test_esqueleto.py,
  https://github.com/GHDaru/maestro/blob/19823c2/painel/tests/test_transporte.py
- Gatilhos append-only — https://github.com/GHDaru/maestro/blob/19823c2/painel/schema_workflow.sql
- `check-agents.sh` — https://github.com/GHDaru/maestro/blob/19823c2/scripts/check-agents.sh
- Catálogo de anti-padrões (itens 16, 18 e 23) —
  https://github.com/GHDaru/maestro/blob/19823c2/skills/anti-patterns/SKILL.md
- Workflow de CI — https://github.com/GHDaru/maestro/blob/19823c2/.github/workflows/ci.yml
- Handbook do método, cap. 05 §5.3 e cap. 13 §5.5–5.6 (cópia congelada em
  `maestro-handbook/`, versão `19823c2`).

**Externas**:

- N. Ford, R. Parsons e P. Kua, *Building Evolutionary Architectures*, O'Reilly, 2017 — o conceito
  de *fitness function* de arquitetura.
- A. Cockburn, "Hexagonal Architecture" (portas e adaptadores), 2005, alistair.cockburn.us.
- R. C. Martin, *Clean Architecture*, Prentice Hall, 2017 — a regra da dependência.
- E. Evans, *Domain-Driven Design*, Addison-Wesley, 2003 — agregados e invariantes no domínio.
- M. Nygard, "Documenting Architecture Decisions", 2011, cognitect.com — o formato do ADR.
- M. E. Conway, "How Do Committees Invent?", *Datamation*, 1968.
- D. L. Parnas, "On the Criteria To Be Used in Decomposing Systems into Modules",
  *Communications of the Association for Computing Machinery*, 1972.
- Ferramentas de regra de dependência citadas como alternativa: ArchUnit (archunit.org),
  import-linter (pypi.org/project/import-linter), dependency-cruiser
  (github.com/sverweij/dependency-cruiser), Nx `enforce-module-boundaries` (nx.dev), Packwerk
  (github.com/Shopify/packwerk), pacotes `internal` do Go (go.dev). Acesso em 02/11/2026.
