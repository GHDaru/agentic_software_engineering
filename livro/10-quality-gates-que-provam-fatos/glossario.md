# Glossário do capítulo 10

| termo | definição |
|---|---|
| *quality gate* (portão) | Verificação automática ou humana que decide se um trabalho avança; no capítulo, quase sempre um script que sai com código zero (verde) ou diferente de zero (vermelho). |
| proxy (check que mede o proxy) | Algo que costuma andar junto com o fato que o portão deveria medir — a palavra, a linha, a existência do arquivo — e que pode estar presente com o fato ausente. Anti-padrão 13 do Maestro. |
| decoração | Portão que fica verde em pelo menos um mundo quebrado de propósito, ou vermelho num mundo certo: tem a forma de verificação sem proteger nada. |
| segunda lei | "Um check que você nunca viu acusar não é um check — é uma esperança": antes de confiar num portão, quebre o mundo de propósito e veja o vermelho (corolário C2). |
| prova por mutação de portão | Procedimento que testa o portão mutando o mundo que ele inspeciona: propriedade, fixture positiva, fixtures negativas, fixtures legítimas e resultado esperado. |
| fixture positiva | Entrada que representa o mundo certo; o portão tem de passar. |
| fixture negativa (mutação) | Entrada que representa o mundo quebrado de propósito; o portão tem de reprovar. Mutação que passa "sobreviveu". |
| fixture legítima | Entrada que representa o mundo certo de forma incômoda (a palavra proibida no meio de uma frase verdadeira, duas fontes numa linha); o portão tem de passar, senão é falso vermelho. |
| falso vermelho | Reprovação de um mundo certo. Repetido, ensina o time a ignorar o portão. |
| família (de um portão) | Conjunto de formatos, atributos, canais ou campos que um portão precisa cobrir para cobrir algum (corolário C5; anti-padrões 16 e 23). |
| check negativo | Invariante escrito como busca pelo que não pode existir, com resultado esperado vazio. |
| par (comando, esperado) | Forma de critério estrutural: o comando e o resultado que prova o critério (`vazio`, `= N`, `exit 0`). |
| Easy Approach to Requirements Syntax (EARS) | Sintaxe controlada de requisito: `QUANDO <condição> O SISTEMA DEVE <comportamento observável>`; vira teste quase um para um. |
| gate humano | Critério que não se automatiza e é declarado como tal, com dono — o contrário de critério vago. |
| linha de base registrada | Critério para saída não comparável por igualdade (teorema T7): entrada fixa, asserções que discriminam (incluindo o que uma resposta errada afirmaria) e observação datada. |
| cauda de fechamento (*closing tail*) | Os quatro passos finais de um ciclo no Maestro (`TAIL:review`, `TAIL:security`, `TAIL:mutation`, `TAIL:gate`), escritos como tokens no `tasks.md`, com evidência no `qa-report.md`. |
| `TAIL:mutation` | Passo da cauda que exige que todo portão criado ou alterado no ciclo tenha sido visto reprovando; a dispensa é lida do diff. |
| portão bloqueante / consultivo | Bloqueante impede o merge quando vermelho; consultivo só avisa. Portão que fica vermelho durante todo trabalho em andamento é consultivo na CI e bloqueante no ponto em que o trabalho termina. |
| válvula de escape declarada | Forma registrada de dispensar um portão (uma label, um `n/a:` com motivo), que mantém o desvio auditável. |
| piso | Primeiro ciclo a partir do qual uma regra nova vale; abaixo dele, a dívida fica declarada e não é rejulgada. |
| morte silenciosa | Portão que termina sem medir e é lido como verde — por exemplo, `grep -q` no fim de um pipe sob `pipefail` (anti-padrão 21). |
| veredito conferível | Evidência de gate com cabeçalho verificável por máquina: gate, objeto @ hash, veredito, autor, data. |
| jornada viva | Documento de jornada de tela com capturas geradas do build real por script versionado e heurística datada, no mesmo pull request. |
| escape de gate | Defeito achado depois do merge com o portão verde no momento do merge; métrica de saúde dos portões. |
| aceitação na primeira passada | Fração de entregas aprovadas pela revisão independente sem reprovação. |
| teste de caracterização | Teste que registra o comportamento atual de código existente antes de alterá-lo. |
