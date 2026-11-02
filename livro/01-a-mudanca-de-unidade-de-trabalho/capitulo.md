# 01 — A mudança de unidade de trabalho

> *Quando a máquina executa, o valor deixa de estar em digitar.*

Você passou a carreira otimizando a produção de código: estimativas em horas de
desenvolvimento, *pull requests* (PRs) por semana, velocidade por *sprint*. Agentes de
Inteligência Artificial (IA) derrubaram o preço dessa produção, e o instinto é comemorar ou
frear. Este capítulo propõe outra leitura: o custo não sumiu, mudou de lugar. Se você não
souber para onde ele foi, vai gerenciar o que ficou barato e deixar sem dono o que ficou
caro. É o capítulo que dá o vocabulário econômico para o resto do livro.

## Pergunta central

Se gerar código ficou barato, o que ficou caro?

## Resultado de aprendizagem

Ao final deste capítulo, você consegue:

1. **Decompor** o custo de uma mudança em gerar, verificar e desfazer, e dizer qual desses
   termos domina no seu time hoje.
2. **Definir** a nova unidade de trabalho, a *mudança aceita*, e distingui-la da mudança
   escrita, com um exemplo do seu repositório.
3. **Explicar** a um par, com o argumento do tamanho de lote, por que frear os agentes piora
   velocidade *e* estabilidade.
4. **Classificar** uma ação do seu fluxo pelo custo de desfazê-la, e decidir se ela pede gate
   humano ou só verificação automática.
5. **Rodar** o modelo do `exemplo/` com os parâmetros do seu time e ler onde está o piso de
   custo que gerar mais rápido não move.

## A falha real

Entre 26 de outubro e 1º de novembro de 2026, o ciclo 074 do Maestro — o método que este
livro usa como objeto de estudo — produziu um protótipo navegável do painel de regência: as
telas em que um humano acompanha e comanda várias sessões de agentes. Em sete dias, o ciclo
acumulou 303 commits [CLAIM-01-001]. Produzir não era o problema. Agentes trabalhando em
fatias paralelas geravam telas, módulos e correções num ritmo que nenhum time humano do
mesmo tamanho acompanharia.

A barra de qualidade era exigente de propósito. Cada peça do protótipo enfrentava um
*crítico às cegas*: um agente em contexto fresco, que não sabia qual versão era a nossa,
comparava o protótipo com um produto de referência e dizia qual era melhor e qual era a
maior lacuna. O laço continuava até a nossa versão vencer. Ao todo, o *gauntlet* do 074
registrou onze críticas desse tipo [CLAIM-01-004].

A peça P3, a tela de Andares, perdeu quatro rodadas seguidas [CLAIM-01-002]. A crítica da
quarta rodada, de 29 de outubro, abre com um veredito que todo tech lead já ouviu de um
usuário: o protótipo «mente depois de agir». Pousar um andar não o tirava da contagem; dois
avisos diziam que algo tinha acontecido quando nada tinha acontecido; e os contadores de
duas telas, que começavam iguais (4 = 4), divergiam a cada decisão (3 × 4, depois 4 × 5),
para sempre [CLAIM-01-003].

O detalhe que transforma o episódio em falha de método, e não de tela, está na decisão
registrada naquele mesmo dia: da terceira rodada em diante, a lacuna **deixou de ser
layout** e passou a ser coerência de estado entre telas [CLAIM-01-002]. Cada tela lia sua
própria fixture; não existia um estado único que todas consultassem. Nenhuma quantidade de
polimento no HTML (*HyperText Markup Language*) resolveria isso, porque o defeito não estava
no que cada rodada produzia. Estava fora da unidade em que o trabalho era cortado.

Gerar uma nova versão da tela custava pouco. Cada rodada, porém, consumia uma crítica
independente, uma leitura do humano e mais um ciclo de integração. O que era caro era
verificar, e era decidir que a pergunta estava errada. O laço gastava o recurso caro para
refinar o barato.

No dia seguinte, 30 de outubro, um segundo crítico — o que «anda» pelo protótipo como um
usuário — reprovou o fecho do ciclo: seis jornadas falharam, com uma causa única, telas e
avisos que afirmavam efeitos que o estado não tinha registrado [CLAIM-01-005]. A essa
altura, uma única fatia do ciclo já tinha declarado um piso de cerca de 20,24 milhões de
*tokens* consumidos [CLAIM-01-006]. Barato não é grátis; é só muito menos caro do que o
resto.

O desfecho veio em 1º de novembro, às 15h40. O responsável humano pelo projeto, o Darú, fez
o *corte da v1* [CLAIM-01-007]. O crítico às cegas saiu do caminho de cada fatia: ficou um
só crítico no fim da primeira versão, mais o gate humano. Por fatia, continuaram valendo o
teste que nasce vermelho e fica verde, os gates de integração contínua (CI, *continuous
integration*) e uma pré-revisão do integrador. Entraram três tarefas pequenas que fechavam
lacunas reais; saíram para depois da v1 os críticos contra a referência e um *spike* de
integração. E uma regra do laço foi aplicada ao pé da letra: quando o juiz devolveu a mesma
nota pela segunda vez seguida, parou-se o laço e a questão subiu para o humano
[CLAIM-01-008]. No mesmo dia, o Darú aprovou o gate do 074, com a coerência de estado
declarada como dívida transferida ao ciclo seguinte [CLAIM-01-009].

Leia o episódio como contabilidade. Produção praticamente ilimitada; verificação limitada;
atenção humana mais limitada ainda. O método só destravou quando trocou a pergunta "esta
tela está boa?" — barata de responder com mais uma geração — por "o que esta versão precisa
provar, e quem decide quando parar?". Essa troca é o assunto deste capítulo.

## Teoria

### O axioma: fazer e desfazer custam coisas diferentes

O Maestro organiza suas regras a partir de cinco axiomas. O quinto, A5, diz que o custo é
assimétrico entre fazer e desfazer: produzir é barato e fica mais barato; apagar dados,
fazer *deploy*, migrar e publicar têm custos que nenhuma velocidade compensa
([axioms.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/axioms.md)). O
teste de independência do axioma é instrutivo: retire A5 e toda ação merece o mesmo
tratamento — exatamente o gate uniforme que o método rejeita.

A5 é antigo como intuição e novo como premissa operacional. Engenharia de software sempre
soube que corrigir em produção custa mais que corrigir no teste. O que mudou é a outra ponta
da desigualdade. Quando gerar exigia horas de um engenheiro, o custo de produzir dominava a
conta, e era natural medir o trabalho por ele. Quando gerar passa a custar minutos de
máquina, a desigualdade se abre e o termo "desfazer" — junto com "verificar", que é o que
evita ter de desfazer — passa a dominar.

### Três termos de custo

Toda mudança paga três contas:

- **Gerar**: escrever o código, o teste, o documento. É o que os agentes baratearam.
- **Verificar**: estabelecer que a mudança faz o que devia, inclusive que atende à intenção.
  Inclui revisão, testes, gates e, em última instância, o julgamento humano.
- **Desfazer**: o custo esperado do erro que escapa — diagnosticar, reverter, migrar de
  volta, explicar ao cliente. Cresce com o tamanho do lote e com a irreversibilidade da ação.

O `exemplo/` deste capítulo transforma essa decomposição num modelo de valor esperado. Com
parâmetros ilustrativos, quando gerar fica 32 vezes mais barato, o custo por mudança aceita
cai só 6,5 vezes [CLAIM-01-013]. A diferença é o que não barateou. E com gerar tendendo a
zero, o custo não tende a zero: tende a um piso formado por verificar e desfazer
[CLAIM-01-015]. Não dá para chegar abaixo do piso gerando mais rápido. Só dá verificando
melhor ou tornando o erro mais barato de desfazer.

### A nova unidade: a mudança aceita

Daí o título. A unidade de trabalho de um time com agentes não é a linha escrita, o *commit*
ou o PR aberto. É a **mudança aceita**: uma alteração que alguém especificou, um mecanismo
independente verificou e um humano — ou uma política que um humano escreveu — aceitou
integrar. A linha escrita virou insumo abundante. A mudança aceita continua escassa, porque
depende de dois recursos que a máquina não substitui.

O texto de entrada do Maestro diz isso numa frase: quando a máquina executa, o valor deixa
de estar em digitar e passa a estar em **duas coisas humanas** — deixar a intenção clara e
verificar o resultado ([comece-por-aqui.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/comece-por-aqui.md)).
O método nasceu de levar a sério uma pergunta simples: se um agente escreve o código, o que
muda? A resposta reorganiza papéis, artefatos e gates, e cada capítulo deste livro trata de
um pedaço dessa reorganização.

As duas coisas humanas correspondem aos dois primeiros axiomas. A intenção é humana (A1):
um agente propõe e escreve, mas não *quer*. A consequência precisa de dono (A2): quem não
tem nada a perder não responde pelo resultado. Juntos com A5, eles dão a forma do princípio
operacional central do Maestro: *IA para explorar, propor e escrever; humano para
especificar, decidir e aprovar; testes, gates e revisão independente para validar*
([operating-model.md §2](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/operating-model.md)).
A frase distribui exatamente os três termos de custo: gerar fica com a IA; a intenção e a
decisão ficam com o humano; a verificação fica com mecanismos que não dependem de quem
escreveu.

### O modo de falha mais caro: compilar e errar a intenção

Um prompt vago não gera uma dúvida; gera código. O agente preenche o silêncio adivinhando
requisitos que ninguém disse, e o resultado compila, passa nos testes que o próprio agente
escreveu e erra a intenção. É o modo de falha mais caro que existe, porque parece sucesso.
O ciclo 074 é uma versão dele em escala de produto: cada tela, isolada, parecia pronta; o
sistema mentia.

Por isso a verificação da era dos agentes não é só "o teste passa". É também "o que foi
pedido está escrito em algum lugar que a verificação possa consultar". Esse é o argumento do
[capítulo 4](../04-a-spec-como-partitura/capitulo.md): a especificação deixa de descrever o
código e passa a gerá-lo. Aqui basta registrar o efeito econômico: intenção clara reduz a
chance de a mudança estar errada, e essa chance multiplica todos os outros custos.

### Os dois extremos que falham

O material de apresentação do Maestro resume a dor em dois extremos
([02-problema-solucao.md](../../maestro-handbook/diagramas/02-problema-solucao.md), cópia
congelada do handbook do método):

- **Sem IA**, entender um sistema legado exige dúzias de pessoas só para ler o código,
  reconstruir a intenção perdida e documentar o que existe. Lento, caro, e o conhecimento
  evapora com quem sai.
- **Com IA, mas sem método**, o agente escreve código que compila e erra a intenção;
  artefatos nascem e apodrecem; agentes trabalham sem contrapeso. Velocidade sem governança
  vira risco.

O modelo do `exemplo/` dá número a essa intuição, com a ressalva de que os parâmetros são
ilustrativos. O cenário do agente sem verificação, integrando em lote grande, sai 1,7 vez
mais caro que o humano digitando [CLAIM-01-014]. Gerar quase de graça não compensa um erro
que escapa e arrasta dez mudanças com ele. Falta um método no meio, e o meio não é um ponto
de equilíbrio entre os extremos: é uma redistribuição deliberada do esforço para verificar e
para tornar o erro barato.

O mesmo material aponta onde a redistribuição rende mais: o sistema legado. Ali, a
economia de contexto (a especificação como memória que sobrevive ao reinício do agente), a
paralelização por fronteira (agentes lendo partes diferentes do legado sem colidir) e a
rastreabilidade (spec ↔ PR ↔ teste) atacam justamente o custo que dominava o extremo sem IA.
O próprio material declara que a comparação "antes × depois" é **direcional** — dúzias de
pessoas por meses contra um humano e agentes por semanas — e não medida [CLAIM-01-019]. Vale
imitar essa honestidade: o argumento mecânico é forte, o número ainda é hipótese.

### Lote pequeno: a alavanca que move tudo junto

Se o termo que domina é desfazer, a alavanca mais barata é encolher o que se desfaz. O
programa DevOps Research and Assessment (DORA) mostrou, ao longo de anos de pesquisa com
equipes de entrega, que velocidade e estabilidade andam juntas: os mesmos times são rápidos
*e* estáveis, e as métricas são resultados de capacidades como integração contínua, testes
automatizados, revisão e entregas pequenas (Forsgren, Humble e Kim, 2018). A pesquisa que
fundou o modelo operacional do Maestro registra as quatro métricas clássicas — frequência de
entrega, tempo de espera da mudança, taxa de falha e tempo de recuperação — e a taxa de
retrabalho como quinta [CLAIM-01-018].

O handbook do método resume o mecanismo
([02-dora-space.md §5.3](../../maestro-handbook/handbook/02-dora-space.md)): mudança pequena
chega mais vezes, atravessa mais rápido, é fácil de testar e revisar e, quando falha, é
fácil de reverter. Uma alavanca, quatro métricas. A analogia que o diário do método usa é a
**linha de produção cognitiva**. A fábrica anterior a Ford era lenta porque cada peça era
única; padronizar barateou o fluxo. Mas a linha de Ford não tinha desfazer barato, e a
cognitiva tem: controle de versão, *checkpoints*, reversão de um commit. Lote pequeno somado
a reversibilidade dá rápido *e* estável.

No modelo do `exemplo/`, com a mesma verificação, passar de lotes de dez mudanças para lotes
de uma (com uma spec que reduz a chance de erro) leva o custo por mudança aceita de 6,91 para
1,65 [CLAIM-01-013]. Quase toda a diferença vem do termo desfazer.

### Reversibilidade compra velocidade

A última peça liga A5 à autonomia. O gate humano sempre foi um *proxy* de "torne reversível
ou olhe antes". Onde existe backup, execução a seco (*dry-run*), homologação e exclusão
lógica (*soft-delete*), a ação muda de classe de risco e passa a ser delegável. É o que o
Maestro chama de reversibilidade engenheirada, e é o tema do
[capítulo 11](../11-risco-reversibilidade-e-autonomia/capitulo.md).

O modelo mostra o reverso: quando a mesma mudança vira irreversível — o custo de desfazer
multiplicado por dez —, pagar mais verificação, com um gate humano antes de agir, baixa o
custo esperado de 4,08 para 2,45 [CLAIM-01-015]. O gate não é uma taxa fixa sobre todo
trabalho. É um investimento que só se paga onde desfazer é caro. Aplicado a tudo, ele vira o
funil que o ciclo 074 encontrou.

### O recurso escasso: atenção humana

Juntando as peças: gerar ficou abundante; verificar automaticamente escala com
infraestrutura; mas decidir — o que construir, quando parar, o que aceitar — continua
passando por uma cabeça. A Jornada do Maestro, que reconstrói o método na ordem em que foi
descoberto, tem uma parada só para isso: a nona, "Gargalo", cuja pergunta é *o que passa a
ser escasso?* e cuja resposta é a atenção humana — logo, poucos gates, nos pontos
irreversíveis [CLAIM-01-020]. O [capítulo 3](../03-um-humano-muitos-agentes/capitulo.md)
trata desse limite. Aqui ele fecha a conta: a mudança aceita é escassa porque cada uma
consome um pouco do único recurso que não escala com dinheiro.

### Governança, não framework

Uma consequência para o restante do livro. Se o custo migrou para intenção, verificação e
reversibilidade, a resposta não é mais um *framework* de agentes — mais uma forma de fazer
agentes gerarem. É um sistema de **governança operacional**: constituição, raias, papéis,
artefatos, gates, registros de decisão, *skills*, scripts e *hooks*, rodando sobre
diferentes *harnesses* e modelos. Essa é a tese da base de pesquisa deste livro
([base-de-pesquisa.md](../../pesquisa/base-de-pesquisa.md)), e a razão de o Maestro aparecer
aqui como caso de estudo e não como ferramenta obrigatória.

A literatura acadêmica caminha na mesma direção por outro lado. A revisão de He, Treude e Lo
sobre sistemas multiagente baseados em modelos de linguagem para engenharia de software,
publicada em 2025 na *Transactions on Software Engineering and Methodology* (TOSEM) da
Association for Computing Machinery (ACM), organiza o campo e propõe uma agenda de
pesquisa em que a colaboração entre humanos e agentes aparece como frente aberta. A leitura
deste livro, que é nossa e não dos autores, é que essa frente é onde o custo foi parar.

## Alternativas

Há outras respostas à pergunta do capítulo. Todas têm algo de certo; nenhuma resolve a conta
inteira.

| Alternativa | O que faz | Veredito |
|---|---|---|
| **Manter a unidade antiga** (medir linhas, PRs por pessoa, *story points* entregues) | Continua otimizando a produção | **Rejeitar.** Mede o que ficou barato. Com agentes, PRs por semana sobem sem que nada de valor suba; a métrica vira alvo e para de medir |
| **Freio burocrático** (comitê de mudança, janela de deploy mensal, aprovação em várias instâncias) | Responde ao risco reduzindo a frequência | **Rejeitar.** Aumenta o lote, e lote grande piora as quatro métricas do DORA ao mesmo tempo. Trata desfazer caro com mais coisa para desfazer |
| **Autonomia total** (o agente decide, integra e publica) | Elimina a espera humana | **Rejeitar para o irreversível; aceitar no reversível.** É o cenário B do `exemplo/` quando falta verificação. Onde desfazer é barato e há verificação automática, autonomia alta é a escolha certa |
| **Frameworks de orquestração** (LangGraph, CrewAI, Google Agent Development Kit (ADK), Microsoft Agent Framework, OpenAI Agents Software Development Kit (SDK)) | Estruturam como agentes cooperam e chamam ferramentas | **Complementar.** Resolvem a execução — o termo gerar. Não dizem quem decide, o que é verificado nem o que é reversível |
| **Desenvolvimento guiado por especificação** (por exemplo, o GitHub Spec Kit) | Põe a intenção num artefato antes do código | **Adotar como peça.** Ataca a intenção, o termo `p` do modelo. Sozinho, não cobre verificação independente nem reversibilidade |
| **Scrum completo** | Organiza um time humano por papéis e cerimônias | **Adaptar, não adotar.** A pesquisa que fundou o modelo operacional do Maestro recomendou o esqueleto de Shape Up e Kanban (apetite fixo, limite de trabalho em andamento) em vez de Scrum, porque daily e planejamento de sprint sincronizam pessoas, não agentes [CLAIM-01-017] |

O padrão comum aos vereditos: cada alternativa otimiza um termo da conta. A resposta que
este livro defende trata os três ao mesmo tempo e, principalmente, decide *onde* gastar o
recurso escasso.

## O padrão Maestro

O Maestro responde à mudança de unidade em quatro camadas. Vale distinguir o que é regra
(texto que um agente lê), o que é script (um comando que dá verde ou vermelho) e o que é
hook (um mecanismo do *harness* que intercepta a ação antes de ela acontecer).

**1. A regra: o princípio operacional central.** O modelo operacional abre com a divisão já
citada — IA explora, propõe e escreve; humano especifica, decide e aprova; testes, gates e
revisão independente validam — e dela tira três regras: a spec é a fonte de verdade; quem
executa não verifica; e "prove, não declare"
([operating-model.md §2](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/operating-model.md)).
A origem está documentada. A pesquisa de 22 de julho de 2026 que fundamentou o Registro de
Decisão de Arquitetura (ADR, *Architecture Decision Record*) 0004 chegou à mesma máxima
depois de comparar práticas de mercado: desenvolvimento guiado por especificação, o
programa DORA, Shape Up, os padrões de agentes da Anthropic e o fluxo do Claude Code
([resultado-pesquisa-praticas-desenvolvimento-avaliacao.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/research/resultado-pesquisa-praticas-desenvolvimento-avaliacao.md))
[CLAIM-01-017]. A pesquisa registra também sua ressalva mais honesta: a literatura pressupõe
times de várias pessoas, e transpor para um humano com agentes foi síntese própria, não
padrão pronto.

**2. A derivação: axiomas e teoremas.** A regra não fica solta. O teorema T3 do Maestro diz
que o gate escala com a irreversibilidade e nunca é uniforme, e deriva de A2 e A5
([axioms.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/axioms.md)). O
corolário C4 completa: reversibilidade baixa a classe de risco e é mais barata do que mais
uma aprovação. Quando alguém propõe uma regra nova, a primeira pergunta é de qual axioma ela
deriva. É assim que o método evita que "frear os agentes" entre por medo.

**3. O registro: como o método foi descoberto.** Duas trilhas guardam o caminho. O diário de
aprendizado do modelo operacional critica, um a um, os doze elementos do método — princípio
central, especificação, fluxo com agentes, orquestração, papéis, cerimônias, artefatos,
definições de pronto, gates, evidência do DORA, rastreabilidade e governança leve — e fecha
com uma síntese dos fios que os amarram, em que a reversibilidade aparece como alavanca-mestra
([jornada-aprendizado-modelo-operacional.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/research/jornada-aprendizado-modelo-operacional.md)).
A Jornada reorganiza o mesmo material em doze paradas, cada uma com a tensão, a pergunta que
a destravou e a regra que nasceu ([docs/jornada/README.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/jornada/README.md))
[CLAIM-01-016]. Para quem vai adotar o método, o valor dessas trilhas é mostrar que cada
regra nasceu de uma dor: a parada 3 pergunta "quanto custa desfazer?" e responde que
reversibilidade compra velocidade; a parada 9 pergunta o que passa a ser escasso e responde
"atenção humana".

**4. O mecanismo: scripts e hooks que contabilizam a mudança aceita.** É aqui que o método
deixa de ser intenção:

- **Script** — `scripts/promote-main.sh` promove o trabalho à linha principal e grava o gate
  em `docs/records/decisoes.jsonl`, sozinho. O índice de decisões é, na prática, o registro
  das mudanças aceitas. Até o commit de referência deste livro, o repositório tinha 943
  commits e 50 promoções registradas como gate de merge [CLAIM-01-010], ao longo de 75
  ciclos numerados [CLAIM-01-011]. A proporção entre o que se produz e o que se aceita está
  à vista, sem painel.
- **Script** — `scripts/check-conformance.sh <ciclo>` responde "estou seguindo o método?" com
  saída de máquina, e não com a memória do agente.
- **Hook** — um `PreToolUse` (`scripts/hooks/guard-immutables.py`, ligado em
  [`.claude/settings.json`](https://github.com/GHDaru/maestro/blob/19823c2/.claude/settings.json))
  recusa reescrever o que o método guarda como histórico: um ADR aceito, o índice de
  decisões. É A5 aplicado ao próprio processo: o que é caro de desfazer não depende de o
  agente lembrar.
- **Hook** — um `Stop` roda a conferência de conformidade no fim de cada turno do agente.

**O padrão em movimento: o corte da v1.** O episódio da seção "A falha real" é o padrão
funcionando, não falhando. O ciclo 076, que sucedeu o 074, foi aberto com construtor e
crítico separados por fatia — aplicação literal de "quem executa não verifica". Quando o
custo dessa verificação passou a dominar, o humano não abandonou a verificação: realocou-a
([tasks.md do 076, seção «Corte da v1»](https://github.com/GHDaru/maestro/blob/19823c2/specs/076-padroes-de-engenharia-e-react/tasks.md))
[CLAIM-01-007]. Ficou por fatia o que é barato e automático (teste vermelho→verde, gates da
CI); ficou para o fim o que é caro e humano (um crítico, um gate). O desenvolvimento guiado
por testes e a fronteira hexagonal "NÃO baixam", diz o registro. Os 75 commits do 076 entre
29 de outubro e 1º de novembro [CLAIM-01-012] mostram que a produção não parou. O que mudou
foi onde se gastou a atenção.

Note o que o Maestro **não** faz: não mede produtividade por agente, não instrumenta painel
de métricas do DORA (foi descartado por YAGNI, *You Aren't Gonna Need It*, enquanto não houver
com quem comparar) e não exige gate humano por mudança. A unidade contabilizada é a promoção
aceita, e o gate humano fica nos pontos em que desfazer é caro.

## Exemplo executável

O diretório [`exemplo/`](exemplo/README.md) tem um modelo em Python 3, só com a biblioteca
padrão, que calcula o custo esperado por mudança aceita em seis cenários: humano digitando;
agente sem verificação em lote grande; agente com verificação em lote grande; agente com
spec, verificação e lote de uma mudança; o mesmo com ação irreversível; e o irreversível com
gate humano.

```bash
cd livro/01-a-mudanca-de-unidade-de-trabalho/exemplo
python economia.py               # a tabela
python economia.py --conferir    # 0 = bate com saida-esperada.txt
```

O que observar na saída:

1. **Gerar 32 vezes mais barato derruba o total só 6,5 vezes** [CLAIM-01-013]. O resto é
   verificar e desfazer.
2. **O agente sem verificação sai mais caro que o humano** (1,7 vez) [CLAIM-01-014].
3. **O piso**: no cenário com spec, verificação e lote de uma mudança, com gerar tendendo a
   zero, o custo para em 1,38 [CLAIM-01-015]. Esse número é o seu limite de produtividade
   enquanto verificar e desfazer não mudarem.
4. **O gate compensa onde desfazer é caro**: no cenário irreversível, o gate humano baixa o
   total de 4,08 para 2,45 [CLAIM-01-015].

Os parâmetros são ilustrativos e estão em `cenarios.json`. O exercício útil é trocá-los
pelos do seu time: quanto tempo leva uma revisão, que fração dos defeitos ela pega, quanto
custa reverter um deploy, de quantas mudanças é o seu lote típico. O README do exemplo
mostra também como provar que a conferência acusa uma divergência: um check que nunca falhou
é uma esperança, não um check.

## Contraexemplo

A mudança de unidade não vale em todo lugar, e a regra tem preço.

**Quando verificar já era o custo dominante.** Em domínios em que gerar nunca foi o gargalo —
migração de dados em produção, mudança de esquema de cobrança, firmware embarcado —,
agentes mexem pouco na conta. O termo desfazer sempre dominou, e o processo já era desenhado
em torno dele. Aí o capítulo acrescenta pouco ao que o time sabe, e o risco é o inverso:
usar a velocidade de geração como argumento para encurtar uma verificação que continua
necessária.

**Quando a mudança é descartável.** Um protótipo para jogar fora, um script de análise de
uma tarde, uma prova de conceito: desfazer custa zero, porque ninguém depende do resultado.
Gastar verificação aí é cerimônia. O Maestro reconhece isso nas raias (um *typo* não merece
spec) e é tema do [capítulo 4](../04-a-spec-como-partitura/capitulo.md). O cuidado é a
transição: o protótipo do 074 era descartável como código, mas não como decisão de produto,
e foi a decisão que precisou do gate.

**O custo da própria regra.** "Quem executa não verifica", aplicada a cada fatia, foi exatamente
o que o corte da v1 aliviou. A verificação independente tem custo de *tokens*, de tempo de
integração e, principalmente, de atenção humana para ler o veredito. Aplicada uniformemente,
ela vira o gate uniforme que A5 manda evitar. O sinal de excesso é visível: o mesmo achado
voltando rodada após rodada sem convergir [CLAIM-01-008]. Nesse ponto, a resposta não é mais
uma rodada, é mudar a pergunta ou subir a decisão.

**Quando o "barato" esconde custo.** Gerar é barato em relação ao resto, não grátis. Uma
fatia do 074 declarou cerca de 20 milhões de *tokens* [CLAIM-01-006]. Em times com orçamento
de inferência apertado, o termo gerar volta a pesar, e o [capítulo 13](../13-observabilidade-e-economia/capitulo.md)
trata de medi-lo por tarefa aceita.

**Quando a unidade "mudança aceita" é gameável.** Contar promoções aceitas também pode virar
alvo: dividir artificialmente uma mudança em dez para inflar a contagem. A defesa é a mesma
do DORA — ler aos pares, aceitação junto com retrabalho e escape —, não confiar num número só.

## Evidência

O que sustenta o capítulo, separado pelo estado:

**Medido no repositório do Maestro** (comandos em `claims.md`, todos reproduzíveis no commit
`19823c2`): o volume de commits do ciclo 074 [CLAIM-01-001] e do 076 [CLAIM-01-012]; as
onze críticas às cegas do 074 [CLAIM-01-004]; os 943 commits e as 50 promoções registradas
[CLAIM-01-010]; os 75 ciclos [CLAIM-01-011].

**Observado em registros datados**: as quatro rodadas perdidas da P3 e a mudança de natureza
da lacuna [CLAIM-01-002]; a divergência dos contadores [CLAIM-01-003]; as seis jornadas
reprovadas [CLAIM-01-005]; o piso de *tokens* de uma fatia [CLAIM-01-006]; o corte da v1
[CLAIM-01-007]; a nota repetida do juiz [CLAIM-01-008]; o gate aprovado [CLAIM-01-009]; a
pesquisa que fundou o modelo operacional [CLAIM-01-017]; as métricas do DORA tal como essa
pesquisa as registra [CLAIM-01-018]; as doze paradas da Jornada [CLAIM-01-016] e a parada do
gargalo [CLAIM-01-020].

**Medido num modelo, não no mundo**: os números do `exemplo/` [CLAIM-01-013, CLAIM-01-014,
CLAIM-01-015] são saídas reproduzíveis de parâmetros ilustrativos. Provam a forma da
redistribuição de custo, não a magnitude no seu time.

**Hipóteses** (da agenda de pesquisa do livro, `pesquisa/base-de-pesquisa.md`): o modelo
assume três coisas que ainda não foram testadas com rigor no Maestro.

- **H1** — a spec reduz retrabalho (no modelo, `p` cai de 0,30 para 0,15).
- **H5** — gate com teste de mutação reduz escapes (no modelo, `d` alto).
- **H8** — reversibilidade permite mais autonomia (no modelo, `u` e `b` pequenos).

A comparação "dúzias de pessoas × meses contra um humano e agentes × semanas" é declarada
direcional pela própria fonte e fica como hipótese [CLAIM-01-019]. O [capítulo 15](../15-validando-o-maestro/capitulo.md)
descreve o protocolo que as testaria.

O limite mais importante: um caso, um repositório, um humano regendo. O episódio do 074 é
evidência de que a redistribuição acontece, não de quanto ela vale em geral.

## Checklist

Aplique no seu time, nesta ordem:

- [ ] Para as últimas dez mudanças integradas, estime em horas os três termos: gerar,
      verificar e desfazer (inclusive retrabalho). Qual domina?
- [ ] Defina por escrito o que conta como **mudança aceita** no seu fluxo (quem especifica,
      o que verifica, quem aceita) e conte quantas houve no último mês.
- [ ] Rode `exemplo/economia.py` com os seus parâmetros e anote o piso de custo.
- [ ] Liste as ações do seu fluxo cujo desfazer custa mais de um dia (deploy, migração,
      publicação, apagar dados). Cada uma tem gate humano ou reversibilidade engenheirada?
- [ ] Liste as ações cujo desfazer custa minutos. Alguma delas ainda espera aprovação humana?
      Remova a espera e ponha uma verificação automática no lugar.
- [ ] Meça o tamanho típico do seu lote (mudanças por integração). Se for maior que um,
      escolha uma mudança de processo que o reduza.
- [ ] Verifique se alguma métrica do time mede produção (PRs, linhas, *story points*) sem
      par de qualidade. Ponha o par ou retire a métrica.
- [ ] Defina uma regra de parada para laços de revisão: se o mesmo achado voltar duas vezes,
      a decisão sobe para um humano.
- [ ] Confirme que a intenção de cada mudança relevante está escrita num artefato que a
      verificação consulta, e não só no prompt.

## Referências

**Maestro** (objeto de estudo; todas as citações no commit `19823c2`):

- Axiomas, teoremas e corolários — https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/axioms.md
- Modelo operacional, §2 — https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/operating-model.md
- Princípios (constituição) — https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/principles.md
- Comece por aqui — https://github.com/GHDaru/maestro/blob/19823c2/docs/comece-por-aqui.md
- A Jornada — https://github.com/GHDaru/maestro/blob/19823c2/docs/jornada/README.md
- Diário de aprendizado do modelo operacional — https://github.com/GHDaru/maestro/blob/19823c2/docs/research/jornada-aprendizado-modelo-operacional.md
- Avaliação da pesquisa de práticas (base do ADR 0004) — https://github.com/GHDaru/maestro/blob/19823c2/docs/research/resultado-pesquisa-praticas-desenvolvimento-avaliacao.md
- Tarefas do ciclo 076, seção «Corte da v1» — https://github.com/GHDaru/maestro/blob/19823c2/specs/076-padroes-de-engenharia-e-react/tasks.md
- Tarefas do ciclo 074 — https://github.com/GHDaru/maestro/blob/19823c2/specs/074-prototipo-navegavel/tasks.md
- Crítica da P3, rodada 4 — https://github.com/GHDaru/maestro/blob/19823c2/specs/074-prototipo-navegavel/gauntlet-maestri/critica-p3-rodada-4.md
- Índice de decisões — https://github.com/GHDaru/maestro/blob/19823c2/docs/records/decisoes.jsonl
- Configuração de hooks — https://github.com/GHDaru/maestro/blob/19823c2/.claude/settings.json

**Handbook do método** (cópia congelada neste repositório, `maestro-handbook/`, de `19823c2`):

- 01 — Princípio central, §5.3 (reversibilidade) — `../../maestro-handbook/handbook/01-principio-central.md`
- 02 — DORA e SPACE, §5.3 (tamanho de lote) — `../../maestro-handbook/handbook/02-dora-space.md`
- 03 — Spec-driven, §2 (compilar e errar a intenção) — `../../maestro-handbook/handbook/03-spec-driven.md`
- Diagrama problema → solução — `../../maestro-handbook/diagramas/02-problema-solucao.md`
- Apresentação executiva (slides "Antes × Depois" e "Onde o retorno sobre investimento (ROI) é maior") — `../../maestro-handbook/handbook/apresentacao-executiva-maestro.html`

**Literatura e fontes externas**:

- Forsgren, N.; Humble, J.; Kim, G. *Accelerate: The Science of Lean Software and DevOps*. IT
  Revolution, 2018.
- He, J.; Treude, C.; Lo, D. "LLM-Based Multi-Agent Systems for Software Engineering:
  Literature Review, Vision, and the Road Ahead". *ACM Transactions on Software Engineering
  and Methodology*, 2025.
- DORA. *DORA metrics (four keys)* — https://dora.dev/guides/dora-metrics-four-keys/ (URL
  como registrada na pesquisa do Maestro de 22/07/2026; não reacessada nesta escrita).
- Anthropic. *Building effective agents* — https://www.anthropic.com/engineering/building-effective-agents
  (idem).
- GitHub. *Spec-driven development with AI* (2025-09-02) —
  https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/
  (idem).
- Basecamp. *Shape Up* — https://basecamp.com/shapeup/1.1-chapter-02 (idem).

**Base deste livro**: `../../pesquisa/base-de-pesquisa.md` (tese, hipóteses H1–H10,
referências-base).
