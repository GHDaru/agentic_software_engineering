# Glossário do apêndice A

| termo | definição |
|---|---|
| Maestro | Método de engenharia de software em que um humano rege vários agentes de IA: a spec é a fonte de verdade, os agentes executam, o humano decide, aprova e verifica. Objeto de estudo deste livro. |
| Elemento `[n]` | Uma das 12 peças do modelo operacional do Maestro, rotuladas `[1]`–`[12]`; o rótulo não coincide com o número do capítulo do handbook que a trata. |
| Camada | Agrupamento dos elementos pela pergunta que respondem: fundamento (por quê), mecânica (como flui), estrutura (quem e quando), qualidade (o que se produz e como se prova), governança (como evolui). |
| Steward | O humano que decide o quê e o porquê de uma mudança e é dono dos gates indelegáveis. |
| Raia (de trabalho) | Quanto processo uma mudança recebe: leve (o pull request é o artefato), plena (spec completa) ou infra (plena mais portões de reversibilidade). |
| Raia (de BPMN) | Faixa horizontal de um diagrama de processo (*swimlane*) que agrupa os passos de um mesmo executor. Não confundir com a raia de trabalho. |
| Business Process Model and Notation (BPMN) | Notação padronizada pelo Object Management Group (OMG), versão 2.0.2, para desenhar processos com raias, tarefas, decisões e artefatos. |
| Losango (gate) | Ponto do desenho em que o fluxo para até uma decisão: humano (ouro, indelegável) ou mecânico (verde, a DoD). |
| Retrato | Resumo ou diagrama que descreve o método numa versão datada; envelhece quando o repositório anda e o retrato não. |
| Planta gerada | Diagrama produzido por ferramenta (no Maestro, o Archify) a partir de um arquivo JSON versionado, que registra a revisão de onde saiu. |
| Archify | Gerador de diagramas interativos a partir de JSON (raias, fases, nós, arestas); versão 3.2.0 na peça 07 do Maestro. |
| Proposta não vigente | Peça que descreve um processo desejado, não o em vigor, e se declara assim no título, no primeiro parágrafo e no índice. |
| Trilha (do site) | Um dos cinco caminhos de leitura do site do Maestro, cada um de um tipo de documentação: Jornada, Capítulos, Receitas, Referência, Bastidores. |
| Cadência de estudo | Profundidades de leitura com custo de tempo declarado: Entender (~20 min), Aprender (~2 h), Aplicar (~1 dia), Aprofundar (contínuo). |
| Medir a frase em vez do fato | Defeito de verificação em que se confere o texto de uma afirmação, não o estado do disco que ela descreve. |
| Axioma, teorema, corolário | A camada de derivação do Maestro (`docs/governance/axioms.md`): cinco verdades assumidas (A1–A5), sete teoremas derivados delas com evidência no repositório (T1–T7) e treze corolários (C1–C13), de onde saem as regras do dia a dia. |
| Catálogo do ecossistema | Registro do Maestro sobre o que avaliou de terceiros: uma ficha datada por ideia e um índice append-only com o veredito corrente (adotar, absorver, observar, descartar). |
| Easy Approach to Requirements Syntax (EARS) | Formato de requisito `QUANDO <condição> O SISTEMA DEVE <comportamento>`, absorvido pelo Maestro a partir do Kiro. |
| Passo zero | A escolha da raia de trabalho antes de especificar: quanto processo a mudança merece, por ambiguidade × raio de impacto × irreversibilidade. |
