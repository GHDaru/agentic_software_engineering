# Exemplo do capítulo 6 — onde cortar

O que este exemplo prova, em oito passos: o mesmo trabalho, cortado de três jeitos, dá três
resultados diferentes. O corte por **tela** e o corte por **quantidade** produzem colisões que
uma regra de "arquivos diferentes" não enxerga (um conceito com três donos, um contrato que
ninguém escreve); o corte por **fronteira** dá um dono a cada conceito e a cada arquivo, e a
ordem de execução sai dos contratos, não de uma lista. O exemplo também mostra que paralelizar
só compensa enquanto a passagem entre fatias é barata, escolhe o padrão de orquestração pela
menor autonomia que resolve e reproduz a colisão de numeração entre duas linhas de trabalho
paralelas.

Os planos são um modelo simplificado do caso real do capítulo (ciclo 074 do Maestro, o "número
único" de quem precisa do humano). Os custos são unidades abstratas, não horas medidas.

Requisito: Python 3.8+ (só biblioteca padrão) e bash. Nada pago, nada de rede.

## Como rodar

```bash
cd livro/06-como-dividir-o-trabalho/exemplo
bash rodar.sh                               # imprime a saída
bash rodar.sh | diff - saida-esperada.txt   # confere: nenhuma linha de diferença
```

No Windows, rode no Git Bash. O script procura `python3`, `python` e `py`, nessa ordem, e usa
o primeiro que for Python 3.8+. Para forçar um interpretador: `PYTHON=... bash rodar.sh`.

## Os arquivos

| Arquivo | Papel |
|---|---|
| `dividir.py` | `colisao`, `ondas`, `custo`, `autonomia`, `numerar` |
| `planos/por-tela.json` | cada agente com uma tela; os três calculam o mesmo número |
| `planos/por-quantidade.json` | seis mudanças, duas por agente, na ordem da lista |
| `planos/por-fronteira.json` | um dono por conceito; a casca expõe uma porta inerte; quem consome espera |
| `casos.json` | seis situações para a regra da menor autonomia |
| `linhas.json` | duas linhas de trabalho que numeraram ciclos sem se falar |
| `saida-esperada.txt` | a saída de `bash rodar.sh`, conferida em 02/11/2026 |
| `medir_maestro.py` | opcional: reproduz num clone do Maestro os números do capítulo |

## O modelo de custo (passos 5 e 6)

- **um agente, em sequência** = soma dos custos das fatias;
- **caminho crítico** = soma, onda a onda, da fatia mais cara da onda;
- **passagens** = quantas vezes uma fatia consome um contrato de outra (cada uma custa
  `custo_handoff`, ou o valor de `--handoff`);
- **retrabalho** = para cada colisão, a soma dos custos das fatias envolvidas: um corte fora
  da costura não se reconcilia, se refaz;
- **overhead de coordenação** = (passagens + retrabalho) ÷ tempo paralelo.

## Saída esperada

Os passos 1, 2, 5, a segunda linha do 6 e o 8 saem com código 1 **de propósito**: são as
colisões e o paralelo que não paga.

```text

== 1. corte por tela: o mesmo conceito ganha três donos
plano: um número só para «precisa de mim», cortado por TELA  (critério do corte: cada agente fica com uma tela e resolve tudo o que ela mostra)
  ✗ conceito com mais de um dono: contagem-precisa-de-mim  ← W01, W04, W05
✗ 1 colisão(ões): a reconciliação vai custar o que o paralelo economizou.
(exit 1)

== 2. corte por quantidade: dois agentes no mesmo arquivo, e um contrato que ninguém escreve
plano: o mesmo trabalho, cortado por QUANTIDADE  (critério do corte: seis mudanças, duas para cada agente, na ordem da lista)
  ✗ arquivo com dois escritores: casca.js  ← A, B
  ✗ contrato consumido sem dono: contagem-dos-andares  ← C
✗ 2 colisão(ões): a reconciliação vai custar o que o paralelo economizou.
(exit 1)

== 3. corte por fronteira: cada arquivo e cada conceito com um dono
plano: o mesmo trabalho, cortado por FRONTEIRA (um dono por conceito)  (critério do corte: o conceito tem um dono; quem consome espera o contrato; a casca expõe uma porta inerte)
✓ 4 fatias, cada arquivo e cada conceito com um dono só.
(exit 0)

== 4. a ordem sai dos contratos: o dono antes de quem consome
  onda 1: W01 · W02 · W03
  onda 2: W05 (espera W01, W02)
✓ 2 onda(s); dentro de uma onda as fatias correm em paralelo.
(exit 0)

== 5. quanto custa: o corte por tela e o por quantidade não pagam a coordenação
plano: um número só para «precisa de mim», cortado por TELA
  um agente, em sequência ......... 9
  caminho crítico das ondas ....... 3
  passagens entre fatias .......... 0 × 1 = 0
  colisões → retrabalho ........... 1 colisão(ões) = 9
  paralelo (caminho + coordenação)  12
  overhead de coordenação ......... 9/12 = 75% do tempo paralelo
✗ paralelizar NÃO compensa: 12 ≥ 9. Um agente só, ou um corte melhor.
(exit 1)
plano: o mesmo trabalho, cortado por QUANTIDADE
  um agente, em sequência ......... 9
  caminho crítico das ondas ....... 9
  passagens entre fatias .......... 3 × 1 = 3
  colisões → retrabalho ........... 2 colisão(ões) = 9
  paralelo (caminho + coordenação)  21
  overhead de coordenação ......... 12/21 = 57% do tempo paralelo
✗ paralelizar NÃO compensa: 21 ≥ 9. Um agente só, ou um corte melhor.
(exit 1)

== 6. o corte por fronteira paga ... enquanto a passagem for barata
plano: o mesmo trabalho, cortado por FRONTEIRA (um dono por conceito)
  um agente, em sequência ......... 14
  caminho crítico das ondas ....... 7
  passagens entre fatias .......... 2 × 1 = 2
  colisões → retrabalho ........... 0 colisão(ões) = 0
  paralelo (caminho + coordenação)  9
  overhead de coordenação ......... 2/9 = 22% do tempo paralelo
✓ paralelizar compensa: 14 → 9
(exit 0)
plano: o mesmo trabalho, cortado por FRONTEIRA (um dono por conceito)
  um agente, em sequência ......... 14
  caminho crítico das ondas ....... 7
  passagens entre fatias .......... 2 × 4 = 8
  colisões → retrabalho ........... 0 colisão(ões) = 0
  paralelo (caminho + coordenação)  15
  overhead de coordenação ......... 8/15 = 53% do tempo paralelo
✗ paralelizar NÃO compensa: 15 ≥ 14. Um agente só, ou um corte melhor.
(exit 1)

== 7. a menor autonomia que resolve, caso a caso
  1. Conduzir um ciclo: spec → plano → tarefas → implementar → DoD
    → encadeamento + avaliador-otimizador  (passos conhecidos: fluxo fixo, barato e depurável; o laço para quando o critério passa)
  2. Triar o que chega: correção de texto, funcionalidade nova, migração de banco
    → roteamento  (classificar a entrada e escolher o caminho fixo)
  3. Número único: domínio, casca e entrada, com o contrato escrito antes
    → paralelização + avaliador-otimizador  (fatias por fronteira, cada uma com dono e contrato; o laço para quando o critério passa)
  4. Metade dos arquivos para cada agente, 'porque são independentes'
    → encadeamento  (partes 'independentes' sem fronteira declarada: corte antes de paralelizar)
  5. Integrar 42 branches de outra linha: o corte só aparece lendo o histórico
    → orquestrador-trabalhadores  (as fatias só se conhecem lendo o problema; o reduce é humano)
  6. Um agente que 'descobre sozinho' o que refatorar no repositório
    → encadeamento  (autônomo pedido sem evidência de que o simples falhou: recusado)
(exit 0)

== 8. numerar em duas linhas paralelas: colisão de endereço e recusa
  ✗ número 064 alocado 2 vezes: dev:064-capa-para-a-ia-que-instala × paralela:064-workflow-painel
  ✗ número 065 alocado 2 vezes: dev:065-o-metodo-se-cobra × paralela:065-board
  ✗ 'ciclo 064' → recusado: 2 destinos (endereço ambíguo não se resolve, se recusa)
  ✓ 'ciclo 066' → paralela:066-custeio
  ✗ 'ciclo 068' → recusado: nenhum destino
  renumeração (a linha 'dev' fica; a outra ganha o próximo livre):
    064-workflow-painel      → 066-workflow-painel
    065-board                → 067-board
    066-custeio              → 068-custeio
    067-painel-chamados      → 069-painel-chamados
    070-conferidor           → 070-conferidor
(exit 1)
```

Leia o passo 8 até o fim: a renumeração resolve a colisão e **quebra** a referência que
estava certa. Quem anotou "ciclo 066" antes dela apontava para `066-custeio`; depois, o mesmo
texto aponta para outra coisa ou para nada. A política "próximo livre" é a do brinquedo; o
mapa real do Maestro foi aprovado por um humano e seguiu a ordem de integração (ver o
capítulo, seção "O padrão Maestro").

## Exercícios

1. Em `planos/por-tela.json`, dê o conceito `contagem-precisa-de-mim` a uma fatia só e faça
   as outras duas consumi-lo. Rode `colisao`, `ondas` e `custo`: quantas ondas aparecem, e o
   paralelo passa a compensar?
2. Em `planos/por-fronteira.json`, faça `W01` consumir `api.contarMenu` e `W02` consumir
   `quemPrecisaDeVoce`. Rode `ondas`: o que o script diz, e por que nenhuma ordem serve?
3. Ache o valor de `--handoff` a partir do qual o corte por fronteira deixa de pagar.

## Opcional: os números do Maestro

```bash
git clone https://github.com/GHDaru/maestro /tmp/maestro
python medir_maestro.py /tmp/maestro 19823c2
```

Imprime as pastas de `specs/` com número repetido, as decisões de renumeração e de integração,
os comandos versionados no ciclo 025 e hoje, os relatórios com portão provado falhando, o
tamanho das listas de tarefas, a worktree por Worker no lançador e o estado corrente das ideias
de divisão no catálogo, e os commits da costura do ciclo 074. Saída conferida em 02/11/2026:

```text
Maestro @ 19823c2

[numeração] 76 pastas em specs/
  prefixo 066 usado 2 vezes: 066-painel-de-coordenacao-v0, 066-painel-de-regencia
  prefixo 070 usado 2 vezes: 070-conferidor-ordem-veredito, 070-workflow-sqlite
  pastas sem número (NNN-*): 1
  decisão ciclo-065-renumerado: registrada em 2026-10-12
  decisão ciclo-066-integra-painel-controle: registrada em 2026-10-20
  decisão decisao-066-sessoes-via-gateway: registrada em 2026-10-19

[comandos] 11 arquivos em .claude/commands/ @ c47ea48

[comandos] 12 arquivos em .claude/commands/ @ 19823c2

[avaliador-otimizador] qa-reports com 'prova... falhando' @ c47ea48 (fora o 025): 4
  specs/017-retro-check-proxy/qa-report.md
  specs/018-instalacao-e-ux-jornadas/qa-report.md
  specs/020-bpmn-navegavel-no-livro/qa-report.md
  specs/021-maestro-instalado-no-maestro/qa-report.md

[tarefas] 74 tasks.md; 8 com mais de 20 caixas de tarefa
    85  074-prototipo-navegavel
    57  072-painel-de-regencia
    31  076-padroes-de-engenharia-e-react

[worktree] scripts/multi-session.py cria worktree por Worker: sim
[catálogo] estado corrente (última linha) das ideias de divisão:
  worktree-por-task              observar   2026-08-10
  grafo-de-dependencias          observar   2026-07-30
  decomposicao-tres-passadas     observar   2026-08-10
  padroes-de-fatiamento          observar   2026-08-10
  fatia-vertical-invest          observar   2026-08-10
  contrato-por-fatia             observar   2026-08-10
  decompose-feature-em-issues    descartar  2026-08-06

[costura 074] commits da fatia «um número só»:
  361070a 2026-10-29 ciclo 074: costura-um-numero — a seam api  [ponta do Worker]
  78a1945 2026-10-29 ciclo 074: costura-um-numero — a seam api  [na linha (cherry-pick do Gerente)]
  79d8076 2026-10-29 ciclo 074: costura-um-numero — o predicad  [ponta do Worker]
  6cba79b 2026-10-29 ciclo 074: costura-um-numero — o predicad  [na linha (cherry-pick do Gerente)]
  c3d2e55 2026-10-30 ciclo 074: chip do numero unico, chamada   [ponta do Worker]
  692bf8c 2026-10-30 ciclo 074: chip do numero unico, chamada   [na linha (cherry-pick do Gerente)]
```

As pontas dos Workers (`361070a`, `79d8076`, `c3d2e55`) existem num clone que tenha as
branches de trabalho; num clone só da linha principal, aparecem como `AUSENTE`, e os três
cherry-picks bastam para a conferência.
