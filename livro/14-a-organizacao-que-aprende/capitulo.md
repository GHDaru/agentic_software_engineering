# 14 — A organização que aprende

> "A correção feita na conversa tem a vida de uma sessão; só a regra versionada chega à
> próxima." — teorema T6 do Maestro, parafraseado

Todo time que trabalha com agentes descobre, em algumas semanas, que corrige as mesmas coisas: o
padrão de nome, o teste do caso de falha, o registro no changelog. A reação natural é escrever
mais regra, e o corpo de regras incha até ninguém lê-lo. Este capítulo trata de duas forças que
precisam andar juntas: **aprender**, transformar a correção que se repete em regra que se cobra
sozinha, e **podar**, tirar o que não paga o próprio custo. Para o tech lead que decide o que vira
processo, aqui está o critério das duas decisões, e a prova, num repositório real, de que ele
também falha quando ninguém o cobra.

## Pergunta central

Como uma correção vira regra que sobrevive à próxima sessão do agente, sem que a governança
inche até ser ignorada?

## Resultado de aprendizagem

Ao final, você consegue:

1. **Distinguir** correção de regra: dizer, para uma correção que você fez a um agente, se ela
   vai sobreviver à próxima sessão e o que falta para isso (artefato versionado, consumidor,
   cobrança).
2. **Dar gatilho mensurável** a uma cerimônia, em especial à retrospectiva, de modo que ela
   aconteça por dívida acumulada e não por lembrança ou calendário.
3. **Escolher o destino** da regra nova (princípio, modelo operacional, skill, script ou
   registro de decisão) pela natureza dela, e justificar a escolha.
4. **Auditar os artefatos** do seu time pelo teste das duas perguntas (quem consome? o que
   quebra quando fica velho?) e decidir o que cobrar, o que tornar imutável e o que podar.
5. **Manter memória só-anexar**: corrigir um registro de decisão sem reescrevê-lo, e montar o
   portão que impede a reescrita.

## A falha real

Em 2 de agosto de 2026, o ciclo 027 do Maestro migrava para o padrão editorial novo o capítulo
do handbook sobre cerimônias. Para escrever a seção prática, o autor contou as retrospectivas do
próprio projeto e registrou o resultado no relatório de qualidade: em 26 ciclos, a
retrospectiva tinha sido executada **uma vez**, no ciclo 017, e só porque o Steward (o humano que
responde pelo método) a cobrou [CLAIM-14-001]. A cerimônia que o modelo operacional chamava de
"a de maior retorno" era também a mais adiada.

A ironia era dupla. A única retrospectiva executada, a do ciclo 017, tinha produzido exatamente o
anti-padrão que descreve isso. Duas vezes, nos relatórios dos ciclos 015 e 016, alguém escrevera
"candidato a anti-padrão" sobre um defeito de verificação, e a retro não rodou nenhuma das duas
[CLAIM-14-002]. A retro do 017 batizou o fenômeno de **anti-padrão 14, "achado que morre em
candidato"**, e escreveu a meta-lição no relatório: o processo não falhara por falta de norma,
mas por norma sem função de força. No ciclo 027, a norma "rode a retrospectiva" continuava sem
função de força nenhuma.

O ciclo 027 fez o certo pela metade. Registrou o fato no índice de decisões, um arquivo JSON Lines
(JSONL), em que cada linha é um objeto JavaScript Object Notation (JSON) com uma decisão ou um
achado, como `achado-027-retro-sem-gatilho`, status `aberta`, e deixou a pergunta: qual gatilho,
número de ciclos, de achados abertos, ou ambos?
([`qa-report.md` do 027](https://github.com/GHDaru/maestro/blob/19823c2/specs/027-capitulo-07-padrao-v2/qa-report.md)).
O achado se juntou a outros quatro na mesma situação: a régua de raias não aplicada (023), a
regra nova de uma skill que não chegava ao capítulo (029), a citação do ciclo no commit só por
convenção (031) e o renome em massa que quebrava link (033).

No dia seguinte, o ciclo 034 deu o relógio. Antes de escrever qualquer regra, escreveu o portão
`check-retro.sh` e o rodou contra o índice real: vermelho, **cinco achados abertos, o mais velho
com onze ciclos** [CLAIM-14-003]. A retrospectiva rodou, os cinco achados viraram quatro
portões e dois anti-padrões novos (17, "cerimônia sem gatilho", e 18, "renome em massa por
substituição de texto") [CLAIM-14-053], e a linha `retro-034` entrou no índice
([commit `7264fe6`](https://github.com/GHDaru/maestro/commit/7264fe6)).

E aí veio a parte que transforma a história em lição. O protocolo para fechar um achado foi
inventado no meio da retro e nasceu errado. As cinco primeiras linhas de fechamento tinham ids
novos, diziam em prosa que fechavam os achados e não apontavam para eles: o `check-retro.sh`
continuou vendo os cinco abertos [CLAIM-14-004]. O fechamento existia no texto e não no dado.
A correção foi um campo estrutural, `fecha`, que liga a linha de fechamento ao id do achado; o
portão passou a ler o campo, nunca a frase. O executor reconheceu ali o anti-padrão 13 (o
check que mede o proxy) aplicado ao próprio registro, com uma diferença: desta vez o check
acusou antes do commit.

O gatilho tocou sozinho pela primeira vez em 7 de agosto, no ciclo 041: quatro achados abertos
no teto de quatro, sem ninguém lembrar da cerimônia [CLAIM-14-005]. Essa retro achou uma coisa
que nenhuma retro por memória teria achado: **a ferramenta que prepara o material da retro
mentia**. O `retro.sh` reconhecia gates pelo formato `gate-NNN-*`, usado por sete gates, enquanto
o script de promoção gravava `gate-main-<sha>` desde a decisão que automatizou o registro, e já
eram 33. Todo ciclo do 011 em diante aparecia como gate pendente: vinte e nove ciclos de um
instrumento com crédito e sem verdade [CLAIM-14-006]. A memória não desconfia do próprio
instrumento; um gatilho que obriga a olhar, sim.

Em uma semana de agosto, o Maestro passou de "a retro acontece quando alguém lembra" para "a
retro acontece quando a dívida passa do limite, e o fechamento é um fato no dado". O resto deste
capítulo explica por que essa é a forma certa, quanto ela custa, e onde ela ainda falha.

## Teoria

### Por que a correção não sobrevive: o teorema T6

O Maestro deriva suas regras de cinco axiomas [CLAIM-14-036]
([`axioms.md`](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/axioms.md)).
Dois deles bastam para este capítulo. O **A3** diz que o contexto do agente é finito e se degrada
ao encher. O **A4** diz que só sobrevive o que está escrito: o agente começa cada sessão do zero,
e o que não está num artefato não existe para a próxima execução. Deles sai o **teorema T6**: a
correção que não vira regra se repete. Uma correção feita na conversa vive uma sessão; a janela
da próxima não a contém, e o agente não lembra da anterior.

Num time só de pessoas, a melhoria que sai da retrospectiva é um hábito mole, que depende de
alguém lembrar. Com agentes, ela pode ser outra coisa: uma **instrução versionada**, num arquivo
que o agente lê no começo de toda sessão, numa skill ou num script que falha. A diferença é a
que separa "combinamos de tomar cuidado" de "o comando falha se não tomarmos". O modelo
operacional do Maestro diz isso numa linha: toda correção recorrente feita a um agente tem de
virar instrução versionada, e a retrospectiva é a cerimônia de maior retorno
([`operating-model.md` §5](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/operating-model.md)).

A evidência que o `axioms.md` registra para T6: o anti-padrão 13
("check que mede o proxy") recorreu **quatro vezes** antes de o antídoto virar lei numa skill, e
a retrospectiva, ela mesma uma regra, ficou trinta e três ciclos sem gatilho [CLAIM-14-007]. O
teorema não fala só do agente: o operador humano, que também tem atenção finita, está sujeito a
ele. A regra "rode a retro" sofreu de T6 exatamente como as correções que ela deveria capturar.

Daí o **corolário C1**: toda cerimônia tem gatilho, e o gatilho é mensurável. E o **anti-padrão
12**, "corrigir a mesma coisa duas vezes": a correção recorrente que nunca virou regra é falha de
processo, não do agente. Quando o seu agente erra pela terceira vez o mesmo padrão, a pergunta
útil não é "por que ele errou?", mas "onde está a regra que ele deveria ter lido, e o que a
cobra?".

A teoria organizacional clássica chama isso de aprendizado de laço duplo (*double-loop
learning*, Argyris e Schön): corrigir o erro é o laço simples; mudar a regra que produziu o
erro é o laço duplo. Com agentes, o laço simples é quase inútil, porque não deixa memória
nenhuma; só o duplo acumula.

### Por que a regra também apodrece: o teorema T5

Se T6 fosse a história inteira, a resposta seria "escreva tudo". Não é, porque escrever cria um
segundo problema. Manter um artefato atualizado custa atenção, que é o recurso escasso (A3), e
o que não se lê não se mantém. Do mesmo par de axiomas sai o **teorema T5**: um artefato
sobrevive por **consumo** ou por **imutabilidade**. Sobrevive o que algo a jusante consome e
que falha alto quando está velho; e sobrevive o que descreve um instante e, por isso, nunca fica
velho. Tudo o mais apodrece, por melhor que seja (**corolário C9**).

O teste prático, no handbook, tem duas perguntas: *quem consome este artefato?* e *o que quebra,
alto, quando ele fica velho?* A spec passa nas duas: o agente gera código dela, e spec velha vira
código errado. O teste automatizado passa: a integração contínua (CI, de *continuous
integration*) o executa, e teste velho fica vermelho. Um documento de design avulso não passa em
nenhuma das duas, e por isso apodrece.

O Princípio VI do Maestro é a forma normativa de T5: um artefato só existe se for insumo
consumido com função de força, ou imutável, como o registro de decisão; e a cadeia spec ↔ pull
request ↔ testes ↔ jornada é a memória durável do projeto
([`principles.md`](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/principles.md)).
Há um corolário de corte: **duplicar função é como o apodrecimento começa**; de dois artefatos
com a mesma função, um é atualizado e o outro fica para trás parecendo válido. O documento de requisitos de produto (PRD, de *product
requirements document*) avulso duplica a spec; o documento de design ou a *request for comments*
(RFC) avulsa duplicam plano mais registro de decisão. A pergunta de corte é também "alguém vivo
já faz isso?".

A segunda forma de sobreviver, a imutabilidade, é a do registro de decisão de arquitetura
(ADR, de *architecture decision record*), na forma que Michael Nygard propôs em 2011: contexto,
decisão, consequências. Um ADR descreve um instante, o que se sabia, o que se decidiu e o preço
aceito. Ele nunca fica desatualizado; no máximo fica **superado**, e o sucessor o diz
explicitamente. É a única categoria de documento que envelhece sem apodrecer. Em troca, exige
disciplina de outra natureza: nunca reescrever o mérito, e sempre acrescentar.

### As duas forças, e o modo de falha de cada uma

T6 empurra para adicionar regra; T5 empurra para cortar o que não é consumido. Uma governança
saudável precisa das duas, e cada uma tem o seu modo de falha.

O modo de falha de quem só aprende é a **ossificação**. Regras acumulam porque adicionar é barato
e remover é politicamente caro: cada regra nasceu de uma dor real, e remover exige argumentar
contra uma dor que existiu. Sem uma força contrária explícita, o conjunto endurece; ninguém sabe
quais regras estão vivas, e a resposta racional de quem opera é ignorar tudo o que não for
cobrado. A versão mais
visível disso é o **teatro de cerimônia** (anti-padrão 11): o processo que não muda decisão
nenhuma, o gate que nunca rejeita. Se um portão nunca ficou vermelho, ele é decoração e deve ser
podado.

O modo de falha de quem só poda, ou de quem aprende sem cobrar, é o **artefato que congela**
(anti-padrão 15): o roadmap ou o índice que para de ser atualizado e continua parecendo válido.
O Maestro tem o caso de origem e o caso reincidente. No ciclo 017, o roadmap tinha parado no
ciclo 009 enquanto sete ciclos aconteciam fora do mapa [CLAIM-14-008]. Em 10 de agosto, no ciclo
046, o índice de ADRs estava congelado desde o 0017: os ADRs 0018 e 0019 existiam e não estavam
listados, e o 0017 aparecia como "Aceito" sete ciclos depois de ter sido superado
[CLAIM-14-009]. Um índice que lista como vigente uma decisão revertida não está incompleto, está
**errado**, e quem o consulta, pessoa ou agente, decide com base nele.

O ciclo 039 mostra o mesmo defeito do lado da memória. O Steward reverteu a divisão do
repositório em dois, e o ADR 0018 superou o 0017; mas o 0017 continuava "Aceito", o roadmap dizia
"F14b — aguarda gate humano" e o `boundary.json` descrevia dois repositórios: a próxima sessão
leria "vamos separar" como verdade vigente [CLAIM-14-010]. É o axioma A4 cobrando o preço: o que
está escrito sobrevive, inclusive quando está errado. O mesmo ciclo viu que a lista de perfis de
agente era escrita à mão e saudável só por memória, e criou o `check-roles.sh`, que a compara com
as definições em disco, visto falhar em quatro condições antes de entrar [CLAIM-14-047].

### Camadas com velocidades diferentes

A arquitetura que equilibra as duas forças tem camadas que mudam em ritmos diferentes:

| Camada | Muda | Como |
|---|---|---|
| Constituição (princípios) | devagar | emenda versionada, com registro de decisão |
| Modelo operacional e livro | rápido | versão própria, subordinada à constituição |
| Registros de decisão | nunca | imutáveis; um novo pode superar o anterior |
| Skills e scripts | conforme a dor | nascem de retrospectiva, com lei própria |

O documento que muda toda semana não é o mesmo que sustenta as decisões de meses. E o registro
imutável e superável dá **reversibilidade à decisão**: preserva a liberdade de mudar de ideia e a
memória de por que se pensava diferente, a reversibilidade do
[capítulo 11](../11-risco-reversibilidade-e-autonomia/capitulo.md) aplicada à governança.

Há uma terceira peça que costuma faltar: a **poda escrita**. YAGNI (*you aren't gonna need it*,
"você não vai precisar disso") é poda ativa com gatilho: a complexidade além do necessário é
justificada por escrito ou removida, e a decisão adiada carrega uma condição escrita de revisão,
que transforma "vamos observar" num evento. E **o que não se adota também se escreve**, para não
reabrir a mesma discussão a cada trimestre.

## Alternativas

Há várias formas conhecidas de fazer um time aprender. Elas não se excluem, e só algumas
sobrevivem ao fato de que metade do seu time agora esquece tudo entre uma sessão e outra.

**Retrospectiva de calendário (Scrum, Derby e Larsen).** A retro no fim de cada sprint, com
formato facilitado (o que foi bem, o que foi mal, o que mudar). Funciona para pessoas, que
carregam o combinado na cabeça. Com agentes, o combinado não carrega: se a saída da retro não
virar artefato lido pelo agente, ela não existe para ele. E o calendário cria o problema inverso,
a retro sem matéria, que vira teatro. **Veredito**: a cerimônia fica, o gatilho por calendário
sai. Use dívida de achados como gatilho, e exija destino executável para cada resposta "sim".

**Postmortem sem culpa (a cultura de engenharia de confiabilidade de sites, SRE, do Google).**
Documento escrito depois de um incidente, com linha do tempo, causa raiz e ações com dono. É o
melhor modelo para o incidente grande e raro, e a regra "sem culpa" vale integralmente com
agentes: a falha recorrente é do processo, não do agente (anti-padrão 12). Mas o postmortem é
disparado por incidente; a maior parte do que um time de agentes precisa aprender são correções
pequenas e repetidas que nunca chegam a ser incidente. **Veredito**: adote o formato para o
incidente; para a correção recorrente, use o achado registrado e a dívida.

**Registro de decisões de arquitetura (Nygard; MADR).** ADR em arquivos de texto no repositório,
com o formato de contexto, decisão e consequências; o *Markdown Architectural Decision Records*
(MADR) é a variante com campos para alternativas consideradas. Resolve a memória do porquê, e é
imutável por desenho. Não resolve, sozinho, a descoberta: sem índice e sem curadoria vira arquivo
morto, e o índice escrito à mão congela (o caso do 0017 acima). **Veredito**: adote, com o
índice verificado por portão.

**Processo de RFC.** Proposta escrita, circulada para comentários de um grupo amplo antes da
decisão. Útil quando há muitas partes interessadas e decisões de longo alcance. Num time de um
humano regendo agentes, duplica o que plano mais ADR já fazem, e o custo de circulação não paga.
**Veredito**: rejeitado como processo pesado; a decisão vai para o ADR, a discussão para o plano.

**"Adicionar sempre" (o *playbook* que só cresce).** Toda dor vira item no documento de boas
práticas, o arquivo de instrução do agente ganha um parágrafo por incidente. É a alternativa mais comum e a que
leva direto à ossificação, com um agravante agêntico: o arquivo de instrução lido no começo de
cada sessão consome contexto, e A3 diz que contexto cheio degrada o agente. **Veredito**:
rejeitado. Toda regra nova tem destino escolhido pela natureza, e a retro também poda.

Uma nota sobre ferramentas. Os *toolkits* de desenvolvimento orientado por especificação (como o
GitHub Spec Kit) trazem um comando para criar e emendar uma "constituição" do projeto. Quando o
projeto já tem uma, preencher o template do toolkit cria a **segunda fonte de verdade** (T5). No
ciclo 048, o Maestro manteve o template do upstream intacto e **sem uso**, e apontou o comando
para a constituição única do método
([`.specify/UPSTREAM.md`](https://github.com/GHDaru/maestro/blob/19823c2/.specify/UPSTREAM.md)).
A ferramenta é intercambiável; a regra de não duplicar função não é.

## O padrão Maestro

O Maestro responde à pergunta do capítulo com as peças abaixo. Para cada uma, digo o que é regra
(texto que um agente lê), o que é script (portão que falha) e o que é hook (guarda que recusa
antes de a ação acontecer). Tudo citado em `maestro@19823c2`.

### 1. O achado registrado e a dívida como gatilho

**Regra.** Todo achado que não coube no ciclo entra no índice de decisões
`docs/records/decisoes.jsonl` como `achado-NNN-<slug>`, com status `aberta`. O ciclo que o
encontra não o resolve à força; registra. A receita de rodar a retro
([`receitas/rodar-a-retro.md`](https://github.com/GHDaru/maestro/blob/19823c2/docs/receitas/rodar-a-retro.md))
diz que o gatilho é dívida, não calendário.

**Script.** O `check-retro.sh` lê o índice, calcula os achados abertos (os que nenhuma linha
fecha pelo campo `fecha`) e falha com quatro ou mais abertos, ou com um aberto há seis ciclos ou
mais [CLAIM-14-011]
([`scripts/check-retro.sh`](https://github.com/GHDaru/maestro/blob/19823c2/scripts/check-retro.sh)).
O cabeçalho do script registra a decisão de desenho que a falha real ensinou: a ligação é
estrutural (um campo), nunca textual, porque um fechamento reconhecido pela prosa seria um check
medindo as palavras em vez do fato.

O gatilho mudou o comportamento observável. Antes do 034, uma retro em 26 ciclos
[CLAIM-14-001]; depois, a
retro passou a ser disparada pela dívida: no ciclo 041 (quatro achados de avaliação, mais o
`retro.sh` mentindo), no 055, no 061 e outros. A spec do ciclo 061 mostra a dinâmica que o
desenho queria: o ciclo 060 **indexou três achados novos em vez de segurá-los para manter o
número verde**, o gatilho foi a vermelho com cinco abertos (limite quatro), e a retro rodou
[CLAIM-14-012]
([spec 061](https://github.com/GHDaru/maestro/blob/19823c2/specs/061-retro-da-caixa-marcada-sem-testemunha/spec.md)).

**O preço desse gatilho** também está escrito. O portão roda na CI como consultivo, e no ciclo
055 estava vermelho desde o 053, com um achado de oito ciclos, enquanto cada ciclo novo empurrava a
dívida [CLAIM-14-013]. O achado tinha sido remediado virando gatilho de reavaliação e ficou aberto
à espera de um evento que podia nunca vir: a dívida passou a medir calendário. A correção foi dar
forma ao fechamento "virou gatilho", nomeando o gatilho no ato.

Cada retro disparada pela dívida deixou um rastro executável, que é o que a distingue da conversa
boa. A do 041 transformou os achados sobre avaliações de agentes em três anti-padrões novos (19,
20 e 21) [CLAIM-14-054] e numa regra de aposentadoria: um caso de avaliação só sai do corpus com
motivo escrito e impresso em toda execução, porque aposentar em silêncio é esconder vermelho. A do
055 viu que, em seis de nove ciclos, a revisão independente achara portão que mede a frase e não
o fato, e tornou obrigatório, em todo ciclo que cria ou altera portão, o `TAIL:mutation`: a prova
de que o portão foi visto reprovar [CLAIM-14-046]
([commit `0e82c8c`](https://github.com/GHDaru/maestro/commit/0e82c8c)). A do 061 tornou
bloqueante a metade checável da conformidade (o modo `--ticked-only`: caixa marcada exige
evidência) e corrigiu o portão de capítulos, que comparava datas de commit e por isso não
disparava dentro do ciclo que desatualizava um capítulo.

### 2. As três perguntas e o destino da regra

**Regra.** A retro responde três perguntas, e cada "sim" tem destino:

| Pergunta | Se "sim" |
|---|---|
| Que erro ou correção se **repetiu**? | vira regra versionada |
| Que regra existente **não pagou** o custo? | poda (YAGNI) |
| Que passo manual se repetiu **idêntico**? | vira script ou skill |

O destino da regra nova depende da natureza dela: inegociável e válida para todo o método vai
para a **constituição** (sobe versão, exige ADR); regra do dia a dia vai para o **modelo
operacional** (sobe versão); procedimento recorrente vira **skill**, com lei de ferro e linha de
base testada; passo mecânico repetido vira **script**; decisão pontual com alternativas vira
**ADR**. A segunda pergunta é a que a maioria dos times esquece. Sem ela, a retro é uma máquina
de adicionar.

**Script.** O `retro.sh` pré-calcula o material (ciclos, vereditos, gates pendentes, decisões,
inventário) e é somente leitura por declaração no cabeçalho: não decide nada, só elimina o
"recarregar o contexto de cabeça". A retro continua cerimônia humana. A ideia de
retrospectiva como comando, e não como reunião, veio do estudo de outro repositório do autor (o
`maestro-02`, ideia 007, observada em 31/07/2026 com veredito "absorver"), junto com a do índice
consultável por máquina (ideia 006) [CLAIM-14-055]
([ideia 007](https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/ideias/007-retro-executavel.md);
[ideia 006](https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/ideias/006-registro-consultavel-jsonl.md)),
e ambas entraram no ciclo 008 com o catálogo de anti-padrões
([spec 008](https://github.com/GHDaru/maestro/blob/19823c2/specs/008-absorcoes-maestro-02/spec.md)).

O exemplo mais curto do laço inteiro é o primeiro uso desse script. Rodado no ciclo 008, o
`retro.sh` mostrou que os relatórios dos ciclos 003 a 007, já promovidos à linha principal,
ainda diziam "aguarda aprovação humana": o gate tinha sido exercido na conversa, e o artefato
não o registrava [CLAIM-14-014]. O resultado foi o ADR 0009: o índice de decisões vira a fonte do
estado dos gates de merge, o `promote-main.sh` anexa `gate-main-<sha>` sozinho depois da
confirmação humana, e os gates 003 a 007 foram registrados retroativamente
([ADR 0009](https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0009-registro-automatico-gate-merge.md)).
Ferramenta achou a falha, a falha virou regra, a regra virou código, em dois ciclos
[CLAIM-14-051].

### 3. O catálogo de anti-padrões como memória do que já custou caro

**Regra (skill).** O catálogo `skills/anti-patterns/SKILL.md` tem 23 itens [CLAIM-14-015], e a lei
de ferro dele é "nomeie o anti-padrão antes de corrigir". Cada item tem origem datada, e o
histórico do arquivo mostra quando cada leva entrou: a retro do 017 trouxe 13, 14 e 15 e a
segunda lei da verificação ("um check que você nunca viu acusar não é um check, é uma
esperança"); a do 034 trouxe 17 e 18; a do 041 trouxe 19, 20 e 21 [CLAIM-14-054]. É a forma
versionada da pergunta 1: aprender é adicionar o que já custou caro.

Os itens que este capítulo usa como lentes:

- **11, teatro de cerimônia**: processo que não muda decisão; gate que nunca rejeita é teatro.
- **12, corrigir a mesma coisa duas vezes**: correção recorrente que não virou regra é falha de
  processo.
- **14, achado que morre em candidato**: o laço retro → regra só existe se for executado.
- **15, artefato de planejamento que congela**: está vivo ou está morto.
- **17, cerimônia sem gatilho**: toda cerimônia recorrente declara gatilho mensurável, e uma
  checagem falha quando ele dispara sem a cerimônia.

O catálogo também mostra o limite do próprio catálogo. O anti-padrão 21 (um `grep -q` no fim de
um *pipe* sob `pipefail`, que mata o script ou inverte o resultado) nasceu na retro do 041,
quando a correção do `retro.sh` quebrou por esse motivo. No ciclo 063, um achado registrou que
ele tinha sido **fechado pontualmente sete vezes e reaparecido todas**; havia quatro ocorrências
vivas, e nenhum portão procurava a forma [CLAIM-14-016]. O achado fecha com a frase que resume
T6 melhor do que o próprio teorema: um anti-padrão que só a atenção pega não está fechado.

### 4. Memória só-anexar, com guarda

**Regra.** Nunca reescrever o que o método guarda como histórico: o corpo de um ADR já no Git, as
linhas passadas do índice de decisões, os cartões datados do catálogo do ecossistema. A rota é
sempre anexar: um ADR novo que supera o anterior, uma linha nova no índice
([`CLAUDE.md`](https://github.com/GHDaru/maestro/blob/19823c2/CLAUDE.md)).

**Script.** O `record-decision.sh` anexa uma decisão validando JSON numa linha só, campos
obrigatórios e unicidade do id; a correção é uma linha nova com status `superseded by <id>`. Duas
marcas mostram a regra levada a sério: as chaves do JSON ficaram em português (`data`, `titulo`,
`registro`) depois que o método instalável passou ao inglês, porque traduzir linhas imutáveis
quebraria a regra [CLAIM-14-017]; e, no ciclo 045, depois de duas linhas citarem um relatório em
branco, o script passou a recusar marcador de preenchimento [CLAIM-14-018]. Em `19823c2`, o
índice tem 199 linhas, de 22 de julho a 1º de novembro de 2026: 50 `gate-main-*`, 48 `achado-*`,
32 `adr-*`, 28 `gate-*`, 18 `retro-*`, 16 `decisao-*` e sete linhas de quatro formas avulsas; 31
carregam o campo `fecha`, e nenhum id se repete [CLAIM-14-019]. Na captura do handbook, em
agosto, eram 38 linhas, 21 delas gates de merge [CLAIM-14-020]. Ninguém o mantém à mão, e por
isso ele cresce sem custo de manutenção.

**Hook.** Até o ciclo 056, nada impunha essa imutabilidade: os portões conferiam forma, nunca
imutabilidade, e a regra vivia em prosa. O ciclo 056 instalou o `guard-immutables.py`, que roda
antes de cada uso de ferramenta de edição e **recusa** reescrever o que está no histórico do Git
([`scripts/hooks/guard-immutables.py`](https://github.com/GHDaru/maestro/blob/19823c2/scripts/hooks/guard-immutables.py)).
A primeira versão tratava "o arquivo existe" como imutável e bloqueava a escrita de um ADR novo a
partir da segunda chamada; a revisão independente achou o defeito, e a definição virou "já está
no Git" [CLAIM-14-021]. O cabeçalho declara os limites: a guarda não vigia o *shell*, e um
`sed -i` alcança o corpo de um ADR. Um portão audita depois do dano; uma guarda recusa antes.
Nenhum dos dois cobre tudo.

O catálogo do ecossistema repete o padrão: o `estado.jsonl` tem 52 linhas só acrescentadas, e a
última de cada ideia é o veredito vigente [CLAIM-14-022]; o `check-ecosystem.sh` exige que uma
ideia "absorvida" aponte o arquivo que prova a absorção e recusa "observar" sem gatilho. Foi por
ele que a revisão reprovou o ciclo 047: seis vereditos tinham sido trocados e **retrodatados**
(uma linha de 30 de julho afirmando o que aquele dia não decidiu), e foram corrigidos no ciclo e
reverificados por 13 mutações [CLAIM-14-023]. Reescrever o passado tenta até quem escreveu a
regra.

**A imutabilidade se verifica contando, sem arredondar.** No ciclo 028, o handbook quase publicou
"dez ADRs, dez commits, imutabilidade perfeita"; a contagem mostrou o 0008 com dois commits, o
segundo só de status [CLAIM-14-024]. Em `19823c2`, dos 30 ADRs (0004 a 0033), 16 têm um commit;
nos que abri, o segundo é renome de caminho (o 0004) ou troca de status (o 0017, "Superado pelo
ADR 0018", com a nota de que "o corpo abaixo fica intacto") [CLAIM-14-025]. A regra não é "um
commit por ADR"; é "o mérito nunca muda", e isso só se afirma lendo o diff.

### 5. Portões contra o artefato que congela

Um índice escrito à mão sobre arquivos legíveis por máquina envelhece em silêncio. A spec do
ciclo 050 deu nome à forma, "cópias de um fato mantidas em acordo pela memória", e a contou cinco
vezes no repositório: o índice de perfis de agente, o índice de ADRs, a tabela de proveniência, a
cópia instalada e a versão [CLAIM-14-026]. A resposta em cada caso foi um portão que compara a
cópia com a fonte:

- **`check-adr.sh`** (ciclo 049): todo ADR em disco está no índice, todo item do índice aponta
  para arquivo real, e o status concorda, incluindo "superado". Foi visto acusar o defeito
  original reconstruído por mutação
  ([commit `71b79c1`](https://github.com/GHDaru/maestro/commit/71b79c1);
  [spec 049](https://github.com/GHDaru/maestro/blob/19823c2/specs/049-indice-de-adrs-com-portao/spec.md)),
  e a spec escreveu a próxima escalada: se o índice divergir de novo, passa a ser gerado do disco.
- **`check-version.sh`** (ciclo 050): a versão era declarada em quatro lugares (CHANGELOG, README,
  roadmap e plugin empacotado) sem nada que os mantivesse em acordo [CLAIM-14-026]; o portão
  falha na divergência e no silêncio de um deles
  ([spec 050](https://github.com/GHDaru/maestro/blob/19823c2/specs/050-fechar-v0-2-0/spec.md)).
- **`check-cycle.sh` e `check-links.sh`** (retro do 034): o primeiro cobra a justificativa da raia
  de cada ciclo e exige que todo commit cite o ciclo, que era só convenção; o segundo valida todo
  link relativo, porque o renome em massa do ciclo 033 quebrou caminhos.
- **`check-chapters.sh`** (retro do 034): a segunda lei da verificação nasceu no ciclo 017 e ficou
  dez ciclos só na skill, fora do capítulo que ensina a Definition of Done (DoD), a definição de
  pronto [CLAIM-14-027]. O portão compara a data da regra mais nova das skills com a revisão do
  capítulo que a cita.
- **O Constitution Check contra a constituição** (ciclo 021): a constituição tinha oito princípios
  desde o ADR 0010 e o template de plano checava sete, e os planos 013 a 019 não tinham onde
  marcar o Princípio VIII [CLAIM-14-028]; quatro linhas do modelo operacional citavam "(P. VII)"
  com a numeração do FlowBuilder, de onde o texto migrara [CLAIM-14-029]. A correção não foi
  editar o template: foi uma verificação que compara norma e executável e falha quando divergem.

O **gate de CHANGELOG** é o exemplo de livro de T5: toda pull request adiciona entrada em
`[Unreleased]` ou aplica o rótulo `skip-changelog`, uma válvula de escape declarada
([`.github/workflows/ci.yml`](https://github.com/GHDaru/maestro/blob/19823c2/.github/workflows/ci.yml));
com escape nomeado, o desvio fica registrado em vez de contornado por fora. Mas o gate cobra a
entrada, não a forma nem o corte: o arquivo acumulou onze subseções repetidas em 44 ciclos,
consolidadas só no ciclo 048 [CLAIM-14-030], e o bloco `[Unreleased]` ocupa hoje cerca de mil
linhas, desde a v0.3.0 de 22 de agosto [CLAIM-14-031]. O corte de versão segue humano, e a nota
da v0.3.0 aprendeu a dizer o estado **verificado** da tag, depois de a tag da v0.1.0 nunca ter
chegado ao GitHub [CLAIM-14-032]
([spec 062](https://github.com/GHDaru/maestro/blob/19823c2/specs/062-fechar-v0-3-0/spec.md)).

### O método se cobra no fim de cada turno

A peça mais recente responde ao corolário C13 (uma pergunta respondível de memória será
respondida de memória, e memória relata intenção). Até o ciclo 065, "estou seguindo o método?"
era respondido por texto no arquivo de instrução e por uma medição no início da sessão. O ADR
0021 instalou um hook de parada que roda o portão de conformidade no fim de cada resposta do
agente: vermelho, ele não deixa o agente parar, **uma vez**; na segunda, deixa e avisa o humano,
porque um portão que vira laço queima tokens sem decidir nada [CLAIM-14-033]
([ADR 0021](https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0021-o-metodo-se-cobra-e-bate-o-ponto.md)).
É T6 levado ao limite: a regra não espera a retro para ser cobrada.

### A governança se aplica a si mesma

As camadas da Teoria têm versão, e o histórico mostra o desenho funcionando. Na captura do
handbook, em agosto, a constituição fora tocada três vezes em 32 ciclos, enquanto a periferia
executável crescera para seis skills, dez scripts e dez ADRs, três deles para **descartar** algo
[CLAIM-14-034]. A constituição está na versão 1.3.0, emendada por ADR e versionamento semântico
(MAJOR remove ou redefine um princípio, MINOR acrescenta, PATCH esclarece); o modelo operacional
foi de 1.0.0 a 1.4.0 e tem a retro como fonte primária de emendas [CLAIM-14-035]. O Princípio VII
junta as peças: núcleo firme, periferia evolutiva, memória só-anexar e retro que vira regra
versionada. Acima delas, o ADR 0015 (ciclo 035) criou a camada de derivação, com axiomas,
teoremas provados com evidência do repositório (inclusive a desfavorável) e corolários; nasceu com
cinco, seis e dez e está com cinco, sete e treze [CLAIM-14-036]. A regra dela é a pergunta que
este capítulo deixa ao tech lead: **toda regra nova é argumentada contra um axioma**; a que não
deriva de nenhum é axioma novo (por ADR) ou é cerimônia, e se poda. O diagrama do processo em
Business Process Model and Notation (BPMN), refeito no mesmo ciclo, termina a trilha de artefatos
em axioma, teorema e regra nova
([`05-bpmn-processo.md`](https://github.com/GHDaru/maestro/blob/19823c2/docs/diagramas/05-bpmn-processo.md)).

A poda também está escrita. O modelo operacional lista seis itens que **não** adota, com motivo:
Scrum completo, backlog formal, segundo toolkit de spec, RFC pesado, diagramas formais com
métricas e estimativa de prazo [CLAIM-14-037]; do OpenSpec, descartado, absorveu-se o modelo de
*delta* como raia leve. E a poda é reversível: o painel de coordenação era "depois/YAGNI" e virou
essencial no ciclo 066 (ADR 0022), quando a escala o justificou, com eventos só-anexar e o banco
SQLite como projeção reconstruível dos arquivos, nunca como fonte [CLAIM-14-038]. O catálogo de
artefatos aplica o mesmo corte: spec, plano, tarefas (efêmeras), código com testes, ADR, jornada
de tela, changelog, índice de decisões e definições de pronto são essenciais, cada um com
consumidor e cobrança; PRD e design avulsos são YAGNI por duplicarem função. O catálogo vigente
([`artifacts.md`](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/artifacts.md))
separa a memória fora do ciclo (ADR imutável, índice só-anexar, CHANGELOG cobrado pela CI, roadmap
no mesmo pull request), e o template do índice de ADRs é justamente a lista à mão que o
`check-adr.sh` confronta com o disco. Na captura do ciclo 028, 26 de 28 ciclos tinham os quatro
artefatos completos, e os dois restantes estavam abertos [CLAIM-14-048].

**O preço de cada decisão está escrito.** O handbook fixa o formato (quando, por quê, o que faz,
o que provoca, incluindo o efeito indesejado aceito), porque decisão sem preço escrito não é
revogável; seu quadro de 14 decisões de engenharia, com data e registro, é o mapa didático dos
ADRs [CLAIM-14-049]. A jornada do método resume a construção em três lições: cada regra nasceu de
uma dor, o método se aplicou a si mesmo, e o preço está escrito [CLAIM-14-051].

O livro do método segue as mesmas regras. O handbook se declara ao lado do documento normativo,
do diário e da pesquisa, e explica o porquê sem substituir a regra; o caderno técnico descreve a
cobrança pelo portão na CI, pelo modelo de pull request que espelha a DoD e pelo comando `/dod`.
O ciclo 013 (ADR 0011) trocou a anatomia antiga por um esqueleto com exemplo de ciclo real
obrigatório, trilhas de navegação e um tutor com busca no livro [CLAIM-14-052], e entregou um
instalador que não sobrescreve sem `--forcar`. A migração seguiu um capítulo por ciclo ("reescrever
a forma, preservar o fato"), cada passo deixando um portão (página fora do corpus do tutor; o BPMN
como índice navegável, com build que falha por imagem sem arquivo), e fechou em 13/13 no ciclo 032
declarando quatro achados abertos, porque um capítulo de governança que esconde a própria dívida
seria publicidade [CLAIM-14-039]. O roadmap conta a mesma história em fases (fase = ciclo = spec =
gate) de F0 a F35, com o tutor ainda "falta publicar o serviço" [CLAIM-14-050]; o guia editorial
data cada capítulo vivo pelo fato, pela captura e pelo ciclo, sem sobrescrever a captura antiga,
regra que este livro herdou. Até o lar do método é decisão registrada: o ADR 0007 deu à
metodologia um repositório único, os de origem ficaram somente leitura, e a constituição tem uma
nota de linhagem para os textos migrados que citam a numeração de lá. Dois lares seriam duas
fontes de verdade.

### Como montar isso no seu time, sem o Maestro

Nada acima depende do Maestro. O mínimo que reproduz as engrenagens em qualquer repositório e
qualquer CI é este:

1. **Um arquivo de achados só-anexar** na raiz, uma linha JSON por achado:
   `{"id": "achado-012-teste-sem-falha", "ciclo": 12, "status": "aberta", "titulo": "..."}`.
   Fechar é anexar outra linha com `"fecha": "achado-012-teste-sem-falha"`; nunca editar a antiga.
2. **Um script de gatilho**, em qualquer linguagem, que conta como aberto todo achado sem linha
   que o feche pelo campo e sai com código diferente de zero acima de N abertos ou com um aberto
   há mais de M ciclos. Comece com os números do Maestro e ajuste pelo ruído.
3. **Dois passos na CI**: um roda o script (consultivo no começo, bloqueante quando o time
   confiar no limiar); o outro recusa o diff que altera ou remove linha existente do arquivo.
   `git diff -U0 origin/main -- achados.jsonl | grep '^-[^-]'` sem saída é a regra inteira.
4. **Uma recusa antes do dano**: proteção de branch ou hook de pré-commit para os registros
   imutáveis (ADRs, o arquivo de achados), porque o portão da CI só audita depois.
5. **Uma pauta fixa e uma lista de recusas**: as três perguntas da retro, e uma seção "o que não
   adotamos" no arquivo de instrução que o agente lê no início da sessão.

O `aprende.py` do exemplo abaixo é o item 2 com os dados reais; troque a pasta `dados/` pelos
seus. E, depois de cada erro, use a pergunta do material de apresentação do Maestro: não "quem
esqueceu?", mas "que função de força faltava?".

## Exemplo executável

A pasta [`exemplo/`](exemplo/README.md) traz um script Python 3 sem dependência externa,
`aprende.py`, com as três engrenagens do capítulo reduzidas ao essencial: o gatilho da retro por
dívida, o índice só-anexar e a auditoria de artefatos por consumo ou imutabilidade.

Os dados das duas primeiras partes **não são inventados**: `dados/indice.jsonl` traz, sem edição,
as linhas de achados abertas quando o ciclo 034 começou, e `dados/fechamento-estrutural.jsonl` as
linhas `retro-034-fecha-*` que a retro anexou. A terceira parte, `dados/artefatos.json`, é
ilustrativa, e o README diz isso.

Rode:

```bash
cd livro/14-a-organizacao-que-aprende/exemplo
python3 aprende.py demo
```

O que observar na saída [CLAIM-14-040]:

1. **O gatilho reproduz o número real.** Com os cinco achados e o ciclo corrente 034, o script
   imprime "5 achados abertos (limite 4); o mais velho tem 11 ciclos (limite 6)", o mesmo que o
   relatório do ciclo 034 registrou antes da retro.
2. **O fechamento em prosa não fecha.** Uma linha que diz "fechados os achados 023, 027, 029,
   031 e 033", com id novo e sem o campo `fecha`, deixa os cinco abertos, a falha que o ciclo 034
   cometeu. Com as linhas reais, que têm `fecha`, o gatilho fica verde.
3. **Corrigir editando é recusado.** Trocar `aberta` por `fechada` na linha antiga é recusado
   ("linha 1 reescrita"): a versão nova tem de começar pela antiga, linha a linha.
4. **A auditoria separa quatro destinos**, as quatro classes da saída: consumido e cobrado vive;
   o ADR imutável vive; o que tem leitor sem cobrança (o índice à mão, o roadmap) aparece
   apodrecendo; o que ninguém consome aparece para poda.

O roteiro sai com código 0 quando os três vermelhos esperados aparecem: o vermelho prova que o
portão discrimina. O exercício do README dá ao roadmap uma "cobrança" que não existe e o resumo
melhora: é o anti-padrão 13 dentro da auditoria, o campo mede a frase, não o fato.

## Contraexemplo

As regras deste capítulo têm custo, e há situações em que atrapalham.

**Gatilho que vira ruído.** Um limiar de dívida baixo demais produz retro sem matéria, e retro
sem matéria vira teatro (anti-padrão 11), o mesmo defeito do calendário. O limiar alto demais
deixa a dívida envelhecer. O Maestro escolheu quatro abertos ou seis ciclos [CLAIM-14-011], e o
portão aceita os dois números por variável de ambiente; não há medição de que esses números sejam os certos. E o
gatilho consultivo pode ficar vermelho e ser ignorado, como do 053 ao 055 [CLAIM-14-013]. Se o
seu time ignora um vermelho consultivo ciclo após ciclo, ou o limiar está errado, ou a retro precisa
bloquear algo, ou o portão é decoração e deve sair.

**Achado que não tem dono no mundo.** O caso do 055 mostra o limite do "registre tudo":
registrar o que não tem ação possível infla a dívida e degrada o gatilho. No seu time: se o achado
não tem ação nem gatilho escrito, ele não é achado, é desabafo.

**Imutabilidade que esconde.** Só-anexar custa acúmulo, que exige índice e curadoria, e custa
leitura: o estado de um achado exige ler todas as linhas. O protocolo de fechamento falhou duas
vezes por isso: no ciclo 039, uma linha com `fecha` apontando para o próprio id
fechava um achado nunca aberto, e o erro se repetiu no ciclo 041; a causa raiz era que o
protocolo não oferecia forma para "achado encontrado e corrigido no mesmo ciclo", e a forma foi
criada [CLAIM-14-041]. Regra de memória sem forma para o caso comum produz improviso, e o
improviso se repete.

**Portão que cobra a frase da evidência.** A caixa marcada antes da evidência é a forma mais
persistente de "correção que não vira regra" no Maestro. Ela apareceu de novo no ciclo 044, num
critério de aceite da spec que dava como fechado um achado aberto; era a quarta ocorrência
[CLAIM-14-042]. Nos ciclos 057 a 060, a revisão independente achou a mesma dupla de
defeitos quatro vezes seguidas [CLAIM-14-043]. A regra existia; o que faltava era o portão que a
cobrasse sem ficar vermelho durante toda a vida de um ciclo em andamento. A lição: às vezes a
regra certa é impossível de cobrar inteira, e a saída é cobrar a metade que é sempre verificável
("se marcou, a evidência existe"), como fez o ciclo 061. O [capítulo 10](../10-quality-gates-que-provam-fatos/capitulo.md)
conta o que aconteceu em seguida.

**Artefato vivo que congela mesmo assim.** O roadmap do Maestro recebeu, depois do 017, a regra
de ser atualizado no mesmo pull request de cada ciclo. Mas o candidato a portão que o relatório
do 017 escreveu (comparar o maior ciclo em `specs/` com o maior citado no roadmap) não foi
implementado. Em `19823c2`, a última edição do roadmap é de 24 de outubro, ele termina na fase
F35, e as fases dos ciclos 066 a 069 ainda dizem "aguarda o gate humano", embora o índice
registre esse gate concedido em 20 de outubro [CLAIM-14-044]. É o anti-padrão 15 sobrevivendo à
própria regra: o método quebrou a regra que escreveu, e quem pegou foi a contagem, não a
atenção.

**Quando não aplicar.** Para um protótipo descartável, uma prova de conceito de uma semana ou um
time em que a mesma pessoa conduz uma única sessão longa, o aparato de índice, gatilho e guarda
custa mais do que devolve. T6 só morde quando há sessões sucessivas e correções que se repetem.
A regra prática: comece a registrar achados na segunda vez que corrigir a mesma coisa, e instale
o gatilho na primeira vez que um achado registrado envelhecer sem retro.

## Evidência

O que sustenta o capítulo, separado pelo estado de cada afirmação. A evidência reproduzível de
cada claim está em [`claims.md`](claims.md).

**Medido** (reproduzível por comando em `19823c2`): os limiares do gatilho, o tamanho e as levas
do catálogo de anti-padrões, a composição do índice de decisões e do estado do ecossistema, os
commits por ADR, o bloco `[Unreleased]`, a camada de derivação, os itens não adotados, os portões
da retro do 034, o roadmap defasado e a saída do exemplo executável [CLAIM-14-011, CLAIM-14-015,
CLAIM-14-019, CLAIM-14-022, CLAIM-14-025, CLAIM-14-031, CLAIM-14-036, CLAIM-14-037, CLAIM-14-040,
CLAIM-14-044, CLAIM-14-050, CLAIM-14-053, CLAIM-14-054].

**Observado** (em relatório de qualidade, spec, ADR, cabeçalho de script ou índice de decisões do
Maestro): a história da retro sem gatilho e do gatilho [CLAIM-14-001 a CLAIM-14-007,
CLAIM-14-012, CLAIM-14-013, CLAIM-14-046]; os artefatos que congelaram e os portões que os
substituíram [CLAIM-14-008 a CLAIM-14-010, CLAIM-14-026 a CLAIM-14-030, CLAIM-14-032,
CLAIM-14-047]; o laço do ciclo 008 e suas origens [CLAIM-14-014, CLAIM-14-051, CLAIM-14-055]; o
registro só-anexar e a guarda [CLAIM-14-016 a CLAIM-14-018, CLAIM-14-021, CLAIM-14-023,
CLAIM-14-024]; o hook de parada, as camadas e a poda [CLAIM-14-033, CLAIM-14-035, CLAIM-14-038,
CLAIM-14-039, CLAIM-14-048, CLAIM-14-052]; as falhas do protocolo de fechamento e da caixa marcada
[CLAIM-14-041 a CLAIM-14-043]. Três números são capturas do handbook de agosto de 2026, citadas
como tal [CLAIM-14-020, CLAIM-14-034, CLAIM-14-049].

**Hipótese** (não medida). A H10 da base de pesquisa deste livro diz que retrospectiva → regra
reduz recorrência [CLAIM-14-045]. Os casos do Maestro são compatíveis com ela e mostram onde ela
falha: a recorrência caiu onde a regra virou portão (o campo `fecha`, o índice de ADRs, a versão)
e não caiu onde a regra ficou como nome no catálogo (o anti-padrão 21) ou como texto (a caixa
marcada antes da evidência). A hipótese refinada, também não medida, é mais estreita: **retro →
regra cobrada por executável** reduz recorrência; **retro → regra escrita** reduz pouco. Os dados
são de um repositório, com um operador humano e sem grupo de controle; o desenho que testaria
isso (contar recorrências por forma de achado, antes e depois de cada tipo de destino) está no
[capítulo 15](../15-validando-o-maestro/capitulo.md).

## Checklist

Aplique ao seu time. Cada item é verificável por um comando, um arquivo ou uma contagem.

- [ ] Existe um registro de achados **só-anexar** (um arquivo JSONL, uma planilha de linhas que
      não se editam, um rótulo de *issue*) e cada correção recorrente a um agente entra nele com
      data e ciclo.
- [ ] A retrospectiva tem **gatilho mensurável** (número de achados abertos, idade do mais
      velho, ou ambos) e há um script que fica vermelho quando o gatilho dispara sem a retro.
- [ ] O fechamento de um achado é **estrutural** (um campo que aponta o id), e você já viu o
      gatilho continuar vermelho com um fechamento escrito só em prosa.
- [ ] Toda resposta "sim" da retro tem **destino escolhido** (princípio, modelo operacional,
      skill, script ou ADR) **e** artefato criado no mesmo ciclo.
- [ ] A retro responde também "que regra **não pagou** o custo?", e a última retro podou pelo
      menos uma coisa ou registrou por que não.
- [ ] Existe uma lista escrita do que o time **não adota**, com motivo, e cada item adiado tem
      condição escrita de revisão.
- [ ] Para cada artefato do repositório, você sabe responder **quem consome** e **o que quebra
      quando fica velho**; o que não tem resposta está marcado para poda.
- [ ] Todo índice escrito à mão sobre arquivos (de ADRs, de agentes, de versões) tem um portão
      que o compara com o disco.
- [ ] ADRs nunca são editados no mérito: `git log --follow` de cada um mostra só criação,
      renome de caminho ou troca de status, e uma decisão revertida tem ADR novo que a supera.
- [ ] Existe uma guarda (hook ou proteção de branch) que recusa reescrever o histórico, e os
      limites dela estão declarados.
- [ ] Toda regra nova é argumentada contra um princípio do método e citada na instrução que o
      agente lê no início da sessão; a que não deriva de nenhum vira princípio novo ou é podada.

## Referências

- Maestro, versão citada `19823c2`:
  [`docs/governance/axioms.md`](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/axioms.md) (A3, A4, T5, T6, C1, C9) ·
  [`docs/governance/principles.md`](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/principles.md) (Princípios VI e VII) ·
  [`docs/governance/operating-model.md`](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/operating-model.md) (§5, §6, §10, §11) ·
  [`docs/governance/artifacts.md`](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/artifacts.md) ·
  [`skills/anti-patterns/SKILL.md`](https://github.com/GHDaru/maestro/blob/19823c2/skills/anti-patterns/SKILL.md) ·
  [`scripts/check-retro.sh`](https://github.com/GHDaru/maestro/blob/19823c2/scripts/check-retro.sh) ·
  [`scripts/retro.sh`](https://github.com/GHDaru/maestro/blob/19823c2/scripts/retro.sh) ·
  [`scripts/record-decision.sh`](https://github.com/GHDaru/maestro/blob/19823c2/scripts/record-decision.sh) ·
  [`scripts/check-adr.sh`](https://github.com/GHDaru/maestro/blob/19823c2/scripts/check-adr.sh) ·
  [`scripts/check-version.sh`](https://github.com/GHDaru/maestro/blob/19823c2/scripts/check-version.sh) ·
  [`scripts/hooks/guard-immutables.py`](https://github.com/GHDaru/maestro/blob/19823c2/scripts/hooks/guard-immutables.py) ·
  [`docs/records/decisoes.jsonl`](https://github.com/GHDaru/maestro/blob/19823c2/docs/records/decisoes.jsonl) ·
  [`docs/ecosystem/estado.jsonl`](https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/estado.jsonl) ·
  [`docs/adr/README.md`](https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/README.md) ·
  [`docs/roadmap.md`](https://github.com/GHDaru/maestro/blob/19823c2/docs/roadmap.md) ·
  [`docs/jornada/README.md`](https://github.com/GHDaru/maestro/blob/19823c2/docs/jornada/README.md) ·
  [`docs/receitas/rodar-a-retro.md`](https://github.com/GHDaru/maestro/blob/19823c2/docs/receitas/rodar-a-retro.md) ·
  ADRs [0007](https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0007-separacao-repo-maestro.md),
  [0009](https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0009-registro-automatico-gate-merge.md),
  [0011](https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0011-livro-padrao-editorial-e-companion.md),
  [0015](https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0015-axiomas-teoremas-corolarios.md),
  [0017](https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0017-divisao-em-dois-repositorios.md),
  [0018](https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0018-fronteira-interna-em-vez-de-divisao.md),
  [0021](https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0021-o-metodo-se-cobra-e-bate-o-ponto.md),
  [0022](https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0022-painel-de-coordenacao-como-projecao-dos-arquivos.md) ·
  specs e relatórios dos ciclos 008, 017, 020, 021, 027, 028, 029, 032, 034, 035, 039, 041, 044,
  045, 047, 049, 050, 055, 061, 062 e 063 em `specs/`.
- Handbook do Maestro (cópia em `maestro-handbook/` na raiz deste livro, capturada de
  `19823c2`): capítulos 07 (cerimônias, §5.2 e §6), 08 (entregáveis e artefatos), 12 (governança
  leve) e 13 (decisões de engenharia, §3, §5.8, §5.10); receita `rodar-a-retro.md`.
- NYGARD, Michael. *Documenting Architecture Decisions*. Cognitect, 15 nov. 2011.
  https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions (acesso em
  02/11/2026).
- *Markdown Architectural Decision Records* (MADR). https://adr.github.io/madr/ (acesso em
  02/11/2026).
- ARGYRIS, Chris; SCHÖN, Donald. *Organizational Learning: A Theory of Action Perspective*.
  Reading: Addison-Wesley, 1978.
- DERBY, Esther; LARSEN, Diana. *Agile Retrospectives: Making Good Teams Great*. Pragmatic
  Bookshelf, 2006.
- BEYER, Betsy et al. (org.). *Site Reliability Engineering: How Google Runs Production
  Systems*. O'Reilly, 2016. Capítulo 15, "Postmortem Culture: Learning from Failure".
  https://sre.google/sre-book/postmortem-culture/ (acesso em 02/11/2026).
- GitHub Spec Kit (comando de constituição). https://github.com/github/spec-kit (acesso em
  02/11/2026).
- Base de pesquisa deste livro, `pesquisa/base-de-pesquisa.md`, agenda H1–H10 (H10).
