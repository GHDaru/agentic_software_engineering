# Exemplo do capítulo 10 — provar um portão por mutação

Três propriedades, dois portões para cada uma: um mede o **proxy** (a forma que um portão
real do Maestro tinha antes de alguém o quebrar de propósito), o outro mede o **fato**. Um
harness pequeno põe os seis à prova com fixtures — e separa portão de decoração.

| Arquivo | O que é |
|---|---|
| `portoes.py` | os seis portões, funções puras (texto → verde/vermelho) |
| `casos.json` | para cada propriedade: fixture positiva, fixtures legítimas e mutações |
| `provar.py` | o harness: roda cada portão contra cada fixture e dá o veredito |

Cada propriedade em `casos.json` segue a forma de *gate mutation* estruturado: **propriedade**,
**fixture positiva** (o mundo certo), **fixtures negativas** (o mundo quebrado de propósito) e
**resultado esperado** (verde na positiva, vermelho em cada negativa). A fixture *legítima* é a
quarta peça que o capítulo defende: um mundo certo de forma incômoda, que o portão não pode
reprovar — senão ele vira falso vermelho, e portão de falso vermelho se aprende a ignorar.

## Como rodar

Requisito: Python 3.8 ou mais novo, sem dependência externa. No Git Bash do Windows, onde
`python3` pode ser um atalho vazio, use `python`.

```bash
cd livro/10-quality-gates-que-provam-fatos/exemplo
python3 provar.py               # os seis portões
python3 provar.py --so fato     # só os que medem o fato
```

## Saída esperada

`python3 provar.py` — **sai com código 1**, e é esse o ponto: três dos seis portões são decoração.

```text
P1 — a evidência de TAIL:review registra uma revisão que aconteceu
  P1/ingenua  mutações mortas 1/8  →  DECORAÇÃO
      ✗ mutação sobreviveu: 'pendente.'
      ✗ mutação sobreviveu: 'não executada'
      ✗ mutação sobreviveu: 'ainda não executada'
      ✗ mutação sobreviveu: '(pendente)'
      ✗ mutação sobreviveu: '> pendente'
      ✗ mutação sobreviveu: 'NÃO EXECUTADA'
      ✗ mutação sobreviveu: 'token fora da linha da cauda'
  P1/fato     mutações mortas 8/8  →  PORTÃO
P2 — a página declara o número certo de fontes
  P2/ingenua  mutações mortas 2/3  →  DECORAÇÃO
      ✗ falso vermelho em 'duas fontes na mesma linha'
      ✗ mutação sobreviveu: 'prosa citando o prefixo conta como fonte'
  P2/fato     mutações mortas 3/3  →  PORTÃO
P3 — o aviso de limiar afirma a porcentagem certa
  P3/ingenua  mutações mortas 0/3  →  DECORAÇÃO
      ✗ mutação sobreviveu: 'fator 100 aplicado duas vezes'
      ✗ mutação sobreviveu: 'aviso sem número'
      ✗ mutação sobreviveu: 'número de outra sessão'
  P3/fato     mutações mortas 3/3  →  PORTÃO
resumo: 6 portões provados, 3 portão(ões), 3 decoração(ões)
```

`python3 provar.py --so fato` — **sai com código 0**:

```text
P1 — a evidência de TAIL:review registra uma revisão que aconteceu
  P1/fato     mutações mortas 8/8  →  PORTÃO
P2 — a página declara o número certo de fontes
  P2/fato     mutações mortas 3/3  →  PORTÃO
P3 — o aviso de limiar afirma a porcentagem certa
  P3/fato     mutações mortas 3/3  →  PORTÃO
resumo: 3 portões provados, 3 portão(ões), 0 decoração(ões)
```

Conferido em 02/11/2026 com Python 3.12.10 (Windows 11, Git Bash): as duas saídas acima são
cópia literal da execução.

## O que observar

- **Os três portões ingênuos ficam verdes na fixture positiva.** Rodados só no caminho feliz,
  os seis parecem iguais. Só a mutação os separa.
- **P1/ingenua mata uma mutação em oito** — a do marcador `<...>` que o gerador de ciclo
  escreve. É o portão que reconhece a forma que *ele mesmo* produz, não a ausência de fato.
- **P2/ingenua erra nos dois sentidos**: reprova a página certa (duas fontes numa linha) e
  aprova a errada (a palavra `https://` na prosa). Contar linhas não é contar itens.
- **P3/ingenua não mata nada.** A palavra "limite" está em todo aviso, certo ou errado.

## Exercício: quebre o portão bom

Abra `portoes.py` e afrouxe o P1/fato: na constante `_AUSENCIA`, troque o começo do padrão
`r"^[\s>(*_`\-]*(ainda\s+)?(pendente|` por `r"(ainda\s+)?(pendente|`, e em `evidencia_fato`
troque `_AUSENCIA.match(valor)` por `_AUSENCIA.search(valor)`. Rode `python3 provar.py --so fato`.
Saída esperada (código 1):

```text
P1 — a evidência de TAIL:review registra uma revisão que aconteceu
  P1/fato     mutações mortas 8/8  →  DECORAÇÃO
      ✗ falso vermelho em ''pendente' no meio da frase'
```

O portão continua matando as oito mutações — e passou a reprovar a evidência legítima. É o
defeito espelhado que o ciclo 063 do Maestro evitou ao ler o vocabulário **do início** da
evidência: a correção ingênua de um proxy costuma ser outro proxy. Desfaça a mudança antes de
seguir.
