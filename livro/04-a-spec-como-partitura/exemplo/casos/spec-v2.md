# Spec 001 — Frete grátis acima de um valor (v2: o comercial baixou o limite)

- **Status**: Aprovada · **Raia**: plena · **Data**: 2026-11-09
- **Origem**: pedido do time comercial; v2 depois de uma semana de dados

> **Raia**: plena. **Ambiguidade** baixa agora; **raio** pequeno; **irreversibilidade** baixa.
> Mudança de escopo volta à spec antes de virar código (Princípio I).

## Requisitos funcionais

- **FR1**: QUANDO o subtotal for maior ou igual a R$ 150,00, O SISTEMA DEVE cobrar frete de R$ 0,00.
- **FR2**: QUANDO o subtotal for menor que R$ 150,00, O SISTEMA DEVE cobrar o frete da tabela da região.
- **FR3**: SE o subtotal for negativo, ENTÃO O SISTEMA DEVE recusar o cálculo com erro.
- **FR4**: SE a região não estiver na tabela, ENTÃO O SISTEMA DEVE recusar o cálculo com erro.

## Critérios de aceite

- `python test_frete.py` → exit 0
- `python partitura.py rastreio casos/spec-v2.md test_frete.py` → exit 0
