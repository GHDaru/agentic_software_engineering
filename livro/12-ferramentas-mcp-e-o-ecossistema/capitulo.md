# 12 — Ferramentas, MCP e o ecossistema

> "Um guarda que ninguém chama passava no portão que existe para provar que ele é chamado."
> — revisão independente do ciclo 056, Maestro

Enquanto o agente só escreve texto, o pior que ele faz é um diff ruim, e um diff ruim para no
merge. No dia em que você liga uma ferramenta a ele (um terminal, um banco, uma interface de programação (API, *application programming
interface*) de terceiros, um servidor do Model Context Protocol (MCP)), cada chamada passa a ser um **efeito** que
acontece agora, longe do seu portão de merge. Este capítulo é sobre essa troca: o que muda no
risco, quem decide quais ferramentas o agente vê, como tratar o que volta delas e como escolher
o que adotar de um ecossistema que lança uma ferramenta nova por semana. Se o seu time vai ligar
agentes a ferramentas reais, a pergunta deixa de ser "o modelo é bom?" e passa a ser "o que ele
pode tocar, e quem garante isso sem depender de ele ter lido a regra?".

## Pergunta central

O que muda quando o agente age no mundo por ferramentas, e como governar essa superfície (o que
ele vê, o que ele pode chamar, o que volta para o contexto dele e de onde vêm as ferramentas)
sem depender de o agente obedecer a uma instrução?

## Resultado de aprendizagem

Ao final, você consegue:

1. **Classificar** cada ferramenta ligada a um agente pela classe de risco da ação que ela
   executa, e atribuir a ela `allow`, `deny` ou `ask` numa política que vive fora do modelo.
2. **Distinguir** instrução de imposição (*enforcement*): apontar, num arquivo de instrução do
   seu repositório, cada regra que só vale enquanto for lida, e dizer qual mecanismo (hook,
   portão, permissão) a impõe ou declarar que nenhum impõe.
3. **Sondar** um servidor de ferramentas antes de ligá-lo, com casos que provam descoberta
   mínima, identidade fora do argumento, resultado cercado como dado e confinamento de caminho.
4. **Julgar** uma ferramenta ou framework do ecossistema por ideia, não por produto, com licença
   e reversibilidade como dimensões que reprovam sozinhas e um gatilho escrito para tudo que
   ficar em "observar".
5. **Distribuir** o método do seu time para outro repositório sem mentir sobre o que foi
   instalado: escolha de agente declarada, atualização que não pisa no arquivo alheio, licença
   e atribuição que viajam com a cópia.

## A falha real

Em 16 de agosto de 2026, o Maestro abriu o ciclo 056 com um diagnóstico incômodo. O método
declarava três coisas imutáveis (o corpo de um registro de decisão de arquitetura (ADR,
*Architecture Decision Record*) já commitado, as linhas passadas do índice de decisões e os
cartões datados do catálogo do ecossistema) e **nada** impedia um agente de reescrevê-las.
Nenhum dos portões que tocavam aqueles caminhos conferia imutabilidade; conferiam forma e
índice. A regra existia como uma frase que o agente precisava ter lido e lembrado
([spec 056](https://github.com/GHDaru/maestro/blob/19823c2/specs/056-instalar-o-harness/spec.md)).

A resposta foi instalar uma camada de *harness*: um hook `PreToolUse`, que o Claude Code chama
**antes** de executar uma ferramenta de escrita e que pode recusar a chamada. Pela primeira vez
o método recusaria antes de o dano existir, em vez de auditar depois. O instalador passaria a
escrever o `.claude/settings.json` do repositório de destino, e o bloco de instrução gerado
diria ao agente que aqueles artefatos estavam protegidos. O ciclo foi para a revisão
independente, em contexto fresco, com a instrução de refutar e de executar os ataques.

A revisão reprovou o ciclo com 24 achados, nove deles bloqueantes [CLAIM-12-001]. Os que mais
ensinam não são bugs de lógica; são falhas da ferramenta **como ferramenta**:

- **Um espaço no caminho do projeto desligava o guarda em silêncio.** O comando do hook não
  estava entre aspas. Num projeto em `~/My Projects/…`, o hook saía com código 127, que o
  `PreToolUse` trata como erro não bloqueante [CLAIM-12-002]. O guarda ficava inerte **enquanto
  o `CLAUDE.md` instalado no mesmo repositório afirmava que ele protegia**.
- **O portão provava o script, nunca a fiação.** Apagar o `settings.json` deixava tudo verde:
  um guarda que ninguém chama passava no portão escrito para provar que ele é chamado.
- **Três desvios por link simbólico** [CLAIM-12-003], todos executados pelo revisor. O guarda
  normalizava caminhos de forma léxica, sem resolver links. O instalador tinha aprendido essa
  lição quatro ciclos antes, no 052; o guarda novo, não.
- **O instalador podia morrer no meio e deixar a instalação órfã para sempre.** Com o
  `settings.json` somente leitura, o script morria depois de escrever 78 arquivos e antes do
  manifesto; a execução seguinte gravava um manifesto vazio e passava a desconhecer 77 arquivos
  do método [CLAIM-12-004].
- **O bloco afirmava proteção mesmo quando ela não era instalada** (com `--no-hooks`, em
  conflito, com link simbólico). E o trecho "exato para colar" que o instalador imprimia era
  JSON (*JavaScript Object Notation*) inválido: sete chaves abertas contra oito fechadas [CLAIM-12-005].

Repare na forma do pior achado. O defeito que a spec existia para combater era "norma sem
função de força". A entrega o inverteu: **função de força inexistente, afirmada**. Um texto que
diz "este guarda protege você" num repositório onde o guarda sai com 127 é pior que nenhum texto,
porque desliga a desconfiança de quem lê, humano ou agente.

O conserto foi na raiz: comando entre aspas, escrita atômica do `settings.json`, o guarda
confinado ao repositório e resolvendo links, o bloco de instrução dizendo a verdade conforme o
que foi de fato instalado, e asserções novas que provam a **fiação**, cada uma vista reprovando
por mutação: guarda apagado, `settings.json` apagado, `settings.json` sem o `PreToolUse`, script
de sessão apagado [CLAIM-12-006]. O commit da entrega é de 21 de agosto
([`813a469`](https://github.com/GHDaru/maestro/commit/813a469)).

Duas semanas depois, a mesma lição apareceu do outro lado da mesa. O ciclo 064 reescreveu a
capa do repositório para a inteligência artificial (IA) que vai instalar o método, e publicou um
comando que clonava para `/tmp/maestro` em três linhas soltas. A nota de segurança do próprio
ciclo examinou exatamente aquele caminho e concluiu "nada a fazer", porque o `git clone` recusa
destino existente. A recusa era verdadeira e irrelevante: as linhas não estavam encadeadas, e a
seguinte executava `/tmp/maestro/bin/maestro` de qualquer jeito. A revisão independente provou
com um executável plantado, que imprimiu "código de terceiro executado" com o bloco saindo 0
([qa-report 064](https://github.com/GHDaru/maestro/blob/19823c2/specs/064-capa-para-a-ia-que-instala/qa-report.md);
commit [`00bea14`](https://github.com/GHDaru/maestro/commit/00bea14)) [CLAIM-12-007]. Um
comando publicado para um agente copiar e executar é uma ferramenta, e quem o publica responde
pelo que ele faz na máquina de outro.

## Teoria

### Do texto ao efeito

O capítulo 11 derivou do teorema T3 do Maestro que o portão escala com a irreversibilidade,
nunca de modo uniforme: se o custo de desfazer é assimétrico (axioma A5) e a consequência
precisa de dono (A2), um portão igual para tudo vira carimbo ou deixa passar o irreversível
([axioms.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/axioms.md);
[capítulo 11](../11-risco-reversibilidade-e-autonomia/capitulo.md)). Ferramenta é onde esse
teorema deixa de ser teoria.

Sem ferramenta, a saída do agente é um artefato que espera. O diff fica numa branch, o portão
fica no merge, e entre um e outro cabem revisão, teste e humano. Com ferramenta, a saída é uma
chamada que **executa**: apaga a linha, publica o pacote, manda a mensagem, roda o comando. A
classe de risco não está mais no artefato final; está em cada chamada. Por isso a unidade de
governança muda. Você não governa "o agente"; governa **a superfície de ferramentas** que ele
alcança, uma ferramenta por vez, pela classe da ação que ela executa.

A taxonomia do capítulo 11 se aplica direto, ferramenta a ferramenta: leitura (buscar, listar)
pode rodar sozinha; leitura sensível (segredo, dado pessoal) pede política e máscara; criação
reversível passa pelo merge; alteração, exclusão, efeito externo e o irreversível pedem humano,
proporcional ao estrago. O que o mundo das ferramentas acrescenta são três modos de falha que o
diff não tinha.

### Três riscos que o diff não tinha

O projeto OWASP (*Open Worldwide Application Security Project*) mantém um Top 10 de riscos para
aplicações com modelos de linguagem grandes (LLM, *large language model*). Três itens da edição
2025 descrevem quase tudo o que este capítulo trata.

**Agência excessiva (LLM06).** O agente tem funcionalidade demais (ferramentas de que a tarefa
não precisa), permissão demais (a ferramenta de leitura conecta com credencial de escrita) ou
autonomia demais (ação de alto impacto sem confirmação humana). Os três se resolvem fora do
modelo: menos ferramentas visíveis, credencial do tamanho da tarefa e `ask` onde a ação não se
desfaz.

**Injeção de prompt (LLM01), sobretudo a indireta.** O texto que volta de uma ferramenta (a
issue, o e-mail, a página, o resultado da busca) entra no contexto com a mesma tinta das
instruções do operador. Greshake e colegas mostraram em 2023 que aplicações reais podem ser
comprometidas por instruções plantadas em conteúdo que o modelo apenas lê. A regra que o
Maestro escreveu no agente de segurança é curta: dado que chega de fora é hostil por padrão
([`.claude/agents/security.md`](https://github.com/GHDaru/maestro/blob/19823c2/.claude/agents/security.md)).

**Cadeia de suprimento (LLM03).** O que você instala de terceiros (um servidor MCP, uma skill,
um plugin, um template) entra no seu processo. Num sistema agêntico, boa parte dessa carga
**é prosa**: instrução que o modelo lê e segue. O ciclo 046 do Maestro chamou de teatro a ideia
de resolver isso com um inventário de dependências (SBOM, *Software Bill of Materials*): um
arquivo todo em markdown, sob licença MIT (*Massachusetts Institute of Technology*), sem uma
dependência sequer, ainda pode instruir dano
([glossário](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/glossary.md)).
O risco de um pacote de prompts não está no manifesto; está no texto.

### Instrução não é imposição

A tese que atravessa este livro tem aqui seu caso mais nítido: **instrução não é
*enforcement***. O arquivo de instrução do agente (`CLAUDE.md`, `AGENTS.md`,
`.github/copilot-instructions.md`, conforme a ferramenta) é um pedido. O agente o lê no começo
da sessão, e a compactação de contexto, a pressa ou uma instrução injetada podem fazê-lo
esquecer ou desobedecer. Uma regra que só existe ali vale enquanto for seguida.

Imposição é outra coisa: um mecanismo que o agente não pode pular porque não passa por ele. A
permissão que o harness aplica antes de chamar a ferramenta; o hook que recusa a escrita; o
portão da integração contínua (CI, *continuous integration*) que reprova o pull request. A falha
real deste capítulo mostra que o mecanismo também tem modos de falha (falhar aberto, não ser
chamado, ser contornado por outra porta) e que **afirmar** uma imposição inexistente é o pior
dos mundos. O corolário C7 do Maestro diz isso numa linha: norma sem executável é norma sem
efeito.

### Autorização fora do modelo

Se o modelo pode ser convencido por um texto que leu, ele não pode ser quem decide o que tem
permissão de fazer. O handbook do Maestro escreve a regra como dois princípios juntos:
autorização fora do modelo (quem decide permissão é a política, não a IA) e menor privilégio
([handbook, cap. 10 §4](../../maestro-handbook/handbook/10-gates-classes-de-risco.md)). Na
prática, isso significa três escolhas de desenho:

1. **A identidade de quem chama vem do processo, nunca do argumento.** Se a ferramenta aceita
   `autor` no corpo da chamada, o modelo escreve o autor que quiser.
2. **A política é por papel e por ferramenta**, com três valores: `allow`, `deny`, `ask`. O que
   não está escrito é negado. E `ask` não é sugestão: a ação não executa até um humano dizer sim.
3. **A ferramenta negada nem aparece.** Menor privilégio vale também para a descoberta: um
   agente que vê `apagar_registro` na lista é um agente que pode ser convencido a pedi-la.

### O que o MCP padroniza, e o que não

O MCP, publicado pela Anthropic em novembro de 2024 e hoje mantido como
especificação aberta, padroniza **como** um cliente (o harness do agente) descobre e chama
capacidades expostas por um servidor. As mensagens são JSON-RPC 2.0 (*JSON Remote Procedure
Call*), por dois transportes principais: a entrada e saída
padrão de um subprocesso local (stdio) ou HTTP (*Hypertext Transfer Protocol*). Um servidor
oferece três tipos de primitiva: **ferramentas** (funções que o modelo pode chamar, como
`tools/list` e `tools/call`), **recursos** (dados que o cliente pode ler) e **prompts** (modelos
de instrução reutilizáveis).

O ganho é real: uma ferramenta escrita uma vez serve a qualquer harness que fale o protocolo, e o
time deixa de escrever um adaptador por agente. O estudo de campo do Maestro sobre o projeto
homônimo `maestro-02` mostra o padrão em escala: um servidor MCP com 25 prompts, 10 ferramentas
e 8 recursos que transforma as skills do toolkit em serviço, distribuído a partir de uma fonte
única para 10 provedores de agente [CLAIM-12-008]
([apêndice A do handbook](../../maestro-handbook/handbook/apendice-a-maestro-02.md)).

O que o protocolo **não** decide é exatamente o que importa para o seu risco: se aquela sessão
deveria ver aquela ferramenta, se o argumento `autor` é verdade, se o texto que volta é dado ou
ordem, se o arquivo pedido está dentro do diretório permitido. O MCP é o encanamento; a
política é sua. Um servidor MCP que você instala é, do ponto de vista do risco, um pedaço de
código de terceiro com acesso ao contexto do seu agente.

### A interface também é desenho

Há um argumento de qualidade, além do de segurança. O trabalho do SWE-agent (Yang e colegas,
2024) mostrou que o desenho da interface entre agente e computador (que comandos existem, o que
eles devolvem, quanto devolvem) muda de forma mensurável o desempenho do mesmo modelo em tarefas
de engenharia. Uma ferramenta que devolve cinco mil linhas enche o contexto (o axioma A3: o
contexto é finito e se degrada ao encher; ver o
[capítulo 5](../05-engenharia-de-contexto/capitulo.md)); uma que devolve um erro ambíguo
induz tentativa cega. Teto de saída, marca de corte e erro que diz o que fazer são desenho de
produto, e servem ao mesmo tempo à segurança e à qualidade.

### O ecossistema como fonte de ideias

A última peça da teoria é sobre escolher. O ecossistema de ferramentas para agentes muda mais
rápido que qualquer avaliação. Adotar uma ferramenta inteira traz junto o processo, o
vocabulário e o aprisionamento (*lock-in*) dela. A alternativa que o Maestro pratica é tratar o
ecossistema como **fonte de ideias**: a unidade de julgamento é a ideia, não o produto; a ideia
entra reimplementada num artefato seu, com destino verificável; licença e reversibilidade
reprovam sozinhas; e o que fica em "observar" leva um gatilho escrito, senão é esquecimento com
cerimônia. O axioma A4 (o que está escrito é o que sobrevive) explica por que o julgamento
precisa morar num arquivo datado: a próxima sessão não lembra que aquilo já foi avaliado.

## Alternativas

Há quatro famílias de resposta à pergunta "como dou ferramentas a um agente com segurança?". Elas
não se excluem; o veredito é sobre onde cada uma resolve e onde para.

**SDKs e frameworks de agente.** O OpenAI Agents SDK (2025) organiza o agente em ferramentas,
*handoffs* entre agentes e *guardrails* que validam entrada e saída, e aceita servidores MCP como
fonte de ferramentas. O Google ADK (*Agent Development Kit*, 2025) e o Microsoft Agent Framework
(anunciado em 2025 como sucessor do Semantic Kernel e do AutoGen) oferecem o mesmo tipo de
peça, com integração forte às nuvens de cada empresa; LangGraph e CrewAI, tratados no
[capítulo 6](../06-como-dividir-o-trabalho/capitulo.md), focam em orquestração. **Veredito**:
bons para construir um agente de produto, com as ferramentas declaradas em código. Nenhum deles
decide a sua política por você, e quase todos tornam fácil dar ferramentas demais. Use o
*guardrail* como camada, não como política.

**O harness de desenvolvimento como fronteira.** Ferramentas como o Claude Code trazem
permissões `allow / deny / ask` por ferramenta e padrão de comando, hooks (`PreToolUse`,
`SessionStart`, `Stop`, entre outros) e configuração de servidores MCP por projeto. **Veredito**:
é o lugar certo para a imposição, porque fica entre o modelo e a ação. O custo é o acoplamento:
hook é mecanismo de um harness, e a regra imposta por ele não existe nos outros. O Maestro adota
e declara esse limite (ver "O padrão Maestro").

**Plataformas gerenciadas e *control planes*.** Plataformas de agentes em nuvem oferecem memória
gerenciada, delegação entre agentes e fluxo determinístico; *control planes* de agentes prometem
coordenar muitas sessões. O Maestro avaliou a plataforma do Google em agosto de 2026 e registrou
"observar", com gatilho: ir para nuvem gerenciada é decisão de infraestrutura, não de método
([ideia 040](https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/ideias/040-plataforma-gerenciada-de-agentes.md)).
Em outubro de 2026, cinco análises na fonte (Paperclip, CompozyOS, AgentConnect, o Agent Client
Protocol (ACP) e o protocolo Agent2Agent (A2A)) levaram a "construir, com os padrões nas bordas":
nenhum produto como base, os nomes do A2A no envelope de mensagem, e os três produtos viraram
régua do crítico [CLAIM-12-009]
([decisões](https://github.com/GHDaru/maestro/blob/19823c2/docs/records/decisoes.jsonl),
id `decisao-076-control-plane-v2`). **Veredito**: adote o protocolo nas bordas, onde ele
garante interoperabilidade; não adote o produto como base enquanto ele exigir infraestrutura que
você não tem ou sessões que morrem com um processo central.

**Frameworks inteiros de processo.** No espaço de desenvolvimento orientado por especificação
(SDD, *Spec-Driven Development*), o Maestro avaliou em julho de 2026 sete ferramentas
(Superpowers, BMAD, Kiro, Taskmaster, Agent OS, GSD e Tessl) [CLAIM-12-010] e decidiu: manter o
Spec Kit como ferramenta única, descartar o BMAD (substituiria o modelo de governança com
cerimônia já rejeitada), descartar o Kiro **como ferramenta** por aprisionamento de IDE
(*integrated development environment*) e não adotar o Superpowers por atacado (seria uma segunda
fonte de verdade de processo), absorvendo ideias com destino concreto
([ADR 0008](https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0008-avaliacao-ecossistema-sdd.md)).
**Veredito**: framework inteiro de processo compete com o seu; absorva a ideia, não o pacote.

| Família | Resolve | Para em | Veredito |
|---|---|---|---|
| SDK de agente (Agents SDK, ADK, Agent Framework) | declarar ferramentas, *guardrails* | política e menor privilégio são seus | adotar como peça, não como política |
| Harness com permissões e hooks | imposição antes da ação | acoplado a um harness | adotar, declarando o limite |
| Plataforma gerenciada / *control plane* | coordenação e memória gerenciadas | infraestrutura e aprisionamento | observar com gatilho; protocolo nas bordas |
| Framework inteiro de processo | processo pronto | segunda fonte de verdade | absorver ideias |
| MCP | interoperabilidade da ferramenta | não decide permissão nem confiança | adotar como encanamento |

## O padrão Maestro

O Maestro resolve a superfície de ferramentas em cinco camadas. Em cada uma, vale dizer o que é
**regra** (texto que o agente lê), o que é **script** (portão que reprova) e o que é **hook**
(mecanismo do harness que recusa antes). Tudo citado em `maestro@19823c2`.

### 1. A camada de harness: o que recusa antes

Regra: nunca reescrever o que o método guarda como história; a via é sempre acrescentar (novo
ADR que substitui, `scripts/record-decision.sh`, linha nova de estado)
([`CLAUDE.md`](https://github.com/GHDaru/maestro/blob/19823c2/CLAUDE.md)).

Hook: o `.claude/settings.json` liga três ganchos
([settings.json](https://github.com/GHDaru/maestro/blob/19823c2/.claude/settings.json)). O
`PreToolUse` chama `guard-immutables.py` antes de ferramentas de escrita, de leitura e de shell;
o `SessionStart` chama `session-state.sh`, que imprime o estado **medido** do método (ciclo em
curso, conformidade, achados abertos) em vez de deixar o agente reconstruí-lo de memória; o
`Stop`, acrescentado em outubro de 2026 (commit `cc4e95f`), roda a conformidade das caixas marcadas
quando o agente vai parar e bloqueia a parada uma vez se uma caixa marcada não tem evidência
([stop-conformance.py](https://github.com/GHDaru/maestro/blob/19823c2/scripts/hooks/stop-conformance.py)).
Na entrega do ciclo 056 eram dois ganchos e o *matcher* cobria só as quatro ferramentas de
escrita [CLAIM-12-011].

O guarda tem uma definição precisa de imutável: **já está no histórico do git**. Escrever um ADR
leva várias chamadas (esqueleto, consequências, correção de digitação), e recusar a segunda
chamada bloquearia justamente o que o método pede; a primeira versão tratava "o arquivo existe"
como imutável e a revisão independente pegou
([guard-immutables.py](https://github.com/GHDaru/maestro/blob/19823c2/scripts/hooks/guard-immutables.py)).

E o guarda **declara os próprios limites**, o que é a parte mais rara e mais útil do desenho.
O shell não é guardado para as regras de histórico: para o índice de decisões há razão positiva
(a via sancionada é um comando de shell), mas para corpo de ADR e cartões não há, e um `sed -i`
os alcança. O docstring diz "dito, não desculpado". A regra do banco do painel, acrescentada no
ciclo 075, julga o shell, mas lê o **texto** do comando; um caminho montado em tempo de execução
escapa, e isso fica como risco residual declarado, que vai ao portão humano. O
`estado.jsonl` do catálogo é append-only por regra e não é guardado, porque não tem script de
acréscimo e recusar a escrita deixaria o método sem via. E o guarda **falha aberto** de
propósito: quem impede que um guarda quebrado passe despercebido é o portão, não ele.

Script: `check-installed.sh` prova a fiação na cópia instalada, com os casos que o guarda deve
bloquear e os que deve deixar passar; a revisão do 056 mostrou que provar o script sem provar
que ele é chamado é decoração (o mesmo diagnóstico do
[capítulo 10](../10-quality-gates-que-provam-fatos/capitulo.md)).

Duas lições de origem. A ideia de usar um hook de sessão para impor o "consulte as skills
antes de agir" veio do estudo do Superpowers, cujo hook de início de sessão injeta a meta-skill
em toda conversa; o Maestro absorveu como parágrafo de imposição no `CLAUDE.md`
([apêndice B do handbook, §8](../../maestro-handbook/handbook/apendice-b-superpowers.md)).
E hooks de terceiro também entram por decisão registrada: o ADR 0025 aceitou, com ressalva,
que hooks `SessionStart`/`Stop` de uma ferramenta de workflow gravassem direto no SQLite do
painel, com condições: tabelas próprias, nunca as derivadas; append-only ainda por convenção, sem
gatilho no banco (dívida declarada); o arquivo do banco como fronteira de confiança, porque quem
escreve nele põe texto no contexto do modelo; e a frase que resume a categoria: **os hooks são
ferramenta, não método**, instalados por opção e nunca pelo instalador do método
([ADR 0025](https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0025-hooks-de-terceiro-gravando-sqlite.md)).

### 2. A porta de ferramentas: identidade, política e cerca

O painel de regência do Maestro (a aplicação que acompanha as sessões de agentes em paralelo)
expõe um servidor MCP próprio, em Python sem dependências, com quatro ferramentas:
`estado_atual`, `registrar_status`, `registrar_peca` e `quem_sou_eu`
([mcp_painel.py](https://github.com/GHDaru/maestro/blob/19823c2/painel/mcp_painel.py))
[CLAIM-12-012]. Três decisões de desenho, todas nascidas de achados de revisão de segurança no
ciclo 075, valem para qualquer servidor que você escreva:

- **As ferramentas de escrita não têm argumento de identidade.** O `inputSchema` não declara
  `autor` nem `sessao`. O autor vem do token do processo, resolvido pelo registro do host; um
  `autor` mandado por engano volta num campo `ignorado`. A identidade nunca é escrita pelo modelo.
- **O que volta ao modelo vem cercado como dado.** O resultado entra entre duas marcas
  (`<<<DADO-DE-TERCEIROS>>>` e `<<<FIM-DO-DADO>>>`), com teto de 8 KB e marca explícita de corte
  [CLAIM-12-013]; uma marca de fechamento que venha **dentro** do conteúdo é neutralizada, senão
  bastaria ao texto injetado trazê-la para sair da cerca. E o código diz o limite em voz alta: a
  cerca não é uma sandbox; quem lê ainda pode obedecer ao que está dentro; o que ela faz é tornar
  a fronteira visível
  ([http.py](https://github.com/GHDaru/maestro/blob/19823c2/painel/servidor/adaptadores/http.py)).
- **O token não anda na linha de comando.** A revisão de segurança da tarefa T06 do ciclo 075
  mediu o token escrito no comando codificado de cada painel de terminal, o lugar mais público que
  um processo tem (título da janela, lista de processos, logs). Agora ele é sorteado por subida,
  gravado num arquivo fora do repositório, lido e apagado pelo próprio painel, e só o **hash** fica
  registrado; um teste roda as peças do lançador e confere
  ([test_multi_session_token.py @ 28f495a](https://github.com/GHDaru/maestro/blob/28f495a/scripts/test_multi_session_token.py)).

A política sobre quem chama qual ferramenta segue a mesma lógica: na pesquisa da área
administrativa (ciclo 073), a decisão D2 fixou que **a ferramenta MCP é escopo da política
`allow / deny / ask` por agente**, e não uma tela própria; cada ferramenta aponta para a regra
que a governa ([glossário](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/glossary.md)).
E a credencial do provedor de modelo também fica fora do repositório: quando o ciclo 066 passou
a abrir sete sessões construtoras (um gerente e seis trabalhadores) por um *gateway* de modelos,
três pareceres em contexto fresco chegaram ao mesmo desenho: o token fica na configuração de
escopo do usuário, colocado pelo humano; o repositório declara só o endereço e os modelos; uma
lista mínima de permissões com negação explícita para `git push`, `rm -rf`, `docs/adr`,
`docs/records` e `.env`; e nada de copiar permissões e hooks de outro projeto por conveniência
[CLAIM-12-014] (id `decisao-066-sessoes-via-gateway` no índice de decisões).

Quem revisa essa superfície é um papel sem poder de escrita: o agente `security` tem só
`Read, Grep, Glob, Bash`, avalia injeção, segredos e autorização e trata resultado de ferramenta
como potencialmente hostil
([security.md](https://github.com/GHDaru/maestro/blob/19823c2/.claude/agents/security.md)).

### 3. Instalar é agir no repositório de outro

O método do Maestro chega a outros repositórios por três caminhos, decididos no ADR 0012 do
ciclo 019 ([ADR 0012](https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0012-distribuicao-em-tres-camadas.md)):

- **A — script** `install-maestro.sh`, canônico, leva o método inteiro (agentes, skills,
  scripts, comandos, templates, governança);
- **B — plugin do Claude Code**, gerado das fontes por `package-plugin.sh`, que leva agentes,
  skills e comandos com versão e atualização;
- **C — `npx skills add`**, que leva só as seis skills para qualquer agente compatível com o
  padrão da comunidade, e saiu de graça porque o layout do Maestro já era esse.

Cada caminho declara o que **não** leva. O mesmo ADR decidiu **não** construir uma interface de
linha de comando (CLI, *command-line interface*) própria no estilo do Spec Kit, com números: o
Spec Kit tinha cerca de 6.900 linhas de Python e publicação em índice de pacotes, para entregar o
que um script de 90 linhas já entregava [CLAIM-12-015]. Quando o ciclo 058 criou a porta da
frente `bin/maestro init`, ela nasceu como **despachante** em bash: o arquivo diz que despacha e
nunca implementa, e cada subcomando roda o script que já é dono do passo
([bin/maestro](https://github.com/GHDaru/maestro/blob/19823c2/bin/maestro)).

A ordem dos ciclos é uma lista de lições sobre agir em casa alheia:

- **Existir fora da porta é não existir (ciclo 018).** O instalador existia desde o ciclo 013,
  mas não estava no README; outra IA concluiu que o Maestro "não tinha" instalador
  ([qa-report 018](https://github.com/GHDaru/maestro/blob/19823c2/specs/018-instalacao-e-ux-jornadas/qa-report.md)).
- **Instalar não é copiar.** A receita diz: copiar é um passo; instalado é quando a IA sabe que
  deve seguir o método, e `check-install.sh` só fica verde com as duas metades
  ([receita](../../maestro-handbook/receitas/instalar-o-maestro.md)).
- **Instalar é também atualizar (ciclo 051).** Reinstalar não entregava nada (destino existente
  era pulado) e o `--force` recomendado pela nota da v0.2.0 aninhava diretórios. O instalador
  passou a gravar um manifesto com o hash de cada arquivo escrito: o que é nosso e está intacto
  é renovado; o que o projeto modificou fica, com a versão nova ao lado como `*.maestro-new`; o
  `manifest.tsv` distingue arquivo nosso de arquivo seu
  ([spec 051](https://github.com/GHDaru/maestro/blob/19823c2/specs/051-instalador-que-atualiza/spec.md)).
- **Link simbólico não é porta de saída (ciclo 052).** Com o poder de remover, um link no alvo
  fazia o instalador escrever e podar fora do repositório; o conserto recusa, nomeia e conta a
  recusa, e o ataque virou asserção do portão.
- **Configuração de terceiro não se sobrescreve.** `merge-settings.py` decide o destino do
  `settings.json` alheio em seis veredictos (WRITE, CURRENT, MERGED, UPGRADE, CONFLICT, ERROR) [CLAIM-12-029].
  O CURRENT nasceu porque o instalador conflitava **consigo mesmo**; o UPGRADE, porque um projeto
  instalado na v0.3.0 recebia CONFLICT ao atualizar, já que os hooks antigos do Maestro eram
  indistinguíveis dos de terceiro
  ([merge-settings.py](https://github.com/GHDaru/maestro/blob/19823c2/scripts/hooks/merge-settings.py)).
- **O agente é escolha declarada (ciclo 057).** Até ali o instalador copiava `.claude/*` fosse
  qual fosse a ferramenta. O modelo medido do Spec Kit grava a escolha em arquivo e mapeia 26
  agentes ao arquivo de instrução de cada um [CLAIM-12-016]. O Maestro adotou a forma com
  **quatro** (`claude`, `copilot`, `cursor-agent`, `codex`), nos ids do upstream, porque o custo
  de um agente não é a linha da tabela, é **testar** a instalação lá
  ([install-agents.tsv](https://github.com/GHDaru/maestro/blob/19823c2/scripts/install-agents.tsv)).
  A tabela diz que "a tabela é o suporte"; `-` em comandos significa "formato não verificado, nada
  instalado". E a primeira versão afirmava que as quatro instruções vinham do upstream quando
  duas não vinham, e foi a revisão independente que pegou. A escolha fica gravada em
  `.maestro/install-options.json`, com o campo `harness` registrando o **fato** desta instalação.
- **Hook é mecanismo de um harness.** Para os agentes que não executam hooks do Claude Code, a
  camada não é instalada, o resumo diz por quê, e o bloco de instrução muda: diz que a regra
  vale **enquanto for seguida**, sem afirmar proteção inexistente. É a correção direta do pior
  achado do ciclo 056.
- **A porta da frente roda sem humano (ciclo 058).** `maestro init` conduz agente, destino,
  instalação e verificação, e sai diferente de zero se a verificação falhar; toda pergunta tem
  forma de flag, e sem terminal e sem `--yes` ele **recusa** em vez de responder por você. O mesmo ciclo achou três mentiras na documentação da instalação (uma flag com o nome errado, a
  promessa de que o script não sobrescreve, um uso que não citava as flags novas) e criou o
  portão `check-flags`, que compara as flags que o parser aceita com as que a documentação
  promete [CLAIM-12-031].
- **A capa serve a quem instala (ciclo 064).** A sessão de um agente não tem terminal; o README
  publicava só a forma interativa, e a IA que o seguisse saía com código 2 e zero arquivos
  escritos [CLAIM-12-017]. A capa passou a publicar primeiro `--ai <id> --yes`, e a falha do
  `/tmp/maestro` contada na falha real foi corrigida na raiz.

Numa instalação real por `maestro init --ai claude`, o projeto recebe 81 arquivos; com
`--ai codex`, 53 e nenhum `.claude/` [CLAIM-12-018]. O motor de especificação chega como 12
comandos (`/speckit.specify`, `clarify`, `plan`, `tasks`, `implement`, `analyze`, `checklist`,
`constitution`, `converge`, `taskstoissues`, mais `/dod` e `/eval`), ao lado de 13 subagentes e 6
skills [CLAIM-12-019]. Tudo isso é escrito em inglês: a superfície instalável é lida por agentes
em repositórios de terceiros, e o ciclo 033 fixou a fronteira (instalável em inglês, livro em
português), guardada por `check-language.sh`
([spec 033](https://github.com/GHDaru/maestro/blob/19823c2/specs/033-ingles-no-instalavel/spec.md)).

O que o instalador **não** faz também é decisão. O `maestro-ledger`, mod do Claude Code que
transforma as etiquetas de tarefa em registro de tokens e tentativas, é instalado por
`claude plugin install`, nunca pelo instalador do método, porque escreve nas configurações do
usuário, fora do projeto; e a documentação manda instalá-lo só com escopo de projeto e só em
repositórios confiáveis, porque ele executa o script do repositório aberto
([task-ledger.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/task-ledger.md)).

O caminho B tem seu portão: `package-plugin.sh --verify` reconstrói o plugin num diretório
temporário e falha se ele diverge das fontes
([package-plugin.sh](https://github.com/GHDaru/maestro/blob/19823c2/scripts/package-plugin.sh)).
O ciclo 044 mostrou por quê: o plugin é build commitado; o autor editou a fonte de um comando
vendorizado e não reconstruiu, e o plugin continuou entregando o texto que o ciclo existia para
apagar. O `--verify` estava vermelho, era passo bloqueante da CI escrito uma hora antes, no
ciclo 043, e o autor não o rodou porque a lista de verificação do próprio plano não o citava
[CLAIM-12-020]
([qa-report 044](https://github.com/GHDaru/maestro/blob/19823c2/specs/044-speckit-plan-defere-a-declaracao/qa-report.md)).

### 4. Proveniência e licença: o que entra e o que viaja

O Spec Kit foi **vendorizado** no ciclo 009: os templates passaram a ser fonte do Maestro,
adaptados (raias, critérios verificáveis, gate humano), e o upstream entra por decisão
registrada, nunca por reinstalação automática. O custo declarado é assumir a manutenção
([handbook, cap. 13 §5.13](../../maestro-handbook/handbook/13-decisoes-de-engenharia.md)). O
`.specify/UPSTREAM.md` marca o estado de cada peça, e a segunda regra dele nasceu de um achado:
o comando vendorizado `speckit.plan` mandava gerar quatro artefatos incondicionalmente,
contradizendo a tabela de declaração do template de plano; mexer nele era questão de
proveniência, logo decisão, e o ciclo 044 fechou com a regra "divergência declarada, nunca
silenciosa" (ids `achado-042-speckit-plan-contraditorio` e `spec-044-fecha-042`).

A licença virou portão depois de uma ironia. No ciclo 036, o catálogo mais útil encontrado, 70
skills de gestão de produto, estava sob CC BY-NC-SA (Creative Commons
Atribuição-NãoComercial-CompartilhaIgual), incompatível com a distribuição do Maestro; a
regra passou a ser verificar licença **antes** de propor uso [CLAIM-12-021]
([qa-report 036](https://github.com/GHDaru/maestro/blob/19823c2/specs/036-pesquisa-upstream-decomposicao/qa-report.md);
[ideia 015](https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/ideias/015-skills-de-gestao-de-produto.md)).
Dez ciclos depois, um painel de catorze especialistas convocado para outro assunto achou o
espelho [CLAIM-12-022]: por 45 ciclos o Maestro recusara licença alheia sem ter `LICENSE`
próprio, sem nota de terceiros, sem aviso de copyright nos arquivos vindos do Spec Kit, e com o
manifesto do plugin declarando "MIT" sem o texto [CLAIM-12-023]. Repositório sem licença não é
neutro; é "todos os direitos reservados", pior que a licença recusada
([spec 046](https://github.com/GHDaru/maestro/blob/19823c2/specs/046-licenca-e-atribuicao/spec.md)).

O ADR 0020 decidiu: MIT com titular; `THIRD-PARTY-NOTICES.md` separando o que é cópia literal do
que foi modificado, com a linha de copyright de cada upstream; e a atribuição **viajando pelos
dois canais**, renomeada no destino do instalador (`docs/governance/MAESTRO-LICENSE`), porque um
`LICENSE` solto na raiz de um repositório alheio afirmaria que aquele projeto inteiro é MIT do
Maestro ([ADR 0020](https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0020-licenca-mit-e-atribuicao-que-viaja.md)).
O `check-licensing.sh` mede a coerência dos artefatos, não a conformidade jurídica, e diz isso no
cabeçalho; a primeira versão saía com código 0 se o instalador fosse apagado, e "entrada ausente
é falha, nunca aprovação" virou regra
([check-licensing.sh](https://github.com/GHDaru/maestro/blob/19823c2/scripts/check-licensing.sh)).

A mesma honestidade vale para a versão. Ao fechar a v0.2.0, o ciclo 050 registrou que a tag
`v0.1.0` nunca tinha chegado ao GitHub: o push de tag recebia 403 do proxy de saída enquanto o
de branch passava, e a nota de release passou a declarar a meia versão
([spec 050](https://github.com/GHDaru/maestro/blob/19823c2/specs/050-fechar-v0-2-0/spec.md))
[CLAIM-12-024]. E a CI, com token só de leitura, referencia *actions* por tag maior; fixá-las
pelo hash SHA (*Secure Hash Algorithm*) do commit está no roadmap com gatilho escrito: quando um
segredo entrar no workflow ou o token deixar de ser só leitura
([roadmap](https://github.com/GHDaru/maestro/blob/19823c2/docs/roadmap.md)).

### 5. O catálogo do ecossistema: a ideia como unidade

O ciclo 047 criou o catálogo em três peças: `fontes.md` (endereço, licença, data), um cartão
datado e imutável por **ideia** em `ideias/`, e o veredito **corrente** num índice append-only,
`estado.jsonl`. Momento e estado são artefatos diferentes: o cartão diz o que se julgou num dia;
o veredito de hoje mora no índice. O vocabulário é fechado (`adotar`, `absorver`, `observar`,
`descartar`); `adotar` e `absorver` exigem destino que é arquivo e um texto literal que tem de
estar dentro dele; `observar` exige gatilho; e sete dimensões são avaliadas sempre, duas das quais
reprovam sozinhas: conflito insanável com princípio e licença [CLAIM-12-025]
([README do catálogo](https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/README.md)).
O `check-ecosystem.sh` mede que todo julgamento está ancorado.

O portão foi escrito antes do conteúdo e, na primeira execução, achou absorções fantasmas. Duas
ideias que o ADR 0008 registrara como absorvidas (worktree isolado por tarefa e padrões por
camada) nunca tinham chegado ao disco, e ficaram 39 ciclos registradas assim [CLAIM-12-026]
([check-ecosystem.sh](https://github.com/GHDaru/maestro/blob/19823c2/scripts/check-ecosystem.sh)).
Ao todo, cinco ideias estavam como "absorver" com destino condicional e nenhuma tinha arquivo;
voltaram para "observar" com gatilho, em linha nova datada (id
`achado-047-cinco-absorcoes-sem-destino`).

Três cartões mostram o julgamento em ação:

- **Kiro (ideia 009): descartar a ferramenta.** A melhor parte dela, a sintaxe de requisitos
  EARS (*Easy Approach to Requirements Syntax*), atravessou sozinha; a IDE proprietária, não. A
  dimensão de reversibilidade reprova sozinha
  ([ideia 009](https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/ideias/009-ide-proprietaria-spec-first.md)).
- **Skills de gestão de produto (ideia 015): descartar pela licença.** O cartão de 6 de agosto
  dizia "observar e citar"; o veredito corrente, em linha nova de 10 de agosto, é "descartar". O
  cartão não foi reescrito: mudar de ideia é legítimo, apagar o registro de que se pensava
  diferente não é.
- **Plataforma gerenciada de agentes (ideia 040): observar**, com o gatilho "ida a nuvem
  gerenciada".

Dois estudos de campo anteriores ao catálogo seguem a mesma régua. O do `maestro-02` absorveu
cinco ideias (decisões em JSONL (*JSON Lines*) consultável, retrospectiva executável, catálogo de
anti-padrões, entre outras), pôs uma em observação e descartou a adoção integral, que seria segunda fonte de verdade de processo [CLAIM-12-030]. E o
companion, o tutor do livro do Maestro (ciclo 015), mostra o mesmo critério aplicado a um serviço
próprio: busca lexical sem *embeddings* (YAGNI, *You Aren't Gonna Need It*), resposta obrigada a
citar a página, adaptador de modelo compatível com a API
da OpenAI, chave do próprio usuário (BYOK, *bring your own key*) usada só na requisição e nunca
persistida, banco fora do ar sem derrubar o serviço, e **sem ferramentas**: o tutor só lê o livro
([spec 015](https://github.com/GHDaru/maestro/blob/19823c2/specs/015-companion-tutor/spec.md)).
A ferramenta mais segura é a que o agente não tem.

O resultado aparece no corte de versão: a v0.3.0, de 22 de agosto de 2026, foi "a versão em que o
método ganhou porta de entrada", com 17 portões executáveis, 14 bloqueando inteiros na CI e um
bloqueando pela metade [CLAIM-12-027]
([CHANGELOG](https://github.com/GHDaru/maestro/blob/19823c2/CHANGELOG.md)).

## Exemplo executável

O exemplo em [`exemplo/`](exemplo/README.md) é um servidor MCP mínimo, em Python sem
dependências, com três ferramentas escolhidas porque cada uma carrega um risco diferente:
`ler_doc` (o risco é o conteúdo que volta), `registrar_status` (o risco é quem assina) e
`apagar_registro` (o risco é a ação). Ele existe em duas versões com a mesma interface: a
ingênua, que faz o que o pedido manda, e a guardada, com as cinco regras deste capítulo fora do
modelo: identidade pelo token do processo, política `allow / deny / ask` por papel, descoberta
mínima, resultado cercado com teto e marca de corte, e confinamento de caminho.

Um harness, `sondar.py`, sobe cada versão como subprocesso, passa o token por variável de
ambiente, conversa em JSON-RPC pela entrada padrão (como um cliente MCP de verdade) e roda oito
sondas. A S2 é a fixture legítima, um pedido certo que a versão guardada não pode recusar; as
outras sete medem agência excessiva (descoberta, `deny`, `ask`), identidade forjada, injeção
indireta com cerca falsa dentro do documento, teto de contexto e saída de diretório.

```bash
cd livro/12-ferramentas-mcp-e-o-ecossistema/exemplo
python3 sondar.py                  # sai com código 1: a versão ingênua fica EXPOSTA
python3 sondar.py --so guardado    # sai com código 0: 8/8
```

A saída esperada está no README: a versão ingênua passa só na S2 (`1/8 sondas → EXPOSTO`); a
guardada passa nas oito [CLAIM-12-028]. O README traz também a mutação que prova que a sonda
acusa: trocar `ask` por `allow` em `apagar_registro` derruba a S3 e a versão guardada vira
`7/8 → EXPOSTO`. O ponto do exemplo não é o servidor, que é de brinquedo. É o hábito: **sondar a
ferramenta antes de ligá-la ao agente**, com um caso legítimo ao lado dos ataques, e ver cada
sonda reprovar ao menos uma vez.

## Contraexemplo

**Ferramenta só de leitura, em ambiente descartável.** Um agente explorando um repositório
clonado num contêiner que será jogado fora, com ferramentas de busca e leitura, não precisa de
política por papel nem de `ask`. A classe de risco é leitura; o pior caso é gasto de contexto.
Impor a mesma cerimônia de uma ferramenta de escrita em produção é o portão uniforme que o T3
rejeita, na direção do excesso. O custo real ali é o teto de saída, não a política.

**Hook como única linha de defesa.** O hook é mecanismo de um harness; o mesmo repositório
aberto em outra ferramenta não o executa, e o próprio Maestro declara que o guarda falha aberto,
não cobre o shell para as regras de histórico e lê o texto do comando, não a intenção. Tratar o
hook como garantia, em vez de primeira linha atrás da qual há portão e humano, repete o pior
achado do ciclo 056 em escala maior.

**A cerca vendida como defesa.** Cercar o resultado de ferramenta torna a fronteira visível; não
impede o modelo de obedecer ao que está dentro. Se a sua defesa contra injeção indireta é só a
cerca, a ação perigosa continua disponível. O que segura é a política fora do modelo: no exemplo,
é o `ask` que impede a S3, não a cerca da S6.

**Catálogo como burocracia.** Para um time pequeno avaliando uma biblioteca de uso pontual, sete
dimensões e cartão datado custam mais que a decisão. O catálogo paga quando a pergunta "isso já
foi avaliado?" se repete e quando o que entra é **prosa que instrui agentes**. Para uma
dependência de build que não é redistribuída, a regra da licença basta, e o próprio ciclo 046
deixou a auditoria das dependências de build fora de escopo, chamando-a de teatro.

**Construir em vez de adotar, por princípio.** A decisão de "construir, com padrões nas bordas"
do painel do Maestro se apoiou em restrições concretas (Windows, sem Docker, sessões que não
podem morrer com um processo central). Sem essas restrições, adotar um produto maduro pode ser a
decisão certa; "o ecossistema é fonte de ideias" não é dogma contra dependências. O custo do
caminho do Maestro é manutenção própria, e vendorizar o Spec Kit já mostrou o preço: o achado do
`speckit.plan` contraditório e o plugin não reconstruído.

## Evidência

A falha real é observada e reproduzível no relatório do ciclo 056 (24 achados, nove bloqueantes;
o hook que sai com 127; a fiação nunca provada) [CLAIM-12-001, CLAIM-12-002, CLAIM-12-006], e a
do comando publicado em `/tmp/maestro`, no relatório do ciclo 064 [CLAIM-12-007]. As decisões de
desenho da porta MCP (identidade pelo token, cerca de 8 KB com neutralização, token fora do argv)
estão no código e nos testes em `19823c2` e `28f495a` [CLAIM-12-012, CLAIM-12-013]. A
contagem de agentes do upstream (26) e a escolha de quatro estão na tabela de agentes e na spec
057 [CLAIM-12-016].

Há uma divergência medida que vale registrar: o roadmap do Maestro descreve a entrega do catálogo
como "30 cards imutáveis, 18 fontes", mas no commit do próprio ciclo 047 (`e73ee0d`) havia 40
cartões, número que o README do catálogo confirma [CLAIM-12-025]. É um fato dito em dois lugares
sem nada comparando, a família de defeito que este capítulo encontra em instaladores, licenças e
versões; aqui, nos números do registro de um portão.

O exemplo executável é medido: oito sondas, a versão ingênua passa em uma, a guardada em oito, e a
mutação `ask → allow` derruba a guardada para sete [CLAIM-12-028].

O que é **hipótese**, e como tal deve ser lido:

- **H8 (reversibilidade permite mais autonomia).** O capítulo assume que tornar uma ferramenta
  reversível (escrita atômica, `*.maestro-new`, manifesto com hash) permite delegá-la com menos
  portão humano. O Maestro tem casos, não uma medida comparativa; a medida está na agenda do
  [capítulo 15](../15-validando-o-maestro/capitulo.md).
- **Ferramenta desnecessária (GOV-008) e injeção de prompt na documentação (GOV-010)** são dois
  dos dez cenários do benchmark de governança proposto na base de pesquisa do livro
  ([apêndice B](../apendices/b-aseg-bench/)). Que a política por papel e a cerca reduzam esses
  dois modos de falha em agentes reais é hipótese; o exemplo prova o comportamento do servidor,
  não o do modelo diante dele.
- Que o MCP vá se manter como encanamento dominante é aposta de mercado, não evidência. O
  argumento do capítulo (política fora do modelo, identidade fora do argumento, resultado como
  dado) não depende disso: sobrevive à troca do protocolo.

## Checklist

- [ ] Existe uma tabela, versionada, de **toda** ferramenta que cada papel de agente alcança,
      com a classe de risco da ação e o valor `allow`, `deny` ou `ask`; o que não está na tabela
      é negado.
- [ ] Nenhuma ferramenta de escrita aceita identidade (`autor`, `user`, `session`) como
      argumento; a identidade vem do processo ou do harness.
- [ ] A ferramenta negada a um papel não aparece na descoberta (`tools/list` ou equivalente)
      daquele papel.
- [ ] Toda ferramenta que devolve conteúdo de terceiros tem teto de saída, marca de corte e
      delimitação como dado; e o time sabe dizer, por escrito, o que impede a ação caso o
      modelo obedeça ao conteúdo mesmo assim.
- [ ] Ferramentas de arquivo resolvem o caminho (incluindo links simbólicos) e recusam o que
      sai do diretório permitido; há um caso de teste com `../` e um com link.
- [ ] Credenciais de ferramenta e de provedor ficam fora do repositório e fora da linha de
      comando; o repositório guarda no máximo o endereço e o hash.
- [ ] Cada regra do arquivo de instrução do agente está marcada como "imposta por" (hook,
      permissão, portão) ou "vale enquanto for seguida"; nenhuma afirma proteção que não existe
      naquele harness.
- [ ] Todo hook ou guarda tem um portão que prova a **fiação** (apagar a configuração reprova),
      não só o script.
- [ ] Antes de ligar um servidor de ferramentas novo, o time roda sondas com ao menos um caso
      legítimo e viu cada sonda reprovar uma vez.
- [ ] Toda ferramenta ou framework avaliado tem um registro datado com veredito; licença e
      reversibilidade foram olhadas antes de propor uso; e todo "observar" tem gatilho escrito.
- [ ] O que o time redistribui (instalador, plugin, template) leva licença e atribuição, não
      sobrescreve configuração do destino e distingue arquivo seu de arquivo alheio ao atualizar.

## Referências

- Maestro, `maestro@19823c2` — specs 015, 018, 019, 033, 036, 044, 046, 047, 050, 051, 056, 057,
  058, 064; ADRs 0008, 0012, 0020, 0025; `docs/ecosystem/`; `docs/records/decisoes.jsonl`;
  `scripts/hooks/`; `painel/mcp_painel.py`.
  <https://github.com/GHDaru/maestro/tree/19823c2>
- Maestro handbook (por versão, neste repositório): cap. 10 (gates e classes de risco), cap. 13
  §5.13 (vendorização), apêndices A (`maestro-02`) e B (Superpowers), receita "instalar o
  Maestro". `../../maestro-handbook/`
- Model Context Protocol — especificação e documentação. <https://modelcontextprotocol.io>
  (acesso em 02/11/2026).
- OWASP. *Top 10 for LLM Applications 2025* (LLM01 Prompt Injection, LLM02 Sensitive
  Information Disclosure, LLM03 Supply Chain, LLM06 Excessive Agency, LLM10 Unbounded
  Consumption). <https://genai.owasp.org/llm-top-10/> (acesso em 02/11/2026).
- Greshake, K. et al. *Not what you've signed up for: Compromising Real-World LLM-Integrated
  Applications with Indirect Prompt Injection*. arXiv:2302.12173, 2023.
- Yang, J. et al. *SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering*.
  NeurIPS 2024. arXiv:2405.15793.
- Anthropic. Claude Code — documentação de hooks, permissões e MCP.
  <https://docs.anthropic.com/en/docs/claude-code> (acesso em 02/11/2026).
- OpenAI. Agents SDK. <https://openai.github.io/openai-agents-python/> (acesso em 02/11/2026).
- Google. Agent Development Kit (ADK). <https://google.github.io/adk-docs/> (acesso em
  02/11/2026).
- Microsoft. Agent Framework. <https://github.com/microsoft/agent-framework> (acesso em
  02/11/2026).
- GitHub. Spec Kit. <https://github.com/github/spec-kit> (acesso em 02/11/2026).
- Agent2Agent (A2A) Protocol. <https://a2a-protocol.org> (acesso em 02/11/2026).
