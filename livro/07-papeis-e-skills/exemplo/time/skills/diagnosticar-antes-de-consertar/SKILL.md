---
name: diagnosticar-antes-de-consertar
description: Disciplina de causa raiz. Use quando aparecer um bug, um teste falhando ou um comportamento inesperado, ANTES de propor qualquer conserto.
nasceu-de: três consertos de sintoma seguidos no mesmo módulo, registrados na retrospectiva
linha-de-base: linha-de-base.md
---

# Diagnosticar antes de consertar

## Lei de ferro

```
NENHUM CONSERTO SEM INVESTIGAÇÃO DE CAUSA RAIZ ANTES
```

Violar a letra é violar o espírito. Isto NÃO é desculpa:
- "está óbvio o que quebrou" — se estivesse, o bug não existiria; prove com evidência.
- "o conserto é pequeno, testo depois" — conserto sem causa confirmada é aposta.
- "já vi esse erro antes" — padrão parecido não é a mesma causa.

## Fases (em ordem)

1. Ler o erro inteiro. 2. Reproduzir com um teste que falha. 3. Isolar.
4. Uma hipótese explícita. 5. Provar que o teste falha por ela. 6. Só então consertar.
