# ADR 0003 — Cupom não se acumula com outro cupom

- **Status**: Aceito · **Data**: 2026-09-01

## Contexto

Campanhas sobrepostas geravam descontos somados acima da margem.

## Decisão

Um carrinho tem no máximo um cupom; aplicar outro substitui o primeiro.

## Alternativas

Somar com teto: rejeitada — o teto vira mais uma regra a manter por campanha.
