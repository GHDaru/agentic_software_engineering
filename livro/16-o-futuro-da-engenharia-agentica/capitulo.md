# 16 — O futuro da engenharia agêntica

> Observar sem gatilho é esquecer com cerimônia. — tradução nossa da mensagem de erro de um
> portão do Maestro, que no original diz "observing without a trigger is forgetting with
> ceremony" [CLAIM-16-001]

Todo livro sobre agentes de inteligência artificial (IA) envelhece no dia em que sai: o modelo
da próxima geração lê mais, erra menos e custa menos, e metade das recomendações parece, de
repente, prudência exagerada. Este capítulo não tenta adivinhar o próximo modelo. Faz uma
pergunta mais útil para quem precisa decidir segunda-feira: das regras dos quinze capítulos
anteriores, quais dependem de uma limitação da ferramenta de hoje e quais dependem de coisas
que nenhum modelo muda — pessoas, consequências e custo de desfazer? E, para as que dependem da
ferramenta, como o seu time percebe a hora de revê-las sem esperar que alguém se lembre?

## Pergunta central

O que deste livro sobrevive à próxima geração de modelos, e como o time descobre, com data e
evidência, a hora de mudar o resto?

## Resultado de aprendizagem

Ao final, você consegue:

1. **Classificar** cada regra do seu processo pela premissa de que ela deriva — sobre pessoas,
   sobre consequência, sobre custo de desfazer ou sobre a ferramenta — e dizer quais caem se um
   modelo novo remover a limitação de que dependem.
2. **Escrever um gatilho de reavaliação** que um script consegue conferir contra eventos reais,
   em vez de um "observar" que só a memória de alguém vigia.
3. **Ler um calendário regulatório escalonado**, como o do Regulamento Europeu de Inteligência
   Artificial (*AI Act*), separando o que já se aplica, o que foi adiado, o que mudou de
   conteúdo, e dizendo o que o time faz em cada marco.
4. **Decidir entre comprar uma plataforma de agentes, adotar um protocolo ou construir**, pelo
   critério de reversibilidade, e registrar a decisão com a condição que a reabriria.
5. **Montar a vigília do futuro** do seu time: um catálogo do que foi visto e não adotado, com
   gatilho, portão e cadência que não dependem de lembrança.

## A falha real

Em 10 de agosto de 2026, o ciclo 047 do Maestro deu ao método um lugar para o futuro. Até ali,
o que o projeto via no ecossistema — ferramentas, repositórios, ideias de outros times — ficava
espalhado em notas e capítulos. O ciclo criou um catálogo em que a unidade é a **ideia**, cada
uma com um cartão datado e imutável e com o seu estado corrente num índice que só cresce
(`docs/ecosystem/estado.jsonl`). Quatro vereditos são possíveis: absorver, adotar, descartar e
observar. E um portão novo, `scripts/check-ecosystem.sh`, passou a recusar o veredito mais
cômodo dos quatro quando vinha sozinho: uma ideia em "observar" sem gatilho de reavaliação
reprova o portão com a frase da epígrafe, escrita em inglês no script [CLAIM-16-001].

Era uma boa regra. Ela transforma o "vamos ficar de olho" — a frase com que todo time adia uma
decisão e a esquece — num compromisso com condição escrita. Em 1º de novembro de 2026, na versão
`19823c2` que este livro estuda, o catálogo tinha 41 ideias com estado corrente: 14 absorvidas,
uma adotada, dez descartadas e 16 em observação, todas as 16 com gatilho [CLAIM-16-002]. O
portão estava verde.

Duas dessas dezesseis mostram o defeito. A ideia 029, "trilha de auditoria com custo por
invocação", foi observada em 31 de julho com o gatilho "alguém precisar responder 'quanto custou
este ciclo?' com número, e não com estimativa". Em 12 de outubro o humano que rege o projeto
abriu o ciclo 065 pedindo justamente isso — "Quero ver quanto estou gastando" —, e o ciclo construiu o livro de ponto que mede tokens e dinheiro por
tarefa — a história está no [capítulo 13](../13-observabilidade-e-economia/capitulo.md). A ideia
003, "*worktree* git isolado por task", foi reclassificada para observação em 10 de agosto com
o gatilho "dois ou mais agentes escrevendo no mesmo repositório ao mesmo tempo, com conflito
observado". Em 20 de outubro o ciclo 066 entregou um lançador de sessões por modelo e por
*worktree* (commit `d5feef2`); em 25 de outubro o ciclo 072 integrou a *worktree* de um
trabalhador escrevendo "conflitos resolvidos mantendo ambas as evidências" na própria mensagem
do commit `d71cee6` [CLAIM-16-003].

O da 029 disparou pela letra do próprio gatilho. O da 003 disparou numa leitura deste livro,
que um mantenedor pode contestar: o conflito registrado é de integração de *worktree*, e não
de dois agentes escrevendo ao mesmo tempo (a objeção é discutida em "Evidência"). Em qualquer
das leituras, nenhuma das duas ideias foi reavaliada. Em `19823c2`, o estado
corrente de ambas continua "observar", com as datas de julho e agosto [CLAIM-16-004]. E não foi
por abandono do catálogo: em 29 de outubro, quatro dias depois do conflito entre *worktrees*, o
índice ganhou uma linha nova — a da ideia 041, o diagrama vivo do time — no commit `f79b1be`, a
única linha acrescentada naquele commit [CLAIM-16-005]. Alguém abriu o arquivo, escreveu nele,
e não releu os gatilhos das linhas de cima.

O portão estava verde porque media a coisa errada. A linha 255 de `check-ecosystem.sh` confere
que todo "observar" **tem** gatilho; nada confere se o gatilho **disparou** [CLAIM-16-006]. É o
anti-padrão que o [capítulo 10](../10-quality-gates-que-provam-fatos/capitulo.md) chama de
"o check mede o proxy, e não o fato": o fato desejado era "o método percebe quando o mundo
muda"; o proxy medido foi "o método escreveu a condição". O resultado é que o mecanismo que o
projeto montou para lidar com o futuro funcionava exatamente como a memória de um humano
ocupado — lembrava quando lembrava.

A falha importa para este capítulo por um motivo simples: ela não é sobre o próximo modelo. É
sobre como um time percebe que o próximo modelo chegou. Toda a discussão sobre o que sobrevive
às gerações de IA é inútil se a revisão das regras depender de alguém notar.

## Teoria

### De onde as regras vêm, e por que isso decide o que envelhece

Uma regra de processo não envelhece por ser antiga. Envelhece quando a premissa de que ela
deriva deixa de ser verdade. Por isso a pergunta "o que sobrevive à próxima geração de
modelos?" não se responde olhando as regras uma a uma; responde-se olhando as premissas.

O Maestro escreveu as suas. O documento de axiomas
([`docs/governance/axioms.md`](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/axioms.md))
assume cinco verdades sem prová-las, deriva delas sete teoremas — cada um com evidência no
próprio repositório — e treze corolários, que são de onde saem as regras do dia a dia
[CLAIM-16-007]. A estrutura existe para um uso declarado: quando alguém propõe uma regra nova,
a primeira pergunta é de qual axioma ela deriva; a que não deriva de nenhum "é um axioma novo
ou é cerimônia". Este capítulo usa a mesma estrutura para a pergunta inversa: se um axioma
deixar de valer, quais regras perdem o chão?

Leia os cinco com essa pergunta em mente:

| Axioma | Enunciado (resumo) | Sobre o quê |
|---|---|---|
| A1 | A intenção é humana: o agente propõe, escreve e verifica, mas não *quer* | pessoas |
| A2 | Consequência precisa de dono: quem não tem nada a perder não responde | pessoas e consequência |
| A3 | O contexto é finito e degrada ao encher | a ferramenta |
| A4 | O que está escrito é o que sobrevive: o agente começa cada sessão do zero | a ferramenta (e a organização) |
| A5 | O custo é assimétrico entre fazer e desfazer | o mundo |

Três deles não falam de modelo nenhum. A1 e A2 falam de quem quer e de quem responde; A5 fala
de apagar dados, migrar banco e publicar, que custam o mesmo com o melhor modelo do mundo. Um
modelo dez vezes mais capaz produz mais rápido — e, pelo próprio A5, torna o desfazer
relativamente **mais** caro, não menos. O próprio texto de A2 já antecipa a objeção: a
responsabilidade não se transfere ao agente "não por falta de capacidade, mas por falta de
exposição". Capacidade é exatamente o que a próxima geração traz; exposição, não.

Os outros dois são diferentes. A3 se declara, nas palavras do documento, "uma propriedade
física da ferramenta, não um hábito do operador". A4 é metade ferramenta: "o agente começa cada
sessão do zero" descreve o *harness* de hoje, e o catálogo do Maestro já tem, em observação
desde 1º de agosto de 2026, a ideia 017, memória persistente de sessão, com o gatilho "sessões de vários dias sobre a
mesma intenção começarem a doer, com perda de contexto medida" [CLAIM-16-008]. Janelas de
contexto maiores e memória entre sessões são justamente as duas frentes em que os fornecedores
de modelos e de *harness* mais investem. Se uma delas avançar o bastante, o axioma não fica
falso de um dia para o outro: fica **menos verdadeiro**, e as regras que dependem dele passam
a custar mais do que protegem.

### O mapa da fragilidade

Os teoremas dizem de quais axiomas derivam, e isso permite um cálculo que o Maestro não faz,
mas que qualquer time pode fazer com o próprio processo:

- **T1** (a especificação precede o código) deriva de A1 e A4;
- **T2** (quem executa não verifica) deriva de A2 e A3;
- **T3** (o portão cresce com a irreversibilidade) deriva de A2 e A5;
- **T4** (critério sem comando não é critério) deriva de A2 e A4;
- **T5** (artefato sobrevive por consumo ou por imutabilidade) deriva de A3 e A4;
- **T6** (correção que não vira regra se repete) deriva de A3 e A4;
- **T7** (onde a saída não é comparável, o critério é uma linha de base) deriva de A2 e A4.

Cinco dos sete teoremas apoiam-se em pelo menos um axioma sobre pessoas ou sobre o mundo; dois,
T5 e T6, apoiam-se **só** nos dois axiomas que descrevem a ferramenta [CLAIM-16-009]. Essa é a
leitura deste livro, não uma afirmação do Maestro, e vale como **hipótese** até um modelo novo
testá-la: as regras mais expostas à próxima geração são as que nascem de T5 e T6 — o corte de
contexto, a poda de artefato que ninguém consome, a obrigação de transformar toda correção em
regra escrita. As mais protegidas são as que nascem de T3: o portão proporcional ao risco não
depende de nada que um modelo melhore.

Há uma ressalva honesta. T6 talvez sobreviva mesmo que A3 e A4 deixem de valer para o agente,
porque continuam valendo para o **time**: gente sai, gente entra, e a conversa de terça não
chega a quem começa na quarta. Um modelo com memória perfeita não dá memória ao humano que o
rege. É por isso que o mapa acima classifica premissas, e não decreta a morte de regras.

### O gatilho é a teoria da mudança

Saber quais regras são frágeis não basta; é preciso perceber o momento em que a premissa
mudou. O Maestro tem uma resposta escrita para isso desde cedo. O capítulo de decisões de
engenharia do *handbook* descreve o YAGNI (*You Aren't Gonna Need It*, "você não vai precisar
disso") como **poda ativa**: só entra o que dói agora, e o risco de subestimar uma necessidade
real é mitigado por um gatilho — "decisão adiada com condição escrita de revisão"
[CLAIM-16-010]. O corolário C1 dos axiomas dá a forma completa: "toda cerimônia tem um gatilho,
e o gatilho é **mensurável**", derivado de T6. A evidência que o documento oferece para T6 é o
caso que o motivou: a própria retrospectiva do método foi uma regra sem gatilho por 33 ciclos,
até o ciclo 034 dar um a ela [CLAIM-16-011].

A falha deste capítulo está toda na palavra "mensurável". Os gatilhos das ideias 029 e 003
eram **escritos** e eram **bons** — específicos, observáveis, com um evento que qualquer um
reconheceria. Mas nenhum comando os confrontava com os eventos do repositório. Aplique T4 ao
gatilho e a conclusão é imediata: um gatilho sem comando que o verifique não é um gatilho; é
uma intenção registrada. Medir que ele existe, como fazia a linha 255 do portão, é o "proxy"
do [capítulo 10](../10-quality-gates-que-provam-fatos/capitulo.md); o fato é se ele disparou.

Junte as duas metades e a teoria do capítulo fica em uma frase. **O futuro entra no processo
por dois caminhos: pela premissa que enfraquece e pelo gatilho que dispara. Os dois só
funcionam se forem verificados por máquina**, porque a alternativa — alguém se lembrar — é
justamente o que A4 diz que não sobrevive. O resto do capítulo trata do que isso exige: como
escrever gatilhos que um script consegue ler, o que fazer com um calendário externo que muda
sozinho, como o regulatório de aplicação escalonada, e onde a regra de vigiar o futuro passa a
custar mais do que vale.

### Um calendário externo de verdade: o *AI Act* marco a marco

Os modelos não publicam a data em que vão mudar. A lei publica. O Regulamento (UE) 2024/1689,
o Regulamento Europeu de Inteligência Artificial (*AI Act*), saiu no Jornal Oficial da União
Europeia em 12 de julho de 2024, entrou em vigor em 1º de agosto de 2024 e escalonou a
aplicação no art. 113 [CLAIM-16-018]. Dois anos depois, o Regulamento (UE) 2026/1744, chamado
de *Digital Omnibus on AI*, foi publicado em 24 de julho de 2026 e entrou em vigor em 27 de
julho, mudando datas e parte do conteúdo [CLAIM-16-023]. Para um tech lead cujo produto chega
a usuários na União Europeia, o regulamento é o melhor exemplo de gatilho de relógio que este
capítulo tem, e também do relógio que muda de hora.

A tabela abaixo dá, para cada marco, o que passa a valer e o que um time que constrói com
agentes faz a respeito. O conteúdo vem do texto do regulamento e da alteração, conferidos em
eur-lex.europa.eu em 2 de novembro de 2026 [CLAIM-16-018, CLAIM-16-023, CLAIM-16-024]. Isto
não é parecer jurídico. Serve para o time saber o que perguntar ao jurídico, e quando.

| Data | O que passa a valer | O que o tech lead faz |
|---|---|---|
| 02/02/2025 | **Proibições** do art. 5: manipulação que distorce comportamento e causa dano, exploração de vulnerabilidade (idade, deficiência, situação social), pontuação social, previsão de crime só por perfil, raspagem indiscriminada de rostos para bases de reconhecimento, inferência de emoção no trabalho e na escola, categorização biométrica de traços sensíveis e identificação biométrica remota em tempo real para a polícia, com exceções estreitas. **Letramento em IA** (art. 4). | Inventário de onde o produto usa IA, com uma linha por uso e a pergunta "isto cai no art. 5?" respondida por escrito. Um programa de letramento para quem opera e para quem rege agentes. Desde o 2026/1744, o art. 4 pede "tomar medidas que apoiem" o letramento, sem exigir nível garantido de cada pessoa [CLAIM-16-024]. A obrigação ficou mais branda, mas não acabou. |
| 02/08/2025 | **Modelos de IA de uso geral** (capítulo V): quem fornece o modelo mantém documentação técnica, repassa informação a quem o integra, tem política de direitos autorais e publica resumo do conteúdo de treino (art. 53); com risco sistêmico, avalia o modelo com testes adversariais, mitiga risco, reporta incidente grave e protege o modelo (art. 55). Também passam a valer governança e penalidades. | Quase todo time é **integrador**, não fornecedor do modelo. Peça ao fornecedor a documentação que o art. 53(1)(b) o obriga a repassar e versione-a junto do registro da decisão que escolheu o modelo. Se o time faz ajuste fino ou distribui um modelo próprio, leve a pergunta "somos fornecedores?" ao jurídico. |
| 27/07/2026 | Entra em vigor o 2026/1744. | Reconferir o calendário inteiro. Foi o que este capítulo não tinha feito na primeira versão (ver "Contraexemplo"). |
| 02/08/2026 | Aplicação geral, incluindo a **transparência** do art. 50: quem fala com uma IA precisa saber disso, salvo quando é óbvio (50(1)); saída sintética de áudio, imagem, vídeo ou texto marcada em formato legível por máquina (50(2)); aviso a quem é exposto a reconhecimento de emoção (50(3)); quem publica *deepfake* informa que o conteúdo foi gerado ou manipulado (50(4)). | Todo agente que conversa com cliente se apresenta como IA. Toda geração de mídia sai marcada, e a marca tem teste automatizado no portão, como qualquer outro critério verificável do [capítulo 10](../10-quality-gates-que-provam-fatos/capitulo.md). |
| 02/12/2026 | Sistema generativo que **já estava no mercado** antes de 02/08/2026 tem até aqui para cumprir a marcação do art. 50(2) (art. 111(4), novo). Começam as **proibições novas** do art. 5: gerar ou manipular imagem, vídeo ou áudio realista das partes íntimas ou de atividade sexual de pessoa identificável sem consentimento, e material de abuso sexual infantil. Para o fornecedor, a proibição vale quando isso é a finalidade **ou** um resultado razoavelmente previsível e reproduzível sem modificação técnica significativa, e o sistema não tem salvaguardas adequadas [CLAIM-16-025]. | Se o produto gera imagem, vídeo ou áudio: salvaguardas escritas, testadas com casos adversariais e com o resultado guardado como evidência antes da data. É o critério "previsível e reproduzível" que torna o teste obrigatório na prática: sem teste, o time não sabe o que é previsível. |
| 02/12/2027 | **Alto risco do Anexo III** (emprego, crédito, educação, serviços essenciais, entre outros): gestão de risco (art. 9), dados e governança de dados (10), documentação técnica (11), registro automático de eventos durante toda a vida do sistema (12), informação a quem implanta (13), supervisão humana efetiva (14), exatidão, robustez e cibersegurança (15). Quem implanta guarda os registros por pelo menos seis meses (art. 26(6)). Era 02/08/2026 no texto original. | Classificar cada uso: o agente decide ou apoia decisão sobre emprego, crédito ou educação? Se sim, o que o método deste livro já pede vira exigência legal: rastreabilidade, registro, revisor humano com poder de parar. O 2026/1744 não tocou nos arts. 9, 12, 13, 14 e 15. Alterou os arts. 6, 10 e 11 (documentação simplificada para empresas pequenas e médias). E um sistema já no mercado antes da data só entra no regime se mudar de forma significativa depois dela (art. 111(2)) [CLAIM-16-024]. Planeje a "mudança significativa" como evento que dispara a conformidade. |
| 02/08/2028 | **Alto risco embutido em produto já regulado** (art. 6(1), Anexo I: brinquedos, elevadores, dispositivos médicos e outros; o 2026/1744 também mexe na lista desse anexo). Era 02/08/2027. | Só para quem põe IA como componente de segurança de um produto desses. A conformidade passa pelo processo de avaliação do produto, e não por um processo separado. |

Três leituras saem da tabela. A primeira: o que foi adiado foi a **data** do alto risco, e não
os requisitos centrais (gestão de risco, registro, supervisão humana) [CLAIM-16-024]. A
segunda: a alteração de 2026 também **criou** obrigação, com as proibições novas de dezembro
de 2026, e quem leu "Omnibus" como "adiamento" leu metade. A terceira é a deste capítulo. Um
calendário regulatório é um gatilho de relógio, e o relógio pode ser remarcado por outro ato.
O exemplo executável trata o calendário como dado com fonte **e** data da última conferência, e
recusa responder quando essa data fica velha demais.

## Alternativas

Há pelo menos cinco jeitos de um time lidar com o que vem depois. Todos existem na prática, e
cada um resolve uma parte do problema que a falha deste capítulo expôs: perceber, com data, que
uma premissa mudou ou que um gatilho disparou.

**Reagir quando doer.** É o padrão de quase todo time, e não é descuido: ninguém tem tempo de
vigiar o mercado de modelos toda semana. O custo aparece no momento errado. Quando dói, a
decisão é tomada às pressas, sem o registro do que se tinha visto antes e sem a condição que
teria permitido antecipá-la. A ideia 003 do Maestro mostra a versão desse custo: o conflito
entre *worktrees* aconteceu e foi resolvido à mão no commit, mas a decisão de método ("isolar
por tarefa, ou não?") nunca foi retomada. A dor foi tratada; a regra continuou como estava.

**Radar de tecnologia.** O formato popularizado pelo *Technology Radar* da Thoughtworks
classifica ferramentas e técnicas em anéis (adotar, experimentar, avaliar, segurar) e revisa
tudo numa cadência fixa. Tem duas virtudes: obriga a escrever o veredito e cria um ritual de
revisão. Tem dois limites para o problema deste capítulo. A unidade costuma ser a
**ferramenta**, e não a ideia — e o Maestro registrou por escrito por que isso não é acionável:
"absorver + observar" sobre uma ferramenta inteira não diz o que entra nem onde. E a revisão é
por **calendário**, não por evento: o gatilho da ideia 029 disparou em 12 de outubro, e um
radar periódico o veria, com sorte, semanas depois, se alguém se lembrasse de cruzá-lo.

**ADR com data de revisão.** Muitos times acrescentam ao registro de decisão de arquitetura
(ADR, *Architecture Decision Record*) um campo "revisitar em". É barato e melhor que nada, mas
troca um gatilho de evento por um de relógio. Para a próxima geração de modelos, o relógio é
o gatilho errado: ninguém sabe em que trimestre a janela de contexto deixa de degradar, e uma
revisão marcada para março não vê o lançamento de fevereiro. Para o regulatório, ao contrário,
o relógio é o gatilho certo — a lei publica as datas.

**Comprar uma plataforma gerenciada.** As plataformas de agentes dos grandes provedores
oferecem memória de longo prazo, delegação entre agentes e fluxos determinísticos — ou seja,
prometem resolver por você justamente as premissas A3 e A4. O Maestro avaliou uma delas, o
*Agent Development Kit* (ADK) do Google, como a ideia 040: o que ela ensina "já foi absorvido
sem ela", a reversibilidade é **baixa** (*lock-in* de nuvem), e o veredito é observar, com o
gatilho "ida a nuvem gerenciada", que é uma decisão de infraestrutura e não de método
[CLAIM-16-014]. A ideia 016, a especificação executável da Tessl, recebeu o mesmo tratamento
por outra via: a tese reforça o método, mas a **aposta** numa ferramenta comercial e imatura
não é reversível barato, e o gatilho é duplo — a ferramenta amadurecer **e** existir caso
público de produção que se possa ler [CLAIM-16-015].

**Adotar um protocolo e construir o resto.** Entre comprar e fazer tudo em casa existe a opção
de seguir os protocolos abertos que estão se formando — o *Agent2Agent* (A2A), para conversa
entre agentes, e o *Agent Client Protocol* (ACP), para a conversa entre editor e agente — e
construir o mínimo por cima. Foi o que o Maestro decidiu em 28 de outubro de 2026, depois de
analisar na fonte cinco candidatos a plano de controle de agentes (Paperclip, CompozyOS,
AgentConnect, ACP e A2A): **construir**, com os padrões nas bordas e nenhum produto como base;
os nomes de estado do A2A entram no envelope das mensagens, "sem fio nem SDK", e o ACP entra
como um dos modos de uma porta de *harness*, com versões fixadas [CLAIM-16-013]. Protocolo
envelhece mais devagar que produto, e o custo de sair dele é trocar um adaptador.

| Alternativa | Percebe o evento? | Unidade | Custo de sair | Veredito |
|---|---|---|---|---|
| Reagir quando doer | só depois da dor | nenhuma | — | rejeitada: decide às pressas e não corrige a regra |
| Radar de tecnologia | só na cadência | ferramenta | baixo | **parcial**: bom ritual, gatilho de relógio |
| ADR com "revisitar em" | só na data | decisão | baixo | **parcial**: certo para o regulatório, cego para modelo |
| Plataforma gerenciada | o fornecedor percebe por você | produto | alto | observar; só com decisão de infraestrutura |
| Protocolo nas bordas + construir | depende do seu gatilho | ideia | médio | **adotada** no Maestro, com gatilho por ideia |

O quadro deixa uma lacuna que nenhuma das cinco fecha sozinha: todas registram a decisão, e
nenhuma confronta, por máquina, o gatilho escrito com o que aconteceu. É essa a peça que o
padrão do Maestro tem pela metade.

## O padrão Maestro

O Maestro trata o futuro como trata qualquer outra afirmação do método: separa a **regra**,
o **artefato** que a carrega, o **script** que a confere e o **gancho** (*hook*) que impede
reescrevê-la. Tudo abaixo está em `maestro@19823c2`.

**A regra.** O corolário C1 dos axiomas diz que toda cerimônia tem um gatilho, e que o gatilho
é **mensurável**; deriva de T6 e aponta como mecanismo o `check-retro.sh`
([`docs/governance/axioms.md`](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/axioms.md)).
O Princípio VII da constituição dá o resto: governança que aprende sem inchar, com YAGNI podando
o que não se paga
([`docs/governance/principles.md`](https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/principles.md)).
Aplicadas ao ecossistema, as duas viram uma frase do catálogo: "observar" sem gatilho é
esquecer com cerimônia; quando nenhuma condição futura mudaria a decisão, o veredito honesto
é descartar.

**Os artefatos.** O catálogo
([`docs/ecosystem/README.md`](https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/README.md))
tem três peças com ritmos diferentes de mudança: `fontes.md`, uma linha por fonte com a
licença; `ideias/`, um cartão datado por ideia, que **nunca** muda; e `estado.jsonl`, o
veredito corrente, que só cresce — o estado de hoje é a última linha de cada ideia. Todo
cartão avalia sete dimensões, sempre na mesma ordem, e duas reprovam sozinhas: conflito
insanável com princípio e licença incompatível [CLAIM-16-012]. A quinta dimensão é a
reversibilidade — quanto custa sair depois —, e é ela que decide quase todas as escolhas entre
comprar, adotar protocolo e construir que a seção anterior comparou. Não há nota agregada, por
decisão escrita: uma média esconderia qual dimensão decidiu.

**O script.** O
[`scripts/check-ecosystem.sh`](https://github.com/GHDaru/maestro/blob/19823c2/scripts/check-ecosystem.sh)
roda na integração contínua (CI, *continuous integration*) junto com os outros portões
([`.github/workflows/ci.yml`](https://github.com/GHDaru/maestro/blob/19823c2/.github/workflows/ci.yml)).
O próprio cabeçalho diz o que ele mede e o que não mede: não mede se um veredito é sábio — isso
é julgamento humano, que nenhum script faz —; mede que todo julgamento está ancorado: fonte com
licença, cartão datado, estado corrente e, para o que foi adotado ou absorvido, um destino que
**existe** no disco, com uma prova textual encontrada dentro dele. O motivo também está escrito:
duas ideias do ADR 0008 ficaram registradas como absorvidas por 39 ciclos sem nunca chegarem a
um arquivo [CLAIM-16-016]. É o mesmo defeito da falha deste capítulo visto do outro lado: lá, o
registro sobreviveu ao fato; aqui, o fato aconteceu e o registro não soube.

**O gancho.** Um gancho `PreToolUse` — `scripts/hooks/guard-immutables.py`, ligado em
`.claude/settings.json` — recusa a edição de qualquer arquivo em `docs/ecosystem/ideias/`.
O agente que muda de ideia sobre uma ferramenta não pode reescrever o que se julgou em julho;
anexa uma linha nova ao índice. É isso que permite a alguém, em novembro, perguntar "o que
sabíamos em agosto?" e obter a resposta de agosto.

**O que falta, dito com franqueza.** O portão verifica a **forma** do gatilho, não o
**disparo**. As peças para verificar o disparo já existem no próprio repositório — o histórico
do git, o índice de decisões, os ciclos com data —, mas não estão ligadas ao catálogo. Este
livro propõe a ligação mais barata, sem reescrever o catálogo: um arquivo de **eventos**
anexável, em que cada linha diz "a ideia X teve o gatilho tocado na data D, com esta prova", e
uma checagem que reprova quando existe evento posterior à data do estado corrente de uma ideia
em observação. A proposta é do livro, não do Maestro; o exemplo a seguir a executa contra o
índice real. Ela não transforma julgamento em máquina — quem decide que o gatilho disparou
continua sendo uma pessoa, que escreve o evento —, mas transforma o esquecimento num vermelho.

O mesmo desenho serve para as premissas. Os teoremas declaram de quais axiomas derivam; um
script que lê essas derivações responde, para qualquer cenário do tipo "a próxima geração
enfraquece A3", quais regras perdem apoio. Quando o fornecedor anunciar o modelo novo, a
conversa do time começa por essa lista, e não pela opinião de quem leu o anúncio.

## Exemplo executável

O exemplo está em [`exemplo/`](exemplo/README.md): um único script, `futuro.py`, em Python 3
sem nenhuma dependência externa, e quatro arquivos de dados. Rode da raiz do livro:

```bash
python livro/16-o-futuro-da-engenharia-agentica/exemplo/futuro.py demo
```

O roteiro faz três verificações e sai com código 0 se os resultados esperados aparecerem.

**1. Sensibilidade do método à próxima geração.** `dados/axiomas.json` copia, de
`maestro@19823c2:docs/governance/axioms.md`, de quais axiomas cada teorema deriva e de quais
teoremas (ou axiomas) cada corolário deriva. A regra do script é simples: um elemento fica
**exposto** se alguma das suas fontes enfraqueceu, e **sem apoio** se todas enfraqueceram.
No cenário "janela de contexto maior e que não degrada" (A3 enfraquece), três teoremas ficam
expostos — T2, T5 e T6 — e nenhum fica sem apoio. No cenário "janela maior e memória
persistente do fornecedor" (A3 e A4 enfraquecem), seis dos sete ficam expostos, T5 e T6 ficam
sem apoio, e só T3, o portão proporcional à irreversibilidade, fica intacto; entre os
corolários, 12 de 13 ficam expostos e quatro ficam sem apoio: C1, C9, C10 e C12
[CLAIM-16-017]. O resultado mais útil é o que surpreende: C1 — "toda cerimônia tem um gatilho
mensurável", a regra deste capítulo inteiro — está entre os que perdem o chão. Não porque fique
errada, mas porque o motivo escrito para ela é sobre a ferramenta; se A4 deixar de valer para o
agente, o time precisa dar a ela outro motivo (a memória do **time**, que nenhum modelo
melhora) ou aceitar que virou cerimônia.

Rode também só o cenário que interessa ao seu time:

```bash
python livro/16-o-futuro-da-engenharia-agentica/exemplo/futuro.py sensibilidade A3 A4
```

**2. Gatilhos escritos e gatilhos vigiados.** `dados/estado.jsonl` é o índice real do catálogo
em `19823c2`; `dados/eventos.jsonl` tem três eventos, cada um com a prova no Maestro: o pedido
de custo do ciclo 065, o lançador por *worktree* do ciclo 066 e a integração com conflitos do
ciclo 072. O script aplica o portão antigo (todo "observar" tem gatilho?) e o portão novo
(algum gatilho disparou depois da data do estado, sem reavaliação?). Sobre o índice como está,
o antigo fica VERDE com 16 ideias em observação, e o novo fica VERMELHO com duas,
`trilha-com-custo` e `worktree-por-task`, cada uma com o evento e a prova que a disparou.
Depois de anexar uma linha de reavaliação para cada uma — sem apagar nada —, os dois portões
ficam verdes e restam 15 em observação [CLAIM-16-017]. No seu repositório, a forma de uso é a
mesma:

```bash
python futuro.py gatilhos caminho/estado.jsonl caminho/eventos.jsonl   # sai 1 se houver disparo
```

**3. O relógio regulatório.** O Regulamento Europeu de Inteligência Artificial (*AI Act*) tem
aplicação escalonada, e um tech lead que vende para a União Europeia precisa saber o que já
vale numa data. `dados/ai-act.json` registra sete marcos, cada um com a data original do
art. 113 e a data depois do Regulamento (UE) 2026/1744, além do que mudou no conteúdo. Para 2
de novembro de 2026, três marcos se aplicam: as proibições originais com o letramento, os
modelos de uso geral e a transparência do art. 50. Quatro mudaram de data ou nasceram com a
alteração: as proibições novas e a transição da marcação de conteúdo sintético, ambas para 2
de dezembro de 2026, e os dois marcos de alto risco [CLAIM-16-018, CLAIM-16-023,
CLAIM-16-026]. O arquivo é material didático, não parecer jurídico, e diz isso no campo
`_fonte`, que cita os dois atos com o endereço oficial.

O dado carrega também `conferido_em` (a data em que alguém o comparou com o Jornal Oficial) e
`validade_dias`. O roteiro consulta o mesmo arquivo em 1º de março de 2027, sem nova
conferência, e o calendário responde "VENCIDO" em vez de responder datas. Essa é a única parte
da verificação 3 que não é circular. O resto confere que o script lê corretamente o que foi
digitado; um erro de digitação contra o Jornal Oficial passaria verde. O mesmo vale para a
verificação 1, cujo `axiomas.json` foi copiado à mão de `axioms.md`. Só a verificação 2 lê um
dado que o livro não escreveu: o índice real do catálogo.

A saída completa esperada está no [`README.md` do exemplo](exemplo/README.md). Se algum número
divergir, o roteiro imprime "FALHOU" e sai com código 1: é um teste do próprio capítulo.

## Contraexemplo

Vigiar o futuro custa atenção, e em alguns lugares a regra deste capítulo atrapalha mais do que
protege. Seis casos, cada um com o custo que a regra cobra.

**O gatilho que nenhuma máquina mede.** A ideia 018 do catálogo, orquestrar uma frota de
agentes, tem um gatilho bem escrito e humano de propósito: "existir trabalho paralelo real que a
atenção de **um** humano consiga governar". O próprio cartão sublinha que "a condição é o
humano, não a máquina" [CLAIM-16-019]. Nenhum script mede atenção. Se o time quiser
transformar esse gatilho em comando, vai acabar contando alguma coisa vizinha, como sessões
abertas, *worktrees* vivas ou mensagens por hora, e cai no anti-padrão do
[capítulo 10](../10-quality-gates-que-provam-fatos/capitulo.md): o portão mede o proxy e fica
verde ou vermelho pelo motivo errado. Para gatilhos assim, a forma honesta é a da proposta
deste capítulo, mas lida ao contrário: o evento é escrito por uma pessoa ("nesta semana não
consegui acompanhar três trabalhadores ao mesmo tempo"), e a máquina cobra só que alguém releia
o gatilho depois do evento. Ela vigia a releitura, não o mundo. Quem anunciar "nossos gatilhos
são todos automáticos" está escondendo um gate humano atrás de um verde.

**O evento que ninguém escreve.** A proposta da seção anterior troca o esquecimento de lugar.
Antes, alguém precisava se lembrar de reler dezesseis gatilhos; depois, precisa se lembrar de
anotar um evento. Se o arquivo de eventos depender de boa vontade, o portão novo fica verde pelo
mesmo motivo que o antigo, e o capítulo terá acrescentado uma cerimônia. O remédio é prender a
escrita do evento a um passo que já existe e que ninguém pula: a seção de origem da
especificação, a abertura do ciclo, a retrospectiva. O ciclo 065 é o caso favorável, porque a
frase que disparou o gatilho da ideia 029 estava escrita na origem da própria especificação
[CLAIM-16-003]; um revisor que lesse a especificação com o catálogo ao lado teria visto. Sem esse
elo, não adote a proposta, porque ela só acrescenta cerimônia.

**O relógio que muda de hora.** Na seção "Alternativas", este capítulo disse que, para o
regulatório, o relógio é o gatilho certo. Isso é só meio verdade. O Regulamento Europeu de
Inteligência Artificial publicou os marcos de 2025 a 2027 no art. 113, e o Regulamento (UE)
2026/1744 remarcou os dois de alto risco, criou proibições novas para dezembro de 2026 e deu
prazo de transição à marcação de conteúdo sintético [CLAIM-16-023]. A data publicada é,
portanto, um gatilho que pode ser remarcado. Um script que lê um calendário congelado responde
com confiança e erra no dia em que a lei muda de novo.

Este capítulo caiu nisso. A primeira versão registrava as datas novas sem o número do ato que
as mudou, sem data de conferência, e afirmava que nada no conteúdo tinha mudado. As
proibições novas de dezembro de 2026 não apareciam, e as alterações nos arts. 4, 10 e 11 também
não. O exemplo rodava e dizia "OK". Um revisor independente apontou; a correção foi conferir o
texto no Jornal Oficial e acrescentar ao dado a data da conferência, com prazo de validade
[CLAIM-16-026]. É o defeito do capítulo dentro do capítulo, e um caso a mais de "o check mede o
proxy": o "OK" media a coerência do script com o arquivo, e não a do arquivo com a lei.

Disso saem duas consequências práticas. A primeira: o gatilho regulatório é duplo, a data
**e** a publicação de alteração, e o arquivo de calendário precisa de fonte e de data da última
conferência. A segunda pesa mais: o que não mudou com o adiamento (gestão de risco, registro de
eventos, supervisão humana) é o que um método derivado de A2 e A5 já pediria de qualquer jeito.
Use o adiamento para planejar com folga, mas não como licença para adiar a rastreabilidade que
o seu time construiria por outros motivos.

**A vigília que vira vigilância.** Para perceber eventos, a tentação é registrar tudo: cada
*prompt*, cada sessão, cada mensagem. A base de pesquisa deste livro tem uma regra curta para
isso, "*tracing* não é retenção indiscriminada", e a põe ao lado da Lei Geral de Proteção de
Dados (LGPD) e do *sandbox* regulatório da Autoridade Nacional de Proteção de Dados (ANPD)
[CLAIM-16-020]. Um arquivo de eventos com uma linha por gatilho tocado e a prova apontando para
um commit é pequeno, auditável e não guarda dado pessoal. Um rastreador que guarda conversas
inteiras "para o caso de algum gatilho disparar" cria um passivo maior do que a ideia que ele
vigia.

**O mapa da fragilidade lido como decreto.** A conclusão de que T5 e T6 são os teoremas mais
expostos é uma hipótese deste livro [CLAIM-16-009]. O uso errado é podar a retrospectiva ou o
corte de contexto no dia em que um fornecedor anuncia janela maior. Isso troca uma premissa por
uma nota de lançamento. O gatilho da ideia 017, "com perda de contexto medida", mostra o modelo
certo [CLAIM-16-008]: a regra muda quando o time **mede** que a premissa enfraqueceu no seu
próprio trabalho, e não quando alguém lê o anúncio. Vale o mesmo para o padrão que o
*handbook* do Maestro deixa de fora de propósito: dos seis padrões de orquestração que mapeia, o
agente autônomo, "modelo aberto com guarda-corpos", é o único marcado como evitado, por YAGNI
[CLAIM-16-021]. Um modelo melhor não reabre essa porta. O que reabre é uma medida, no seu
contexto, de que os guarda-corpos bastam.

**Construir quando comprar seria o certo.** A decisão do Maestro de construir sobre protocolos
[CLAIM-16-013] serve a um projeto cujo produto é a própria governança. Num time cuja empresa já
decidiu por uma nuvem gerenciada, o gatilho da ideia 040, "ida a nuvem gerenciada"
[CLAIM-16-014], disparou antes do primeiro dia, e construir o próprio plano de controle passa a
ser custo sem retorno. A reversibilidade continua decidindo, mas a partir do lugar onde o time
já está. Vale o mesmo para o tamanho do catálogo: 41 ideias com estado corrente [CLAIM-16-002]
fazem sentido para quem tem o método como produto. Para um time de produto pequeno, a versão que
se paga é uma lista curta, com gatilho por linha e uma releitura presa à retrospectiva. O resto
cai pelo critério de YAGNI.

## Evidência

O que sustenta o capítulo vem separado pelo estado de cada afirmação. A tabela completa, com a
evidência reproduzível de cada claim, está em [`claims.md`](claims.md). Quase tudo aqui é do
Maestro na versão `19823c2`, e os comandos de conferência são `git show` e `git log` sobre essa
versão.

**Medido** (reproduzível por comando). O catálogo do ecossistema e os seus números: 41 ideias
com estado corrente, 16 delas em observação e todas as 16 com gatilho [CLAIM-16-002]. O estado
corrente das duas ideias cujo gatilho disparou [CLAIM-16-004]. O commit de 29 de outubro que
acrescentou uma única linha ao índice sem tocar nas de cima [CLAIM-16-005]. O bloco do portão
que confere a existência do gatilho e mais nada [CLAIM-16-006]. A contagem de axiomas, teoremas e
corolários [CLAIM-16-007]. A derivação dos teoremas, de onde sai que dois deles dependem só dos
axiomas sobre a ferramenta [CLAIM-16-009]. A saída do exemplo executável, que reproduz tanto o
cálculo de sensibilidade quanto os dois portões [CLAIM-16-017]. Esses números não dependem de
interpretação: mude a versão do Maestro e eles mudam, mas, na versão citada, qualquer pessoa
chega a eles.

**Observado** (registrado em commit, especificação, cartão ou índice de decisões). A criação do
catálogo e do portão no ciclo 047 [CLAIM-16-001]. Os eventos que tocaram os gatilhos das ideias
029 e 003, com as datas e os commits [CLAIM-16-003]. A ideia 017 e o seu gatilho de perda de
contexto medida [CLAIM-16-008]. O YAGNI descrito como poda ativa [CLAIM-16-010] e a evidência de
T6, a retrospectiva sem gatilho por 33 ciclos [CLAIM-16-011]. As três peças e as sete dimensões
do catálogo [CLAIM-16-012]. A decisão de 28 de outubro sobre o plano de controle, depois de
cinco análises na fonte [CLAIM-16-013]. Os vereditos das ideias 040, 016 e 018 [CLAIM-16-014,
CLAIM-16-015, CLAIM-16-019]. O que o cabeçalho do portão diz medir e o gancho que protege os
cartões [CLAIM-16-016]. O padrão autônomo marcado como evitado no *handbook* [CLAIM-16-021].

**Interpretação do livro, não do Maestro.** Duas leituras centrais deste capítulo são nossas e
precisam ser lidas assim. A primeira é dizer que os gatilhos das ideias 029 e 003 **dispararam**.
O pedido do ciclo 065 bate com a letra do gatilho da 029 quase palavra por palavra. O da 003 é
mais discutível: o gatilho fala de "dois ou mais agentes escrevendo no mesmo repositório ao
mesmo tempo, com conflito observado", e o que o commit `d71cee6` registra é um conflito
resolvido na integração de uma *worktree*. Um mantenedor do Maestro pode argumentar que isso é
conflito de integração, e não de escrita simultânea. A tese do capítulo sobrevive a essa
objeção, porque o defeito apontado não é "o veredito está errado". O defeito é que ninguém foi
chamado a decidir. A segunda leitura é o mapa da fragilidade: o Maestro declara de quais
axiomas cada teorema deriva, e a conclusão de que T5 e T6 são os mais expostos à próxima geração
é deste livro [CLAIM-16-009].

**Observado em fonte oficial.** O calendário do Regulamento Europeu de Inteligência Artificial
e o seu conteúdo, conferidos em eur-lex.europa.eu em 2 de novembro de 2026: as datas do art.
113, original e alterado [CLAIM-16-018]; a identidade, a publicação e a vigência do Regulamento
(UE) 2026/1744 e as regras de transição do art. 111 [CLAIM-16-023]; o que cada marco exige e o
que a alteração mudou ou não mudou [CLAIM-16-024, CLAIM-16-025]. A leitura de "o que o tech
lead faz" em cada marco é deste livro, e não substitui parecer jurídico. A conferência tem data
e vence: o arquivo do exemplo a declara, e o script cobra a próxima [CLAIM-16-026].

**Hipótese** (não medida; agenda da pesquisa). Três hipóteses da agenda do livro tocam este
capítulo. A H10, de que retrospectiva que vira regra reduz recorrência, é a hipótese por trás do
corolário C1. A falha real mostra a metade que o desenho da H10 não captura: uma regra com
gatilho escrito que não reduziu nada, porque ninguém confrontou o gatilho com o mundo. A H8, de
que reversibilidade permite mais autonomia, é o critério que este capítulo usa para escolher
entre plataforma, protocolo e construção. A H9, de que modelo menor basta em tarefa estruturada,
é o ponto em que o futuro mais pode mudar a economia: se a estrutura (especificação, critério
verificável, papel definido) faz um modelo barato bastar, então o que o livro descreve fica mais
valioso a cada geração, e não menos. Nenhuma das três foi medida com braço de controle. A
métrica e o desenho de cada uma estão em [`pesquisa/hipoteses.md`](../../pesquisa/hipoteses.md);
os níveis de comparação comuns a toda a agenda estão no
[capítulo 15](../15-validando-o-maestro/capitulo.md).

**Limites.** Os casos são de um repositório, com um humano regendo. O catálogo é o de um projeto
cujo produto é o próprio método, o que o torna mais cuidadoso que a média, e mesmo assim os dois
gatilhos passaram. A proposta do registro de eventos não foi testada em nenhum time: o exemplo
a executa sobre três eventos escritos por este livro, e o que ela promete (transformar o
esquecimento num vermelho) depende do elo de escrita do evento, que o "Contraexemplo" mostra
ser o ponto fraco. A literatura acadêmica sobre sistemas multiagente para engenharia de
software, como a revisão e agenda de He, Treude e Lo [CLAIM-16-022], aponta para onde o campo
vai, mas é visão e não evidência de que alguma regra deste livro sobreviva. O capítulo não faz
previsão sobre modelos. Afirma só que o processo do seu time deve ter, por escrito e conferido
por máquina, o caminho pelo qual uma previsão errada seria corrigida.

## Checklist

Aplique no seu time. Cada item tem uma forma de conferir; os que não têm comando estão marcados
como julgamento, com dono.

**Premissas**

- [ ] Cada regra do processo do time aponta para a premissa de que deriva: pessoas, consequência,
      custo de desfazer ou ferramenta. Confira: uma busca por regra sem premissa no documento de
      processo volta vazia.
- [ ] As regras que dependem só da ferramenta (no Maestro, as derivadas de T5 e T6) estão
      marcadas como **expostas**, e cada uma tem escrito o que o time mediria para saber que a
      premissa enfraqueceu.
- [ ] Existe um comando, como o `futuro.py sensibilidade`, que responde quais regras perdem apoio
      num cenário do tipo "a janela de contexto deixa de degradar". O time o roda quando um modelo
      novo é adotado, antes da conversa sobre mudar o processo.
- [ ] Nenhuma regra foi removida por causa de um anúncio. Toda remoção cita uma medida feita no
      trabalho do próprio time (julgamento; dono: quem aprova mudanças de processo).

**Gatilhos**

- [ ] Todo "observar", "adiar" ou "revisitar" tem gatilho escrito, e um portão reprova quando o
      gatilho falta. É o portão antigo, e ele continua necessário.
- [ ] Todo gatilho é de **evento** quando o evento é observável no repositório (pedido, commit,
      conflito, medida) e de **relógio** só quando quem publica a data é externo, como uma lei ou
      o fim de suporte de um fornecedor.
- [ ] Há um registro de eventos anexável (uma linha por gatilho tocado, com data e prova), e um
      portão reprova quando existe evento posterior ao estado corrente de uma ideia em observação.
      Confira: anexe um evento de teste e veja o vermelho.
- [ ] A escrita do evento está presa a um passo que já existe: a origem da especificação, a
      abertura do ciclo ou a retrospectiva. Não depende de alguém lembrar.
- [ ] Os gatilhos que dependem de julgamento humano (atenção, confiança, maturidade de mercado)
      estão marcados como tal, e o portão cobra a releitura, não o fato.
- [ ] Reavaliar é anexar: a decisão nova entra como linha nova, e um gancho ou portão recusa a
      reescrita do que foi decidido antes.

**Calendário externo**

- [ ] Os marcos regulatórios que afetam o produto (por exemplo, o calendário escalonado do
      Regulamento Europeu de Inteligência Artificial, se o time vende para a União Europeia)
      estão num arquivo versionado com fonte (número do ato e endereço oficial), data da
      última conferência e prazo de validade. Confira: consultado depois da validade, o
      calendário responde "vencido", e não datas.
- [ ] O gatilho regulatório é duplo: a data do marco **e** a publicação de alteração. Alguém tem o
      dever, com cadência escrita, de conferir o texto oficial (julgamento; dono nomeado).
- [ ] Para cada marco que se aplica ao produto, há uma ação com dono e prazo anterior à data:
      inventário contra o art. 5, aviso de IA e marcação de conteúdo do art. 50, documentação
      do fornecedor do modelo guardada, classificação de alto risco (julgamento; dono: o tech
      lead, com o jurídico).
- [ ] O que não muda com adiamento (gestão de risco, documentação, registros, supervisão humana)
      tem plano próprio, desvinculado da data.
- [ ] A vigília não guarda mais dado do que precisa: o registro de eventos aponta para commits e
      documentos, não para conversas inteiras, e passa pela revisão de proteção de dados do time.

**Plataforma, protocolo ou construção**

- [ ] Toda adoção de plataforma, protocolo ou ferramenta de agentes tem registrado o custo de
      sair (a dimensão de reversibilidade) e a condição que reabriria a decisão.
- [ ] Onde há protocolo aberto estável, o time o adota nas bordas, com versão fixada, e mantém o
      núcleo trocável por adaptador.
- [ ] A decisão de construir cita o que já está decidido na empresa (nuvem, fornecedor,
      contrato). Se a infraestrutura já escolheu a plataforma, o gatilho de reavaliação já
      disparou.

**Cadência**

- [ ] O catálogo do que foi visto e não adotado cabe na atenção do time. Se ninguém relê a lista
      inteira numa retrospectiva, ela está grande demais, e as linhas sem gatilho viram
      "descartar".
- [ ] Uma vez por trimestre, o time compara o portão novo com a realidade: houve gatilho
      disparado que o registro de eventos não pegou? Se houve, o elo da escrita do evento falhou,
      e isso vira achado da retrospectiva.

## Referências

**Maestro** (versão `19823c2`, salvo indicação):

- Axiomas, teoremas T1–T7 e corolários C1–C13 —
  https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/axioms.md
- Constituição, Princípios III e VII —
  https://github.com/GHDaru/maestro/blob/19823c2/docs/governance/principles.md
- Catálogo do ecossistema (as três peças e as sete dimensões) —
  https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/README.md
- Índice de estado das ideias —
  https://github.com/GHDaru/maestro/blob/19823c2/docs/ecosystem/estado.jsonl
- Cartões das ideias citadas: 003 (*worktree* por tarefa), 016 (especificação executável),
  017 (memória persistente de sessão), 018 (frota de agentes), 029 (trilha com custo), 040
  (plataforma gerenciada de agentes), 041 (diagrama vivo do time) —
  https://github.com/GHDaru/maestro/tree/19823c2/docs/ecosystem/ideias
- Portão do catálogo —
  https://github.com/GHDaru/maestro/blob/19823c2/scripts/check-ecosystem.sh
- Gancho que protege o que é imutável —
  https://github.com/GHDaru/maestro/blob/19823c2/scripts/hooks/guard-immutables.py
- Workflow de CI — https://github.com/GHDaru/maestro/blob/19823c2/.github/workflows/ci.yml
- Índice de decisões (decisão `decisao-076-control-plane-v2`) —
  https://github.com/GHDaru/maestro/blob/19823c2/docs/records/decisoes.jsonl
- Síntese das bancas do ciclo 076 (plano de controle, v2) —
  https://github.com/GHDaru/maestro/blob/19823c2/specs/076-padroes-de-engenharia-e-react/sintese-das-bancas.md
- Especificação do ciclo 065 (a origem do pedido de custo) —
  https://github.com/GHDaru/maestro/blob/19823c2/specs/065-o-metodo-se-cobra-e-bate-o-ponto/spec.md
- Roteiro com os itens adiados e os seus gatilhos —
  https://github.com/GHDaru/maestro/blob/19823c2/docs/roadmap.md
- Commits citados: `e73ee0d` (ciclo 047), `d5feef2` (ciclo 066), `d71cee6` (ciclo 072),
  `f79b1be` (ideia 041) — https://github.com/GHDaru/maestro/commit/<sha>
- *Handbook* do método, capítulos 05 (§5.4, os seis padrões) e 13 (§5.10, YAGNI como poda
  ativa), cópia congelada em
  [`maestro-handbook/`](../../maestro-handbook/handbook/13-decisoes-de-engenharia.md)

**Deste livro:**

- Base de pesquisa (tese, agenda, riscos e regulação) —
  [`pesquisa/base-de-pesquisa.md`](../../pesquisa/base-de-pesquisa.md)
- Hipóteses H8, H9 e H10 — [`pesquisa/hipoteses.md`](../../pesquisa/hipoteses.md)
- Capítulos relacionados: [10 — Quality gates que provam fatos](../10-quality-gates-que-provam-fatos/capitulo.md),
  [11 — Risco, reversibilidade e autonomia](../11-risco-reversibilidade-e-autonomia/capitulo.md),
  [12 — Ferramentas, MCP e o ecossistema](../12-ferramentas-mcp-e-o-ecossistema/capitulo.md),
  [13 — Observabilidade e economia](../13-observabilidade-e-economia/capitulo.md),
  [14 — A organização que aprende](../14-a-organizacao-que-aprende/capitulo.md),
  [15 — Validando o Maestro](../15-validando-o-maestro/capitulo.md)

**Externas.** Obras e textos normativos de referência. Nenhuma URL foi reconsultada para esta
versão; confira antes de citar:

- Regulamento (UE) 2024/1689 do Parlamento Europeu e do Conselho (Regulamento Europeu de
  Inteligência Artificial, *AI Act*), arts. 4, 5, 9–15, 26, 50, 53, 55, 111 e 113 —
  https://eur-lex.europa.eu/eli/reg/2024/1689/oj (conferido em 02/11/2026).
- Regulamento (UE) 2026/1744 do Parlamento Europeu e do Conselho, de 8 de julho de 2026, que
  altera os Regulamentos (UE) 2024/1689, (UE) 2018/1139 e (UE) 2023/1230 (*Digital Omnibus on
  AI*), JO L de 24/07/2026 — https://eur-lex.europa.eu/eli/reg/2026/1744/oj (conferido em
  02/11/2026).
- National Institute of Standards and Technology (NIST), *Artificial Intelligence Risk
  Management Framework (AI RMF 1.0)*, NIST AI 100-1, 2023, e o perfil de IA generativa,
  NIST AI 600-1, 2024.
- Lei nº 13.709/2018, Lei Geral de Proteção de Dados Pessoais (LGPD), e o programa de *sandbox*
  regulatório da Autoridade Nacional de Proteção de Dados (ANPD).
- J. He, C. Treude e D. Lo, "LLM-Based Multi-Agent Systems for Software Engineering: Literature
  Review, Vision and the Road Ahead", *ACM Transactions on Software Engineering and
  Methodology* (TOSEM), 2025.
- Anthropic, "Building effective agents", 2024 — os seis padrões de orquestração mapeados no
  §5.4 do *handbook*.
- Thoughtworks, *Technology Radar* — o formato de anéis citado em "Alternativas".
- Protocolos citados em "Alternativas": *Agent2Agent* (A2A) e *Agent Client Protocol* (ACP),
  tal como analisados na síntese das bancas do ciclo 076 do Maestro.
