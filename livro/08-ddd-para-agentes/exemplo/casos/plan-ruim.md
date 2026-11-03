# Plano — aviso de estouro do prazo de resposta (versão com três defeitos)

## Modelo de domínio

- `DOM:aggregate=Ticket`
- `DOM:invariants=estouro_calculado_pelo_chamado=domain | alerta_sai_uma_vez=edge`
- `DOM:glossary=changed` — entra "Alerta de estouro" (atendimento).
