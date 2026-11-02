# 04 — A spec como partitura

> *O regente não toca os instrumentos. Escreve o que cada um vai tocar, e escuta se tocou.*

Seu time já escreve especificação, e você já viu o destino dela: a pasta de documentos que
ninguém abre porque ninguém confia. Com agentes de Inteligência Artificial (IA) escrevendo o
código, esse documento esquecido deixa de ser um problema de higiene e passa a ser o lugar
por onde entra o erro mais caro: o código que compila, passa no teste e faz a coisa errada.
Este capítulo mostra por que a especificação precisa estar **antes** do código e alimentá-lo,
e não depois, descrevendo-o. Também mostra como escrever um requisito que uma máquina confere
e como decidir quanto processo cada mudança merece, para não trocar adivinhação por
burocracia.

## Pergunta central

Quando quem escreve o código é um agente, por que a especificação precisa gerar o código, e
não descrevê-lo depois?

## Resultado de aprendizagem

Ao final do capítulo, você consegue:

1. **Derivar** a regra "a spec precede o código" de duas premissas (a intenção é humana; só
   o que está escrito sobrevive) e explicar por que a spec que alimenta o código não fica
   desatualizada, sem usar a palavra "disciplina".
2. **Reescrever** um requisito vago na forma QUANDO ‹condição›, O SISTEMA DEVE ‹comportamento
   observável› e dizer qual comando prova que ele vale.
3. **Classificar** uma mudança em raia leve, plena ou de infraestrutura pelos três fatores
   (ambiguidade, raio de impacto, irreversibilidade) e aplicar as duas regras de desempate.
4. **Montar** a sequência de artefatos de um ciclo (spec, plano, tarefas, relatório) e o
   portão de prontidão que separa "spec escrita" de "spec que um agente executa sem adivinhar".
5. **Avaliar** uma ferramenta de desenvolvimento dirigido por especificação separando a ideia,
   que pode atravessar, da ferramenta, que pode não atravessar.

## A falha real

Em 7 de agosto de 2026, no ciclo 041 do Maestro, um agente conduzia uma retrospectiva sobre
disciplina de verificação. No caminho, rodou duas rodadas de avaliação de agentes e as
commitou com a citação "(ciclo 040)" na linha de assunto: os commits `4f6ec0e` e `0873e40`.
Só que não existe ciclo 040. Não há pasta `specs/040-*`, nem spec, nem plano, nem tarefas,
nem relatório [CLAIM-04-001]. Foi trabalho feito sem especificação, batizado com um número
que não correspondia a artefato nenhum, pelo agente que estava escrevendo justamente sobre
disciplina.

Quem pegou não foi a memória do agente nem a leitura atenta de alguém. Foi um script, o
`check-cycle.sh`, que naquela versão exigia que todo commit à frente da linha principal
citasse o ciclo na forma `spec NNN` (ou o número de um *Architecture Decision Record* (ADR), o registro de decisão de arquitetura) [CLAIM-04-002]. O portão ficou vermelho
porque "ciclo 040" não estava no formato esperado. Ele acusou a **forma** da citação, não a
ausência da spec. Foi lendo o vermelho que o agente percebeu o problema de fundo, e o
relatório do ciclo 041 o registra sem atenuante: violação do Princípio I, cometida por quem
escrevia a retrospectiva. Os dois commits não foram reescritos, porque já estavam no
repositório compartilhado, e reescrever histórico para deixar um portão verde é pior que a
falha original. O achado entrou no índice de decisões como "fechada no mesmo ciclo"
[CLAIM-04-003] ([relatório do ciclo 041](https://github.com/GHDaru/maestro/blob/19823c2/specs/041-retro-dos-quatro-achados-de-eval/qa-report.md)).

A segunda falha é cinco dias mais velha e mais incômoda, porque aconteceu dentro do texto que
explicava a regra. Em 2 de agosto, o ciclo 023 reescrevia o capítulo do handbook do Maestro
sobre desenvolvimento dirigido por especificação. A primeira versão da seção de prática
afirmava que as correções de texto do repositório entravam pela raia leve, "com o *pull
request* (PR) servindo de artefato". Soava certo e batia com a norma. O comando mostrou outra coisa:
as 22 pastas de ciclo tinham spec própria, quase todas marcadas como plena
[CLAIM-04-004]. Na véspera do ciclo, eram 19 specs em plena e 2 em leve [CLAIM-04-005]. A
afirmação plausível e falsa foi corrigida antes de publicar, e o relatório do ciclo a nomeou
pelo que era: o anti-padrão "parece que funciona", aplicado à prosa
([relatório do ciclo 023](https://github.com/GHDaru/maestro/blob/19823c2/specs/023-capitulo-03-padrao-v2/qa-report.md)).

O mesmo relatório levantou o achado de fundo: a régua das raias não estava sendo aplicada. Ou
o trabalho era todo ambíguo e de raio largo, o que era improvável num período de ajustes de
tema e correções de texto, ou marcar "plena" tinha virado hábito. O achado foi registrado com
uma pergunta objetiva e ficou aberto até a retrospectiva do ciclo 034, que o fechou
transformando-o em portão: o `check-cycle.sh` passou a exigir que cada spec justifique a raia
pelos três fatores e a imprimir a distribuição das raias [CLAIM-04-006]
([commit `7264fe6`](https://github.com/GHDaru/maestro/commit/7264fe6)). O mesmo portão
absorveu uma segunda observação: a citação do ciclo nos commits tinha se mantido por 28
commits só por hábito, e hábito é o que falha primeiro [CLAIM-04-007].

As duas histórias marcam as duas bordas deste capítulo. A primeira mostra que trabalho sem
spec acontece mesmo com quem conhece a regra, e que só um mecanismo fora da cabeça do agente
pega. A segunda mostra o erro oposto: spec para tudo, aplicada por reflexo, que torna a
regra invisível justamente por ser universal.

## Teoria

### Do axioma ao teorema

O Maestro organiza suas regras numa camada de derivação: cinco premissas assumidas (axiomas),
teoremas derivados delas e corolários
([axioms.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/axioms.md)). Este
capítulo vem do primeiro teorema, T1, e depende de duas das cinco premissas [CLAIM-04-008].

**A1 — a intenção é humana.** Um agente propõe, escreve e verifica, mas não *quer*. O que
construir e por que vale a pena não tem outra origem além de uma pessoa. Sem A1 não haveria
razão para existir especificação: o sistema seria um otimizador sem função objetivo.

**A4 — o que está escrito é o que sobrevive.** Um agente começa cada sessão do zero. O que
não está num artefato não existe para a próxima execução, incluindo o motivo de uma decisão.

**T1 — a especificação precede o código.** Se a intenção é humana e só o escrito sobrevive, a
intenção precisa morar num artefato *antes* de virar código. Caso contrário, o agente preenche
o silêncio adivinhando, e o resultado compila sem acertar o alvo. O documento de axiomas
apresenta como evidência os ciclos do repositório abertos, cada um, por um `spec.md` (34 na
data em que T1 foi escrito) e o caso do ciclo 021, que veremos adiante [CLAIM-04-008].

O Princípio I da constituição do Maestro é a forma normativa de T1: nenhum código nasce sem
especificação; a spec é o insumo que gera o código, por isso não apodrece; e uma mudança de
escopo volta à spec antes de virar código
([principles.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/principles.md)).
Repare que o argumento não diz "porque é boa prática". Diz que, dadas as duas premissas, não
há outro lugar onde a intenção possa morar.

### O modo de falha que parece sucesso

No fluxo tradicional, um requisito vago gera uma dúvida. O desenvolvedor pergunta, alguém
responde, e a ambiguidade se resolve numa conversa. Com um agente, o requisito vago gera
**código**. O agente não para para perguntar; ele preenche o que você não disse com a
hipótese mais plausível, e faz isso para cada uma das muitas decisões implícitas de uma
funcionalidade. O resultado compila, passa nos testes que o próprio agente escreveu para a
hipótese que ele próprio escolheu, e erra a intenção.

É o modo de falha mais caro que existe porque se parece com sucesso. Um build vermelho chama
atenção; um build verde com a coisa errada dentro só é descoberto quando alguém usa. A
pergunta que o tech lead precisa fazer não é "o agente é bom o bastante?", e sim "onde
estava escrita a intenção que o agente deveria ter seguido?". Se a resposta é "no prompt da
conversa de ontem", ela não está em lugar nenhum (A4).

### Por que o documento a jusante apodrece

A documentação tradicional descreve o código. Ela fica **a jusante**: quando o código muda, o
documento fica errado e nada acontece. Errar não custa nada a ninguém, então a correção
depende de alguém lembrar. Parnas e Clements já observavam, em 1986, que documentação de
projeto tende a ser escrita depois e para justificar, e propunham "fingir" um processo
racional mantendo os documentos como se tivessem vindo antes. O problema que eles
contornavam é de posição, não de caráter.

A spec que alimenta o código fica **a montante**. É o mesmo movimento da inversão de
dependência em arquitetura (o que dependia passa a ser dependido). Quem quer código novo muda
a spec primeiro; se alguém muda o código sem mudar a spec, algo quebra: um teste que lê o
valor da spec, um verificador que liga requisito a teste, uma revisão que compara o diff com
a spec. A desatualização deixa de ser silenciosa. Por isso a pergunta "por que a spec não
apodrece?" tem uma resposta que não depende de gente mais cuidadosa: ela não apodrece porque
apodrecer quebra alguma coisa a jusante. Documento que não alimenta nada volta a apodrecer,
por melhor que seja o time (é o corolário C9 do Maestro, tratado no
[capítulo 14](../14-a-organizacao-que-aprende/capitulo.md)).

### O quê e por quê, separado do como

A spec diz **o quê** e **por quê**: o problema, o valor, o que se observa quando o problema
está resolvido. O plano diz **como**: arquitetura, cortes, dependências, decisões técnicas.
Misturar os dois é o começo do amontoado. Uma spec que diz "criar a tabela X com as colunas
Y" já é plano. Ela fixou a solução antes de alguém discutir se era a solução, e tirou do
revisor a possibilidade de perguntar se havia outra.

A separação também tem uma razão de contexto. A spec é o artefato que precisa sobreviver a
tudo, inclusive ao reset da sessão do agente; o plano pode ser refeito se o como mudar. Manter
a spec curta e sem como é o que a deixa barata de reler a cada sessão (o
[capítulo 5](../05-engenharia-de-contexto/capitulo.md) trata a spec como o contexto
integrador que se preserva quando o resto é descartado).

### A frase que a máquina confere

Saber que a intenção deve estar escrita não diz *como* escrevê-la. A forma mais barata para tirar ambiguidade de um requisito sem cair em linguagem formal é a *Easy
Approach to Requirements Syntax* (EARS), proposta por Mavin e colegas em 2009 a partir de
requisitos de motores aeronáuticos. No Maestro, a decisão de adotá-la saiu da avaliação
do ecossistema no ciclo 007 e foi materializada no ciclo 008; na véspera do ciclo 023, 14 das
specs do repositório já tinham requisitos nessa forma [CLAIM-04-005]. A ideia é um conjunto pequeno de moldes de frase, cada um
com uma condição e um comportamento:

| Molde | Forma em português |
|---|---|
| Ubíquo | O SISTEMA DEVE ‹comportamento› |
| Por evento | QUANDO ‹gatilho›, O SISTEMA DEVE ‹comportamento› |
| Por estado | ENQUANTO ‹estado›, O SISTEMA DEVE ‹comportamento› |
| Indesejado | SE ‹condição indesejada›, ENTÃO O SISTEMA DEVE ‹comportamento› |
| Opcional | ONDE ‹funcionalidade presente›, O SISTEMA DEVE ‹comportamento› |

O que a frase entrega é uma **condição observável** e um **comportamento observável**. Dela
sai um teste quase sozinho: a condição vira o preparo e a ação do teste, o comportamento vira
a asserção. Compare "QUANDO o subtotal for maior ou igual a R$ 200,00, O SISTEMA DEVE cobrar
frete de R$ 0,00" com "o frete deve ser competitivo". A primeira se prova ou se refuta com
duas linhas de código. A segunda não se prova nem se refuta, e por isso não é requisito: é
desejo.

Quando o critério não é comportamento, mas estrutura ou invariante ("todo link relativo
resolve", "nenhum arquivo de configuração tem segredo"), o equivalente da frase EARS é o par
`comando` → esperado: uma busca com saída vazia, uma contagem, um código de saída. A pergunta
que resolve qualquer critério é a mesma nos dois casos: **que comando prova isto?** Se você
não consegue responder, o critério ainda está vago. O
[capítulo 10](../10-quality-gates-que-provam-fatos/capitulo.md) leva essa pergunta até o fim,
inclusive para o caso em que o comando mede a coisa errada.

O teste real de uma frase EARS é ela virar comando. Foi exatamente esse caminho, da frase da
spec ao executável e à primeira execução, que o ciclo 023 exigiu como requisito do capítulo
que reescrevia, com todo número reproduzível por comando. No ciclo 021 do Maestro, antes de existir
o código, a spec dizia:

> **FR3** (o terceiro requisito funcional, *functional requirement* (FR)): QUANDO uma skill existe em `skills/` e não é citada na instrução, O SISTEMA DEVE
> falhar — skill invisível é skill que não existe.

A condição virou um laço sobre os diretórios de `skills/`; o comportamento virou uma
mensagem de erro e um código de saída, no script que confere a instalação do método
([check-install.sh](https://github.com/GHDaru/maestro/blob/19823c2/scripts/check-install.sh)).
Na primeira execução, o verificador nasceu vermelho: a skill de jornada viva tinha sido
criada no ciclo 018 e nunca entrara na instrução que a IA lê; ficou três ciclos no disco,
invisível. A mesma auto-instalação achou outras duas derivas da mesma família, entre elas um
Constitution Check que listava sete princípios quando a constituição já tinha oito havia oito
ciclos [CLAIM-04-009]. Nada disso quebrava o build. A IA apenas seguia menos método do que o
repositório declarava, e só uma frase escrita antes do código, numa forma que virava laço,
encontrou isso.

### Quanto processo esta mudança merece

Spec para tudo é burocracia; spec para nada é adivinhação. A saída é graduar. O valor de uma
spec escala com três fatores, e é deles que sai a decisão:

- **Ambiguidade** — quão claro é o que se quer? Um erro de digitação tem uma resposta certa;
  "frete grátis para pedidos grandes" tem dezenas.
- **Raio de impacto** — quanto do sistema a mudança alcança? Uma função privada, ou um
  formato lido por três serviços?
- **Irreversibilidade** — dá para desfazer com um commit, ou a mudança apaga, migra, publica?

No Maestro isso é o corolário C6: quanto processo uma mudança recebe é função de ambiguidade
× raio × irreversibilidade. Ele deriva de T1 (a intenção precisa estar escrita quando há o
que adivinhar) e de T3 (o portão escala com a irreversibilidade, assunto do
[capítulo 11](../11-risco-reversibilidade-e-autonomia/capitulo.md)). Na prática, viram três
raias:

| Raia | Quando | O artefato | Verificação |
|---|---|---|---|
| **Leve** | bug, erro de digitação, renomeação, log: o diff cabe numa frase | o pull request é o artefato; bug exige um teste que o reproduz falhando antes | reduzida, mas mantém testes, verificações automáticas e revisão independente |
| **Plena** | funcionalidade ambígua, contrato, mudança que cruza funcionalidades | spec, plano, tarefas, relatório | completa |
| **Infra** | infraestrutura, migração, implantação | sempre plena | completa, mais os portões de reversibilidade (backup, ensaio, ambiente de homologação, plano de volta) |

Duas regras de desempate fazem a classificação durar mais de uma semana. **Na dúvida entre
leve e plena, é plena.** E **infraestrutura e migração nunca são leves**, mesmo quando a
mudança é de uma linha: uma linha de configuração que aponta a aplicação para outro banco
tem raio pequeno no diff e irreversibilidade alta no mundo. Uma terceira regra impede o
abuso da raia leve: ela dispensa os artefatos de planejamento, mas não afrouxa revisão
independente nem testes.

### Pronto para começar

A última peça teórica fecha a ponte entre spec e execução. Uma spec pode estar escrita e
ainda não estar pronta. A Definition of Ready (DoR), na versão do Maestro para a raia plena,
diz que uma spec só entra em execução quando: os critérios de aceite são testáveis; as
ambiguidades foram resolvidas ou registradas; o plano passou pelo Constitution Check; há
`ux-design.md` se a mudança toca tela; e o apetite (o tempo fixo que a aposta merece) está
definido ([operating-model.md §7](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/operating-model.md)).
O critério que resume todos: a spec e o plano estão completos o bastante para o agente
executar **sem adivinhar**. Se o agente vai precisar adivinhar, a spec não está pronta,
independentemente de quantas páginas tenha.

## Alternativas

O desenvolvimento dirigido por especificação (*Spec-Driven Development*, SDD) virou um
ecossistema em 2025 e 2026. O Maestro avaliou boa parte dele: a avaliação do ciclo 007,
registrada no ADR 0008,
fichou sete ferramentas por fontes primárias [CLAIM-04-010], e o catálogo do ecossistema
guarda um cartão datado por ideia
([docs/ecosystem/](https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/README.md)).
A tabela resume o que interessa a um tech lead que vai escolher, com o veredito do Maestro e
o porquê.

| Alternativa | O que propõe | Veredito | Por quê |
|---|---|---|---|
| Prompt ad hoc | a intenção vive na conversa | **rejeitado** | produz o código que compila e erra a intenção; a conversa não sobrevive à sessão (A4) |
| GitHub Spec Kit | uma spec por funcionalidade; fases com portão (especificar, esclarecer, planejar, quebrar em tarefas, implementar); templates versionados | **adotado** | casa com uma constituição e com ciclos numerados; é a única ferramenta de terceiro adotada pelo Maestro [CLAIM-04-011] |
| OpenSpec (Fission-AI) | mudança como *delta* contra o comportamento atual: propor, aplicar, arquivar | **ferramenta descartada, ideia absorvida** | duas ferramentas de SDD custam mais do que valem; o delta virou a raia leve (ADR 0005) |
| Kiro (Amazon Web Services, AWS) | IDE (*Integrated Development Environment*) com fluxo de spec e requisitos em EARS | **ferramenta descartada, ideia absorvida** | a IDE proprietária prende; a sintaxe EARS é técnica pública e atravessou sozinha |
| Tessl | *spec-as-source*: a spec é reexecutada e o código é saída | **observar** | a tese é a deste capítulo levada ao extremo; o que reprova é a dependência de um produto imaturo, que não se desfaz barato |
| BMAD-METHOD | pirâmide de documento de requisitos de produto (*Product Requirements Document*, PRD), épicos e histórias, com papéis prontos | **descartado** | três camadas obrigatórias para quem opera sozinho é estrutura que custa mais que o problema; a spec faz o papel do PRD e `tasks.md` o da história |
| Agent OS | três documentos curtos acima da spec: missão, roadmap, base técnica | **formato absorvido** | o roadmap do Maestro ganhou a coluna que liga cada fase ao ciclo que a entregou |
| Superpowers | leis mandatórias, incluindo design aprovado para *toda* mudança | **absorvido em parte** | o rigor das leis atravessou; o portão universal não, porque contradiz as raias |
| GSD e fluxos em comandos (Pimzino) | baixa cerimônia; o fluxo spec → design → tarefas empacotado em comandos | **descartado** | função já servida: a raia leve cobre a baixa cerimônia, e o Spec Kit já é o motor; serve como validação externa, não como absorção |

Três leituras atravessam a tabela.

**Primeira: a ideia atravessa, a ferramenta nem sempre.** O caso que estabeleceu o critério
foi o OpenSpec: a ferramenta foi descartada no ADR 0005 porque manter duas ferramentas de SDD
não se justificava, mas o modelo delta (para mudança pequena, o artefato é o que muda, não uma
spec inteira) virou a raia leve
([cartão 005](https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/ideias/005-raia-leve-delta.md)).
O EARS seguiu o mesmo caminho: veio do Kiro, a IDE ficou de fora, e a sintaxe entrou no
template de spec e na skill de critério verificável no ciclo 008
([cartão 001](https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/ideias/001-ears.md)).
Para o tech lead, a consequência é prática: você pode adotar as ideias deste capítulo com
qualquer ferramenta, inclusive nenhuma.

**Segunda: uma ferramenta de spec só.** Duas fontes de verdade de processo são piores que
uma ruim. O Spec Kit foi escolhido como motor único
([cartão 031](https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/ideias/031-spec-kit.md)),
e cada alternativa posterior foi julgada contra a pergunta "isto é uma ideia que cabe no
motor que já temos, ou um segundo motor?". GSD e os fluxos empacotados em comandos foram
descartados em vez de observados por essa razão: observar exige um gatilho de reavaliação, e
não existe condição futura que faria adotar um segundo motor para uma função já servida
([cartão 020](https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/ideias/020-fluxo-spec-em-comandos.md),
[cartão 021](https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/ideias/021-baixa-cerimonia-para-mudanca-simples.md)).

**Terceira: a tensão real é sobre a raia, não sobre a spec.** O Superpowers exige design
aprovado para tudo e chama de anti-padrão a frase "isto é simples demais para precisar de
design". O Maestro decidiu o contrário no ADR 0005: para um erro de digitação, spec é
cerimônia. Manteve as raias e absorveu só o aviso que vinha da posição oposta, que já era
regra: na dúvida, plena. Se o seu time escolher o portão universal, escolha sabendo o custo,
que aparece no contraexemplo.

## O padrão Maestro

Esta seção descreve como o Maestro implementa o capítulo, citado por versão
(`maestro@19823c2`). Para cada peça, digo o que é **regra** (texto que o agente lê),
**script** (verificação que roda e reprova) e **hook** (gancho do *harness* que dispara
sozinho num evento do agente).

### Regra: o princípio, as raias e a prontidão

- **Princípio I** (regra): spec antes de código; mudança de escopo volta à spec
  ([principles.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/principles.md)).
- **Raias** (regra): o modelo operacional §3 define leve, plena e infra, com as regras de
  desempate e a ressalva de que a raia leve não afrouxa revisão nem testes
  ([operating-model.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/operating-model.md));
  a decisão e o descarte do OpenSpec estão no
  [ADR 0005](https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0005-raias-de-trabalho-e-specs-de-infra.md).
- **Definition of Ready** (regra): o §7 do mesmo documento, para a raia plena.

### Os artefatos de um ciclo

Cada ciclo da raia plena vive numa pasta `specs/NNN-slug/` com quatro artefatos que sempre
existem e cinco que são condicionais, mas sempre declarados [CLAIM-04-012]
([artifacts.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/artifacts.md)):

| Artefato | Responde | Quem consome |
|---|---|---|
| `spec.md` | o quê e por quê; a raia e sua justificativa | o plano, a revisão, o portão humano |
| `plan.md` | como; o Constitution Check completo | as tarefas, o guardião do processo |
| `tasks.md` | a lista executável, incluindo a cauda de fechamento | quem implementa |
| `qa-report.md` | o que foi observado, com evidência | o portão humano |

O catálogo faz uma observação que vale ouro para quem rege agentes: `tasks.md` pesa mais do
que o tamanho sugere. É a lista que o agente executor de fato segue, e ela sobrevive à
compactação do contexto só na medida em que está escrita. Um passo que está na spec e não
está nas tarefas será pulado por um agente que obedece perfeitamente.

Os cinco condicionais (`research.md`, `data-model.md`, `contracts/`, `checklist.md`,
`ux-design.md`) são declarados no plano com um *token* legível por máquina, como
`ART:research=no`, sempre com o motivo. "Não se aplica, porque X" é auditável; silêncio não
é. A regra nasceu de uma medição: zero de quarenta ciclos tinha produzido qualquer um dos
cinco, o que para a maioria era correto, mas nada registrava qual [CLAIM-04-013]. O
`ux-design.md` é a exceção dura: se a mudança toca tela, ele não é opcional. Desde o ciclo
067, o plano também declara o modelo de domínio com tokens `DOM:` (assunto do
[capítulo 8](../08-ddd-para-agentes/capitulo.md)).

### Os templates

Os templates são onde a regra encontra o agente, porque é deles que o agente parte
([.specify/templates/](https://github.com/GHDaru/maestro/tree/19823c2/.specify/templates)):

- O **template de spec** traz no cabeçalho a raia e a origem, um comentário com a régua das
  três raias, as seções "o quê e por quê" (nunca o como), requisitos funcionais (FR1, FR2…), fora de escopo, critérios de aceite em EARS ou como par comando →
  esperado, e o Clarify, onde a ambiguidade vira pergunta para o humano em vez de requisito
  inventado. Os critérios **não têm caixa de marcação**, de propósito: a spec diz o que deve
  valer, o relatório diz se valeu. A caixa convidava a marcar antes de o trabalho existir, e
  isso aconteceu quatro vezes entre os ciclos 042 e 044 [CLAIM-04-014].
- O **template de plano** traz o Constitution Check com uma linha por princípio, oito no
  total, nenhuma vazia [CLAIM-04-012]; a tabela de declaração dos condicionais (`=no` por padrão, com
  motivo); e a tabela do modelo de domínio. Uma violação real de princípio é reformulada ou
  registrada em *Complexity Tracking*, e o portão humano decide (a skill
  `constitution-check` diz quando um princípio conta como violado).

### Script: abrir, conferir, cobrar

- **`new-cycle.sh`** (script) cria `specs/NNN-slug/` com os quatro artefatos em esqueleto e
  nunca sobrescreve um ciclo existente; se o esqueleto divergir dos templates, os templates
  mandam ([new-cycle.sh](https://github.com/GHDaru/maestro/blob/19823c2/scripts/new-cycle.sh)).
- **`check-cycle.sh`** (script) exige, dos ciclos 034 em diante, raia declarada **e**
  justificada pelos três fatores; imprime a distribuição das raias "como visibilidade, nunca
  como veredito"; e exige que todo commit à frente da linha principal cite o ciclo
  ([check-cycle.sh](https://github.com/GHDaru/maestro/blob/19823c2/scripts/check-cycle.sh)).
  Ele admite o próprio limite no comentário de cabeçalho: força o raciocínio e torna o viés
  visível, mas não julga a resposta. A versão de hoje aceita "spec NNN", "ciclo NNN" e
  "cycle NNN"; a do ciclo 041 aceitava só a primeira forma, e foi por isso que o "ciclo 040"
  ficou vermelho.
- **`check-conformance.sh`** (script) responde, por máquina, "este ciclo seguiu o método?"
  lendo os tokens `ART:` e a cauda de `tasks.md`. Um detalhe mostra como ele lida com o que
  não é ciclo. A pasta `specs/070-conferidor-ordem-veredito/` não é um ciclo do Maestro: é um
  chamado importado do Hindiana, outro projeto que usa o método, trazido como evidência. Tem
  um `00-chamado.md`, uma spec com requisitos R1 a R4 em EARS (em inglês, com *SHALL*), e
  um arquivo por veredito de portão, de G0 (reprodução, feita por quem não é autor) a G3
  [CLAIM-04-015]. O verificador o isenta **pela forma** (tem `00-chamado.md` e arquivos
  `G*-*.md`, e não tem `tasks.md`), não pelo nome, e imprime a isenção em vez de calá-la
  ([check-conformance.sh](https://github.com/GHDaru/maestro/blob/19823c2/scripts/check-conformance.sh)).
  É um bom exemplo de spec que atravessa projetos: o formato da frase é o mesmo, mesmo quando
  o resto do processo muda.

### Hook: o que dispara sozinho, e o que não dispara

O Maestro tem três *hooks* configurados [CLAIM-04-025]
([.claude/settings.json](https://github.com/GHDaru/maestro/blob/19823c2/.claude/settings.json)):
um que recusa reescrever o que é histórico (ADRs, índice de decisões), um que carrega no
início da sessão o estado medido do ciclo aberto, e um que, quando o agente diz "terminei",
roda a conformidade do ciclo mais novo e o impede de parar se houver caixa marcada sem
evidência. **Nenhum deles impede escrever código sem spec.** O Princípio I é cobrado depois,
por script (`check-cycle.sh` na citação, `check-conformance.sh` nos artefatos), e na revisão.
É uma escolha honesta de registrar: a falha do ciclo 040 passou pelo momento da escrita e só
foi pega no portão.

### Os comandos do motor

O fluxo é conduzido por comandos de agente que vieram do Spec Kit
([.claude/commands/](https://github.com/GHDaru/maestro/tree/19823c2/.claude/commands)):

| Comando | O que faz |
|---|---|
| `/speckit.specify` | cria ou atualiza a spec a partir da descrição em linguagem natural |
| `/speckit.clarify` | faz até cinco perguntas dirigidas sobre o que está subespecificado e grava as respostas na spec [CLAIM-04-016] |
| `/speckit.plan` | gera o plano a partir do template; desde o ciclo 044, produz só os condicionais declarados `=yes` |
| `/speckit.tasks` | gera `tasks.md` ordenado por dependência |
| `/speckit.analyze` | análise de consistência, sem alterar nada, entre spec, plano e tarefas |
| `/speckit.implement` | executa o plano processando as tarefas |
| `/speckit.converge` | compara o repositório real com spec, plano e tarefas e **anexa** o que falta como tarefas novas, sem reescrever as existentes |

O `converge` merece atenção. Ele veio de um *fork* da casa, não do original, e resolve um
problema típico de agentes: o "implementar" termina, mas nem todo requisito ficou provado. O
comando classifica cada requisito em feito e verificado, feito sem verificação ou não feito,
e anexa uma tarefa com o comando que a prova para cada lacuna. Uma das suas regras é a
tradução direta do Princípio I para dentro da execução: trabalho novo descoberto que **não**
está na spec vira nota de Clarify ou registro, nunca tarefa silenciosa. É o antídoto do
anti-padrão 10 do Maestro, a mudança de escopo silenciosa, em que o agente "aproveita" para
refatorar e o diff pequeno vira um problema maior
([anti-patterns](https://github.com/GHDaru/maestro/blob/19823c2/skills/anti-patterns/SKILL.md)).

### Vendorizar: a ferramenta vira fonte própria

Adotar uma ferramenta de terceiro tem um risco que este capítulo não pode esconder: os
templates genéricos não conhecem as suas regras. O ciclo 009 resolveu isso vendorizando o Spec
Kit seletivamente, isto é, trazendo para dentro do repositório, como fonte própria, o que era
usado, adaptado ao método: templates com raias, EARS, Constitution Check real e portão humano
no fim; o comando `converge` do fork; e um arquivo de proveniência
([spec do ciclo 009](https://github.com/GHDaru/maestro/blob/19823c2/specs/009-vendorizar-spec-kit/spec.md),
fase F4 do [roadmap](https://github.com/GHDaru/maestro/blob/19823c2/docs/roadmap.md)).

O [UPSTREAM.md](https://github.com/GHDaru/maestro/blob/19823c2/.specify/UPSTREAM.md) registra
de onde veio cada peça (o Spec Kit oficial na versão 0.4.3 e o fork no commit `0117a7b`
[CLAIM-04-017]) e marca o estado de cada uma com um token, `UP:state=adapted` ou
`UP:state=verbatim`. As regras são duas: novidade do original só entra por spec, nunca
reinstalando por cima (o que apagaria as adaptações); e divergência é declarada, nunca
silenciosa.

A segunda regra nasceu de uma contradição real. Até o ciclo 044, quem instalava o Maestro
recebia duas ordens: o template de plano mandava **declarar** os cinco condicionais, e o
comando `/speckit.plan` vendorizado mandava **gerar** quatro artefatos incondicionalmente,
entre eles um `quickstart.md` que nem existia no catálogo, um sexto artefato sem dono
[CLAIM-04-018]. Nada dizia qual ordem vencia, e um agente obediente segue a que leu por
último. O ciclo 044 emendou o comando para deferir à tabela de declaração e registrou a
divergência no arquivo de proveniência
([spec do ciclo 044](https://github.com/GHDaru/maestro/blob/19823c2/specs/044-speckit-plan-defere-a-declaracao/spec.md)).
A spec desse ciclo é um bom modelo de justificativa de raia: ambiguidade baixa (a contradição
era textual), raio amplo (o comando é copiado para todo repositório que instala o método),
irreversibilidade baixa (é texto, e a reversão é um commit). Logo, plena.

### A receita: abrir um ciclo

Juntando as peças, abrir um ciclo no Maestro tem cinco passos
([receita](https://github.com/GHDaru/maestro/blob/19823c2/docs/receitas/abrir-um-ciclo.md)):

1. **Classifique a raia em trinta segundos** pelos três fatores. Se é leve, não abra ciclo: o
   pull request é o artefato.
2. **Crie o esqueleto** com `scripts/new-cycle.sh NNN slug`.
3. **Escreva a spec nesta ordem**: origem, o quê e por quê, requisitos, fora de escopo,
   critérios, Clarify. Não invente requisito que não foi dito; ambiguidade vira pergunta.
4. **Passe o portão de prontidão** com o humano antes de qualquer plano: critérios testáveis,
   ambiguidades resolvidas, fora de escopo explícito, apetite definido.
5. **Só então planeje**, com o Constitution Check de oito linhas, uma por princípio da constituição.

O caderno de desenvolvimento do Maestro (versão 0.2.0, uma das apresentações que acompanham o
handbook) descreve o mesmo ciclo do ponto de vista de quem executa, da intenção à
retrospectiva, e registra o que ficou de fora: sem reunião diária, sem planejamento em
cerimônia, sem refinamento de backlog. As funções que essas cerimônias entregavam foram para
os artefatos e para os portões. A spec é a reunião de planejamento que ficou escrita.

## Exemplo executável

O exemplo em [`exemplo/`](exemplo/README.md) é uma funcionalidade de brinquedo, frete grátis
acima de um valor, com Python 3 e nada mais. Ele não gera código a partir da spec, e isso é
de propósito: o ponto não é automatizar a escrita, é provar que a spec está a montante. Para
rodar:

```bash
cd livro/04-a-spec-como-partitura/exemplo
bash rodar.sh | diff - saida-esperada.txt   # nenhuma linha de diferença
```

São sete passos, cada um ligado a uma ideia deste capítulo [CLAIM-04-019]:

1. **A spec aprovada passa no lint.** `partitura.py lint` classifica cada requisito como EARS,
   par comando → esperado, ou desejo. Os três requisitos da `spec.md` estão em EARS (um deles
   no molde indesejado, SE … ENTÃO), e os critérios são comandos.
2. **A mesma intenção escrita como prompt reprova.** Em `casos/spec-vaga.md`, "o sistema deve
   dar frete grátis para pedidos grandes" sai como desejo (fora da forma), e uma frase com
   cara de EARS também reprova, porque o comportamento é "de forma rápida e intuitiva", que
   não se observa. Três desejos, um requisito.
3. **Cada requisito tem teste, e nenhum teste existe sem requisito.** `partitura.py rastreio`
   liga `FR1` a `test_fr1_*` nos dois sentidos. Teste sem requisito é código que a spec não
   pediu, a forma executável da mudança de escopo silenciosa.
4. **Os testes leem o limite da spec.** O teste de FR1 não tem "200" escrito: ele lê
   "R$ 200,00" da frase da spec e confere que o frete é zero nesse valor.
5. **A spec muda primeiro.** O comercial baixa o limite para R$ 150,00 e pede um requisito
   novo (região desconhecida é recusada). O rastreio acusa o FR4 sem teste.
6. **O código fica vermelho até seguir a spec.** Contra a spec v2, o teste de FR1 falha:
   subtotal 150,00, esperado 0,00, obtido 25,00. A desatualização não é silenciosa, que é toda
   a diferença entre documento a montante e a jusante.
7. **Quanto processo cada mudança merece.** `partitura.py raia` classifica cinco mudanças
   pelos três fatores: duas leves (uma delas um bug, que exige teste que o reproduz), duas
   plenas (uma pelo desempate "na dúvida, plena", outra pelo raio) e uma infra (a migração de
   uma linha, que nunca é leve). A última linha imprime a distribuição, como o portão do
   Maestro: visibilidade, nunca veredito.

O README traz a saída esperada completa e um exercício para fechar a v2. Traz também um script
opcional, `medir_maestro.py`, que reproduz num clone do Maestro os números deste capítulo.

## Contraexemplo

A regra tem custo, e há situações em que ela atrapalha.

**Spec para o que cabe numa frase é cerimônia.** Corrigir um erro de digitação, renomear uma
variável, ajustar uma linha de log: os três fatores são baixos, e escrever spec, plano e
tarefas para isso é processo que não muda decisão nenhuma (o anti-padrão "cerimônia de
papel"). É exatamente o que o portão universal do Superpowers exige, e é por isso que o
Maestro não o adotou. O custo da raia leve é outro: ela depende de alguém classificar bem, e
"é rapidinho" não é análise de risco.

**A régua pode virar reflexo, e o portão não conserta isso sozinho.** O dado do Maestro é
desconfortável e vale olhar de frente. Na versão citada, todos os 76 ciclos têm `spec.md`; 54
estão marcados como plena, 15 como leve e 5 como infra, e dois não têm raia legível
[CLAIM-04-020]. Das 12 raias leves anteriores ao ciclo 034, dez são a série de migração de
capítulos do handbook (ciclos 023 a 032), e do ciclo 034 em diante, depois que o portão passou
a exigir a justificativa, foram 33 plenas, 5 infra e só 3 leves [CLAIM-04-021]. O portão
mudou o *raciocínio escrito*, que hoje cita os três fatores; não está claro que tenha mudado a
*distribuição*. Pode ser que o trabalho recente seja mesmo mais ambíguo e de raio maior
(houve um painel, um protocolo entre sessões, um protótipo navegável). Pode ser que a regra de
desempate "na dúvida, plena" esteja fazendo o trabalho que a régua deveria fazer. O script
não decide, e diz isso no próprio cabeçalho. Repare também que até as mudanças leves do
Maestro ganharam pasta e spec: o registro numerado é uma escolha do repositório, não uma
exigência da raia, e tem custo de contexto.

**Os templates são custo fixo.** O cartão do Spec Kit no catálogo do Maestro reconhece que os
templates carregados a cada ciclo são o maior custo fixo de contexto do método, e que esse
custo foi aceito. Num time com muitas mudanças pequenas e pouca ambiguidade, esse custo pode
não se pagar.

**A forma não garante o mérito.** EARS tira ambiguidade da frase; não garante que a frase
seja a certa. Um requisito perfeitamente verificável pode especificar a coisa errada, e a spec
a montante propaga o erro mais depressa, porque tudo a jusante obedece. É por isso que a
aprovação da spec é um portão humano e não um verificador: se era a coisa certa é a pergunta
que fica com quem tem a intenção (A1). O próprio lint do exemplo é um verificador de forma,
não de mérito.

**A forma também não é universal na prática.** Das 76 specs do Maestro, 48 trazem a frase
literal "O SISTEMA DEVE" [CLAIM-04-022]. Parte das outras usa variantes (WHEN … THEN, ou
"QUANDO …, o `script` DEVE …", nomeando o ator) que a contagem literal não pega, de modo que o
número é um piso; outras, como as specs de retrospectiva e de capítulo, não têm
comportamento a especificar. O cartão do EARS afirma que a forma foi usada em todas as specs
do ciclo 009 em diante. A contagem não confirma isso de forma literal, e é mais um caso de
afirmação sobre o método que precisa de comando, não de memória.

**Os anti-padrões de spec.** Cinco erros aparecem com regularidade, e todos anulam o
argumento deste capítulo:

- **Spec que descreve solução** ("criar tabela X com colunas Y"): é plano; a spec diz o
  problema e o que se observa quando ele está resolvido.
- **Critério não verificável** ("deve ser rápido", "deve ser intuitivo"): sem número, sem
  comando, sem observável, não entra.
- **Spec escrita depois**, para satisfazer o processo: documento a jusante de novo, com custo
  de cerimônia e benefício zero.
- **Raia plena para tudo**: processo que não muda decisão.
- **Raia leve por conveniência**: infraestrutura nunca é leve.

**Spec como única fonte, ao extremo.** A tese do Tessl (a spec é reexecutada e o código é só
saída) é este capítulo levado ao limite. O Maestro a observa e não adota, e o motivo é
reversibilidade: o método inteiro passaria a depender de um produto. Se a sua plataforma
oferecer isso, a pergunta não é se a ideia é boa; é quanto custa sair dela.

## Evidência

O que sustenta este capítulo, com o estado de cada afirmação. O registro completo, com o
comando ou caminho que reproduz cada número, está em [claims.md](claims.md).

**Medido** (reproduzível por comando no Maestro em `19823c2`, ou pelo exemplo):

- Os commits do "ciclo 040" existem e a pasta não [CLAIM-04-001]; o portão de então aceitava
  só a forma `spec NNN` [CLAIM-04-002].
- A distribuição de raias na véspera do ciclo 023: 19 plena, 2 leve [CLAIM-04-005].
- A distribuição de hoje e o corte antes e depois do ciclo 034 [CLAIM-04-020, CLAIM-04-021].
- O piso de 48 specs com a frase EARS literal [CLAIM-04-022].
- A saída do exemplo executável [CLAIM-04-019].

**Observado** (o Maestro registra; o livro leu o registro, não refez o experimento):

- O vermelho do ciclo 021 na primeira execução, com a skill invisível havia três ciclos
  [CLAIM-04-009].
- A afirmação falsa da primeira versão do capítulo 023 e o achado das raias, fechado pela
  retrospectiva do 034 [CLAIM-04-004, CLAIM-04-006, CLAIM-04-007].
- O registro do achado do ciclo 041 [CLAIM-04-003].
- Os números da camada de axiomas e do catálogo: os ciclos abertos por spec quando T1 foi
  escrito [CLAIM-04-008]; as ferramentas fichadas no ADR 0008 [CLAIM-04-010]; o Spec Kit como
  única ferramenta adotada [CLAIM-04-011]; as versões do original e do fork [CLAIM-04-017].
- A estrutura de artefatos e templates [CLAIM-04-012, CLAIM-04-013, CLAIM-04-014], o limite
  de perguntas do Clarify [CLAIM-04-016], a contradição do `/speckit.plan` [CLAIM-04-018] e o
  chamado importado do Hindiana [CLAIM-04-015].
- A raia leve como herdeira do delta do OpenSpec, usada por doze ciclos quando o cartão foi
  escrito [CLAIM-04-023].

**Hipótese** (não medida):

- **H1 — spec reduz retrabalho** [CLAIM-04-024]. É a afirmação que justificaria
  economicamente o capítulo, e este livro não a mediu. O Maestro tem um único repositório,
  operado pelo próprio autor do método, sem grupo de controle. A agenda de pesquisa propõe o
  desenho que a testaria: a mesma tarefa sob prompt puro, sob spec, sob spec com portões e
  sob o método completo, com repetições e ambiente congelado. O
  [capítulo 15](../15-validando-o-maestro/capitulo.md) trata desse protocolo. Até lá, o que
  este capítulo sustenta é o mecanismo (por que a spec a montante não fica desatualizada) e os
  casos em que a falta dela foi pega, não o tamanho do ganho.

## Checklist

Aplique no seu time, item por item. Cada um se confere por comando ou por inspeção de um
artefato, não por opinião.

- [ ] Toda mudança que não cabe numa frase tem um arquivo de spec versionado no repositório,
      criado **antes** do primeiro commit de código (confira pela data do primeiro commit de
      cada um).
- [ ] A spec diz o quê e por quê; não há nome de tabela, classe ou rota na seção de
      requisitos (busque por eles).
- [ ] Todo requisito comportamental está numa forma EARS, e todo critério estrutural é um par
      `comando` → esperado. Um verificador de forma (como o `partitura.py lint` do exemplo)
      roda na integração contínua.
- [ ] Para cada requisito existe ao menos um teste ligado a ele por nome ou id, e não existe
      teste sem requisito (rastreio nos dois sentidos).
- [ ] Ao menos um valor da spec é lido pelos testes, de modo que mudar a spec sem mudar o
      código deixa algo vermelho.
- [ ] Cada spec declara a raia **e** justifica pelos três fatores: ambiguidade, raio de
      impacto, irreversibilidade.
- [ ] As duas regras de desempate estão escritas onde o agente lê: na dúvida, plena;
      infraestrutura e migração nunca são leves.
- [ ] Na raia leve, o pull request de um bug traz um teste que reproduz o bug falhando antes
      da correção.
- [ ] Há um portão de prontidão humano antes do plano: critérios testáveis, ambiguidades
      resolvidas ou registradas, fora de escopo explícito, apetite definido.
- [ ] Mudança de escopo descoberta durante a execução vira pergunta ou registro, nunca
      tarefa silenciosa.
- [ ] Todo commit cita o ciclo ou a spec que o originou, e um script cobra isso.
- [ ] Se você usa uma ferramenta de spec de terceiro, há um arquivo de proveniência dizendo o
      que veio de onde, em que versão, e o que foi adaptado.
- [ ] A distribuição de raias do último trimestre está impressa em algum lugar que o time vê.

## Referências

Fontes do Maestro, todas na versão `19823c2`:

- Axiomas, teoremas e corolários (A1, A4, T1, C6, C9):
  <https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/axioms.md>
- Constituição, Princípio I:
  <https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/principles.md>
- Modelo operacional, §3 (raias) e §7 (DoR):
  <https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/operating-model.md>
- Catálogo de artefatos:
  <https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/artifacts.md>
- ADR 0005 (raias e specs de infra):
  <https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0005-raias-de-trabalho-e-specs-de-infra.md>
- ADR 0008 (avaliação do ecossistema SDD):
  <https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0008-avaliacao-ecossistema-sdd.md>
- Cartões do ecossistema 001, 005, 016, 020, 021, 031, 036 e 039:
  <https://github.com/GHDaru/maestro/tree/19823c2/docs/ecosystem/ideias>
- Proveniência do Spec Kit vendorizado:
  <https://github.com/GHDaru/maestro/blob/19823c2/.specify/UPSTREAM.md>
- Templates de spec, plano e tarefas:
  <https://github.com/GHDaru/maestro/tree/19823c2/.specify/templates>
- Scripts `new-cycle.sh`, `check-cycle.sh`, `check-install.sh`, `check-conformance.sh`:
  <https://github.com/GHDaru/maestro/tree/19823c2/scripts>
- Specs e relatórios dos ciclos 009, 021, 023, 041 e 044, e o chamado importado 070:
  <https://github.com/GHDaru/maestro/tree/19823c2/specs>
- Índice de decisões (achados 023 e 041):
  <https://github.com/GHDaru/maestro/blob/19823c2/docs/records/decisoes.jsonl>
- Receita "abrir um ciclo":
  <https://github.com/GHDaru/maestro/blob/19823c2/docs/receitas/abrir-um-ciclo.md>

Fontes externas (citadas a partir do registro do Maestro em `19823c2`; os endereços não foram
reacessados para esta edição):

- GitHub. *Spec-driven development with AI: get started with a new open source toolkit*,
  set. 2025. <https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/>
- GitHub Spec Kit. <https://github.com/github/spec-kit>
- Fission-AI. OpenSpec. <https://github.com/Fission-AI/OpenSpec>
- Kiro, documentação de specs. <https://kiro.dev/docs/specs>
- BMAD-METHOD. <https://github.com/bmad-code-org/BMAD-METHOD>
- Agent OS. <https://github.com/buildermethods/agent-os>
- Superpowers. <https://github.com/obra/superpowers>

Literatura:

- MAVIN, A.; WILKINSON, P.; HARWOOD, A.; NOVAK, M. *Easy Approach to Requirements Syntax
  (EARS)*. 17th Institute of Electrical and Electronics Engineers (IEEE) International Requirements Engineering Conference (RE'09), 2009.
- PARNAS, D. L.; CLEMENTS, P. C. *A Rational Design Process: How and Why to Fake It*. IEEE
  Transactions on Software Engineering, SE-12(2), 1986.
- MARTIN, R. C. *The Dependency Inversion Principle*. C++ Report, 1996.
