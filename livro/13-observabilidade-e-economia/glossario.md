# Glossário do capítulo 13

| termo | definição |
|---|---|
| custo por tarefa aceita | Todo o custo de um período ou ciclo (tentativas entregues, bloqueadas, reprovadas e as revisões) dividido pelo número de tarefas cujo último veredito, dado por quem não as executou, é de aprovação. A unidade econômica proposta pelo capítulo. |
| custo por tarefa executada (ingênuo) | O mesmo custo dividido pelas tarefas executadas, aceitas ou não. Mede esforço, não resultado; fica abaixo do custo por tarefa aceita sempre que algo pago não é aprovado. |
| livro de ponto de tarefas (*task ledger*) | Registro só-acréscimo, um evento por linha, de atribuição, início, fim (com tokens e custo) e veredito de cada tarefa. No Maestro, `docs/records/tarefas.jsonl`. |
| etiqueta `[[TASK]]` / `[[DONE]]` | Linha sozinha numa mensagem com que quem distribui abre uma tarefa e quem entrega a fecha; é o contrato entre a sessão gerente e as trabalhadoras. |
| tentativa · desfecho · veredito | Três campos distintos: quantas vezes a tarefa foi tentada; se a sessão conseguiu fazê-la (`delivered`, `blocked`, `failed`…); se o trabalho foi aceito por um juiz independente (`approved`, `approved_with_notes`, `rejected`). |
| retrabalho por tentativa | Custo das tentativas com número ≥ 2 da mesma tarefa. Fácil de medir; subestima quando o conserto vem como tarefa nova. |
| retrabalho por linhagem | Custo de tudo o que começou depois da primeira reprovação e antes da aceitação, inclusive tarefas de correção com nomes novos e a revisão seguinte. |
| órfão | Tarefa com início e sem fim no registro: trabalho pago e não entregue. Nunca é fechado por inferência. |
| não medido | Tentativa cujo fim não traz tokens nem custo. É contada à parte; não vale zero. |
| taxa de *cache* | Tokens de entrada lidos do *cache* de prompt divididos pelo total de entrada. Alta em sessões longas; faz "tokens por tarefa" parecer duas ordens de grandeza maior do que o texto novo. |
| custo por sessão | Contagem de tokens por sessão (e por minuto), lida dos transcritos de forma incremental; só contagens, nunca conteúdo. Mais grossa que o livro de ponto, mas não depende de etiqueta. |
| consumo por agente | O grão mais fino do custo por sessão: tokens por agente, não só por sessão ou modelo. |
| limite de orçamento · emissor do aviso | Teto de consumo declarado de uma sessão ou projeto, lido como "declarar e avisar"; o emissor é quem compara o consumo medido com o limiar e enfileira o aviso. O corte (recusar, suspender) é decisão separada. |
| projeção (telemetria como projeção) | Exportar o registro para outro formato (por exemplo, OpenTelemetry) como leitura derivada, sem que o domínio dependa do exportador. Desligar a projeção não muda nada no registro. |
| convenções semânticas GenAI | Nomes de atributos do OpenTelemetry para IA generativa (`gen_ai.request.model`, `gen_ai.usage.input_tokens`…), ainda em desenvolvimento. |
| minimização (lista de permissão) | Só sai do registro, ou da exportação, o que está explicitamente permitido; texto livre, conteúdo de mensagem e identificadores de sessão ficam para trás. Aplicação do princípio da necessidade da LGPD. |
| YAGNI com gatilho | Decisão de não construir algo agora registrada junto com a condição observável que a reabre. |
