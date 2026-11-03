# Spec 007 — Cupom de desconto no carrinho

- **Raia**: plena · ambiguidade média, raio contido ao carrinho, reversível por flag.

## O quê e por quê

O comercial quer cupons de desconto percentual no carrinho, para campanhas de data marcada.

## Invariantes (o que nenhuma tarefa pode quebrar)

- O total do carrinho nunca fica negativo.
- Cupom não se acumula com outro cupom (ADR 0003).
- O desconto é calculado sobre o subtotal, antes do frete.

## Requisitos

- **FR1**: QUANDO um cupom válido é aplicado, O SISTEMA DEVE reduzir o subtotal pelo percentual do cupom.
- **FR2**: SE o cupom estiver vencido, ENTÃO O SISTEMA DEVE recusá-lo e dizer a data de vencimento.
- **FR3**: QUANDO um segundo cupom é aplicado, O SISTEMA DEVE substituir o primeiro, nunca somar.

## Fechamento do ciclo

Antes do merge: revisão independente em contexto fresco, revisão de segurança (o cupom é
entrada do usuário) e gate humano.
