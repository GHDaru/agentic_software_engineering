# 15 — Validando o Maestro

> "Knowing the gap and stopping there is what T7 names."
> — teorema T7, `axioms.md` do Maestro

Até aqui o livro defendeu um método com histórias do próprio método. Isso é bom para ensinar e
fraco para provar: quem escreveu as regras também escolheu os exemplos. Este capítulo vira a
lente para dentro. Se você vai adotar spec, portões, revisão em contexto fresco e retrospectiva
que vira regra, precisa saber como se descobre que isso funciona, e como se descobre que um
agente piorou sem ninguém perceber. A resposta não é um benchmark famoso nem uma pesquisa de
satisfação do time. É uma disciplina pequena, que o Maestro aprendeu errando duas vezes no mesmo
dia.

## Pergunta central

Como testar uma metodologia, e não só o software que ela produz?

## Resultado de aprendizagem

Ao final, você consegue:

1. **Distinguir** teste, benchmark e avaliação (*eval*): o teste compara por igualdade, o
   benchmark compara modelos entre si, a avaliação registra uma linha de base para um julgamento
   que não se compara por igualdade.
2. **Escrever** um caso de avaliação com entrada fixa, asserções positivas e, sobretudo,
   asserções **negativas** (o que uma resposta errada afirmaria), datado e preso ao alvo que ele
   mede.
3. **Provar** que o caso discrimina, rodando-o contra o alvo **ablado** (o mesmo agente sem a
   instrução que o caso diz medir) e vendo-o reprovar antes de confiar no passe.
4. **Conferir** a premissa da fixture antes de rodar, e reconhecer a fixture que já carrega o
   próprio veredito.
5. **Trocar** a pergunta "você está seguindo o método?" por um comando que lê os artefatos, e
   separar o que esse comando mede (conformidade) do que ele não mede (se o método é bom).

## A falha real

Em 6 de agosto de 2026, o ciclo 037 do Maestro entregou o corpus de avaliações: uma pasta
`evals/`, um portão `check-evals.sh` e um comando `/eval` que roda um caso em contexto fresco. O
motivo estava escrito no teorema que o ciclo criou: durante 36 ciclos, 13 agentes operaram sem
linha de base nenhuma, e nada teria notado se o agente de revisão tivesse regredido
[CLAIM-15-001]. O ciclo saiu com dois casos-semente e, de propósito, com o portão **vermelho**:
nenhum dos dois casos tinha sido executado, e marcar o campo `First-red` sem ter visto o caso
reprovar seria mentir para o próprio portão. O achado foi registrado como
`achado-037-linhas-de-base-pendentes` no índice de decisões [CLAIM-15-002].

No dia seguinte, 7 de agosto, os dois casos rodaram. O caso 001 mede se o agente de revisão
compara o diff com o plano, e não só lê o código. Passou com seis de seis asserções — uma delas
marcada como limítrofe ("borderline": o revisor sugeriu em linha um idioma de uma linha, e o
caso proibia "consertar") — e a própria execução achou dois defeitos de redação no caso, que
foram corrigidos sem afrouxar o que ele exige. Até aí, nada provado: um passe só diz que o alvo
acertou, não que o caso saberia notar um alvo que erra. Então o caso foi rodado de novo contra o
**mesmo agente sem a instrução de comparar com o plano — e sem o plano na entrada**. O agente
ablado fez uma boa revisão de código, achou defeitos reais, e reprovou o caso: viu que faltava
validação, mas atribuiu a falta a um comentário do script e não a um requisito, e sugeriu apagar
a promessa da descrição em vez de implementá-la
([baseline do caso 001](https://github.com/GHDaru/maestro/blob/19823c2/evals/001-review-drops-a-requirement/baseline.md))
[CLAIM-15-003]. Esse vermelho é o que vale. O caso 001 ganhou linha de base.

Leia a ablação com o cuidado que ela merece. Ela removeu **duas** coisas de uma vez: a linha da
instrução e o próprio plano. Um revisor que não recebe o plano não tem como compará-lo com o diff,
com ou sem instrução. Então o vermelho prova que o caso separa um revisor "cego ao plano" de um
que o usa — que é o eixo declarado —, mas não isola quanto do efeito vem da instrução e quanto
vem da ausência do documento. A ablação limpa, que atribuiria o vermelho só à instrução, seria
rodar o ablado **com** o plano na entrada. Ela não foi feita, e o capítulo não a dá como feita.

O caso 002 contou a outra história. Ele mediria se o agente guardião do processo rejeita uma
raia de trabalho declarada errada. A primeira fixture era flagrante: reescrever no lugar um
arquivo documentado como somente-acréscimo, declarado como raia leve. O alvo real acertou. O alvo
ablado, sem a instrução "confira a raia declarada", acertou também, chegando lá só pelo
Princípio III (reversibilidade). A fixture foi reescrita como caso limítrofe, em que todo sinal
de superfície dizia "leve" e o defeito era o raio de impacto de uma linha de regra de portão.
O alvo ablado passou de novo. Duas fixtures, quatro rodadas, e nenhuma separava um agente que
julga raia de um que não julga
([baseline do caso 002](https://github.com/GHDaru/maestro/blob/19823c2/evals/002-guardian-accepts-a-wrong-lane/baseline.md))
[CLAIM-15-004].

E houve o golpe mais incômodo: as duas fixtures, escritas à mão, tinham defeito, e quem achou
foram os agentes avaliados, não o autor. A primeira trazia as conclusões escritas no próprio
enunciado. A segunda tinha premissa falsa: o agente ablado conferiu, sem que ninguém pedisse, que
o padrão citado na fixture não casava com a linha que ela dizia ser sinalizada [CLAIM-15-005].
Para completar o quadro, as rodadas daquele dia foram commitadas citando um ciclo 040 que não
tinha pasta em `specs/`: trabalho sem spec, violação do Princípio I cometida pelo próprio agente
que montava as avaliações, pega pelo `check-cycle.sh` [CLAIM-15-006].

A retrospectiva do ciclo 041 fechou os quatro achados sem afrouxar nada. O caso 002 foi
**aposentado com motivo**, em vez de ajustado até passar. Nasceram o anti-padrão 19 (caso de
avaliação que ninguém viu reprovar) e o 20 (fixture que carrega o próprio veredito ou cuja
premissa nunca foi conferida), e três campos obrigatórios: `Axis` no caso, `Ablation` e
`Premise-checked` na linha de base
([qa-report do ciclo 041](https://github.com/GHDaru/maestro/blob/19823c2/specs/041-retro-dos-quatro-achados-de-eval/qa-report.md))
[CLAIM-15-007]. E o caso 002 deixou um subproduto que nenhuma pesquisa de opinião teria dado:
remover a instrução de conferir raia **não muda nada** no agente guardião. Ou o item é
redundante, ou o caso certo ainda não foi escrito. O método registrou isso como hipótese, não
como regra.

A lição para quem lidera time não é "avaliação é difícil". É que, sem o alvo ablado, o Maestro
teria declarado duas linhas de base verdes na mesma tarde, e uma delas não media nada.

## Teoria

### O teorema: onde a saída não se compara, o critério é uma linha de base

O [capítulo 10](../10-quality-gates-que-provam-fatos/capitulo.md) derivou do teorema T4 que
critério sem comando não é critério. O teorema T7 nota o limite disso: um comando só decide o
que se compara por igualdade. Uma seção existe ou não; um link resolve ou não. Um **julgamento**
— o veredito de uma revisão, a classificação de uma raia, o *trade-off* de um plano — não tem
essa comparação, e "ler com atenção" também não serve: não produz artefato (axioma A4, só o que
está escrito sobrevive à sessão seguinte) nem algo pelo qual alguém responda (axioma A2, a
consequência precisa de dono)
([axioms.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/axioms.md)).

O que substitui a comparação é uma **linha de base registrada**: entrada fixa, asserções que
separam a resposta certa da apenas plausível, e uma observação com data. O ponto fino está no
lado negativo. Uma asserção que só pergunta "achou alguma coisa?" passa com qualquer resposta
prolixa. O que discrimina é o que uma resposta **errada** afirmaria — no caso 001, "o diff
implementa o plano" ou "os testes dão cobertura real". O próprio T7 traz a evidência
desconfortável que o originou: a única ocorrência da palavra *judge* nos scripts do repositório
era um comentário em `check-cycle.sh` admitindo que o portão "não consegue julgar a resposta"
[CLAIM-15-008]. Saber da lacuna e parar ali é exatamente o que o teorema nomeia.

### Teste, benchmark e avaliação não são a mesma coisa

O glossário do Maestro separa os três termos, e a separação evita metade das discussões
([glossary.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/glossary.md)). O
**teste** compara por igualdade e entra na integração contínua (CI, de *continuous
integration*). O **benchmark** compara modelos ou sistemas entre si sobre um corpus de tarefas,
como o SWE-bench e o SWE-Bench Pro, que medem se um agente resolve *issues* reais de repositórios
públicos. A **avaliação** mede um alvo seu — um agente, uma skill, um prompt — contra a linha de
base que você mesmo registrou. Benchmark responde "qual modelo é melhor"; avaliação responde "o
meu revisor piorou desde terça".

Dois corolários de T7 dão a forma prática. O C11 diz que uma avaliação **nomeia seu alvo e
envelhece quando o alvo muda**: a linha de base carrega o commit do agente que mediu
(`Target-commit`), e o `check-evals.sh` acusa a linha de base defasada quando o arquivo do agente
muda depois dela. O portão não julga a saída de agente nenhum — isso exigiria chave de interface
de programação (API, de *application programming interface*) num portão que todos rodam — ele
mede a **saúde do corpus**: o alvo existe, há asserção negativa, a linha de base é atual, o caso
já foi visto reprovando. O julgamento roda sob demanda, pelo comando `/eval`, em contexto fresco.

### A ablação é o grupo de controle

Da falha do dia 7 sai a ideia central do capítulo, que o método aprendeu na prática antes de
escrever em regra: **um caso de avaliação só vale depois de reprovar o alvo ablado no eixo que
ele diz medir**. É o grupo de controle de um experimento, reduzido ao tamanho de um time. Tira-se
do agente exatamente a instrução que o caso alega medir e se roda de novo. Se o ablado passa, o
caso mede outra coisa (no 002, "detectar operação destrutiva óbvia", não "julgar raia"). É a
mesma segunda lei do capítulo 10, "prove o check falhando antes de confiar nele", estendida ao
julgamento: mutação é para portão determinístico o que ablação é para avaliação.

### Memória não é testemunha

O terceiro corolário completa a validação do lado do processo. O C13 afirma que **pergunta
respondível de memória será respondida de memória, e memória relata intenção**. Perguntar ao
agente "você está seguindo o método?" mede o que ele pretendia. No mesmo ciclo 041, o agente do
próprio repositório teria respondido "sim" enquanto dois commits citavam um ciclo sem spec, e um
agente companheiro relatou "CI verde" antes de checar
([check-conformance.sh](https://github.com/GHDaru/maestro/blob/19823c2/scripts/check-conformance.sh)).
Daí o `check-conformance.sh`, decidido no Architecture Decision Record (ADR) 0019: ele lê as
declarações e a cauda de fechamento nos artefatos que o executor consome, e responde com fato.
O limite é declarado no próprio script: ele mede se o método **sobreviveu nos artefatos**, não
se o método é bom nem se o humano leu.

### Três camadas de validação

Juntando, validar uma metodologia tem três camadas, e confundi-las é o erro comum. A primeira é
**conformidade**: o método foi aplicado? Responde-se com comando, como o
`check-conformance.sh`. A segunda é **regressão de julgamento**: os agentes que o método usa
continuam julgando bem? Responde-se com avaliação de linha de base, como `evals/`. A terceira é
**efeito**: aplicar o método produz software melhor, mais barato ou com menos retrabalho do que
não aplicá-lo? Essa só se responde com experimento comparativo — níveis de tratamento (só prompt,
prompt mais spec, spec mais portões, método completo), repetições com distribuição e ambiente
congelado — e o livro a registra como agenda de hipóteses H1 a H10 em
`pesquisa/base-de-pesquisa.md`, não como fato [CLAIM-15-009]. As duas primeiras camadas o
Maestro já executa. A terceira ele ainda não provou, e o restante do capítulo trata cada uma
nessa ordem.

## Alternativas

Quem lidera um time que adotou agentes já usa alguma forma de "validar o processo", mesmo sem
chamar assim. Vale olhar cada uma pela régua das três camadas — conformidade, regressão de
julgamento, efeito — e perguntar o que ela mede de fato.

**Perguntar ao agente (ou ao time) se o método está sendo seguido.** É a mais barata e a mais
comum. O agente lê a instrução, lembra da intenção e responde "sim". O corolário C13 explica por
que isso não serve: a pergunta respondível de memória é respondida de memória, e a memória
relata o que se pretendia fazer. O caso do ciclo 041 contado acima é exatamente esse — dois
commits citavam um ciclo sem spec enquanto a resposta honesta, de memória, seria "estou seguindo".
Veredito: descarte como evidência. Serve para abrir conversa, não para fechar portão.

**Pesquisa de percepção do time.** Questionários sobre satisfação, confiança nos agentes,
sensação de produtividade. Medem algo real — a adoção percebida — e ajudam a priorizar onde
dói. Não medem nenhuma das três camadas: não dizem se o artefato carrega a cauda de
fechamento, não notam um revisor que piorou e confundem "gosto de trabalhar assim" com "entrega
melhor". Veredito: complemento útil para a conversa de gestão, inútil como validação.

**Benchmark público.** O SWE-bench (Jimenez et al., 2024) toma *issues* reais de repositórios
Python públicos e pergunta se o sistema produz um *patch* que faz passar os testes que a correção
original fez passar. O SWE-Bench Pro (Deng et al., 2025) mantém o desenho e endurece a tarefa:
problemas de horizonte longo, tirados de 41 repositórios mantidos [CLAIM-15-027], muitos exigindo mudança
coordenada em vários arquivos. Nos dois, quem decide é um teste — comparação por igualdade, o
mundo do capítulo 10. São a melhor ferramenta disponível para **escolher modelo ou harness**, e
não servem como linha de base de julgamento por três motivos. Primeiro, medem o sistema de
outra pessoa, num corpus alheio: respondem "qual sistema é melhor", não "o meu revisor, com a
minha instrução, ainda compara o diff com o plano". Segundo, medem o que se decide por teste — o
*patch* passa ou não —, e o que o seu processo pede ao revisor (o requisito que faltou, a raia
errada) não tem teste que o decida. Terceiro, não envelhecem com o seu alvo: mudar uma linha da
instrução do seu agente não muda nada no placar público. E dois sistemas empatados num benchmark
podem divergir justamente no julgamento que o seu processo exige. Veredito: use para a decisão de compra e como corpus externo da camada de
efeito (está na agenda de pesquisa do livro); não use como linha de base do seu agente.

**Juiz automático em toda integração contínua.** Um modelo avalia a saída de outro modelo a cada
*push* — o padrão conhecido como *LLM-as-judge*, em que um modelo de linguagem de grande porte (LLM, de *large language model*) faz o papel de juiz. Resolve o problema do "ninguém rodou", mas cria
três outros: o portão passa a exigir uma chave de API que nem todo colaborador tem, fica
não-determinístico (o mesmo commit pode sair verde e vermelho) e, sem ablação, continua sem
provar que o caso discrimina. O Maestro escolheu de propósito a separação: o portão
determinístico mede a saúde do corpus, e o julgamento roda sob demanda, pelo `/eval`, em contexto
fresco. Veredito: viável quando a chave é centralizada e o custo cabe; mesmo assim, só depois que
cada caso foi visto reprovando o alvo ablado.

**Ferramentas de avaliação de prompt.** Há *frameworks* abertos que executam casos contra
prompts e verificam asserções (promptfoo e OpenAI Evals são exemplos). Eles resolvem a parte
mecânica — rodar, comparar, guardar histórico — e podem oferecer o vocabulário do lado negativo:
o promptfoo, por exemplo, documenta que qualquer tipo de asserção pode ser negado com o prefixo
`not-` (documentação de *expected outputs*, acesso em 02/11/2026). Oferecer não é exigir. As duas
disciplinas do capítulo — todo caso com lado negativo, todo caso visto reprovando um grupo de
controle ablado — são regras sobre a suíte, e quem as cobra é um portão seu, como o
`check-evals.sh`, não o executor. Uma suíte cheia de "a resposta menciona X" passa com qualquer
resposta prolixa, em qualquer ferramenta. Veredito: adote a
ferramenta se ela poupar trabalho; a disciplina continua sendo sua. O argumento sobrevive à troca
de ferramenta.

**Métricas de fluxo de entrega.** As métricas do programa DevOps Research and Assessment (DORA)
— frequência de entrega, tempo de espera, taxa de falha de mudança, tempo de recuperação — medem
efeito na entrega, e o [capítulo 13](../13-observabilidade-e-economia/capitulo.md) as trata. São
a aproximação mais honesta da terceira camada que um time consegue no dia a dia. O limite é a
atribuição: a taxa de falha caiu por causa da spec, do modelo novo ou da equipe mais experiente?
Sem grupo de comparação, a métrica observa, não explica. Veredito: acompanhe; não use como prova
de que o método funciona.

**Experimento controlado.** Rodar as mesmas tarefas em níveis de tratamento (só prompt; prompt
mais spec; spec mais portões; método completo), com repetições, distribuição e ambiente
congelado, é o único desenho que responde à terceira camada com atribuição. É também o mais
caro, e por isso o livro o registra como agenda (H1 a H10), não como resultado. Veredito: é o
padrão-ouro e ainda não foi feito; quem afirmar que o Maestro "reduz retrabalho" sem ele está
relatando intenção.

| Alternativa | Camada que mede | Veredito |
|---|---|---|
| Perguntar ao agente | nenhuma (intenção) | descartar como evidência |
| Pesquisa de percepção | nenhuma (adoção percebida) | complemento de gestão |
| Benchmark público | efeito, em corpus alheio | escolher modelo; corpus externo |
| Juiz automático na CI | regressão, se houver ablação | só com chave central e casos provados |
| Ferramenta de avaliação de prompt | regressão (mecânica) | adotar se poupar trabalho; disciplina é sua |
| Métricas DORA | efeito, sem atribuição | acompanhar, não provar |
| Experimento controlado | efeito, com atribuição | padrão-ouro, ainda agenda |

A coluna do meio é o ponto: nenhuma alternativa cobre conformidade, e só duas tocam a regressão
de julgamento — ambas dependendo de uma disciplina que elas mesmas não impõem.

## O padrão Maestro

O Maestro cobre as duas primeiras camadas com peças pequenas e separa, em cada uma, o que é
regra escrita, o que é script e o que roda sozinho. Tudo abaixo está citado na versão
`maestro@19823c2`.

### Camada 1 — conformidade: a resposta executável

**Regra.** O corolário C13 e o Architecture Decision Record (ADR) 0019
([ADR 0019](https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0019-conformidade-executavel-e-catalogo-de-artefatos.md))
transformam omissão em declaração. O plano declara cada artefato condicional com um *token*
legível por máquina — `ART:research=yes|no`, `ART:data-model=`, `ART:contracts=`,
`ART:checklist=`, `ART:ux-design=` — e o `tasks.md` carrega a cauda de fechamento
(`TAIL:review`, `TAIL:security`, `TAIL:mutation`, `TAIL:gate`), cada item presente ou `n/a`
com motivo. O catálogo do que se aplica quando é o
[artifacts.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/artifacts.md). A
falha que originou a regra foi medida no ciclo 042: 35 de 40 `tasks.md` tinham perdido o gate
humano que o template carregava [CLAIM-15-010] — o anti-padrão 22, método instalado como cópia
com perdas, em que o executor segue fielmente um artefato que é subconjunto.

**Script.** O
[check-conformance.sh](https://github.com/GHDaru/maestro/blob/19823c2/scripts/check-conformance.sh)
lê esses *tokens* do disco e do git e responde "você está seguindo o Maestro?" com fato. O
`CLAUDE.md` do projeto proíbe responder a essa pergunta de memória e manda rodar o script.

**Onde bloqueia.** Aqui está o desenho mais instrutivo. A versão completa do script é
**consultiva** na integração contínua, porque um ciclo aberto tem caixas desmarcadas e um
`qa-report.md` de esqueleto, e um portão sempre vermelho é um portão que se aprende a ignorar.
A conformidade bloqueia onde o ciclo de fato termina: o `promote-main.sh` recusa promover para
a linha principal enquanto ela está vermelha. E a metade que pode bloquear sem nunca acusar
trabalho em andamento — `--ticked-only`, "caixa marcada tem evidência" — é bloqueante na CI
([ci.yml](https://github.com/GHDaru/maestro/blob/19823c2/.github/workflows/ci.yml)). Ela nasceu
porque, em quatro ciclos seguidos (057 a 060), as caixas da cauda foram marcadas sem
`qa-report.md` e só a revisão humana pegou [CLAIM-15-011].

**Gancho.** O *hook* `SessionStart`
([session-state.sh](https://github.com/GHDaru/maestro/blob/19823c2/scripts/hooks/session-state.sh))
injeta o estado **medido** do método no início de cada sessão — ciclo aberto, conformidade,
achados abertos — em vez de deixá-lo para a memória do agente. É o C13 aplicado na entrada.

### Camada 2 — regressão de julgamento: o corpus de avaliações

**Regra.** O teorema T7 e o corolário C11, decididos no
[ADR 0016](https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0016-evals-para-saida-nao-deterministica.md),
e os anti-padrões 19 e 20 da skill
[anti-patterns](https://github.com/GHDaru/maestro/blob/19823c2/skills/anti-patterns/SKILL.md).
Cada caso mora em `evals/<NNN-slug>/` com três arquivos:

- `case.md` — `Target:` (o arquivo de instrução avaliado), `Question:` e `Axis:` (a capacidade
  que o caso diz separar); opcionalmente `Status: retired` com `Retired-because:`;
- `expect.md` — pelo menos um `MUST-FIND:` e pelo menos um `MUST-NOT-CLAIM:`;
- `baseline.md` — `Date:`, `Target-commit:`, `First-red:`, `Verdict:`, `Ablation:` e
  `Premise-checked:`.

**Script.** O
[check-evals.sh](https://github.com/GHDaru/maestro/blob/19823c2/scripts/check-evals.sh) é
bloqueante na CI e declara no próprio cabeçalho que **não julga** saída de agente nenhuma. Ele
confere que o alvo existe, que há eixo, que os dois lados das asserções existem, que todos os
campos da linha de base estão lá, que `First-red` saiu de `pending` e que o `Target-commit`
registrado ainda é o último commit que tocou o alvo — se não for, acusa linha de base
defasada. Caso aposentado aparece na saída com o motivo; aposentar sem motivo é tratado como
apagar, e reprova. Corpus vazio sai verde com a frase "and empty. Nothing here is evaluated
yet", para que verde nunca seja lido como cobertura.

**Comando.** O
[/eval](https://github.com/GHDaru/maestro/blob/19823c2/.claude/commands/eval.md) é a parte que
precisa de modelo no laço e roda sob demanda. Tem dois pré-voos, nesta ordem: rodar o
`check-evals.sh` e **reproduzir a premissa** da fixture, procurando também conclusão vazada no
enunciado. Depois responde à pergunta em contexto fresco, obedecendo ao alvo; lê o `expect.md`
**só depois** que a resposta existe; e então roda de novo contra o alvo ablado — a mesma
instrução sem o item que o `Axis:` nomeia. Se o ablado reprova, esse é o `First-red`,
conquistado e não encenado. Se passa, o comando proíbe ajustar a fixture até ficar vermelho
("isso é pescaria") e manda aposentar com motivo ou reescolher o eixo. O veredito é por
asserção, com o trecho citado da resposta; decidir o que ele significa fica com o humano.

**Quando cresce.** O roteiro do Maestro não fixa meta de cobertura. O gatilho para um caso
novo é um agente que **regrediu**: cada regressão observada ganha caso, e a cobertura cresce por
dor, não por meta
([roadmap.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/roadmap.md)).

### Camada 3 — efeito: declarada, não afirmada

O Maestro não tem script para a terceira camada, e não finge ter. O que existe é o registro
honesto do que o próprio repositório pode testemunhar — ciclos, achados, retrospectivas — e a
agenda de hipóteses do livro. A seção de Evidência separa uma coisa da outra.

| Peça | Tipo | Camada | Bloqueia? |
|---|---|---|---|
| T7, C11, C13; ADRs 0016 e 0019; anti-padrões 19, 20, 22 | regra | 1 e 2 | — |
| `check-conformance.sh --ticked-only` | script | 1 | sim, na CI |
| `check-conformance.sh` completo | script | 1 | consultivo na CI; bloqueia a promoção |
| `session-state.sh` (`SessionStart`) | *hook* | 1 | não; informa |
| `check-evals.sh` | script | 2 (saúde do corpus) | sim, na CI |
| `/eval` | comando | 2 (julgamento) | não; produz veredito |

### O que é conceito e o que é o harness

O Maestro roda no Claude Code, e três peças acima usam mecanismos dele: o `/eval` é um comando
de barra, o estado entra por um *hook* `SessionStart`, e a ordem de não responder de memória
mora no `CLAUDE.md`. Nenhuma das três é o padrão; são a forma que o padrão tomou ali. Os scripts
(`check-conformance.sh`, `check-evals.sh`) são shell e git puros e não dependem de harness.

| Conceito | No Maestro (Claude Code) | Em outro harness |
|---|---|---|
| resposta executável à pergunta "estou seguindo?" | `check-conformance.sh`, citado no `CLAUDE.md` | o mesmo script, citado no arquivo de instrução que o seu harness lê ao abrir a sessão (por exemplo um `AGENTS.md`) |
| estado medido na entrada da sessão | *hook* `SessionStart` rodando `session-state.sh` | qualquer gancho de início de sessão; sem gancho, a primeira instrução do arquivo de regras manda rodar o comando antes de agir |
| julgamento sob demanda em contexto fresco, com ablação | comando `/eval` que abre subagentes | dois agentes abertos sem histórico — um com a instrução inteira, outro sem a linha do eixo —, respostas salvas em arquivo e comparadas com o `expect.md` |
| saúde do corpus, sem modelo | `check-evals.sh` bloqueante na CI | o mesmo script, ou o `avaliar.py` do exemplo, em qualquer CI |

Se o seu harness não tem subagente, a ablação continua possível: são duas sessões novas, sem
memória compartilhada. O que não é negociável é o que está na coluna da esquerda.

## Exemplo executável

A pasta [`exemplo/`](exemplo/README.md) reproduz em miniatura as duas metades da segunda camada:
a saúde do corpus, que o `check-evals.sh` mede, e a prova por ablação, que o `/eval` faz. É um
único script, `avaliar.py`, em Python 3 sem dependências, mais um corpus de três casos e dois
alvos — a instrução de um agente de revisão e a de um guardião do processo.

Antes de rodar, um aviso que o próprio script repete: as respostas do alvo e do alvo ablado
foram **escritas à mão**, e o "juiz" casa palavras-sinal. Isso é um *proxy* — o anti-padrão 13
do Maestro, a checagem que mede o substituto e não o fato. Ele está aqui para mostrar a
mecânica sem exigir chave de API de ninguém. No uso real, as duas respostas viriam de dois
subagentes em contexto fresco: um com a instrução inteira, outro com a instrução menos a linha
que o `Axis:` nomeia.

### Os três casos

O **caso 001** espelha o caso 001 real do Maestro em forma reduzida. O alvo é o revisor; o eixo é
"comparar o diff com o plano". A entrada traz só fatos: o plano tem dois requisitos funcionais (FR, de *functional
requirement*), FR1 e FR2;
o diff implementa o FR1 e deixa um `TODO` no lugar do FR2; o teste novo só verifica que nada
levantou exceção. O `expect.md` tem dois `MUST-FIND:` (o FR2 não foi implementado; o teste não
verifica comportamento) e dois `MUST-NOT-CLAIM:` (o diff implementa o plano; basta apagar o
`TODO`). A resposta ablada imita o padrão do agente ablado real de 7 de agosto — que atribuiu a falta a
um comentário e sugeriu apagar a promessa em vez de implementá-la: vê o `TODO`, trata como
problema de estilo e sugere removê-lo.

O **caso 002** espelha o caso aposentado. O alvo é o guardião; o eixo é "conferir a raia
declarada". A entrada é a fixture flagrante — reescrever no lugar um arquivo somente-acréscimo
declarado como raia leve. As duas respostas rejeitam a mudança: a do alvo pela raia, a do
ablado pelo Princípio III.

O **caso 003** é o erro de quem começa: um caso com só o lado positivo ("aponta algum
problema") e nunca rodado contra ablado.

### Rodando

```bash
cd livro/15-validando-o-maestro/exemplo
python avaliar.py        # ou python3
echo $?
```

A saída, copiada da execução de 2 de novembro de 2026, termina assim [CLAIM-15-012]:

```text
• 001-revisor-perde-requisito
  ...
  alvo   PASSA
  ablado REPROVA (não achou: o requisito FR2 do plano não foi implementado; ...)
• 002-guardiao-aceita-raia-errada
  ...
  alvo   PASSA
  ablado PASSA
  ✗ o ablado PASSA — o caso não mede o eixo 'conferir a raia declarada ...'; aposente com
    motivo, não ajuste a fixture até ficar vermelho
• 003-sem-lado-negativo
  ✗ sem MUST-NOT-CLAIM: — sem lado negativo o caso não discrimina
  ✗ nunca visto reprovando (First-red: pending) — rode o caso contra o ablado
──
casos: 3 · saudáveis: 1 · aposentados: 0
✗ o corpus não está saudável (veja acima).
```

O código de saída é 1. A saída completa, linha a linha, está no
[README do exemplo](exemplo/README.md).

### Como ler

Repare que o caso 002 **passa** no critério que a maioria dos times usaria — o alvo real acertou
— e mesmo assim é o caso mais grave do corpus. Ele está bem formado: tem alvo, eixo, os dois
lados das asserções, linha de base atual. Só que o grupo de controle acerta igual, e então o
passe do alvo não diz nada sobre o eixo declarado. Sem a segunda execução, esse corpus teria
dois verdes e um vermelho; com ela, tem um verde, e é o único que vale.

O caso 003 mostra a outra metade: o verificador o reprova **antes** de olhar qualquer resposta,
só pela forma. Um caso sem `MUST-NOT-CLAIM:` aceita qualquer resposta prolixa que mencione "um
problema", e o script nem se dá ao trabalho de julgar.

### Exercícios

O README traz cinco exercícios curtos [CLAIM-15-028], cada um com efeito previsível na saída:

1. **Aposentar o 002 com motivo** (`Status: retired` e `Retired-because:`). Ele passa a
   aparecer como aposentado, visível. Tire o motivo e ele volta a falhar: aposentar sem motivo é
   apagar.
2. **Retirar o 003.** Com o 002 aposentado e sem o 003, a saída termina em "todo caso nomeia um
   alvo real, discrimina e está atual" e o código de saída vira 0.
3. **Mudar o alvo.** Qualquer linha a mais em `alvos/revisor.md` faz o 001 acusar linha de base
   defasada. Aqui a linha de base guarda um *hash* do arquivo em vez do commit, para o exemplo
   rodar fora do git; o efeito é o do corolário C11.
4. **Afrouxar o lado negativo** do 001, apagando os `MUST-NOT-CLAIM:`. O caso cai na falha
   estrutural do 003, embora o alvo real continue acertando.
5. **Vazar a conclusão** no enunciado do 001 ("o FR2 não foi implementado"). O verificador
   continua verde. É o anti-padrão 20, e o exemplo é honesto sobre isso: nenhum script aqui o
   detecta. No Maestro, quem pega é o pré-voo do `/eval`, que manda reler o `case.md` procurando
   conclusão vazada — e, nos dois casos reais de agosto, quem pegou foram os próprios agentes
   avaliados.

### Levando para o seu time

O exemplo é pequeno de propósito; o que transfere é a forma. Escolha **um** agente cujo
julgamento você não pode perder — em geral o revisor. Escreva um caso a partir de uma
regressão que você já viu, com a entrada só de fatos. Escreva o lado negativo primeiro:
o que uma resposta errada, porém plausível, afirmaria. Rode contra o agente como ele é e contra o
mesmo agente sem a linha do eixo. Só registre a linha de base se o ablado reprovar. Se ele
passar, aposente o caso com o motivo escrito — esse motivo é informação sobre o seu agente, e
vale mais do que um verde.


## Contraexemplo

A disciplina do capítulo tem custo, e há lugares onde ela atrapalha. Quatro deles apareceram no
próprio Maestro.

### Quando a saída se compara por igualdade, avaliação é desperdício

O teorema T7 começa com uma condição: "onde a saída não é comparável". Se ela é comparável, a
ferramenta certa é o teste, e montar caso, fixture, ablação e linha de base para isso é
cerimônia. O exemplo mais limpo do repositório é o
[check-chapters.sh](https://github.com/GHDaru/maestro/blob/19823c2/scripts/check-chapters.sh).
No ciclo 016, as nove seções do capítulo 01 do guia do Maestro foram contadas **à mão** no
relatório de qualidade [CLAIM-15-014]. Contar seção não é julgamento: a seção existe ou não, na
ordem ou fora dela. Virou script no ciclo 022, e nenhum agente-juiz entra ali. A pergunta que
separa os dois mundos é simples: duas pessoas atentas discordariam do veredito? Se não, escreva
o comando do [capítulo 10](../10-quality-gates-que-provam-fatos/capitulo.md) e pare.

### A ablação dobra o custo e às vezes não decide nada

Cada caso exige pelo menos duas execuções em contexto fresco, e cada execução é uma chamada de
modelo que alguém paga. O caso 002 consumiu quatro rodadas e duas fixtures para terminar
aposentado [CLAIM-15-004]. Pior: o que ele "descobriu" — que a instrução de conferir a raia
talvez seja redundante no agente guardião — não pôde virar regra. Duas amostras não bastam para
remover instrução de um agente, e a retrospectiva do ciclo 041 fechou o achado como **gatilho**
no roteiro, a ser reavaliado quando houver um terceiro dado
([decisoes.jsonl](https://github.com/GHDaru/maestro/blob/19823c2/docs/records/decisoes.jsonl),
ids `achado-040-raia-sobredeterminada` e `retro-041-fecha-040c`) [CLAIM-15-022]. Quem espera da
avaliação uma resposta em toda rodada vai se frustrar: muitas vezes ela só diz "este caso não
mede o que você achava". É informação, mas não é decisão. Por isso o Maestro não fixa meta de
cobertura; o corpus cresce por regressão observada, e um time com um ou dois agentes estáveis
pode, honestamente, não ter caso nenhum ainda — desde que o portão diga "vazio", e não "verde".

### Avaliação às cegas pode mandar parar de polir

O mesmo desenho — um crítico em contexto fresco comparando sem saber qual é qual — foi usado
como barra de produto no ciclo 074: a tela do painel de regência contra um produto real, o
Maestri, em seis peças, e cada peça só fechava quando o crítico escolhesse a versão do Maestro
(`decisao-074-gauntlet-maestri`). A peça P3, a tela de andares, perdeu **quatro rodadas às
cegas** [CLAIM-15-021]. Da terceira rodada em diante a crítica deixou de falar de layout e
passou a falar de coerência de estado entre telas: decidir um pedido não fechava o andar, duas
telas divergiam, avisos descreviam o que não tinha acontecido. Nenhum polimento da página
resolveria, porque o estado vivia em dados de exemplo. A decisão registrada foi fechar a peça
como **perdida no protótipo** e transferi-la para um ciclo seguinte, refeita sobre o domínio
(`decisao-074-p3-transferida-076`). Aqui o contraexemplo é de expectativa: avaliação com grupo
de controle às vezes mostra que o trabalho certo é outro, e o custo de aceitar isso é jogar fora
rodadas de esforço. O custo de não aceitar seria pior — "ajustar a fixture até ficar verde", que
o `/eval` chama de pescaria.

### Conformidade verde não é verdade

O `check-conformance.sh` responde se o método **sobreviveu nos artefatos**. Ele não lê prosa
para saber se ela é verdadeira, e o Maestro tem dois registros disso. Em 22 de agosto de 2026,
verificou-se que o repositório remoto não tinha **tag nenhuma**: a v0.1.0 e a v0.2.0, descritas
no `CHANGELOG.md`, nunca tinham sido publicadas, e quatro tentativas de enviar a v0.3.0 morreram
na rede [CLAIM-15-019]. No dia seguinte, a revisão independente achou que o fechamento de um
achado do ciclo 055 tinha sido **afirmado falso**: a linha dizia que a correção não nomeava
arquivo nenhum, e a promessa seguia em dois documentos que o instalador não lê
(`achado-063-fechamento-do-055-foi-afirmado-falso`) [CLAIM-15-020]. Em ambos os casos os
portões estavam verdes. A correção veio por linha nova no índice de decisões — o histórico não
se reescreve — e por gente lendo. É o limite declarado da primeira camada: conformidade mede
forma e presença, não veracidade.

### O custo resumido

| Situação | Custo da disciplina | O que fazer |
|---|---|---|
| saída comparável por igualdade | caso, fixture e ablação sem necessidade | teste ou script |
| caso que não discrimina | rodadas pagas sem decisão | aposentar com motivo; gatilho, não regra |
| crítico às cegas reprova sempre | esforço descartado | parar, transferir, registrar |
| conformidade verde | falsa sensação de verdade | revisão humana e independente da prosa |

A regra do capítulo não dispensa o julgamento humano; ela o concentra onde nenhum comando chega.

## Evidência

Este capítulo é o lugar do livro onde a régua de evidência se aplica ao próprio livro. Cada
afirmação abaixo carrega um estado em [claims.md](claims.md): **medido** (reproduz-se com um
comando), **observado** (está registrado num artefato datado) ou **hipótese** (ainda não foi
testado). As três camadas da Teoria ditam a ordem.

### Camada 1 — conformidade: o que o repositório testemunha

O Maestro se aplicou a si mesmo. A fase F10 do roteiro, "o Maestro no Maestro", foi entregue no
ciclo 021 com o `check-install.sh`, que pergunta se o método está **instalado de verdade** — não
se os arquivos foram copiados, mas se a instrução que a IA lê ainda bate com o que está no disco.
A distinção que o script faz é a que importa para quem instala método em time: **instalar é
copiar; estar instalado é a IA saber que deve seguir**. Por isso ele confere três coisas — as
camadas do método no disco, a instrução que o agente lê de fato e se cada skill aparece nela —,
e não só a presença de arquivos. Na primeira execução ele achou três derivas com uma causa só:
o `AGENTS.md` mudo, uma skill invisível para o agente e o Constitution Check ainda nos princípios
I a VII quando a constituição já tinha o VIII — tudo listas escritas à mão que ninguém comparava
com o disco ([qa-report do ciclo 021](https://github.com/GHDaru/maestro/blob/19823c2/specs/021-maestro-instalado-no-maestro/qa-report.md))
[CLAIM-15-013]. A correção foi de estrutura, não de texto: fonte única e instrução gerada a
partir do disco. O roteiro marca a fase F10 como entregue
([roadmap.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/roadmap.md)). Esse é o padrão
de toda a evidência desta camada: o dado favorável e o desfavorável vêm do mesmo lugar, e o
desfavorável só apareceu porque havia um comando para tropeçar nele.

O favorável: quando o guia do Maestro ainda acompanhava 28 ciclos, 26 deles tinham os quatro
artefatos completos (spec, plano, tarefas, relatório de qualidade), e os dois restantes eram os
ciclos abertos naquele momento [CLAIM-15-015]. O desfavorável, medido no ciclo 042: **zero** de
quarenta ciclos tinha produzido algum dos artefatos condicionais — pesquisa, modelo de dados,
contratos, checklist, desenho de interface — **e registrado por quê**, e 35 de 40 `tasks.md`
tinham perdido o gate humano [CLAIM-15-016] [CLAIM-15-010]. Os artefatos obrigatórios
sobreviviam; os condicionais morriam em silêncio. O anti-padrão 22 dá nome ao mecanismo: o
executor segue **fielmente** o artefato que recebe, e o artefato é um subconjunto do método. Num
repositório companheiro, um `plan.md` parava em "documentação e portões verdes"; a cauda de
fechamento vivia na spec e na memória da sessão, a compactação de contexto promoveu a versão
truncada a fonte da verdade, e o agente foi direto para o *pull request* — obedecendo
perfeitamente. Omissão não viola nada que se veja. Daí os *tokens* `ART:`, o catálogo
[artifacts.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/artifacts.md) e um
portão que compara o que o executor consome com o que o método exige.

A caixa marcada antes da evidência é a mesma história em outro artefato, e a contagem dela é
ela própria uma lição de evidência. A spec do ciclo 045, escrita na abertura, fala em quatro
ocorrências entre os ciclos 042 e 044, em dois *tokens* (`TAIL:` e os critérios de aceite). O
relatório de qualidade do mesmo ciclo, escrito no fechamento, corrige o número: a revisão
independente achou uma **quinta**, durante o próprio 045 — duas linhas do índice de decisões
citando como registro um `qa-report.md` ainda em branco —, e o fecho é "cinco ocorrências, três
*tokens*" [CLAIM-15-018]. A resposta foi de forma, não de disciplina, e progrediu em três passos:
instrução no ciclo 043; no 045, os critérios de aceite da spec perderam as caixas, porque quem
diz se um critério valeu é o relatório de qualidade; e o `record-decision.sh` passou a recusar
linha que cite arquivo ainda em esqueleto
([qa-report do ciclo 045](https://github.com/GHDaru/maestro/blob/8b0ced3/specs/045-fechar-v0-1-0/qa-report.md)).
O relatório deixa registrada uma hipótese para uma sexta ocorrência: talvez a linha de fechamento
não deva ser escrita por quem executou o ciclo. Note a ordem das fontes: a spec descreve o estado
de antes, o relatório o de depois; citar só a primeira teria reproduzido aqui o erro que o
capítulo critica.
O mesmo ciclo fechou a v0.1.0, em 9 de agosto de 2026, depois de **zero** versões e zero tags em
44 ciclos: treze agentes, seis skills, vinte e dois anti-padrões, onze portões executáveis e um
corpus de avaliação com **um** caso provado por ablação [CLAIM-15-017]. A nota de release a
chama de linha de base, não de marco de completude — e, como mostrou o Contraexemplo, nem a tag
chegou ao remoto naquele momento [CLAIM-15-019].

### Camada 2 — regressão de julgamento: o que existe e o que falta

A evidência aqui é pequena e honesta. A fase F13 do roteiro, "julgamento com linha de base",
está marcada lá com um aviso e não com um visto: entregue com o portão vermelho de propósito,
linhas de base pendentes [CLAIM-15-024]. É raro um roteiro registrar a própria fase como
incompleta no ato da entrega, e é exatamente o que o T7 pede — o vermelho era o estado
verdadeiro; o primeiro caso ganhou linha de base no dia seguinte, provado por
ablação [CLAIM-15-003]; o segundo foi aposentado [CLAIM-15-004]. Até a v0.1.0, isso era o corpus
inteiro [CLAIM-15-017]. O que se pode afirmar com segurança é que o mecanismo **discrimina
pelo menos uma vez** e que ele **pegou defeito que o autor não viu** — as duas fixtures com
defeito [CLAIM-15-005]. O que não se pode afirmar é que os treze agentes [CLAIM-15-017] estão protegidos contra
regressão. A maioria não tem caso. O roteiro registra isso como gatilho, não como meta.

### Camada 3 — efeito: a agenda, explícita

Nada no repositório prova que o Maestro produz software melhor do que a alternativa. O livro
registra a pergunta como agenda de pesquisa, com dez hipóteses
([base de pesquisa](../../pesquisa/base-de-pesquisa.md)) [CLAIM-15-009]. A base dá a lista, o
desenho geral e o catálogo de métricas; ela não diz, hipótese por hipótese, o que mediria cada
uma nem o que a derrubaria. A tabela abaixo faz esse trabalho e é **proposta deste capítulo**,
não resultado: cada linha diz o que contar, contra qual comparação, e qual resultado obrigaria a
abandonar a hipótese. As métricas vêm todas do catálogo da base (custo por tarefa aceita,
retrabalho, escape de gate, rendimento da revisão independente, aceitação na primeira passada,
tokens por tarefa, tempo de ciclo).

| Hipótese | O que mediria | Comparação | O que a refutaria | Capítulo |
|---|---|---|---|---|
| H1 — spec reduz retrabalho | retrabalho por tarefa aceita (mudanças depois da primeira entrega) | nível A (só prompt) × B (prompt e spec) | B sem queda de retrabalho fora do intervalo das repetições de A | [04](../04-a-spec-como-partitura/capitulo.md) |
| H2 — revisão em contexto fresco acha mais defeito | rendimento da revisão: defeitos semeados achados sobre defeitos semeados | revisor fresco × o próprio executor revisando, mesma entrada | taxas indistinguíveis, ou o executor achando mais | [03](../03-um-humano-muitos-agentes/capitulo.md) |
| H3 — contexto seletivo reduz custo sem perder qualidade | tokens por tarefa **e** aceitação na primeira passada | contexto selecionado × contexto inteiro | o custo cai, mas a aceitação cai junto além do intervalo | [05](../05-engenharia-de-contexto/capitulo.md) |
| H4 — multiagente só ajuda com cortes independentes | tempo de ciclo e retrabalho de integração | um agente × vários, com corte independente e com corte acoplado | vários agentes ganhando também no corte acoplado, ou não ganhando no independente | [06](../06-como-dividir-o-trabalho/capitulo.md) |
| H5 — gate com mutação reduz escapes | escape de gate: defeito que passou e foi achado depois | nível C sem mutação × C com mutação | a mesma taxa de escape | [10](../10-quality-gates-que-provam-fatos/capitulo.md) |
| H6 — catálogo semântico reduz duplicação | componentes duplicados criados por tarefa | com × sem consulta ao catálogo antes de criar | a mesma taxa de duplicação | [08](../08-ddd-para-agentes/capitulo.md) |
| H7 — glossário reduz inconsistência | termos divergentes para o mesmo conceito nos artefatos | com × sem glossário na instrução | a mesma contagem | [08](../08-ddd-para-agentes/capitulo.md) |
| H8 — reversibilidade permite mais autonomia | ações delegadas sem pedido humano, a incidente constante | com × sem reversibilidade de engenharia (backup, *dry run*) | mais autonomia só com mais incidente | [11](../11-risco-reversibilidade-e-autonomia/capitulo.md) |
| H9 — modelo menor basta em tarefa estruturada | aceitação e custo por tarefa aceita | modelo menor × maior, no nível C | aceitação do menor abaixo da do maior além do intervalo | [13](../13-observabilidade-e-economia/capitulo.md) |
| H10 — retrospectiva que vira regra reduz recorrência | recorrência do mesmo achado depois da regra | ciclos antes × depois da regra, no corpus histórico | a mesma classe de achado voltando no mesmo ritmo | [14](../14-a-organizacao-que-aprende/capitulo.md) |

Todas estão no estado **hipótese**. O desenho comum tem quatro níveis — linha de base A só com
prompt, B com spec, C com spec e portões, e o tratamento com o método completo. Dois requisitos
desse desenho decidem se o resultado vale alguma coisa, e o capítulo já mostrou por quê.

**Repetições com distribuição.** Um agente não responde igual duas vezes. Uma execução por nível
é uma anedota; o desenho pede várias e compara distribuições com intervalo, não médias soltas.
Por isso a coluna "o que a refutaria" fala em "fora do intervalo": uma diferença menor que a
variação entre repetições do mesmo nível não é efeito. É a versão estatística da lição do caso
002 — duas amostras não bastam para tirar uma instrução de um agente.

**Ambiente congelado.** Cada execução registra commit do método, modelo, *harness* e *hashes* das
entradas. Sem isso, a comparação mistura o efeito do método com a troca silenciosa de modelo ou
com uma mudança de instrução — o mesmo problema que o C11 trata no corpus de avaliações, quando a
linha de base envelhece com o alvo. Um experimento é, no fundo, uma linha de base com grupo de
controle e muitas repetições.

**Os corpora.** São dois. Os ciclos históricos do Maestro já existem, são datados e têm achados
registrados por linha nova; servem bem a hipóteses observacionais como a H10, porque permitem
contar recorrência antes e depois de uma regra — a caixa marcada antes da evidência, com suas
cinco ocorrências [CLAIM-15-018], é o tipo de série que esse corpus oferece. O limite é que eles
não têm grupo de controle: cada ciclo rodou uma vez, com um método só, e o próprio método mudou
ao longo deles. Os corpora externos, como o SWE-bench e o SWE-Bench Pro, têm tarefa fixa e teste
que decide; servem para rodar os níveis A a C sobre o mesmo problema e comparar com o que a
literatura mede, mas só tocam o que se decide por teste.

Duas ressalvas impedem de ler a camada 1 como prova da camada 3. A primeira é a origem: o método
nasceu de um prompt de pesquisa profunda sobre práticas de desenvolvimento com humano e agentes,
datado de 22 de julho de 2026 [CLAIM-15-026]
([prompt da pesquisa](https://github.com/GHDaru/maestro/blob/19823c2/docs/research/prompt-pesquisa-praticas-desenvolvimento.md)).
Isso dá fundamento na literatura, não evidência de efeito. A segunda é que o próprio desenho do
processo ainda está em discussão: a proposta de fluxo v5, do ciclo 053, comparou o ciclo de vida
do Maestro com um de 13 passos desenhado por um arquiteto externo e concluiu que seis das
dezesseis caixas mudariam [CLAIM-15-023]; ela não está vigente. Medir efeito de um processo que
ainda muda exige congelar a versão medida — daí a exigência de commit no ambiente.

### O livro sob a mesma régua

Este livro não pede ao leitor um padrão que ele mesmo não segue, e a ligação com o tema é
direta: um livro sobre validar método também é um artefato que precisa de critério antes de
conteúdo. Ele foi desenhado de trás para frente, como o guia editorial do Maestro já fazia com
o *Backward Design* de Wiggins e McTighe: objetivos, depois como se verifica que foram
atingidos, só então o conteúdo
([guia editorial do Maestro](https://github.com/GHDaru/maestro/blob/19823c2/docs/livro/guia-editorial.md)).
É a mesma ordem do caso de avaliação: o `expect.md` — o que a resposta certa acha e o que a
errada afirmaria — é escrito antes de qualquer resposta existir, e o "Resultado de
aprendizagem" de cada capítulo é escrito antes do texto que o cumpre.

O guia do Maestro tinha esqueleto de nove seções, com o exemplo real obrigatório: sem ele o
capítulo não publicava. Este livro herdou a regra e a ampliou para as onze seções da anatomia
proposta na base de pesquisa, num sumário de dezesseis capítulos [CLAIM-15-025]. A seção que
pesa aqui é a "falha real antes da regra": é o equivalente editorial do `First-red`, a
exigência de ter visto o problema acontecer antes de escrever a regra que o previne.

A base organiza o conhecimento em quatro corpora — o método normativo, o guia do método por
versão, o livro e a pesquisa (protocolo, execuções, dados, replicação). A separação acompanha as
três camadas: o método normativo e o guia são o que a conformidade confere; o livro é o
argumento; a pesquisa é onde mora o protocolo que testaria o efeito. Misturar os dois últimos é
o erro que este capítulo combate — apresentar argumento como resultado. E a regra que você viu
em todo capítulo, "nenhum número sem claim", vem da mesma agenda: cada `claims.md` é a versão
por capítulo do `CLAIMS.md` previsto lá. Um número que não se reproduz vira hipótese ou sai.

## Checklist

Itens que você aplica no próprio time, cada um com o jeito de verificar. Estão na ordem das três
camadas; comece pela primeira.

### Conformidade

1. **A pergunta "estamos seguindo o processo?" tem um comando como resposta.** Verificação: existe
   um script no repositório que lê os artefatos do ciclo e sai com código diferente de zero
   quando falta algo; a instrução dos agentes manda rodá-lo em vez de responder de memória.
2. **Artefato opcional é declarado, nunca omitido.** Verificação: todo plano carrega uma linha
   legível por máquina para cada artefato condicional (`=yes`, ou `=no` com motivo); uma busca
   nos planos dos últimos ciclos não acha nenhum sem a declaração.
3. **A cauda de fechamento tem evidência, não só caixa.** Verificação: um portão bloqueante na
   integração contínua reprova caixa marcada cujo relatório está vazio ou diz "pendente"; você
   já o viu reprovar pelo menos uma vez.
4. **O método instalado é o método inteiro.** Verificação: um script instala o processo num
   diretório vazio e roda os portões lá dentro; ele acusa referência a arquivo que a instalação
   não copia.
5. **O estado do processo entra na sessão medido, não lembrado.** Verificação: o início de cada
   sessão do agente recebe a saída de um comando (ciclo aberto, conformidade, achados abertos),
   não um parágrafo fixo na instrução.

### Regressão de julgamento

6. **Existe ao menos um caso de avaliação para o agente cujo julgamento você não pode perder.**
   Verificação: há uma pasta por caso, com alvo nomeado por caminho, pergunta e eixo.
7. **Todo caso tem lado negativo.** Verificação: cada caso tem pelo menos uma asserção do tipo
   "a resposta não pode afirmar…", escrita a partir do que uma resposta errada e plausível diria.
8. **Todo passe foi precedido de um vermelho no alvo ablado.** Verificação: a linha de base
   registra a execução contra o mesmo agente sem a linha do eixo, com o veredito reprovado e a
   data. Sem isso, o campo de primeira reprovação continua "pendente" e o portão fica vermelho.
9. **A premissa da fixture foi conferida antes da execução.** Verificação: a linha de base
   registra como a premissa foi reproduzida (comando, arquivo, linha); o enunciado traz fatos, e
   nenhuma conclusão que o alvo deveria tirar.
10. **A linha de base envelhece com o alvo.** Verificação: mudar uma linha da instrução do agente
    faz o portão acusar a linha de base defasada.
11. **Caso que não discrimina é aposentado com motivo.** Verificação: casos aposentados aparecem
    na saída do portão com o motivo; apagar o caso, ou aposentá-lo sem motivo, reprova.
12. **O portão do corpus não exige chave de API.** Verificação: qualquer colaborador roda o
    portão sem credencial; o julgamento com modelo roda sob demanda, em contexto fresco.
13. **O corpus cresce por regressão, não por meta.** Verificação: cada caso novo cita a
    regressão observada que o originou.

### Efeito

14. **Nenhum número sobre o processo circula sem registro.** Verificação: toda afirmação
    quantitativa nos documentos do time tem id, estado (medido, observado ou hipótese) e o
    comando ou arquivo que a reproduz.
15. **"O método funciona" fica marcado como hipótese até haver comparação.** Verificação: a
    afirmação aparece com nível de tratamento, repetições e ambiente congelado (commit, modelo,
    *harness*), ou aparece como hipótese.
16. **Métricas de entrega são acompanhadas, não usadas como prova.** Verificação: o painel de
    métricas não atribui causa sem grupo de comparação.
17. **O dado desfavorável é registrado no mesmo lugar do favorável.** Verificação: o índice de
    decisões tem achados que corrigem afirmações anteriores por linha nova, sem reescrever a
    antiga.

Se só houver tempo para três itens, faça o 1, o 7 e o 8. O primeiro troca a memória por fato; os
outros dois separam um caso de avaliação de uma esperança.

## Referências

### Maestro (versão `19823c2`, salvo indicação)

- Teorema T7 e corolários C11 e C13 —
  [docs/governance/axioms.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/axioms.md)
- Glossário (avaliação, teste, benchmark) —
  [docs/governance/glossary.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/glossary.md)
- Catálogo de artefatos condicionais —
  [docs/governance/artifacts.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/artifacts.md)
- ADR 0016, avaliações para saída não-determinística —
  [docs/adr/0016-evals-para-saida-nao-deterministica.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0016-evals-para-saida-nao-deterministica.md)
- ADR 0019, conformidade executável —
  [docs/adr/0019-conformidade-executavel-e-catalogo-de-artefatos.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0019-conformidade-executavel-e-catalogo-de-artefatos.md)
- Anti-padrões 13, 19, 20 e 22 —
  [skills/anti-patterns/SKILL.md](https://github.com/GHDaru/maestro/blob/19823c2/skills/anti-patterns/SKILL.md)
- Corpus de avaliações —
  [evals/README.md](https://github.com/GHDaru/maestro/blob/19823c2/evals/README.md);
  [caso 001](https://github.com/GHDaru/maestro/blob/19823c2/evals/001-review-drops-a-requirement/baseline.md);
  [caso 002](https://github.com/GHDaru/maestro/blob/19823c2/evals/002-guardian-accepts-a-wrong-lane/baseline.md)
- Comando `/eval` —
  [.claude/commands/eval.md](https://github.com/GHDaru/maestro/blob/19823c2/.claude/commands/eval.md)
- Portões —
  [check-evals.sh](https://github.com/GHDaru/maestro/blob/19823c2/scripts/check-evals.sh),
  [check-conformance.sh](https://github.com/GHDaru/maestro/blob/19823c2/scripts/check-conformance.sh),
  [check-install.sh](https://github.com/GHDaru/maestro/blob/19823c2/scripts/check-install.sh),
  [check-chapters.sh](https://github.com/GHDaru/maestro/blob/19823c2/scripts/check-chapters.sh),
  [hooks/session-state.sh](https://github.com/GHDaru/maestro/blob/19823c2/scripts/hooks/session-state.sh),
  [ci.yml](https://github.com/GHDaru/maestro/blob/19823c2/.github/workflows/ci.yml)
- Índice de decisões (achados 037, 040, 041, 062 e 063; decisões do ciclo 074) —
  [docs/records/decisoes.jsonl](https://github.com/GHDaru/maestro/blob/19823c2/docs/records/decisoes.jsonl)
- Roteiro (F10, F13 e o gatilho de cobertura de avaliações) —
  [docs/roadmap.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/roadmap.md)
- Nota de release da v0.1.0 —
  [CHANGELOG.md](https://github.com/GHDaru/maestro/blob/19823c2/CHANGELOG.md)
- Ciclos citados —
  [021](https://github.com/GHDaru/maestro/blob/19823c2/specs/021-maestro-instalado-no-maestro/qa-report.md),
  [037](https://github.com/GHDaru/maestro/blob/19823c2/specs/037-evals-linha-de-base/spec.md),
  [041](https://github.com/GHDaru/maestro/blob/19823c2/specs/041-retro-dos-quatro-achados-de-eval/qa-report.md),
  [042](https://github.com/GHDaru/maestro/blob/19823c2/specs/042-conformidade-executavel/spec.md),
  [045 spec](https://github.com/GHDaru/maestro/blob/8b0ced3/specs/045-fechar-v0-1-0/spec.md) e [045 qa-report](https://github.com/GHDaru/maestro/blob/8b0ced3/specs/045-fechar-v0-1-0/qa-report.md) (versão `8b0ced3`)
- Crítica às cegas da peça P3 —
  [critica-p3-rodada-4.md](https://github.com/GHDaru/maestro/blob/19823c2/specs/074-prototipo-navegavel/gauntlet-maestri/critica-p3-rodada-4.md)
- Prompt da pesquisa profunda —
  [docs/research/prompt-pesquisa-praticas-desenvolvimento.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/research/prompt-pesquisa-praticas-desenvolvimento.md)
- Guia editorial do Maestro —
  [docs/livro/guia-editorial.md](https://github.com/GHDaru/maestro/blob/19823c2/docs/livro/guia-editorial.md)

### Deste livro

- Base de pesquisa (hipóteses H1–H10, desenho, corpora) —
  [pesquisa/base-de-pesquisa.md](../../pesquisa/base-de-pesquisa.md)
- Guia do método por versão: `maestro-handbook/handbook/08-entregaveis-artefatos.md` §6 e
  `maestro-handbook/diagramas/06-fluxo-v5-proposta.md`, na raiz do repositório do livro
- [Capítulo 10 — Quality gates que provam fatos](../10-quality-gates-que-provam-fatos/capitulo.md);
  [Capítulo 13 — Observabilidade e economia](../13-observabilidade-e-economia/capitulo.md);
  [Capítulo 14 — A organização que aprende](../14-a-organizacao-que-aprende/capitulo.md)

### Externas

- Jimenez, C. E. et al. *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?*
  International Conference on Learning Representations (ICLR), 2024. https://www.swebench.com
  (acesso em 02/11/2026).
- Deng, X. et al. *SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks?*
  arXiv:2509.16941, 2025. https://arxiv.org/abs/2509.16941 (acesso em 02/11/2026).
- Wiggins, G.; McTighe, J. *Understanding by Design*. 2. ed. ASCD, 2005.
- Zheng, L. et al. *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*. NeurIPS Datasets and
  Benchmarks Track, 2023 — origem do padrão citado na alternativa "juiz automático".
- OpenAI Evals — https://github.com/openai/evals (acesso em 02/11/2026).
- promptfoo — https://www.promptfoo.dev; asserções negadas com `not-` em
  https://www.promptfoo.dev/docs/configuration/expected-outputs/ (acesso em 02/11/2026).
- DORA — https://dora.dev (acesso em 02/11/2026).
