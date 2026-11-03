# 13 — Observabilidade e economia

> "Um *start* sem *stop* é trabalho pago que não foi entregue. Nunca é completado por inferência."
> — limites declarados do livro de ponto de tarefas, Maestro

Quando um agente escreve o código, a conta chega de outro jeito: não em horas de gente, mas em
tokens, em tentativas e em espera humana. Quem rege agentes descobre cedo que sabe quanto gastou
no mês e não sabe quanto custou a coisa que entregou, nem quanto desse dinheiro foi para refazer
o que saiu errado. Este capítulo trata de medir sem cair nas duas armadilhas vizinhas: o painel
que ninguém consulta e o rastreamento que guarda tudo. O argumento é que a unidade certa é a
**tarefa aceita**, e que só um registro só-acréscimo, gravado no momento em que as coisas
acontecem, consegue respondê-la.

## Pergunta central

Quanto custa uma tarefa aceita, e onde o custo se perde entre o primeiro pedido e a aprovação
independente?

## Resultado de aprendizagem

Ao final, você consegue:

1. **Calcular** o custo por tarefa aceita a partir de um registro de eventos, separando-o do
   custo por tarefa executada e explicando por que os dois números divergem.
2. **Medir** retrabalho de duas formas, por tentativa e por linhagem, e mostrar com dados do seu
   próprio time qual delas esconde o custo.
3. **Ler** as métricas de entrega do DevOps Research and Assessment (DORA) aos pares, no próprio
   repositório, sem instrumentar painel, e decidir quando um painel passa a se pagar.
4. **Projetar** o registro de custo no formato do OpenTelemetry (OTel) com uma lista de permissão
   de campos, de modo que o conteúdo das mensagens nunca saia, e provar essa minimização com um
   portão que reprova quando o filtro é removido.
5. **Declarar** um teto de consumo com quem avisa ao cruzá-lo, distinguindo aviso de corte.

## A falha real

Em 26 de outubro de 2026, a sessão regente do Maestro conduzia o ciclo 073, que desenhava a área
administrativa do painel. A rodada de juízes daquele ciclo (seis execuções em contexto fresco,
das quais três se perderam por falha de rede) levou o consumo semanal da sessão a 39 %. O teto
combinado para o dia era 40 %. O humano responsável, o Darú, subiu o teto para 60 % ("Podemos ir
até 60% hoje"), e a segunda rodada de julgamento foi refeita com subagentes da própria regente
em vez de sessões trabalhadoras no *gateway* [CLAIM-13-001]. A decisão foi razoável e ficou
registrada como deve: uma linha no índice de decisões, com data, motivo e consequência.

O que chama atenção é a unidade em que ela foi tomada. "39 % do semanal" é o medidor do
fornecedor do modelo, uma barra de uso da conta. Ele diz quanto saiu do bolso, mas não diz
**por quê**: quanto foi julgamento útil, quanto foi execução perdida pela rede, quanto foi
retrabalho de uma rodada anterior. E o método tinha, desde 12 de outubro, um instrumento feito
exatamente para responder a isso.

Duas semanas antes, no ciclo 065, o Maestro tinha ganhado um **livro de ponto de tarefas**
(*task ledger*): um arquivo JSON Lines (JSONL, um objeto JavaScript Object Notation por linha),
só-acréscimo, em que cada tarefa entregue por uma sessão gerente a uma sessão trabalhadora
grava um evento de atribuição, um de início, um de fim (com tokens e custo em dólares) e, quando
alguém a audita, um veredito. Na versão `19823c2` do repositório, esse arquivo tem 52 linhas, e
todas são de 12 de outubro; ele foi tocado por um único commit [CLAIM-13-002]. Depois dele vieram
doze diretórios de especificação, do 066 ao 076 [CLAIM-13-003], e nenhum evento novo. O
componente que grava o livro é um *mod* do Claude Code instalado à parte, por um comando que o
instalador do método imprime e não executa; nas configurações do próprio repositório na versão
citada, nenhum plugin está habilitado [CLAIM-13-004].

A história anterior explica como se chegou ali, e ela é mais interessante do que um esquecimento.
Em 31 de julho, o Maestro avaliou a ideia de uma "trilha de auditoria com custo por invocação",
vinda de um repositório irmão, e deu o veredito **observar**, com um gatilho escrito: reavaliar
quando "alguém precisar responder 'quanto custou este ciclo?' com número, e não com estimativa".
Na dimensão "dor real hoje", a resposta registrada foi "não: ninguém pediu o número"
[CLAIM-13-005]. Em 14 de agosto, um documento de comparação do fluxo do Maestro com o de outro
time listou a lacuna sem rodeio: "aprendizados sim, métricas não". A retrospectiva e o índice de
decisões existiam; métrica, nenhuma. O modelo operacional classificava o *metrics dashboard* como
"depois, YAGNI" (*You Aren't Gonna Need It*, você não vai precisar disso), e o passo de
fechamento do ciclo terminava "com narrativa e sem número" — por escolha declarada, não por
descuido [CLAIM-13-006].

O gatilho disparou em 12 de outubro, com a frase do próprio humano: "Quero ver quanto estou
gastando" [CLAIM-13-007]. O livro de ponto nasceu naquele dia, foi revisado, reprovado,
corrigido, aprovado — e mediu um único ciclo. A falha, portanto, não é a falta de instrumento. É
de três camadas, cada uma com uma lição:

1. **O instrumento não tinha consumidor obrigatório.** Nada no fluxo dependia do livro de ponto;
   quando a instalação não acompanhou as sessões seguintes, nada ficou vermelho. É o teorema T5 do
   Maestro em ação: um artefato só sobrevive se algo o consome e falha alto quando ele envelhece.
2. **A decisão de custo foi tomada na unidade errada.** Percentual da conta mede o gasto, não o
   desperdício. Para saber se a rodada de juízes valia o preço, seria preciso o custo por
   veredito válido e o custo das execuções perdidas.
3. **O único ciclo medido já mostrava onde o custo se perde** — e é dele que tiramos a maior parte
   dos números deste capítulo. Lá, como se verá, quase metade do dinheiro foi retrabalho, e a
   métrica de retrabalho que o próprio relatório oferecia enxergava pouco mais de 2 % disso
   [CLAIM-13-012].

## Teoria

### O que ficou caro

O axioma A5 do Maestro diz que o custo é assimétrico entre fazer e desfazer: produzir é barato e
fica mais barato; desfazer não. O [capítulo 1](../01-a-mudanca-de-unidade-de-trabalho/capitulo.md)
tirou daí a consequência econômica principal: quando gerar código custa pouco, o que fica caro é
**verificar** e **refazer**. Este capítulo põe preço nessa frase. Se gerar é barato, o custo
relevante de uma tarefa não é o do primeiro rascunho, e sim o do caminho inteiro até alguém
independente aceitá-la — incluindo as tentativas reprovadas, as revisões e o que se perdeu no
meio.

Daí a unidade proposta: **custo por tarefa aceita**. A definição é simples e tem duas partes
que importam:

- **no numerador**, todo o custo do período ou do ciclo: tentativas entregues, bloqueadas,
  interrompidas, as que foram reprovadas e as próprias revisões;
- **no denominador**, só as tarefas cujo último veredito, dado por quem **não** as executou, é de
  aprovação.

A segunda parte é o que separa a métrica de uma média de gasto. "Custo por tarefa executada"
divide o gasto pelo esforço; "custo por tarefa aceita" divide pelo resultado. Num exemplo
pequeno, com três tarefas, uma delas reprovada duas vezes e nunca aceita, a primeira dá
US$ 1,43 e a segunda, US$ 2,15 [CLAIM-13-015]. A diferença é exatamente o preço do que não
chegou: tudo o que foi pago e não foi aprovado é carregado pelas tarefas que foram. É o número
que um tech lead deveria querer ver, porque é o que se compara com o valor de uma entrega.

### Onde o custo se perde

A agenda de pesquisa deste livro lista dez métricas para o trabalho com agentes, além das do
DORA [CLAIM-13-035]. Cinco delas
servem diretamente a este capítulo, e cada uma responde a uma pergunta diferente:

| Métrica | Pergunta | Armadilha |
|---|---|---|
| custo por tarefa aceita | quanto paguei por resultado? | contar veredito de quem executou |
| custo do retrabalho | quanto paguei para refazer? | definir retrabalho só como "tentativa 2" |
| tokens por tarefa | quanto contexto cada tarefa consumiu? | somar *cache* com texto novo |
| tempo de ciclo | quanto demorou do pedido à aceitação? | parar o relógio no "pronto" do autor |
| retrabalho (taxa) | que fração do trabalho foi refeita? | medir por contagem, sem peso de custo |

As outras cinco — espera humana, sobrecarga de coordenação, aceitação na primeira passada,
escape de gate e rendimento da revisão independente — são tratadas nos capítulos sobre o limite
humano ([3](../03-um-humano-muitos-agentes/capitulo.md)), divisão do trabalho
([6](../06-como-dividir-o-trabalho/capitulo.md)) e portões
([10](../10-quality-gates-que-provam-fatos/capitulo.md)). Aqui elas aparecem só quando cruzam o
custo.

Três observações valem para todas.

**Retrabalho tem duas definições, e elas dão números muito diferentes.** A definição mecânica é
"tentativa com número maior ou igual a dois": a mesma tarefa, refeita. A definição por
**linhagem** é "tudo o que começou depois da primeira reprovação e antes da aceitação". A
primeira é fácil de medir e quase sempre subestima: quando uma revisão reprova um ciclo inteiro,
o conserto não vem como "tentativa 2" das tarefas originais, vem como tarefas novas, com nomes
novos ("corrigir achado 5"), mais uma revisão nova. No único ciclo medido do Maestro, a primeira
definição achou US$ 0,13 de retrabalho; a segunda, US$ 5,75, ou 46,5 % do custo do ciclo
[CLAIM-13-012]. Não é erro de arredondamento: é a diferença entre olhar a árvore e olhar a
floresta.

**Tokens sem peso enganam.** Agentes que trabalham em sessões longas releem o mesmo contexto a
cada requisição, e os fornecedores cobram essa releitura (o *cache* de prompt) por uma fração do
preço do texto novo. No ciclo medido, a taxa de leitura de *cache* foi de 96,7 % da entrada; a
média por tentativa foi de 2,27 milhões de tokens no total e de 19 mil tokens de entrada e saída
novas [CLAIM-13-010]. "Tokens por tarefa" sem separar as duas coisas é um número de duas ordens
de grandeza de folga. Por isso o registro precisa guardar as categorias separadas, e o custo em
dinheiro tem de vir de quem cobra, não de uma tabela de preços aplicada depois.

**O custo mede por tentativa, não por modelo.** Uma sessão pode usar mais de um modelo dentro da
mesma tarefa (o principal e um subagente, por exemplo), mas o relatório de uso dá um valor em
dólar para a sessão inteira. Dividir esse valor entre os modelos por proporção de tokens é
inventar número. O relatório do Maestro mostra os tokens por modelo e põe um travessão na coluna
de custo por modelo, com a explicação ao lado [CLAIM-13-029]. Essa recusa é parte da teoria: a
métrica que não pode ser medida é declarada ausente, nunca estimada em silêncio.

### Por que DORA continua valendo, e onde ela para

O programa DORA mediu o desempenho de entrega de software de um grande número de equipes e
chegou a métricas que só informam **aos pares**: duas de vazão (frequência de
entrega e tempo de mudança, o *lead time*) e duas de estabilidade (taxa de falha de mudança e
tempo de recuperação). O guia atual do DORA acrescenta uma quinta, a taxa de retrabalho de
implantação (*deployment rework rate*), ao lado da taxa de falha, no grupo de instabilidade
[CLAIM-13-025]. A leitura em pares é o que impede o erro clássico: vazão sozinha premia atropelo;
estabilidade sozinha premia paralisia.

A segunda lição do DORA é mais útil ainda: as métricas são **resultado**, não alavanca. Ninguém
"faz" *lead time*; ele cai quando muda o que o produz — integração contínua, desenvolvimento em
tronco único, testes automatizados, revisão, entregas pequenas. Cobrar o número sem mexer na
capacidade é cobrar o termômetro pela febre. E a alavanca que move as cinco ao mesmo tempo é o
tamanho do lote: mudança pequena chega mais vezes, atravessa mais rápido, é mais fácil de testar
e, quando falha, é mais fácil de desfazer.

O relatório de 2025 do DORA, *State of AI-assisted Software Development*, tem como achado
central que a inteligência artificial (IA) funciona como amplificador: intensifica as forças e
as fraquezas que a organização já tinha [CLAIM-13-032]. Para quem rege agentes, isso se traduz
assim: um time de lote grande e portão fraco, com agentes, produz mais lote grande e mais escape.
As métricas DORA continuam sendo a bússola da entrega.

Onde elas param é na economia da tarefa. DORA mede o fluxo de mudanças até produção; não mede o
que cada mudança custou para ser produzida, nem quantas vezes foi refeita antes de chegar ao
tronco. Com humanos, isso estava escondido na folha de pagamento, que é um custo fixo. Com
agentes, o custo é variável, por requisição, e aparece na fatura do mês seguinte. A quinta
métrica do DORA olha o retrabalho **depois** da implantação; o custo por tarefa aceita olha o
retrabalho **antes** dela. As duas se complementam.

### Observabilidade como projeção, e o limite da privacidade

Para medir isso, alguém tem de registrar. Aqui a teoria encontra o segundo teorema de que o
capítulo deriva, o T7 do Maestro: onde a saída não é comparável por igualdade, o critério é uma
**linha de base registrada**, com entrada fixa e observação datada. Custo de agente não é
comparável entre dias por igualdade — o mesmo pedido custa diferente em duas execuções. O que
torna o número utilizável é ele estar num registro imutável, com data, e ser lido sempre da
mesma forma. Um painel que recalcula de uma fonte mutável não serve de linha de base; um arquivo
só-acréscimo serve.

A segunda metade é o formato. O OpenTelemetry é o padrão aberto de rastreamento distribuído:
um *trace* é uma operação de ponta a ponta, um *span* é um trecho com início e fim, e os dois
carregam atributos com nomes convencionados. Existe um conjunto de convenções semânticas para IA
generativa (GenAI), com nomes como `gen_ai.request.model`, `gen_ai.usage.input_tokens` e
`gen_ai.usage.output_tokens` — ainda marcadas como em desenvolvimento. Adotar os **nomes** custa
quase nada e evita migração depois; adotar a **infraestrutura** (coletor, exportador, *backend*)
antes de haver quem consuma é o painel prematuro com outro nome.

E há o limite que não é técnico. Rastreamento de agente, feito sem cuidado, grava o conteúdo
inteiro de cada mensagem: código do cliente, dados pessoais colados num *prompt*, segredos lidos
de um arquivo. A Lei Geral de Proteção de Dados Pessoais (LGPD), no Brasil, põe entre os seus
princípios o da **necessidade**: o tratamento se limita ao mínimo necessário para a finalidade.
Se a finalidade é saber quanto custou uma tarefa, o mínimo necessário são contagens, identificadores
de tarefa e vereditos — não o texto. A regra que a agenda de pesquisa deste livro adota resume:
*tracing* não é retenção indiscriminada. Minimização não é um filtro aplicado no fim; é uma lista
de permissão aplicada na gravação e de novo na exportação.

O cenário regulatório reforça a prudência. A Autoridade Nacional de Proteção de Dados (ANPD), que
fiscaliza a LGPD, tratou inteligência artificial como frente própria e propôs um *sandbox*
regulatório — um ambiente supervisionado de experimentação — para IA e proteção de dados. A
mensagem para o tech lead é que as regras sobre dados pessoais em sistemas de IA ainda estão sendo
assentadas no país; enquanto isso, o desenho que não guarda conteúdo é o que não precisa ser
refeito quando elas assentarem. A agenda de pesquisa deste livro põe LGPD e ANPD na lista de
riscos, ao lado do OWASP (*Open Worldwide Application Security Project*) GenAI Top 10 e do regulamento europeu de IA (*AI Act*), que o
[capítulo 12](../12-ferramentas-mcp-e-o-ecossistema/capitulo.md) discute.

## Alternativas

Há pelo menos quatro famílias de resposta ao "quanto custa", e elas não são excludentes.

**O medidor do fornecedor.** Toda plataforma de modelo tem um painel de uso: tokens, dólares,
percentual do limite. É de graça, é exato no que mede e é o que o Maestro usou na decisão de 26
de outubro. O defeito é a unidade: mede a conta, não a tarefa. Não sabe o que é uma revisão, uma
reprovação, uma tentativa. **Veredito**: necessário como total de controle, insuficiente como
métrica de engenharia. Use-o para conferir que a soma do seu registro bate com a fatura.

**Plataformas de observabilidade de LLM** (*large language model*, modelo de linguagem de grande
porte). Ferramentas como Langfuse, LangSmith, Arize Phoenix, Helicone e a instrumentação
OpenLLMetry registram cada chamada ao modelo como um *span*, com tokens, latência e custo
estimado, e várias delas falam OpenTelemetry. São boas para depurar uma cadeia de chamadas e para
avaliar respostas. Duas ressalvas para o tech lead: por padrão, a maioria captura o **conteúdo**
dos *prompts* e respostas, o que precisa ser desligado ou contratado com cuidado; e a unidade
nativa delas é a chamada ou a sessão, não a tarefa com veredito independente. **Veredito**:
adote quando houver um consumidor real do rastreamento detalhado (depurar um agente em produção,
por exemplo), configure a minimização antes do primeiro dado, e traga para elas a noção de
tarefa e de veredito — não espere que elas a tenham.

**Frameworks de produtividade.** O DORA (cinco métricas de entrega), o SPACE (satisfação,
desempenho, atividade, comunicação e eficiência — um lembrete de que não existe métrica única) e
o DX Core 4 (velocidade, efetividade, qualidade e impacto, prescritivo). Medem o time, não a
tarefa. O risco do terceiro é o mesmo de toda métrica prescritiva: "*pull requests* por pessoa" mede
digitação, não valor, e com agentes mede ainda menos. **Veredito**: DORA como bússola, lida no
repositório; SPACE como referência; métricas de atividade, nunca como meta.

**FinOps** (*financial operations*, a disciplina de gestão financeira de nuvem). Traz a ideia de
**custo unitário**: custo dividido por uma unidade de negócio, em vez de custo total. É
exatamente o movimento deste capítulo, aplicado a agentes: a unidade de negócio do time de
engenharia é a tarefa aceita. **Veredito**: adote o raciocínio; a ferramenta de FinOps entra
quando o gasto com agentes for linha relevante do orçamento de nuvem.

O que nenhuma dessas alternativas faz sozinha é **amarrar o custo ao veredito de quem não
executou**. É essa amarração que transforma gasto em economia de engenharia, e ela depende de um
protocolo entre quem distribui e quem entrega o trabalho — que é o que o padrão a seguir
descreve.

## O padrão Maestro

O Maestro chegou ao seu padrão em camadas, e cada camada tem uma natureza diferente: regra
escrita, script ou gancho (*hook*) do *harness*. Vale separar, porque só as duas últimas se
cobram sozinhas.

### Primeiro, não medir — e escrever por quê

A posição inicial foi deliberada. O capítulo do handbook sobre DORA, migrado no ciclo 022 em
agosto, leu as quatro métricas da época **do próprio repositório, sem instrumentar nada**: a
especificação daquele ciclo exigia trazer "a métrica em que vamos mal" [CLAIM-13-033]. O retrato:

- **Frequência de entrega**: 17 promoções para a linha principal em três dias (4 em 31/07, 9 em
  01/08, 4 em 02/08), contadas no índice de decisões, porque o script de promoção grava cada gate
  [CLAIM-13-016]. Na versão `19823c2`, são 50 promoções registradas, de 31 de julho a 21 de
  outubro [CLAIM-13-017].
- **Tempo de mudança**: cada ciclo entrava na linha principal num único commit, no mesmo dia em
  que abria.
- **Taxa de falha** — a ruim: nove defeitos escaparam para a linha principal nas 17 promoções,
  todos com a verificação verde, e nenhum foi pego por revisão: todos apareceram quando alguém
  escreveu um check [CLAIM-13-019].
- **Tempo de recuperação**: nenhuma reversão no histórico; todo defeito foi corrigido avançando
  no ciclo seguinte [CLAIM-13-018].

A leitura foi: vazão de elite, estabilidade medíocre, e a resposta **não** é entregar mais
devagar, é atacar a capacidade que falta (portões que provam fatos). A regra que saiu dali é das
que este capítulo recomenda manter: **DORA é bússola, não painel**. E a decisão de não
instrumentar foi registrada com a condição de reabertura, em vez de esquecida. Essa é a parte
que o leitor deve copiar: YAGNI com gatilho escrito é governança; YAGNI sem gatilho é preguiça.

### Depois, o livro de ponto (regra + script + mod)

Quando o gatilho disparou, o ciclo 065 construiu o livro de ponto. A especificação está em
<https://github.com/GHDaru/maestro/blob/19823c2/specs/065-o-metodo-se-cobra-e-bate-o-ponto/spec.md>,
a decisão no ADR (*Architecture Decision Record*, registro de decisão de arquitetura) 0021 e o
protocolo em <https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/task-ledger.md>.
Um detalhe do registro histórico mostra a disciplina do só-acréscimo: o ciclo foi renumerado de
064 para 065 ao entrar na branch de desenvolvimento, mas os eventos já gravados continuaram com
`cycle: "064"` — corrigir o rótulo seria reescrever a história.

As peças:

- **A regra** (documento de governança): quem distribui uma tarefa escreve, sozinha numa linha,
  uma etiqueta `[[TASK id=... kind=... attempt=... cycle=...]]`; quem entrega termina com
  `[[DONE id=... outcome=...]]`. Uma auditoria nomeia a tarefa julgada (`target`) e o veredito.
  Os vocabulários são fechados: nove tipos de tarefa (de `spec` a `research`), três desfechos que
  a sessão declara (`delivered`, `blocked`, `failed`) e dois que o próprio mod escreve
  (`interrupted`, `superseded`) [CLAIM-13-034].
- **O script gravador** (`scripts/record-task.py`): valida cada linha contra os vocabulários e a
  acrescenta ao arquivo. O limite está declarado na própria documentação: no Linux e no macOS, a
  escrita em modo de acréscimo manteve 30 linhas simultâneas de cerca de 2 KB intactas; no
  Windows, o modo de acréscimo do Python não é atômico entre processos, e a recomendação é um
  escritor por vez ou aceitar uma linha danificada, que o relatório conta como inválida em vez de
  quebrar [CLAIM-13-022].
- **O mod** (`maestro-ledger`): um plugin que roda dentro do processo do *harness*, lê as
  etiquetas, soma os tokens de cada requisição ao modelo e grava os eventos. Ele **impõe** a
  revisão independente: um veredito só é gravado se a tarefa ativa for de tipo `audit` ou
  `review`. É instalado à parte, por comando do usuário, nunca pelo instalador do método.
- **O script de relatório** (`scripts/report-tasks.py`): deriva tudo na leitura — custo e tokens
  por tipo, por ciclo e por modelo; aprovação na primeira passada; custo de retrabalho
  (tentativa ≥ 2); taxa de *cache*; e **órfãos**, tarefas com início e sem fim. Nenhuma métrica
  é gravada; uma métrica nova nunca exige migração.
- **O portão** (`scripts/check-ledger.sh`): testa gravador, relatório e ganchos em *fixtures*
  escritas num diretório temporário, com os números esperados calculados à mão nos comentários,
  e roda as mutações numa cópia — o que o [capítulo 10](../10-quality-gates-que-provam-fatos/capitulo.md)
  chama de provar o portão vendo-o falhar.

O desenho tem três decisões que valem fora do Maestro.

**Tentativa, desfecho e veredito são três coisas.** Tentativa é quantas vezes se tentou;
desfecho é se a sessão conseguiu fazer; veredito é se o trabalho foi aceito — e o veredito
**nunca** vem de quem executou. O relatório também confere na leitura: só conta veredito cujo
autor é uma tarefa de auditoria do próprio livro **e** cuja sessão é a que executou essa
auditoria.

**Órfão é visível, nunca inferido.** Se a sessão cai no meio de uma tarefa, o livro mostra um
início sem fim. O relatório não fecha a tarefa por suposição.

**Custo ausente não é zero.** Uma parada sem tokens é "não medida", contada à parte.

### O que o único ciclo medido mostrou

Rodando o relatório no livro da versão `19823c2` (é o mesmo arquivo que o exemplo deste capítulo
usa), o ciclo 064/065 aparece assim:

- **US$ 12,36** em 13 tentativas medidas, das quais as duas revisões independentes custaram
  US$ 6,34, ou 51,3 % do total [CLAIM-13-008]. As revisões rodaram num modelo maior, com 12,1
  milhões de tokens em duas tentativas; as onze tentativas de implementação, correção e
  documentação, num modelo menor, somaram 17,4 milhões [CLAIM-13-029].
- **Três tentativas sem medida**. As notas do próprio livro explicam: foram executadas pela
  sessão gerente, que não tinha o mod carregado, porque o *sandbox* das trabalhadoras protegia
  os arquivos do mod [CLAIM-13-009]. O ponto cego do instrumento era exatamente o trabalho que o
  gerente fez com as próprias mãos.
- **Aprovação na primeira passada: não calculável.** Cinco vereditos foram descartados pelo
  relatório: quatro dados pela sessão gerente sobre tarefas de implementação e documentação e um espelho de
  veredito gravado na sessão errada [CLAIM-13-011]. O gerente reexecutou as provas e aprovou —
  mas gerente não é revisor independente, e a métrica se recusou a contar. Ficou só o veredito do
  ciclo inteiro: reprovado pela primeira revisão, aprovado com ressalvas pela segunda.
- **Retrabalho**: US$ 0,13 pela definição de tentativa; US$ 5,75 pela de linhagem, 46,5 % do
  ciclo [CLAIM-13-012]. Quase metade do dinheiro foi gasto entre a primeira reprovação e a
  aceitação.
- **Tempo de ciclo**: 42,9 minutos do primeiro evento à aceitação [CLAIM-13-013].

Para o tech lead, a leitura é esta: o custo de um ciclo com revisão independente séria é
dominado por **verificar e refazer**, não por escrever. Isso é o axioma A5 com números. E é por
isso que a métrica de produtividade que conta linhas ou tarefas executadas engana: o ciclo
produziu doze tarefas executadas a US$ 1,03 cada, uma média que não diz nada sobre o que foi
aceito [CLAIM-13-014].

### Custo por sessão, consumo por agente e teto

O livro de ponto mede por tarefa, se as sessões usarem as etiquetas. Os ciclos seguintes
atacaram o problema por outro lado, pelo painel de coordenação (ADR 0022), que é uma projeção
dos arquivos do repositório num banco SQLite local, reconstruível a cada leitura:

- **Custo por sessão** (ciclo 068): o painel lê de forma incremental os transcritos das sessões
  e soma tokens por sessão e por minuto. Com dezesseis sessões abertas, "quanto custou este
  chamado" era pergunta diária sem resposta; o painel passou a mostrar o custo de cada passo
  **como estimativa rotulada**, porque a sessão pode ter feito outra coisa na mesma janela
  [CLAIM-13-027].
- **Privacidade por construção**: a decisão D4 do ciclo 066, registrada em 20 de outubro, aceitou
  o leitor de custo porque ele grava **só contagens de tokens**, título e caminho da sessão num
  banco local ignorado pelo controle de versão, e nada disso chega ao servidor HTTP (*Hypertext
  Transfer Protocol*). A mesma decisão registrou duas dívidas com dono: o filtro de pasta por
  substring em vez de igualdade e um valor padrão que apontava para um projeto real
  [CLAIM-13-020].
- **Consumo por agente** (ciclo 073): o grão desceu de sessão e modelo para **agente**.
- **Limite de orçamento** (ciclo 073): o teto de consumo deixou de ser um número declarado e
  passou a ser lido como **declarar o teto e avisar**. O emissor do aviso é a ingestão de uso do
  painel: ao cruzar o limiar, ela enfileira uma mensagem para a sessão dona e para a regente —
  "aviso tardio, nunca perdido". O **corte** (recusar, suspender) fica para depois. Na versão
  citada, isso está desenhado no protótipo da área administrativa; o leitor de custo mede, e o
  emissor ainda não é código.

O modelo operacional registra a reviravolta: o painel de coordenação é "essencial desde o ciclo
066" e, na mesma linha, a tabela lembra que o item "era *metrics dashboard*, depois/YAGNI"
[CLAIM-13-031]. E o ADR do painel traz duas regras anti-autoengano que valem para qualquer
métrica: DORA conta **implantação registrada, nunca merge** (o merge aparece só como
aproximação rotulada), e quando não há dado o painel mostra "—" em vez de inventar número
[CLAIM-13-030].

### OpenTelemetry como projeção (ADR 0033)

Em 29 de outubro, o ADR 0033 fechou a questão do formato: **OpenTelemetry é projeção do log, não
dependência** [CLAIM-13-021]. Agora, só os nomes dos campos de custo seguem as convenções GenAI,
para o dado nascer no formato certo. O exportador pelo OpenTelemetry Protocol (OTLP) entra só
com o primeiro consumidor real, e a tradução está fixada: *trace* é o chamado, *span* é a
execução, eventos são as transições — **nunca o conteúdo da mensagem**. Os identificadores já
são compatíveis com `trace_id` e `span_id`. Desfazer é desligar o exportador; nada no domínio
depende dele, que é a razão de ele ser projeção.

Em resumo, o que é regra, script e gancho no padrão:

| Peça | Natureza | Se cobra sozinha? |
|---|---|---|
| "DORA é bússola, não painel"; YAGNI com gatilho | regra escrita | não |
| protocolo `[[TASK]]`/`[[DONE]]` | regra escrita | só onde o mod está instalado |
| gravador e relatório do livro de ponto | script | o relatório sim, ao ser lido |
| veredito só de `audit`/`review` | mod + script | sim, nos dois lados |
| custo por sessão, só contagens | script do painel | sim |
| aviso ao cruzar o teto | desenho | ainda não |
| OTel como projeção | ADR | não há o que cobrar até haver exportador |

A falha real deste capítulo mora na segunda linha: o protocolo era regra e só se cobrava onde o
mod estava instalado. Onde não estava, não houve vermelho nenhum.

## Exemplo executável

O exemplo está em [`exemplo/`](exemplo/README.md). São dois scripts em Python 3 com biblioteca
padrão e dois livros de ponto:

- `tarefas-064.jsonl` — cópia byte a byte do livro do Maestro na versão `19823c2` (o *hash* está
  no README do exemplo);
- `sintetico.jsonl` — um livro pequeno, de três tarefas, com números redondos, para conferir a
  conta à mão.

`economia.py` deriva, na leitura, as métricas da seção "Teoria": custo por tipo de tarefa, tokens
com e sem *cache*, vereditos válidos e descartados, custo por tarefa aceita contra o custo
ingênuo por tarefa executada, retrabalho pelas duas definições, tempo de ciclo e órfãos. No livro
do Maestro, ele reproduz os números do relatório oficial (US$ 12,3561, 96,7 % de *cache*,
US$ 0,1312 de retrabalho por tentativa) e acrescenta o que o relatório não mostra: os US$ 5,7457
de retrabalho por linhagem. No livro sintético, mostra o custo por tarefa aceita funcionando:
US$ 2,15 contra US$ 1,43 ingênuos, com o veredito de aprovação dado pelo gerente descartado
[CLAIM-13-015].

`projetar_otel.py` projeta o mesmo livro em *spans* no formato de dados do OpenTelemetry, com
nomes `gen_ai.*` para uso de modelo, sem coletor e sem biblioteca. A minimização é uma lista de
permissão: no livro do Maestro, os 52 eventos viram 19 *spans*, e ficam para trás, entre outros,
7 textos livres de motivo de veredito, 7 notas e 52 identificadores de sessão [CLAIM-13-023]. O
script termina com um portão que procura qualquer atributo fora da lista. Com a opção
`--sem-filtro`, que remove a lista de propósito, o portão reprova e o script sai com código 1
[CLAIM-13-024] — é a mutação que prova que a minimização é verificada, e não prometida.

Rode os dois antes de seguir; a saída esperada completa está no README.

## Contraexemplo

**Quando não medir.** O Maestro passou de julho a outubro sem métrica de custo, e isso estava
certo. Um time pequeno, com gasto de agentes irrelevante perto da folha, sem decisão que dependa
do número, não precisa de livro de ponto. Instrumentar sem pergunta é o anti-padrão "painel sem
decisão associada" — cerimônia em papel. O critério para começar é o da ideia 029: alguém
precisa responder "quanto custou?" com número, para tomar uma decisão. Antes disso, leia DORA no
repositório e escreva o gatilho.

**Quando a métrica vira meta.** A lei de Goodhart vale em dobro com agentes, porque agentes
otimizam o que se mede com uma diligência que nenhum humano tem. Três exemplos concretos do que
dá errado:

- **custo por tarefa aceita como meta** premia quem pula a revisão independente — ela custou
  mais da metade do ciclo medido. O número cai, a qualidade cai junto;
- **tokens por tarefa como meta** premia o agente que lê menos contexto do que precisa, que é
  exatamente o erro que o [capítulo 5](../05-engenharia-de-contexto/capitulo.md) combate;
- **taxa de *cache* como meta** premia sessões longas e acumuladas, contra o reinício de
  contexto que mantém o agente estreito.

A regra é a mesma do DORA: olhe a tendência, ataque a capacidade, nunca cobre o número.

**Quando o protocolo custa mais do que mede.** Etiquetas exigem disciplina de quem distribui o
trabalho. O próprio documento do protocolo lista onde ele não chega: sessões na nuvem e sessões
no subsistema Linux do Windows não carregam o mod; recarregar o mod perde a tarefa ativa;
sessões aninhadas repetem identificadores; e o rótulo do juiz não é autenticado. Num time em que
metade das sessões cai num desses casos, o livro vai mostrar uma fração do gasto com cara de
total. Pior que não ter número é ter um número parcial sem rótulo de parcial. Se o seu ambiente
é assim, prefira o custo por sessão lido dos transcritos — mais grosso, mas completo — e rotule
como estimativa.

**Quando a minimização atrapalha a depuração.** Sem o conteúdo, não se depura por que um agente
gastou 6 milhões de tokens numa revisão. Para isso, o rastreamento detalhado tem lugar — local,
com retenção curta, com finalidade declarada, longe do registro de custo. O erro é misturar os
dois e reter tudo para sempre "porque pode ser útil".

**O custo do próprio instrumento.** O teste ao vivo do gancho de fim de resposta, no ciclo 065,
custou US$ 0,017 [CLAIM-13-026]; as tentativas medidas do ciclo inteiro que construiu o livro de
ponto somaram US$ 12,36 [CLAIM-13-008]. Não é caro.
O caro é o que a falha real mostrou: um instrumento sem consumidor obrigatório, que deixa de ser
alimentado sem que nada fique vermelho.

## Evidência

O que sustenta o capítulo, separado pelo estado de cada afirmação. A tabela completa, com a
evidência reproduzível de cada claim, está em [`claims.md`](claims.md).

**Medido** (reproduzível por comando na versão citada): o livro de ponto com 52 linhas de um só
dia e um só commit [CLAIM-13-002]; os doze diretórios de especificação sem evento no livro
[CLAIM-13-003]; a ausência de plugin habilitado nas configurações [CLAIM-13-004]; os números do
ciclo medido — custo total e por tipo, tokens por modelo, *cache*, vereditos descartados,
retrabalho pelas duas definições, tempo de ciclo, custo ingênuo [CLAIM-13-008, CLAIM-13-010 a
CLAIM-13-014, CLAIM-13-029]; o exemplo sintético [CLAIM-13-015]; a projeção e a sua mutação
[CLAIM-13-023, CLAIM-13-024]; as promoções e a ausência de reversões [CLAIM-13-016 a
CLAIM-13-018].

**Observado** (registrado em spec, ADR, índice de decisões ou documento do Maestro, ou em fonte
pública): a decisão do teto de 60 % [CLAIM-13-001]; a ideia 029 e o seu gatilho [CLAIM-13-005];
a lacuna "aprendizados sim, métricas não" [CLAIM-13-006]; a demanda que abriu o ciclo 065
[CLAIM-13-007]; as tentativas não medidas da sessão gerente [CLAIM-13-009]; os nove escapes
[CLAIM-13-019]; a decisão de privacidade do custo por sessão [CLAIM-13-020]; o ADR 0033
[CLAIM-13-021]; o limite do modo de acréscimo [CLAIM-13-022]; as métricas e o relatório de 2025
do DORA [CLAIM-13-025, CLAIM-13-032]; o custo do teste ao vivo [CLAIM-13-026]; o custo por
sessão como estimativa rotulada [CLAIM-13-027]; as regras do painel e do modelo operacional
[CLAIM-13-030, CLAIM-13-031]; a especificação do ciclo 022 [CLAIM-13-033]; os vocabulários fechados do protocolo [CLAIM-13-034]; a lista de métricas da agenda de pesquisa [CLAIM-13-035].

**Hipótese** (não medida; agenda da pesquisa). Duas hipóteses da base de pesquisa do livro
encostam neste capítulo [CLAIM-13-028]. A H3 diz que contexto seletivo reduz custo sem perder
qualidade; a taxa de *cache* de 96,7 % sugere que boa parte do custo de uma sessão longa é
releitura, mas não mostra que cortá-la preservaria a qualidade. A H9 diz que um modelo menor
basta em tarefa estruturada; o ciclo medido usou o modelo maior só nas revisões, o que é
coerente com a hipótese, mas um ciclo não é amostra. Os números do ciclo 064/065 são um estudo
de caso de **um** ciclo, de **um** operador, num dia; nenhum deles é estimativa de frequência,
e nenhuma comparação entre arranjos foi feita. O desenho que testaria H3 e H9 — linhas de base
com e sem cada prática, repetições, ambiente congelado — está no
[capítulo 15](../15-validando-o-maestro/capitulo.md).

Um limite honesto adicional: o livro de ponto do Maestro só funciona num *harness* (o Claude
Code) e com um mod. O argumento do capítulo não depende disso — etiquetas numa mensagem e um
arquivo só-acréscimo funcionam com qualquer ferramenta que deixe ler o uso de tokens —, mas a
evidência, por enquanto, vem de uma só.

## Checklist

Aplique no seu time, na ordem.

- [ ] O time sabe dizer **por que** quer o número de custo, e escreveu a decisão que ele vai
      informar. Sem isso, escreveu o gatilho de reavaliação e parou aqui.
- [ ] As métricas DORA são lidas aos pares, a partir do repositório (registro de promoções,
      *changelog*, histórico), e implantação registrada não é confundida com merge.
- [ ] Existe um registro **só-acréscimo** de tarefas com início, fim, tentativa, desfecho,
      tokens por categoria (entrada, saída, *cache* lido, *cache* gravado) e custo em dinheiro
      vindo de quem cobra.
- [ ] Tentativa, desfecho e veredito são campos diferentes, e o veredito só conta quando vem de
      quem não executou — conferido na gravação **e** na leitura.
- [ ] O relatório publica o **custo por tarefa aceita** ao lado do custo por tarefa executada.
- [ ] Retrabalho é medido também por **linhagem** (da primeira reprovação até a aceitação), e não
      só como "tentativa 2".
- [ ] Custo ausente aparece como "não medido", com a lista das tentativas; órfãos aparecem como
      órfãos; nenhum número é completado por inferência ou rateado entre modelos.
- [ ] O registro tem um **consumidor obrigatório** — um relatório que alguém lê no fechamento do
      ciclo, ou um portão que fica vermelho quando um ciclo fecha sem eventos.
- [ ] A soma do registro é conferida contra o painel do fornecedor; a diferença tem explicação.
- [ ] O que se grava sobre custo são **contagens e identificadores**, nunca o conteúdo das
      mensagens; a exportação usa lista de permissão, e um teste prova que removê-la reprova.
- [ ] Os nomes de campo seguem as convenções GenAI do OpenTelemetry; o exportador só existe
      quando há quem consuma.
- [ ] Rastreamento detalhado com conteúdo, se existir, é local, tem finalidade declarada e
      retenção curta.
- [ ] Há um teto de consumo declarado, com **quem avisa** ao cruzar o limiar; o corte automático
      é uma decisão separada, de risco próprio.
- [ ] Nenhuma dessas métricas é meta individual nem de agente.

## Referências

**Maestro** (versão `19823c2`, salvo indicação):

- Axiomas A5, teoremas T5 e T7 —
  https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/axioms.md
- Protocolo do livro de ponto (*task ledger*) —
  https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/task-ledger.md
- Livro de ponto — https://github.com/GHDaru/maestro/blob/19823c2/docs/records/tarefas.jsonl
- Gravador, relatório e portão —
  https://github.com/GHDaru/maestro/blob/19823c2/scripts/record-task.py ·
  https://github.com/GHDaru/maestro/blob/19823c2/scripts/report-tasks.py ·
  https://github.com/GHDaru/maestro/blob/19823c2/scripts/check-ledger.sh
- Spec do ciclo 065 —
  https://github.com/GHDaru/maestro/blob/19823c2/specs/065-o-metodo-se-cobra-e-bate-o-ponto/spec.md
- Spec do ciclo 022 —
  https://github.com/GHDaru/maestro/blob/19823c2/specs/022-capitulo-02-padrao-v2/spec.md
- Spec do ciclo 068 —
  https://github.com/GHDaru/maestro/blob/19823c2/specs/068-chamados-gate-a-gate/spec.md
- ADR 0021, ADR 0022, ADR 0033 —
  https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0021-o-metodo-se-cobra-e-bate-o-ponto.md ·
  https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0022-painel-de-coordenacao-como-projecao-dos-arquivos.md ·
  https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0033-opentelemetry-como-projecao-do-log.md
- Índice de decisões (`decisao-066-d4-custo-privacidade`, `decisao-073-teto-60`, `gate-main-*`) —
  https://github.com/GHDaru/maestro/blob/19823c2/docs/records/decisoes.jsonl
- Ideia 029, trilha de auditoria com custo —
  https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/ideias/029-trilha-de-auditoria-com-custo.md
- Glossário (custo por sessão, consumo por agente, limite de orçamento, emissor do aviso) —
  https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/glossary.md
- Modelo operacional, §6 e §10 —
  https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/operating-model.md
- Leitor de custo por sessão — https://github.com/GHDaru/maestro/blob/19823c2/painel/custo.py
- Handbook do método, capítulo 02 (DORA e SPACE), apêndice A §2, receita "instalar o Maestro" e
  diagrama 06 (cópia congelada em
  [`maestro-handbook/`](../../maestro-handbook/handbook/02-dora-space.md))

**Externas**:

- DORA, "DORA's software delivery performance metrics" — https://dora.dev/guides/dora-metrics/
  (acesso em 02/11/2026).
- DORA, *State of AI-assisted Software Development 2025* —
  https://dora.dev/research/2025/dora-report/ (acesso em 02/11/2026).
- N. Forsgren, J. Humble e G. Kim, *Accelerate: The Science of Lean Software and DevOps*, IT
  Revolution, 2018.
- N. Forsgren, M.-A. Storey, C. Maddila, T. Zimmermann, B. Houck e J. Butler, "The SPACE of
  Developer Productivity", *ACM Queue*, 2021.
- OpenTelemetry, convenções semânticas para IA generativa —
  https://opentelemetry.io/docs/specs/semconv/gen-ai/ (não reconsultada para esta versão; os
  nomes de atributo citados são os que a banca de arquitetura do ciclo 076 do Maestro registrou
  em `specs/076-padroes-de-engenharia-e-react/banca-arq/r3-arq3.md`).
- Brasil, Lei nº 13.709/2018 (Lei Geral de Proteção de Dados Pessoais), art. 6º, princípio da
  necessidade.
- Autoridade Nacional de Proteção de Dados (ANPD), iniciativa de *sandbox* regulatório em
  inteligência artificial e proteção de dados (não reconsultada para esta versão).
- C. A. E. Goodhart, "Problems of Monetary Management: The U.K. Experience", 1975 — a origem da
  lei de Goodhart.
