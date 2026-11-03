# Cobertura do inventário — prefácio

Inventário derivado (ver `inventario.md`: o arquivo não existia e `itens.json` não atribui itens
ao prefácio). O prefácio não tem as 11 seções nem exemplo executável (fora do `check-anatomia`).

Conferido em 02/11/2026: `scripts/check-claims.sh` OK (12 claims citados e registrados) e
`node publicar/build.mjs` com «links internos OK» (a saída gerada em `docs/` foi descartada).

**Portão global (rodada 3):** `scripts/check-claims.sh` sobre o repositório inteiro reporta
desvios em outras pastas (ids malformados `CLAIM-91-*`); não são do prefácio, que só pode
escrever em `livro/00-prefacio/`. Os claims do prefácio estão todos citados e registrados.

**Para o gate humano:** os 16 principais foram definidos pelo próprio autor do prefácio
(`PREF-01` a `PREF-05` saem da tarefa; os demais, de uma seleção feita por ele sobre o corpus).
A barra «100% do Maestro e da pesquisa atribuídos» não é verificável de forma independente
para este texto; confirme o recorte no gate.

## Itens principais (16/16)

| id | seção onde está coberto |
|---|---|
| PREF-01 | Para quem é este livro |
| PREF-02 | O que é o Maestro, em um parágrafo |
| PREF-03 | Como ler as quatro partes (partes, capítulos linkados, três rotas, anatomia) |
| PREF-04 | A regra de evidência |
| PREF-05 | O que este livro não é |
| LIVRO-METODO-241 | A tese (1º parágrafo); O que este livro não é («Não é manual de ferramenta») |
| LIVRO-METODO-242 | A tese, «Instrução não é enforcement» (o *hook* `guard-immutables.py`, com o limite declarado: o `Bash` não é julgado nas regras de histórico; e a tradução para qualquer *harness*: interceptação antes da ação, com poder de recusa) |
| LIVRO-METODO-243 | O ciclo 047; A tese, «Quem executa não verifica» (lista de capacidades por agente; com o limite: `Bash` em `review`/`security`) |
| GOV-020 | A tese, «Autonomia proporcional à irreversibilidade» |
| LIVRO-METODO-245 | O ciclo 047 (o `README.md` que passava); A tese, «O check mede o proxy» |
| LIVRO-METODO-246 | A tese, «Contexto é recurso finito» |
| GOV-012 | A tese, «De onde vêm essas ideias» |
| LIVRO-METODO-229 | Para quem é este livro (as duas pontas e a pergunta de origem) |
| LIVRO-METODO-230 | Para quem é este livro (o valor migra para intenção clara e verificação) |
| LIVRO-METODO-248 | A regra de evidência (quatro corpos de texto) |
| LIVRO-METODO-288 | A regra de evidência |

## Secundários usados

| id | seção |
|---|---|
| CICLOS-B-004 | O ciclo 047; Uma última coisa |
| GOV-013 a GOV-017 | De onde vêm essas ideias |
| GOV-019, GOV-021, GOV-023 | A tese |
| GOV-038 | O que é o Maestro, em um parágrafo |
| LIVRO-METODO-198 | O que é o Maestro, em um parágrafo |
