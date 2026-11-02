# Glossário do capítulo 4

| termo | definição |
|---|---|
| Spec (especificação) | Documento que diz **o quê** e **por quê** de uma mudança: o problema, o valor e o que se observa quando o problema está resolvido. Não diz o como. |
| Spec a montante / a jusante | A montante: a spec alimenta algo (teste, verificador, revisão), e mudá-la quebra o que está abaixo. A jusante: o documento descreve o código depois e pode ficar errado sem que nada aconteça. |
| Spec-Driven Development (SDD) | Desenvolvimento dirigido por especificação: a spec é a fonte de verdade e vem antes do código. |
| Easy Approach to Requirements Syntax (EARS) | Conjunto de moldes de frase para requisito (ubíquo, por evento, por estado, indesejado, opcional), cada um com condição e comportamento observáveis. Em português: QUANDO ‹condição›, O SISTEMA DEVE ‹comportamento›. Mavin et al., 2009. |
| Requisito funcional (functional requirement, FR) | Item numerado da spec (FR1, FR2…) que descreve um comportamento esperado. |
| Par comando → esperado | Forma de critério para estrutura ou invariante: um comando e o resultado que prova o critério (saída vazia, contagem, código de saída). |
| Desejo | Critério que não se prova nem se refuta ("deve ser rápido"). Não entra como requisito. |
| Raia | Quanto processo uma mudança recebe, decidido por ambiguidade × raio de impacto × irreversibilidade. Três raias: leve, plena, infra. |
| Raia leve (delta) | Mudança que cabe numa frase (erro de digitação, renomeação, log, bug óbvio): o pull request é o artefato; bug exige teste que o reproduz falhando antes; revisão e testes continuam obrigatórios. |
| Raia plena | Funcionalidade ambígua, contrato ou mudança que cruza funcionalidades: spec, plano, tarefas e relatório. |
| Raia infra | Infraestrutura, migração, implantação: sempre plena, mais portões de reversibilidade (backup, ensaio, homologação, plano de volta). |
| Raio de impacto | Quanto do sistema uma mudança alcança. |
| Regras de desempate | Na dúvida entre leve e plena, plena; infraestrutura e migração nunca são leves. |
| Delta (modelo) | Descrever a mudança pelo que muda em relação ao comportamento atual, e não por uma spec inteira. Origem: OpenSpec; no Maestro virou a raia leve. |
| Definition of Ready (DoR) | Portão humano antes da execução: critérios testáveis, ambiguidades resolvidas ou registradas, Constitution Check aprovado, `ux-design.md` se toca tela, apetite definido. A spec está pronta quando o agente executa sem adivinhar. |
| Apetite | Tempo fixo que uma aposta merece; quando acaba, corta-se escopo, não se estende prazo. |
| Clarify | Etapa e seção da spec em que a ambiguidade vira pergunta para o humano, em vez de requisito inventado. |
| Constitution Check | Tabela do plano com uma linha por princípio da constituição do Maestro, nenhuma vazia; violação é reformulada ou registrada. |
| Complexity Tracking | Registro, no plano, de uma violação de princípio inevitável: qual princípio, por que, o que a torna reversível. O portão humano decide. |
| Artefato condicional | Artefato do ciclo que só existe quando se aplica (`research.md`, `data-model.md`, `contracts/`, `checklist.md`, `ux-design.md`), mas que é sempre declarado no plano com um token como `ART:research=no` e o motivo. |
| Cauda de fechamento | As linhas finais de `tasks.md` (revisão, segurança, mutação, portão) que todo ciclo carrega, com a evidência no relatório. |
| Vendorizar | Trazer para dentro do repositório, como fonte própria e adaptada, o que se usa de uma ferramenta de terceiro, consultando o original por decisão e não por acidente. |
| Arquivo de proveniência | Registro (no Maestro, `UPSTREAM.md`) de onde veio cada peça vendorizada, em que versão, e se foi adaptada ou mantida igual. |
| Divergência declarada | Regra de vendorização: quando uma peça vendorizada contradiz o método, a contradição é resolvida por spec e registrada; nunca fica silenciosa. |
| Converge | Comando que compara o repositório real com spec, plano e tarefas e anexa tarefas para o que falta, sem reescrever as existentes. |
| Mudança de escopo silenciosa | Anti-padrão em que o agente "aproveita" para fazer o que a spec não pediu. Trabalho novo vira pergunta ou registro, não tarefa escondida. |
| Rastreio nos dois sentidos | Todo requisito tem teste, e todo teste tem requisito. Teste sem requisito é código que a spec não pediu. |
| Spec-as-source | Tese (Tessl) em que a spec é reexecutada continuamente e o código é só saída. |
| Chamado (Hindiana) | Formato de outro projeto que usa o método: `00-chamado.md`, spec em EARS e um arquivo por veredito de portão (G0…G9). No Maestro, entra como evidência importada. |
| Hook | Gancho do *harness* do agente que roda sozinho num evento (início de sessão, uso de ferramenta, fim de turno). |
