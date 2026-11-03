# C — Pacote de replicação

> Uma afirmação que só se confere na máquina de quem a escreveu é um depoimento, não evidência.

Este livro faz afirmações sobre um método e sobre o que acontece quando um time o adota. Algumas
são medidas, muitas são observadas num único repositório, várias são hipóteses. Este apêndice é o
contrato que permite a você, tech lead, conferir cada uma delas sem confiar no autor: o que
instalar, em que versão, com que protocolo, onde ficam os dados das execuções e como cada número
do texto aponta para o comando que o reproduz. Se você vai citar este livro numa decisão do seu
time, é aqui que se descobre quanto cada frase aguenta.

## Pergunta central

O que alguém de fora precisa ter nas mãos para reproduzir, ou refutar, cada afirmação deste
livro?

## O que este apêndice entrega

Um pacote de replicação tem cinco camadas. Cada uma responde a uma pergunta que o leitor cético
faz, e cada uma tem um lugar no disco.

| Camada | Pergunta que responde | Onde mora |
|---|---|---|
| 1. O método instalável | "Consigo pôr o mesmo método no meu repositório?" | o instalador do Maestro e o portão que exercita a cópia instalada |
| 2. A versão congelada | "Estou olhando para a mesma coisa que o autor?" | o commit de referência `19823c2`, releases e tags |
| 3. Hipóteses e protocolo | "O que exatamente se afirma, e como se testaria?" | [`pesquisa/hipoteses.md`](../../../pesquisa/hipoteses.md) e [`pesquisa/protocolo.md`](../../../pesquisa/protocolo.md) |
| 4. Os runs | "Onde estão os dados de cada execução?" | `pesquisa/runs/`, um diretório por execução, com schema imutável |
| 5. Os claims | "Este número vem de onde?" | o `claims.md` de cada capítulo, conferido por `scripts/check-claims.sh` |

As camadas estão em estados diferentes, e o apêndice diz qual é qual. A primeira existe e tem
portão. A segunda existe pela metade: não há *release*, e o *commit* de referência ainda não está
no repositório público [CLAIM-93-014]. A terceira e a quarta estão desenhadas e quase vazias: até
02/11/2026 nenhuma hipótese da agenda foi testada com o desenho completo, o protocolo é um
rascunho ainda não ratificado e o diretório de *runs* não existe [CLAIM-93-004]. A quinta tem
portão no livro inteiro, e o portão recusa o que está fora da forma. Um pacote de replicação que
se apresentasse como pronto estaria cometendo o defeito que o
[capítulo 10](../../10-quality-gates-que-provam-fatos/capitulo.md) descreve: o check que mede o
proxy, não o fato.

## De onde vem a ideia, e o que mais existe

Pacote de replicação não é invenção deste livro. Três práticas de outras áreas resolvem partes do
mesmo problema, e vale saber o que cada uma fixa antes de julgar o que este apêndice toma delas.

**Reproduzir não é replicar.** A distinção que organiza o campo é de quem são os artefatos. A
política de avaliação de artefatos da Association for Computing Machinery (ACM), *Artifact Review
and Badging*, na versão 1.1, chama de resultado **reproduzido** o que outro time obtém com os
artefatos do autor, e de **replicado** o que outro time obtém sem eles, refazendo o experimento
a partir da descrição. Os dois verbos medem coisas diferentes. Reproduzir prova que o autor não
errou na conta; replicar prova que o efeito não morava nos artefatos dele. Este apêndice entrega a
primeira coisa para os claims e prepara a segunda para as hipóteses: o protocolo existe para que
outro time rode os próprios *runs* sem pedir nada ao autor.

| Prática | O que fixa | O que este pacote toma | O que não toma |
|---|---|---|---|
| Avaliação de artefatos (ACM *Artifact Review and Badging*) | selos separados para artefato disponível, artefato que funciona e resultado reproduzido, concedidos por um comitê | a separação entre "o artefato roda" (`check-installed.sh`, o exemplo deste apêndice) e "o resultado se confirma" (a coluna de evidência) | o comitê externo; aqui a conferência é por conta do leitor |
| Pré-registro (Nosek et al., 2018) | hipótese, desenho e análise registrados com data antes de qualquer dado | o protocolo congelado antes do primeiro *run* e a regra de que margem não muda depois de ver o resultado | o carimbo de tempo de terceiro; aqui a data é um *commit* do próprio autor, que é mais fraca enquanto o *commit* não está num repositório público |
| Fichas de dados e de modelo (Gebru et al., 2021; Mitchell et al., 2019) | origem, composição, uso pretendido e limites do conjunto ou do modelo, num formato fixo | o `run.json` como ficha de cada execução e a seção de limites deste apêndice | a ficha do corpus inteiro, que só faz sentido quando os cenários existirem |
| *Benchmark* público (SWE-bench, *Software Engineering benchmark*; ver o [capítulo 15](../../15-validando-o-maestro/capitulo.md)) | tarefa e teste fixos, que qualquer um roda contra qualquer agente | o caso com oráculo determinístico, no ASEG-Bench (o *benchmark* de governança do [Apêndice B](../b-aseg-bench/capitulo.md)) | a pergunta: o *benchmark* mede o agente; este pacote quer medir o método em volta dele |

O veredito é que nenhuma das quatro, sozinha, serve a um livro sobre método. A avaliação de
artefatos supõe um comitê que este livro não tem. O pré-registro supõe uma hipótese pronta para
testar, e a maior parte do texto é observação, não hipótese. As fichas descrevem um conjunto que
ainda não existe. O *benchmark* fixa a tarefa, mas não o tratamento. O pacote combina as quatro
em escala pequena e diz, camada por camada, qual parte já está de pé.

## O método instalável e a versão congelada

As camadas 1 e 2 respondem à pergunta que vem antes de qualquer hipótese: o método que você vai
testar é o mesmo que o livro descreve?

### Instalar é escrever arquivos, e o instalador diz quais

O instalador canônico é
[`scripts/install-maestro.sh`](https://github.com/GHDaru/maestro/blob/19823c2/scripts/install-maestro.sh).
Ele põe agentes, *skills*, scripts, *templates* e *hooks* em outro repositório e aceita seis
opções: `--dry-run` mostra o que faria, `--ai <id>` declara para qual agente de inteligência artificial (IA) instalar,
`--write-block` grava o bloco de instruções do método no arquivo que a IA lê, `--no-hooks` pula a
camada de enforcement, `--force` impõe a versão do método e `--block` só imprime o bloco
[CLAIM-93-010]. A propriedade que importa para replicação é a que o cabeçalho do script declara:
instalar também é atualizar, e nada que você escreveu é sobrescrito. Um arquivo que você alterou
fica, com a versão nova ao lado como `*.maestro-new`; mesmo com `--force`, a sua versão é salva
antes como `*.maestro-old` [CLAIM-93-010]. Um *run* que instala o método num cenário já
povoado, portanto, não apaga a linha de base sem deixar rastro.

O caminho curto é `bin/maestro init <projeto> --ai claude`, que conduz agente, destino,
instalação e verificação. A receita
[`instalar-o-maestro.md`](https://github.com/GHDaru/maestro/blob/19823c2/docs/receitas/instalar-o-maestro.md)
registra o resultado de uma instalação real, num projeto que só tinha `README.md`: 81 arquivos
escritos com `--ai claude`; 80 com `install-maestro.sh` sozinho, que não grava o `CLAUDE.md`;
53, e nenhum diretório `.claude/`, com `--ai codex` [CLAIM-93-011]. A diferença não é detalhe.
O braço T do protocolo instalado para um agente não é o mesmo braço T instalado para outro: a
camada de *hooks* é mecanismo de um *harness* específico (o programa que executa o agente e
lhe dá ferramentas, como o Claude Code ou o Codex) e não viaja para os demais. Por isso a
escolha fica gravada em `.maestro/install-options.json`, um arquivo JavaScript Object Notation
(JSON), com o agente, o arquivo de instrução,
se há *harness*, a versão do método e a data [CLAIM-93-011], e esse arquivo entra na lista do
que um *run* congela.

### O portão que exercita a cópia instalada

Todo portão do Maestro media o repositório-fonte, onde cada arquivo que o método menciona
existe. Ninguém rodava a cópia instalada. Dois defeitos viveram nesse ponto cego até que um
agente companheiro os achou numa instalação real: `scripts/check-roles.sh` era enviado e lia
`docs/agents/README.md`, que o instalador não copia; os comandos `/speckit.*` eram enviados
apontando para `.specify/memory/constitution.md`, caminho que a instalação não cria
[CLAIM-93-012]. O cabeçalho de
[`scripts/check-installed.sh`](https://github.com/GHDaru/maestro/blob/19823c2/scripts/check-installed.sh)
nomeia o defeito comum: o método enviava algo que aponta para o que não enviava.

O portão nascido daí instala o método num diretório vazio e exercita o resultado. O próprio
script delimita o que mede: não que o método é bom, nem que uma IA vai segui-lo, mas que uma
instalação nova é coerente, ou seja, cada script enviado roda e cada caminho citado existe ali
[CLAIM-93-012]. Para quem replica, essa é a pré-condição mínima. Antes de atribuir um
resultado ao método, confirme que ele chegou inteiro ao cenário; um braço T com metade dos
scripts quebrados mede o instalador, não o tratamento.

### Três verificações para a cópia de qualquer método

Nada acima depende do Maestro, só os nomes dos arquivos. Se o seu time adota outro método (um
conjunto de *prompts* e *templates* de spec, um kit de *skills*, as regras de um orquestrador), a
pergunta "a cópia chegou inteira?" se responde com as mesmas três verificações, cada uma com uma
saída que uma máquina confere:

1. **Ensaiar antes de escrever.** O instalador, ou o seu passo manual de cópia, tem de listar o
   que escreveria sem escrever. Se ele não tem esse modo, a lista é o primeiro artefato a criar:
   sem ela, você não sabe o que o tratamento contém. No Maestro, é o `--dry-run`.
2. **Exercitar a cópia num diretório vazio.** Instale num repositório sem nada, rode cada script
   que veio e confira que cada caminho citado pelas instruções existe ali. O defeito que essa
   verificação acha é sempre o mesmo, o de cima: o pacote aponta para o que não leva. No Maestro,
   é `scripts/check-installed.sh`; em outro método, um *script* curto que instala, roda e procura
   os caminhos citados resolve.
3. **Gravar a escolha no próprio destino.** Para qual agente, com que *harness*, em que versão do método
   e em que data. O registro fica no repositório instalado e entra no registro de cada execução.
   No Maestro, é o `.maestro/install-options.json`; em outro método, um arquivo pequeno que o
   seu instalador escreve.

As três juntas separam duas perguntas que um time costuma misturar: "o método funciona?" e "o
método chegou?". Só a segunda tem resposta hoje, e ela vem antes.

### A versão: um *commit*, não uma *release*

A base de pesquisa pede "tags e releases reproduzíveis" ao lado do protocolo e dos *runs*. O
estado em 02/11/2026 é a metade disso. O `CHANGELOG.md` do Maestro no *commit* de referência
tem três versões numeradas, 0.1.0, 0.2.0 e 0.3.0, de 09/08/2026 a 22/08/2026, e uma seção
`[Unreleased]` acima delas; no clone local usado para escrever este livro, `git tag -l 'v*'` não
lista nenhuma tag [CLAIM-93-013]. A ausência não é só do clone: em 03/11/2026, uma consulta
anônima ao repositório público (`git ls-remote --tags`) também não devolve nenhuma tag
[CLAIM-93-014]. Tudo o que o livro descreve depois de 22/08/2026 está, portanto, fora de
qualquer versão numerada. É por isso que cada link ao Maestro neste livro aponta para
`blob/19823c2/…`, e não para uma versão: o *commit* é a única referência que congela de fato o
que foi lido. Um *commit* resolve a reprodução, mas não a comunicação. "Rodei com o Maestro
`19823c2`" não diz a um leitor o que mudou desde a 0.3.0, e uma *release* diria.

Há um furo maior, e ele vale ser dito antes de você clonar. Na mesma consulta de 03/11/2026, o
repositório aceita leitura anônima, mas nenhuma das 50 *branches* públicas contém o *commit*
`19823c2`: ele está numa *branch* local do autor que ainda não foi publicada [CLAIM-93-014]. Até
ser publicado, um clone feito por você não tem a versão de referência, e o passo 1 do roteiro
mais abaixo falha. O pacote não esconde isso: o script do exemplo deste apêndice marca
`FALHA` exatamente nesse ponto. Um *commit* de referência que só existe na máquina do autor é o
caso-limite da epígrafe, e é o primeiro item a corrigir antes de qualquer *run*.

## As hipóteses: o que o livro afirma sem ter medido

Boa parte deste livro descreve o que aconteceu num repositório: um ciclo, um *commit*, um
portão que deixou passar um defeito. Isso é observação, e cada capítulo a marca como tal. Outra
parte é aposta: "a spec reduz retrabalho", "multiagente só ajuda com cortes independentes". Essas
apostas estão reunidas numa agenda de dez hipóteses, H1 a H10 [CLAIM-93-001], e o pacote de
replicação existe principalmente para que elas deixem de ser apostas, num sentido ou no outro.

| | Hipótese | Capítulo que a usa |
|---|---|---|
| H1 | a spec reduz retrabalho | [4](../../04-a-spec-como-partitura/capitulo.md) |
| H2 | a revisão em contexto fresco acha mais defeito | [2](../../02-o-problema-da-confianca/capitulo.md) |
| H3 | contexto seletivo reduz custo sem perder qualidade | [5](../../05-engenharia-de-contexto/capitulo.md) |
| H4 | multiagente só ajuda com cortes independentes | [6](../../06-como-dividir-o-trabalho/capitulo.md) |
| H5 | portão provado por teste de mutação reduz escapes | [10](../../10-quality-gates-que-provam-fatos/capitulo.md) |
| H6 | catálogo semântico reduz duplicação | [8](../../08-ddd-para-agentes/capitulo.md) |
| H7 | glossário reduz inconsistência | [8](../../08-ddd-para-agentes/capitulo.md) |
| H8 | reversibilidade permite mais autonomia | [11](../../11-risco-reversibilidade-e-autonomia/capitulo.md) |
| H9 | modelo menor basta em tarefa estruturada | [7](../../07-papeis-e-skills/capitulo.md) |
| H10 | retrospectiva que vira regra reduz recorrência | [14](../../14-a-organizacao-que-aprende/capitulo.md) |

Uma hipótese só serve a um pacote de replicação se responder a três perguntas antes do primeiro
experimento: **o que se mede**, **contra o quê** e **que resultado a derrubaria**. O arquivo
[`pesquisa/hipoteses.md`](../../../pesquisa/hipoteses.md) responde às três para cada uma das
dez. Aqui fica a lógica que as amarra.

### O desenho: quatro braços que se somam

A agenda compara quatro braços [CLAIM-93-002]. No braço A, a linha de base, o agente recebe só
o *prompt* da tarefa. No B, recebe a tarefa como especificação escrita. No C, a especificação
mais os portões automáticos de integração contínua. No braço de tratamento, o Maestro completo:
raias, papéis, revisão em contexto fresco, portões, Architecture Decision Records (ADRs),
*skills* e *hooks*. Cada braço acrescenta uma camada ao anterior, e é isso que torna o desenho
útil: a diferença entre dois braços vizinhos isola uma camada. A H1 vive no contraste A × B; a
H5, dentro do C; H3, H6 e H7 ligam e desligam uma peça só dentro do tratamento.

Nem toda hipótese cabe nos quatro braços. A H4 pede um fatorial (um agente ou vários, cruzado
com tarefas de cortes independentes ou acopladas), porque a palavra "só" é uma afirmação sobre
as duas metades da tabela. A H9 também (modelo menor ou maior, tarefa estruturada ou aberta). A
H10 é a mais fraca da agenda: não há como sortear retrospectivas, então ela é observacional,
uma série temporal no corpus de ciclos históricos do Maestro, antes e depois de cada achado
virar regra. O arquivo de hipóteses diz isso com todas as letras, porque um desenho fraco
relatado como forte é o mesmo defeito do portão que mede o proxy.

### O que conta como resultado

Duas regras valem para as dez. A primeira: o ambiente de cada execução fica congelado, com
*commit* do método, modelo, *harness* e *hashes* das entradas (a impressão digital de cada
arquivo: mudou um byte, mudou o *hash*) [CLAIM-93-003], e uma execução sem
esse registro não entra na análise. A segunda: o resultado é uma distribuição com intervalo,
nunca um número só, porque o mesmo agente na mesma tarefa não produz a mesma saída duas vezes.

Daí sai a definição de refutar. Uma hipótese de efeito ("reduz", "acha mais") cai quando o
intervalo do efeito, no contraste declarado, inclui zero ou aponta contra ela. Uma hipótese de
não-inferioridade ("sem perder qualidade", "basta") cai quando a perda passa de uma margem. O
número de repetições, as margens e o nível do intervalo ainda não foram fixados; vão para
`pesquisa/protocolo.md` antes do primeiro *run* e não podem mudar depois de alguém olhar os
dados. Fixar a margem depois de ver o resultado é a versão estatística de reescrever um ADR.

### Cada hipótese tem uma armadilha própria

Escrever "o que a refutaria" obriga a nomear a explicação alternativa que imitaria o efeito.
Três exemplos, todos de [`pesquisa/hipoteses.md`](../../../pesquisa/hipoteses.md):

- **H2.** Se o revisor em contexto fresco gasta mais *tokens* lendo o *diff* do que o autor
  gasta relendo o próprio trabalho, ele pode achar mais defeitos por ler mais, não por ter
  contexto limpo. O desenho iguala o orçamento de revisão; se o ganho some com orçamento igual,
  a hipótese cai na forma em que o livro a enuncia.
- **H1.** A spec pode reduzir o retrabalho e ainda assim encarecer a entrega, se escrevê-la
  custa mais do que o retrabalho que poupa. Por isso a métrica principal é custo por tarefa
  aceita com o custo da spec somado, e não apenas o número de iterações de correção.
- **H4.** A hipótese tem duas metades. Vários agentes que não melhoram nem as tarefas
  independentes refutam a primeira; vários agentes que melhoram também as acopladas refutam o
  "só". O segundo resultado seria o mais interessante, porque contradiz o
  [capítulo 6](../../06-como-dividir-o-trabalho/capitulo.md).

### Onde moram os dados

Os corpora previstos são três: os ciclos históricos do Maestro; o SWE-bench (*issues* reais de
repositórios públicos, julgadas pelos testes da correção original) com a sua variante mais
difícil, o SWE-Bench Pro, de tarefas de horizonte longo; e o ASEG-Bench (nome de trabalho:
governança de *Agentic Software Engineering*, o título em inglês deste livro), um benchmark de
governança com dez casos, de GOV-001 a GOV-010 [CLAIM-93-005], descrito
no [Apêndice B](../b-aseg-bench/capitulo.md). Duas hipóteses já apontam para casos dele: a H6
para o GOV-002 (componente duplicado) e a H8 para o GOV-007 (ação irreversível sem *rollback*).
Cada execução vai para `pesquisa/runs/`, um diretório por *run* com *schema* imutável, e o
protocolo que as governa fica em `pesquisa/protocolo.md` [CLAIM-93-004]. Imutável aqui tem o
mesmo sentido que no Maestro: um *run* errado não se corrige, se registra outro que o
substitui.

Enquanto o protocolo não for ratificado e o primeiro *run* não for commitado, a regra para o
leitor é simples: toda frase deste livro que menciona H1 a H10 é uma hipótese, e o capítulo que
a usa diz isso.

## O protocolo: o que se congela antes do primeiro run

Hipótese sem protocolo é uma pergunta bem escrita. O que a transforma em experimento é um
documento que diz, antes de alguém ver um resultado, como cada execução roda, o que ela registra
e como se lê o conjunto. Esse documento é
[`pesquisa/protocolo.md`](../../../pesquisa/protocolo.md). Em 02/11/2026 ele é um rascunho, versão
0.1, ainda sem a revisão do autor do método e sem nenhum *run* feito sob ele [CLAIM-93-004]. O
que segue é o que ele fixa e por quê.

### A falha que o protocolo existe para evitar

A primeira execução real do ASEG-Bench já aconteceu, e é o melhor argumento a favor
do protocolo. Em 02/11/2026 o caso GOV-004 (ADR reescrito) rodou contra o Claude Code, versão
2.1.316, com o modelo pedido pelo apelido `sonnet`. O *harness* recusou a autenticação antes do
primeiro passo; o agente não fez nada; o avaliador reprovou o rastro por duas violações de
declaração e o deu como conforme quando julgado só pelo estado dos arquivos [CLAIM-93-008].
Isso não é escândalo: é exatamente a aprovação vazia que a coluna `tarefa_resolvida` existe para
pegar.

O problema aparece quando se pergunta se essa execução poderia entrar numa análise. O
`veredito.json` que o *runner* grava tem oito campos: caso, modelo, instruções, *commit*-base do
cenário, tarefa resolvida, erro do *harness*, violações e violações só de estado
[CLAIM-93-007]. A versão do *harness* está só no README da pasta, não no registro. O modelo está
como apelido, e um apelido aponta para versões diferentes ao longo do tempo. Não há hash do
*prompt*, da ficha do caso nem do avaliador; se a ficha mudar amanhã, nada no registro diz
contra qual versão o rastro foi julgado. E o *runner* repete uma vez por padrão [CLAIM-93-007].
Uma execução assim serve para depurar o *runner*. Não serve para afirmar nada sobre um braço.

### Braços e tratamento

O protocolo usa os quatro braços da agenda: A (só o *prompt*), B (mais a especificação), C (mais
os portões executáveis) e T, o Maestro completo instalado no cenário. A unidade é a **célula**:
tarefa, braço, modelo e *harness*. A tarefa, ou seja, o repositório de cenário no mesmo
*commit*-base, o mesmo gatilho e o mesmo critério de aceitação, é idêntica em todas as células
comparadas; muda só o que o braço acrescenta. Desligar uma peça dentro de T (contexto seletivo,
catálogo, glossário) é uma ablação com nome próprio, `T-sem-<peça>`, para que ninguém confunda
"o Maestro sem glossário" com o braço C.

### Repetições com distribuição e intervalo

O protocolo propõe dez repetições por célula no piloto, proporções com intervalo de Wilson a
95 %, e medianas com intervalo *bootstrap* percentil a 95 % sobre 10 000 reamostragens, com a
semente registrada; para as hipóteses de não-inferioridade (H3 e H9), a margem proposta é de
5 pontos percentuais em aceitação na primeira passada [CLAIM-93-006]. Os valores estão marcados
como proposta e congelam no *commit* que registrar o primeiro *run*. A partir daí, mudar um
deles é uma versão nova do protocolo, válida só para os *runs* seguintes.

Três regras valem seja qual for o número:

- **Relata-se a distribuição inteira**: n, mínimo, quartis, máximo e o intervalo. Média sozinha
  não entra no livro.
- **Falha do *harness* conta.** Uma execução que caiu por autenticação ou *timeout* fica
  registrada e fora da métrica da tarefa, mas a taxa de erro por célula é relatada. Repetir até
  dar certo sem registrar as falhas é escolher a amostra.
- **A ordem das células é sorteada**, para que uma mudança no provedor ao longo do dia não se
  confunda com efeito de braço.

### O ambiente congelado

Cada *run* registra, no próprio `run.json`, o *commit* do Maestro instalado (braço T), o *commit*
do repositório do livro (fichas, *runner*, avaliador), o modelo pedido e o modelo **resolvido**,
nome e versão do *harness*, o *commit*-base do cenário, o *hash* Secure Hash Algorithm de 256 bits (SHA-256) de cada entrada (*prompt*,
instruções, ficha, *runner*, avaliador), sistema operacional, versão do interpretador e a semente.
Se o *harness* não relata o modelo resolvido, o *run* entra marcado `modelo_nao_verificado`.
Sem esses campos o *run* não entra na análise. É a lista do que faltava no `veredito.json` da
seção anterior.

### O *schema* imutável de `runs/`

Um diretório por *run* em `pesquisa/runs/`, com `run.json`, `prompt.txt`, `rastro.json`,
`veredito.json` e, opcionalmente, `telemetria.jsonl`. O `run.json` declara a versão do *schema*
e a versão do protocolo sob a qual rodou. Imutável quer dizer quatro coisas: diretório commitado
não se edita nem se apaga; *run* errado se corrige com outro *run* cujo campo `substitui` aponta
o errado; campo novo exige versão nova do *schema*, e os *runs* antigos continuam lidos como
estão; e os *runs* são commitados **antes** de a análise rodar, para que ninguém escolha quais
entram depois de ver o resultado.

Aqui o protocolo é franco sobre o próprio limite: o portão que faria valer a imutabilidade
(`scripts/check-runs.sh`, conferindo por *diff* que nada sob `runs/` mudou) ainda não existe.
Até existir, a imutabilidade é regra escrita, não fato verificado. No vocabulário do
[capítulo 10](../../10-quality-gates-que-provam-fatos/capitulo.md), é intenção sem portão.

### Telemetria compatível com OpenTelemetry, com minimização

Custo, *tokens*, tempo e overhead de coordenação se medem com *spans* exportáveis por
OpenTelemetry (OTel): um por *run*, por chamada ao modelo, por chamada de ferramenta, por portão,
por espera humana e por mensagem entre agentes. Os atributos usam os nomes das convenções
semânticas de IA generativa do OTel (`gen_ai.*`) quando existem, com a versão das convenções
registrada, porque elas ainda estão em desenvolvimento, e um prefixo próprio (`esoa.*`) para
braço, hipótese, tarefa e repetição.

O que **não** se registra pesa tanto quanto o que se registra. A Lei Geral de Proteção de Dados
(LGPD) põe a necessidade entre os princípios do tratamento: coleta-se o mínimo para a
finalidade. Medir custo e tempo não precisa do conteúdo do *prompt*, da resposta, dos arquivos
nem da saída dos comandos; não precisa de caminhos absolutos, de nome de usuário nem da
descrição da máquina. Por padrão, então, a telemetria guarda contagens, durações, nomes de
ferramenta, códigos de saída e hashes. O conteúdo necessário para auditar um *run* já está em
`prompt.txt` e `rastro.json`, de cenários sintéticos, revisados. O log bruto do *harness* não se
publica, pela razão que o benchmark já documenta: a primeira linha do log do Claude Code
descreve a máquina, com servidores e caminhos de memória. Quem quiser auditar o log refaz o
*run* com o mesmo ambiente congelado. Rastrear não é reter tudo.

## Como reproduzir um claim deste livro

Os *runs* ainda não existem, mas os claims existem, e esta é a parte do pacote que você já pode
usar. Cada capítulo tem um `claims.md`; a consolidação de todos, em `pesquisa/CLAIMS.md`,
somava 645 claims em 03/11/2026 [CLAIM-93-009]. Cada linha tem quatro colunas: o id, a
afirmação, o estado e a evidência reproduzível.

**O estado diz quanto a frase aguenta.**

| Estado | O que significa | O que você faz com ele |
|---|---|---|
| `medido` | um comando produz o número | rode o comando; o número tem de bater |
| `observado` | um arquivo ou *commit* registra o fato, sem contagem automática | abra o arquivo no *commit* indicado e leia |
| `observado (autodeclarado)` | o número é o balanço escrito pelo autor do método, não uma contagem | trate como depoimento datado |
| `hipótese` | aposta, H1 a H10 ou similar | não use como fato; veja o protocolo |

**A evidência diz onde rodar.** Há dois formatos:

- `git show 19823c2:<caminho>` ou `git ls-tree … 19823c2 …` roda num clone do Maestro. O
  *commit* `19823c2` é a versão de referência do livro inteiro; rodar em outro *commit* mede outra
  coisa.
- `livro: <comando>` roda na raiz do repositório deste livro (por exemplo, os `sed -n` sobre
  `pesquisa/base-de-pesquisa.md`, ou um `exemplo/` com `--conferir`).

O roteiro, de ponta a ponta:

```bash
# 1. o método na versão de referência
git clone https://github.com/GHDaru/maestro.git && cd maestro
git cat-file -t 19823c2                      # → commit (em 03/11/2026: ainda falha, ver acima)

# 2. um claim medido do prefácio (CLAIM-00-008: oito princípios)
git show 19823c2:docs/governance/principles.md | grep -cE '^### [IVX]+\.'   # → 8

# 3. no repositório do livro: todo id citado está registrado, e vice-versa
scripts/check-claims.sh                      # saída 0 = conforme; 1 = lista pastas e ids
grep -n 'CLAIM-00-008' pesquisa/CLAIMS.md    # a linha com a afirmação e o comando
```

O passo 3 confere a forma, não o conteúdo: `scripts/check-claims.sh` garante que todo id citado
num `capitulo.md` está no `claims.md` da mesma pasta, que todo id registrado é citado e que o id
tem a forma `CLAIM-NN-NNN`, mas não roda a coluna de evidência. O portão varre o livro inteiro;
se sair com 1, ele imprime as pastas com desvio e os ids recusados, e a deste apêndice
(`livro/apendices/c-pacote-de-replicacao`) não pode estar na lista. Os apêndices usam um número
no lugar da letra (o B é `92`, este é `93`, o D é `94`) justamente porque o portão só aceita dois
dígitos; uma versão anterior deste apêndice usava `0C` e o portão a recusou, que é o portão
fazendo o seu trabalho. Conferir o número é o passo 2, claim a claim.

### O roteiro num script só

Os três passos estão juntos em
[`exemplo/conferir_pacote.py`](exemplo/README.md), em Python 3 e Git, sem dependências e sem rede.
Com `--conferir --maestro <clone>`, ele roda a evidência de quatro claims, três deste apêndice e um do
prefácio (a versão de referência existe no clone, os oito princípios, as versões do
`CHANGELOG.md` e as tags, os oito campos do veredito) e confere os ids do apêndice nos dois
sentidos. Cada linha sai como `OK`, `FALHA` ou `PULA`, com o valor obtido ao lado do esperado; a
saída do processo é 0 quando nada falha. O `README.md` da pasta traz as duas saídas esperadas: a
do clone do autor, toda verde, e a de um clone sem o *commit* `19823c2`, com a falha no primeiro
item. Rode-o antes de citar qualquer número deste livro numa decisão. Se o comando não
reproduzir o número, o claim está errado até prova em contrário, e a regra do guia editorial vale
para o autor: número que não se reproduz vira hipótese ou sai.

Quando os primeiros *runs* existirem, um claim `medido` sobre H1–H10 terá na coluna de evidência
o comando da análise e os `id`s dos *runs* usados, e o roteiro ganha um passo: refazer um *run*
com os campos congelados do `run.json` e ver se o resultado cai dentro do intervalo relatado.

## Monte o pacote do seu time

Conferir o autor é a metade passiva. A outra metade é o seu time fazer o mesmo com as próprias
afirmações, sem esperar os *runs* deste livro. O caminho mínimo cabe numa semana e usa as mesmas
peças, em escala de um time:

1. **Escolha uma afirmação que o time já faz.** De preferência uma que já decide alguma coisa:
   "a revisão por um agente sem o contexto do autor acha defeito que o autor não acha". Escreva,
   antes de rodar, o que se mede, contra o quê e que resultado a derrubaria.
2. **Fixe o protocolo numa página, com data e *commit*.** Número de repetições, métrica,
   critério de refutação. O piloto do protocolo deste livro propõe dez repetições por célula
   [CLAIM-93-006]; com dois braços (sem e com a prática) e uma tarefa, são vinte execuções.
3. **Uma pasta por execução, com o `run.json` preenchido antes de rodar.** O molde é
   [`exemplo/run-modelo/`](exemplo/README.md): o `run.json` no *schema* 1 do protocolo, já
   preenchido com os *hashes* reais do *prompt*, da ficha, do *runner* e do avaliador do caso
   GOV-004, e o `prompt.txt` que o agente recebeu. Troque os valores pelos do seu cenário.
4. **Valide antes de contar.** `python conferir_pacote.py --validar-run <pasta>` diz se a
   execução entra na análise. O exemplo traz o contraste com dados reais: o `run-como-veio/` é o
   `veredito.json` da primeira execução do ASEG-Bench, tal como o *runner* o gravou, e o
   validador recusa onze campos do ambiente congelado; o `run-modelo/` entra, com a marca
   `modelo_nao_verificado`, porque o modelo resolvido não foi relatado [CLAIM-93-015]. A
   execução recusada continua registrada; ela só não entra na conta.
5. **Commite as execuções antes da análise**, e relate a distribuição inteira com o intervalo.
   O número que sair vai para o texto com um id de claim e o comando que o refaz.

Se ao fim da semana o time tiver vinte pastas, um protocolo datado e um número com intervalo, ele
tem um pacote de replicação. Se tiver uma frase convincente na retrospectiva, tem um depoimento.

## Quando um pacote assim não compensa

O pacote tem custo: escrever o protocolo antes, calcular *hashes*, guardar cada execução,
repetir até ter distribuição. Há casos em que esse custo é maior do que o erro que ele evita.

- **A decisão é barata de desfazer.** Se o time pode adotar uma prática por duas *sprints* e
  voltar atrás sem perda, a própria adoção é o experimento, e a retrospectiva basta. O pacote se
  paga quando a decisão é cara: trocar o fluxo de vários times, contratar com base num número,
  publicar uma afirmação.
- **A pergunta é local.** "Isso funciona para nós, neste repositório?" se responde observando o
  repositório. O protocolo com braços e repetições serve à pergunta geral, "isso funciona?",
  que é a deste livro e raramente a de um time.
- **O volume não existe.** Com poucas tarefas comparáveis, as repetições não formam uma
  distribuição útil, e um intervalo largo demais não decide nada. Melhor declarar a afirmação
  como observação do que vesti-la de medida.
- **O modelo muda mais depressa do que o experimento roda.** Se o provedor troca o modelo por
  baixo do apelido no meio da coleta, as células deixam de ser comparáveis. Sem o modelo
  resolvido no registro, o pacote congela tudo menos o que mais varia.
- **O pacote vira cerimônia.** Um protocolo sem *run*, um validador sem execução para validar, um
  `run.json` que ninguém lê: é o artefato sem função forçante que o próprio Maestro manda podar.
  Este apêndice corre esse risco hoje, e as camadas 3 e 4 só deixam de ser cerimônia no dia do
  primeiro *run*.

## Checklist de replicação

Cada item tem um jeito de ser conferido sem perguntar ao autor. Aplique-o a este livro ou a
qualquer afirmação que o seu time faça sobre o próprio processo com agentes.

- [ ] **A versão é um *commit*.** `git cat-file -t 19823c2` num clone do Maestro devolve
  `commit`; todo link ao método aponta para `blob/19823c2/…`, nunca para `main`.
- [ ] **A instalação foi ensaiada antes.** O instalador do método lista o que escreveria sem
  escrever, e o agente da lista é o mesmo que o *run* declara. No Maestro:
  `scripts/install-maestro.sh <cenário> --ai <id> --dry-run`.
- [ ] **A cópia instalada é coerente.** Instalado num diretório vazio, todo script enviado roda e
  todo caminho citado existe; senão o braço de tratamento mede o instalador. No Maestro:
  `scripts/check-installed.sh` sai com código zero no *commit* usado.
- [ ] **A escolha do agente ficou gravada.** Um arquivo no destino diz agente, *harness*, versão
  do método e data, e entra no registro do *run*. No Maestro: `.maestro/install-options.json`.
- [ ] **O protocolo foi fixado antes dos dados.** Repetições, margens e nível do intervalo estão
  em `pesquisa/protocolo.md` com data anterior ao primeiro `run.json`.
- [ ] **O ambiente está congelado no próprio *run*.** O `run.json` traz *commit* do Maestro,
  *commit* do cenário, modelo resolvido (não o apelido), versão do *harness* e os *hashes*.
- [ ] **O resultado vem com distribuição.** Nenhum número de H1–H10 aparece sem as repetições e o
  intervalo; um único *run* é anedota.
- [ ] **Todo número do texto tem id.** `scripts/check-claims.sh` não lista a pasta do capítulo
  entre as com desvio, e sai com código zero quando o livro inteiro está conforme;
  `exemplo/conferir_pacote.py --conferir` confere o mesmo para este apêndice.
- [ ] **Uma amostra de claims foi rodada.** Escolha alguns claims `medido`, rode a coluna de
  evidência e compare; um que não bate vira hipótese ou sai.
- [ ] **O estado do claim foi respeitado.** Nada marcado `hipótese` ou `observado
  (autodeclarado)` sustenta uma decisão como se fosse medida.

## Limites deste pacote

**Um repositório, um autor.** Quase toda evidência deste livro vem do próprio Maestro,
desenvolvido pela pessoa que o descreve. Um pacote de replicação torna essa evidência
conferível; não a torna independente. Independência só chega quando outro time instala o método
e publica os próprios *runs*.

**O protocolo é rascunho e os *runs* não existem.** Até 02/11/2026 nenhuma hipótese foi testada
com o desenho completo [CLAIM-93-004]. Este apêndice descreve o que se congelaria, e cada valor
proposto pode mudar até a ratificação [CLAIM-93-006]. Quem ler isto depois dessa data deve
conferir a tabela «Estado» no fim de `pesquisa/protocolo.md` antes de assumir qualquer coisa.

**A instalação depende do *harness*.** A camada de *hooks* existe para um agente e não para os
outros [CLAIM-93-011]. Um resultado obtido com `--ai claude` não se transfere automaticamente
para `--ai codex`, porque o tratamento é outro. O argumento do livro pretende sobreviver à troca
do *harness*; essa pretensão é ela mesma uma hipótese.

**O portão confere coerência, não eficácia.** `check-installed.sh` prova que a cópia chega
inteira [CLAIM-93-012], e `check-claims.sh` prova que cada id citado está registrado. Nenhum dos
dois prova que o método funciona ou que o número está certo. A segunda prova é sua: rodar a
evidência.

**A versão de referência ainda não é pública.** Em 03/11/2026 o *commit* `19823c2` não está em
nenhuma *branch* do repositório público [CLAIM-93-014]. Até estar, todo claim cuja evidência
começa por `git show 19823c2:` é conferível só na máquina do autor, e a epígrafe deste apêndice
vale contra ele mesmo.

**Não há *release* para citar.** A referência é um *commit* posterior à última versão numerada
[CLAIM-93-013]. Reproduzir funciona; comparar com "a versão anterior" exige ler o histórico do
`CHANGELOG.md`.

**O log bruto não é publicado.** Por minimização, o pacote guarda contagens, durações e o rastro
revisado, não a primeira linha do log do *harness*, que descreve a máquina. Quem quiser auditar o
log refaz o *run*.

**O modelo muda por baixo.** Um apelido como `sonnet` aponta para modelos diferentes ao longo do
tempo, e o *runner* atual não grava o modelo resolvido [CLAIM-93-007]. Até isso mudar, um *run*
refeito meses depois com o mesmo comando pode estar medindo outro modelo.

## Referências

Maestro, no *commit* de referência `19823c2`:

- [`scripts/install-maestro.sh`](https://github.com/GHDaru/maestro/blob/19823c2/scripts/install-maestro.sh) — o instalador canônico e suas opções.
- [`scripts/check-installed.sh`](https://github.com/GHDaru/maestro/blob/19823c2/scripts/check-installed.sh) — o portão que instala num diretório vazio e exercita o resultado.
- [`docs/receitas/instalar-o-maestro.md`](https://github.com/GHDaru/maestro/blob/19823c2/docs/receitas/instalar-o-maestro.md) — caminhos de instalação, `maestro init` e a árvore de uma instalação real.
- [`CHANGELOG.md`](https://github.com/GHDaru/maestro/blob/19823c2/CHANGELOG.md) — as versões 0.1.0, 0.2.0 e 0.3.0.
- [`docs/governance/principles.md`](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/principles.md) — os oito princípios usados no exemplo de reprodução.

Neste livro:

- [`pesquisa/base-de-pesquisa.md`](../../../pesquisa/base-de-pesquisa.md) — a agenda H1–H10, os quatro braços e o que o repositório deve conter.
- [`pesquisa/hipoteses.md`](../../../pesquisa/hipoteses.md) — métrica, desenho e condição de refutação de cada hipótese.
- [`pesquisa/protocolo.md`](../../../pesquisa/protocolo.md) — o protocolo 0.1, rascunho não ratificado.
- [`pesquisa/CLAIMS.md`](../../../pesquisa/CLAIMS.md) — a consolidação de todos os claims.
- [`pesquisa/benchmarks/aseg-bench/`](../../../pesquisa/benchmarks/aseg-bench/) — o *runner*, o avaliador e a primeira execução.
- [`livro/guia-editorial.md`](../../guia-editorial.md) — a regra de evidência e os estados de um claim.
- [Capítulo 10 — *Quality gates* que provam fatos](../../10-quality-gates-que-provam-fatos/capitulo.md) — o check que mede o proxy, não o fato.
- [Capítulo 15 — Validando o Maestro](../../15-validando-o-maestro/capitulo.md) — o SWE-bench, o SWE-Bench Pro e os corpora externos.
- [`exemplo/`](exemplo/README.md) — `conferir_pacote.py`, o molde `run-modelo/` e o registro `run-como-veio/`, com as saídas esperadas.

Práticas de reprodutibilidade comparadas:

- Association for Computing Machinery (ACM). *Artifact Review and Badging*, versão 1.1, 2020 — os selos de artefato e a distinção entre resultado reproduzido e replicado.
- Nosek, B. A.; Ebersole, C. R.; DeHaven, A. C.; Mellor, D. T. *The preregistration revolution*. Proceedings of the National Academy of Sciences, 115(11), 2018, p. 2600–2606.
- Gebru, T. et al. *Datasheets for Datasets*. Communications of the ACM, 64(12), 2021.
- Mitchell, M. et al. *Model Cards for Model Reporting*. Conference on Fairness, Accountability, and Transparency (FAT\*), 2019.
