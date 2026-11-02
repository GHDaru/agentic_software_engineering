# publicar/ — o motor do site do livro

Gera o site estático do livro em `../docs/`, servido pelo GitHub Pages em modo
**Deploy from a branch → `main`, pasta `/docs`**. Adaptado do motor do Maestro
(`../maestro-handbook/publicar/`): markdown-it como biblioteca, o motor é nosso.

## Uso

```bash
cd publicar
npm install
npm run build        # = node build.mjs ; regera ../docs/
```

Depois do build, faça commit de `docs/` junto com o texto — o Pages publica o que está na branch.

## O que entra

| Fonte | Página |
|---|---|
| `livro/sumario.yaml` | a ordem (fonte única), a capa e a lateral |
| `livro/00-prefacio/capitulo.md` | `00-prefacio.html` |
| `livro/NN-slug/capitulo.md` | `NN-slug.html` |
| `livro/NN-slug/exemplo/README.md` (se existir) | `NN-slug-exemplo.html`, filha do capítulo |
| `livro/apendices/x-slug/capitulo.md` | `apendice-x-slug.html` |
| `livro/glossario.md` (se existir) | `glossario.html` |
| `pesquisa/CLAIMS.md` (se existir) | `evidencias.html` |

Capítulo do sumário ainda sem `capitulo.md` aparece na capa e na lateral como **em escrita**, sem link.

## Links

- Para um `.md` publicado → a página `.html` (com a âncora, que tem de existir).
- Para qualquer outro arquivo ou pasta do repositório (`maestro-handbook/`, `claims.md`, scripts do
  exemplo) → `https://github.com/GHDaru/agentic_software_engineering/blob/main/...` (`tree/` para pasta).
- **Reprova o build** (e `docs/` não é tocado): alvo inexistente (com caixa exata — o Windows
  perdoa, o Pages não), link que sai do repositório, âncora inexistente numa página publicada,
  imagem ausente, slug repetido, e chave desconhecida ou vazia no `sumario.yaml` (título com
  vírgula sem aspas dentro de `{...}`).

Âncoras seguem o padrão do GitHub (acento mantido), então `#evidência` funciona no GitHub e no site.

## Portões irmãos (`../scripts/`)

`check-sumario.sh` (sumário × pastas), `check-anatomia.sh` (as 11 seções do guia editorial),
`check-claims.sh` (claims citados × registrados).
