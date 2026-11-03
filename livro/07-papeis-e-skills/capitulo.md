# 07 — Papéis e skills

> *Um papel que só existe no documento é um papel que ninguém exerce, e o documento continua
> parecendo correto.*

Todo tech lead que começa a usar agentes escreve, cedo ou tarde, um prompt que começa com
"você é um engenheiro sênior". Funciona por uma tarde. Este capítulo é sobre o que vem
depois: como transformar uma frase de identidade num **modo de trabalho**, com escopo, contrato,
permissões, faixa de modelo e um portão que diz quando ele deixou de existir; e como empacotar
os procedimentos que o seu time repete numa **skill** que o agente segue sem que você precise
lembrá-lo. A tese é simples e custou ao Maestro três falhas para aprender: papel e skill não são
texto, são **pares** (a norma que os prescreve e o executável que os entrega), e a distância entre
os dois lados só fica pequena se uma máquina a medir.

## Pergunta central

Como dar a um agente um modo de trabalho, e não só um prompt, e como saber, por máquina, que
esse modo de trabalho existe de fato?

## Resultado de aprendizagem

Ao final deste capítulo, você consegue:

1. **Derivar** do teorema "quem executa não verifica" (T2) por que os papéis de um time de
   agentes são estreitos, separados por janela de contexto e diferenciados por permissão de
   ferramenta.
2. **Escrever** o perfil de um papel com os sete campos que o distinguem de um prompt (escopo,
   faz e não faz, consome e produz, entrega a, ferramentas, gate e faixa de modelo) e
   **distinguir** perfil de sessão, e skill de comando e de agente.
3. **Redigir** uma skill com gatilho, lei de ferro e desculpas fechadas, e **testá-la** contra
   uma linha de base em que o agente falha sem ela.
4. **Montar** um portão que compara, nos dois sentidos, os papéis que a sua norma prescreve com
   os executáveis que o seu repositório tem, e **provar** por mutação que ele acusa.
5. **Decidir** a faixa de modelo de cada papel como uma escolha registrada, com custo e gatilho
   de revisão, em vez de deixá-la implícita.

## A falha real

Em 1º de agosto de 2026, o Steward do Maestro (o humano que decide o quê e o porquê) trouxe dois
relatos sem relação aparente. No primeiro, outra Inteligência Artificial (IA) tinha tentado
instalar o método num projeto e respondido que "não tinha" instalador. No segundo, o diagrama do
processo, desenhado em *Business Process Model and Notation* (BPMN), não mostrava nada sobre
experiência de usuário (*user experience*, UX) nem sobre jornadas. O ciclo 018 abriu para
investigar os dois e achou duas lacunas de naturezas diferentes [CLAIM-07-001].

A primeira era de visibilidade: o instalador existia desde o ciclo 013, mas o `README.md`, o
único arquivo que uma IA lê primeiro, não o citava. A segunda é a que interessa a este capítulo.
O modelo operacional do método prescrevia um **UX-agent** na tabela de papéis, declarava
`ux-design.md` como artefato essencial sempre que houvesse interface, citava um documento de
jornada e exigia o `ux-design.md` na definição de pronto para iniciar. Não havia agente, skill nem
template para nenhum dos quatro. A prescrição estava ali **havia catorze ciclos** [CLAIM-07-001].
Nenhum relatório de qualidade pegou, e o relatório do 018 diz por quê: os checks olhavam sempre
para dentro do ciclo, nunca para a distância entre o que o modelo manda e o que o toolkit tem.

A correção não foi só criar o agente. Foi criar o agente (`ux-semantica`, hoje `ux-semantics`),
a skill de jornada viva, os dois templates **e** um script, `verificar-papeis.sh` (hoje
`check-roles.sh`), que falha quando um papel prescrito não tem agente. O script foi aceito só
depois de ser visto falhando: com o agente removido, saiu com código 1 nomeando o papel ausente.
E houve um efeito colateral que o relatório registra com gosto: ao subir de doze para treze
agentes, o portão anterior, `verificar-agentes.sh`, que esperava doze, falhou sozinho
[CLAIM-07-002]. O portão de contagem tinha feito o trabalho dele.

O 018 seria uma anedota se a mesma família de defeito não tivesse voltado duas vezes no mesmo
mês, por outras portas.

Em 16 de agosto, a retrospectiva do ciclo 055 achou que o `plan-architect`, o agente que escreve
o plano, era instruído a consumir "a linguagem ubíqua" do projeto como fonte obrigatória. O
artefato não existia em projeto nenhum. O registro de decisões resume o defeito numa frase: o
agente segue fielmente uma fonte que não existe. O ciclo 061 fechou o achado tirando a promessa da
instrução; no dia seguinte, a revisão independente dos ciclos 061 e 062, registrada no 063,
mostrou que o fechamento era falso: a promessa tinha saído do arquivo que o portão de instalação
lê e continuado em outros que ele não lê [CLAIM-07-005].

Em 23 de agosto, o mesmo ciclo 063 registrou o terceiro caso, agora do lado das skills: **quatro
das seis skills** do método não eram citadas por nenhum capítulo numerado do livro que as ensina,
e o portão que existia para isso pulava o pior caso em silêncio [CLAIM-07-004].

Três falhas, uma forma. No 018, a **norma** prescrevia um papel que nenhum **executável**
entregava. No 055, o executável mandava consumir algo que nenhuma norma produzia. No 063, a skill
existia sem que nada de fora a consumisse. Em todos, o documento parecia certo, e o defeito só
existia na **diferença** entre dois lugares que ninguém comparava. É desse defeito que este
capítulo parte.

## Teoria

### Papel é modo de trabalho, não cargo

Num time humano, decidir, executar e verificar são, em geral, pessoas diferentes, e é essa
separação que cria o contrapeso: quem escreveu não aprova, quem aprova não confere sozinho.
Quando uma pessoa opera muitos agentes, os três papéis colapsam naturalmente na mesma cabeça. O
contrapeso some sem que ninguém decida acabar com ele, e some com a sensação de estar indo mais
rápido, porque de fato está, até o primeiro erro caro.

A resposta do Maestro é tratar papel como **modo de trabalho**, e não como cargo. Um papel é
exercido por um humano, por um agente ou pelos dois com um gate entre eles. O vocabulário mínimo
para separar os modos é a matriz *Responsible, Accountable, Consulted, Informed* (RACI): quem
executa (R), quem responde (A), quem é consultado (C) e quem é informado (I). A adaptação que
importa é uma só: **o A não migra**. Executar (R) e verificar (C) vão para agentes; informar (I)
vai para o registro (o changelog, o índice de decisões); responder pelas consequências fica com
um humano, exatamente um por tarefa. O [capítulo 2](../02-o-problema-da-confianca/capitulo.md)
trata do porquê (o axioma A2, "a consequência precisa de dono") e da armadilha do funil, em que o
humano responde por cada item e vira o gargalo do próprio sistema. Aqui interessa a outra metade:
como os R e os C, que são agentes, ganham forma.

### De T2 ao papel estreito

O teorema T2 do Maestro diz que **quem executa não verifica**, e o deriva de dois axiomas. De A2:
alguém precisa responder pelo resultado, então alguém que não o produziu precisa olhá-lo. De A3,
"o contexto é finito e se degrada conforme enche": o agente que escreveu carrega na janela os becos
sem saída que explorou, e o único jeito de olhar o diff sem essa carga é um **contexto fresco**
([axioms.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/axioms.md)).

Leia o teorema do lado de quem desenha os papéis e saem três consequências.

A primeira: papéis distintos são **janelas distintas**. Um "agente que escreve e depois revisa"
não satisfaz T2 por mais que o prompt peça imparcialidade, porque a janela é a mesma. Separar
papéis é, antes de tudo, separar sessões. O handbook do Maestro registra a consequência prática
como duas decisões gêmeas: o agente generalista gigante foi **rejeitado** (a janela cheia degrada e
o prompt cresce sem limite) e a **revisão adversarial do diff**, um modelo fresco tentando refutar o
"pronto", foi adotada como gate antes do merge.

A segunda: a independência do verificador é **configuração, não promessa**. Pedir ao revisor que
não conserte é intenção; tirar dele a ferramenta de edição é estrutura. O corolário C3 diz isso em
uma linha ("o papel que julga não recebe permissão de escrita"), e o Maestro o cumpre na lista de
ferramentas de cada agente. O capítulo 2 mostra o mecanismo e o seu limite (o `Bash` também
escreve); este capítulo o toma como dado.

A terceira consequência é o corolário C8, que o Maestro deriva de T2 e do teorema T5 (um artefato
sobrevive por ser consumido ou por ser imutável): **um agente estreito é mais barato que um agente
capaz**. O perfil é consumido a cada invocação, e por isso custa a cada invocação: o próprio texto
e as skills que ele carrega. O que o papel não vai usar é ruído pago em contexto, e o ruído degrada
o que vem depois (A3). Daí o formato: um papel do Maestro cabe em vinte e poucas linhas. Os treze perfis
executáveis do método somam 285 linhas na versão citada por este livro, com média de 21,9 e o
maior com 36 [CLAIM-07-006]. É pouco porque o papel não é um manual; é um contrato.

### Anatomia de um papel: os sete campos

O que distingue um papel de um prompt não é o tamanho nem o tom; é o que ele **declara**. Lendo os
treze perfis do Maestro, a estrutura é sempre a mesma, e um oitavo campo, que o Maestro não tem,
este livro propõe acrescentar.

| Campo | Pergunta que responde | Exemplo no Maestro |
|---|---|---|
| Escopo | o que este papel é, numa frase | "julgar, não consertar" (`review`) |
| Faz / não faz | o que nunca é deste papel | o `spec-agent` não decide arquitetura; o `plan-architect` não escreve código de produção |
| Consome / produz | que artefato entra, que artefato sai | o `qa` consome o build e a spec, produz testes e o `qa-report.md` |
| Entrega a | para quem vai o trabalho (o *handoff*) | o `dev-implementer` entrega ao `review`, em contexto fresco |
| Ferramentas | o que o papel consegue fazer no mundo | `review`: `Read, Grep, Glob, Bash`, sem `Write` nem `Edit` |
| Gate | o que precisa ser verdade para o trabalho avançar | "o humano aprova o plano" (modelo operacional, §4) |
| Faixa de modelo | em que classe de modelo este papel roda, e por quê | **ausente no Maestro** — ver "Papel × modelo × custo" |

Dois campos merecem um comentário. O "não faz" parece redundante com o escopo, e não é: é ele que
impede o papel de crescer por acréscimo. O `review` do Maestro diz que aponta **só lacunas de
correção ou de requisito, não preferências de estilo**, porque um revisor que caça tudo induz
*over-engineering* ([review.md](https://github.com/GHDaru/maestro/blob/19823c2/.claude/agents/review.md)).
Sem essa linha, o revisor faz o que um modelo prestativo faz por padrão: sugere. E o "entrega a"
transforma uma coleção de agentes num fluxo: cada papel sabe quem vem depois, e o artefato que
passa de um para o outro (a spec, o plano, o diff, o veredito) é a interface entre eles, não a
conversa.

### Perfil e sessão

Uma distinção que o Maestro só tornou explícita no ciclo 073 evita muita confusão na prática. O
**perfil** de um agente é o par arquivo descritivo e arquivo executável (no Maestro, o
`.claude/agents/<nome>.md`), com papel, ferramentas e, segundo o glossário, modelo padrão; não
tem identidade de execução. A **sessão de agente** é uma execução: o humano a sobe, a observa e a
derruba, e ela é a unidade de administração [CLAIM-07-026]. Quando alguém diz "o revisor errou", vale perguntar qual dos dois: se o
perfil está errado, todas as sessões futuras errarão igual, e a correção é no arquivo; se a sessão
errou com um perfil certo, a correção é de contexto, e o arquivo não deve mudar por causa dela.

### Skill: o como, que dispara pelo contexto

O papel diz **quem** faz. A skill diz **como** se faz um procedimento recorrente, e dispara pelo
contexto, sem que alguém a chame. O formato que o ecossistema convergiu é um diretório com um
arquivo `SKILL.md`: um cabeçalho com `name` e `description`, e um corpo com passos verificáveis. A
`description` é a peça crítica, porque é ela que o harness lê para decidir se a skill se aplica; o
agente que escreve skills no Maestro tem uma linha só para isso: a descrição é o que faz a skill
**disparar na hora certa**, então os gatilhos ("Use quando…") se escrevem com cuidado
([skill-author.md](https://github.com/GHDaru/maestro/blob/19823c2/.claude/agents/skill-author.md)).

Três peças costumam ser confundidas, e o Maestro as separa assim
([skills/README.md](https://github.com/GHDaru/maestro/blob/19823c2/skills/README.md)):

- **Skill**: *como fazer*; dispara pelo contexto.
- **Comando**: invocação explícita (`/dod`, `/eval`); alguém o chama.
- **Agente**: *quem faz*; consome skills e comandos.

O exemplo do próprio README é bom: a skill `verifiable-dod` ajuda a **escrever** as verificações
de um critério de aceite; o comando `/dod` as **roda**. Uma é conhecimento que entra na janela quando
o contexto pede; o outro é uma ação com hora marcada.

A regra de nascimento de uma skill é a parte que mais falta nos times que adotam o formato:
**skill só nasce de dor recorrente provada**, nunca de especulação, e, desde o ciclo 011, uma skill
original nova só é publicada com uma **linha de base testada** (o cenário de pressão em que o agente
falha sem ela e cumpre com ela). Skill especulativa é contexto pago para ensinar algo que ninguém
mostrou ser necessário, e pior: ensina sem que ninguém saiba se ensina a coisa certa.

### Lei de ferro: engenharia de prompt como engenharia de processo

Uma skill que descreve é racionalizável. "Considere investigar a causa antes de consertar" é uma
frase que o modelo pondera contra a pressa do pedido e, sob pressão, descarta. O padrão que o
Maestro absorveu do projeto Superpowers em julho de 2026 resolve isso com engenharia de linguagem:
cada skill abre com uma **lei de ferro** (*Iron Law*), uma regra em imperativo absoluto num bloco
de código, seguida da fórmula "violar a letra é violar o espírito" e de duas ou três desculpas
**explicitamente fechadas** ("isto NÃO é desculpa: …").

A skill de diagnóstico do Maestro mostra o formato inteiro:

```text
NO FIX WITHOUT A ROOT-CAUSE INVESTIGATION FIRST
```

Seguem as desculpas que não valem: "está óbvio o que quebrou" (se estivesse, o bug não existiria),
"o conserto é pequeno, testo depois" (conserto sem causa confirmada é aposta), "já vi esse erro
antes" (padrão parecido não é a mesma causa)
([diagnose-before-fix/SKILL.md](https://github.com/GHDaru/maestro/blob/19823c2/skills/diagnose-before-fix/SKILL.md)).
Depois vêm seis fases em ordem (ler o erro inteiro, reproduzir com um teste que falha, isolar,
formular **uma** hipótese, prová-la, só então consertar) e os sinais de que uma foi pulada: a
segunda tentativa "tenta isto" seguida, o conserto que funcionou sem que se saiba explicar por quê,
o conserto que alargou o escopo. A skill nasceu de uma lacuna real: o Maestro já exigia um teste que
reproduzisse o bug, mas não tinha nenhuma disciplina de diagnóstico antes do conserto.

Por que funciona: a lei fecha a racionalização **antes** de ela aparecer. O modelo que lê
"considere" negocia; o que lê a lei com a desculpa dele já listada e recusada tem menos por onde
escapar. Por que tem limite: a lei continua sendo instrução. Ela muda a probabilidade, não a
possibilidade. O que torna uma regra impossível de violar é um portão ou uma permissão, e é por
isso que o Maestro põe a independência do revisor na lista de ferramentas, e não numa lei de
ferro. A lei é para o que não se consegue impedir por configuração: a disciplina de raciocínio.

A forma não é exclusiva de skills. O guia editorial do livro do Maestro tem a sua própria lei de
ferro (nenhum capítulo publica sem objetivos, exemplo real e verificação), cobrada pelo
`check-chapters.sh`, e o guia deste livro a herdou na anatomia de onze seções. Sempre que uma regra
é violada por racionalização ("o tema é abstrato", "verifico depois"), e não por incapacidade, a
lei de ferro é a forma certa.

Duas restrições acompanham a lei para que ela não vire tirania. Ela é **estreita**, uma regra por
skill, não um código de conduta. E a exceção existe, mas é **decisão humana registrada**, nunca
interpretação do agente.

### Linha de base para skills, ablação para papéis

A segunda ideia absorvida do Superpowers é tratar a skill como código: *test-driven development*
(TDD) aplicado a prosa. Escreve-se o cenário de pressão; roda-se um subagente **sem** a skill e
registra-se a falha (vermelho); escreve-se a skill; roda-se de novo **com** ela (verde); fecham-se
as brechas que o teste expôs (refatoração). A frase que justifica o protocolo vale para qualquer
time: se você não viu um agente falhar sem a skill, não sabe se ela ensina a coisa certa.

O mesmo raciocínio vale para cada linha de um papel, e o Maestro o aplicou aos agentes a partir do
ciclo 037 com uma técnica que vale roubar: a **ablação**. Roda-se o caso contra o agente real e contra o mesmo
agente **menos uma instrução**. Se o ablado falha onde o real passa, a linha paga o contexto que
custa; se os dois passam, a linha talvez não sirva. No caso 001, o `review` sem a instrução de
comparar o diff com o plano fez uma ótima revisão de código, achou cinco defeitos reais e **reprovou
o caso**, porque tratou como bug de código o que era um requisito não implementado. No caso 002, o
`process-guardian` sem a instrução de conferir a raia declarada chegou à mesma conclusão que o
real, duas vezes, pelo Princípio III sozinho [CLAIM-07-013]. A primeira linha provou que paga; a
segunda ficou sob suspeita de redundância.

### Papel × modelo × custo

Um papel tem três custos, e só um deles costuma ser medido.

O **custo fixo de contexto** é o que o papel carrega para a janela a cada invocação: o próprio
perfil, as skills que ele consome e o que a instrução do projeto importa por padrão. No Maestro,
os treze perfis somam cerca de 3,7 mil *tokens* estimados [CLAIM-07-006], e a constituição
importada em toda sessão custa, medido no ciclo 056, 6.072 bytes, cerca de 1.518 tokens
[CLAIM-07-017]. Esse custo é a razão do corolário C8, e o Maestro o mede.

O **custo de modelo** é o preço por token da classe de modelo em que o papel roda, multiplicado
pelo volume que ele lê e escreve. Aqui o Maestro tem uma lacuna que ele mesmo documenta sem querer:
a spec do ciclo 003, que criou os subagentes, previa o campo `model` no cabeçalho de cada um, e o
glossário define o perfil como portador de um "modelo padrão"; mas **nenhum** dos treze arquivos
declara modelo [CLAIM-07-008]. Todos rodam no modelo da sessão que os chama. O revisor que julga um
diff de infraestrutura e o escritor técnico que atualiza o changelog custam o mesmo por token.

O **custo de coordenação** é o das passagens de bastão: cada papel a mais é um *handoff* a mais, um
artefato intermediário a mais e uma chance a mais de um papel consumir algo que o anterior não
produziu (a falha do 055).

A proposta deste livro para a lacuna do meio é modesta: **declare a faixa de modelo por papel**,
como decisão registrada, com o motivo e o gatilho de revisão. A intuição é que papéis mecânicos e
bem especificados (atualizar changelog, aplicar um template, rodar uma verificação) toleram um
modelo menor, e papéis que julgam (revisão, segurança, arquitetura) são onde um erro escapa para
mais longe e, portanto, onde o modelo maior se paga. É uma intuição, não um resultado: a hipótese
H9 da agenda de pesquisa ("um modelo menor basta em tarefa estruturada") ainda não foi testada
[CLAIM-07-024]. O que já se sabe é que, sem o campo declarado, a escolha existe do mesmo jeito,
só que implícita, e escolha implícita não se revisa.

## Alternativas

A pergunta "como dar papéis a agentes" tem pelo menos sete respostas no mercado e na literatura. O
quadro abaixo as compara pelo que importa a quem responde pelo resultado: a independência do
verificador, a separação de janelas e a existência de um portão que mede a distância entre a
norma e o executável.

| Abordagem | O que oferece | O que falta | Veredito |
|---|---|---|---|
| **Um agente generalista grande** | simplicidade aparente; nenhum *handoff* | a janela enche e degrada; o prompt cresce sem limite; quem escreve é quem revisa | **rejeitado** — viola T2 e C8 de uma vez |
| **Persona no prompt** ("você é um engenheiro sênior") | tom e foco por uma sessão | escopo, contrato, permissões e gate; nada que um portão confira | **insuficiente** — é o ponto de partida, não o papel |
| **Papel como identidade narrativa** (o padrão *role, goal, backstory* do CrewAI) | vocabulário claro para declarar papéis e ferramentas por agente | o invariante de que quem julga não escreve não é cobrado; a norma e o executável são o mesmo arquivo, sem nada que os compare | **aproveitar o vocabulário**, acrescentar o portão |
| **Procedimentos operacionais codificados em papéis** (o MetaGPT, de Hong e coautores) | papéis de uma empresa de software (gerente de produto, arquiteto, engenheiro, engenheiro de testes) que trocam **documentos estruturados**, não conversa | o humano como Accountable em gates por classe de risco; a verificação em contexto fresco como regra | **o mais próximo do Maestro** — adotar a troca por artefato |
| **Metáfora de empresa** (o ChatDev, de Qian e coautores: diretor executivo, diretor de tecnologia, programador, revisor) | um enredo fácil de explicar | o enredo vira requisito: "contratar", "board", hierarquia que não corresponde a nenhuma decisão real | **recusado** — o ciclo 076 recusou explicitamente a metáfora de empresa [CLAIM-07-020] |
| **Metodologia agêntica inteira** (o BMAD-METHOD, um time ágil com cerca de doze agentes e artefatos próprios) | um pacote completo, pronto | é concorrente integral: adotá-lo cria uma segunda fonte de verdade de processo | **descartado** pelo Maestro [CLAIM-07-016] |
| **Skills sem papéis** (o Superpowers: catorze skills compostas e um gancho que as injeta em toda sessão) | execução disciplinada por skill, com lei de ferro e skills testadas | papéis, matriz RACI, classes de risco e registro de decisão; é método de execução, não de governança | **absorver as ideias, não o método** [CLAIM-07-015] |

Dois vereditos do handbook do Maestro sobre papéis humanos completam o quadro. Os papéis do Scrum
foram adotados **em parte**: o *Product Owner* virou o Steward, e o resto (Scrum Master, time
cross-funcional) é cerimônia de papel para quem opera sozinho. E o time em forma de T foi
**reinterpretado**: o agente cobre a largura de habilidades, o humano guarda a profundidade da
decisão. Fica de fora, como rejeitado, o par "aprovo tudo / aprovo nada": o primeiro vira o funil,
o segundo descobre o erro quando ele já é irreversível.

A orientação mais citada da indústria, o texto *Building effective agents* da Anthropic, chega ao
mesmo lugar por outro caminho: comece pela solução mais simples e só acrescente agentes e
autonomia quando a mais simples não bastar. O Princípio V do Maestro diz o mesmo ("use a menor
autonomia que resolve o problema"), e o anti-padrão 4 da skill `anti-patterns` dá nome ao desvio:
**multiagente para um problema de agente único**.

O veredito do capítulo: papéis estreitos com artefato como interface (a ideia do MetaGPT),
vocabulário declarativo (a ideia do CrewAI) e skills com lei de ferro e linha de base (as ideias do
Superpowers), **mais** duas coisas que nenhum dos três traz: o humano como Accountable que não
migra, e um portão que mede a distância entre a norma e o executável.

## O padrão Maestro

O que segue é citado por versão (`maestro@19823c2`), não copiado. Em cada parte, o texto diz o que
é **regra** (escrita para ser lida), o que é **script** (que falha) e o que é **hook** (que impede).

### A norma: a tabela de papéis e a matriz RACI

A seção 4 do modelo operacional
([operating-model.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/operating-model.md))
lista onze papéis como modos de trabalho. Dois são só humanos: o **Product Steward**, que decide o
quê e o porquê e aprova specs e releases, e o **Orchestrator**, que sequencia os agentes, limpa o
contexto entre tarefas e para quando algo é caro de desfazer. Um é misto: **Architect / Tech
Lead**, humano com o `plan-architect`. Os oito restantes são agentes: Spec, Plan, UX, Dev, QA/SDET (*quality assurance* e
*Software Development Engineer in Test*, garantia de qualidade e engenheiro de testes), Review,
Security e Tech Writer, cada um com o seu gate. A tabela RACI por etapa do ciclo de vida fecha a norma com uma frase que vale copiar: o
humano é o Accountable fixo em toda linha que carrega risco, e nenhum agente decide sozinho algo
nas classes de alteração, exclusão, ação externa ou irreversível [CLAIM-07-023]. Isso é **regra**.

A regra deixa rastro. Quando o capítulo de papéis do handbook foi reescrito no ciclo 026, em 2 de
agosto, a tese dele era justamente essa: a independência do verificador é uma linha de
configuração, e o Accountable humano já tinha deixado 21 gates de promoção registrados, cada um com
nome e data; na versão citada por este livro, são 50 [CLAIM-07-019]. O Accountable não é uma
caixa no organograma: é uma linha por decisão num arquivo que só cresce.

### Os executáveis: treze perfis estreitos

Os papéis viraram arquivo em três ciclos de julho de 2026. O ciclo 003 transformou os perfis
descritivos em oito subagentes executáveis, os do fluxo principal, com uma lista de ferramentas
estreita por papel; o 004 acrescentou os quatro meta-agentes de toolkit e fechou a primeira versão
com doze de doze; e o 018, como contou a falha real, acrescentou o décimo terceiro, o de semântica
de interface [CLAIM-07-009]. O roteiro do método registra essas etapas como fases: depois da F0 (a fundação), vieram a F1
(os doze agentes), a F2 (a primeira leva de skills) e a F3 (os scripts do ritual, como a promoção
com registro do gate); a F8 tornou o método instalável, com o agente de semântica de interface, a
skill de jornada viva e o `check-roles.sh`, e a F9 pôs o ramo de interface no diagrama do processo
[CLAIM-07-022].

Os perfis do fluxo principal são o que se espera: o `spec-agent` escreve a spec (o quê e o porquê,
com critérios testáveis) e levanta ambiguidades, sem decidir arquitetura; o `plan-architect`
escreve o plano com a conferência contra a constituição e os registros de decisão, sem
implementar; o `dev-implementer` implementa uma tarefa por vez, com testes, e não revisa o próprio
trabalho; o `qa` garante caminho feliz e caminho de falha por caso de uso e produz o relatório de
qualidade; o `review` e o `security` julgam o diff, somente leitura; o `process-guardian` confere a
conformidade com o processo e devolve CONFORME ou NÃO CONFORME, só com `Read, Grep, Glob`; o
`tech-writer` atualiza a documentação viva **no mesmo pull request**. Os três que não têm
permissão de escrita são exatamente os três que julgam [CLAIM-07-007].

Os meta-agentes são a parte menos óbvia e talvez a mais útil para um tech lead: são os papéis que
**constroem e evoluem o próprio método**. O `agent-designer` mantém em sincronia o catálogo de
perfis e os executáveis, e só aceita papel novo nascido de dor real. O `skill-author` empacota um
procedimento recorrente como skill, com lei de ferro e linha de base. O `research-curator` traz
evidência externa com fonte citada e é o **único** dos treze com acesso a busca na web. O
`didactics-editor` combate o "amontoado" (o documento denso, de sigla nua) sem mudar a decisão
técnica. Alguém sempre faz esse trabalho; a questão é se com escopo e "não faz".

E o décimo terceiro, `ux-semantics`, é o único perfil com lei de ferro própria: **nenhuma tela
nasce sem um papel semântico declarado**. É por isso, e pela lista de passos, que ele é o maior dos
treze, com 36 linhas [CLAIM-07-006].

### Os portões: o que é script

Dois scripts guardam os papéis, e um terceiro, as skills.

O `check-agents.sh` confere invariantes estruturais: a contagem esperada de agentes (treze), o
campo `name` no cabeçalho de cada um e o invariante de segurança, que falha se `review`,
`security` ou `process-guardian` ganharem `Write` ou `Edit`
([check-agents.sh](https://github.com/GHDaru/maestro/blob/19823c2/scripts/check-agents.sh)).

O `check-roles.sh`, nascido da falha do 018, compara quatro pares e falha em qualquer divergência:
cada papel que o modelo operacional prescreve contra o arquivo de agente que o entrega (oito
mapeamentos); cada artefato essencial contra o seu template; o número de princípios da constituição
contra o número de linhas da tabela de conferência do template de plano; e, desde o ciclo 039, o
índice de perfis contra os agentes em disco, **nos dois sentidos**, incluindo a coluna de
ferramentas e o total declarado em prosa [CLAIM-07-003]. Este último existe porque o índice era
uma tabela escrita à mão que nada comparava com o disco, e o comentário no script diz por que isso
é perigoso: a lista bater hoje é exatamente o que a torna perigosa, porque parece saudável e a
saúde depende de memória. O roteiro registra o passo como a fase F15, "o último lugar do
repositório que dependia de memória" [CLAIM-07-022].

Do lado das skills, o `check-install.sh` falha quando a instrução que a IA lê não cita uma skill que
existe em disco (a deriva que o ciclo 021 achou), e o `check-chapters.sh` compara a data de uma
skill com a revisão do capítulo que a cita, depois que uma regra nascida numa skill passou dez ciclos
fora do livro [CLAIM-07-027]. É esse mesmo portão que, no 063, passou a **nomear** as quatro skills
que nenhum capítulo ensina, sem reprovar: cobrir uma skill é decisão editorial, não de máquina
[CLAIM-07-004].

### As skills: seis, cada uma com a sua lei

| Skill | Lei de ferro (tradução) | Nasceu de | Consumida por |
|---|---|---|---|
| `constitution-check` | nenhum plano sem as oito linhas, uma por princípio, nenhuma vazia | a tabela refeita à mão nos ciclos 003 e 004 | `plan-architect`, `process-guardian` |
| `verifiable-dod` | nenhum critério de aceite sem o comando que o prova | verificações reescritas iguais a cada ciclo | `spec-agent`, `qa`, comando `/dod` |
| `fight-the-pile-up` | nenhuma sigla nua | o retorno do Steward sobre documentos densos | `didactics-editor`, `tech-writer` |
| `anti-patterns` | nomeie o anti-padrão antes de corrigi-lo | retrospectivas dos ciclos 001–008 e 017–020 | todos; `review`, `process-guardian` |
| `diagnose-before-fix` | nenhum conserto sem investigação de causa raiz antes | lacuna real de disciplina de depuração (ciclo 011) | `dev-implementer`, `qa` |
| `living-journey` | jornada sem captura do build real é ficção; heurística sem data é ficção vencida | a lacuna do ciclo 018 | `qa`, `tech-writer`, `ux-semantics` |

A `constitution-check` ilustra o que uma skill acrescenta além da lei: ela **decide** quando um
princípio conta como violado (quando o plano só funciona quebrando-o; desconforto não é violação) e
dá duas saídas, nunca "ignorar": refazer o plano ou registrar a violação numa seção de complexidade
justificada, com o motivo e o que a torna reversível, para o gate humano decidir.

As seis carregam lei de ferro, e a coluna "nasceu de" não é decoração: é a regra de nascimento
cumprida. As três primeiras vieram do ciclo 005, todas de dor observada nos ciclos 003 e 004, como
a tabela de conferência que todo plano refazia à mão [CLAIM-07-010]. A `anti-patterns` veio do
estudo de outro repositório do mesmo autor (`maestro-02`) e cresceu por retrospectiva até 23 itens,
em cinco grupos (contexto, orquestração, qualidade, processo e verificação), cada item com o ciclo
de origem; o histórico do arquivo mostra mudanças em nove ciclos, do 008 ao 055 [CLAIM-07-014]. A lei dela é a mais curta e talvez a mais útil fora do Maestro: **nomeie antes de
corrigir**. Corrigir sem nomear conserta o sintoma uma vez; nomear ("este é o número 4") liga o
erro ao catálogo, encurta a conversa e alimenta a retrospectiva que decide se ele vira regra.

O ciclo 011, de 31 de julho, é onde as skills deixaram de **sugerir** e passaram a **comandar**. Os
vereditos do estudo do Superpowers, aprovados integralmente pelo Steward, viraram seis requisitos:
lei de ferro nas quatro skills que existiam, o protocolo de linha de base no `skill-author`, a skill
nova de diagnóstico, um checkpoint leve por tarefa na raia plena com mais de três tarefas, a regra
de escrever cada tarefa para quem tem zero contexto e um parágrafo de "skills primeiro" na instrução
do projeto [CLAIM-07-011]. Os cartões datados do catálogo do ecossistema registram cada ideia com o
seu veredito: absorver a lei de ferro, o catálogo de anti-padrões, a causa raiz antes do conserto, o
teste de skills e o *bootstrap* da instrução; descartar a adoção integral de uma metodologia
[CLAIM-07-016].

### "Skills primeiro": regra, não hook

O Superpowers garante que o agente consulte as skills com um **hook** de início de sessão, que
injeta a meta-skill em toda conversa. O Maestro escolheu outro mecanismo, e vale ser preciso sobre
qual. O "skills primeiro" é um **parágrafo** da instrução do projeto: antes de agir, verifique se uma
skill se aplica; havendo chance razoável, siga-a. O que o torna mais que um conselho é que o bloco
é **gerado do disco** pelo instalador, e não escrito à mão, e que o `check-install.sh` falha se a
instrução não apontar para o método [CLAIM-07-017]. É regra com forcing function, não hook: nada
impede um agente de ignorar o parágrafo. O hook que o Maestro tem (um guarda `PreToolUse`) protege
outra coisa, o histórico que não se reescreve. Para um time que adote o formato, a escolha é real:
o hook impede, mas é específico do harness; a instrução gerada sobrevive à troca de ferramenta, mas
só orienta.

### Ordem entre papéis e papéis de ocasião

Dois episódios do ciclo 076, já no fim de outubro de 2026, mostram o padrão em uso.

O primeiro é uma regra de **ordem**. O Steward fixou que o agente de semântica de interface declara o
papel de um objeto de tela **antes** de o construtor deixar o teste verde. No commit `103604f`, de 2
de novembro, o `ux-semantics` escreveu o papel semântico de "derrubar sessão" no `ux-design.md`
antes do verde da tarefa que o implementaria: derrubar vira um **pedido de decisão** com prazo, a
confirmação irreversível diz o que se perde (a tentativa em curso) e o que se reverte (a retomada), e
o estado da sessão só muda quando o desfecho do pedido chega, nunca no clique. A mensagem do commit
registra também que dois toques fora do escopo foram revertidos pelo agente que coordenava
[CLAIM-07-021]. O papel não só existia; ele vinha na ordem certa, e o seu "não faz" foi cobrado.

O segundo é o uso de papéis **de ocasião**. Para decidir a arquitetura e a interface do painel do
método, o 076 convocou duas bancas de três especialistas cada (jornada, catálogo e linguagem do
lado de UX; um arquiteto orientado a *Domain-Driven Design*, um pragmático e um de integração do
outro lado), todos em contexto fresco, e os arquitetos leram os votos uns dos outros e responderam
ponto a ponto. A síntese emenda o briefing do ciclo anterior, registra treze decisões de
arquitetura com voto e gatilho de revisão e, numa seção de versão 2 escrita depois de um estudo de
plataformas de controle de agentes, diz o que muda e o que entra, chegando a quinze [CLAIM-07-020]. Esses
especialistas não viraram perfis permanentes, e não deveriam: são papéis C (consultados) de uma
decisão, com escopo de uma pergunta. Nem todo papel merece um arquivo em `.claude/agents/`; merece
um arquivo o papel que se repete.

## Exemplo executável

O exemplo em [`exemplo/`](exemplo/README.md) é um portão de papéis e skills que você pode apontar
para o seu próprio repositório. Ele lê um time fictício descrito em arquivos (uma tabela de papéis,
que é a norma; seis perfis, que são os executáveis; duas skills com linha de base) e aplica dez
regras, seis de papel e quatro de skill.

As regras de papel são a anatomia deste capítulo virada em verificação: todo papel prescrito tem um
perfil (P1) e todo perfil entrega um papel prescrito (P2), que é o `check-roles.sh` nos dois
sentidos; quem julga não tem caneta (P3); o contrato tem Faz, Não faz, Consome, Produz e Entrega a
(P4); o perfil cabe num teto de 40 linhas (P5); e o papel **declara a faixa de modelo** (P6). A P6
não existe no Maestro: é a recomendação deste capítulo para a lacuna papel × modelo × custo. As
regras de skill são o nascimento e a forma: gatilho na descrição (S1), lei de ferro com as desculpas
fechadas (S2), dor de origem e linha de base com o "sem" e o "com" (S3), e consumo nos dois sentidos,
nenhuma skill órfã e nenhum papel citando skill inexistente (S4).

Para não ser um portão que nunca reclamou, o script aplica dez mutações numa cópia do time, uma por
regra, e exige que cada uma seja acusada **pela regra certa**: o papel de interface perde o agente
(a falha do 018), o revisor ganha permissão de edição, a lei de ferro vira sugestão, a skill nasce
sem linha de base, ninguém consome a skill (a família do 063). Rodando:

```text
$ python confere.py
...
== o time como está
  ✓ dez regras conformes

== mutações (cada uma deve ser acusada pela SUA regra)
  ✓ M1 o papel de interface perde o agente: P1 acusou — 'Semântica de interface' é prescrito pelo modelo e nenhum perfil o entrega
  ✓ M3 o revisor ganha caneta: P3 acusou — 'revisor' julga e tem Edit
  ...
resultado: time conforme · mutações acusadas: 10/10
```

O segundo script, `mede.py`, mede qualquer pasta de perfis: linhas, bytes, tokens estimados,
ferramentas, se escreve e se declara modelo. Apontado para os agentes do Maestro na versão citada,
ele produz os números que este capítulo usa: treze perfis, 285 linhas, três sem escrita e **zero**
com modelo declarado [CLAIM-07-006, CLAIM-07-007, CLAIM-07-008]. O que o exemplo **não** prova está no
README [CLAIM-07-025].

## Contraexemplo

A regra deste capítulo tem custo, e há situações em que ela atrapalha.

**O problema é de um agente só.** Se a tarefa cabe numa janela e não tem nada de irreversível,
dividir em papéis compra *handoffs*, artefatos intermediários e a chance de um papel esperar algo
que o anterior não produziu, e não compra nada em troca. É o anti-padrão 4. Mesmo no Maestro, nem
todo papel trabalha em todo ciclo: numa varredura dos registros dos primeiros 23 ciclos, o `qa`
aparecia citado em quinze arquivos, o `dev-implementer` e o `review` em seis, o `tech-writer` e o
`agent-designer` em três [CLAIM-07-018]. O toolkit oferece treze janelas; o trabalho usa as que a
raia pede, e isso é a regra funcionando, não desperdício.

**O papel vira cerimônia.** Importar papéis de um time grande para quem opera sozinho (um "Scrum
Master" de agentes, uma *daily* de uma pessoa) é o anti-padrão 11, o teatro de cerimônia. O teste
é o mesmo do capítulo 14: se o papel nunca muda uma decisão, ele é enfeite. A metáfora de empresa
que o 076 recusou é a versão narrativa do mesmo erro.

**A lei de ferro universal.** A skill de *brainstorming* do Superpowers exige design aprovado antes
de **qualquer** código e nomeia como anti-padrão o "isto é simples demais para precisar de design".
O Maestro recusou essa posição: o valor da spec escala com ambiguidade × raio × irreversibilidade,
e para um erro de digitação a spec é cerimônia de papel. Uma lei de ferro aplicada a tudo vira
burocracia; a lei precisa ser estreita, e a exceção, uma decisão humana registrada. O que o Maestro
absorveu da posição oposta foi só o aviso: na dúvida entre a raia leve e a plena, é plena.

**A linha que não paga.** Cada instrução de um papel custa contexto em toda invocação. A ablação
do caso 002 sugeriu que a linha "confira a raia declarada" do `process-guardian` era redundante: o
agente sem ela chegou à mesma conclusão duas vezes. A tentação é apagar a linha. A retrospectiva
do ciclo 041 (a fase F16 do roteiro, a mesma que descobriu que o próprio script de retrospectiva
reportava um gate pendente falso desde o ciclo 011 [CLAIM-07-022]) fez o oposto, e com razão: duas amostras não bastam para tirar instrução de um agente;
o achado virou **gatilho** (reavaliar com o terceiro dado), não regra [CLAIM-07-013]. Cortar papel
por ablação tem o mesmo rigor que criar papel por dor: exige evidência, não impressão.

**O protocolo que ninguém rodou.** O Maestro exige linha de base para skill original nova desde o
ciclo 011. Na versão citada, nenhuma das seis skills tem um arquivo de linha de base no
repositório, e os dois casos de avaliação existentes miram agentes, não skills [CLAIM-07-012,
CLAIM-07-013]. Há explicação honesta para parte disso: o relatório do 011 registra que a skill de
diagnóstico nasceu adaptada de uma fonte já testada em produção e que o protocolo passaria a valer
para as próximas originais [CLAIM-07-011]; a única skill nascida depois disso, a de jornada viva,
veio no ciclo 018. Mas a lição para o tech lead é direta: o protocolo custa uma rodada de subagente
por skill e por brecha, e é exatamente o tipo de passo que o time pula quando a skill "obviamente"
funciona. Se for pular, registre que pulou.

**O número que envelheceu.** O corolário C8 cita como evidência "13 agentes em 267 linhas", e o
capítulo do handbook que o ensina diz "média de vinte, o menor com dezessete". Na versão citada, são
285 linhas, média de 21,9, o menor com dezoito [CLAIM-07-006]. Nada quebrou: o `ux-semantics` ganhou
a sua lei de ferro, o `skill-author`, o protocolo de teste, e os papéis continuam estreitos. Mas é o
teorema T5 (sobrevive o que é consumido ou imutável) aplicado ao próprio método: o número escrito em prosa não é consumido por nada, então
envelhece calado. Se o tamanho dos papéis é uma propriedade que importa, ele deve ser medido por
script (como o `mede.py` deste capítulo), e não citado.

**O portão mede a forma.** O `check-roles.sh` confere que o nome do papel aparece no modelo e que
o arquivo existe; o `confere.py` deste capítulo confere seções, campos e tamanhos. Nenhum dos dois
sabe se o agente se comporta como o papel diz. Um perfil conforme pode ser ignorado; uma lei de
ferro pode ser racionalizada. É o anti-padrão 13 (o check que mede o *proxy*, não o fato), e o
[capítulo 10](../10-quality-gates-que-provam-fatos/capitulo.md) é inteiro sobre ele. O
comportamento só se prova com avaliação contra linha de base, o assunto do
[capítulo 15](../15-validando-o-maestro/capitulo.md).

## Evidência

A tese central (a distância entre a norma e o executável produz defeitos silenciosos, e só um
portão a fecha) se apoia em três falhas datadas: o papel prescrito sem agente por catorze ciclos
[CLAIM-07-001, CLAIM-07-002], a instrução que mandava consumir um artefato inexistente, com
fechamento afirmado falso [CLAIM-07-005], e as quatro skills sem capítulo [CLAIM-07-004]. O
`check-roles.sh` é observável no script e foi visto falhando antes de ser aceito [CLAIM-07-002,
CLAIM-07-003].

**Medido**: treze perfis em 285 linhas, os três sem escrita sendo os três que julgam, nenhum com
modelo declarado [CLAIM-07-006, CLAIM-07-007, CLAIM-07-008]; seis skills com lei de ferro e sem linha
de base registrada; 23 anti-padrões com a história no Git [CLAIM-07-012, CLAIM-07-014]; o exemplo,
dez regras e dez mutações [CLAIM-07-025]. **Observado** nos artefatos: o nascimento dos papéis e das
skills nos ciclos 003, 004, 005, 011 e 018 [CLAIM-07-009, CLAIM-07-010, CLAIM-07-011]; os vereditos
sobre o ecossistema [CLAIM-07-015, CLAIM-07-016]; o roteiro [CLAIM-07-022]; a ablação [CLAIM-07-013];
os gates registrados [CLAIM-07-019]; perfil e sessão [CLAIM-07-026]. O uso dos papéis em 23 ciclos
[CLAIM-07-018] é contagem do handbook, não refeita aqui.

**Hipóteses**: que declarar a faixa de modelo por papel reduz custo sem perder qualidade nos papéis
mecânicos é a H9 da agenda de pesquisa, não testada [CLAIM-07-024]; que a revisão fresca acha mais
defeito que a autorrevisão é a H2, tratada no capítulo 2; que a lei de ferro aumenta a obediência é
plausível pelo mecanismo e pelo relato do catálogo (a tentativa cega teria sumido das
retrospectivas depois da skill de diagnóstico) [CLAIM-07-016], mas não tem linha de base com e sem a
lei. O desenho para medi-la é o do caso 001: o mesmo agente, com e sem a lei, no mesmo cenário de
pressão.

## Checklist

- [ ] Cada papel de agente que a sua norma (modelo operacional, wiki, README) prescreve tem **um
      arquivo executável** que o entrega, e um script falha quando um lado existe sem o outro, nos
      dois sentidos.
- [ ] Cada perfil declara escopo, **o que não faz**, o que consome, o que produz e a quem entrega.
- [ ] Os papéis que julgam (revisão, segurança, conformidade) **não têm** ferramenta de escrita, e
      um script falha se ganharem; o `Bash` deles está anotado como risco conhecido.
- [ ] Revisor e implementador rodam em **sessões diferentes**; o revisor recebe o diff, a spec e o
      plano, não a conversa.
- [ ] Cada perfil cabe em uma tela (algo como 40 linhas), e o tamanho é **medido por script**, não
      citado em prosa.
- [ ] Cada papel declara a **faixa de modelo** em que roda, com o motivo e o gatilho de revisão.
- [ ] Cada skill tem `description` com gatilho ("Use quando…"), lei de ferro em bloco e pelo menos
      duas desculpas fechadas.
- [ ] Nenhuma skill nasce sem a dor que a originou escrita e sem uma **linha de base** (o agente
      falhando sem ela, cumprindo com ela); se pular o protocolo, registre que pulou.
- [ ] Toda skill tem pelo menos um papel que a consome, e a instrução que o agente lê primeiro
      lista as skills **geradas do disco**, não de memória.
- [ ] Antes de apagar uma instrução de um papel por parecer redundante, existe uma **ablação** com
      mais de duas amostras.
- [ ] Um papel novo só entra com uma dor nomeada (retrospectiva ou roteiro); um especialista de
      ocasião fica como papel consultado da decisão, sem arquivo permanente.

## Referências

**Maestro** (`https://github.com/GHDaru/maestro`, versão `19823c2`):

- Axiomas, teoremas e corolários (A2, A3, T2, T5, C3, C8):
  [docs/governance/axioms.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/axioms.md)
- Modelo operacional, §4 (papéis e RACI):
  [docs/governance/operating-model.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/operating-model.md)
- Glossário (agente-perfil e sessão de agente):
  [docs/governance/glossary.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/glossary.md)
- Os treze perfis: [.claude/agents/](https://github.com/GHDaru/maestro/tree/19823c2/.claude/agents)
- Catálogo de skills e regra de nascimento:
  [skills/README.md](https://github.com/GHDaru/maestro/blob/19823c2/skills/README.md); as seis
  skills em [skills/](https://github.com/GHDaru/maestro/tree/19823c2/skills)
- Portões: [scripts/check-agents.sh](https://github.com/GHDaru/maestro/blob/19823c2/scripts/check-agents.sh),
  [scripts/check-roles.sh](https://github.com/GHDaru/maestro/blob/19823c2/scripts/check-roles.sh)
- Ciclos: [specs/003](https://github.com/GHDaru/maestro/blob/19823c2/specs/003-perfis-agentes-executaveis/spec.md),
  [specs/004](https://github.com/GHDaru/maestro/blob/19823c2/specs/004-agentes-toolkit-executaveis/spec.md),
  [specs/005](https://github.com/GHDaru/maestro/blob/19823c2/specs/005-skills-v0/spec.md),
  [specs/011](https://github.com/GHDaru/maestro/blob/19823c2/specs/011-absorcoes-superpowers/spec.md),
  [specs/018](https://github.com/GHDaru/maestro/blob/19823c2/specs/018-instalacao-e-ux-jornadas/qa-report.md),
  [specs/063](https://github.com/GHDaru/maestro/blob/19823c2/specs/063-pendente-nao-e-evidencia/qa-report.md),
  [specs/076 — síntese das bancas](https://github.com/GHDaru/maestro/blob/19823c2/specs/076-padroes-de-engenharia-e-react/sintese-das-bancas.md)
- Avaliações: [evals/](https://github.com/GHDaru/maestro/tree/19823c2/evals)
- Catálogo do ecossistema, cartões 002, 008, 010, 013, 023 e 028:
  [docs/ecosystem/ideias/](https://github.com/GHDaru/maestro/tree/19823c2/docs/ecosystem/ideias)
- Índice de decisões: [docs/records/decisoes.jsonl](https://github.com/GHDaru/maestro/blob/19823c2/docs/records/decisoes.jsonl);
  roteiro: [docs/roadmap.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/roadmap.md)
- Commit posterior citado: [103604f](https://github.com/GHDaru/maestro/commit/103604f) (ciclo 076,
  §F4 do `ux-design.md`)
- Handbook do método (cópia congelada em `maestro-handbook/`): capítulos 04 (§5.4, §6), 06 (papéis e
  RACI), 13 (§5.14, Iron Laws) e apêndice B (estudo do Superpowers)

**Externas** (referências bibliográficas; não reacessadas nesta versão, escrita sem acesso à web):

- Hong, S. et al. *MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework*.
  International Conference on Learning Representations (ICLR), 2024. arXiv:2308.00352.
- Qian, C. et al. *ChatDev: Communicative Agents for Software Development*. arXiv:2307.07924.
- Anthropic. *Building effective agents*, dez. 2024.
  https://www.anthropic.com/engineering/building-effective-agents
- Vincent, J. *Superpowers* (`obra/superpowers`), licença de código aberto do Massachusetts
  Institute of Technology (MIT); estudado pelo Maestro no fork
  `GHDaru/superpowers`, commit `44c9b2d` (v6.2.0), em 31/07/2026.
- *BMAD-METHOD* (`bmad-code-org/BMAD-METHOD`), lido pelo Maestro em 30/07/2026 (cartão 010).
- CrewAI, documentação de agentes (atributos *role*, *goal*, *backstory* e *tools*).
- O formato aberto de skills `SKILL.md` (agentskills.io), adotado pelo Maestro no ciclo 005.
