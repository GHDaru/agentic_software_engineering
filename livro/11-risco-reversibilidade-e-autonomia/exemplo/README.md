# Exemplo do capítulo 11 — a classe vem do desfazer, e a reversibilidade compra autonomia

Dois programas pequenos, sem dependência externa, cada um com uma ideia do capítulo.

| Arquivo | O que é |
|---|---|
| `politica.py` | a política de autonomia: classifica uma ação por **custo de desfazer × raio**, aplica as alavancas de reversibilidade e devolve a classe (0–6), a política (`permitir` / `perguntar` / `negar`) e o gate humano |
| `acoes.json` | as ações classificadas, inspiradas em casos do Maestro, cada uma com a classe esperada; e um "dia" fictício para o modo `--funil` |
| `instalador.py` | um instalador em miniatura que ganhou o poder de apagar: cinco cenários, cada um rodado contra a versão ingênua (v1) e a corrigida (v2) |
| `saida-*.txt` | a saída esperada de cada comando, para conferir com `diff` |

## Como rodar

Requisito: Python 3.8 ou mais novo. No Git Bash do Windows, onde `python3` pode ser um atalho
vazio, use `python`. O `-B` só evita criar `__pycache__`.

```bash
cd livro/11-risco-reversibilidade-e-autonomia/exemplo
python3 -B politica.py                 # classifica as 15 ações
python3 -B politica.py --funil         # quantas decisões humanas um dia pede, em cada regime
python3 -B instalador.py               # os cinco cenários do instalador

# conferir contra a saída esperada (nenhuma linha de diferença):
python3 -B politica.py         | diff --strip-trailing-cr - saida-politica.txt
python3 -B politica.py --funil | diff --strip-trailing-cr - saida-funil.txt
python3 -B instalador.py       | diff --strip-trailing-cr - saida-instalador.txt
```

Os três comandos saem com **código 0**.

## Saída esperada

### `politica.py` (trecho; o arquivo inteiro está em `saida-politica.txt`)

```text
[0] ler o código do repositório
     alavancas: —                      classe: leitura                    política: permitir             gate: nenhum  ok
[5] ler o .env de produção (segredo lido não se desvê)
     alavancas: —                      classe: financeira / irreversível  política: perguntar            gate: dupla aprovação  ok
[2] push de uma branch nova no remoto
     alavancas: —                      classe: criação reversível         política: permitir             gate: no merge  ok
[5] apagar tabela em produção
     alavancas: —                      classe: financeira / irreversível  política: perguntar            gate: dupla aprovação  ok
[4] apagar tabela em produção
     alavancas: backup                 classe: exclusão / efeito externo  política: perguntar            gate: confirmação forte  ok
[3] apagar tabela em produção
     alavancas: soft_delete            classe: alteração                  política: perguntar            gate: aprovação com resumo  ok
[0] migração destrutiva
     alavancas: dry_run                classe: leitura                    política: permitir             gate: nenhum  ok
[6] agente escreve no registro que lhe dá endereço
     alavancas: —                      classe: lote / administrativa      política: negar                gate: fluxo humano formal  ok
resumo: 15 ações, 0 divergência(s)
```

O que observar: a mesma ação ("apagar tabela em produção") desce três classes com três
alavancas diferentes, sem ganhar nenhuma aprovação a mais; e uma **leitura** (o `.env`) cai na
classe irreversível, porque o que decide a classe é o custo de desfazer, não o verbo.

### `politica.py --funil`

```text
ações no dia (fictício): 189
  classe 0 (leitura): 143
  classe 2 (criação reversível): 41
  classe 3 (alteração): 3
  classe 5 (financeira / irreversível): 1
  classe 6 (lote / administrativa): 1
gate uniforme pesado : 189 decisões humanas
gate proporcional    : 4 decisões humanas, 1 bloqueada(s) por política
gate uniforme leve   : 0 decisões humanas — e 1 ação(ões) irreversível(is) sem ninguém olhar
```

Os números do "dia" são fictícios (estão em `acoes.json`); o que o modo mostra é a forma dos
dois fracassos simétricos do gate uniforme.

### `instalador.py`

```text
C1 a flag destrutiva não vence o freio
   v1:
      --force --dry-run → force=1 dry=0
   v2:
      --force --dry-run → force=0 dry=1
   → defeito reproduzido na v1: sim; invariante na v2: sim  [ok]
C2 reivindicar é consequência de escrever, não de olhar
   v1:
      arquivo do projeto, idêntico ao nosso, depois da poda: APAGADO
   v2:
      arquivo do projeto, idêntico ao nosso, depois da poda: existe
   → defeito reproduzido na v1: sim; invariante na v2: sim  [ok]
C3 o --force guarda a edição do projeto antes de sobrescrever
   v1:
      edição do time depois do --force: PERDIDA, sem cópia
   v2:
      edição do time depois do --force: recuperável em .maestro-old
   → defeito reproduzido na v1: sim; invariante na v2: sim  [ok]
C4 a poda não sai do alvo
   v1:
      arquivo fora do alvo depois da poda: APAGADO
   v2:
      recusado: '../fora.txt' resolve fora do alvo — o manifesto é dado, não comando
      arquivo fora do alvo depois da poda: existe
   → defeito reproduzido na v1: sim; invariante na v2: sim  [ok]
C5 execução a seco não escreve nada
   v1:
      --force --dry-run mudou a árvore? SIM
   v2:
      --force --dry-run mudou a árvore? não
   → defeito reproduzido na v1: sim; invariante na v2: sim  [ok]
resumo: 5 cenários, 0 falha(s)
```

A v1 não é o instalador antigo do Maestro (que pulava tudo o que existia e não apagava nada):
é a primeira versão do instalador que **atualiza e poda**, montada com os defeitos que a revisão
independente do ciclo 051 achou nela. Cada cenário só conta se o defeito **aparecer** na v1; um
cenário em que a v1 também passa não prova nada sobre a v2, e o programa sai com código 1.

O cenário do *symlink* (ciclo 052) não está aqui porque criar *symlink* no Windows exige
privilégio. O invariante que ele protege é o mesmo do C4: o destino **resolvido** tem de ficar
dentro do alvo — e a função `dentro()` já resolve o caminho, de modo que um link para fora cai
na mesma recusa.

## Exercícios

1. Em `politica.py`, troque o mapa de `soft_delete` para `{"impossivel": "caro"}` e rode de
   novo: a expectativa de uma ação diverge e o programa sai com código 1. A política mudou; o
   caso escrito avisa.
2. Acrescente a `acoes.json` uma ação do seu time (um *deploy* com *feature flag*, por exemplo)
   e decida antes de rodar qual classe ela deve ter. Se a classe que saiu é outra, o erro está
   na política ou na sua intuição?
3. Em `instalador.py`, apague a linha que copia para `.maestro-old` e rode: o C3 falha na v2.
