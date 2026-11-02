# Glossário do apêndice B — ASEG-Bench

| termo | definição |
|---|---|
| ASEG-Bench | Benchmark de governança para engenharia de software com agentes: dez casos (GOV-001 a GOV-010), cada um com oráculo determinístico. Nome de trabalho da agenda de pesquisa; a expansão "governança para *Agentic Software Engineering*" é adotada por este apêndice, não fixada pela agenda. |
| benchmark de capacidade | Conjunto de tarefas cujo veredito é "o agente resolveu?" (por exemplo, os testes da tarefa passam). SWE-bench e SWE-Bench Pro são exemplos. |
| benchmark de governança | Conjunto de tarefas cujo veredito é "o agente resolveu sem violar a regra do time?". Pressupõe capacidade e mede o custo de governança da solução. |
| caso | Unidade do benchmark: eixo, hipótese, ablação, origem e sua classe, cenário, gatilho, comportamento esperado, oráculo, limite declarado, contrato de declaração e fixtures. |
| gatilho | O pedido entregue ao agente, nas palavras de um humano, em geral com a pressão que levou à violação original. |
| oráculo | Função determinística que julga o rastro de uma execução e devolve a lista de violações (vazia = conforme). Roda sem modelo no laço. |
| rastro | O que sobra de uma execução, em formato neutro de ferramenta: arquivos antes (`base`) e depois (`final`) e a linha do tempo ordenada de commits, chamadas, aprovações e resposta. |
| adaptador de rastro | Conversor do log de um harness específico para o rastro neutro; é onde mora a dependência de ferramenta. O pacote traz um mínimo para o Claude Code e um validador que reencena as fixtures como execuções reais. |
| fixture positiva | Rastro que cumpre a governança do caso; o oráculo tem de aprová-lo. |
| fixture negativa | Rastro que encena a violação da família do caso (observada ou de risco, conforme a classe da origem); o oráculo tem de reprová-lo, inteiro e só pelo estado. Carrega fatos, nunca o veredito. |
| autoteste | Execução do oráculo contra as próprias fixtures: prova que cada oráculo já foi visto reprovando (a "segunda lei" aplicada ao benchmark). |
| eixo | A capacidade de governança que o caso afirma separar. |
| ablação | O mesmo agente menos exatamente a capacidade do eixo. Se o ablado passa, o caso não discrimina e sai da comparação. |
| mutante | Versão deliberadamente estragada de um código (GOV-005) ou de uma saída (GOV-006) que um teste ou gate correto tem de rejeitar. |
| canário | Cadeia única plantada numa instrução hostil (GOV-010); se aparece em ação ou escrita do agente, a instrução foi obedecida. |
| MUST-FIND / MUST-NOT-CLAIM | No corpus de avaliação do Maestro, o que uma resposta certa tem de achar e o que uma resposta errada diria. Origem do par positiva/negativa do ASEG-Bench. |
| níveis A, B, C e tratamento | Desenho de comparação da agenda: A só prompt, B com spec, C com spec e gates, tratamento com o método completo. |
| contrato de declaração | Bloco de cada caso, anexado ao gatilho igual em todos os níveis, que diz o formato em que o agente registra o que fez (caminhos, linhas como `Aprovado por:`), nunca a regra medida. Existe para que o nível sem método não seja reprovado por desconhecer um formato. |
| violação de estado / de declaração | Classes das violações que um oráculo emite: de estado vem dos arquivos e da linha do tempo; de declaração depende do formato do contrato e leva o prefixo `[declaração]`. |
| veredito só de estado | Veredito com as violações de declaração descartadas (`--so-estado`); vale mesmo para execuções que não receberam o contrato. |
| vazamento do contrato | Quando o contrato ensina a regra em vez de só o formato. Pego em parte por `contrato_nao_diz` (termos da regra) e, no resto, medido rodando o nível A com e sem o contrato. |
| aprovação vazia | Veredito "conforme" de uma execução que não fez nada: nada escrito, nada violado. Por isso cada veredito leva ao lado a coluna "tarefa resolvida". |
| classe da origem | *Observada* (um registro datado mostra uma falha da família do caso) ou *de risco* (origem em leitura de código ou referência externa, relatada em separado). |
| operador do experimento | O humano que conduz a execução e dá as aprovações, com o protocolo `APROVO <alvo>`, igual em todos os níveis. |
