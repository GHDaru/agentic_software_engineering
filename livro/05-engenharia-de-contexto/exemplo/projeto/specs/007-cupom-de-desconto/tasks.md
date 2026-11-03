# Tasks 007 — Cupom de desconto

- [ ] **T1** — Escrever os testes de FR1–FR3 em `tests/test_cupom.py`, vermelhos. → `python -m pytest tests/test_cupom.py` falha 3.
- [ ] **T2** — Implementar validação e cálculo. Arquivos: `src/cupom.py`, `src/carrinho.py`. → os 3 testes de T1 passam.
- [ ] **T3** — Ajustar a mensagem do jeito que combinamos na conversa.
- [ ] **T4** — Renomear `desconto` para `abatimento` em todo o código. Arquivos: `src/cupom.py`, `src/carrinho.py`, `src/pagamento.py`, `src/frete.py`, `src/relatorios.py`, `src/usuarios.py`. → `grep -rn desconto src/` vazio.
- [ ] **T5** — Atualizar `CHANGELOG.md`. → docs e testes verdes.
