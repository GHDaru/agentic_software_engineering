# Apêndice A — O Maestro em uma página

> *Um humano rege. Muitos agentes executam.*

Os capítulos deste livro discutem ideias que valem com qualquer ferramenta. Eles usam o
Maestro como objeto de estudo: um método de engenharia de software em que uma pessoa conduz
vários agentes de Inteligência Artificial (IA), construído e documentado no próprio
repositório. Este apêndice é o mapa desse objeto. Dá a definição em uma frase, o sistema em
uma tabela, o ciclo em uma linha do tempo e o processo em um desenho de raias. Também diz de
que axiomas o método se deriva, em que ele difere das alternativas que um tech lead
consideraria, por que todo resumo como este envelhece, como conferir se ele ainda vale e
quando ele atrapalha mais do que ajuda. Leia antes do
capítulo 1 se quiser o vocabulário; volte a ele quando um capítulo citar uma peça do método
e você quiser saber onde ela se encaixa.

Tudo o que segue é citado na versão `19823c2` do Maestro (01/11/2026). Onde um número
aparece, há um identificador de claim (prefixo 91) em [claims.md](claims.md) com o comando que o reproduz.

Uma ressalva honesta antes de começar: o título promete uma página, e o apêndice tem bem
mais que isso. Mais adiante ele cobra do Maestro o resumo que envelhece e que ninguém
consome; seria incoerente esconder que ele próprio não cabe numa página. Por isso a página
de verdade é o quadro abaixo. Tudo o que vem depois dele é **aprofundamento**, para ler
quando um capítulo citar uma peça do método ou quando você estiver decidindo adotá-lo.

## Se você só tem uma página

**Definição.** O Maestro é um método em que **um humano rege vários agentes de IA**: a
especificação diz o que fazer, os agentes executam, o humano decide, aprova e verifica.

**Três ideias** [CLAIM-91-001]:

1. **A spec é a fonte de verdade** — não o código, que o agente refaz, nem o prompt, que
   some com a conversa.
2. **O humano responde pela política, não por cada item** — ele define o que o agente faz
   sozinho e o que pede aprovação.
3. **Reversibilidade compra velocidade** — o que torna seguro delegar é poder desfazer
   barato, não aprovar tudo.

**O que fazer na segunda-feira:**

1. **Instale num repositório de teste.** A receita do Maestro estima cerca de 5 minutos com
   `maestro init <projeto> --ai claude`, que termina rodando a própria verificação
   (`check-install.sh`) e falha se ela não passar [CLAIM-91-029].
2. **Rode um ciclo da raia leve.** Escolha um bug pequeno: escreva o teste que o reproduz
   falhando, corrija, abra o pull request como único artefato e peça a revisão a um agente
   que não escreveu o código. A raia leve dispensa spec, plano e tarefas, mas não dispensa
   teste nem revisão independente [CLAIM-91-025].
3. **Marque o tempo.** O Maestro não publica quanto custa um ciclo; o número que vale para a
   sua decisão é o do seu primeiro ciclo leve e, depois, o do primeiro ciclo pleno.

Se depois disso você quiser saber o que adotar e o que deixar de fora, vá direto a «Em que o
Maestro difere das alternativas» e ao critério de adoção que fecha aquela seção.

---

*Daqui em diante, aprofundamento.*

## A página

**O que é.** Um método para construir software em que **um humano rege N agentes de IA**.
Não é "a IA escreve código"; é orquestração governada: a especificação é a fonte de verdade,
os agentes executam, e o humano decide, aprova e verifica.

**O nome.** Numa orquestra, o maestro não toca os instrumentos. A **partitura** (a *spec*,
especificação) diz o que tocar; o **compasso** (os *gates*, portões de controle) marca o
ritmo; os **músicos** (os agentes) executam
([01-definicao.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/diagramas/01-definicao.md)).
A metáfora tem uma consequência que vale mais que a imagem: o regente é avaliado pelo que a
orquestra tocou, não pelas notas que ele mesmo tocou. Quando a máquina digita, o trabalho
humano que resta é deixar a intenção clara antes e verificar o resultado depois.

**Três ideias costuram o resto** [CLAIM-91-001]. Se guardar só isto, já tem o essencial:

1. **A spec é a fonte de verdade.** Não o código, que o agente refaz, nem o prompt, que
   evapora com a conversa. A intenção vive na especificação, e por isso ela vem antes do
   código e o alimenta ([capítulo 4](../../04-a-spec-como-partitura/capitulo.md)).
2. **O humano responde pela política, não por cada item.** Ele define os trilhos — o que um
   agente faz sozinho e o que precisa de aprovação — e deixa os agentes correrem dentro
   deles. É o que permite escalar sem que a pessoa vire gargalo
   ([capítulo 2](../../02-o-problema-da-confianca/capitulo.md)).
3. **Reversibilidade compra velocidade.** O que torna seguro delegar não é aprovar tudo; é
   tornar as ações reversíveis (backup, simulação sem efeito, *rollback*). Errar barato é o
   que deixa correr rápido
   ([capítulo 11](../../11-risco-reversibilidade-e-autonomia/capitulo.md)).

O caderno de desenvolvimento do Maestro reformula as três para quem programa, e a
reformulação é útil porque cada uma vira uma pergunta de revisão: *a intenção está na spec?*
— *a norma que importa virou um script que a confere?* — *errar aqui é barato?* A segunda é
a mais operacional das três: no Maestro, "norma que ninguém confere não existe", e uma
regra que importa vira um `check-*.sh`
([apresentacao-desenvolvimento-maestro.html](https://github.com/GHDaru/maestro/blob/19823c2/docs/handbook/apresentacao-desenvolvimento-maestro.html),
último slide).

**O sistema, em 12 elementos e 5 camadas** [CLAIM-91-001]:

| Camada | Pergunta que responde | Elementos |
|---|---|---|
| Fundamento | Por quê? | Princípio central · evidência de desempenho de entrega |
| Mecânica | Como o trabalho flui? | Desenvolvimento dirigido por spec · fluxo agêntico e contexto · orquestração |
| Estrutura | Quem faz e quando? | Papéis · cadência |
| Qualidade | O que se produz e como se prova? | Artefatos · prontidão e pronto · gates de risco · rastreabilidade |
| Governança | Como tudo evolui? | Constituição · registros de decisão · poda do desnecessário |

Lida de cima para baixo, a tabela é uma cadeia de dependência. O **fundamento** diz por que
o resto existe: a Inteligência Artificial explora, propõe e escreve; o humano especifica,
decide e aprova; testes, gates e revisão independente validam. Os números de DevOps
Research and Assessment (DORA) entram como bússola: velocidade e estabilidade não se trocam
uma pela outra quando o lote é pequeno e a mudança é reversível. A **mecânica** diz como uma
intenção vira código sem que o agente adivinhe: a spec gera, o contexto é economizado, o
trabalho é cortado por fronteira para que agentes em paralelo não colidam. A **estrutura**
diz quem responde: na matriz Responsible, Accountable, Consulted, Informed (RACI), quem
executa e quem é consultado podem ser agentes, mas o Accountable é sempre humano, e responde
pelos critérios, não por cada linha. A **qualidade** diz o que conta como pronto: um
artefato só vive se alguém o consome; a Definition of Done (DoD, a definição de pronto) é o
que uma máquina confere; o gate cresce com o risco; e o fio spec ↔ pull request ↔ teste é a
memória que sobrevive quando o agente perde o contexto. A **governança** diz como o método
muda sem inchar: uma constituição que só se emenda, registros de decisão que nunca se
reescrevem e a regra You Aren't Gonna Need It (YAGNI) podando o que não se paga.

Dois detalhes evitam confusão para quem for ao repositório. Primeiro: são 12 elementos, mas
a tabela tem 14 rótulos, porque a camada de governança é **um** elemento (o `[12]`,
governança leve) apresentado por três faces [CLAIM-91-002]. Segundo: o handbook do método
tem 13 capítulos, um por elemento mais um de decisões de engenharia sem elemento próprio, e o
**número do capítulo não é o rótulo do elemento**. O capítulo 02 do handbook trata do elemento
`[10]` (DORA), o 03 do `[2]` (spec), e assim por diante; a ordem dos capítulos é a ordem de
dependência de leitura, e o rótulo era a linguagem que o autor usava durante a construção
[CLAIM-91-003]. O handbook avisa disso numa nota abaixo do índice, porque quem lê os dois
números lado a lado tende a tomá-los pelo mesmo
([handbook/README.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/handbook/README.md)).

## De onde vêm as três ideias

As três ideias não são preferências de estilo. O Maestro as deriva de uma camada abaixo da
constituição, o arquivo de axiomas: cinco verdades assumidas, sete teoremas derivados delas,
cada um com evidência no próprio repositório, e treze corolários, que é de onde sai a
maioria das regras do dia a dia [CLAIM-91-026]
([axioms.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/axioms.md)).
Os cinco axiomas cabem numa linha cada:

| Axioma | O que assume |
|---|---|
| A1 | A intenção é humana: o agente propõe, escreve e verifica, mas não *quer*. |
| A2 | Consequência precisa de dono: quem não tem nada a perder não responde pelo resultado. |
| A3 | O contexto é finito e piora à medida que enche. |
| A4 | O que está escrito é o que sobrevive: o agente começa cada sessão do zero. |
| A5 | O custo é assimétrico: fazer é barato, desfazer não. |

A derivação das três ideias é curta [CLAIM-91-026]:

- **A spec é a fonte de verdade** é o teorema T1 (de A1 e A4): se a intenção é humana e só o
  escrito sobrevive, a intenção tem de estar num artefato **antes** de virar código.
- **O humano responde pela política** sai de A2 e do teorema T3 (de A2 e A5): o gate cresce
  com a irreversibilidade, nunca por igual; pesado em tudo, o humano vira carimbo. A regra
  irmã, **quem executa não verifica**, é o T2 (de A2 e A3): quem escreveu carrega no contexto
  os becos que explorou.
- **Reversibilidade compra velocidade** é o corolário C4 (de T3): tornar a ação reversível
  baixa a classe de risco e sai mais barato que mais uma aprovação.

A frase do caderno de desenvolvimento, "norma que ninguém confere não existe", é o
corolário C7 (de T4 e T6), e o gatilho da retrospectiva é o C1 (de T6). É também por isso
que a raia de portões do desenho de processo diz que a regra nova "é argumentada contra os
axiomas": uma regra que não deriva de nenhum é um axioma novo, que entra por um Architecture
Decision Record (ADR, o registro de decisão), ou
cerimônia, que a poda remove.

Um detalhe mostra o tema deste apêndice dentro da própria constituição. O parágrafo dela
que resume os axiomas fala em "seis teoremas" e "dez corolários"; o arquivo de axiomas, na
mesma versão, tem sete e treze [CLAIM-91-026]. A constituição registra sua última emenda em
03/08/2026; o arquivo de axiomas está na versão 1.2.0, de 07/08/2026. O resumo parou na
emenda, e o arquivo resumido andou.

## O ciclo, com quem executa cada passo

Toda mudança nasce de uma intenção e termina num gate humano. Entre os dois, cada passo
produz um artefato que o passo seguinte consome
([03-fluxo.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/diagramas/03-fluxo.md)):

| Passo | O quê | Quem | Produz |
|---|---|---|---|
| — | Intenção | Steward (o humano que decide o quê e o porquê) | o problema, o valor, o apetite |
| 1 | Especificar | agente de spec | `spec.md`, com critérios testáveis |
| ◆ | Spec pronta: Definition of Ready (DoR) | humano aprova | — |
| 2 | Planejar | agente arquiteto | `plan.md`, com a conferência da constituição e, se houver decisão, um Architecture Decision Record (ADR) |
| 3 | Fatiar | (do plano) | `tasks.md`, cortado por fronteira |
| 4 | Implementar | agente implementador | código e testes, em diffs pequenos |
| 5 | Verificar | revisor em contexto fresco, segurança, qualidade | veredito com evidência |
| ◆ | Pronto (DoD) | checks mecânicos | verde local, que não é certo global |
| ◆ | Gate de merge | humano decide | — |
| ● | Entregue | redator técnico | documentação viva no mesmo pull request |

Três losangos param o fluxo [CLAIM-91-022]. Dois são humanos e não se delegam (a spec pronta e o merge); um
é mecânico (a DoD, que bloqueia sozinha). O plano também passa por aprovação humana na raia
completa, como mostra o desenho de processo da próxima seção. A linha do tempo não mostra o
que o caderno de desenvolvimento chama de «passo zero», «o mais barato e o mais
esquecido» (o capítulo 4 trata do mesmo passo como a classificação em raias, sem esse
nome): antes de especificar, decide-se **quanto processo** a mudança
merece [CLAIM-91-025]. Na raia leve (um bug, um erro de digitação), o pull request é o
artefato e as caixas de planejamento são puladas, mas não a revisão independente nem os
testes; na plena, o ciclo é o da tabela; na de infraestrutura, é o da tabela mais os
portões de reversibilidade. O critério é ambiguidade × raio de impacto × irreversibilidade,
e na dúvida entre leve e plena, é plena.

Duas regras do ciclo são as que mais se esquecem, e as duas derivam do Princípio II da constituição do Maestro:
**quem executa não verifica** (a revisão final é de um agente que não viu a conversa, só o
diff, a spec e o plano), e **o humano responde pela política, pelos gates e pelos critérios**,
não por cada linha. O capítulo 3 discute o que isso faz com o gargalo
([capítulo 3](../../03-um-humano-muitos-agentes/capitulo.md)); o capítulo 7, como cada papel
vira um agente estreito ([capítulo 7](../../07-papeis-e-skills/capitulo.md)).

## O processo em sete raias

A linha do tempo diz a ordem. O desenho de processo diz **quem** executa cada passo e
**onde o fluxo para**. O Maestro o desenha em Business Process Model and Notation (BPMN), a
notação de processos padronizada pelo Object Management Group (OMG) na versão 2.0.2. Da
notação, o desenho usa só o essencial: raias horizontais por executor (as *swimlanes*),
caixas para tarefas, losangos para decisões e artefatos ligados ao fluxo
([05-bpmn-processo.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/diagramas/05-bpmn-processo.md)).
São sete raias [CLAIM-91-004]:

| Raia | O que acontece nela |
|---|---|
| Steward (humano) | a intenção, os gates indelegáveis e a retrospectiva |
| Agentes de IA | especificar → clarificar → planejar → fatiar → implementar → verificar → documentar |
| Ramo de interface | só quando há tela: papel semântico antes do componente → desenho de interface → gate de interface → captura do *build* real → avaliação heurística datada |
| Automação | esqueleto do ciclo, conferência da constituição, testes e *fitness functions*, promoção com registro, publicação |
| Distribuição | o método sai do repositório em três camadas, depois de conferido que o pacote está sincronizado com as fontes |
| Portões | a DoD executável: scripts que falham sozinhos |
| Artefatos | a trilha auditável, de `spec.md` até a regra nova |

O desenho tem duas propriedades que um diagrama de processo comum não tem. A primeira:
**cada caixa é um link** para o capítulo, a receita ou a norma que define aquele passo. O
desenho é o índice da documentação na ordem em que o trabalho acontece; quem quer saber por
que a revisão é fresca clica na caixa "Verificar" e cai no texto que justifica. A segunda:
**os losangos em ouro estão na raia do humano**, não na dos agentes. A leitura que o
desenho sugere é a mais importante do método: o gate não julga o raciocínio do agente, ele
localiza a responsabilidade. O desenho declara quatro losangos humanos (aprovar a spec,
aprovar o plano, o merge e, na raia de infraestrutura, autorizar deploy ou migração) e um
mecânico, a DoD [CLAIM-91-005].

A raia de artefatos fecha um laço que a linha do tempo não mostra: o achado que não coube no
ciclo entra no índice de decisões, e um script cobra a retrospectiva quando a dívida
chega a quatro achados abertos ou quando o mais velho chega a seis ciclos de idade
[CLAIM-91-006]. O desenho diz "passa de quatro"; o script falha já no quarto (`>=`), e é o
script que vale. O erro recorrente vira
regra versionada, e a regra nova é argumentada contra os axiomas do método. O
[capítulo 14](../../14-a-organizacao-que-aprende/capitulo.md) conta esse laço por dentro.

O desenho tem história, e a história mostra como ele cresceu: gerado no ciclo 017, ganhou a
raia de distribuição no 019, a versão navegável no 020 e a raia de portões com o gatilho da
retrospectiva no 035 [CLAIM-91-007]. Nenhuma raia foi planejada antes; cada uma entrou quando
o processo real já a tinha e o desenho ainda não.

## As outras formas do mesmo desenho

O Maestro conta a si mesmo em várias peças, cada uma para um leitor. Vale conhecê-las porque
elas mostram uma técnica que você pode copiar: **o mesmo conteúdo em formas diferentes, cada
forma com sua fonte versionada**.

**As peças numeradas.** A pasta de diagramas tem peças de 01 a 05 (definição,
problema-solução, fluxo, a cadeia fornecedor-cliente e o processo em raias). Cada uma existe
em três formas [CLAIM-91-008]: Markdown (o texto, que se compara linha a linha numa revisão), um arquivo
HyperText Markup Language (HTML) que é a fonte visual, e um Portable Document Format (PDF)
gerado do HTML por um navegador automatizado (Playwright, num script versionado,
`render-pdf.mjs`). A 05 é a exceção: troca o PDF por uma imagem Portable Network Graphics
(PNG). O HTML é a fonte de verdade visual; o PDF é derivado e se regenera
([diagramas/README.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/diagramas/README.md)).

**O código de cores.** As peças 01 a 05 usam três cores para responder a **uma** pergunta,
"quem executa?": violeta para agente de IA, ouro para humano (decisão ou gate indelegável),
verde para o que é verificado mecanicamente. A peça 06 usa outra escala, em que verde quer
dizer "já existe hoje", e o README dos diagramas declara o conflito em voz alta: são duas
perguntas, duas escalas, e a segunda não pode passar por continuação da primeira
[CLAIM-91-008]. A lição para o seu time é pequena e barata: se uma cor significa algo, escreva
o quê, e escreva onde ela deixa de significar.

**O deck executivo.** Dez slides para quem decide se adota [CLAIM-91-009]. O argumento é uma
sequência: dois extremos que falham (sem IA, dúzias de pessoas para reconstruir a intenção
perdida de um sistema legado; com IA sem método, código que compila e erra a intenção), o
método no meio, os 12 elementos em 5 camadas, seis pilares (spec como partitura, um rege N,
gates por risco, DoD verificável, cadência enxuta, laço de aprendizado) e, no penúltimo
slide, a "prova viva": a metodologia foi construída por ela mesma, numa sessão humano + IA
([apresentacao-executiva-maestro.html](https://github.com/GHDaru/maestro/blob/19823c2/docs/handbook/apresentacao-executiva-maestro.html)).
Esse slide é o mais fraco do deck como evidência, e vale dizer por quê: "construído
por ele mesmo" é uma afirmação sobre o processo, não uma medida de resultado. O
[capítulo 15](../../15-validando-o-maestro/capitulo.md) trata o que seria preciso para
transformá-la em evidência.

**Os prompts de imagem.** O deck tem um arquivo com um prompt de imagem por slide, dez ao
todo, sob uma direção de arte única — um regente diante de uma orquestra feita de nós de
luz —, com um sufixo de estilo comum colado em todos, pedindo **nenhum texto** e muito espaço
negativo, porque o texto é sobreposto depois
([apresentacao-prompts-imagens.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/handbook/apresentacao-prompts-imagens.md))
[CLAIM-91-010]. Parece detalhe de design, mas é o mesmo princípio do resto: a imagem gerada
não é guardada como o artefato, o **prompt** é, e por isso a imagem pode ser refeita com outro
gerador sem perder a intenção. É a spec aplicada a uma figura.

**O caderno de desenvolvimento.** Dezoito slides para quem vai programar dentro do método
[CLAIM-91-011]: a raia, os artefatos do ciclo, os comandos, os portões, a revisão
independente, o gate, a retrospectiva e as armadilhas que mais custaram. Fecha com as três
coisas a guardar que abrem este apêndice. Um detalhe mostra como até um retrato cuidadoso
escorrega: os slides dos artefatos se numeram «1 de 4», «2 de 4» e «3 de 4» (spec, plano,
tarefas), e não há slide «4 de 4»; o relatório de qualidade aparece noutro slide, «Depois
do merge», sem número [CLAIM-91-023]. Ele nasceu no ciclo 053, que é a história da
próxima seção.

**A planta gerada.** A peça 07 é o ciclo desenhado por uma ferramenta, o Archify (versão
3.2.0 registrada no próprio HTML), a partir de um arquivo JavaScript Object Notation (JSON)
que descreve raias, fases, nós e arestas. O resultado é interativo, em cinco raias (o humano
Accountable; os agentes Responsible; portões, scripts e *hooks*; artefatos vivos; vermelho e
retrospectiva) e cinco fases (especificar, planejar, executar, provar, portão humano)
[CLAIM-91-012]. O que torna a peça interessante é o rótulo que o README põe nela: **retrato
de 22/10, commit `39a86ba`, sem os portões do ADR 0030**. O ADR 0030, aceito em 29/10,
trouxe portões novos que a planta não mostra, e a peça entrou no repositório no mesmo dia em
que o ADR foi aceito, já declarando o que lhe faltava [CLAIM-91-013]. Um diagrama gerado é
tão datado quanto um desenhado à mão; a diferença é que o gerado sabe de que versão veio, e
pode dizer.

## A falha real: o resumo que afirmava o que o disco não tinha

Em 14/08/2026, o ciclo 053 (raia leve) produziu duas peças de comunicação: o caderno de
desenvolvimento e a peça 06, um fluxo comparado a um desenho externo de 13 passos e marcado
como **proposta não vigente** já no título [CLAIM-91-014]. A spec tinha um requisito que,
lido de hoje, é a regra deste apêndice: todo número que a apresentação citasse — agentes,
portões, comandos, skills — deveria conferir com o disco, e o comando que confere deveria
estar no relatório de qualidade
([spec.md](https://github.com/GHDaru/maestro/blob/19823c2/specs/053-pecas-de-apresentacao/spec.md)).

Os números passaram. O relatório registra cada um com o comando: 13 agentes, 12 comandos, 6
skills, 12 templates, 16 scripts de portão, 13 deles bloqueando a integração contínua
[CLAIM-91-015]. O que não passou foi o resto. A revisão independente, em contexto fresco e
instruída a **refutar**, reprovou o ciclo com **oito grupos de defeito**, todos da mesma
família: afirmação sem lastro no disco [CLAIM-91-016]. Os mais caros:

- o caderno mandava o leitor rodar no próprio repositório um script que o instalador não
  instala (o certo era outro, que o próprio instalador indica);
- dizia que a instalação **escreve** o bloco de método no arquivo de instruções do agente,
  quando ela o **imprime** e quem acrescenta é o humano — exatamente a confusão ("copiar
  arquivo não é instalar") que um dos portões existe para impedir;
- a peça 06 dizia que "não existe fila nem critério de entrada" para intenções, quando o
  roadmap tinha fases ordenadas e uma tabela de gatilhos;
- citava um comando de busca como devolvendo zero ocorrências, e a própria página, ao
  citá-lo, fazia o comando devolver três [CLAIM-91-024].

A revisão pegou mais uma coisa, processual: as caixas da revisão e do gate estavam marcadas
no `tasks.md` enquanto o relatório ainda era um esqueleto por preencher. E a bateria de
portões não ficou verde: o script da retrospectiva estava **vermelho**, mas por dívida de
outro ciclo — um achado do ciclo 047 tinha completado seis ciclos aberto, o limite. O
relatório declarou o vermelho com o motivo em vez de deixá-lo passar como ruído, e a
retrospectiva do ciclo 055 fechou o achado dois dias depois [CLAIM-91-017]
([qa-report.md](https://github.com/GHDaru/maestro/blob/19823c2/specs/053-pecas-de-apresentacao/qa-report.md)).

A lição é desconfortável para quem escreve um apêndice como este. Um resumo é feito de
afirmações curtas, e uma afirmação curta parece verdadeira porque é fácil de ler. Num ciclo
de código, o teste reprova o que não funciona; num ciclo de documentação, nada reprova a
frase errada — salvo um revisor que não escreveu a frase e foi instruído a procurar o erro.
O catálogo de anti-padrões do Maestro registra esse defeito como o
de número 13, o portão que mede o indício e não o fato, e o
[capítulo 10](../../10-quality-gates-que-provam-fatos/capitulo.md) trata dele por inteiro.

## Por que este resumo também envelhece

Os números do ciclo 053 estavam certos **em 14/08**. O exemplo deste apêndice
([exemplo/](exemplo/README.md)) os mede de novo, em duas versões, só lendo o Git:

```text
medida                            9be9c3f    19823c2
agentes (.claude/agents/*.md)          13         13
comandos (.claude/commands)            12         12
skills (pastas em skills/)              6          6
templates (.specify/templates)         12         12
portoes (scripts/check-*.sh)           16         19
raias no BPMN (bpmn-raia)               7          7
portoes que o BPMN anuncia              8          8
archify: retrato tirado em     (peça não existe)    39a86ba
```

Entre 14/08 e 01/11, os scripts de portão foram de 16 para 19, e o desenho de processo
continua anunciando **oito** checks nas duas versões [CLAIM-91-018]. Nenhum dos três números
está errado no dia em que foi escrito; o desenho é que não tem relógio. A planta gerada, ao
contrário, carrega a versão de onde saiu. O padrão que o livro tira disso tem três partes:

1. **Todo resumo cita a versão.** Este apêndice cita `19823c2` em todo link. Se o Maestro
   mudar, o link continua mostrando o que o texto descreveu.
2. **Todo número tem um comando.** É a regra de evidência do livro inteiro, e o motivo de
   cada identificador de claim (prefixo 91).
3. **Proposta e vigente não se misturam.** A peça 06 diz "proposta" no título, no primeiro
   parágrafo e no índice; a 05 é o processo em vigor. Uma proposta que passa por adotada é
   pior que a ausência dela, como dizia o primeiro requisito do ciclo 053.

## Como ler o Maestro

O repositório tem um ponto de entrada, chamado "Comece por aqui", que conta a dor, a
jornada e o sistema em cinco minutos e depois dá um mapa de leitura em quatro paradas
[CLAIM-91-021]
([comece-por-aqui.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/comece-por-aqui.md)):

1. **os princípios** — os oito inegociáveis, curtos, para ler primeiro [CLAIM-91-020];
2. **o modelo operacional** — a regra vigente: papéis, cerimônias, artefatos, raias, gates;
3. **o handbook** — o porquê de cada regra, um capítulo por elemento;
4. **a prática** — os moldes já prontos: o comando que abre uma spec, o modelo de pull request
   que espelha a DoD, o comando que roda a DoD e mostra a evidência.

E um glossário para toda sigla, porque a constituição do método proíbe sigla sem forma por
extenso na primeira ocorrência.

O site do método organiza o mesmo material em **cinco trilhas**, cada uma de um tipo
diferente de documentação: a Jornada (tutorial: o diálogo que construiu o método), os
Capítulos (explicação), as Receitas (como fazer: abrir um ciclo, escrever um critério
verificável, rodar a retrospectiva), a Referência (princípios, modelo, glossário, agentes,
skills, moldes) e os Bastidores (decisões, estudos, histórico de mudanças). Por cima delas, uma
**cadência de estudo** que diz quanto tempo cada profundidade custa: Entender em cerca de
20 minutos, Aprender em cerca de 2 horas, Aplicar em cerca de 1 dia, Aprofundar de forma contínua
[CLAIM-91-019]
([guia-editorial.md §5–6](https://github.com/GHDaru/maestro/blob/19823c2/docs/livro/guia-editorial.md)).
A cadência é uma boa ideia para copiar no onboarding do seu time: um novo membro sabe o que
ler na primeira hora e o que pode esperar a primeira semana.

## Em que o Maestro difere das alternativas

Um tech lead que lê esta página vai perguntar o que o Maestro tem que um fluxo já conhecido
não tem. A resposta curta: o Maestro não compete com as ferramentas de desenvolvimento
dirigido por spec; ele se apoia numa delas e acrescenta a camada que elas não trazem. O
registro de decisão que criou o modelo operacional diz isso com todas as letras: a
constituição dá os princípios, o Spec Kit (a ferramenta de spec do GitHub) dá o fluxo
técnico de uma feature, e faltava o meio — quem faz o quê, quando, e o que se produz com
qual portão — para **um** desenvolvedor regendo vários agentes, não um time de várias
pessoas [CLAIM-91-028]
([ADR 0004](https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0004-modelo-operacional.md)).

O Maestro avaliou as alternativas e guarda o veredito num catálogo com uma ficha por
**ideia**, não por ferramenta, e um índice com o veredito corrente. Na versão citada, o
índice tem 41 ideias: uma adotada, 14 absorvidas, 16 em observação e 10 descartadas
[CLAIM-91-027]
([docs/ecosystem/](https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/README.md)).
As que um tech lead mais provavelmente consideraria:

| Alternativa | O que oferece | Veredito no Maestro | Por quê |
|---|---|---|---|
| Prompt sem spec | velocidade no primeiro dia | rejeitado | produz código que compila e erra a intenção |
| GitHub Spec Kit | spec → plano → tarefas como comandos, com moldes | **adotado**, a única ferramenta de terceiro | dá forma ao Princípio I; o Maestro roda por cima dele |
| OpenSpec | mudança como *delta* (propor, aplicar, arquivar), leve | descartado como segunda ferramenta; a ideia virou a raia leve | duas ferramentas de spec seriam duas fontes de verdade de processo |
| Breakthrough Method for Agile AI-Driven Development (BMAD) | um time ágil inteiro de agentes (gerente de produto, arquiteto, desenvolvedor, *Scrum Master*), com épicos e *stories* | descartado | substituiria o modelo em vez de somar; a cerimônia ao estilo Scrum já tinha sido cortada |
| Kiro (da Amazon Web Services, AWS) | ambiente de desenvolvimento integrado (*Integrated Development Environment*, IDE) com spec primeiro e requisitos no formato Easy Approach to Requirements Syntax (EARS) | ferramenta descartada (proprietária, prende à IDE); a sintaxe EARS absorvida | a ideia atravessa, o *lock-in* não |
| Superpowers | biblioteca de skills com leis obrigatórias | não adotado por atacado; ideias absorvidas (a Iron Law, causa raiz antes do conserto) | criaria um segundo processo obrigatório |

Fontes da tabela: o capítulo de spec do handbook (§5.4), o ADR 0005, o ADR 0008 e as fichas
do catálogo [CLAIM-91-027]. O formato EARS é `QUANDO <condição> O SISTEMA DEVE
<comportamento>`; a expansão da sigla BMAD é a que a ficha de pesquisa do Maestro registra.

O que fica de diferente, para decidir o que copiar:

- **Scrum com agentes** transporta cerimônias de um time de pessoas. O Maestro as troca por
  artefatos e portões: o caderno de desenvolvimento diz "sem daily, sem planning, sem
  backlog grooming", porque a função dessas reuniões passou para os arquivos e os scripts
  [CLAIM-91-028]. Se o seu time tem várias pessoas que precisam se sincronizar, essa troca
  não vale por inteiro.
- **Um fluxo de spec sozinho** (Spec Kit puro) dá a sequência, mas não dá o gate
  proporcional ao risco, a revisão sem permissão de escrita, a regra de raia nem o gatilho
  da retrospectiva. É essa camada que vale avaliar no Maestro, não o fluxo.
- **O próprio catálogo** é a parte mais barata de copiar: uma ficha datada por ideia, um
  veredito corrente com gatilho de reavaliação, e "observar" sem gatilho recusado por
  script.

O limite da comparação está declarado no ADR 0008: as ferramentas foram fichadas por fontes
primárias, sem instalar cada uma [CLAIM-91-027]. É um veredito de leitura, não de uso, e o
livro o trata assim.

### Critério de adoção para um tech lead

O mapa acima diz o que o Maestro é; a decisão de adotá-lo depende do que ele custa e do
primeiro passo que a testa. Três custos são conferíveis no disco:

- **O que se mantém.** Na versão citada, o método instalado traz 13 agentes, 12 comandos,
  6 skills, 12 moldes (*templates*) e 19 scripts de portão `check-*.sh` [CLAIM-91-018].
  Cada um é código ou instrução que alguém do time precisa entender quando der vermelho.
  Os scripts passaram de 16 para 19 entre agosto e novembro de 2026: o método muda, e
  acompanhá-lo é parte do custo.
- **O que se instala.** O caminho completo leva cerca de 5 minutos, segundo a receita. Os
  atalhos (plugin, `npx skills add`) são mais leves, mas não trazem scripts nem governança
  [CLAIM-91-029]: levam o vocabulário sem os portões, que são justamente a camada que o
  diferencia de um fluxo de spec sozinho.
- **O tempo por ciclo.** Não há número publicado no Maestro, e este livro não inventa um.
  Meça no primeiro ciclo leve e no primeiro pleno, e compare com o que o mesmo trabalho
  custava antes.

A decisão, em três perguntas:

1. **Uma pessoa vai reger vários agentes?** Se sim, o Maestro foi desenhado para esse caso
   [CLAIM-91-028]. Se o time é de várias pessoas que se sincronizam em reuniões, adote as
   peças (raias, revisão independente, portões que conferem fatos), não o modelo inteiro.
2. **O projeto vai durar mais que algumas semanas?** Um protótipo que vai para o lixo não
   paga spec, claims nem retrospectiva com gatilho; a raia leve basta, ou nem ela.
3. **Alguém vai manter os scripts?** Um portão que dá vermelho e ninguém sabe consertar vira
   portão desligado. Se não há quem mantenha os 19, comece com os dois ou três que conferem o
   que mais dói no seu time.

O primeiro passo que testa tudo isso é o da página de abertura: instalar num repositório de
teste e rodar um ciclo da raia leve. Se o ciclo leve já pesar, o pleno vai pesar mais.

## Quando este resumo atrapalha

Tudo o que este apêndice recomenda tem custo, e há casos em que o custo não se paga.

**Um resumo que ninguém consome apodrece.** O Maestro tem um corolário para isso: a
documentação que nada consome vai apodrecer, por melhor que seja (C9). O caso mais claro
está dentro da própria constituição, que resume a camada de axiomas com contagens que não
acompanharam o arquivo resumido [CLAIM-91-026]. Nenhum script lê aquele parágrafo, e
por isso nenhum script reclamou. Se ninguém vai ler a sua página "o processo em uma
página" para tomar uma decisão, não a escreva; aponte para a fonte.

**Um claim por número custa.** Este apêndice tem mais de vinte claims, cada um com um
comando. Num projeto de duas semanas, com uma pessoa, um deck que serve a uma reunião só não
precisa disso: marque os números como opinião com data e siga. A regra se paga quando
alguém vai decidir com base no número — adotar, investir, auditar — ou quando o resumo vai
viver mais que a versão que descreve.

**A revisão que refuta é a parte cara e a que mais rende.** O ciclo 053 era de raia leve, e
mesmo assim a revisão independente achou oito grupos de defeito [CLAIM-91-016]. Para um
texto interno, de vida curta, a revisão do próprio autor contra o disco pode bastar; para o
que vai a quem decide, não basta.

**O resumo não substitui o método.** O caderno do 053 mandava o leitor rodar um script que o
instalador não instala. Quem seguiu o resumo em vez da fonte seguiu o erro. Use esta página
para se orientar e o repositório, na versão citada, para agir.

**O Maestro inteiro pode ser demais.** O método foi desenhado para uma pessoa regendo vários
agentes [CLAIM-91-028]. Num time de várias pessoas sem agentes, ou num protótipo que vai
para o lixo, a spec para tudo vira burocracia — o próprio handbook diz isso ao justificar
as raias. A raia leve existe para esse caso, e a pergunta do passo zero vale mais que
qualquer peça desta página.

## Onde cada peça aparece neste livro

| Peça do Maestro | O que o livro discute | Onde |
|---|---|---|
| Princípio central, os dois extremos | o que fica caro quando gerar fica barato | [capítulo 1](../../01-a-mudanca-de-unidade-de-trabalho/capitulo.md) |
| O humano responde pela política | o Accountable humano e o gate que localiza responsabilidade | [capítulo 2](../../02-o-problema-da-confianca/capitulo.md) |
| Um rege N | o gargalo da atenção humana | [capítulo 3](../../03-um-humano-muitos-agentes/capitulo.md) |
| Spec como partitura, raias | a spec que gera, o requisito que a máquina confere | [capítulo 4](../../04-a-spec-como-partitura/capitulo.md) |
| Fluxo agêntico, rastreabilidade | as operações sobre o contexto | [capítulo 5](../../05-engenharia-de-contexto/capitulo.md) |
| Orquestração, fatiar por fronteira | onde cortar | [capítulo 6](../../06-como-dividir-o-trabalho/capitulo.md) |
| Os agentes estreitos, as skills | papel como modo de trabalho | [capítulo 7](../../07-papeis-e-skills/capitulo.md) |
| Portões, DoD executável | o check que mede o fato | [capítulo 10](../../10-quality-gates-que-provam-fatos/capitulo.md) |
| Gates por risco, reversibilidade | quanta autonomia dar | [capítulo 11](../../11-risco-reversibilidade-e-autonomia/capitulo.md) |
| Retrospectiva com gatilho, constituição | a organização que aprende sem inchar | [capítulo 14](../../14-a-organizacao-que-aprende/capitulo.md) |
| "Construído por ele mesmo" | testar uma metodologia | [capítulo 15](../../15-validando-o-maestro/capitulo.md) |

## Checklist para quem avalia adotar o Maestro

- [ ] Instalou num repositório de teste e a verificação da instalação passou.
- [ ] Rodou um ciclo da raia leve inteiro (teste falhando antes, pull request, revisão por
      quem não escreveu) e anotou quanto tempo levou.
- [ ] Sabe quem do time vai manter os scripts de portão quando um deles der vermelho.
- [ ] Decidiu, por escrito, quais peças adota e quais deixa de fora, e por quê.
- [ ] Marcou a versão do Maestro que avaliou, para saber o que mudou na próxima vez.

## Checklist para o resumo do seu próprio método

Se o seu time tem um deck, um diagrama ou uma página "o nosso processo em uma página", confira:

- [ ] O resumo diz de que versão do repositório ele é um retrato (commit ou data), e o link
      aponta para essa versão, não para a ponta do ramo.
- [ ] Cada número do resumo tem um comando que o reproduz, escrito ao lado ou num arquivo de
      claims; número sem comando foi removido ou marcado como opinião datada.
- [ ] O que é proposta está marcado como proposta no título, no primeiro parágrafo e no índice.
- [ ] Toda cor, ícone ou forma que carrega significado tem legenda, e a legenda diz onde ela
      deixa de valer.
- [ ] Os pontos de parada humanos (os losangos) estão desenhados na raia do humano, e a lista
      deles bate com a lista de gates do processo vigente.
- [ ] Um revisor que não escreveu o resumo, instruído a refutar, leu cada afirmação contra o
      disco antes da publicação.
- [ ] Há um mapa de leitura para quem chega: o que ler na primeira hora, no primeiro dia e
      depois.

## Evidência

Os claims deste apêndice estão em [claims.md](claims.md), 29 ao todo, em dois estados:

- **`medido`** (13): um comando sobre o Git do Maestro reproduz o número — 004, 006, 009,
  010, 011, 012, 013, 018, 020, 022, 023, 026 e 027.
- **`observado`** (16): o Maestro registra o fato e o livro leu o registro; não há comando
  que gere o número, só a linha do arquivo que o afirma — 001, 002, 003, 005, 007, 008, 014,
  015, 016, 017, 019, 021, 024, 025, 028 e 029. Estes valem o que vale a leitura: o comando do
  claim mostra o trecho, e conferir é ler.

O exemplo executável ([exemplo/](exemplo/README.md)) reproduz de uma vez só o CLAIM-91-018
e, de passagem, o número de raias do CLAIM-91-004; os demais `medido` se conferem um a um
pelo comando da tabela. O script só lê o Git; o tempo de execução depende de quão rápido o
Git responde na máquina: em três execuções no Windows, entre 02 e 03/11/2026, levou de
11 s a cerca de 80 s, com a mesma saída. Conte com segundos a pouco mais de um minuto.

**Hipóteses que o apêndice toca e não prova.** O apêndice descreve o método; não mede se ele
funciona. Quatro hipóteses da agenda de pesquisa do livro (H1–H10) aparecem aqui como
premissa do Maestro, e o livro as trata como **hipótese**:

- **H1** — a spec reduz retrabalho (a primeira ideia; capítulos 4 e 15);
- **H2** — a revisão em contexto fresco acha mais defeito (o caso do ciclo 053 é um episódio
  a favor, não uma medida);
- **H8** — a reversibilidade permite mais autonomia (a terceira ideia; capítulo 11);
- **H10** — a retrospectiva que vira regra reduz recorrência (o gatilho da retro;
  capítulo 14).

Uma afirmação do deck executivo — que o método foi construído por ele mesmo numa sessão
humano + IA — é tratada como **afirmação da fonte**, não como evidência: o livro a reporta e
não a usa como argumento. O mesmo vale para os vereditos do catálogo do ecossistema, que
são de leitura de fontes primárias, não de uso das ferramentas.

## Referências

- Maestro, versão `19823c2` (01/11/2026): <https://github.com/GHDaru/maestro/tree/19823c2>.
  Arquivos citados: `docs/comece-por-aqui.md`, `docs/handbook/README.md`,
  `docs/handbook/apresentacao-executiva-maestro.html`,
  `docs/handbook/apresentacao-desenvolvimento-maestro.html`,
  `docs/handbook/apresentacao-prompts-imagens.md`, `docs/diagramas/README.md`,
  `docs/diagramas/01-definicao.md`, `docs/diagramas/03-fluxo.md`,
  `docs/diagramas/05-bpmn-processo.md`, `docs/diagramas/maestro-workflow.archify.json`,
  `docs/livro/guia-editorial.md`, `specs/053-pecas-de-apresentacao/`,
  `docs/governance/axioms.md`, `docs/governance/principles.md`,
  `docs/adr/0004-modelo-operacional.md`, `docs/adr/0005-raias-de-trabalho-e-specs-de-infra.md`,
  `docs/adr/0008-avaliacao-ecossistema-sdd.md`, `docs/ecosystem/` (README, `estado.jsonl`,
  `fontes.md`, fichas 010 e 031), `docs/handbook/03-spec-driven.md`,
  `docs/research/avaliacao-ecossistema-sdd.md`, `docs/receitas/instalar-o-maestro.md`.
- Object Management Group. *Business Process Model and Notation (BPMN), Version 2.0.2*.
  OMG, 2013. <https://www.omg.org/spec/BPMN/2.0.2/> (acesso em 02/11/2026).
- Archify, gerador de diagramas interativos a partir de JSON; versão 3.2.0, conforme
  registrada no arquivo gerado `docs/diagramas/maestro-workflow.archify.html` do Maestro.
