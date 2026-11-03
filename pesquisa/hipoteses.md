# Hipóteses H1–H10 (agenda de pesquisa do livro)

> Versão 0.1 · 02/11/2026 · estado de todas: **hipótese, não testada**.
> Origem: [`base-de-pesquisa.md`](base-de-pesquisa.md), seção «Agenda de pesquisa» (linhas
> 41–54): o enunciado de cada hipótese, o desenho de quatro braços, os corpora e a lista de
> métricas vêm de lá. **O que é deste arquivo** (e ainda não foi revisado pelo Darú): a escolha
> de qual métrica mede qual hipótese, o contraste que isola cada uma e o critério de refutação.
> Apresentação no livro: [Apêndice C](../livro/apendices/c-pacote-de-replicacao/capitulo.md).

## Regras comuns a todas as hipóteses

**Braços do desenho** (da base de pesquisa):

| Braço | O que o agente recebe |
|---|---|
| A — linha de base | só o *prompt* da tarefa |
| B — spec | a tarefa como especificação escrita |
| C — spec + portões | B mais os portões automáticos (integração contínua, *fitness functions*) |
| T — tratamento | o Maestro completo: raias, papéis, revisão em contexto fresco, portões, ADRs (Architecture Decision Records), *skills*, *hooks* |

**Ambiente congelado** em cada execução: *commit* do Maestro, modelo e versão, *harness* e
versão, hashes das entradas. Sem isso o *run* não entra na análise.

**Repetições**: cada célula do desenho roda várias vezes; o resultado se relata como
distribuição com intervalo, nunca como um número só. O número de repetições, as margens de
não-inferioridade e o nível do intervalo **ainda não estão fixados**: vão para
`pesquisa/protocolo.md` antes do primeiro *run* e não mudam depois de olhar os dados.

**Refutar** significa: o intervalo do efeito, no contraste declarado, inclui zero ou aponta
contra a hipótese. Uma hipótese de não-inferioridade («sem perder qualidade», «basta») é
refutada quando o intervalo da perda ultrapassa a margem fixada no protocolo.

**Corpora disponíveis** (da base): ciclos históricos do Maestro; SWE-bench e SWE-Bench Pro;
o benchmark de governança ASEG-Bench (casos GOV-001 a GOV-010, ver
[Apêndice B](../livro/apendices/b-aseg-bench/capitulo.md)).

## As dez hipóteses

### H1 — A spec reduz retrabalho

- **Métrica**: retrabalho (iterações de correção depois da primeira entrega até a aceitação) e
  aceitação na primeira passada; secundária, custo do retrabalho em *tokens*.
- **Desenho**: contraste **A × B** sobre o mesmo conjunto de tarefas (SWE-bench / SWE-Bench Pro
  e ciclos históricos do Maestro reexecutados), mesmo modelo e *harness*. B × A isola a spec;
  C e T não entram neste contraste.
- **O que a refutaria**: retrabalho em B igual ou maior que em A (intervalo inclui zero ou
  favorece A); ou redução que some quando se soma o custo de escrever a spec ao custo por
  tarefa aceita.
- **Tratada em**: [capítulo 4](../livro/04-a-spec-como-partitura/capitulo.md).

### H2 — A revisão em contexto fresco acha mais defeito

- **Métrica**: rendimento da revisão independente — defeitos semeados encontrados ÷ defeitos
  semeados; secundária, falsos positivos por revisão.
- **Desenho**: o mesmo conjunto de *diffs* com defeitos injetados de forma conhecida, revisado
  (a) pelo agente autor, no contexto em que escreveu, e (b) por um agente em contexto fresco,
  mesmo modelo, **mesmo orçamento de tokens** de revisão.
- **O que a refutaria**: rendimento de (b) igual ou menor que o de (a); ou ganho que desaparece
  quando o orçamento é igualado (o efeito seria de «mais leitura», não de «contexto fresco»).
- **Tratada em**: [capítulo 2](../livro/02-o-problema-da-confianca/capitulo.md).

### H3 — Contexto seletivo reduz custo sem perder qualidade

- **Métrica**: *tokens* por tarefa e custo por tarefa aceita (eficácia); aceitação na primeira
  passada (qualidade, não-inferioridade).
- **Desenho**: dentro do braço T, contexto integral (tudo que o repositório oferece) × contexto
  seletivo (seleção, compressão, persistência, transferência), mesmas tarefas.
- **O que a refutaria**: custo por tarefa aceita que não cai; ou queda de aceitação além da
  margem de não-inferioridade fixada no protocolo.
- **Tratada em**: [capítulo 5](../livro/05-engenharia-de-contexto/capitulo.md).

### H4 — Multiagente só ajuda com cortes independentes

- **Métrica**: tempo de ciclo e custo por tarefa aceita; overhead de coordenação (*tokens* e
  mensagens gastos entre agentes, espera humana).
- **Desenho**: fatorial 2 × 2 — um agente × vários agentes, cruzado com tarefas de cortes
  independentes (contextos delimitados sem estado compartilhado) × tarefas acopladas.
- **O que a refutaria**: a hipótese tem duas metades. Refuta a primeira se vários agentes não
  melhoram tempo de ciclo nem custo nas tarefas independentes; refuta o «só» se vários agentes
  melhoram também nas tarefas acopladas.
- **Tratada em**: [capítulo 6](../livro/06-como-dividir-o-trabalho/capitulo.md).

### H5 — Portão provado por teste de mutação reduz escapes

- **Métrica**: escape de portão — defeitos que chegam à linha principal com o portão verde e
  são achados depois.
- **Desenho**: braço C em duas versões — portões como escritos × os mesmos portões depois de
  provados por mutação (propriedade, fixture positiva, fixture negativa, resultado esperado),
  sobre tarefas com defeitos semeados. Complemento observacional: os escapes registrados nos
  ciclos históricos do Maestro antes e depois de cada portão ganhar prova.
- **O que a refutaria**: taxa de escape igual nas duas versões; ou queda de escape paga com
  bloqueios falsos que o protocolo classifique como inaceitáveis.
- **Tratada em**: [capítulo 10](../livro/10-quality-gates-que-provam-fatos/capitulo.md).

### H6 — Catálogo semântico reduz duplicação

- **Métrica**: componentes duplicados criados por tarefa (um objeto novo cujo papel um objeto
  existente já cumpria); no ASEG-Bench, o caso GOV-002 (componente duplicado).
- **Desenho**: braço T com e sem o passo de catálogo (REUSE / EXTEND / ALIAS / CREATE antes de
  criar objeto), mesmas tarefas, sobre um repositório com componentes pré-existentes.
- **O que a refutaria**: contagem de duplicados igual nos dois; ou redução de duplicação
  acompanhada de reuso errado (objeto reaproveitado para papel que não é o dele) em proporção
  equivalente.
- **Tratada em**: [capítulo 8](../livro/08-ddd-para-agentes/capitulo.md).

### H7 — Glossário reduz inconsistência

- **Métrica**: inconsistências de vocabulário — o mesmo conceito com nomes diferentes, ou o
  mesmo nome para conceitos diferentes, entre spec, código, testes e tela.
- **Desenho**: braço T com e sem glossário vinculante, mesmas tarefas de várias fatias sobre o
  mesmo domínio; contagem feita por verificador que não conhece o braço.
- **O que a refutaria**: inconsistências iguais nos dois braços; ou redução que só aparece nos
  termos já listados no glossário e não nos termos novos que a tarefa cria.
- **Tratada em**: [capítulo 8](../livro/08-ddd-para-agentes/capitulo.md).

### H8 — Reversibilidade permite mais autonomia

- **Métrica**: fração de ações executadas sem aprovação humana; espera humana; incidentes
  irreversíveis (dano que nenhum mecanismo desfez).
- **Desenho**: o mesmo conjunto de ações de risco, executadas com e sem reversibilidade
  engenheirada (*backup*, *dry run*, *staging*, *soft delete*), com a política de aprovação
  reclassificada conforme a reversibilidade. Caso de governança: GOV-007 (ação irreversível sem
  *rollback*).
- **O que a refutaria**: autonomia maior acompanhada de mais incidentes irreversíveis; ou
  reversibilidade que não reduz a espera humana (o humano continua aprovando tudo).
- **Tratada em**: [capítulo 11](../livro/11-risco-reversibilidade-e-autonomia/capitulo.md).

### H9 — Modelo menor basta em tarefa estruturada

- **Métrica**: aceitação na primeira passada (não-inferioridade) e custo por tarefa aceita.
- **Desenho**: fatorial — modelo menor × modelo maior, cruzado com tarefas estruturadas (spec,
  critério verificável, papel definido) × tarefas abertas; mesmo *harness*.
- **O que a refutaria**: em tarefa estruturada, perda de aceitação do modelo menor além da
  margem; ou custo por tarefa aceita que não cai (o retrabalho come a economia do preço).
- **Tratada em**: [capítulo 7](../livro/07-papeis-e-skills/capitulo.md).

### H10 — Retrospectiva que vira regra reduz recorrência

- **Métrica**: recorrência — novas ocorrências do mesmo achado (mesmo anti-padrão) por ciclo,
  antes e depois de ele virar regra versionada.
- **Desenho**: observacional, série temporal interrompida no corpus de ciclos históricos do
  Maestro (índice de decisões, catálogo de anti-padrões, relatórios de qualidade). Não há braço
  de controle; é o desenho mais fraco da agenda e assim deve ser relatado.
- **O que a refutaria**: taxa de recorrência depois da regra igual ou maior que antes; ou queda
  que já vinha acontecendo antes da regra (tendência anterior à interrupção).
- **Tratada em**: [capítulo 14](../livro/14-a-organizacao-que-aprende/capitulo.md).

## Métricas — dicionário mínimo

| Métrica | Definição operacional proposta |
|---|---|
| custo por tarefa aceita | *tokens* (ou moeda) de todas as tentativas ÷ tarefas aceitas |
| retrabalho | iterações de correção entre a primeira entrega e a aceitação |
| aceitação na primeira passada | tarefas aceitas sem correção ÷ tarefas |
| escape de portão | defeitos achados depois de um portão verde ÷ defeitos totais |
| rendimento da revisão independente | defeitos achados pelo revisor ÷ defeitos presentes |
| overhead de coordenação | *tokens*, mensagens e espera gastos entre agentes, não na tarefa |
| espera humana | tempo em que o trabalho ficou parado aguardando decisão humana |

A base também lista tempo de ciclo, *tokens* por tarefa e as métricas DORA (DevOps Research and
Assessment); entram como secundárias onde o protocolo disser.

## Estado

Nenhuma das dez foi testada com este desenho até 02/11/2026: não existem
`pesquisa/protocolo.md` nem `pesquisa/runs/`. Os capítulos que as citam as marcam como
hipótese.
