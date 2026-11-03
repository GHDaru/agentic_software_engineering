# Glossário do capítulo 15

| termo | definição |
|---|---|
| avaliação (*eval*) | Linha de base de julgamento: entrada fixa, asserções que discriminam (inclusive o lado negativo) e observação datada, presa ao alvo que mede. Não é teste (igualdade) nem benchmark (sistemas entre si). |
| linha de base (*baseline*) | Registro datado de uma execução do caso contra o alvo, com o commit do alvo, o veredito, a ablação e a premissa conferida. Envelhece quando o alvo muda. |
| alvo | O arquivo de instrução avaliado (agente, skill, prompt), nomeado por caminho no caso. |
| eixo (`Axis`) | A capacidade que o caso diz separar; é a linha que se remove para produzir o alvo ablado. |
| alvo ablado / ablação | O mesmo alvo sem a instrução que o eixo nomeia, com todo o resto igual; funciona como grupo de controle. O caso só vale se o ablado reprovar. Se a ablação remover mais de uma coisa (no caso 001 real do Maestro: a instrução **e** o plano da entrada), o vermelho não se atribui só à instrução. |
| lado negativo (`MUST-NOT-CLAIM`) | Asserção sobre o que uma resposta errada, porém plausível, afirmaria; é o que impede uma resposta prolixa de passar. |
| primeira reprovação (`First-red`) | Registro de que o caso já foi visto reprovando; enquanto "pending", o portão fica vermelho. |
| premissa conferida (`Premise-checked`) | Registro de como a premissa da fixture foi reproduzida antes da execução. |
| fixture | Entrada fixa do caso; deve trazer fatos e nenhuma conclusão que o alvo deveria tirar. |
| aposentadoria com motivo | Retirar um caso que não discrimina deixando-o visível com `Retired-because:`; aposentar sem motivo equivale a apagar. |
| conformidade | Primeira camada de validação: o método foi aplicado e sobreviveu nos artefatos? Responde-se com comando. |
| regressão de julgamento | Segunda camada: os agentes continuam julgando como julgavam quando a linha de base foi registrada? |
| efeito | Terceira camada: aplicar o método produz resultado melhor do que não aplicá-lo? Só se responde com experimento comparativo. |
| cauda de fechamento (`TAIL:`) | Itens de fechamento do ciclo (revisão, segurança, mutação, gate) que precisam de evidência no relatório de qualidade. |
| declaração de artefato (`ART:`) | Token legível por máquina no plano que declara cada artefato condicional como `yes` ou `no` com motivo. |
| crítico às cegas / *gauntlet* | Avaliador em contexto fresco que compara versões sem saber qual é qual; usado como barra de produto no ciclo 074. |
| *Backward Design* | Planejamento de trás para frente (Wiggins e McTighe): objetivos, depois verificação, só então conteúdo. |
| claim | Afirmação quantitativa com id, estado (medido, observado, hipótese) e evidência reproduzível. |
| *LLM-as-judge* | Padrão em que um modelo de linguagem de grande porte (LLM, de *large language model*) avalia a saída de outro modelo. |
| FR (FR1, FR2) | Requisito funcional (*functional requirement*), numerado na spec. |
