# Exemplo do capítulo 9 — portões de arquitetura provados por mutação

Um projeto de brinquedo com dois leitores (um servidor em camadas, lido por máquina, e um livro
publicado, lido por gente) e sete portões de arquitetura. Um harness prova cada portão: ele tem de
ficar verde no projeto como está e nas fixtures legítimas, e vermelho em cada mutação da sua
família. Portão que deixa mutação viva, ou que reprova o mundo certo, é **decoração**.

| Arquivo | O que é |
|---|---|
| `projeto/` | o projeto de brinquedo: `fronteira.json` (os dois domínios e o caminho compartilhado), `publicar/sumario.json` (dois canais de publicação: itens e materiais), `servidor/` (domínio, portas, adaptadores) |
| `portoes.py` | os sete portões, funções que recebem a raiz do projeto e devolvem a lista de violações |
| `provar.py` | o harness: copia o projeto para um diretório temporário, aplica cada mutação e roda todos os portões |

## Os portões

| Portão | Forma | Inspirado em |
|---|---|---|
| `fronteira/um-canal` | ingênuo: lê só `itens` | `check-boundary.sh` antes do ciclo 054 |
| `fronteira/dois-canais` | ingênuo: lê `itens` e `materiais` pelo nome | a correção pontual do ciclo 054 |
| `fronteira/fato` | lê todo campo `arquivo` do sumário, em qualquer canal | uma resposta possível ao anti-padrão 23 (não é a forma do Maestro) |
| `dependencias/texto` | ingênuo: procura a linha `import <módulo de I/O>` | a busca por texto que o capítulo 10 chama de proxy |
| `dependencias/fato` | lê a árvore sintática; domínio não importa I/O, porta nem adaptador; porta não importa adaptador | `painel/tests/test_import_fronteira.py` e `test_esqueleto.py` |
| `registro/fato` | lê a árvore sintática do adaptador; recusa `w`, `x`, `r+`, modo não constante, `truncate()` e `seek()` | `TestF14AbreEmAppend` e o ADR 0027 |
| `portas/fato` | toda porta tem dois adaptadores, contando o falso | a síntese das bancas do ciclo 076 (A4) |

As três invariantes da fronteira são as do Maestro: todo arquivo com exatamente um dono (prefixo
mais longo, empate é falha); todo caminho compartilhado com dono no toolkit; toda página publicada
vinda do guia ou de caminho compartilhado.

## Como rodar

Requisito: Python 3.8 ou mais novo, sem dependência externa. No Git Bash do Windows, onde
`python3` pode ser um atalho vazio, use `python`.

```bash
cd livro/09-arquitetura-que-se-defende/exemplo
python3 provar.py
```

Leva poucos segundos no Linux; no Windows, com antivírus varrendo o diretório temporário, cerca de
um minuto (são dezenove cópias do projeto: a base, três legítimas e quinze mutações).

## Saída esperada

**Sai com código 0**, porque o resultado bate com o que o capítulo afirma: os portões "fato" são
portões e os ingênuos são decoração.

```text
fronteira/um-canal     mutações mortas 4/6  →  DECORAÇÃO
    ✗ mutação sobreviveu: 'arquivo do toolkit publicado pelo 2º canal (materiais)'
    ✗ mutação sobreviveu: 'arquivo do toolkit publicado por um 3º canal (anexos)'
fronteira/dois-canais  mutações mortas 5/6  →  DECORAÇÃO
    ✗ mutação sobreviveu: 'arquivo do toolkit publicado por um 3º canal (anexos)'
fronteira/fato         mutações mortas 6/6  →  PORTÃO
dependencias/texto     mutações mortas 1/5  →  DECORAÇÃO
    ✗ mutação sobreviveu: 'domínio faz from sqlite3 import connect'
    ✗ mutação sobreviveu: 'domínio importa o adaptador por import relativo'
    ✗ mutação sobreviveu: 'domínio usa __import__('sqlite3')'
    ✗ mutação sobreviveu: 'porta importa o adaptador'
dependencias/fato      mutações mortas 5/5  →  PORTÃO
registro/fato          mutações mortas 3/3  →  PORTÃO
portas/fato            mutações mortas 1/1  →  PORTÃO
resumo: 7 portões provados, 4 portão(ões), 3 decoração(ões)
✓ o resultado bate com o capítulo
```

Saída conferida em 02/11/2026, Python 3.12, Windows 11 (Git Bash).

## Exercícios

1. **A porta nova (anti-padrão 23).** Acrescente ao `projeto/publicar/sumario.json` um canal
   `"destaques": [{"arquivo": "scripts/interno.html"}]` e rode `python3 -c "import portoes;
   print(portoes.fronteira_dois_canais('projeto')); print(portoes.fronteira('projeto'))"`. O
   primeiro devolve lista vazia (verde); o segundo acusa. Desfaça a edição depois.
2. **O falso senso de segurança.** Em `provar.py`, acrescente à lista `MUTACOES` uma mutação de
   dependências que insere `import importlib` e `_b = importlib.import_module("sqlite3")` no
   domínio. Rode: `dependencias/fato` passa a ser DECORAÇÃO. O portão testa o que foi codificado,
   não o que foi esquecido. Corrija `portoes._importados` para reconhecer a chamada e veja o
   portão voltar.
3. **O portão mais estrito que a regra.** Em `portoes.so_acrescenta`, troque a condição para
   reprovar qualquer modo com `+`. A fixture legítima `"a+"` vira falso vermelho e o portão vira
   DECORAÇÃO, embora mate todas as mutações.
