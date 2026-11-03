# Plano — aviso de estouro do prazo de resposta

## Modelo de domínio

- `DOM:aggregate=Ticket` — o estouro é um fato do chamado; quem decide se estourou é a raiz.
- `DOM:invariants=estouro_calculado_pelo_chamado=domain | alerta_sai_uma_vez=edge(a deduplicação usa a chave da fila de saída, que mora no adaptador de mensagens)`
- `DOM:glossary=changed` — entra "Alerta de estouro" (atendimento), com definição no modelo.
- `DOM:ports=none` — o aviso usa a porta de mensagens que já existe.
