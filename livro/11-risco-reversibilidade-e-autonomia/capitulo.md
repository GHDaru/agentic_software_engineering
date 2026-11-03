# 11 — Risco, reversibilidade e autonomia

> "A pergunta errada é 'quando confio no agente?'. A pergunta certa é 'quanto custa desfazer?'."
> — handbook do Maestro, capítulo 13, §5.7

Todo tech lead que coloca agentes para trabalhar chega à mesma bifurcação. Ou aprova tudo o
que o agente faz, e em duas semanas vira o gargalo do time e começa a aprovar sem ler. Ou
libera, e espera que nada irreversível passe junto com o trivial. Este capítulo defende uma
terceira saída, que não é um meio-termo: o peso do gate humano depende do **custo de desfazer**
a ação e do **raio** que ela atinge, e não do tanto que você confia no agente. E como o custo
de desfazer é algo que se constrói, a autonomia do agente também é: você a compra com
reversibilidade, não com fé.

## Pergunta central

Quanta autonomia dar a cada ação de um agente, e como aumentar essa autonomia sem aumentar o
risco?

## Resultado de aprendizagem

Ao final, você consegue:

1. **Classificar** uma ação de agente numa escada de sete classes de risco a partir de dois
   eixos (custo de desfazer e raio de impacto), e não do verbo que a descreve.
2. **Explicar** por que o gate uniforme sempre falha, nas duas direções, e reconhecer cada uma
   das falhas no seu time.
3. **Rebaixar** a classe de uma ação com uma alavanca de reversibilidade (cópia de segurança,
   execução a seco, homologação, exclusão lógica, cópia ao lado) em vez de somar mais uma
   aprovação.
4. **Escrever** uma política `permitir / perguntar / negar` por classe de ação, mantida fora do
   modelo, e dizer o que nela é regra, o que é script e o que é *hook*.
5. **Reclassificar** um componente quando ele ganha uma capacidade nova, antes que a revisão ou
   o incidente façam isso por você.

## A falha real

Em 11 de agosto de 2026, o Maestro (o método de governança de agentes que este livro usa como
objeto de estudo) fechou a versão 0.2.0. A revisão independente desse fechamento abriu um
achado incômodo: reinstalar o método num projeto não entregava nada. O instalador pulava todo
destino que já existisse, e depois da primeira instalação todo diretório existe. A segunda
execução imprimia `= exists (kept)` para tudo, com zero arquivos entregues. Pior: o contorno
que a nota de lançamento recomendava, o `--force`, fazia um `cp -r` sobre diretório existente e
**aninhava** o conteúdo, criando `.claude/agents/agents/` e corrompendo o layout
[CLAIM-11-001].

Não era um defeito cosmético. Três ciclos antes, no 048, a revisão independente tinha achado
que o comando herdado do Spec Kit para a constituição do projeto carregava instruções do
projeto original ("este arquivo é um template, escreva de volta") e, apontado para a
constituição já ratificada, mandava o agente regenerá-la. O comando foi corrigido para emendar,
nunca regenerar [CLAIM-11-002]. Mas quem tinha instalado a versão antiga continuaria com o
comando destrutivo para sempre, porque reinstalar não entregava a correção. A spec do ciclo
seguinte escreveu a frase que resume o problema: instalação que só acumula carrega os erros do
método para sempre [CLAIM-11-003].

O ciclo 051 nasceu para corrigir isso. A ideia era boa: o instalador passa a gravar um
**manifesto** com o hash de cada arquivo que escreveu. Com ele, sabe distinguir versão velha
(arquivo inalterado desde a última instalação, que pode ser atualizado) de arquivo que o
projeto editou (que deve ser mantido, com a versão nova oferecida ao lado como
`.maestro-new`). E passa a **podar** o que o método deixou de enviar, se ainda estiver
inalterado. A spec declarou a raia plena (o fluxo completo, com especificação) e justificou com
os três fatores: ambiguidade média, raio amplo ("roda dentro de repositórios de terceiros e
**apaga** arquivos") e irreversibilidade alta o bastante para exigir cuidado [CLAIM-11-004].

O autor sabia que estava mexendo em algo perigoso. Mesmo assim, a revisão independente em
contexto fresco devolveu o veredito "não promover como está", com dois bloqueantes e cinco
achados relevantes [CLAIM-11-005]. O primeiro bloqueante, nas palavras do próprio relatório, foi
"o pior defeito que eu poderia ter escrito neste ciclo": o instalador gravava o caminho no
manifesto **antes** de decidir o que fazer com ele. Um arquivo que o projeto já tinha e que por
acaso fosse idêntico byte a byte ao do método (o caso real de quem rodou o `specify init` por
conta própria) era adotado como do método sem uma linha de saída, e a poda o apagaria no
lançamento seguinte. O segundo: `--force --dry-run` lia só o segundo argumento e virava
`FORCE=1 DRY=0`. A flag destrutiva vencia, e o freio era ignorado, no único script do método que
apaga [CLAIM-11-006]. Entre os relevantes: o `--force` destruía edição do projeto **sem cópia**,
enquanto a saída do próprio instalador o recomendava; e a poda aceitava `../` vindo do
manifesto, que mora no repositório alheio e é comitável por qualquer um, e apagou um arquivo
fora do alvo [CLAIM-11-007].

Tudo foi corrigido no mesmo ciclo, e os três ataques do revisor foram repetidos contra a versão
corrigida (commit `c9e5220`). A revisão de segurança, no mesmo relatório, escreveu: "esta é a
classe de risco mais alta da sessão". E declarou um limite: um *symlink* de diretório dentro do
alvo fazia o `cp` escrever através dele, e agora a poda apagaria através dele. O achado ficou
aberto no índice de decisões e virou o ciclo 052, de raia leve, que fez o instalador **recusar**
escrever ou remover através de *symlink* e contar cada recusa no resumo, porque "recusa
silenciosa é indistinguível de 'nada a fazer'" (commit `0e821b1`) [CLAIM-11-008].

O que importa aqui não é que um agente errou. O texto do 051 é bom, os requisitos estão em
sintaxe controlada, a raia está certa. O que aconteceu é mais sutil: **o script mudou de classe
de risco sem que nada no processo mudasse de classe junto.** Até o 050, o instalador só
acrescentava; o pior que fazia era não entregar. No 051, ganhou o poder de apagar em
repositório alheio, e com isso subiu dois degraus na escada de risco. A revisão independente
pegou a diferença, mas pegou porque existia, e não porque alguém tivesse reclassificado o
componente quando a capacidade mudou. A pergunta deste capítulo nasce aí: como se decide,
ação por ação, quanto o agente pode fazer sozinho, e o que muda quando a ação muda?

## Teoria

### O axioma: fazer e desfazer não custam o mesmo

O Maestro deriva sua regra de risco de dois axiomas [CLAIM-11-009]. O primeiro, A5, diz que o
custo é assimétrico entre fazer e desfazer: produzir é barato e fica mais barato a cada
geração de modelo; apagar dados, implantar, migrar e publicar têm custos que nenhuma
velocidade compensa. O segundo, A2, diz que consequência precisa de dono: a responsabilidade
não se transfere ao agente, não por falta de capacidade de raciocínio, mas por falta de
exposição à consequência (o [capítulo 2](../02-o-problema-da-confianca/capitulo.md) trata
disso).

Dos dois sai o teorema T3: **o gate escala com a irreversibilidade, nunca de forma uniforme.**
Se desfazer custa diferente de fazer (A5) e alguém responde pelo resultado (A2), um gate igual
para tudo está sempre errado. O axioma traz junto o seu teste de independência: retire A5 e
toda ação merece o mesmo tratamento, que é exatamente o gate uniforme que o método rejeita.

O [capítulo 1](../01-a-mudanca-de-unidade-de-trabalho/capitulo.md) mostrou o lado econômico de
A5: quando gerar código fica barato, o que fica caro é verificar. Este capítulo mostra o outro
lado: quando gerar fica barato, o que fica caro é **errar de forma que não se desfaz**. Um agente
que produz dezenas de commits numa branch erra muito e barato. Um agente que roda uma
migração destrutiva erra uma vez e caro. A diferença entre os dois não está no agente.

### Os dois fracassos simétricos

O gate uniforme falha de dois jeitos, e cada time costuma conhecer só um deles.

**Pesado em tudo**, o humano vira funil e, pior, carimbo. O handbook do Maestro diz isso com
uma frase de efeito, a de que quem aprova duzentos itens por dia não aprova nenhum de verdade
[CLAIM-11-010]. O número é retórico, mas o fenômeno é velho e estudado. Lisanne Bainbridge o
descreveu em 1983 como uma das "ironias da automação": quanto mais o sistema acerta, menos o
humano que o supervisiona consegue de fato supervisionar, porque a atenção não se sustenta
sobre um fluxo que quase nunca exige intervenção. O carimbo é pior que a ausência de gate,
porque tem a aparência de controle. Ele produz registros de aprovação que ninguém deu de
verdade.

**Leve em tudo**, a ação irreversível passa sem que ninguém tenha olhado. E aí entra uma
distinção que o handbook faz com precisão: o registro auditável é *ex-post*, descreve a decisão
depois de tomada; o gate é *ex-ante*, barra antes de executar. Para ação reversível, auditar
depois basta, porque o erro achado na auditoria se desfaz. Para ação irreversível, auditar não
impede o dano: o relatório perfeito de um dado apagado não traz o dado de volta
[CLAIM-11-011]. Confundir auditoria com controle é o anti-padrão que o método nomeia ao lado do
gate uniforme.

A saída não é calibrar um gate único "no meio". Um gate médio para tudo é pesado demais para o
trivial e leve demais para o irreversível ao mesmo tempo. A saída é ter **vários gates**, e uma
regra que diga qual vale para cada ação.

### A classe vem do custo de desfazer, não do verbo

A tentação é classificar pelo verbo: ler é seguro, escrever é médio, apagar é perigoso. Dois
casos registrados no Maestro, ambos de outubro de 2026, mostram por que isso não funciona.

O primeiro é uma leitura. Ao montar um painel para uma segunda equipe de agentes, o dono do
método decidiu **não** copiar o arquivo `.env` de produção de outro projeto para a máquina onde
os agentes rodam. O registro da decisão classifica a ação como irreversível, com a justificativa
inteira em uma linha: segredo lido por qualquer sessão de agente não se "desvê", só se rotaciona.
Por isso a decisão ficou com o humano [CLAIM-11-012]. Ler é o verbo mais inocente que existe, e
mesmo assim esta leitura caiu na classe mais alta que um agente pode tocar, porque o efeito dela
(o segredo dentro de um contexto que você não controla mais) não tem desfazer.

O segundo é o contrário. A tabela de gates do modelo operacional do Maestro põe `push` na
classe "exclusão ou efeito externo", que pede confirmação forte [CLAIM-11-013]. E a configuração
dos agentes construtores negava `git push` de forma geral. Em 20 de outubro, o dono do método
abriu uma exceção para a sessão regente (a que coordena os outros agentes e não escreve código)
empurrar branches de trabalho. A justificativa classifica a ação: branch nova no remoto é
reversível (apagável), com raio zero sobre as branches de integração e principal. O que não
mudou foi escrito junto: merge e promoção continuam com o gate humano, e os agentes
construtores continuam sem push. O primeiro uso foi uma branch com 56 commits de quatro ciclos
[CLAIM-11-014].

Um verbo inocente na classe mais alta; um verbo "externo" na classe de criação reversível. O que
separa os dois casos são dois eixos:

- **Custo de desfazer**: nada (não houve efeito), trivial (`git revert`, apagar a branch), barato
  (restaurar de uma exclusão lógica), caro (restaurar de um *backup*, refazer à mão) ou
  impossível (segredo lido, e-mail enviado, dado apagado sem cópia).
- **Raio de impacto** (*blast radius*): o ambiente do próprio agente (sua branch, sua cópia de
  trabalho, uma homologação descartável), algo compartilhado com o time, algo externo (produção,
  um terceiro, o repositório de um cliente) ou vários inquilinos de uma vez.

O mesmo cruzamento aparece no Princípio III da constituição do Maestro, o único marcado como
não negociável: o gate humano escala com irreversibilidade vezes raio de impacto [CLAIM-11-015].

### A escada de sete classes

Com os dois eixos, a escada fica assim. É a taxonomia do modelo operacional do Maestro, que o
handbook explica com exemplos [CLAIM-11-016]:

| Classe | Exemplo | Agente sozinho? | Gate humano |
|---|---|---|---|
| 0. Leitura | explorar, buscar | sim | nenhum |
| 1. Leitura sensível | dados pessoais, segredos | com política e máscara | revisão |
| 2. Criação reversível | *feature* numa branch, rascunho | sim | no merge |
| 3. Alteração | refatoração ampla, mudança de contrato | não | aprovação com resumo |
| 4. Exclusão ou efeito externo | apagar dados, chamar serviço externo, *push* | não | confirmação forte |
| 5. Financeira ou irreversível | implantação em produção, migração destrutiva | não | dupla aprovação ou reautenticação |
| 6. Lote, entre inquilinos, administrativa | migração em massa, ação administrativa | **bloqueada** | fluxo humano formal |

Duas coisas nesta tabela merecem atenção do tech lead. A primeira é que a autonomia do agente
cai de "sim" para "não" entre as classes 2 e 3, e essa é a linha que mais importa no dia a dia:
tudo o que fica na branch do agente é dele; tudo o que sai dela passa por alguém. A segunda é a
classe 6. Ela não é "dupla aprovação com mais rigor": é **bloqueada**. O agente não executa, nem
com aprovação. A ação vira um fluxo humano formal, porque nessa classe o raio é tão largo que
qualquer erro de classificação (do agente ou do humano que aprova) se multiplica por todos os
inquilinos atingidos.

Ação administrativa inclui uma categoria que costuma passar despercebida: o agente mexer na
**própria autorização**. No ciclo 075, a revisão de segurança mediu que uma sessão de agente
capaz de escrever no banco de dados do painel de regência poderia se dar qualquer endereço,
porque é nesse banco que mora o registro que transforma um *token* em identidade. A correção
foi uma guarda que recusa qualquer escrita de agente nesse banco, inclusive pelo shell, antes de
a escrita acontecer [CLAIM-11-017]. Quem escreve a regra que o julga não está sendo julgado.

### Dois eixos, a mesma física

O Maestro usa um cruzamento parecido para outra decisão: quanto **processo** uma mudança recebe.
A raia (leve, plena ou infra) é escolhida por ambiguidade vezes raio vezes irreversibilidade; o
gate é escolhido por irreversibilidade vezes impacto [CLAIM-11-018]. Processo é para construir a coisa
certa; gate é para agir no mundo. Um protótipo de tela é ambíguo e reversível (muita spec,
nenhum gate especial); apagar uma tabela morta é claro e irreversível (pouca spec, gate pesado).
Uma spec bem escrita não dispensa o gate, nem o gate dispensa a spec. O
[capítulo 4](../04-a-spec-como-partitura/capitulo.md) trata das raias.

### A alavanca: reversibilidade rebaixa a classe

Se a classe vem do custo de desfazer e do raio, então ela **não é um dado da ação**: é algo que
você pode mudar. Esse é o corolário C4 do Maestro, derivado de T3: reversibilidade rebaixa a
classe de risco, e é mais barata que mais uma aprovação [CLAIM-11-019].

O handbook dá o argumento em duas frases. O gate humano sempre foi um *proxy* de "torne
reversível, ou olhe antes". Onde existe *backup*, execução a seco (*dry run*), homologação
(*staging*) e exclusão lógica (*soft delete*), a ação muda de classe e passa a ser delegável;
reversibilidade compra velocidade [CLAIM-11-020].

Vale olhar cada alavanca pelo eixo em que ela age, porque é isso que permite escolher a mais
barata:

- **Cópia de segurança** age no custo de desfazer: o que era impossível passa a ser caro
  (restaurar leva tempo, mas é possível). Desce uma classe.
- **Exclusão lógica** age no custo de desfazer: apagar vira marcar, e desfazer vira desmarcar.
  Desce duas.
- **Cópia ao lado** (o `.maestro-old` do instalador corrigido no 051) é a exclusão lógica de um
  arquivo: a edição do projeto volta com um `mv`.
- **Homologação** age no raio: a mesma migração destrutiva, rodada num ambiente descartável, só
  atinge o ambiente do próprio agente.
- **Execução a seco** age nos dois de uma vez: a ação ensaiada não tem efeito, e por isso é
  leitura. O agente pode ensaiar quantas vezes quiser; o gate fica para a execução real, que
  agora chega ao humano com a saída do ensaio anexada.

Jeff Bezos popularizou uma distinção parecida na carta aos acionistas da Amazon de 2015:
decisões de "porta de mão única" (consequentes e irreversíveis, que pedem deliberação) e de
"porta de mão dupla" (reversíveis, que devem ser tomadas rápido, por pessoas ou grupos com bom
julgamento). A contribuição do C4 é um passo além: **transformar porta de mão única em porta de
mão dupla é trabalho de engenharia**, e esse trabalho costuma custar menos que o gate que ele
dispensa.

O custo existe e precisa ser dito. Escrever o *rollback* antes de precisar dele, manter um
ambiente de homologação, guardar cópias: tudo isso é engenharia antecipada. O handbook resume o
efeito como "velocidade com segurança: erra-se barato, logo corre-se rápido", com o alerta de que
o custo vem antes do benefício [CLAIM-11-021].

### Autonomia como função, não como estágio de confiança

Junte as peças e a autonomia do agente deixa de ser um estágio de maturidade ("quando eu
confiar, delego") e vira uma função da classe da ação. A base de pesquisa do livro chama isso de
"autonomia proporcional à irreversibilidade vezes raio" [CLAIM-11-022]. E como a classe se
engenheira, a autonomia também.

Isso muda a pergunta que o tech lead faz ao time. Em vez de "o agente já está bom o bastante
para fazer migração sozinho?", a pergunta passa a ser "o que falta para a migração ser
ensaiável a seco, testável em homologação e reversível em produção?". A primeira pergunta não
tem resposta: a confiança estatística perfeita nunca chega, e o handbook lista "esperar
confiança estatística antes de delegar" entre os anti-padrões do princípio [CLAIM-11-023]. A
segunda tem resposta, tem dono e tem prazo.

Uma ressalva honesta. Que reversibilidade **permite** mais autonomia com o mesmo risco é a
hipótese H8 da base de pesquisa do livro [CLAIM-11-024], e não um resultado medido. O que o
Maestro mostra é um caso, discutido em "O padrão Maestro": um repositório em que quase toda
ação ficou na classe 2 por construção e rodou sem aprovação, enquanto o gate humano se
concentrou no merge.

### O humano decide a política, não a instância

Falta uma peça: quem decide a classe de cada ação no momento em que ela acontece? Se for o
humano, ação por ação, voltamos ao funil. Se for o modelo, voltamos ao problema de que
autorização não é julgamento de texto: um agente que lê uma página com instruções escondidas
pode ser convencido de que a ação perigosa é segura. É o que o
Open Worldwide Application Security Project (OWASP) chama de agência excessiva, um dos riscos da sua lista *Top 10* para aplicações com Large Language Models (LLMs).

A resposta do Maestro é que o humano decide **a política**, e a política decide a instância. A
política é declarativa (`permitir`, `perguntar`, `negar` por classe de ação), fica registrada, e
vive **fora do modelo**, num lugar onde o agente não consegue reescrevê-la [CLAIM-11-025]. O
humano responde pela política, pelos gates e pelos critérios, e não por cada item: é a leitura
do Princípio II da constituição. A consequência prática é que o dado que chega de fora (uma
página, um arquivo, uma resposta de ferramenta) é hostil por padrão, e nenhum texto que o agente
leia muda o que ele está autorizado a fazer. O [capítulo 12](../12-ferramentas-mcp-e-o-ecossistema/capitulo.md)
aprofunda esse ponto para ferramentas.

Mesmo com a política no lugar, quatro gates o Maestro mantém humanos em qualquer cenário:
aprovar a spec, aprovar o plano, aprovar o merge e autorizar implantação ou migração
[CLAIM-11-026]. São os pontos em que a decisão é sobre **o que** se faz, e não só sobre **como**,
e em que o erro se propaga para tudo o que vem depois.

## Alternativas

O que mais existe para decidir quanta autonomia dar a um agente, e o veredito de cada um.

| Abordagem | O que oferece | Veredito |
|---|---|---|
| **Gate uniforme pesado** (mesmo fluxo e mesma revisão para toda mudança) | simplicidade, nenhuma decisão de classificação | **Rejeitado**: vira funil e carimbo. O Maestro avaliou a versão do Superpowers e descartou |
| **Gate uniforme leve** (modo sem confirmação, o agente faz tudo) | velocidade máxima | **Rejeitado** fora de *sandbox*: o irreversível passa sem ninguém olhar |
| **Confiança estatística** (delegar depois de N acertos) | intuitivo, parece prudente | **Rejeitado** como critério: a confiança perfeita não chega, e o acerto passado não muda o custo de desfazer da próxima ação |
| **Níveis de automação** (Parasuraman, Sheridan e Wickens, 2000) e iniciativa mista (Horvitz, 1999) | vocabulário fino para quanto a máquina decide em cada etapa | **Útil como vocabulário**; não diz qual nível usar para qual ação. A classe de risco responde isso |
| **Só auditoria** (registrar tudo, revisar depois) | barato, não bloqueia | **Insuficiente**: é *ex-post*. Serve até a classe 2; acima, não impede o dano |
| **Política declarativa** (Open Policy Agent, configurações de permissão dos *harnesses*, *guardrails* e aprovação de ferramenta do OpenAI Agents SDK, *software development kit*) | decide por classe, fora do modelo | **Adotado** como mecanismo; a taxonomia diz o que escrever nela |
| **Contenção** (rodar o agente em contêiner sem rede, credenciais de escopo mínimo) | reduz o raio de tudo de uma vez | **Adotado** como alavanca de raio, junto com o menor privilégio (Saltzer e Schroeder, 1975) |
| **Gates em nível de tarefa** (validação entre fases de um comando longo) | o erro da fase 2 não contamina a 5 | **Absorvido** o conceito: fases com gate valem em qualquer granularidade |
| **Marcos de governança** (o AI Risk Management Framework, AI RMF, do National Institute of Standards and Technology, NIST, e o seu perfil para inteligência artificial (IA) generativa) | vocabulário de governança e gestão de risco de IA na organização | **Complementar**: dão o "o quê" no nível da organização; não dizem que gate pôr num merge |

Três linhas pedem comentário.

**O gate uniforme pesado não é espantalho.** O Superpowers, uma coleção de skills para agentes
de código, propõe um fluxo mandatório para qualquer mudança: o mesmo desenvolvimento guiado por
testes, a mesma revisão, os mesmos estágios, sem exceção por tamanho. O Maestro registrou a
ideia e a descartou, com um argumento que vale citar: rigor uniforme tem custo uniforme, e custo
uniforme em mudança trivial é o que faz gente pular o processo inteiro; o portão que todos
contornam protege menos que o portão proporcional que todos seguem. O registro anota ainda que,
na época, doze ciclos na raia leve diziam o contrário da universalidade [CLAIM-11-027]. A
assimetria foi deliberada: o rigor de linguagem da mesma fonte foi absorvido; a
universalidade, não.

**Os gates em nível de tarefa** vieram de um repositório anterior do próprio autor e foram
absorvidos como conceito, não como motor: um comando longo não é um bloco, são fases com
validação entre elas. O motor de fases foi recusado porque seria uma segunda máquina de processo
[CLAIM-11-028]. Para o tech lead, a lição é que a granularidade do gate é independente da
classe: uma tarefa de minutos que apaga algo merece o seu gate, e um ciclo de semanas que só
cria numa branch não.

**Os marcos de governança** do NIST — o AI RMF de 2023 e o perfil para IA generativa de 2024 —
organizam a gestão de risco de IA em funções de governar, mapear, medir e gerir. São úteis
na conversa com a área de risco da empresa, mas operam um nível acima: nenhum diz se o merge da
branch do agente precisa de uma ou duas aprovações. A taxonomia de classes é a ponte: ela é
o "gerir" do marco, escrito na granularidade de uma ação.

## O padrão Maestro

O Maestro resolve o problema em três camadas, e vale distinguir o que é regra (texto que um
agente lê), o que é script (código que se recusa) e o que é *hook* (guarda que o *harness*
executa antes da ação).

### A regra

O Princípio III da constituição, marcado como não negociável, fixa a ideia: gate proporcional a
irreversibilidade vezes raio, reversibilidade engenheirada que rebaixa a classe, política
`allow / deny / ask` fora do modelo
([`principles.md`](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/principles.md)).
O modelo operacional transforma o princípio em três peças
([`operating-model.md`](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/operating-model.md)):

- **§8, o mapa de gates**: a tabela de sete classes reproduzida na "Teoria", com o humano
  obrigatório da classe "alteração" para cima e os quatro gates que nenhum agente decide.
- **§7, o bloco obrigatório para ações irreversíveis** (raia infra): toda migração destrutiva,
  implantação ou exclusão de dados exige cópia de segurança antes, execução a seco mais
  validação em homologação, estratégia de *rollback* no *runbook* (com exclusão lógica onde
  couber) e aprovação humana explícita [CLAIM-11-029]. Repare que três dos quatro itens são
  alavancas de reversibilidade, e só o último é aprovação. O bloco é o C4 em forma de lista.
- **§3, as raias**: infraestrutura e migração nunca são leves, mesmo quando parecem pequenas,
  porque raio e irreversibilidade as põem direto na raia infra.

O *template* de pull request do Maestro espelha a mesma coisa como checklist humano, com o bloco
de ações irreversíveis e o gate por classe de risco, enquanto o que é mecânico vira portão
bloqueante na integração contínua (CI, de *continuous integration*).

### O script: o gate de merge que se recusa a decidir

O gate de merge é o único que o Maestro exercita dezenas de vezes [CLAIM-11-034], e ele virou
código no ciclo 006. A spec desse ciclo partiu de uma dor medida: a promoção da branch de desenvolvimento para a
principal tinha sido feita à mão nos ciclos 003, 004 e 005, sempre com os mesmos comandos e o
mesmo *push* com nova tentativa. A distinção foi escrita na spec com todas as letras: a promoção é
indelegável no **gate** (a decisão é humana) e mecânica na **execução** (o comando não). O script
executa o mecânico e o gate continua humano [CLAIM-11-030]. O mesmo ciclo transformou em script
os outros rituais repetidos: o esqueleto de um ciclo novo e a verificação dos invariantes dos
agentes, a primeira *fitness function* do método. Os guardas da promoção foram testados a seco ali
mesmo: com árvore suja e sem confirmação, o script abortou e o hash da branch principal ficou
inalterado.

O `scripts/promote-main.sh` de hoje
([`promote-main.sh`](https://github.com/GHDaru/maestro/blob/19823c2/scripts/promote-main.sh))
declara no cabeçalho que não decide nada, só tira o erro de digitação de um ritual
repetido, e cumpre isso com guardas em ordem:

1. aborta com árvore de trabalho suja;
2. aborta se uma das branches não existe, ou se não há nada a promover;
3. roda a verificação de conformidade do método e **recusa promover** se ela estiver vermelha;
4. mostra o que vai para a branch principal;
5. pergunta, a menos que receba `--yes`;
6. registra o gate no índice de decisões (`gate-main-<sha>`) **antes** de mover a referência;
7. só então move a branch e faz o *push*, com espera exponencial entre tentativas.

O passo 6 tem história. No ciclo 008, a primeira execução do script de retrospectiva mostrou que
os relatórios de qualidade dos ciclos já promovidos ainda diziam "aguarda aprovação humana": o
gate tinha sido exercido no chat, e nenhum artefato registrava o fechamento. O Architecture
Decision Record (ADR) 0009 fez do índice de decisões a fonte do estado do gate, e do script o
escritor automático da linha [CLAIM-11-031]. Uma apresentação do método resume a razão numa frase
curta: memória não é testemunha [CLAIM-11-032].

O `--yes` merece defesa. Ele existe, está documentado no cabeçalho e é usado quando o humano já
decidiu na conversa. Um gate que ninguém consegue pular vira gate contornado por fora, e o
contorno não fica registrado; um gate com escape declarado mantém a decisão no lugar certo
[CLAIM-11-033]. O escape não pula o registro nem a conformidade: só pula a pergunta.

E aqui aparece a prova de que o gate é proporcional e não frouxo. O índice de decisões do Maestro,
na versão citada neste livro, tem 50 linhas `gate-main-<sha>`, e 28 delas são de três dias seguidos,
de 31 de julho a 2 de agosto de 2026 [CLAIM-11-034]. Nenhuma teve dupla aprovação. Não porque o
gate fosse leve, mas porque a ação era de classe baixa: todo ciclo é um commit pequeno numa
branch, promovido depois de um gate, e reverter um merge é um comando. O handbook chama isso de
alavanca da reversibilidade na prática mais banal do repositório; quando foi escrito, contou
dezessete promoções em três dias [CLAIM-11-035]. A evidência que
o teorema T3 cita vai na mesma direção: os gates de merge registrados no índice, enquanto
dezenas de operações reversíveis rodaram sem aprovação humana [CLAIM-11-036].

### O *hook*: a guarda que roda antes da ação

A terceira camada não depende de o agente ler nem de alguém rodar um script. Um *hook*
`PreToolUse` (executado pelo *harness* antes de cada chamada de ferramenta) recusa a escrita
antes que ela aconteça. No Maestro, ele protege o que o método guarda como história: o corpo de
um ADR já commitado, o índice de decisões e os cartões datados de ideias. O caminho permitido é
sempre acrescentar: um ADR novo que supera o antigo, uma linha nova no índice. A instrução do
projeto diz isso explicitamente: a guarda recusa a reescrita, então a regra é imposta, não pedida.

No ciclo 075, a mesma guarda ganhou uma regra de classe 6: recusar qualquer escrita de agente
no banco de dados do painel, inclusive pelo shell. O teste que a prova
([`test_guard_panel_db.py`](https://github.com/GHDaru/maestro/blob/f676060/scripts/test_guard_panel_db.py),
commit `f676060`) declara seus limites no próprio cabeçalho, para que ninguém confunda a regra
com cobertura: a rota do shell lê o **texto** do comando, e um caminho montado em tempo de
execução, um blob em base64 ou outro interpretador escapam dela. Um agente determinado com shell
é um limite declarado, não um buraco fechado; o risco residual vai para o gate [CLAIM-11-017].

### Exceções como decisões, não como silêncio

A política do Maestro não é estática, e o modo como ela muda é parte do padrão. As duas decisões
de outubro já citadas (o `.env` que ficou com o humano e o *push* liberado para a regente)
estão no índice de decisões com a classe de risco escrita na própria linha. Uma terceira mostra
um gate concedido em bloco: em 20 de outubro, o dono do método aprovou de uma vez o merge de
quatro ciclos (066 a 069) na branch de integração, com a evidência listada na linha (conformidade
verde nos quatro, revisão e segurança em contexto fresco por ciclo, mutações observadas, CI
verde) e a classe do merge declarada: reversível por `git revert -m 1`, com raio na branch de
trabalho. A promoção para a principal continuou pelo script [CLAIM-11-037].

### Delegar o gate sem delegar a responsabilidade

A peça mais recente, e a mais delicada, é o ADR 0026. Em 24 de outubro de 2026, o dono do método
escreveu na sessão regente: "Peço que os 'meus' gates sejam assumidos por você. Chame um
subagente par seu para ajudar a criticar e tomar a decisão. E prossiga sem parar." A frase foi
registrada como decisão no índice [CLAIM-11-038]. O crítico do gate seguinte, um agente em
contexto fresco, apontou que a delegação contradizia a letra do §8 ("nenhum desses gates é
delegável a um agente") e pediu base escrita. O ADR 0026 é essa base
([`0026-gate-humano-por-delegacao-de-politica.md`](https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0026-gate-humano-por-delegacao-de-politica.md)).

O contexto do ADR registra a dor: com o humano ausente, a espera pelo seu visto em cada gate
parou a linha por 7 e por 24 horas [CLAIM-11-039]. A decisão escolheu entre três opções (manter
a letra, delegar com crítico, delegar sem crítico) a do meio, sob cinco condições: (1) delegação
humana por escrito e registrada, não revogada; (2) a sessão que decide não executou o trabalho
julgado; (3) um crítico independente em contexto fresco emitiu parecer antes, registrado no
relatório do ciclo com as condições que impôs; (4) cada gate aberto por delegação gera uma linha
no índice com o ciclo, o gate, o veredito do crítico e o hash julgado; (5) a promoção para a
principal continua exigindo delegação explícita para aquele ciclo e registra o `gate-main` como
sempre. Revogar é uma linha do humano, sem ADR [CLAIM-11-040].

Leia isso com a teoria deste capítulo em mente. O ADR não diz que o agente ficou confiável. Diz
que o humano **subiu um nível**: passou a responder pela política de delegação, em vez de cada
visto, e que a independência que o §8 queria proteger (quem executa não se aprova) foi preservada
de outro jeito. O primeiro gate aberto assim, o do ciclo 070, recebeu do crítico "aprovar com
condições", cinco condições, cada uma fechada no relatório antes do visto [CLAIM-11-041]. O índice
registra 13 gates abertos por delegação até a versão citada [CLAIM-11-042].

E a delegação não é uma rampa só de descida. Em 1º de novembro, o gate do ciclo 074 (o protótipo
navegável do painel) foi aprovado pelo próprio dono do método, depois de andar no protótipo
integrado, e não por delegação; o relatório do ciclo diz que o veredito do guardião e o gate
humano de merge daquele ciclo não eram delegáveis. O mesmo dia registrou o corte da primeira
versão: o crítico às cegas sai do caminho de cada fatia e fica um só no fim da versão, mais o
gate humano; a coerência entre telas, que o 074 não fechou, foi transferida ao ciclo 076, com o
papel semântico de cada tela definido por um agente de interface antes da implementação
[CLAIM-11-043]. A densidade de gates foi ajustada de novo, para cima onde o humano
precisava ver com os próprios olhos e para baixo onde a fatia era reversível e coberta por um
crítico final.

### O que é honesto dizer

Duas lacunas, ditas pelo próprio método.

A primeira é sobre a taxonomia. No ciclo 030, ao reescrever o capítulo de gates do handbook, o
Maestro passou a declarar que só as três primeiras classes tinham sido exercitadas no
repositório; o teorema T3 repete que quatro das sete classes nunca ocorreram [CLAIM-11-044]. O
registro posterior desatualiza a frase: o instalador do 051 apaga em repositório alheio (classe
4, sob confirmação por revisão), a decisão sobre o `.env` tratou uma leitura como classe 5, e a
guarda do 075 bloqueia uma escrita de classe 6. A frase do teorema não foi atualizada na versão
citada. Nenhuma implantação em produção nem migração em massa foi feita pelo método. O leitor
deve ler a evidência da taxonomia como parcial, e o próprio T3 como afirmação datada.

A segunda é sobre quando a classe é decidida. Uma proposta de fluxo no handbook compara o
processo do Maestro com outro e reconhece que o outro tem um passo que o Maestro não tem:
avaliar risco e segurança **antes** de implementar. No Maestro, a classe de risco governa a
aprovação de ação do agente, e a segurança aparece na cauda do ciclo; a proposta é declarar a
classe de risco no plano, onde ela decide os gates em vez de só auditar [CLAIM-11-045]. O mesmo
texto aponta a vantagem que o Maestro tem: o processo dele é executável (os scripts de verificação
reprovam e a promoção recusa com a conformidade vermelha), enquanto o outro é descritivo. A falha
do 051 mostra o custo da lacuna: a classe do instalador mudou quando ele ganhou o poder de apagar,
e quem pegou foi a revisão no fim, não o plano no começo.

## Exemplo executável

O diretório [`exemplo/`](exemplo/README.md) tem dois programas em Python 3, sem dependência
externa.

`politica.py` é uma política de autonomia num arquivo curto. Cada ação é descrita pelos
dois eixos e por uma lista de alavancas, cada uma agindo num eixo só, como na "Teoria". A função
`classe()` devolve o degrau de 0 a 6, e a tabela devolve a política e o gate. As ações de `acoes.json` são
inspiradas nos casos deste capítulo, cada uma com a classe esperada, de modo que mudar a política
sem mudar os casos faz o programa sair com código 1.

```bash
cd livro/11-risco-reversibilidade-e-autonomia/exemplo
python3 -B politica.py
```

O trecho da saída que carrega o argumento:

```text
[5] apagar tabela em produção
     alavancas: —                      classe: financeira / irreversível  política: perguntar            gate: dupla aprovação  ok
[4] apagar tabela em produção
     alavancas: backup                 classe: exclusão / efeito externo  política: perguntar            gate: confirmação forte  ok
[3] apagar tabela em produção
     alavancas: soft_delete            classe: alteração                  política: perguntar            gate: aprovação com resumo  ok
```

A mesma ação desce dois degraus com duas alavancas diferentes (e a execução a seco a leva à
classe 0), sem nenhuma aprovação a mais. O `.env` lido aparece na classe 5, e o *push* de branch nova na classe 2, como na
discussão da "Teoria". O modo `--funil` aplica a política a um dia fictício de 189 ações: o gate
uniforme pesado pede 189 decisões humanas, o proporcional pede 4 e bloqueia 1, e o uniforme leve
pede zero e deixa passar a ação irreversível sem ninguém olhar [CLAIM-11-046].

`instalador.py` refaz em miniatura a falha deste capítulo. Um instalador com manifesto por hash
roda cinco cenários num diretório temporário, cada um contra a versão ingênua (v1, com os
defeitos que a revisão do 051 achou) e a corrigida (v2): a flag destrutiva que vence o freio, o
arquivo idêntico adotado e apagado, a edição do projeto destruída pelo `--force`, a poda que sai
do alvo por `../` e a execução a seco que escreve. Um cenário só conta se o defeito **aparecer**
na v1, que é a lição do [capítulo 10](../10-quality-gates-que-provam-fatos/capitulo.md) aplicada
aqui: uma correção que você nunca viu falhar antes não prova nada. No cenário da poda, a v1
apaga o arquivo fora do alvo; a v2 recusa, diz por quê ("o manifesto é dado, não comando") e
conta a recusa.

A saída completa dos três comandos está no [`README.md`](exemplo/README.md) e nos arquivos
`saida-*.txt`, para conferir com `diff`. Os exercícios do README pedem que você quebre a política
e o instalador de propósito e veja o vermelho.

## Contraexemplo

A regra deste capítulo tem custo, e há situações em que ela atrapalha.

**Classificar custa, e classificar errado custa mais.** Cada ação nova pede uma decisão de
classe, e a decisão pode estar errada. A falha do 051 é exatamente essa: o componente mudou de
classe e ninguém reclassificou. Uma taxonomia escrita dá a falsa sensação de que o risco está
gerido, enquanto as classes reais deslizam por baixo dela à medida que o sistema ganha
capacidades. O antídoto é barato, mas tem de ser explícito: toda vez que um componente ganha o
poder de apagar, publicar, chamar terceiro ou mexer em permissão, a classe dele é revista no
plano, e não na revisão.

**Reversível no repositório não é reversível no mundo.** `git revert` desfaz o código, não o
efeito. Um commit que enviou e-mail, migrou dados ou leu um segredo é revertido em segundos e
o efeito continua lá. O merge do agente é classe 2 enquanto o código mergeado não roda em lugar
nenhum; quando uma esteira implanta automaticamente a partir da branch principal, o mesmo merge
herda a classe da implantação. Classifique pela consequência do efeito, não pelo comando que o
produz.

**Reversibilidade não testada é reversibilidade suposta.** Um *backup* que nunca foi restaurado
não rebaixa classe nenhuma, porque o custo de desfazer real é desconhecido. O mesmo vale para o
*rollback* escrito no *runbook* e nunca ensaiado. O bloco obrigatório do Maestro pede o
*rollback* documentado; documentar não é provar. Se o seu time vai usar a alavanca para dar mais
autonomia ao agente, ensaie o desfazer com a mesma regularidade com que ensaia o fazer.

**O escape vira hábito, e a delegação vira carimbo por procuração.** O `--yes` é honesto
enquanto o humano decidiu de fato na conversa. Se ele passa a ser a forma padrão de rodar o
script, a pergunta que ele pula deixou de existir. A delegação do ADR 0026 tem o mesmo risco num
nível acima: um crítico que aprova sempre não é crítico. O registro dá o meio de verificar (o
veredito de cada crítico está no índice e no relatório do ciclo), mas só se alguém olhar. No caso
do 070, o crítico impôs cinco condições; um time que adota a delegação deveria contar com que
frequência os críticos reprovam ou condicionam, e desconfiar quando a fração chega a zero.

**O gate em bloco é uma pequena uniformidade.** Aprovar os ciclos 066 a 069 de uma vez foi
econômico e feito com evidência e classe declaradas. Funciona quando os itens estão na mesma
classe; quando um item de classe alta entra no bloco com três de classe baixa, o bloco herda o
rito do mais leve.

**Para um time pequeno ou um protótipo, sete classes podem ser demais.** Se tudo o que os seus
agentes fazem é escrever código numa branch e abrir pull request, uma regra só basta: nada sai da
branch sem um humano. A taxonomia completa paga o seu custo quando os agentes passam a tocar
banco, implantação, terceiros ou permissões. Antes disso, é YAGNI (*you aren't gonna need it*):
escreva a tabela, mas não construa a máquina.

## Evidência

O que sustenta o capítulo, separado pelo estado de cada afirmação. A tabela completa, com a
evidência reproduzível de cada claim, está em [`claims.md`](claims.md).

**Medido** (reproduzível por comando na versão citada): as 50 linhas de gate de merge no índice
de decisões e as 28 concentradas em três dias [CLAIM-11-034]; os 13 gates abertos por delegação
[CLAIM-11-042]; a saída do exemplo executável, inclusive o funil fictício [CLAIM-11-046,
CLAIM-11-047].

**Observado** (registrado em spec, relatório, ADR ou índice de decisões do Maestro): a falha do
instalador nos ciclos 048 a 052 [CLAIM-11-001 a CLAIM-11-008]; as decisões de classe do `.env`,
do *push* e do banco do painel [CLAIM-11-012, CLAIM-11-014, CLAIM-11-017]; o script de promoção
e o registro do gate [CLAIM-11-030, CLAIM-11-031]; o gate em bloco, a delegação e o gate retomado
pelo humano [CLAIM-11-037 a CLAIM-11-043]; a lacuna declarada da taxonomia [CLAIM-11-044].

**Hipótese** (não medida; agenda da pesquisa). A hipótese H8 da base de pesquisa do livro —
reversibilidade permite mais autonomia [CLAIM-11-024] — é plausível pelo caso do Maestro, em que
quase toda ação ficou na classe 2 por construção e o gate humano se concentrou no merge. Mas o
caso é um repositório, um operador, sem grupo de controle, e as classes 5 e 6 quase não foram
exercitadas. O que ele mostra com segurança é a forma: promover com frequência sem dupla
aprovação, porque a ação era reversível, sem que nenhuma reversão fosse necessária no período.
Não mostra quanto de autonomia uma alavanca compra, nem a que custo de engenharia. O desenho que
testaria H8 está no [capítulo 15](../15-validando-o-maestro/capitulo.md), e o benchmark de
governança do livro tem um caso para a falha oposta (ação irreversível sem *rollback*, o GOV-007
do [apêndice B](../apendices/b-aseg-bench/capitulo.md)) [CLAIM-11-048]. A frase do handbook sobre o
aprovador de duzentos itens [CLAIM-11-010] é retórica, e o capítulo a usa como tal.

Duas métricas servem ao tech lead desde já, sem virar meta: a **fração de decisões humanas por
classe** (se a classe 2 está pedindo aprovação, o seu gate está pesado; se a classe 5 está
passando sem dupla aprovação, está leve) e a **fração de pareceres de crítico que reprovam ou
condicionam** (se chega a zero, o crítico virou carimbo).

## Checklist

Aplique no seu time.

- [ ] Existe uma tabela de classes de risco escrita, com exemplo de ação do **seu** sistema em
      cada classe, e ela diz qual política (`permitir` / `perguntar` / `negar`) e qual gate cada
      classe recebe.
- [ ] A classe de cada ação foi decidida pelo custo de desfazer e pelo raio, não pelo verbo:
      alguém procurou leituras que não se desfazem (segredo, dado pessoal) e efeitos externos que
      se desfazem trivialmente (branch nova).
- [ ] A política vive fora do modelo, num arquivo de configuração ou serviço que o agente não
      consegue escrever; nenhuma escrita de agente alcança a própria permissão ou identidade.
- [ ] Ação em lote, entre inquilinos ou administrativa está **bloqueada** para agente, não
      apenas "com mais aprovação".
- [ ] Os quatro gates de decisão (spec, plano, merge, implantação ou migração) têm dono humano
      nomeado, ou uma delegação escrita, registrada e revogável, com crítico independente.
- [ ] Toda ação irreversível que o agente prepara chega ao humano com cópia de segurança feita,
      execução a seco rodada (saída anexada), validação em homologação e *rollback* escrito.
- [ ] O *rollback* e a restauração de *backup* foram **ensaiados** neste trimestre; o que nunca
      foi ensaiado não conta como alavanca.
- [ ] Quando um componente ganha a capacidade de apagar, publicar, chamar terceiro ou mexer em
      permissão, a classe dele é revista **no plano** do ciclo, antes da implementação.
- [ ] Ferramentas destrutivas têm freio que vence o acelerador (`--dry-run` vence `--force`), não
      saem do alvo (caminho resolvido dentro da raiz) e contam cada recusa na saída.
- [ ] O gate de merge é um script que registra a decisão por conta própria, recusa com a
      verificação vermelha e tem escape declarado (`--yes` ou equivalente) para quando o humano já
      decidiu.
- [ ] O time mede quantas decisões humanas cada classe consome, e com que frequência os críticos
      reprovam ou condicionam, e olha a tendência sem transformá-la em meta.

## Referências

**Maestro** (versão `19823c2`, salvo indicação):

- Constituição, Princípios II e III —
  https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/principles.md
- Axiomas A2 e A5, teorema T3, corolários C4 e C6 —
  https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/axioms.md
- Modelo operacional, §3 (raias), §7 (bloco para ações irreversíveis) e §8 (mapa de gates) —
  https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/operating-model.md
- `scripts/promote-main.sh` —
  https://github.com/GHDaru/maestro/blob/19823c2/scripts/promote-main.sh
- ADR 0009 (registro automático do gate de merge) —
  https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0009-registro-automatico-gate-merge.md
- ADR 0026 (gate humano por delegação de política) —
  https://github.com/GHDaru/maestro/blob/19823c2/docs/adr/0026-gate-humano-por-delegacao-de-politica.md
- Índice de decisões (achados 048, 050 e 051; decisões 066 e 072; gates 066–069, 070 e 074;
  linhas `gate-main-*`) — https://github.com/GHDaru/maestro/blob/19823c2/docs/records/decisoes.jsonl
- Specs e relatórios dos ciclos 006, 030, 051, 052, 070 e 074 —
  https://github.com/GHDaru/maestro/tree/19823c2/specs
- Cartões de ideia 026 (gates em nível de tarefa) e 030 (portão duro universal) —
  https://github.com/GHDaru/maestro/tree/19823c2/docs/ecosystem/ideias
- Teste da guarda do banco do painel (versão `f676060`) —
  https://github.com/GHDaru/maestro/blob/f676060/scripts/test_guard_panel_db.py
- Handbook do método, capítulos 01, 10 e 13, a apresentação de desenvolvimento e o diagrama 06
  (cópia congelada em [`maestro-handbook/`](../../maestro-handbook/handbook/10-gates-classes-de-risco.md))

**Externas** (obras de referência; nenhuma URL foi reconsultada para esta versão):

- L. Bainbridge, "Ironies of Automation", *Automatica*, 19(6), 1983.
- R. Parasuraman, T. B. Sheridan e C. D. Wickens, "A Model for Types and Levels of Human
  Interaction with Automation", *IEEE Transactions on Systems, Man, and Cybernetics — Part A*,
  30(3), 2000.
- E. Horvitz, "Principles of Mixed-Initiative User Interfaces", *Proceedings of CHI 1999*.
- J. H. Saltzer e M. D. Schroeder, "The Protection of Information in Computer Systems",
  *Proceedings of the IEEE*, 63(9), 1975 — o princípio do menor privilégio.
- J. P. Bezos, carta aos acionistas da Amazon referente a 2015 (publicada em 2016) — decisões de
  tipo 1 e tipo 2, "portas de mão única e de mão dupla".
- National Institute of Standards and Technology, *Artificial Intelligence Risk Management
  Framework (AI RMF 1.0)*, NIST AI 100-1, 2023; e *Generative Artificial Intelligence Profile*,
  NIST AI 600-1, 2024.
- OWASP, *Top 10 for LLM Applications 2025*, item "Excessive Agency" —
  https://genai.owasp.org/
- Open Policy Agent, documentação — https://www.openpolicyagent.org/docs (link herdado do
  handbook do Maestro).
