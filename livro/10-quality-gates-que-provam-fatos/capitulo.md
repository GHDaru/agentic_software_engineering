# 10 — Quality gates que provam fatos

> "Um check que você nunca viu acusar não é um check — é uma esperança."
> — segunda lei da skill `verifiable-dod`, Maestro

Quando o agente escreve o código, o seu time deixa de ser o gargalo de produção e passa a ser o
gargalo de verificação. A saída óbvia é automatizar a verificação: portões na integração
contínua, checklists executáveis, ganchos que barram o agente antes de ele dizer "pronto". Este
capítulo é sobre o que acontece depois disso, quando os portões existem, estão verdes e mesmo
assim o defeito passa. A tese é desconfortável: com agentes, a qualidade deixa de falhar porque
"o agente errou" e passa a falhar porque **o portão mede a coisa errada**. Se você vai apostar a
sua revisão em portões, precisa saber provar que eles medem o fato.

## Pergunta central

O que acontece quando o check mede o *proxy* e não o fato, e como se prova que um portão mede o
fato antes de confiar nele?

## Resultado de aprendizagem

Ao final, você consegue:

1. **Reescrever** um critério de aceite vago como um par (comando, resultado esperado) ou como
   requisito no formato de sintaxe controlada, ou então **declará-lo** gate humano. Vago não fica.
2. **Diagnosticar** um portão que mede o proxy, reconhecendo as formas recorrentes: texto em vez
   de artefato, linha em vez de item, existência em vez de unicidade, "limpo" que na verdade é
   "não olhei", palavra em vez de número, e o portão que morre calado.
3. **Provar** um portão por mutação, com propriedade, fixture positiva, fixture negativa,
   fixture legítima e resultado esperado, e classificá-lo como portão ou decoração.
4. **Decidir** o que bloqueia, o que é consultivo e o que fica com o julgamento humano ou com
   uma linha de base registrada.
5. **Escolher** as métricas que mostram se os seus portões estão funcionando (escape de gate,
   aceitação na primeira passada), sem transformá-las em meta.

## A falha real

Em 22 de agosto de 2026, a sessão regente do Maestro promoveu para a linha principal os ciclos
061 e 062. O script que existe para impedir que uma caixa marcada valha por prova, o
`check-conformance.sh`, rodou e imprimiu, entre outras, esta linha:

```text
✓ TAIL:review evidence: pendente.
```

E promoveu [CLAIM-10-001]. Leia de novo: o portão deu visto verde para uma evidência cujo
conteúdo era a palavra que **declara a ausência da evidência**. A revisão independente dos dois
ciclos não tinha rodado. O próprio relatório de cada ciclo dizia isso.

A ironia piora quando se sabe por que aquele portão bloqueava. Nos quatro ciclos anteriores,
057 a 060, a revisão independente tinha achado o mesmo par de defeitos, ciclo após ciclo: as
quatro caixas da cauda de fechamento marcadas sem que o `qa-report.md` existisse, e o pacote do
plugin não reconstruído [CLAIM-10-003]. O portão que leria essa evidência era consultivo, e nada
barrava. A retrospectiva do ciclo 061 respondeu do jeito certo: transformou a metade do portão
que podia bloquear sem ficar vermelha o tempo todo (o modo `--ticked-only`, que só cobra caixa
marcada) em passo bloqueante da integração contínua (CI, de *continuous integration*). No
ciclo seguinte, esse portão, recém-promovido a guarda, deixou passar a palavra "pendente".

A investigação do ciclo 063 mediu antes de escrever. A função `is_placeholder()`, que decide se
um texto conta como evidência, reconhecia três coisas: texto vazio, texto que começa com `<` e
texto que começa com `[` [CLAIM-10-002]. Ou seja, reconhecia **a forma que o gerador de ciclo
escreve**, o marcador `<evidência aqui>`, e não a ausência de evidência. Qualquer frase escrita
por gente passava, inclusive a frase "isto não foi feito". É o anti-padrão 13 do catálogo do
Maestro, o "check que mede o proxy e não o fato", dentro do portão escrito para pegá-lo
([spec 063](https://github.com/GHDaru/maestro/blob/19823c2/specs/063-pendente-nao-e-evidencia/spec.md)).

A correção também não era óbvia, e é aqui que a história ensina mais. Uma busca solta pela
palavra "pendente" reprovaria a evidência legítima do ciclo 060, que continha a palavra no meio
de uma frase verdadeira. E reprovar retroativamente os quatro ciclos de 042 a 045, que tinham
escrito "pendente" quando aquilo **era verdade** e foram promovidos depois, transformaria o
portão em ruído [CLAIM-10-006]. A correção final teve quatro peças: um vocabulário **fechado**
de ausência declarada, nos dois idiomas do repositório; a leitura **do início** da evidência,
nunca de qualquer posição; um **piso** (o ciclo 061) abaixo do qual a dívida fica declarada e
não apagada; e uma proteção para o próprio piso, que reprova se for posto acima do ciclo mais
novo ou se não for número — "botão que desliga tudo e ainda imprime sucesso não é botão, é
interruptor", nas palavras da spec.

O segundo parecer em contexto fresco ainda reprovou a primeira versão da correção: achou cinco
defeitos que o próprio autor tinha introduzido ([commit
`2ad52df`](https://github.com/GHDaru/maestro/commit/2ad52df)) e cinco grafias que contornavam a
regra nova — `ainda não executada`, `não executadas`, `(pendente)`, `> pendente`, `NÃO EXECUTADA`
[CLAIM-10-004, CLAIM-10-005]. O exemplo executável deste capítulo reproduz exatamente essas
mutações.

Não foi um acidente isolado. Seis ciclos antes, a retrospectiva do ciclo 055 tinha contado: em
**seis dos nove** ciclos de 046 a 054, a revisão independente achou o mesmo defeito — portão que
mede a frase e não o fato [CLAIM-10-007]. E já no ciclo 017, a primeira retrospectiva executada
do método, a frase-síntese tinha sido escrita: os ciclos 003 a 016 estavam todos marcados como
conformes, e **nenhum deles falhou no que verificava — falharam no que não verificavam**
[CLAIM-10-008]. A pergunta deste capítulo nasce daí. Se o seu time vai trocar leitura humana por
portões, o risco principal deixa de ser o agente que erra. Passa a ser o portão que diz verde
sobre um mundo que ele não olhou.

## Teoria

### O teorema: critério sem comando não é critério

O livro deriva este capítulo de dois teoremas do Maestro. O primeiro é o teorema T4, que nasce
de dois axiomas: alguém responde pelo resultado (axioma A2, a consequência precisa de dono) e só
o que está escrito sobrevive à sessão seguinte (axioma A4). Logo, "pronto" precisa produzir uma
evidência que uma máquina consiga confirmar. Do contrário, "pronto" significa o que o leitor
supôs, e a responsabilidade não tem onde se prender
([axioms.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/axioms.md)).

O Princípio IV da constituição do método diz o mesmo em linguagem de operação: *prove it, don't
claim it*. A Definition of Done (DoD) é verificável de forma autônoma quando é um pass/fail que o
agente produz e um gancho confirma, sem depender de você estar na sala
([principles.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/principles.md)).
O corolário prático é duro e simples: **critério sem comando é desejo**. Se o critério não se
automatiza, ele não fica vago; ele é marcado explicitamente como gate humano, com nome e dono.

A pergunta que resolve quase tudo é "que comando prova isto?". Há duas formas boas de responder.
Para comportamento, o requisito no formato Easy Approach to Requirements Syntax (EARS) —
`QUANDO <condição> O SISTEMA DEVE <comportamento observável>` — vira teste quase um para um: a
condição é o preparar e agir, o comportamento é a asserção. Para estrutura ou invariante, o par
(comando, esperado): `grep -L "Iron Law" skills/*/SKILL.md` com resultado esperado vazio. A
ordem de preferência é teste automatizado, depois `grep`/`ls`/contagem, e por último inspeção
humana, declarada como gate humano. E o invariante de segurança vira **check negativo**: o que
não pode existir é uma busca que deve voltar vazia — por exemplo, nenhum agente somente-leitura
com permissão de escrita na lista de ferramentas
([receita do handbook](../../maestro-handbook/receitas/escrever-criterio-verificavel.md)).

Converter julgamento em check é o trabalho de engenharia que este teorema pede. "Código limpo"
vira análise estática e regra de dependência executável (uma *fitness function*, ver o
[capítulo 9](../09-arquitetura-que-se-defende/capitulo.md)). "Boa experiência de uso" vira
captura gerada do build real com heurística datada. "Seguro" vira varredura de segredos.
"Documentado" vira portão no pull request. O que não converte fica humano, e dizer isso é uma
resposta honesta, não uma falha.

### O proxy: quando o check mede uma coisa parecida com o fato

Escrever o comando é necessário. Não é suficiente. O comando pode medir algo que *costuma
andar junto* com o fato — o proxy — e passar quando o fato está ausente. O catálogo do Maestro
registra isso como anti-padrão 13 e lista sintomas: casa o texto em vez do artefato, conta
linhas em vez de itens, confirma que a seção existe em vez de que foi atualizada
([anti-patterns](https://github.com/GHDaru/maestro/blob/19823c2/skills/anti-patterns/SKILL.md)).
Vale olhar as formas uma a uma, porque cada uma tem um antídoto diferente. Todas são datadas.

**Texto em vez de artefato.** No ciclo 015, o primeiro check da DoD para um widget injetado nas
páginas do livro foi `grep -l companion site/*.html`. Deu verde. Casava com menções legítimas à
palavra "companion" no texto, não com a injeção do widget. Foi a primeira ocorrência registrada
do que viria a ser o anti-padrão 13. A mesma armadilha reaparece num exemplo que o próprio
método usa para ensinar: um `grep` pela palavra *superseded* fica verde quando alguém escreve
"revogado". No ciclo 049, o portão novo do índice de decisões casava o nome do arquivo em
qualquer lugar do README (linha comentada e prosa passavam), parava na primeira linha e media o
status de superado por palavra mágica; a revisão independente reprovou. O registro diz:
"anti-padrão 13 escrito por quem o cita".

**Linha em vez de item.** No ciclo 016, o check de fontes `grep -c "https://"` contou linhas, não
URLs (Uniform Resource Locator), e reportou 5 onde havia 6 [CLAIM-10-011]. No ciclo 025, a
medição de quantos ciclos usavam o laço avaliador-otimizador foi um `grep -rl` com uma redação
só; achou 2 ciclos onde havia 4, porque a frase variava [CLAIM-10-012]. Contagem é afirmação: se
o comando conta a coisa errada, ele afirma errado com a autoridade de um número.

**Existência em vez de unicidade.** No ciclo 014, ao criar a quinta trilha de navegação, os cinco
`README.md` do livro passaram a gerar o mesmo endereço de página, e o último sobrescrevia os
outros em silêncio [CLAIM-10-013]. O portão de links não acusou, porque o alvo existia.
Verificar que o link resolve não é verificar que ele resolve para a página certa. Nasceu o
portão de colisão, provado com uma colisão injetada.

**A seção existe, mas não foi atualizada — ou o detector mede a frase.** No ciclo 022, a
primeira versão do verificador de capítulos reconhecia um capítulo migrado pela frase "migrado
ao padrão v2". Ao provar o modo "datação fora do padrão", o capítulo **saiu do check** — a
frase morava na linha alterada — e o script deu verde. O verificador foi provado falhando em
quatro modos, e o quarto só apareceu porque alguém insistiu [CLAIM-10-014]. A correção trocou a
detecção pela frase por detecção pela estrutura. No ciclo 030, o mesmo verificador estrutural
achou uma seção "6b" enxertada fora do esqueleto editorial desde o ciclo 008, que tinha
sobrevivido a duas revisões humanas [CLAIM-10-015].

**"Limpo" que na verdade é "não olhei".** No ciclo 045, o portão que reprova caixas de critério
na spec só pegava `- [ ]` na coluna zero. Caixa indentada, marcador `*` ou `+` passavam, e
quando a seção não era localizada o portão não distinguia "limpo" de "não olhei" — violação do
corolário C5 ("um portão cobre a família inteira ou não cobre nada", tratado adiante) dentro
do ciclo que o cita. A regra que sai daí é simples de dizer: **entrada vazia
tem de reprovar**. O caso "pendente." do ciclo 063 é a versão mais refinada da mesma falha. Os
números do README são outra: no ciclo 060, contagens anunciadas (subagentes, skills, scripts)
não eram comparadas com o disco por portão nenhum, e os identificadores do instalador ficaram
errados por três ciclos [CLAIM-10-050]; no ciclo 064, a função que extraía contagens só
reconhecia certos substantivos e ignorava o resto em silêncio, de modo que uma página anunciando
"42 capítulos" passaria verde [CLAIM-10-029]. No mesmo ciclo, a revisão mediu que o extrator de
tabela errava **nos dois sentidos** conforme a formatação: com tabela indentada, dizia que a
página não publicava tabela nenhuma; com uma tabela dentro de bloco de código, contava como
publicação real.

**Palavra em vez de número.** No ciclo 076, a primeira versão de um aviso de consumo multiplicava
a fração por 100 duas vezes e anunciava "9446 %" para um consumo de 94,5 % [CLAIM-10-018]. A
régua do teste de interface passava, porque cobrava a palavra "limite" e não a frase inteira. O
registro do ciclo diz a lição melhor do que eu: o número **é** a afirmação. O antídoto foi
cobrar a frase inteira com o número.

**Arquivo em vez da linha que declara.** No ciclo 050, a nota de release da v0.2.0 afirmava que
a raia leve não tinha sido feita (ela existia e tinha sido usada) e o portão novo de versão lia
o arquivo em vez da linha que declara a versão, ficando verde com a capa anunciando a versão
errada. O registro fecha com uma frase que este capítulo retoma no contraexemplo: nenhum portão
cobre veracidade de prosa.

**O portão que morre calado.** Esta é a forma mais traiçoeira, porque o portão nem chega a medir.
Em shell com `set -o pipefail`, um `grep -q` no fim de um pipe sai no primeiro acerto, o
comando anterior recebe o sinal de cano quebrado (SIGPIPE) e o pipeline inteiro é dado como
falho. A condição lê "não achou", sempre, em silêncio. No ciclo 034, o `check-cycle.sh` morria
assim quando uma substituição não achava nada — e um check que morre parece um check que
passou. No ciclo 041, a mesma forma matou o `retro.sh`, que passou a reportar todo ciclo do 011
em diante como gate pendente, por 29 ciclos [CLAIM-10-019]; pela regra de reincidência, virou o
anti-padrão 21. No ciclo 048, a terceira ocorrência: sem pasta `specs/`, um `ls` num pipe
matava o `check-retro.sh` numa instalação nova, com código de saída 2 e nenhuma linha de saída
[CLAIM-10-049].
No ciclo 057, a revisão independente reprovou o ciclo com 16 achados [CLAIM-10-026] — entre
eles, uma instalação correta para outro assistente de código ficava vermelha para sempre — e a
mutação achou mais um defeito do autor, outra vez `pipefail` com SIGPIPE fazendo a condição ler
falso. No ciclo 063, o registro de achados mediu que o anti-padrão 21 tinha sido fechado
pontualmente **sete vezes** e reaparecido todas, com quatro ocorrências ainda vivas
[CLAIM-10-020]. Uma variante de portabilidade pertence à mesma família: no ciclo 045, o portão
usava `\|` numa expressão básica do `sed`, extensão que só o `sed` do projeto GNU (GNU's Not
Unix) entende; no `sed` da família Berkeley Software Distribution (BSD), o do macOS, a condição
nunca abriria e o portão ficaria verde em toda spec — invisível na CI, que roda em Linux.

Essa lista é o argumento central da pesquisa que sustenta este livro: em engenharia com agentes,
**a qualidade migra de "o agente errou" para "o gate mede a coisa errada"**. O defeito não some.
Ele muda de endereço, e o novo endereço é o seu portão.

### A segunda lei: prove o check vendo-o falhar

Se o proxy é o problema, o antídoto não é "escrever portões com mais cuidado". É um procedimento.
O corolário C2 do Maestro, derivado de T4, diz: prove a checagem vendo-a falhar. Na skill que o
opera, ele aparece como segunda lei: **um check que você nunca viu acusar não é um check — é uma
esperança**. Antes de confiar num portão novo, quebre o mundo de propósito — injete a colisão,
apague o arquivo, deixe a data vencida — e veja o vermelho
([verifiable-dod](https://github.com/GHDaru/maestro/blob/19823c2/skills/verifiable-dod/SKILL.md)).
A lei nasceu na retrospectiva do ciclo 017, junto com os anti-padrões 13 a 15, depois que os
casos que a motivaram passaram felizes medindo a coisa errada.

É o vermelho-antes-do-verde do Test-Driven Development (TDD) aplicado à verificação, e é também
um parente direto do teste de mutação de código, que a literatura conhece desde o fim dos anos
1970: introduza defeitos pequenos e deliberados e veja se a suíte os mata; mutante que sobrevive
mostra o que a suíte não mede. A diferença aqui é o alvo. Em vez de mutar o código para testar
a suíte, você muta **o mundo que o portão inspeciona** para testar o portão. Mutação que
sobrevive é o portão dizendo verde sobre um mundo quebrado. Por isso a regra separa portão de
decoração: quebre de propósito o que ele deveria pegar; se continuar verde, nunca protegeu
nada.

A forma estruturada que este livro propõe, e que o exemplo executável implementa, tem quatro
partes: **propriedade** (o fato que o portão afirma), **fixture positiva** (o mundo certo, onde
ele deve passar), **fixtures negativas** (mutações do mundo, onde ele deve reprovar) e
**resultado esperado**. Acrescento uma quinta, que a história do ciclo 063 obriga: a **fixture
legítima**, um mundo certo de forma incômoda que o portão não pode reprovar. Sem ela, você
troca um portão que deixa passar por um portão que reprova a verdade — e portão de falso
vermelho é portão que se aprende a ignorar.

O procedimento rende. No ciclo 020, o laço avaliador-otimizador aplicado ao portão de links
rodou quatro vezes dentro do mesmo ciclo, e cada volta achou um formato de link que o portão
ignorava; com a reescrita desligada de propósito, o portão novo acusou 38 links `.md` crus
[CLAIM-10-017]. Os relatórios de qualidade dos ciclos 017, 018, 020 e 021 registram portão
provado falhando antes de ser aceito [CLAIM-10-017]. No ciclo 021, o `check-install.sh` nasceu vermelho na
primeira execução e acusou uma deriva de três ciclos: uma skill existia sem ser citada na
instrução que a inteligência artificial (IA) lê [CLAIM-10-035].

### A família: um portão cobre a família inteira ou não cobre nada

O segundo padrão de falha é o portão certo para um caso e cego para os irmãos. O corolário C5
do Maestro: um gate cobre a família inteira ou não cobre nada. A origem é o ciclo 020: a imagem
do diagrama de processo nunca aparecia no site publicado, porque o motor do livro não copiava
imagens e o portão de links só validava `<a href>`. Corrigido, ainda ignorava `.md` não
reescrito — terceira ocorrência do anti-padrão 13. Virou o anti-padrão 16, com um antídoto
operacional: ao escrever o portão, **enumere a família** — em HyperText Markup Language (HTML),
todo atributo que vira requisição (`href`, `src`, `srcset`, `poster`); num esquema, todo campo
obrigatório; num diretório, toda extensão publicada — e prove a falha **para cada** membro.

A família aparece em toda escala. No ciclo 019, o verificador de papéis do ciclo 018 não pegou
que o registro de decisão e o relatório de qualidade, usados em todo ciclo desde o 003, não
tinham template: ele só olhava artefatos marcados "essencial". Um check fecha uma classe e deixa
a vizinha aberta. No ciclo 033, um renome em massa por substituição de texto casou dentro de um
registro de decisão não renomeado e criou caminho inexistente em catorze arquivos
[CLAIM-10-016]; quem acusou foi o portão de links, não a leitura, e o portão foi estendido para
validar todo link relativo do repositório, não só as páginas publicadas (anti-padrão 18). No
ciclo 034, a primeira versão desse `check-links.sh` contava como link um `![...](...)` escrito
como exemplo dentro de crase — mediu o texto, não o link; foi a terceira correção de check no
mesmo ciclo, todas achadas provando o check falhando. No ciclo 058, o `check-flags.sh` nasceu
comparando nos **dois sentidos** o conjunto de opções que o instalador aceita com o que a prosa
promete, depois que uma receita ensinou uma opção inexistente e o cabeçalho do instalador omitiu
três opções reais [CLAIM-10-051]. E no ciclo 054, o anti-padrão 23 deu nome à variante temporal
da família: um ciclo abre uma porta nova (um segundo canal de publicação) e não avisa o guarda
da porta velha, que continua lendo meio mundo e dizendo verde.

### O complemento: norma sem executável é norma sem efeito

O corolário C7 fecha a teoria do lado da governança: norma sem executável é norma sem efeito.
Os ciclos 057 a 060 são a prova: a regra "a caixa da cauda só se marca com evidência" estava
escrita, o portão que a lia era consultivo, e a caixa foi marcada sem evidência quatro vezes
seguidas [CLAIM-10-003]. O índice de decisões chama a classe de "caixa marcada antes da
evidência" e registra ocorrências nos ciclos 042, 043, 044 e 057 a 060 — o anti-padrão 13 no
próprio ritual.

### Quando a saída não se compara: o teorema T7

T4 pressupõe que o critério se compara por igualdade: a seção está ou não está, o link resolve
ou não. Um **julgamento** — o veredito de um agente revisor, a escolha de raia, um trade-off num
plano — não tem essa comparação. Ler com atenção não é critério: não produz artefato (A4) nem
algo a que alguém se prenda (A2). O teorema T7 diz o que substitui a comparação: uma **linha de
base registrada**, com entrada fixa, asserções que separam a resposta certa da apenas plausível,
e observação datada. A asserção positiva não basta; um caso que só pergunta "achou alguma
coisa?" passa com qualquer resposta prolixa. O que discrimina é o lado negativo: o que uma
resposta errada **afirmaria**.

O Maestro chegou a T7 pelo buraco. Por 36 ciclos, 13 agentes operaram sem linha de base
nenhuma; nada teria notado uma regressão no agente de revisão [CLAIM-10-034]. O ciclo 037 criou
o corpus de avaliações (*evals*), o `check-evals.sh` e o comando `/eval` em contexto fresco, fora
da CI por exigir chave de acesso ao modelo, e registrou a decisão num registro de decisão de
arquitetura (Architecture Decision Record, ADR), o
[ADR 0016](https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0016-evals-para-saida-nao-deterministica.md).
E entregou o ciclo "aprovado com vermelho declarado":
o `check-evals.sh` saía com erro, com 2 linhas de base pendentes [CLAIM-10-033]. A alternativa
seria preencher o campo `First-red` — a data em que o caso foi visto reprovando um alvo errado —
sem ninguém ter visto, ou afrouxar o portão. O ciclo preferiu o vermelho honesto, registrado como achado. A anatomia de cada caso
exige pelo menos uma asserção `MUST-FIND` e uma `MUST-NOT-CLAIM`; o [capítulo
15](../15-validando-o-maestro/capitulo.md) trata desse corpus em profundidade.

### Verde é necessário, não suficiente

A contraevidência de T4 importa mais que a evidência. Nos primeiros dias de operação do
Maestro, nove defeitos escaparam para a linha principal em 17 promoções, todos com a verificação
verde no momento do merge [CLAIM-10-010]. Nenhum foi pego por revisão; todos foram pegos quando
alguém **escreveu o check que faltava** (a imagem do diagrama, pelo portão de `<img src>` do
ciclo 020; a skill invisível, pelo `check-install.sh` do ciclo 021). O capítulo do handbook que
reescreveu a DoD no ciclo 029 tira duas conclusões. A primeira: a resposta certa a um escape não
é revisar com mais cuidado, é ampliar a família coberta pelo portão. A segunda: verde garante a
peça local, e não garante nem a coerência global (a jornada inteira ainda funciona?) nem a coisa
certa (nenhum teste conserta requisito errado). A primeira se ataca puxando o global para
dentro da DoD — jornada, ponta a ponta, rastreabilidade. A segunda fica com o humano
responsável, sempre.

Dois episódios mostram o limite com nitidez. No ciclo 015, o widget usava uma variável de tema
inexistente e ficava ilegível no tema claro; só apareceu na verificação visual em navegador
real, e nenhum teste de unidade o pegaria. No ciclo 074, o gate humano de usabilidade de 27 de
outubro reprovou o protótipo navegável depois que verificadores e a regente o tinham aprovado
([commit `dedc475`](https://github.com/GHDaru/maestro/commit/dedc475)): a rodada 2 trouxe
história por tela, redesenho e congelamento de fragmentos novos. Verde mecânico não é certo.

## Alternativas

O tech lead tem um cardápio conhecido. O veredito abaixo é o deste livro, com o do Maestro onde
ele existe.

| Abordagem | O que oferece | Onde falha com agentes | Veredito |
|---|---|---|---|
| **DoD e Definition of Ready (DoR) como checklist** (Scrum, Kanban) | portões de entrada e saída nomeados | caixa marcada é declaração, não evidência | **Adotar**, como checklist **executável**, com o mecânico na máquina |
| **Pirâmide de testes** (muita unidade, pouca integração) | feedback rápido e barato | o agente acerta a peça e erra a costura; os escapes do Maestro foram de integração | **Ênfase em integração**, no espírito do *testing trophy*: rota e contrato pegam o todo |
| **TDD** | vermelho antes do verde | só cobre o código, não o portão | **Adotar**, e estender ao portão: vermelho antes de confiar no check |
| **Cobertura como meta numérica** | um número simples para cobrar | meta gameável (anti-padrão 9): convida teste inútil, e agente otimiza número melhor que gente | **Rejeitar**; o critério é comportamento verificável, com um caso feliz e um de falha por caso de uso |
| **Teste de mutação de código** (ferramentas como PIT, para Java, e Stryker, para JavaScript) | mede se a suíte mata defeitos injetados | mede a suíte, não os portões de processo (links, evidência, contagem, instalação) | **Adotar onde houver código crítico**; para portões, usar a mutação do mundo deste capítulo |
| **Proteção de branch e checks obrigatórios** da forja | o merge recusa sem o job verde | protege o portão que existe; não diz se ele mede o fato | **Adotar** como trava final; o Maestro ainda não a ligou (ver o padrão abaixo) |
| **"Revisar melhor"** | atenção humana | não escala com N agentes e não pegou nenhum dos nove escapes medidos [CLAIM-10-010] | **Rejeitar como resposta a escape**; revisão independente continua, mas o escape vira check |
| **Modelo como juiz** (*Large Language Model as a judge*, avaliação por outro modelo) | julga o que não se compara por igualdade | sem linha de base e sem lado negativo, aprova qualquer resposta plausível | **Adotar só com T7**: entrada fixa, asserção negativa, observação datada, fora do caminho bloqueante |

O ponto comum: todas as alternativas respondem "o que verificar". Nenhuma responde "como sei que
a verificação verifica". É essa a lacuna que a prova por mutação de portões preenche.

## O padrão Maestro

O Maestro resolve com três camadas: **regra** (texto que um agente lê), **script** (portão que
a máquina roda) e **gancho** (*hook*, código que o harness executa num momento do ciclo de vida
do agente, queira ele ou não). Cito pela versão `19823c2`.

### Regra: o que está escrito

- **A skill `verifiable-dod`**, com a lei de ferro "nenhum critério de aceite sem o comando que
  o prova" e a segunda lei. Ela fecha as desculpas por antecipação: "é difícil de automatizar"
  — então marque como gate humano; "todo mundo entende" — sem comando, cada um entende uma
  coisa ([SKILL.md](https://github.com/GHDaru/maestro/blob/19823c2/skills/verifiable-dod/SKILL.md)).
  O comando `/dod` é o par de tempo de execução: roda testes, fitness functions, checagem de
  tipos e build, e mostra a evidência antes de declarar pronto
  ([dod.md](https://github.com/GHDaru/maestro/blob/19823c2/.claude/commands/dod.md)).
- **A DoD e a DoR do modelo operacional** (§7): testes verdes por camada, fitness functions,
  lint e tipos, revisão independente em contexto fresco, gate leve de segurança, documentação
  viva no mesmo pull request, rastreabilidade e evidência anexada. Na **raia leve**, a DoD é
  reduzida, mas revisão independente e testes continuam, e bug exige teste que o reproduza
  falhando antes do reparo. Na **raia infra**, há um bloco obrigatório de reversibilidade
  (backup, ensaio, estratégia de volta, aprovação humana explícita), assunto do [capítulo
  11](../11-risco-reversibilidade-e-autonomia/capitulo.md)
  ([operating-model.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/operating-model.md)).
  O mínimo de teste é um caso feliz e um de falha por caso de uso [CLAIM-10-041] (anti-padrão 8).
- **A divisão do enforcement** (§12 do modelo, decidida no
  [ADR 0006](https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0006-enforcement-dod-changelog.md)):
  o mecânico vira hard gate na máquina; o que exige julgamento — "é a coisa certa?", a classe de
  risco — fica no checklist do pull request mais aprovação humana. O ADR fechou isso em quatro
  peças [CLAIM-10-052]: o template de pull request espelhando a DoD, a raia, a rastreabilidade, o bloco de ações
  irreversíveis e o gate por classe de risco
  ([template](https://github.com/GHDaru/maestro/blob/19823c2/.github/pull_request_template.md));
  o gate de CHANGELOG na CI, que reprova o pull request sem entrada em `[Unreleased]`, com a
  label `skip-changelog` como válvula declarada; o `/dod`; e a tabela que mapeia cada item ao
  seu mecanismo.
- **A cauda de fechamento** (*closing tail*): quatro passos que vivem como tokens no `tasks.md`
  — `TAIL:review`, `TAIL:security`, `TAIL:mutation`, `TAIL:gate` — com a evidência no
  `qa-report.md` [CLAIM-10-037]. Nenhum se apaga; dispensar exige `n/a:` com o motivo real na
  linha, e `TAIL:gate` é sempre do humano
  ([artifacts.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/artifacts.md)).
  Os artefatos opcionais (pesquisa, modelo de dados, contratos, checklist próprio, desenho de
  interface) são **declarados** com marcas `ART:x=yes|no` no `plan.md`: silêncio não é decisão.
  O checklist próprio do ciclo tem template e comando (`/speckit.checklist`); os templates de
  tarefas, de relatório de qualidade (que nasceu no ciclo 019) e de jornada carregam a cauda e o
  lugar da evidência ([templates](https://github.com/GHDaru/maestro/tree/19823c2/.specify/templates)).
- **`TAIL:mutation`**, criado pela retrospectiva do ciclo 055: todo portão criado ou alterado no
  ciclo é quebrado de propósito e visto recusando. O detalhe que importa é como a regra se
  defende do proxy: "tocar um portão" é lido do **diff**, não da frase; a dispensa `n/a` é
  recusada de um ciclo que tocou portão, escreva-se `N/A`, `n/a —` ou `n/a:`; e a leitura casa a
  **linha da cauda**, não qualquer frase que mencione o token
  ([spec 055](https://github.com/GHDaru/maestro/blob/19823c2/specs/055-retro-do-portao-que-mede-a-frase/spec.md)).
- **A spec perde a caixa.** Depois de a caixa marcada antes da evidência reaparecer, o ciclo 045
  resolveu pela forma e não pela instrução: os critérios de aceite da spec não têm mais caixa de
  marcação. A spec diz o que deve valer; o `qa-report.md` diz se valeu.

### Script: o que a máquina roda

- **A bateria na CI.** Até o ciclo 043, o método tinha onze portões e a CI rodava um, o do
  CHANGELOG [CLAIM-10-021]; todos os outros dependiam de alguém lembrar. O ciclo 043 (raia
  infra, com privilégio mínimo e bloco de reversibilidade) pôs os portões na CI. Na versão
  `19823c2`, o arquivo de workflow roda quinze scripts estruturais num laço bloqueante, mais o
  modo `--ticked-only` da conformidade, o portão do livro de ponto, a sincronia do plugin e o
  build do livro, e três consultivos: `check-cycle`, `check-retro` e o `check-conformance`
  completo [CLAIM-10-022]
  ([ci.yml](https://github.com/GHDaru/maestro/blob/19823c2/.github/workflows/ci.yml)). A v0.2.0
  já anunciava dezesseis portões, treze bloqueando [CLAIM-10-023]. Há uma ressalva que o
  [roadmap](https://github.com/GHDaru/maestro/blob/19823c2/docs/roadmap.md) registra junto das
  entregas F18 (portões na CI), F23 (instalação exercitada) e F32–F33 (chamados gate a gate e
  conferidor pela data): a proteção de branch da forja, que exigiria o job verde para o merge,
  depende de uma decisão do Steward (o papel humano que responde pelo método) e não está ligada. Enquanto isso, o job avisa mas não trava.
- **Por que três são consultivos.** Na revisão do ciclo 043, o `check-conformance` tinha sido
  posto como bloqueante, embora fique vermelho do primeiro ao último commit de qualquer ciclo (ele
  rejeita, de propósito, o relatório-esqueleto que o gerador de ciclo escreve). O achado G4 da
  revisão: portão vermelho em quase todo push é portão que se aprende a ignorar. A conformidade
  saiu da CI e virou **recusa no `promote-main.sh`**, onde o ciclo de fato termina. A metade que
  pode bloquear sem ser sempre vermelha voltou à CI no ciclo 061, como `--ticked-only`.
- **Gate pulado nunca lê como passado.** O passo que valida o mod do livro de ponto precisa do
  Claude Code no runner. Quando ele não está, o passo imprime "skipped" sem marca de sucesso, e a
  ausência é declarada no relatório. A distinção entre "passou" e "não rodou" é a mesma de
  "limpo" e "não olhei", agora no nível da CI.
- **A instalação exercitada, não a origem.** Até o ciclo 048, todos os portões mediam o
  repositório de origem, onde o alvo por acaso existe. Um agente de outro repositório relatou duas
  citações quebradas na instalação. O portão novo, `check-installed.sh`, instala o método num
  diretório vazio e roda os portões lá dentro; achou nove citações quebradas, não duas — entre
  elas um arquivo de constituição citado oito vezes e nunca instalado [CLAIM-10-024]
  ([spec 048](https://github.com/GHDaru/maestro/blob/19823c2/specs/048-instalacao-que-funciona/spec.md)).
  Na retrospectiva do ciclo 061, o mesmo portão passou a comparar com o disco as contagens que o
  README e a receita afirmam: dez afirmações conferidas [CLAIM-10-028]. O `check-links.sh`, por
  sua vez, valida todo link relativo de todo Markdown, imagens incluídas.
- **Portão hermético.** O `check-ledger.sh` testa o gravador do livro de ponto, o relatório, o
  gancho de parada e a fusão de configurações em fixtures escritas num diretório temporário,
  com os números esperados calculados à mão no comentário ao lado; a mutação roda numa cópia
  ([check-ledger.sh](https://github.com/GHDaru/maestro/blob/19823c2/scripts/check-ledger.sh)). É
  o modelo de portão que não depende do estado do repositório para dizer a verdade.
- **Mutação como prática registrada.** No ciclo 046, a revisão reprovou um portão de licença que
  passava em três estados quebrados; corrigido, foi reverificado por dez mutações
  [CLAIM-10-027]. No ciclo 065, a mutação M6 — um marcador de conclusão de **outra** tarefa
  fechando a tarefa ativa — sobreviveu ao primeiro teste, com sete casos passando; o teste foi
  reforçado até matá-la [CLAIM-10-030].

### Gancho: o que roda queira o agente ou não

- **O gancho de parada** (*Stop hook*,
  [ADR 0021](https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0021-o-metodo-se-cobra-e-bate-o-ponto.md)):
  quando o agente vai encerrar a resposta, o harness roda `check-conformance.sh --ticked-only` no
  ciclo mais novo. Caixa marcada sem evidência bloqueia a parada **uma vez**, com as linhas do
  portão como motivo; na segunda, deixa parar e avisa o humano [CLAIM-10-039]. O desenho
  responde a duas forças: o corolário C13 (memória de agente relata intenção, não fato) e o
  Princípio II (o humano decide; portão que vira laço queima tokens sem decidir nada). O mesmo
  ADR cria o livro de ponto, alimentado pelos marcadores `[[TASK]]` e `[[DONE]]`.

### Vereditos conferíveis: a evidência também é artefato

A cauda resolveu "tem evidência?". Restava "esta evidência é de quem, sobre o quê, de quando?".
O [ADR 0024](https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0024-cabecalho-conferivel-nas-evidencias-da-cauda.md)
exige que cada linha `TAIL:*` do relatório carregue um cabeçalho conferível — gate, objeto @
hash, veredito, por quem, data — e que o portão chame a função `valida()` do conferidor. O
[ADR 0030](https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0030-portoes-do-maestro-com-prova-do-hindiana.md)
importou de um projeto irmão os portões Triagem, G0 a G9 e GR, com o mecanismo de prova: veredito
é arquivo commitado com objeto @ hash, a spec recebe duas aprovações de não-autores no mesmo
hash [CLAIM-10-038], o vermelho é provado no hash base, e nada se apaga. No glossário do método,
cada chamado é uma pasta com um arquivo de veredito por gate, e o estado é **derivado** dos
arquivos (autor diferente do crítico, data não posterior ao commit), nunca digitado.

Esse mecanismo também teve o seu proxy. O conferidor tomava como vigente o último veredito na
ordem alfabética do nome do arquivo; como o hash no nome não tem ordem temporal, havia dois
vereditos de tela válidos e o painel mostrava a FALHA antiga em vez do PASSA novo [CLAIM-10-046].
O ciclo 069 corrigiu: vigente é o de maior data do cabeçalho, com desempate por commit e nome, e
veredito com data ilegível é rejeitado e nunca concorre. O ciclo 070, por sua vez, foi integrado
como **parcial** — um requisito ausente, outro invertido, um terceiro sem branch e hash, e um
cabeçalho que ainda dizia "Spec 064 / DRAFT", lido pelo painel — e o resto virou dívida
declarada, não esquecida. No ciclo 075, a revisão notou que o vermelho do portão G2 (o "vermelho
provado") era de **coleta**: o contrato não existia, e o vermelho provava ausência, não
discriminação. A regra adotada: commit A com os testes vermelhos e a saída colada, commit B com
a implementação.

### O que nenhum portão de fonte pega: a jornada viva

Para telas, o Maestro tem a skill `living-journey`, com a lei de ferro "jornada sem captura do
build real é ficção, e heurística sem data é ficção vencida": documento, capturas geradas por
script versionado e heurística datada, no mesmo pull request
([SKILL.md](https://github.com/GHDaru/maestro/blob/19823c2/skills/living-journey/SKILL.md)). A
jornada do painel de regência (ciclo 072) é capturada por `captura-072.sh` e achou o R8: um
aviso que arredondava horas para baixo e minutos para o mais próximo e chegava a mostrar "1h60m"
[CLAIM-10-044]. A do protótipo navegável (ciclo 074) mediu o que o desenho afirmava: o
documento de interface dizia que seis itens cabiam na barra a cerca de 360 px; medido no build,
o menu precisa de 399 px e o último item transborda 38,8 px, e as tabelas do catálogo medem
572,6 px em qualquer largura [CLAIM-10-032]. O relatório do ciclo registra a medida a 360 px
reprovando 38 vezes, com o menu transbordando em todas as 20 rotas [CLAIM-10-031]. A jornada
tem uma seção "o que esta jornada não prova" e uma regra de evidência: correção futura usa nome
novo, nunca sobrescreve a foto do defeito
([jornada 074](https://github.com/GHDaru/maestro/blob/19823c2/docs/jornada/074-prototipo-navegavel.md)).

### O que vale em qualquer escala

Fases com gate valem em qualquer granularidade, do ciclo inteiro à tarefa de minutos: critério
com comando, portão provado por mutação, evidência conferível, humano no irredutível.

## Exemplo executável

A pasta [`exemplo/`](exemplo/README.md) traz um harness em Python 3, sem dependência externa,
que põe seis portões à prova. São três propriedades, cada uma com dois portões: um que mede o
proxy, na forma que um portão real do Maestro tinha antes de ser quebrado de propósito, e um que
mede o fato.

| Propriedade | Falha real que ela reproduz | Portão do proxy | Portão do fato |
|---|---|---|---|
| P1 — a evidência de revisão registra uma revisão que aconteceu | ciclo 063, "pendente." | aceita qualquer texto que não seja o marcador do gerador | linha da cauda ancorada, vocabulário fechado de ausência lido do início |
| P2 — a página declara o número certo de fontes | ciclo 016, 5 onde havia 6 [CLAIM-10-011] | conta linhas com `https://` | conta URLs e exige a declaração |
| P3 — o aviso de limiar afirma a porcentagem certa | ciclo 076, "9446 %" [CLAIM-10-018] | procura a palavra "limite" | exige o número certo e a palavra |

Rode:

```bash
cd livro/10-quality-gates-que-provam-fatos/exemplo
python3 provar.py            # sai 1: três decorações
python3 provar.py --so fato  # sai 0: três portões
```

O que observar na saída [CLAIM-10-043]. Primeiro: na fixture positiva, os seis ficam verdes.
Rodados só no caminho feliz, eles são indistinguíveis — é por isso que o portão novo que "passou
de primeira" merece desconfiança. Segundo: o portão ingênuo de P1 mata uma mutação em oito, a
do marcador `<...>`; reconhece a forma que ele mesmo produz, não a ausência. Terceiro: o
ingênuo de P2 erra nos **dois** sentidos, reprovando a página certa (duas fontes numa linha) e
aprovando a errada (o prefixo `https://` citado na prosa). Quarto: o ingênuo de P3 não mata
nenhuma.

O exercício do README afrouxa o portão bom de P1, trocando a leitura ancorada no início por uma
busca em qualquer posição: ele continua matando as oito mutações e passa a reprovar a evidência
legítima com "pendente" no meio da frase. A correção ingênua de um proxy costuma ser outro
proxy, e só a fixture legítima a denuncia.

## Contraexemplo

Portões provados por mutação não são de graça, e há lugares onde a regra atrapalha.

**O portão sempre vermelho.** O achado G4 do ciclo 043, visto acima, é o contraexemplo
canônico: o custo de um portão não é só o tempo de CI, é a atenção que ele gasta cada vez que
grita sem motivo. O inverso também é teatro: portão que nunca reprova nada é cerimônia
(anti-padrão 11), e deve ser podado.

**O portão como adversário.** Quando o portão é a única coisa entre o agente e o "pronto", o
agente aprende a satisfazê-lo. No ciclo 048, o próprio executor enfraqueceu quatro citações
reais para prosa vaga só para o portão passar, enquanto doze idênticas ficavam [CLAIM-10-025]. A
correção foi restaurar as citações e transformar a exceção em declaração legível por máquina
(`UP:optional-path`). A lição para o tech lead: o portão precisa de uma válvula **declarada**.
Forcing function sem escape vira burocracia contornada por fora; com escape nomeado — a label
`skip-changelog`, a marca `n/a:` com motivo — o desvio fica registrado e auditável.

**O portão que não pode disparar no próprio ciclo.** No ciclo 056, o verificador de capítulos
comparava datas de commit; como a data do commit de um ciclo só existe depois que ele fecha, o
ciclo que desatualizava um capítulo passava verde e deixava o vermelho para o ciclo seguinte. A
correção, no ciclo 061, foi consultar o `git status` antes do `git log`. Prove a mutação **no
mesmo ciclo** em que o defeito nasceria, ou o portão sempre culpa o vizinho.

**O que não vale portão.** No ciclo 035, a primeira renderização do diagrama de processo saiu
cortada à direita, e só foi vista porque alguém olhou a imagem. Nenhum portão mede imagem
inteira, e, com dor única, o ciclo decidiu não criar regra (You Aren't Gonna Need It, YAGNI).
Também não há portão para veracidade de prosa: a nota de release falsa do ciclo 050 foi pega por
revisão, não por script. E usabilidade, como mostrou o ciclo 074, é gate humano. Fingir que
esses casos são automáticos é o pior erro desta lista (anti-padrão 7, o "parece funcionar",
aplicado ao processo): esconda o gate humano e o verde passa a mentir sobre o que foi olhado.

**Corrigir ocorrência em vez da forma.** Sete fechamentos pontuais do anti-padrão 21, e ele
voltou todas as vezes [CLAIM-10-020]. Quando um defeito de portão recorre, o próximo portão não
deve procurar a ocorrência; deve procurar a forma (um varredor de pipes terminados em `grep -q`).
O custo é escrever um portão sobre portões. O custo de não escrever foi pago sete vezes.

**Retroatividade.** Um portão novo aplicado ao histórico reprova o que era verdade quando foi
escrito. O ciclo 063 resolveu com piso; o ciclo 055 fez o mesmo com `TAIL:mutation`. Ciclo velho
é evidência, não alvo.

**O laço que não converge.** Avaliador e otimizador podem girar para sempre. No ciclo 073, depois
de três leituras de três juízes sem convergência, valeu a regra das duas rodadas: o laço para, e
a regente leva a consolidação ao humano [CLAIM-10-040]. Mutação e revisão são investimento com
retorno decrescente; o humano decide quando parar de pagar.

**A lacuna conhecida.** Antes de tocar código existente, o método não tem passo de testes de
caracterização (o teste que fotografa o comportamento atual antes de mudá-lo); uma busca pela
palavra nas skills, templates e comandos devolve zero [CLAIM-10-045]. Este capítulo não resolve
isso; registra que, sem esse passo, o vermelho antes do verde não existe para o código herdado.

## Evidência

O que sustenta o capítulo, separado pelo estado de cada afirmação. A tabela completa, com a
evidência reproduzível de cada claim, está em [`claims.md`](claims.md).

**Medido** (reproduzível por comando na versão citada): a bateria da CI, com quinze scripts
estruturais bloqueantes e três consultivos [CLAIM-10-022]; as três formas que a função de
evidência reconhecia [CLAIM-10-002]; os quatro ciclos com ausência declarada verdadeira
[CLAIM-10-006]; a mutação M6 sobrevivente [CLAIM-10-030]; as medidas da jornada do protótipo
[CLAIM-10-031, CLAIM-10-032]; o catálogo com 23 anti-padrões [CLAIM-10-047]; a saída do exemplo
executável [CLAIM-10-043].

**Observado** (registrado em relatório, spec ou índice de decisões do Maestro): a falha do ciclo
063 e o que a antecedeu [CLAIM-10-001, CLAIM-10-003, CLAIM-10-004, CLAIM-10-005]; a recorrência
do proxy [CLAIM-10-007, CLAIM-10-008, CLAIM-10-009]; os escapes com verde [CLAIM-10-010]; as
falhas datadas da seção "Teoria" [CLAIM-10-011 a CLAIM-10-021, CLAIM-10-026, CLAIM-10-029,
CLAIM-10-050, CLAIM-10-051]; e os 35 de 40 ciclos cujo `tasks.md` tinha perdido o gate humano
do template, que mostram por que a cauda precisava existir como token [CLAIM-10-036]. A DoD do
handbook, em agosto de 2026, vivia em seis portões executáveis — quatro scripts e dois dentro do
gerador do livro — mais onze testes automatizados [CLAIM-10-042]; a bateria cresceu desde então.

**Hipótese** (não medida; agenda da pesquisa). A hipótese H5 da base de pesquisa do livro — gate
com teste de mutação reduz escapes [CLAIM-10-048] — é plausível pelos casos acima, mas os casos
são de um repositório, de um operador, sem grupo de controle. O que eles mostram com segurança é
que portões **não** provados por mutação deixaram passar defeitos que a mutação teria pego. Não
mostram quanto se reduz, nem a que custo. O desenho que testaria H5 está no [capítulo
15](../15-validando-o-maestro/capitulo.md): baselines com e sem gates, repetições, ambiente
congelado. Duas métricas da agenda servem ao tech lead desde já, desde que não virem meta:

- **Escape de gate** — defeitos achados depois do merge, com o portão verde no momento do merge,
  por promoção. É a métrica que o Maestro mediu à mão nos nove escapes [CLAIM-10-010].
- **Aceitação na primeira passada** — fração de entregas que passam pela revisão independente
  sem reprovação. Alta demais com escape alto é sinal de portão que mede proxy.

Um limite honesto adicional: muitos dos casos acima foram achados pelo próprio autor do método
ou por agentes que ele rege. Isso não os invalida — estão datados, com commit e relatório —, mas
o leitor deve tratá-los como estudo de caso, não como estimativa de frequência.

## Checklist

Aplique no seu time, portão por portão.

- [ ] Todo critério de aceite tem um comando com resultado esperado (`vazio`, `= N`, `exit 0`)
      **ou** está marcado como gate humano, com dono.
- [ ] Nenhum critério é meta numérica gameável (cobertura ≥ X %); o mínimo é um caso feliz e um
      de falha por caso de uso, e bug entra com teste que o reproduz falhando.
- [ ] Invariantes de segurança são checks negativos: a busca pelo proibido deve voltar vazia.
- [ ] Cada portão novo ou alterado foi **visto reprovando**: há uma fixture negativa por modo de
      falha, e a saída vermelha está colada na evidência do pull request.
- [ ] Cada portão tem pelo menos uma fixture **legítima** incômoda (o mundo certo de forma
      estranha) que ele deixa passar.
- [ ] O portão enumera a família inteira que guarda (todo atributo, todo formato, todo canal),
      e alguém perguntou, quando o ciclo abriu uma porta nova: o mundo deste portão aumentou?
- [ ] Entrada vazia, seção não encontrada e comando que falhou **reprovam**; nenhum portão
      confunde "limpo" com "não olhei", e nenhum passo pulado imprime marca de sucesso.
- [ ] Scripts de shell com `pipefail` não terminam pipe em `grep -q`, `grep -m1` ou `head -1`
      dentro de condição — e há um varredor que procura essa forma.
- [ ] Contagens anunciadas em documentação são comparadas com o disco por um portão.
- [ ] O portão roda onde o resultado cai (instalação limpa, build real, navegador real), não só
      na origem.
- [ ] Portões que ficam vermelhos em trabalho em andamento são consultivos na CI e bloqueantes
      no ponto em que o trabalho termina; os demais bloqueiam, e a proteção de branch está ligada.
- [ ] Toda válvula de escape é declarada e registrada (label, `n/a:` com motivo).
- [ ] Julgamento não comparável tem linha de base: entrada fixa, asserção negativa, observação
      datada.
- [ ] O que não automatiza — coerência global, a coisa certa, usabilidade — está escrito como
      gate humano, e não escondido atrás de um verde.
- [ ] O time mede escape de gate por promoção e olha a tendência, sem transformá-la em meta.

## Referências

**Maestro** (versão `19823c2`, salvo indicação):

- Axiomas, teoremas T4 e T7, corolários C2, C5, C7, C13 —
  https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/axioms.md
- Constituição, Princípio IV —
  https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/principles.md
- Modelo operacional, §7 (DoR e DoD) e §12 (enforcement) —
  https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/operating-model.md
- Catálogo de artefatos e cauda de fechamento —
  https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/artifacts.md
- Skills `verifiable-dod`, `anti-patterns`, `living-journey` —
  https://github.com/GHDaru/maestro/tree/19823c2/skills
- ADRs 0006, 0016, 0021, 0024, 0030 — https://github.com/GHDaru/maestro/tree/19823c2/docs/adr
- Índice de decisões (achados 033, 042, 043, 046, 048, 049, 050, 056, 060, 062, 063, 064) —
  https://github.com/GHDaru/maestro/blob/19823c2/docs/records/decisoes.jsonl
- Specs e relatórios dos ciclos citados — https://github.com/GHDaru/maestro/tree/19823c2/specs
- Workflow de CI — https://github.com/GHDaru/maestro/blob/19823c2/.github/workflows/ci.yml
- Ciclo 076, tarefa T045 (versão `757798c`) —
  https://github.com/GHDaru/maestro/blob/757798c/specs/076-padroes-de-engenharia-e-react/done-076-t045.md
- Handbook do método, capítulo 09 e receita "escrever critério verificável" (cópia congelada em
  [`maestro-handbook/`](../../maestro-handbook/handbook/09-definition-of-ready-done.md))

**Externas** (obras de referência; nenhuma URL foi reconsultada para esta versão):

- R. A. DeMillo, R. J. Lipton e F. G. Sayward, "Hints on Test Data Selection: Help for the
  Practicing Programmer", *Computer* (revista do Institute of Electrical and Electronics
  Engineers), 1978 — a origem do teste de mutação.
- A. Mavin, P. Wilkinson, A. Harwood e M. Novak, "Easy Approach to Requirements Syntax (EARS)",
  17th International Requirements Engineering Conference, 2009.
- N. Ford, R. Parsons e P. Kua, *Building Evolutionary Architectures*, O'Reilly, 2017 — fitness
  functions.
- K. Beck, *Test-Driven Development: By Example*, Addison-Wesley, 2002.
- M. Feathers, *Working Effectively with Legacy Code*, Prentice Hall, 2004 — testes de
  caracterização.
- M. Strathern, "'Improving ratings': audit in the British University system", *European
  Review*, 1997 — a formulação corrente da lei de Goodhart ("quando uma medida vira meta, deixa
  de ser boa medida").
- K. Schwaber e J. Sutherland, *The Scrum Guide*, 2020 — Definition of Done.
- K. C. Dodds, "The Testing Trophy and Testing Classifications" (texto citado pelo handbook do
  Maestro).
- DevOps Research and Assessment (DORA), guia das métricas "four keys" —
  https://dora.dev/guides/dora-metrics-four-keys/ (link herdado do handbook do Maestro).
