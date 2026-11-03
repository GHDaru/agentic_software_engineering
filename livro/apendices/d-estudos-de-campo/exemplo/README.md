# Exemplo do apêndice D — o portão do catálogo do ecossistema

Um portão mínimo, em Python 3 sem dependências, que confere se todo julgamento sobre trabalho
alheio está **ancorado**: fonte com licença, card datado com as sete dimensões, estado corrente
como última linha de um índice append-only, absorção com destino que é arquivo e contém a
prova, observação com gatilho. Inspirado no `check-ecosystem.sh` do Maestro
(`maestro@19823c2:scripts/check-ecosystem.sh`), reescrito do zero.

A fixture reproduz, em miniatura, o dia em que o catálogo do Maestro nasceu (ciclo 047,
10/08/2026): duas ideias registradas como absorvidas no ciclo 007 com destino condicional
(`scripts/`, `docs/standards/`), e uma biblioteca de licença CC BY-NC-SA registrada como
"observar" sem gatilho.

## Arquivos

```text
exemplo/
├── checa_catalogo.py              o portão
└── catalogo/
    ├── fontes.md                  4 fontes, com licença e data
    ├── ideias/                    5 cards imutáveis, um por ideia
    ├── repo/                      o "repositório" onde os destinos têm de existir
    ├── estado-1-migracao.jsonl    o índice como a migração o escreveu (vermelho)
    ├── estado-2-corrigido.jsonl   o mesmo + 3 linhas novas datadas (verde)
    └── estado-3-retrodatado.jsonl o atalho: reescrever as linhas antigas (verde sozinho!)
```

## Como rodar

Da pasta `exemplo/` (no Windows, `python`; em Linux/macOS, `python3`):

```bash
python checa_catalogo.py catalogo --estado catalogo/estado-1-migracao.jsonl
python checa_catalogo.py catalogo --estado catalogo/estado-2-corrigido.jsonl --anterior catalogo/estado-1-migracao.jsonl
python checa_catalogo.py catalogo --estado catalogo/estado-3-retrodatado.jsonl
python checa_catalogo.py catalogo --estado catalogo/estado-3-retrodatado.jsonl --anterior catalogo/estado-1-migracao.jsonl
```

## Saída esperada

Medida em 02/11/2026, Python 3.12.10, Windows 11 (Git Bash).

**1. O índice da migração — saída 1, três achados:**

```text
── catálogo: 4 fontes · 5 cards · 5 linhas de estado
   estado corrente: absorver 4 · observar 1
  ✗ worktree-por-task: 'absorver' com destino 'scripts/' que é pasta, não arquivo
  ✗ standards-por-camada: 'absorver' com destino 'docs/standards/' que não existe no disco
  ✗ skills-de-gestao-de-produto: 'observar' sem gatilho — esquecer com cerimônia
✗ 3 achado(s): há julgamento sem âncora.
```

**2. A correção por acréscimo — saída 0:**

```text
── catálogo: 4 fontes · 5 cards · 8 linhas de estado
   estado corrente: absorver 2 · descartar 1 · observar 2
✓ todo julgamento está ancorado.
```

**3. O atalho da reescrita, sem o índice anterior — saída 0.** O portão de âncora sozinho não
vê que a história foi reescrita: as linhas de 2026-07-30 agora dizem `observar`, como se o
ciclo 007 tivesse decidido isso. Foi exatamente o defeito que a revisão independente do ciclo
047 achou no próprio ciclo 047.

```text
── catálogo: 4 fontes · 5 cards · 5 linhas de estado
   estado corrente: absorver 2 · descartar 1 · observar 2
✓ todo julgamento está ancorado.
```

**4. O mesmo atalho, com o índice anterior — saída 1:**

```text
── catálogo: 4 fontes · 5 cards · 5 linhas de estado
   estado corrente: absorver 2 · descartar 1 · observar 2
  ✗ append-only: a linha 2 de estado-1-migracao.jsonl foi reescrita ou apagada
✗ 1 achado(s): há julgamento sem âncora.
```

## Veja o portão acusar (mutação)

Acrescente ao fim de uma cópia de `estado-2-corrigido.jsonl` uma absorção que aponta para um
arquivo que existe, mas não contém a ideia, e rode com `--anterior` apontando o original:

```bash
cp catalogo/estado-2-corrigido.jsonl /tmp/mut.jsonl
echo '{"ideia": "standards-por-camada", "estado": "absorver", "data": "2026-11-02", "destino": "docs/README.md", "gatilho": "", "ciclo": "999"}' >> /tmp/mut.jsonl
python checa_catalogo.py catalogo --estado /tmp/mut.jsonl --anterior catalogo/estado-2-corrigido.jsonl
```

Esperado (saída 1):

```text
  ✗ standards-por-camada: 'absorver' em 'docs/README.md' sem 'prova' (texto que tem de estar lá)
```

É a mutação que a revisão do ciclo 047 usou para reprovar a primeira versão do portão do
Maestro: sem o campo `prova`, apontar para um `README.md` satisfazia qualquer absorção.

## O que o portão não mede

Se o veredito é sábio; se a descrição da fonte é verdadeira; se um gatilho já disparou sem que
ninguém acrescentasse a linha. O apêndice mostra um caso real de cada um ("O que o portão não
vê").
