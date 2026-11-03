# D — Estudos de campo do ecossistema

> *A ferramenta é o lugar onde você viu a ideia. O que atravessa a fronteira é a ideia.*

Toda semana aparece um framework novo prometendo resolver o trabalho com agentes, e alguém no
seu time vai perguntar se vocês já olharam. Este apêndice reúne os estudos de campo que o
Maestro, o método que este livro estuda, fez sobre o trabalho dos outros entre julho e outubro
de 2026: uma varredura, dois estudos com a mão no código, um panorama, um catálogo com portão e
uma pesquisa de vinte e cinco plataformas sem escrever uma linha de software. Leia-o para
copiar o procedimento, não os vereditos. Os vereditos têm data e envelhecem; o procedimento
é o que você leva para segunda-feira.

## Pergunta central

Como um time avalia o ecossistema de ferramentas para agentes sem adotar o processo de outro
por atacado, sem reavaliar a mesma coisa a cada trimestre e sem registrar como fato uma
absorção que nunca aconteceu?

## O que este apêndice entrega

Ao final, você consegue:

1. **Escolher** a profundidade certa de um estudo (varredura, estudo com a mão no código,
   panorama, pesquisa de mercado com matriz) a partir da pergunta e de um gatilho escrito.
2. **Julgar** uma fonte externa por ideia, com um vocabulário fechado de quatro vereditos e sete
   dimensões, duas das quais reprovam sozinhas.
3. **Separar** o momento da observação (um card datado, imutável) do estado corrente (uma linha
   num índice que só cresce), e explicar por que misturar os dois obriga a mentir ou a
   reescrever a história.
4. **Rodar** um portão que recusa absorção sem destino, observação sem gatilho e reescrita do
   índice, e dizer o que esse portão não enxerga.
5. **Citar** o que cada estudo deste apêndice decidiu, com data, para responder "isso já foi
   avaliado?" com um link, e não com memória.

## Como ler os estudos

Cada estudo tem uma data, e a data é parte do conteúdo. O que se observou em 31 de julho de
2026 sobre o Superpowers, numa versão e num commit, continua verdadeiro para sempre; o veredito
de hoje sobre a mesma ideia pode ser outro. O Maestro aprendeu isso da maneira mais cara, e por
isso este apêndice começa pela falha.

Os estudos usam um vocabulário fechado de quatro vereditos, fixado no catálogo do ciclo 047
([README do catálogo](https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/README.md)):

| Veredito | Significa | O que exige |
|---|---|---|
| `adotar` | a ferramenta entra como dependência do método | destino que é arquivo, com uma prova textual dentro |
| `absorver` | a **ideia** entra, reimplementada num artefato seu | idem |
| `observar` | não agora; pode mudar | gatilho de reavaliação escrito |
| `descartar` | não entra: conflito de princípio, licença ou função já servida | o card diz qual |

Os estudos mais antigos (julho e começo de agosto) usavam rótulos parecidos com outros nomes:
"absorver ideia", "validação mútua", "candidato a estudo com gatilho", "fora do problema".
Mantive os rótulos de cada época quando cito o estudo, porque são o registro do momento.

## A falha que organizou tudo: a absorção que só existia no papel

Em 30 de julho de 2026, o ciclo 007 do Maestro avaliou sete ferramentas do ecossistema de
*Spec-Driven Development* (SDD, desenvolvimento guiado por especificação) e consolidou a decisão
num *Architecture Decision Record* (ADR, registro de decisão de arquitetura), o ADR 0008
[CLAIM-94-001]. Sob o cabeçalho "absorver ideias com destino concreto", o ADR listava três
ideias: a sintaxe de requisitos do Kiro, o *worktree* do Git isolado por tarefa, vindo do
Superpowers, e os padrões por camada, vindos do Agent OS. Para as duas últimas, o destino vinha
com uma condição: o *worktree* iria para `scripts/` ou `skills/` "quando houver dor real de
paralelismo"; os padrões, para `docs/standards/` "apenas quando o Maestro reger codebase de
produto (gatilho, não agora — YAGNI)", onde YAGNI é *You Aren't Gonna Need It*, "você não vai
precisar disso"
([ADR 0008](https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0008-avaliacao-ecossistema-sdd.md)).

Ninguém mentiu. Três linhas abaixo, o mesmo ADR listava o Agent OS em "observar com gatilho
explícito". Um dia depois, o estudo do Superpowers escreveu o *worktree* como "observar" com a
nota "gatilho F3 inalterado" (F3 é uma fase do roteiro do método), em deferência ao ADR. As duas leituras conviviam, e nenhum
arquivo dizia qual era o estado. A frase "absorver quando doer" e a frase "observar até doer"
eram a mesma decisão escrita em duas colunas diferentes.

O defeito só apareceu dez dias depois, no ciclo 047, quando alguém tentou traduzir a prosa
para uma linha que uma máquina pudesse conferir. O portão novo, o `check-ecosystem.sh`, foi
escrito antes do conteúdo; na primeira execução, a absorção do *worktree* apontava para a pasta
`scripts/`, que existia por outros motivos, e a dos padrões apontava para uma pasta que não
existia. O cabeçalho do script registra o tamanho do estrago: as duas ideias ficaram 39 ciclos
registradas como absorvidas sem nunca terem chegado ao disco [CLAIM-94-002]
([check-ecosystem.sh](https://github.com/GHDaru/maestro/blob/19823c2/scripts/check-ecosystem.sh)).
Contando as que vieram de outra pesquisa (padrões de fatiamento, fatia vertical e contrato por
fatia), eram cinco ideias como "absorver" com destino condicional, e nenhuma tinha arquivo.
As cinco voltaram para `observar`, cada uma com gatilho, em linhas novas datadas de 10 de
agosto [CLAIM-94-003]. O achado foi registrado no índice de decisões com o id
`achado-047-cinco-absorcoes-sem-destino`.

A segunda metade da história é mais incômoda. A revisão independente do próprio ciclo 047, em
contexto fresco, reprovou a entrega com cinco bloqueantes, e o mais grave era o mesmo defeito
que o ciclo denunciava: seis vereditos tinham sido trocados e retrodatados. O índice afirmava,
numa linha datada de 30 de julho e marcada como ciclo 007, um veredito que o ciclo 007 nunca
deu [CLAIM-94-004]
([qa-report do 047](https://github.com/GHDaru/maestro/blob/19823c2/specs/047-catalogo-do-ecossistema/qa-report.md)).
Os vereditos históricos foram restaurados, as reclassificações viraram linhas novas com data e
ciclo verdadeiros, e a migração recuperou dez cards e cinco fontes que tinha perdido no
caminho [CLAIM-94-004].

A lição tem duas partes, e o resto do apêndice se organiza em torno delas. Primeira: uma
decisão sobre trabalho alheio só é um fato quando aponta para um arquivo que contém a coisa
decidida. Segunda: a tentação de "arrumar" o registro antigo é forte o bastante para pegar quem
está escrevendo a regra contra ela. Por isso o estado corrente mora num lugar que só cresce.

## O funil: do exploratório ao portão

Os estudos do Maestro não nasceram com um procedimento; o procedimento é o que sobrou deles.
O panorama do ciclo 012 deu nome ao funil: varredura exploratória, gatilho, estudo com a mão no
código, absorção aprovada num portão humano
([spec 012](https://github.com/GHDaru/maestro/blob/19823c2/specs/012-panorama-templates/spec.md)).
Cada etapa custa mais que a anterior, e nada passa de uma para outra sem motivo escrito.

- **Varredura** (ciclo 007): fontes primárias, sem instalar nada. Responde "o que existe e o
  que, à primeira vista, conflita com nossos princípios?".
- **Gatilho**: uma condição observável que, quando acontecer, justifica gastar mais. "Quando
  doer" não é gatilho; "um ciclo com mais de 20 tarefas paralelas e a ordenação manual doer" é
  [CLAIM-94-005].
- **Estudo com a mão no código** (ciclos 010 e o do `maestro-02`): o repositório real, numa
  versão fixada, lido arquivo por arquivo. Responde "o que exatamente esta ideia faz, e o que
  ela pressupõe que nós não temos?".
- **Absorção por portão**: a ideia vira um artefato seu (skill, script, linha de template), num
  ciclo próprio, depois de aprovada por um humano. O estudo só **propõe**.

Por baixo do funil há uma escolha de unidade. O ciclo 047 a formulou assim: o Maestro quase
nunca adota uma ferramenta; ele absorve ideias e descarta o resto. "Superpowers: absorver e
observar" não é acionável. "Causa raiz antes do conserto: absorver, destino
`skills/diagnose-before-fix/SKILL.md`" é, e é falsificável
([spec 047](https://github.com/GHDaru/maestro/blob/19823c2/specs/047-catalogo-do-ecossistema/spec.md)).
O capítulo 12 trata a mesma escolha do ponto de vista do risco de ligar ferramentas ao agente
([Ferramentas, MCP e o ecossistema](../../12-ferramentas-mcp-e-o-ecossistema/capitulo.md)); aqui
ela aparece do ponto de vista de quem decide o que atravessa a fronteira.

## Estudo 1 — A varredura do ecossistema SDD (ciclo 007, 30/07/2026)

**A pergunta.** O Maestro tinha adotado o Spec Kit e descartado o OpenSpec (ADR 0005), mas o
resto do ecossistema nunca tinha passado pelo crivo. A pergunta do responsável pelo método foi
direta: "foi avaliado?". A spec do ciclo explica por que isso importava: o método dizia trazer
conceitos adaptados de todas as fontes, e sem a avaliação a frase não tinha lastro
([spec 007](https://github.com/GHDaru/maestro/blob/19823c2/specs/007-avaliacao-ecossistema-sdd/spec.md)).
O objetivo declarado era também defensivo: blindar contra o re-litígio. Quando alguém
perguntasse "já avaliamos X? onde?", a resposta deveria ser um link.

**O método.** Uma ficha de pesquisa feita pelo papel de curador de pesquisa, com fonte primária
para cada ferramenta e um critério de veredito escrito antes: conflito com princípio descarta;
ideia boa sem a ferramenta é absorvida, com artefato de destino; ferramenta complementar e
madura é adotada em spec própria; imatura ou incerta fica em observação, com gatilho
([ficha de pesquisa](https://github.com/GHDaru/maestro/blob/19823c2/docs/research/avaliacao-ecossistema-sdd.md)).
Nada foi instalado. A profundidade foi uma decisão de YAGNI: instalar só se o veredito fosse "adotar".

**O que saiu.** Sete ferramentas fichadas e um quadro de vereditos:

| Ferramenta | Veredito de 30/07/2026 | O que ficou |
|---|---|---|
| Superpowers | absorver ideias e observar | *worktree* por tarefa (condicional), rigor mandatório nas skills |
| BMAD-METHOD | descartar a adoção | nada essencial não coberto |
| Kiro | absorver a sintaxe de requisitos, descartar a ferramenta | a sintaxe na skill de *Definition of Done* e no template de spec |
| Taskmaster | observar | gatilho: mais de 20 tarefas paralelas ou vários projetos |
| Agent OS | absorver em parte e observar | padrões por camada (condicional) |
| GSD | observar | a raia leve já cobre |
| Tessl | observar | gatilho: maturidade e caso público de produção |

Três vereditos merecem o detalhe, porque o argumento vale para outros times.

O **BMAD-METHOD** (*Breakthrough Method for Agile AI-Driven Development*) organiza agentes como
um time ágil, com gerente de produto, arquiteto, desenvolvedor e garantia de qualidade (*quality assurance*, QA), e artefatos ágeis passados
de mão em mão por arquivo. O veredito foi descartar porque é um concorrente integral: adotá-lo
substituiria o modelo do Maestro em vez de complementá-lo, e traria a cerimônia
*scrum-like* que o método já tinha recusado. O glossário do Maestro guarda a frase que resume a
decisão: uma metodologia concorrente inteira criaria uma segunda fonte de verdade
([glossário](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/glossary.md)). Um
detalhe mostra por que números de terceiros não decidem nada: a ficha descreve o BMAD com
"12+ agentes"; o glossário, escrito depois, com "~22" [CLAIM-94-006]. A própria ficha declarou
a incerteza: contagens de estrelas e de custo vinham de análises de terceiros, ordem de grandeza
confiável, valor exato não auditado.

O **Kiro** é uma IDE (*Integrated Development Environment*, ambiente de desenvolvimento)
proprietária da Amazon Web Services (AWS) que gera requisitos, desenho e tarefas a partir de um prompt. A ferramenta
foi descartada por aprisionamento: presa a uma IDE e a um ecossistema de nuvem. A melhor ideia
dela atravessou sozinha: a *Easy Approach to Requirements Syntax* (EARS), critério de aceite no
padrão "QUANDO <condição> O SISTEMA DEVE <comportamento>", que vira teste quase um para um. É
o exemplo mais limpo do apêndice de ferramenta recusada com ideia absorvida, e o capítulo 4
mostra a sintaxe em uso ([A spec como partitura](../../04-a-spec-como-partitura/capitulo.md)).

O **Superpowers**, na varredura, ficou em "absorver ideias e observar", um veredito que o
ciclo 047 depois chamaria de não acionável. A ficha previu a própria limitação: o ADR 0008
registra, nas consequências negativas, que o fichamento foi feito sem instalar nada e que, se
um gatilho disparasse, a reavaliação deveria incluir estudo com a mão no código. O gatilho
disparou no dia seguinte (Estudo 3).

**O que este estudo ensina.** A varredura é barata e decide bem o que é descartável por
princípio. Ela decide mal o que é sutil, porque fontes secundárias descrevem a promessa, não o
mecanismo. E produz a falha da seção anterior quando mistura "absorver" com "quando doer":
o veredito precisa ser uma coisa ou a outra.

## Estudo 2 — O `maestro-02`: o instrumento ao lado do método (31/07/2026)

**O que é.** Apesar do nome, o `maestro-02` não é o método deste livro. É um *fork* de um
projeto homônimo e independente, `sharpdeveye/maestro`, estudado no commit `00f9115`, versão
2.0.0, licença MIT [CLAIM-94-007]. Ataca o mesmo problema pelo outro lado: o Maestro constrói
governança (papéis, portões, decisão humana); o `maestro-02` constrói instrumento (skills,
memória, telemetria) instalável em qualquer agente. Tem 141 arquivos em três entregáveis: um
núcleo de skills com 24 comandos, um servidor de *Model Context Protocol* (MCP, o protocolo que
padroniza a ligação de ferramentas a agentes) com 25 prompts, 10 ferramentas e 8 recursos, e
uma extensão de editor; e distribui as mesmas skills para 10 provedores a partir de uma fonte
única [CLAIM-94-007]
([apêndice A do handbook](https://github.com/GHDaru/maestro/blob/19823c2/docs/handbook/apendice-a-maestro-02.md)).

**As seis ideias.** O estudo pôs seis ideias na mesa e julgou cada uma contra o que o Maestro
já tinha.

1. **Memória persistente como camada explícita.** Um diretório-padrão, `.maestro/`, com o
   contexto do projeto, um log de decisões *append-only* em *JSON Lines* (JSONL, um objeto
   *JavaScript Object Notation*, JSON, por linha), um log de auditoria e resumos de sessão. O Maestro registrava decisões em
   prosa (specs, ADRs, retrospectivas); a ideia forte é a decisão como dado estruturado, que
   um agente consulta ("as últimas cinco decisões") em vez de um humano reler. Veredito:
   absorver, como registro consultável por agente. Virou o `docs/records/decisoes.jsonl` e o
   `scripts/record-decision.sh`, que o resto deste livro cita o tempo todo.
2. **Trilha de auditoria com custo por invocação.** Cada comando grava comando, duração em
   milissegundos, custo estimado em dólares e código de saída, numa linha JSONL. É telemetria
   na versão mais barata possível: um arquivo que só cresce, sem painel. Veredito: observar,
   como primeiro degrau da telemetria quando alguém precisar responder "quanto custou este
   ciclo" com número. O argumento de fundo, medir antes de construir painel, está no capítulo 13
   ([Observabilidade e economia](../../13-observabilidade-e-economia/capitulo.md)).
3. **A retrospectiva executável.** O comando `/reflect` lê o histórico de invocações e produz
   um placar: quais skills funcionam, quais falham, taxa de conclusão, custo total. Era a
   retrospectiva do Maestro transformada em consulta. Veredito: absorver. Virou
   `scripts/retro.sh`, que pré-computa o material da retrospectiva a partir dos artefatos do
   ciclo.
4. **Fases com validação entre elas.** O *wave-engine* roda cada comando de construção em
   ondas tipadas (mapear, validar, gerar, testar), com um resultado de validação (passou,
   problemas, sugestões) entre cada fase. É o ciclo spec, plano, implementação e verificação em
   miniatura, dentro de um único comando. O valor para o Maestro não foi a ferramenta, foi a
   confirmação independente: fases com portão convergem em qualquer granularidade. Veredito:
   absorver o conceito, como vocabulário para portões em nível de tarefa.
5. **Economia de contexto medida.** O *context-slicer* injeta só as seções relevantes ao comando
   ativo e reporta a economia: a estimativa de tokens da fatia contra a do contexto inteiro.
   O Maestro afirmava o princípio ("cada agente estreito"); o `maestro-02` media. Veredito:
   absorver o conceito de medir. O capítulo 5 desenvolve a ideia
   ([Engenharia de contexto](../../05-engenharia-de-contexto/capitulo.md)).
6. **Anti-padrões como catálogo de primeira classe.** O núcleo de skills lista o que não fazer:
   não despejar o codebase no contexto, não usar vários agentes para problema de um agente, não
   repetir o mesmo prompt esperando resultado diferente, não entregar sem avaliação. O Maestro
   registrava o que não adotava, mas não tinha um catálogo de erros de execução. Veredito:
   absorver. Virou a skill `anti-patterns`, alimentada pelas retrospectivas, hoje com vinte e
   três entradas [CLAIM-94-027], como o capítulo 14 discute
   ([A organização que aprende](../../14-a-organizacao-que-aprende/capitulo.md)).

**Onde não serve.** O `maestro-02` não tem papéis, nem portões humanos, nem classes de risco; o
operador é um desenvolvedor individual. Não é guiado por spec: os comandos melhoram fluxos que
já existem. Adotá-lo por atacado repetiria o erro já recusado no BMAD: uma segunda fonte de
verdade de processo. O placar final foi cinco absorções, uma observação e um descarte (a adoção
integral) [CLAIM-94-008], e o responsável pelo método aprovou as absorções no mesmo dia;
elas foram materializadas na spec 008.

**O que este estudo ensina.** Um projeto que resolve um problema vizinho, pelo lado oposto, é
uma fonte de ideias melhor que um concorrente direto, porque quase nada nele disputa o seu
modelo. E "observar" bem escrito tem um gatilho que um dia vai acontecer: a trilha de custo
continua em observação no catálogo, com o gatilho "alguém precisar responder quanto custou este
ciclo com número" [CLAIM-94-009].

## Estudo 3 — O Superpowers com a mão no código (ciclo 010, 31/07/2026)

**Por que um segundo olhar.** O ADR 0008 tinha avaliado o Superpowers por fontes secundárias e
prometido reavaliação com a mão no código se um gatilho disparasse. O gatilho foi concreto: o
responsável pelo método trouxe um *fork* do repositório. O ciclo 010 cumpriu a promessa
([spec 010](https://github.com/GHDaru/maestro/blob/19823c2/specs/010-estudo-superpowers/spec.md)).
O estudo leu as 14 skills, seis delas na íntegra, os *hooks* e o pacote, no commit `44c9b2d`,
versão 6.2.0, licença MIT [CLAIM-94-010]. Não rodou o plugin; isso estava fora de escopo.

**O que é.** Skills compostas, um *bootstrap* por *hook* de início de sessão que injeta a
meta-skill em toda conversa, e distribuição para vários *runtimes*. Sem servidor e sem
interface: a força do projeto é linguística, não de infraestrutura. O fluxo canônico vai de um
*brainstorming* que exige desenho aprovado antes de qualquer código, passa por *worktree*
isolado, plano em tarefas de dois a cinco minutos, subagente fresco por tarefa com revisão,
*Test-Driven Development* (TDD, desenvolvimento guiado por testes), verificação antes de
concluir e fechamento do ramo.

**As ideias e os vereditos propostos.** O estudo avaliou oito ideias e duas posições de fundo:

- **A Iron Law.** Regras críticas formatadas como bloco inegociável, com a fórmula "violar a
  letra das regras é violar o espírito das regras", e a meta-skill exigindo invocar a skill
  se houver qualquer chance de ela se aplicar. As skills do Maestro descreviam; não comandavam.
  Absorver: as leis das skills reescritas nesse formato. É a origem da seção "Iron Law" que
  toda skill do Maestro tem hoje.
- **TDD para skills.** A ideia mais original do repositório: se você não viu um agente falhar
  sem a skill, não sabe se a skill ensina a coisa certa. Roda-se um subagente sem a skill
  (vermelho), escreve-se a skill, roda-se de novo (verde), fecham-se as brechas. Absorver, como
  protocolo do agente que escreve skills. O capítulo 7 conta essa absorção
  ([Papéis e skills](../../07-papeis-e-skills/capitulo.md)).
- **Causa raiz antes do conserto.** Fase de investigação obrigatória antes de qualquer correção.
  Era uma lacuna real: o Maestro exigia teste que reproduz o bug, mas nenhuma disciplina de
  diagnóstico. Absorver, como a skill `diagnose-before-fix`.
- **Revisão por tarefa**, além da revisão por ciclo. Absorver em parte: checkpoint leve por
  tarefa na raia plena com mais de três tarefas.
- **"Assuma zero contexto"** no plano: cada tarefa autossuficiente. Absorver, numa linha do
  template de tarefas.
- **Execução contínua**, sem perguntar "continuo?". Já era a prática; validação mútua. A
  atenção humana se gasta em portões, não em progresso.
- ***Worktree* por tarefa.** Mantido em observação, com o gatilho do ADR 0008.
- ***Bootstrap* por *hook* de sessão.** O equivalente no Maestro era o arquivo de instruções do
  repositório, que carrega sozinho mas não mandava consultar as skills. Absorver: o parágrafo
  "skills primeiro" no arquivo de instruções.

**A tensão registrada.** A skill de *brainstorming* do Superpowers impõe desenho aprovado para
tudo, e nomeia como anti-padrão o pensamento "isto é simples demais para precisar de desenho".
O Maestro decidira o contrário no ADR 0005: a raia leve existe porque o valor da spec cresce
com ambiguidade, raio de impacto e irreversibilidade, e para um erro de digitação a spec é
cerimônia de papel. O estudo manteve as raias, com o motivo escrito: o Superpowers foi feito
para um desenvolvedor sozinho com um agente, sem o conceito de risco proporcional. Absorveu só o
aviso, que o Maestro já tinha: na dúvida entre leve e plena, é plena. O capítulo 4 retoma a
discussão.

**A decisão.** Adoção integral descartada, de novo, pelo mesmo motivo do BMAD. O registro do
portão humano, `gate-010-vereditos`, diz "5 absorções + 2 descartes mantidos"; a tabela do
estudo mostra cinco absorções integrais, uma parcial (a revisão por tarefa), uma validação, uma
observação e os dois descartes (a adoção integral e o portão universal) [CLAIM-94-011]. A
diferença é de contagem, não de conteúdo, e é exatamente o tipo de divergência que só aparece
quando alguém confere o registro contra a tabela. As absorções viraram a spec 011.

**O que este estudo ensina.** O estudo com a mão no código acha o mecanismo que a varredura não
vê. A varredura tinha resumido o Superpowers como "rigor mandatório"; o código mostrou como o
rigor é construído (a fórmula da Iron Law, o teste da skill contra um subagente sem ela, o
*hook* que injeta a regra). Ideia que se copia é mecanismo, não adjetivo.

## Estudo 4 — O panorama: triagem sem estudo (ciclo 012, 01/08/2026)

**A pergunta.** Depois dos dois estudos profundos, o pedido foi abrir o leque: que outros
templates e frameworks existem? O ciclo 012 fez uma varredura exploratória do resto do
ecossistema com uma regra explícita: não repetir veredito já dado, remeter à ficha do 007 e aos
estudos anteriores
([spec 012](https://github.com/GHDaru/maestro/blob/19823c2/specs/012-panorama-templates/spec.md)).
Nove itens entraram na triagem [CLAIM-94-012], cada um classificado como candidato a estudo com
gatilho, observar ou fora do problema
([apêndice C do handbook](https://github.com/GHDaru/maestro/blob/19823c2/docs/handbook/apendice-c-panorama-templates.md)).

**Frameworks SDD completos.** O `claude-code-spec-workflow` (Pimzino) tem duas trilhas, uma de
funcionalidade (requisitos, desenho, tarefas, implementação) e uma de correção (relato,
análise, conserto, verificação). Ensinou pouco de novo e confirmou muito: a trilha dupla é a
validação externa das raias do Maestro, e a análise antes do conserto ecoa a skill de causa
raiz. Observar. O CCPM (*Claude Code Project Manager*) liga spec, *issues* do GitHub e código,
com execução paralela; é a rastreabilidade spec, *issue*, código feita numa ferramenta de
projeto real. Candidato a estudo com gatilho: quando o método reger um projeto com mais de um
desenvolvedor e *backlog* em *issues*. O `Claude-Code-Workflow` (catlog22), com dezenas de
agentes e orquestração de várias interfaces de linha de comando, ficou fora do problema:
orquestrar várias *Command-Line Interfaces* (CLIs) não era dor, e a complexidade não tinha
contrapartida. No catálogo de 10 de agosto, ele ganhou card próprio (ideia 032) com o
veredito `descartar`: não traz objeto novo e, sem licença declarada, nada dele poderia ser
copiado de qualquer forma
([ideia 032](https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/ideias/032-workflow-de-comandos-generico.md)).
O card registra por que mereceu existir: tinha ficado como rodapé dentro de outro card, "o que
é exatamente a forma de perda que este catálogo existe para impedir".

**Engenharia de contexto.** O PRP (*Product Requirement Prompt*, de Wirasm) parte de uma tese
que todo tech lead reconhece: os times sobre-especificam o quê e sub-especificam o contexto.
O PRP é o documento de requisitos mais a inteligência curada do codebase (arquivos-chave,
convenções, armadilhas) mais o roteiro do agente. A spec do Maestro dizia o quê e o porquê; o
PRP acrescenta empacotar o contexto do código junto. Candidato a estudo com gatilho: o primeiro
ciclo em que o Maestro reger código de produto, onde o contexto de codebase pesa. O padrão
*Memory Bank* do Cline (arquivos markdown estruturados que o agente relê a cada sessão, com um
"contexto ativo" curto) e o `context-forge` (gerador de esqueleto de documentação de contexto)
ficaram em observação: o registro de decisões, a retrospectiva executável e o script que abre
ciclo já cobriam a função; reavaliar se sessões de vários dias começarem a doer.

**Orquestração pesada.** O `claude-flow`, com enxames de dezenas de agentes, ficou fora por ora:
o princípio do Maestro é usar a menor autonomia que resolve, e enxame é a antítese de um humano
regendo com portões. O Google *Agent Development Kit* (ADK) e a plataforma gerenciada de
agentes do Google (memória de longo prazo, delegação entre agentes, fluxos determinísticos para
conformidade) ficaram em observação, com gatilho de ida a uma nuvem gerenciada. A leitura do
panorama é útil: a direção corporativa (memória gerenciada mais orquestração determinística
nos fluxos críticos) valida os portões mecânicos do método, mas é infraestrutura, não método.

**Coleções e *marketplaces*.** Listas curadas de skills e comandos e *marketplaces*
comunitários foram tratados como fonte de garimpo, não como framework: consultados pelo agente
curador de pesquisa quando surgir uma dor específica, nunca importados em bloco.

**O que este estudo ensina.** O panorama convergiu para as apostas que o método já tinha feito,
e isso é informação, não perda de tempo. As duas ideias genuinamente novas (PRP e CCPM) saíram
com o mesmo gatilho de fundo: o Maestro sair do próprio repositório e reger código de produto.
A triagem com gatilho troca a ansiedade de estar perdendo alguma coisa por um evento que você
reconhece quando acontece.

## Estudo 5 — O catálogo: a ideia como unidade, o momento separado do estado (ciclo 047, 10/08/2026)

**A pergunta.** "Temos em algum lugar todos os repositórios que avaliamos e as decisões que
tomamos em relação a cada um?" A resposta honesta era "em parte, e espalhado": o julgamento de
terceiros vivia num ADR, numa ficha de pesquisa, em três apêndices do handbook e numa pesquisa
de outro ciclo, todos julgando por ferramenta e nenhum dizendo qual era o veredito de hoje
([spec 047](https://github.com/GHDaru/maestro/blob/19823c2/specs/047-catalogo-do-ecossistema/spec.md)).

**As três peças.** O catálogo separou três coisas que mudam em ritmos diferentes:

- **`fontes.md`**: uma linha por fonte, com endereço, o que é, licença e data da observação.
  Muda pouco. A licença decide se a ideia pode ser copiada ou só citada; fontes proprietárias,
  comerciais, sem licença declarada ou com licença não comercial levam a marca "citável, não
  copiável" na própria linha
  ([fontes.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/fontes.md)). Sem
  licença, o padrão é todos os direitos reservados. O caso que motivou a regra veio do ciclo
  036: o catálogo mais útil encontrado, 70 skills de gestão de produto, era *Creative Commons*
  Atribuição-NãoComercial-CompartilhaIgual (CC BY-NC-SA), incompatível com a distribuição MIT
  do método [CLAIM-94-013].
- **`ideias/`**: um card por ideia, datado e imutável, com o que se viu, o veredito daquele
  momento, o destino e as sete dimensões. Nunca muda.
- **`estado.jsonl`**: o veredito corrente, uma linha por mudança, só acrescentando. O estado de
  uma ideia é a última linha com o seu id. Muda sempre que o veredito muda.

O card da biblioteca de produto mostra a separação funcionando. O card, de 6 de agosto, diz
"observar e citar". O veredito corrente, numa linha de 10 de agosto, é `descartar`. O card não
foi reescrito; ganhou só um aviso de que o estado corrente é outro. Mudar de ideia é legítimo;
apagar o registro de que se pensava diferente não é.

**As sete dimensões.** Todo card avalia as mesmas sete, na mesma ordem: conflito com princípio,
licença e redistribuição, função já servida, custo de contexto, reversibilidade, maturidade e
evidência, dor real hoje. Duas reprovam sozinhas, o conflito insanável com um princípio e a
licença incompatível, e não existe nota agregada, por decisão: uma média esconde qual dimensão
decidiu, e em quase todo card uma decidiu sozinha [CLAIM-94-014]. A dimensão de maturidade pede
o que nós observamos, numa versão, e não estrelas de terceiros.

**O template.** Para avaliar algo novo, o método instala um template de card, o
`evaluation-template.md`, escrito em inglês porque viaja para outros repositórios
([template](https://github.com/GHDaru/maestro/blob/19823c2/.specify/templates/evaluation-template.md)).
Os comentários dele resumem a disciplina: se você não consegue dizer a ideia sem nomear a
ferramenta, ainda não achou a ideia; o card é imutável; observar sem gatilho é esquecer com
cerimônia; quando nenhuma condição futura poderia mudar a decisão, o veredito honesto é
descartar.

**O portão.** O `check-ecosystem.sh` não mede se um veredito é sábio; isso é julgamento humano.
Mede que todo julgamento está ancorado: fonte com licença, card datado, estado corrente e, para
o que se declara adotado ou absorvido, um destino que existe. Duas regras nasceram de tentativas
de burlá-lo. O destino tem de ser um arquivo, não uma pasta, porque `scripts/` existia por
outros motivos e fazia a promessa parecer cumprida. E o destino precisa de uma prova: um texto
literal que tem de estar dentro do arquivo, porque sem isso apontar para um `README.md`
satisfaria qualquer absorção. O portão foi visto acusar por mutação: 12 mutações na primeira
bateria, todas acusadas, e uma segunda bateria depois da revisão, com as mutações que a própria
revisão usou para reprová-lo [CLAIM-94-015]. A correção foi sempre no conteúdo; o portão não
ganhou exceção.

**O estado hoje.** Na versão do Maestro que este livro cita, o catálogo tem 24 fontes, 41 cards
e 52 linhas de estado. A última linha de cada id dá 16 ideias em observação, 14 absorvidas, 10
descartadas e uma adotada, o Spec Kit, a única ferramenta de terceiro que virou dependência do
método [CLAIM-94-016]. As 14 absorções apontam, cada uma, para o arquivo que as contém: a
sintaxe EARS na skill de *Definition of Done*, a causa raiz na skill de diagnóstico, a
retrospectiva no `retro.sh`, o "skills primeiro" no arquivo de instruções do repositório.

O achado do ciclo 047 ficou aberto no índice de decisões por sete ciclos e foi fechado pela
retrospectiva do ciclo 055, com uma regra nova: achado que vira gatilho fecha no ato, porque não
existe evento de fechamento possível para "esperar a dor" [CLAIM-94-017].

**O que este estudo ensina.** O catálogo é o estudo que estuda os outros estudos. Sem ele, os
quatro anteriores eram quatro documentos que não se conheciam; com ele, cada ideia tem um
endereço, um histórico e um estado que uma máquina confere. O capítulo 12 mostra o mesmo
catálogo como peça de governança de ferramentas
([Ferramentas, MCP e o ecossistema](../../12-ferramentas-mcp-e-o-ecossistema/capitulo.md)).

## Estudo 6 — Pesquisa sem software: a área administrativa (ciclo 073, 24 a 27/10/2026)

**A pergunta.** Em outubro de 2026, o Maestro precisava de uma área administrativa: cadastrar
agentes e papéis, subir e derrubar sessões, ver estado e consumo, deixar as sessões
conversarem. A tentação era construir. O ciclo 073 fez o contrário: quatro rodadas, nenhuma
linha de software
([spec 073](https://github.com/GHDaru/maestro/blob/19823c2/specs/073-area-administrativa/spec.md)).
A rodada 1 pesquisou plataformas (gateways de *Large Language Model*, LLM, observabilidade de
agentes, orquestração, controle de processos); a 2 confrontou o resultado com o Maestro e
decidiu o que entra; a 3 desenhou telas sobre contextos delimitados de *Domain-Driven Design*
(DDD) citando a plataforma de origem; a 4 pôs três críticos em contexto fresco para dar nota de
0 a 10 a cada peça, com a barra em 9 para todos.

**A matriz.** Uma tabela fixa de 26 funcionalidades, decidida antes da pesquisa para fixar o
vocabulário, cruzada com 25 plataformas: 650 células, cada uma com fonte verificável; 629 com
veredito explícito e 21 em branco, convertidas para "sem fonte" [CLAIM-94-018]
([qa-report do 073](https://github.com/GHDaru/maestro/blob/19823c2/specs/073-area-administrativa/qa-report.md)).
A revisão em contexto fresco conferiu uma amostra de células contra as fichas e achou um
bloqueante: as tabelas de leitura subnotificavam o "sim" em quatro (170 em vez de 174). Foi
corrigido e reconferido por script [CLAIM-94-019].

**As regras do confronto.** A rodada 2 decidiu cada funcionalidade como `ENTRA`, `NÃO PRECISA`
ou `DEPOIS`, com três regras escritas
([confronto](https://github.com/GHDaru/maestro/blob/19823c2/specs/073-area-administrativa/confronto/confronto-decisao.md)).
Primeira: `ENTRA` exige fonte, uma plataforma citada ou um requisito do método citado; nada
entra por memória. Segunda: uma célula sem fonte não é base, porque significa "não
encontrado", nunca "não existe". O documento proíbe a expressão "lacuna de mercado" e escreve
"não encontrado na documentação lida". Terceira: YAGNI. O que o método já cobre não se
reconstrói, e `DEPOIS` sem gatilho escrito é `NÃO PRECISA` disfarçado. É o mesmo princípio do
`observar` com gatilho do catálogo, chegando por outro caminho.

**A decisão e o que mudou nela.** A rodada 2 fechou com 26 linhas: 13 `ENTRA`, 8 `NÃO PRECISA`,
5 `DEPOIS`, contados por script [CLAIM-94-020]. Os juízes da rodada 4 não aceitaram de primeira.
Um deles mostrou cinco funcionalidades de intercomunicação que faltavam (recibo de entrega,
reentrega, fila de mensagens mortas, cópia para vários, estabilidade de referência); auditoria
e custo passaram de `NÃO PRECISA` a `ENTRA`; o mecanismo de corte por orçamento virou `DEPOIS`
com gatilho. O confronto terminou com 32 funcionalidades: 16 `ENTRA`, 5 `NÃO PRECISA`, 11
`DEPOIS`. O portão final, decidido por delegação em 27 de outubro, registrou quatro leituras
dos três juízes com 47 das 48 células em nota 9 ou mais, a célula restante corrigida, e 11
telas de *wireframe* com zero achados num verificador de seis regras [CLAIM-94-021]
([registro de decisões](https://github.com/GHDaru/maestro/blob/19823c2/docs/records/decisoes.jsonl),
id `gate-073-delegado`; o desenho da rodada está no id `decisao-073-gauntlet-area-administrativa`).

**O que este estudo ensina.** O estudo de campo não serve só para decidir se adota uma
ferramenta; serve para decidir o que construir. A matriz com fonte por célula transforma "o
mercado tem isso" numa afirmação conferível, e a disciplina de não chamar ausência de evidência
de lacuna evita o erro mais caro de uma pesquisa de mercado: construir a coisa que existe e
você não achou. Os juízes em contexto fresco mudaram o resultado: cinco funcionalidades novas e
três mudanças de casa. É um caso a favor da hipótese H2 da agenda de pesquisa do livro (revisão
fresca acha mais defeito), mas um caso só, sem grupo de controle: continua hipótese.

## O que os estudos ensinaram juntos

Postos lado a lado, os seis estudos deixam um procedimento que não depende do Maestro.

**A pergunta escolhe a profundidade.** "O que existe?" pede varredura. "Como isso funciona e o
que pressupõe?" pede o código numa versão fixada. "O que construir?" pede matriz com fonte por
célula e juízes que não escreveram a matriz. Gastar estudo profundo com o que a varredura já
descarta por princípio é desperdício; decidir com varredura o que depende de mecanismo é risco.

**A unidade é a ideia.** Nenhum dos estudos terminou em adoção de ferramenta; quase todos
terminaram em ideias reimplementadas. A exceção, o Spec Kit, é a mais consequente do método, e
por isso é uma só. Cinco análises de *control plane* no ciclo 076 chegaram ao mesmo lugar por
outro caminho: construir, com os padrões dos outros nas bordas, nenhum produto como base
[CLAIM-94-022].

**Momento e estado são artefatos diferentes.** O card diz o que se julgou num dia; o índice diz
o que vale hoje. Os apêndices do handbook ganharam um aviso de migração no topo e não foram
reescritos; o ADR 0008 também não. O catálogo não reescreve a história, e o guarda de
imutabilidade do Maestro, um *hook* que roda antes de cada escrita do agente, recusa a
reescrita de um card datado.

**"Observar" exige gatilho; "absorver" exige arquivo.** As duas regras parecem burocracia até
você ver as cinco absorções fantasmas do ciclo 047. Uma decisão sem destino conferível é uma
intenção registrada como fato.

**Licença decide antes do mérito.** Uma biblioteca excelente com licença não comercial é
citável, não copiável, e nenhuma quantidade de qualidade compensa isso.

## Exemplo executável

O exemplo em [`exemplo/`](exemplo/README.md) é um portão mínimo de catálogo, em Python 3 sem
dependências, reescrito do zero a partir das regras do `check-ecosystem.sh`. A fixture reproduz
em miniatura o dia em que o catálogo do Maestro nasceu: quatro fontes, cinco cards e três
versões do índice de estado.

```bash
cd livro/apendices/d-estudos-de-campo/exemplo
python checa_catalogo.py catalogo --estado catalogo/estado-1-migracao.jsonl
python checa_catalogo.py catalogo --estado catalogo/estado-2-corrigido.jsonl --anterior catalogo/estado-1-migracao.jsonl
python checa_catalogo.py catalogo --estado catalogo/estado-3-retrodatado.jsonl
python checa_catalogo.py catalogo --estado catalogo/estado-3-retrodatado.jsonl --anterior catalogo/estado-1-migracao.jsonl
```

O índice da migração sai com código 1 e três achados: o *worktree* absorvido numa pasta, os
padrões absorvidos num destino que não existe, e a biblioteca de licença não comercial em
"observar" sem gatilho. O índice corrigido por acréscimo sai com 0. O terceiro comando é o
atalho que pegou o próprio ciclo 047: reescrever as linhas antigas em vez de acrescentar.
Sozinho, o portão de âncora o aprova, com código 0. Com o índice anterior como referência, o
quarto comando acusa a reescrita [CLAIM-94-023]. O README traz a saída esperada de cada
comando e a mutação que a revisão do 047 usou para reprovar o portão do Maestro: uma absorção
apontando para um `README.md` que existe, mas não contém a ideia.

O ponto do exemplo é o terceiro comando. Um portão que só confere o estado atual não vê a
história sendo reescrita; para isso ele precisa de uma referência do passado, seja o índice
anterior, seja o histórico do Git.

## O que o portão não vê

O catálogo do Maestro é o melhor registro de estudos de campo que este livro conhece, e mesmo
assim quatro coisas escapam dele na versão citada. Elas não são falhas de execução; são o limite
do que um portão de âncora mede.

**Um gatilho que disparou sem ninguém acrescentar a linha.** O estado corrente do *worktree*
por tarefa é `observar`, com o gatilho "dois ou mais agentes escrevendo no mesmo repositório
ao mesmo tempo, com conflito observado". Em 20 de outubro de 2026, o ciclo 066 entregou um
lançador de sessões que cria um *worktree* do Git por trabalhador, em `scripts/multi-session.py`
(commit `d5feef2`), e a spec do mesmo ciclo descreve um projeto com 16 sessões simultâneas e
cerca de 160 *worktrees* em três dias [CLAIM-94-024]. A ideia é vizinha, não idêntica (um
*worktree* por trabalhador, não por tarefa), e cabe a um humano dizer se o gatilho disparou.
O fato observável é outro: nada no catálogo registrou o evento. O portão confere que todo
`observar` tem gatilho; não confere se o gatilho já aconteceu. Gatilho escrito é necessário,
mas não é suficiente: alguém precisa ler os gatilhos quando o trabalho muda de forma, e a
retrospectiva é o lugar natural para isso (capítulo 14).

**Uma descrição de fonte que contradiz o estudo.** O `fontes.md` descreve o `maestro-02` como
"tentativa anterior do próprio método", com licença "MIT (nosso)". O estudo de 31 de julho diz
o contrário: projeto homônimo e independente, *fork* de `sharpdeveye/maestro` [CLAIM-94-025].
O portão confere que a linha tem licença e data; não confere se a descrição é verdadeira.

**Um número que envelheceu longe do catálogo.** O roteiro do Maestro, na linha da fase F22,
descreve o catálogo com "30 cards imutáveis, 18 fontes". O relatório de qualidade do mesmo
ciclo fecha com 40 cards e 23 fontes, depois que a revisão recuperou dez cards e cinco fontes
perdidos na migração [CLAIM-94-026]. O número do roteiro é o de antes da revisão, e nenhum
portão liga os dois arquivos. A fase F7, que agrupou os três primeiros estudos de campo
(ciclos 010 a 012), está marcada como concluída no mesmo roteiro
([roadmap](https://github.com/GHDaru/maestro/blob/19823c2/docs/roadmap.md)).

**Um índice que se declara append-only, mas que nada guarda.** O guarda de imutabilidade
protege os cards datados, os ADRs e as linhas passadas do índice de decisões. O `estado.jsonl`
do catálogo ficou de fora, por escolha registrada: diferente do índice de decisões, ele não tem
um script de acréscimo, e recusar a escrita deixaria sem caminho para registrar um veredito. A
lacuna foi anotada como achado no ciclo 056, em vez de meio consertada [CLAIM-94-028]. É
exatamente o buraco por onde passou a retrodatação do ciclo 047, e o que o terceiro comando do
exemplo mostra: sem uma referência do passado, a reescrita parece um estado válido.

## Contraexemplo: quando não fazer estudo de campo

**Ferramenta de uso pontual e reversível.** Se o time vai usar um formatador ou um gerador de
diagrama numa tarefa e jogá-lo fora, um card com sete dimensões é cerimônia. O catálogo existe
para o que atravessa a fronteira e fica: ideias que mudam o método, dependências que viajam
com a distribuição.

**Dor que já é real.** Se o problema está acontecendo agora, a pergunta deixa de ser "vale
observar?" e passa a ser "qual a menor coisa que resolve?". O funil é para o que ainda não
dói; quando dói, vá direto ao estudo com a mão no código das duas ou três opções sérias.

**Time sem ninguém para ler os gatilhos.** Um catálogo de gatilhos que ninguém revisita dá a
sensação de controle sem o controle (o caso do *worktree*, acima). Se o time não tem
retrospectiva regular, comece por ela; o catálogo vem depois.

**O custo.** Cada estudo profundo deste apêndice ocupou um ciclo inteiro, e o 073 ocupou quatro
rodadas com sete agentes e três juízes [CLAIM-94-029]. O catálogo exige disciplina de acréscimo que a revisão
do 047 mostrou ser fácil de quebrar. Para um time que avalia uma ferramenta por ano, uma linha
num ADR com o gatilho escrito basta.

## Evidência

Os fatos deste apêndice vêm de arquivos versionados do Maestro, no commit `19823c2` salvo
indicação, e cada número está registrado em [`claims.md`](claims.md) com o caminho ou o
comando que o reproduz. Os estados:

- **Medidos** (reproduzidos por comando neste trabalho): o estado corrente do catálogo, com 24
  fontes, 41 cards e a contagem por veredito [CLAIM-94-016]; o *worktree* por trabalhador no
  lançador de sessões [CLAIM-94-024]; a saída do exemplo [CLAIM-94-023].
- **Observados** (lidos nos registros do Maestro, sem reexecução): as datas e os vereditos de
  cada estudo [CLAIM-94-001, CLAIM-94-007, CLAIM-94-008, CLAIM-94-010, CLAIM-94-011,
  CLAIM-94-012]; as absorções fantasmas e a reclassificação [CLAIM-94-002, CLAIM-94-003]; a
  revisão do 047 e as baterias de mutação [CLAIM-94-004, CLAIM-94-015]; os números da matriz e
  do confronto do 073 [CLAIM-94-018, CLAIM-94-019, CLAIM-94-020, CLAIM-94-021]; as
  inconsistências de registro [CLAIM-94-006, CLAIM-94-025, CLAIM-94-026].
- **Hipótese**: que juízes em contexto fresco acham mais defeito (H2 da agenda de pesquisa do
  livro). O 047 e o 073 são casos a favor, sem grupo de controle.

Os números de popularidade e de custo de terceiros que apareciam nas fichas de 2026 não entram
aqui como evidência. A própria ficha do ciclo 007 os declarou não auditados, e o catálogo os
excluiu como dimensão de decisão.

## Checklist

- [ ] Toda avaliação de ferramenta externa no seu time tem data e versão (ou commit) observada.
- [ ] O veredito usa um vocabulário fechado, e "absorver" aponta para um arquivo que contém a
      ideia, com um texto que se pode procurar com `grep`.
- [ ] Todo "observar" tem um gatilho observável escrito; "quando doer" não conta.
- [ ] A licença de cada fonte está registrada, e as que impedem cópia dizem "só citável".
- [ ] O registro da observação é imutável; mudança de veredito é linha nova, com data e motivo.
- [ ] Um script confere as âncoras e foi visto acusar ao menos uma mutação.
- [ ] A retrospectiva revisa os gatilhos em observação quando o jeito de trabalhar muda.
- [ ] "Isso já foi avaliado?" se responde com um link, em menos de um minuto.

## Referências

Maestro, versão `19823c2` (01/11/2026), `https://github.com/GHDaru/maestro`:

- ADR 0008 — avaliação do ecossistema SDD:
  https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0008-avaliacao-ecossistema-sdd.md
- Ficha de pesquisa do ciclo 007:
  https://github.com/GHDaru/maestro/blob/19823c2/docs/research/avaliacao-ecossistema-sdd.md
- Specs dos ciclos 007, 010, 012, 047 e 073:
  https://github.com/GHDaru/maestro/blob/19823c2/specs/007-avaliacao-ecossistema-sdd/spec.md ·
  https://github.com/GHDaru/maestro/blob/19823c2/specs/010-estudo-superpowers/spec.md ·
  https://github.com/GHDaru/maestro/blob/19823c2/specs/012-panorama-templates/spec.md ·
  https://github.com/GHDaru/maestro/blob/19823c2/specs/047-catalogo-do-ecossistema/spec.md ·
  https://github.com/GHDaru/maestro/blob/19823c2/specs/073-area-administrativa/spec.md
- Apêndices A, B e C do handbook:
  https://github.com/GHDaru/maestro/blob/19823c2/docs/handbook/apendice-a-maestro-02.md ·
  https://github.com/GHDaru/maestro/blob/19823c2/docs/handbook/apendice-b-superpowers.md ·
  https://github.com/GHDaru/maestro/blob/19823c2/docs/handbook/apendice-c-panorama-templates.md
- Catálogo do ecossistema:
  https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/README.md ·
  https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/fontes.md ·
  https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/estado.jsonl
- Portão e template:
  https://github.com/GHDaru/maestro/blob/19823c2/scripts/check-ecosystem.sh ·
  https://github.com/GHDaru/maestro/blob/19823c2/.specify/templates/evaluation-template.md
- Relatórios de qualidade dos ciclos 047 e 073:
  https://github.com/GHDaru/maestro/blob/19823c2/specs/047-catalogo-do-ecossistema/qa-report.md ·
  https://github.com/GHDaru/maestro/blob/19823c2/specs/073-area-administrativa/qa-report.md

Fontes externas estudadas pelo Maestro, citadas pelo endereço registrado nos estudos (acesso
dos estudos: 30/07 a 01/08/2026; não reabertas para este apêndice): `obra/superpowers`,
`bmad-code-org/BMAD-METHOD`, `kiro.dev/docs/specs`, `eyaltoledano/claude-task-master`,
`buildermethods/agent-os`, `sharpdeveye/maestro`, `Pimzino/claude-code-spec-workflow`,
`catlog22/claude-code-workflow`, `Wirasm/PRPs-agentic-eng`, `webdevtodayjason/context-forge`,
`kennyjpowers/claude-flow`.
