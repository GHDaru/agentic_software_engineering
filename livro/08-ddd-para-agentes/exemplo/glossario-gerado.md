<!-- GERADO de modelo.json · sha256=4c82337ada86f3971847582a80c8e1c5def176096d8b401f8bfb42e55dedea93 · não edite à mão: edite o modelo e regere -->
# Glossário — central de atendimento

| termo de tela | identificador | contexto | definição |
|---|---|---|---|
| Chamado | `Ticket` | atendimento | Pedido de ajuda de um cliente; a raiz do agregado de atendimento. |
| Cliente | `Customer` | atendimento | Quem abre o chamado e recebe a resposta. |
| Fila de atendimento | `ServiceQueue` | atendimento | Chamados à espera de um atendente, em ordem de prazo de resposta. |
| Prazo de resposta | `responseDueAt` | atendimento | Quando o chamado precisa da primeira resposta, pelo SLA contratado. |
| Fatura | `Invoice` | faturamento | Cobrança mensal do contrato do cliente. |
| Prazo de pagamento | `paymentDueAt` | faturamento | Data limite para pagar a fatura sem multa. |
| Fila de saída | `Outbox` | mensageria | Mensagens gravadas e ainda não entregues ao canal. |
| Mensagem | `Message` | mensageria | Texto enviado ao cliente por um canal; imutável depois de enviado. |

Nunca escrever nu:

- **fila** — sempre qualificada: fila de atendimento ou fila de saída
- **prazo** — sempre qualificado: prazo de resposta ou prazo de pagamento

Siglas:

- **API** — Application Programming Interface
- **SLA** — Service Level Agreement
