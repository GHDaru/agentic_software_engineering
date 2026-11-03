# Tasks 007 — Cupom de desconto (com a cauda como token)

- [ ] **T1** — Escrever os testes de FR1–FR3 em `tests/test_cupom.py`, vermelhos. → `python -m pytest tests/test_cupom.py` falha 3.
- [ ] **T2** — Implementar validação e cálculo. Arquivos: `src/cupom.py`, `src/carrinho.py`. → os 3 testes de T1 passam.
- [ ] **T3** — Mensagem de cupom vencido com a data em dd/mm/aaaa (FR2). Arquivos: `src/cupom.py`. → teste `test_fr2_mensagem_com_data` passa.
- [ ] **T5** — Atualizar `CHANGELOG.md`. → docs e testes verdes.

## Fechamento (obrigatório, uma linha cada, nunca apagar)

- [ ] TAIL:review — revisão independente em contexto fresco (skill `revisar-diff`).
- [ ] TAIL:security — o cupom é entrada do usuário: validação e limites.
- [ ] TAIL:gate — gate humano antes do merge.
