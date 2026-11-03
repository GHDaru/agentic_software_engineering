---
name: criterio-verificavel
description: Transforma critério de aceite vago em verificação executável (grep, ls, teste). Use quando escrever ou revisar um critério de aceite, uma spec ou um plano.
nasceu-de: os mesmos checks reescritos à mão em três ciclos seguidos
linha-de-base: linha-de-base.md
---

# Critério verificável

## Lei de ferro

```
NENHUM CRITÉRIO DE ACEITE SEM O COMANDO QUE O PROVA
```

Violar a letra é violar o espírito. Isto NÃO é desculpa:
- "esse critério é qualitativo" — então descreva a evidência que um humano confere, com data.
- "o comando vem depois" — critério sem comando vira opinião no fechamento.

## Passos

1. Para cada critério, escreva o comando e a saída esperada.
2. Rode o comando contra uma versão quebrada e veja-o reclamar.
3. Só então aceite o critério.
