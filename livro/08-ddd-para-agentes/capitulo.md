# 08 — DDD para agentes

> *Um time humano converge para um vocabulário no corredor. Agentes não têm corredor.*

Quando cinco pessoas trabalham juntas por um mês, a palavra "chamado" passa a significar a
mesma coisa para todas, sem que ninguém tenha decidido isso: a conversa do café resolve. Cinco
sessões de agente de Inteligência Artificial (IA) não tomam café. Cada uma começa do zero, escolhe
o nome que lhe parece mais plausível e entrega um código que compila. Uma semana depois você tem
`Ticket`, `Request`, `Chamado` e `Ocorrência` no mesmo repositório, todos para a mesma coisa, e
uma regra de negócio que ninguém decidiu morando numa rota *HyperText Transfer Protocol* (HTTP). Este capítulo mostra por que o
*Domain-Driven Design* (DDD) deixa de ser uma escolha de arquitetura e vira infraestrutura de
coordenação quando quem escreve o código é um agente, e mostra também o que dá para cobrar por
máquina e o que fica com o revisor humano.

## Pergunta central

Como impedir que N agentes criem N nomes para a mesma coisa, e que a regra de negócio vá morar
num lugar que ninguém escolheu?

## Resultado de aprendizagem

Ao final do capítulo, você consegue:

1. **Derivar** do axioma "o que está escrito é o que sobrevive" por que agentes multiplicam
   sinônimos, e por que um glossário que ninguém lê não impede a multiplicação.
2. **Classificar** cada nome que um agente propõe em REUSE, ALIAS, EXTEND ou CREATE, e
   **recusar** o termo novo que chega sem definição e sem contexto dono.
3. **Escrever** as quatro declarações de domínio de um plano (raiz de agregado, onde moram as
   invariantes, mudanças de linguagem ubíqua, portas) e distinguir a regra posta na borda por
   decisão da regra posta na borda por descuido.
4. **Separar** colisão de nomes (uma palavra com dois sentidos) de colisão de endereço (um
   identificador que aponta para duas coisas, ou para nenhuma), e aplicar a invariante "endereço
   ambíguo é recusado, nunca resolvido".
5. **Montar** um modelo de domínio único do qual o glossário e a documentação são gerados, com
   uma integração contínua que regera do modelo e recusa a divergência, e **dizer** o que essa
   geração não garante.

## A falha real

Na madrugada de 3 de outubro de 2026, a equipe do projeto Hindiana, que usa o Maestro, fechou
uma rodada de trabalho de agentes, a rodada 095, e encontrou o defeito que dá nome a este
capítulo. As regras de negócio de uma das tarefas tinham ido parar dentro das rotas HTTP.
Ninguém discutiu linguagem ubíqua, raízes de agregado nem
portas, porque o plano tinha sido pulado. O teste ficou verde pelo caminho errado, e o defeito,
nas palavras do registro, "só apareceu na barra" [CLAIM-08-001].

O que torna a falha instrutiva é o que **não** aconteceu. Nenhum portão reclamou. O verificador
de conformidade do método, o `check-conformance.sh`, já cobrava naquela época que o plano
declarasse os artefatos condicionais (modelo de dados, contratos, desenho de interface), cada um
com um motivo. Nada cobrava o domínio. O plano é o único lugar do fluxo
`spec → plano → tarefas → implementação` onde se decide qual agregado muda, onde a regra mora e
que termo entra no vocabulário, e pular esse passo não produzia sintoma nenhum [CLAIM-08-002].
O plano do Maestro, na época, dizia "use DDD" em prosa. Os agentes leram. Não mudou nada.

A correção saiu na mesma noite, em dois commits do Hindiana. O primeiro, `14f77a5`, à 1h45,
acrescentou ao modelo de plano uma seção com quatro declarações obrigatórias e ensinou o
verificador a lê-las. O segundo, `a94574a`, meia hora depois, aceitou a forma em que o próprio
plano da rodada 095 tinha sido escrito, uma invariante por regra, e foi testado contra ele: os
três itens marcados como "borda" sem motivo reprovaram, e com motivo passaram [CLAIM-08-003].
Pouco mais de duas semanas depois, o Maestro integrou o trabalho como o ciclo 067, com spec retroativa, e
registrou a decisão no *Architecture Decision Record* (ADR) 0023. O ADR diz uma coisa que vale
guardar: aquela era a **segunda** vez que regra de negócio nascia na borda sem decisão, e a
terceira estava a caminho [CLAIM-08-004]
([ADR 0023](https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0023-modelo-de-dominio-declarado-no-plan.md);
[spec 067](https://github.com/GHDaru/maestro/blob/19823c2/specs/067-trava-de-dominio-no-plan/spec.md)).

A segunda falha é o espelho da primeira, e é dois meses mais velha. Em 16 de agosto de 2026, a
retrospectiva do ciclo 055 achou um agente obediente demais. O `plan-architect`, o agente que
escreve planos, estava instruído a consumir "a linguagem ubíqua" do projeto. A documentação dos
perfis repetia a instrução, e o diagrama de entradas e saídas do processo a listava como insumo.
O artefato não existia em projeto nenhum [CLAIM-08-005]. O registro do achado nomeia o defeito
com precisão: instrução sem artefato é o espelho da norma sem função de força, e o agente segue
fielmente uma fonte que não existe. Havia duas saídas honestas: criar o artefato ou tirar a
promessa da instrução.

O achado fechou em 22 de agosto, na retrospectiva do ciclo 061, pela segunda saída. A instrução
parou de mandar consumir um vocabulário que não existia e passou a dizer o que fazer quando ele
falta: propor criá-lo no plano, dizendo onde vai morar. O detalhe que fecha a história é que a
primeira tentativa de correção escreveu na instrução um caminho, `docs/governance/ubiquitous-language.md`,
e o verificador da instalação reprovou, porque nomear o caminho **era** a promessa
[CLAIM-08-006]. A decisão que ficou, e que este capítulo herda, é que o método não entrega
vocabulário de domínio nenhum. O vocabulário pertence ao domínio.

Duas falhas com a mesma raiz. Na primeira, o lugar de decidir o vocabulário existia, mas era
pulável sem sintoma. Na segunda, a instrução apontava para um vocabulário que não estava escrito
em lugar nenhum. Nos dois casos, o agente fez exatamente o que um agente faz quando o vocabulário
não é um artefato lido por alguém: inventou, ou seguiu o vazio.

## Teoria

### Por que agentes multiplicam nomes

Um engenheiro novo no time chega sem vocabulário e o absorve em semanas, por exposição: lê o
código, ouve a reunião, é corrigido no *code review*. A convergência é um efeito colateral de
gente que convive. O agente não convive. Cada sessão começa com a janela vazia, enche-a com o que
você mandou ler e, para o resto, recorre ao que é estatisticamente plausível. "Request" é tão
plausível quanto "Ticket" para um pedido de suporte, e "Chamado" é plausível para quem leu a tela
em português. Três sessões, três escolhas razoáveis, três nomes para a mesma coisa.

Esta é a consequência direta do axioma A4 do Maestro: **o que está escrito é o que sobrevive**.
Um agente começa cada sessão do zero, e o que não está num artefato não existe para a próxima
execução, inclusive o motivo de uma decisão [CLAIM-08-007]
([axiomas](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/axioms.md)). No time
humano, o vocabulário pode morar na cabeça das pessoas, porque as cabeças persistem. No time de
agentes não há cabeça que persista. Ou o vocabulário está escrito, ou ele não existe, e cada
sessão o reinventa.

Escrever não basta. O teorema T5 diz que um artefato só sobrevive se algo a jusante o **consome**
e falha alto quando ele fica velho, ou se ele é imutável [CLAIM-08-008]. Um glossário numa wiki é
escrito e não é consumido: ninguém quebra quando ele está errado, então ele fica errado. O
glossário que segura o vocabulário de um time de agentes é o que alguma máquina lê antes de
aceitar código ou texto. Essa é a diferença entre o DDD de um time humano e o DDD para agentes:
a linguagem ubíqua deixa de ser um acordo social e passa a ser uma entrada de um portão.

### O que o DDD já sabia

Nada do que este capítulo recomenda foi inventado para agentes. Eric Evans descreveu em 2003 o
conjunto de ideias que resolvem o problema; o que muda é o peso de cada uma quando o executor não
tem memória.

**Linguagem ubíqua.** Um vocabulário único, acordado entre quem pede e quem constrói, usado
literalmente no código, nos testes e na conversa. Para Evans, o valor é que a tradução mental
entre "o que o negócio diz" e "o que o código diz" desaparece, e com ela uma classe inteira de
mal-entendidos. Para agentes, o valor é mais direto: um nome que existe no vocabulário é um nome
que o agente **não** precisa inventar.

**Contexto delimitado** (*bounded context*). A fronteira dentro da qual uma palavra tem um sentido
só. "Fila" pode significar duas coisas no mesmo sistema, desde que cada sentido more num contexto
e a fronteira esteja escrita. O contexto delimitado é também a costura por onde o trabalho se
corta para rodar em paralelo: duas sessões em contextos diferentes não disputam o mesmo
vocabulário nem os mesmos arquivos. O [capítulo 6](../06-como-dividir-o-trabalho/capitulo.md)
trata do corte. Aqui interessa o vocabulário: o contexto é o que permite que a mesma palavra
tenha dois donos sem que isso seja uma colisão.

**Raiz de agregado e invariante.** A invariante é uma regra de negócio que precisa valer sempre
("chamado fechado não recebe resposta"). A raiz de agregado é a entidade que guarda a consistência
de um grupo de objetos: toda mudança entra por ela, e é ela quem garante as invariantes. A falha
do Hindiana é a violação literal dessa ideia: a regra foi morar na rota, que é borda, e ninguém
decidiu isso.

**Portas, adaptadores e camada anticorrupção.** A porta é a interface que o domínio expõe ou
exige; o adaptador a implementa com tecnologia (Alistair Cockburn chamou o arranjo de arquitetura
hexagonal). A camada anticorrupção é o adaptador que traduz o vocabulário de outro sistema para o
seu, para que o termo estrangeiro não entre no domínio. Quando o sentido do termo externo é igual
ao seu, a tradução é identidade. Quando não é, o mapa precisa estar escrito, ou o termo de fora
contamina o modelo.

### Colisão de nomes e colisão de endereço

Há duas famílias de confusão de vocabulário, e elas pedem remédios diferentes.

A **colisão de nomes** é uma palavra com dois sentidos. Quando o Maestro desenhou a área
administrativa do seu painel, no ciclo 073, o mapa de contextos achou cinco colisões vivas, todas
com evidência no repositório: "fila" (a fila de decisões do regente e a fila de mensagens de
saída), "caixa de entrada" (a tela de decisões e a entrada de mensagens entre sessões), "livro de
ponto" (o registro de custo por tarefa e o registro de mensagens), "sessão" e "agente" usados como
sinônimos, e "portão" (o portão do chamado e o portão que só o humano registra) [CLAIM-08-009]
([mapa de contextos, §7](https://github.com/GHDaru/maestro/blob/19823c2/specs/073-area-administrativa/confronto/mapa-de-contextos.md)).
O remédio de colisão de nomes é qualificar. O glossário do Maestro transformou isso numa regra
operativa curta: "fila" e "portão" nunca são escritos nus [CLAIM-08-010].

A **colisão de endereço** é outra coisa, e é pior. O mesmo identificador aponta para duas coisas,
ou para nenhuma: o mesmo nome curto de sessão vivo em três referências, o mesmo nome em dois
projetos, uma referência de sessão que mudou quando a sessão reiniciou. Colisão de nomes confunde
quem lê. Colisão de endereço entrega na caixa errada. O Maestro registra a invariante assim:
**endereço ambíguo é recusado, nunca resolvido**, porque uma entrega ao par errado não se desfaz
[CLAIM-08-011]. Não se escolhe "o mais provável". Quem endereça escreve `nome · ref · projeto`, e
uma referência morta é recusada em vez de cair para o nome nu.

A distinção importa para o tech lead porque os dois problemas parecem o mesmo na conversa ("os
agentes estão confundindo os nomes") e têm consertos opostos. Colisão de nomes se resolve com
vocabulário: qualificar a palavra, separar os contextos. Colisão de endereço se resolve com
identidade: um identificador que não depende de um nome, e uma regra que prefere falhar a
adivinhar. Aplicar o remédio de um ao outro não funciona. Qualificar melhor o nome "Gerente" não
impede que duas sessões chamadas "Gerente" existam em dois projetos.

### O catálogo semântico: REUSE, EXTEND, ALIAS, CREATE

Se o vocabulário é uma entrada de portão, cada nome novo que um agente propõe precisa passar por
uma decisão antes de virar código. A base de pesquisa deste livro chama de **catálogo semântico**
a linguagem ubíqua operacional, e propõe que essa decisão tenha quatro saídas [CLAIM-08-012]:

- **REUSE**: o termo já existe no modelo. Use o nome e o identificador que estão lá.
- **ALIAS**: o nome proposto é um apelido conhecido de um termo existente ("Request" para
  `Ticket`). Não nasce identificador novo; o apelido é registrado para que a próxima sessão que o
  propuser seja redirecionada.
- **EXTEND**: o nome qualifica um termo ou uma família que já existe ("prazo de reabertura" numa
  família em que já há "prazo de resposta"). Entra no modelo, com definição e contexto, antes do
  código.
- **CREATE**: o termo é novo de fato. Entra no modelo com definição e contexto dono antes do
  código. Termo novo sem definição é recusado, porque nome que ninguém definiu é o sinônimo de
  amanhã.

A ideia tem um parente direto no Maestro, só que aplicado a componentes de tela em vez de termos.
O agente `ux-semantics` tem como lei que nenhuma tela nasce sem papel semântico declarado: se o
papel já existe no catálogo, consome-se o componente catalogado, e reimplementar localmente um
papel catalogado é violação de revisão; papel novo entra no catálogo **primeiro**, com sua
anatomia, um componente compartilhado e um teste, e só então é usado [CLAIM-08-013]
([ux-semantics](https://github.com/GHDaru/maestro/blob/19823c2/.claude/agents/ux-semantics.md)).
É o REUSE e o CREATE aplicados a botões. O catálogo semântico estende a mesma disciplina aos
nomes.

Fique claro o estado disso. O Maestro não tem, na versão citada, uma ferramenta que classifique
nomes em REUSE, EXTEND, ALIAS e CREATE. O que ele tem são as peças: um modelo de domínio do qual
sai o vocabulário, um glossário com as colisões mapeadas, uma lista de palavras proibidas na tela
e o catálogo de papéis. As duas hipóteses de que o catálogo reduz duplicação (H6) e de que o
glossário reduz inconsistência (H7) estão na agenda de pesquisa e não foram medidas
[CLAIM-08-014]. O exemplo deste capítulo implementa o classificador para você ver a forma; a
evidência de que ele paga o custo ainda não existe.

### Duas línguas, uma fronteira

Há uma segunda razão para o vocabulário precisar de regra escrita, e ela aparece em qualquer time
que não trabalha em inglês. O corolário C10 do Maestro diz que **o que é instalado é lido por
máquina; o que é publicado é lido por gente** [CLAIM-08-015]. Ele deriva de A4 e tem uma
consequência prática: a língua de cada artefato é decidida pelo seu leitor, não pelo humor de
quem digita.

O ADR 0014 aplicou isso ao próprio método: tudo que o instalador copia para outro repositório
(agentes, *skills*, scripts, comandos, templates e a governança) é escrito em inglês, porque é
lido por agentes de IA em qualquer projeto; o livro e as receitas seguem em português, porque têm
um público definido [CLAIM-08-016]. O ADR 0029 emendou o 0014 quando o Maestro ganhou uma tela
própria: a **interface do produto é em português**, os **identificadores são em inglês**, e um
arquivo de modelo liga cada termo de tela ao identificador do código. Nome estrangeiro só entra
onde o sentido é 1:1; onde não é, vale o termo próprio, com uma camada anticorrupção e um mapa
versionado e testado. O contexto do ADR é a falha que motivou a regra: sem ela, os ciclos 073 e
074 já tinham produzido quatro vocabulários para o mesmo estado [CLAIM-08-017]
([ADR 0029](https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0029-tela-em-portugues-codigo-em-ingles.md)).

Para o tech lead brasileiro, essa é a situação do dia a dia: a tela fala português, o código fala
inglês, e o agente traduz como quiser se ninguém escrever a tradução. "Chamado" vira `Call` numa
sessão e `Ticket` em outra. A regra do 0029 não é sobre idioma; é sobre dizer, num arquivo que a
máquina lê, qual identificador corresponde a qual palavra.

### A sigla é o menor termo

O problema dos N nomes tem uma forma mínima que todo time conhece: a sigla sem expansão. Uma
sigla nua é um termo cuja definição ficou na cabeça de quem escreveu. Cada leitor, humano ou
agente, reconstrói a expansão como pode, e reconstrói diferente.

O Maestro começou por aí. O primeiro ciclo do método, o 001, de julho de 2026, nasceu de uma
queixa do mantenedor sobre a governança: "pesada, um amontoado de siglas sem dicionário e sem
storytelling". A resposta foi uma porta de entrada narrativa e um glossário que define todas as
siglas usadas nos documentos de governança [CLAIM-08-018]
([spec 001](https://github.com/GHDaru/maestro/blob/19823c2/specs/001-governanca-didatica/spec.md)).
Quatro dias depois, o ADR 0010 subiu a regra à constituição como Princípio VIII: em cada
resposta, documento ou artefato, a primeira ocorrência de uma sigla vem por extenso, e a contagem
recomeça a cada documento, porque o leitor não tem obrigação de ter lido o anterior
[CLAIM-08-019]. O ADR fecha explicitamente as desculpas de sempre: "todo mundo conhece", "já
expliquei antes", "é jargão do domínio". Termo novo entra no glossário.

A ligação com o resto do capítulo é que o glossário do Maestro é, na prática, a linguagem ubíqua
do próprio método. Cada verbete traz a expansão, o significado no Maestro e onde o termo aparece,
e é ali que moram as colisões mapeadas e as regras de qualificação [CLAIM-08-020]
([glossário](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/glossary.md)). A
regra da sigla e a regra do agregado são a mesma regra em escalas diferentes: nenhum termo sem
definição escrita num lugar que alguém consome.

## Alternativas

Há várias maneiras de tentar manter um vocabulário consistente num time que mistura
pessoas e agentes. Elas não são excludentes, mas custam e entregam coisas diferentes.

| Alternativa | O que resolve | O que não resolve | Veredito |
|---|---|---|---|
| Instrução no prompt ("use DDD", "use nomes consistentes") | Nada que se meça | O agente obedece em espírito e inventa nos detalhes | Necessária, nunca suficiente |
| Glossário descritivo em wiki | Consulta humana | Fica velho sem que nada quebre | Não adote sozinho |
| Contrato por esquema (OpenAPI, *JavaScript Object Notation* (JSON) Schema, Protocol Buffers) | Identificadores nas bordas | O sentido do termo e o vocabulário da tela | Use nas portas |
| Oficinas de descoberta (Event Storming, Impact Mapping, Story Mapping) | Fronteiras e vocabulário do negócio | Consistência depois da oficina | Quando quem usa não é quem decide |
| Modelo de domínio como código, com geração e portão | Consistência verificável entre modelo, tela e documentação | Se o texto gerado é útil a quem lê | Adote quando há tela e mais de um contexto |
| Reconciliar depois, na revisão | Sinônimos que o revisor reconhece | Sinônimos que o revisor não tem como reconhecer | Só com o catálogo na mão do revisor |

**Instrução no prompt.** É o que todo mundo faz primeiro, e foi o que o Maestro tinha antes do
ciclo 067: o plano pedia DDD em prosa [CLAIM-08-004]. A instrução muda a probabilidade de o agente
fazer a coisa certa. Ela não deixa rastro, não falha quando é ignorada, e não diz qual nome usar,
porque o nome certo não está nela. Mantenha a instrução, mas não conte com ela como controle.

**Glossário em wiki.** Resolve a pergunta do humano que quer saber o que um termo significa. Pelo
teorema T5, morre: nada a jusante o consome, e ele diverge do código sem que ninguém perceba.
Tem pior custo-benefício quando o leitor principal é um agente, porque o agente só lê o que você
manda ler, e o que você manda ler precisa estar certo.

**Contrato por esquema.** Um OpenAPI ou um esquema de mensagens fixa os nomes nas bordas do
sistema e pode ser verificado pela integração contínua (*continuous integration*, CI). É a
ferramenta certa para portas. Não diz o que um termo significa, não governa o texto da tela e não
impede que o mesmo conceito ganhe dois nomes em dois esquemas. Trate-o como uma das saídas do
modelo, não como o modelo.

**Oficinas de descoberta.** *Event Storming*, de Alberto Brandolini, e as técnicas irmãs são boas
para descobrir fronteiras e vocabulário quando há distância entre quem decide e quem usa. O
Maestro avaliou as quatro técnicas em agosto de 2026 e deixou o veredito em "observar": todas
pressupõem essa distância, e no Maestro ela era zero, porque o mantenedor era o próprio usuário;
o gatilho para reavaliar é existir produto com usuários externos [CLAIM-08-021]
([cartão 038](https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/ideias/038-tecnicas-de-descoberta.md)).
A oficina produz o vocabulário. Não o mantém. O que sai dela precisa ir para um artefato
consumido, ou será reinventado na primeira sessão de agente.

**Modelo de domínio como código.** Um arquivo único, lido por máquina, com os contextos, os
termos (palavra de tela e identificador), os agregados, as invariantes, os mapas das bordas e as
palavras proibidas; do arquivo saem o glossário e a documentação, e a integração contínua regera
e compara. É o que o Maestro fez no ciclo 076 e o que a seção seguinte descreve. Custa uma linha
de modelo por termo e um gerador para manter [CLAIM-08-017]. Entrega consistência verificável. Não entrega
clareza, como o contraexemplo vai mostrar.

**Reconciliar na revisão.** Um revisor em contexto fresco pode achar `Request` ao lado de
`Ticket` e pedir a unificação. Só acha se souber que os dois são o mesmo conceito, e só sabe se
tiver o catálogo. Sem catálogo, a revisão de vocabulário é leitura atenta, e leitura atenta não é
critério. Com catálogo, metade do que o revisor faria vira um *lint*, e o revisor fica com o que
o *lint* não decide: se um termo novo deveria mesmo ser novo.

## O padrão Maestro

O Maestro resolve o problema em camadas, e vale separar o que é regra escrita, o que é script
que falha e o que é hook. Todas as citações são da versão `19823c2`.

### Regra: o vocabulário pertence ao domínio, e o plano o declara

A regra central é o ADR 0023: o plano de todo ciclo declara o modelo de domínio em quatro linhas,
cada uma com um valor e um motivo [CLAIM-08-022]:

- `DOM:aggregate=`: a raiz de agregado que o ciclo toca ou cria, ou `none` e por quê.
- `DOM:invariants=`: onde moram as regras de negócio, `domain` ou `edge`; `edge` exige o
  motivo de não poder ser domínio. Aceita também uma regra por item:
  `regra_a=domain | regra_b=edge(porquê)`.
- `DOM:glossary=`: `changed`, com os termos que entram ou mudam na linguagem ubíqua, ou `none` e
  por quê.
- `DOM:ports=`: `changed`, com as portas e adaptadores que mudam, ou `none` e por quê.

O título da seção no modelo de plano resume a filosofia: declare as quatro, porque silêncio não é
decisão [CLAIM-08-023]
([plan-template](https://github.com/GHDaru/maestro/blob/19823c2/.specify/templates/plan-template.md)).
O ponto fino está na borda. A regra **não** proíbe pôr uma invariante numa rota ou num adaptador;
ela proíbe pôr ali **sem dizer por quê**. O que se recusa é a borda por descuido, não a borda
decidida.

O primeiro plano a obedecer à regra foi o do próprio ciclo 067, e ele mostra a borda decidida.
Ele declara `DOM:aggregate=none`, porque o ciclo muda um template e um script, e o método não tem
raiz de agregado, tem artefatos lidos por portões. E declara as invariantes como borda, com o
motivo: as invariantes do método moram em scripts de portão porque não existe camada de domínio
onde pudessem morar [CLAIM-08-024]. O ciclo que cria o portão é o primeiro a não poder
dispensá-lo. Os planos seguintes mostram a outra ponta: o do ciclo 075 declara a forma itemizada
com quinze invariantes, catorze no domínio e uma na borda, com o motivo de que ler o ambiente do
processo é entrada e saída, e o domínio não faz entrada e saída [CLAIM-08-025].

A segunda regra é a da língua (ADR 0014 e ADR 0029, na seção anterior), e a terceira é a da
sigla (Princípio VIII). A quarta é o glossário com as colisões e a regra de qualificação. A
quinta é a decisão que fechou o achado 055 e que o diagrama do processo registra: o método
recebe a linguagem ubíqua como insumo **se o projeto mantiver uma**, e não entrega nenhuma
[CLAIM-08-026]. O Maestro instalado num projeto seu não traz um vocabulário de domínio pronto;
traz o lugar onde o seu vocabulário é declarado e o portão que cobra a declaração.

### Script: o que falha quando a regra é ignorada

Pelo corolário C7, norma sem executável é norma sem efeito, e cada regra acima tem um script.

**O bloco de domínio do `check-conformance.sh`.** Lê as quatro declarações de todo plano a partir
do ciclo 067. Declaração ausente, sem valor ou sem motivo é falha; borda sem motivo é recusada e
o item é nomeado. O piso é um botão que **só aperta**: a variável que o controla aceita apenas
número, e um valor acima de 67 faz o script sair com código 2 em vez de afrouxar a regra
[CLAIM-08-027]. A falha é suave durante o trabalho em andamento e bloqueia na promoção para a
linha principal, pela lição de que um portão sempre vermelho no meio do trabalho é um portão que
as pessoas aprendem a ignorar [CLAIM-08-022]. O resultado é medível: todos os planos dos ciclos
067 a 076 têm as quatro declarações, nove de nove; a única pasta da faixa sem as quatro é um
chamado importado que não tem plano [CLAIM-08-028].

**O `check-language.sh`.** Guarda a fronteira de língua do ADR 0014. O cabeçalho dele diz o que
mede com uma honestidade que vale copiar: **resíduo de português** na superfície instalável, e
não "é inglês". Um texto em espanhol, ou em inglês ruim, passa. A linha que precisa carregar
português de propósito (um padrão casado contra o livro, um rótulo de tela) declara o marcador
`PT-DATA` na própria linha, para a exceção ficar visível onde se aplica, nunca numa lista
escondida [CLAIM-08-029]
([check-language.sh](https://github.com/GHDaru/maestro/blob/19823c2/scripts/check-language.sh)).

**O `check-docs-generated.sh`.** É a peça mais recente e a que mais se aproxima do "modelo como
código". No ciclo 076, o painel do Maestro ganhou um modelo de domínio único,
`painel/servidor/dominio/model.yaml`, com nove contextos delimitados (três núcleos, três de apoio,
três genéricos), os termos de tela ligados aos identificadores, as invariantes, as máquinas de
estado, os mapas das bordas, as portas e uma lista de dez palavras proibidas na tela
[CLAIM-08-030]. A seção de documentação do aplicativo e o glossário são **gerados** desse modelo.
O portão grava o resumo `sha256` (do *Secure Hash Algorithm*) do modelo na seção gerada; depois
regera da fonte todos os textos que a tela mostra e compara byte a byte, nomeando a linha que
diverge [CLAIM-08-031]
([check-docs-generated.sh](https://github.com/GHDaru/maestro/blob/19823c2/scripts/check-docs-generated.sh)).

O detalhe de "da fonte" custou uma reprovação. Na primeira versão, o portão regerava os textos a
partir de uma projeção intermediária do modelo, não do modelo. Um juiz em contexto fresco editou
a própria projeção, regerou a seção e a fixture a partir dela, deixou o modelo intacto, e o
portão ficou verde com a tela afirmando o **contrário** do modelo [CLAIM-08-032]. A correção foi
o passo que reconstrói os artefatos a partir do modelo e compara: o modelo é a fonte da verdade,
a projeção é só um passo. A lição vale para qualquer pipeline de geração: confira contra a fonte,
não contra o intermediário que a própria cadeia produziu.

**A lista de proibidos e o mapa das bordas.** O `model.yaml` traz a camada anticorrupção como
dado. Cada borda (o protocolo *Agent2Agent* (A2A), o *Agent Client Protocol* (ACP), os
*hooks* do harness, a ferramenta do painel) tem um mapa termo externo → termo interno, com a
marca `um_para_um`. Das 31 linhas de mapa, 15 não são 1:1 [CLAIM-08-033]. Um exemplo: o
`contextId` do A2A não é o chamado do Maestro, e a tradução `ticketId → contextId` fica na
borda, sem que o `contextId` entre no envelope interno. A lista de palavras proibidas, ao lado,
faz o mesmo pela tela: "agente" nu colide (use "Responsabilidade" para o perfil, "Sessão" para a
execução); "prazo" é sempre qualificado. A lista mora no modelo, que a integração contínua lê,
e não num guia de estilo [CLAIM-08-034].

### O ramo de interface: o papel antes do componente

Quando o ciclo tem tela, o processo do Maestro abre um ramo que não é opcional: o papel semântico
de cada objeto é definido antes do componente (agente `ux-semantics`), num `ux-design.md`, que
passa por um portão de *user experience* (UX) e termina numa jornada viva, com capturas geradas
do build real por script versionado e uma avaliação heurística datada [CLAIM-08-035]
([processo](https://github.com/GHDaru/maestro/blob/19823c2/docs/diagramas/05-bpmn-processo.md)).
O modelo do `ux-design.md` pede, em tabelas separadas, os papéis **consumidos** (já catalogados,
com o componente) e os papéis **introduzidos** (novos, com a anatomia obrigatória e a razão de
não derivarem de um existente) [CLAIM-08-036]
([template](https://github.com/GHDaru/maestro/blob/19823c2/.specify/templates/ux-design-template.md)).
É o catálogo semântico na tela: o desenho declara o que reaproveita e justifica o que cria.

A jornada viva é onde o papel declarado encontra o build. No protótipo navegável do ciclo 074, a
heurística H3 validou no build uma constante do desenho: com o ponto de quebra da navegação em
768 *pixels*, o rótulo mais longo do menu cabia em uma linha a 360 *pixels*, então a constante
ficou onde estava. A H4 registrou o oposto: a barra desenhada tinha ícone sobre o rótulo, a barra
construída tinha só rótulo [CLAIM-08-037]
([jornada 074](https://github.com/GHDaru/maestro/blob/19823c2/docs/jornada/074-prototipo-navegavel.md)).
Ninguém achou isso lendo o desenho; a captura do build mostrou. O mesmo ciclo exigiu que toda
tela do protótipo declarasse um contexto entre os cinco do mapa, e provou o verificador por
mutação: zero achados na fixture boa e 24 na ruim, na primeira tabela do relatório; o corpus
cresceu depois, e a última medição registrada dá 71 na ruim [CLAIM-08-038]. Vocabulário de contexto também se verifica.

### Hook: nenhum, e por quê

O Maestro não tem *hook* de vocabulário. O único guarda `PreToolUse` do repositório protege o
histórico imutável (ADRs, índice de decisões), não os nomes. Há um *hook* `Stop` que roda o
verificador de conformidade quando o agente diz que terminou, mas no modo que só olha caixas
marcadas sem evidência, e nesse modo a declaração de domínio ausente é nota, não bloqueio
[CLAIM-08-039]. Isso é coerente com o
teorema T3: um *hook* bloqueia uma ação no instante em que ela acontece, e se justifica quando a
ação é cara de desfazer. Um nome errado num arquivo é barato de desfazer até a integração; por
isso o controle de vocabulário vive em scripts que rodam no plano, na integração contínua e na
promoção, e não num guarda que interrompe o agente a cada escrita.

### Os papéis de forma

Dois papéis cuidam da forma do vocabulário sem decidir o conteúdo. O `didactics-editor` combate o
amontoado: uma ideia por página, siglas expandidas, jargão órfão removido, e não muda a decisão
técnica, só o modo de contá-la [CLAIM-08-040]. A *skill* `fight-the-pile-up` é a régua que ele
aplica, com a lei "nenhuma sigla nua" e um checklist em que cada item é verificável
[CLAIM-08-041]
([fight-the-pile-up](https://github.com/GHDaru/maestro/blob/19823c2/skills/fight-the-pile-up/SKILL.md)).
O guia editorial do livro do Maestro herdou a mesma regra: sigla nunca nasce nua, evidência por
caminho, tabela só para fato enumerável, uma ideia por seção [CLAIM-08-042]. Este livro herdou o
guia.

## Exemplo executável

O exemplo está em [`exemplo/`](exemplo/README.md). Ele roda com Python 3 e bash, sem rede e sem
dependência paga, sobre um domínio que todo tech lead conhece: uma central de atendimento com
três contextos (atendimento, mensageria, faturamento). Rode:

```bash
cd livro/08-ddd-para-agentes/exemplo
bash rodar.sh | diff - saida-esperada.txt   # nenhuma linha de diferença
```

O arquivo `modelo.json` é o modelo único: cada termo tem a palavra de tela, o identificador, o
contexto dono, a definição e os apelidos conhecidos; as famílias que nunca se escrevem nuas
("fila", "prazo") e as siglas com expansão. Tudo o mais lê dele. São nove passos
[CLAIM-08-043]:

1. **Três sessões nomeiam a mesma tarefa.** As sessões propõem dez nomes para "avisar o atendente
   quando um chamado estoura o prazo de resposta". O classificador decide: três REUSE, três ALIAS,
   um EXTEND, um CREATE e duas recusas ("Fila", nu; "Status", sem definição). Dez nomes viram
   cinco identificadores, dois deles novos e com definição. A linha que importa é esta:

   ```text
     4 nomes para Ticket: Chamado, Ocorrência, Request, Ticket
   ```

   Sem o catálogo, eram quatro tipos no código.
2. **O texto de tela escrito sem catálogo** tem seis achados: duas siglas nuas, dois apelidos no
   lugar do termo do modelo e duas palavras de família escritas nuas.
3. **O mesmo texto depois do catálogo** passa sem achado.
4. **O plano que só diz "usar DDD"** reprova: modelo de domínio nunca declarado.
5. **O plano que pôs uma regra na borda sem motivo** reprova, nomeando o item:

   ```text
     ✗ invariants: 'alerta_sai_uma_vez=edge' é borda sem motivo — escreva alerta_sai_uma_vez=edge(por que não pode ser domínio)
   ```

6. **O plano com as quatro declarações e o motivo da borda** passa.
7. **Endereço**: "Gerente", vivo em dois projetos, é recusado como ambíguo; "Gerente · loja"
   entrega; uma referência morta é recusada em vez de cair para o nome.
8. **Glossário gerado**: confere com o modelo; uma "correção" feita à mão no glossário reprova
   apontando a linha; uma mudança no modelo sem regerar reprova pelo carimbo e pela linha.
9. **Mutação**: as duas réguas (texto e plano) dão zero achados na fixture boa e achados na ruim.
   Régua que não discrimina não é régua.

Repare no que o exemplo **não** faz. Ele não decide se "Alerta de estouro" deveria mesmo ser um
termo novo, nem se o motivo da borda é bom. O classificador garante que a pergunta foi feita e que
a resposta ficou escrita. A qualidade da resposta é do revisor. É a mesma divisão de trabalho do
portão do Maestro, que o ADR 0023 aceita como risco declarado: um motivo vazio de conteúdo passa,
porque o portão mede a existência da decisão, não a qualidade dela [CLAIM-08-044].

Há uma segunda coisa para notar, e ela só aparece no código. O modelo do exemplo tinha, no
rascunho, o apelido "Conta" para Fatura. O *lint* acusaria toda frase com "a conta do cliente",
e o apelido saiu antes da primeira rodada. Apelido que é palavra comum produz falso positivo, e régua que grita
à toa é ignorada. Escolher apelidos é trabalho de domínio, não de ferramenta.

## Contraexemplo

**Projeto pequeno, um contexto, um operador.** O modelo de domínio como código custa uma linha
por termo, um gerador e um portão. Num protótipo de uma semana, com um contexto e uma pessoa,
esse custo não se paga: o vocabulário cabe na spec, e a spec é lida. As quatro declarações do
plano continuam baratas (o plano do 067 declara `DOM:aggregate=none` com uma frase), mas o
`model.yaml` com gerador é exagero. Pelo princípio *You Aren't Gonna Need It* (YAGNI), adote o
modelo gerado quando houver tela e mais de um contexto, ou quando a primeira colisão aparecer.

**O catálogo que congela a língua.** O domínio muda, e um catálogo rígido pode esconder uma
distinção que nasceu. Se "Ocorrência" começou a significar um chamado aberto pelo próprio sistema,
e não pelo cliente, registrá-la como ALIAS de `Ticket` apaga a diferença em vez de nomeá-la. O
ALIAS é uma decisão de domínio com consequência; a ferramenta só a registra. Quem revisa precisa
poder dizer "isto não é apelido, é termo novo", e o catálogo precisa aceitar a mudança com o mesmo
rito do CREATE.

**O portão que mede a forma.** O bloco de domínio do Maestro tem três limites declarados no
próprio ADR. O motivo não é lido: `edge(porque sim)` passa. A forma itemizada divide os itens pelo
caractere `|`, que é também o separador de tabela do Markdown, e numa linha de tabela com a coluna
de motivo preenchida a célula vira item falso e reprova com mensagem confusa. E o script pega a
primeira linha que contém a declaração, de modo que uma menção em prosa antes da tabela vence a
linha real [CLAIM-08-045]. São defeitos com dono e registrados; o ponto é que um portão de
vocabulário verifica que a decisão foi escrita, nunca que foi boa.

**A documentação gerada que ninguém entende.** O caso mais incômodo é do próprio Maestro. Em 1º
de novembro de 2026, um juiz em contexto fresco reprovou a seção de documentação gerada do
modelo. Além dos defeitos de mecânica, fez uma crítica às cegas: comparou o texto gerado com a
descrição de domínio do repositório público `ddd-by-examples/library`, sem rótulo, e escolheu o
outro. O texto de referência dizia em prosa quem age, sobre o quê e quando; o gerado abria
explicando como tinha sido gerado e depois listava mapas de borda, com dezesseis de trinta valores
externos que eram identidade sem conteúdo. E faltava o mapa de contextos, que o modelo tinha
[CLAIM-08-046]. A entrega seguinte consertou a mecânica (o portão passou a regerar do modelo) e
reprovou de novo na pergunta de quem opera [CLAIM-08-047]. Geração garante consistência entre o
modelo e o texto. Não garante que o texto responda à pergunta de quem lê. Essa parte continua
sendo escrita, e julgada, por gente.

**Descoberta onde não há distância.** Rodar *Event Storming* num projeto em que quem decide é quem
usa é cerimônia: o Maestro avaliou e deixou em observação exatamente por isso [CLAIM-08-021]. O
vocabulário sai da conversa que abre o ciclo e vai direto para a spec e o plano.

**Prometer o vocabulário que não existe.** O achado 055 é o contraexemplo da regra mal aplicada:
instruir o agente a "consumir a linguagem ubíqua" num projeto que não tem uma é pior que não
dizer nada, porque o agente segue a instrução e preenche o vazio com confiança. Se o seu projeto
ainda não tem modelo de domínio, a instrução certa é "proponha o vocabulário no plano e diga onde
ele vai morar", não "use o vocabulário".

## Evidência

O que sustenta o capítulo, separado pelo estado de cada afirmação. A tabela completa, com a
evidência reproduzível de cada claim, está em [`claims.md`](claims.md); o script
`exemplo/medir_maestro.sh` reproduz os números do Maestro num clone.

**Medido** (reproduzível por comando na versão citada): os nove planos de nove com as quatro
declarações de domínio de 067 a 076 [CLAIM-08-028]; o piso do portão e a recusa do valor que
afrouxa [CLAIM-08-027]; a composição do `model.yaml`, com nove contextos, dez palavras proibidas e
quinze de 31 linhas de mapa que não são 1:1 [CLAIM-08-030, CLAIM-08-033, CLAIM-08-034]; a forma
itemizada do plano do 075 [CLAIM-08-025]; a saída do exemplo executável [CLAIM-08-043].

**Observado** (registrado em commit, spec, ADR, relatório ou índice de decisões do Maestro): a
falha do Hindiana e a correção da mesma noite [CLAIM-08-001 a CLAIM-08-004]; o achado 055 e seu
fechamento [CLAIM-08-005, CLAIM-08-006]; as cinco colisões de nomes e a invariante de endereço
[CLAIM-08-009 a CLAIM-08-011]; os quatro vocabulários para o mesmo estado que motivaram o ADR
0029 [CLAIM-08-017]; a reprovação da documentação gerada, nas duas rodadas [CLAIM-08-032,
CLAIM-08-046, CLAIM-08-047]; as medições da jornada do ciclo 074 [CLAIM-08-037, CLAIM-08-038].

**Hipótese** (não medida; agenda da pesquisa). As hipóteses H6, o catálogo semântico reduz
duplicação, e H7, o glossário reduz inconsistência, são o que este capítulo mais gostaria de
afirmar e o que menos pode [CLAIM-08-014]. Os casos acima mostram que, **sem** declaração cobrada,
regra de negócio foi parar na borda duas vezes, e que **com** ela todos os planos seguintes
declararam o domínio. Não mostram que o código ficou com menos sinônimos, porque ninguém contou
sinônimos antes e depois. O desenho que testaria H6 e H7 está no [capítulo
15](../15-validando-o-maestro/capitulo.md): a mesma tarefa, com e sem catálogo, em várias sessões
independentes, contando identificadores distintos por conceito. O passo 1 do exemplo é o esboço
dessa métrica: nomes propostos por conceito, antes e depois do catálogo. Duas métricas servem ao
tech lead desde já, desde que não virem meta:

- **Identificadores por conceito**: para os dez termos mais usados do seu domínio, quantos nomes
  diferentes existem no código. O alvo é um.
- **Planos sem declaração de domínio**: quantos planos do último mês não dizem onde moram as
  invariantes. O alvo é zero, e o número mais interessante é quantos dizem `edge`, e por quê.

## Checklist

Itens que você aplica no seu time na segunda-feira; cada um tem um jeito de verificar.

- [ ] Existe **um** arquivo de modelo de domínio lido por máquina, com termo de tela,
      identificador, contexto dono e definição. Verificação: `ls` acha um, não três.
- [ ] O glossário e a documentação de domínio são **gerados** desse arquivo, e a integração
      contínua regera **do modelo** e compara. Verificação: edite uma definição à mão e veja a CI
      ficar vermelha.
- [ ] Todo plano declara raiz de agregado, onde moram as invariantes, mudanças de vocabulário e
      portas, cada uma com motivo. Verificação: um script lê as quatro linhas e reprova a
      ausência.
- [ ] Regra de negócio na borda só com o motivo escrito. Verificação: `edge` sem motivo reprova
      no plano.
- [ ] Nome novo proposto por agente passa por REUSE / ALIAS / EXTEND / CREATE antes de virar
      código; CREATE sem definição é recusado. Verificação: a lista de termos novos do plano bate
      com o diff do modelo.
- [ ] As palavras com dois sentidos estão mapeadas, e as que nunca se escrevem nuas estão numa
      lista que um *lint* lê. Verificação: o *lint* acusa a palavra nua num texto de teste.
- [ ] Endereço ambíguo é recusado. Verificação: mande uma mensagem para um nome que existe em
      dois projetos e confira que nada foi entregue.
- [ ] Toda sigla nasce por extenso na primeira ocorrência de cada documento. Verificação: o
      *lint* de siglas roda nos documentos que vão para pessoas.
- [ ] A língua de cada artefato é decidida pelo leitor (tela, código, instrução de agente), e o
      mapa entre a palavra de tela e o identificador está escrito. Verificação: um check de
      resíduo de língua na superfície que outro repositório consome.
- [ ] Cada régua de vocabulário tem fixture boa e fixture ruim, e foi vista falhando.
      Verificação: rode a régua contra a fixture ruim antes de confiar no verde.
- [ ] A instrução dos agentes não promete um vocabulário que não existe. Verificação: todo
      caminho citado na instrução resolve.

## Referências

Fontes do Maestro, todas na versão `19823c2`:

- Axiomas, teoremas e corolários (A4, T3, T5, C7, C10):
  <https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/axioms.md>
- Constituição, Princípio VIII:
  <https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/principles.md>
- Glossário (colisão de nomes, colisão de endereço, termos de DDD):
  <https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/glossary.md>
- ADR 0010 (Princípio VIII):
  <https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0010-principio-viii-comunicacao-inteligivel.md>
- ADR 0014 (inglês no instalável):
  <https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0014-ingles-no-instalavel.md>
- ADR 0023 (modelo de domínio declarado no plano):
  <https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0023-modelo-de-dominio-declarado-no-plan.md>
- ADR 0029 (tela em português, código em inglês):
  <https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0029-tela-em-portugues-codigo-em-ingles.md>
- Specs dos ciclos 001, 067, 074 e 075; mapa de contextos do 073; críticas das tarefas T035b e
  T035c/T036 do 076: <https://github.com/GHDaru/maestro/tree/19823c2/specs>
- Índice de decisões (achado 055 e retro 061):
  <https://github.com/GHDaru/maestro/blob/19823c2/docs/records/decisoes.jsonl>
- Cartão de ideia 038 (técnicas de descoberta):
  <https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/ideias/038-tecnicas-de-descoberta.md>
- Modelos de plano e de ux-design:
  <https://github.com/GHDaru/maestro/tree/19823c2/.specify/templates>
- Scripts `check-conformance.sh`, `check-language.sh`, `check-docs-generated.sh`:
  <https://github.com/GHDaru/maestro/tree/19823c2/scripts>
- Modelo de domínio do painel:
  <https://github.com/GHDaru/maestro/blob/19823c2/painel/servidor/dominio/model.yaml>
- Agentes `ux-semantics` e `didactics-editor`:
  <https://github.com/GHDaru/maestro/tree/19823c2/.claude/agents>
- Skill `fight-the-pile-up`:
  <https://github.com/GHDaru/maestro/blob/19823c2/skills/fight-the-pile-up/SKILL.md>
- Jornada viva do protótipo navegável:
  <https://github.com/GHDaru/maestro/blob/19823c2/docs/jornada/074-prototipo-navegavel.md>
- Diagramas do processo (*Suppliers, Inputs, Process, Outputs, Customers* (SIPOC) e
  *Business Process Model and Notation* (BPMN)):
  <https://github.com/GHDaru/maestro/tree/19823c2/docs/diagramas>
- Guia editorial do livro do Maestro:
  <https://github.com/GHDaru/maestro/blob/19823c2/docs/livro/guia-editorial.md>

Fontes externas (bibliografia; as páginas web não foram reacessadas na redação desta versão,
o que fica como pendência da revisão):

- Evans, Eric. *Domain-Driven Design: Tackling Complexity in the Heart of Software*.
  Addison-Wesley, 2003.
- Vernon, Vaughn. *Implementing Domain-Driven Design*. Addison-Wesley, 2013.
- Fowler, Martin. "UbiquitousLanguage" e "BoundedContext", bliki:
  <https://martinfowler.com/bliki/UbiquitousLanguage.html>,
  <https://martinfowler.com/bliki/BoundedContext.html>
- Cockburn, Alistair. "Hexagonal Architecture" (portas e adaptadores), 2005.
- Brandolini, Alberto. *Introducing EventStorming*. Leanpub.
- `ddd-by-examples/library` (exemplo público de DDD usado como comparação na crítica da T035b):
  <https://github.com/ddd-by-examples/library>
