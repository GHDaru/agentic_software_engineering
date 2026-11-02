# Spec 001 — Frete grátis acima de um valor

- **Status**: Aprovada · **Raia**: plena · **Data**: 2026-11-02
- **Origem**: pedido do time comercial (exemplo do capítulo 4 do livro)

> **Raia**: plena. **Ambiguidade** média (o que conta como subtotal? o limite inclui o valor
> exato?); **raio** pequeno (uma função, um serviço); **irreversibilidade** baixa (volta com
> um commit). Na dúvida entre leve e plena, plena.

## O que e por quê

O time comercial quer frete grátis para pedidos grandes, para subir o tíquete médio. Hoje
todo pedido paga o frete da tabela da região. O que se observa quando o problema está
resolvido: pedido acima do limite sai com frete zero, e nenhum outro pedido muda.

## Requisitos funcionais

- **FR1**: QUANDO o subtotal for maior ou igual a R$ 200,00, O SISTEMA DEVE cobrar frete de R$ 0,00.
- **FR2**: QUANDO o subtotal for menor que R$ 200,00, O SISTEMA DEVE cobrar o frete da tabela da região.
- **FR3**: SE o subtotal for negativo, ENTÃO O SISTEMA DEVE recusar o cálculo com erro.

## Fora de escopo

- Cupons de desconto e frete internacional.
- Mudar a tabela de frete por região (outra spec, outro dono).

## Critérios de aceite

- `python test_frete.py` → exit 0
- `python partitura.py rastreio spec.md test_frete.py` → exit 0

## Clarify

1. O limite inclui o valor exato (R$ 200,00)? → sim, "maior ou igual" (decisão do comercial).
