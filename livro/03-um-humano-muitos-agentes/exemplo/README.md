# Exemplo do capítulo 3 — o gargalo e a fila de decisões

Dois scripts, só com a biblioteca padrão do Python 3.8+. Nenhum chama modelo de IA: o primeiro
mede a fila que se forma na frente do humano que decide; o segundo constrói essa fila a partir
de um registro só-acréscimo, do jeito que o padrão do capítulo descreve.

| Arquivo | O que é |
|---|---|
| `gargalo.py` | simulação determinística de um dia de um humano que decide as fatias entregues por N agentes; três cenários: mais agentes, gate mais barato, paralelizar dentro da feature |
| `sessoes.json` | roster fictício de um time (humano, gerente, workers), com um nome repetido em outro projeto e uma sessão caída |
| `eventos.jsonl` | registro só-acréscimo de 16 eventos (pedidos de decisão e rulings) de um dia fictício; o campo `esperado` diz o veredito certo |
| `fila.py` | aplica as regras (endereço, pedido, ruling, sem "dispensar", só-acréscimo), deriva a frase-chave, mede a espera humana e prova a guarda por mutação |
| `saida-esperada-*.txt` | a saída de referência dos dois scripts |

## Como rodar

```bash
cd livro/03-um-humano-muitos-agentes/exemplo
python gargalo.py > /tmp/g.txt; diff /tmp/g.txt saida-esperada-gargalo.txt && echo "gargalo: igual"
python fila.py    > /tmp/f.txt; diff /tmp/f.txt saida-esperada-fila.txt    && echo "fila: igual"
```

No Windows com Git Bash, use `python` (o `python3` do Git Bash pode ser um atalho vazio) e, se
o console reclamar de acentos, exporte `PYTHONIOENCODING=utf-8` antes. O `fila.py` sai com
código 0 quando os 16 eventos têm o veredito esperado **e** a mutação é acusada; 1 se não. O
`gargalo.py` sai com 0 sempre: o que se confere é a saída.

Para usar com o seu time, edite em `gargalo.py` a linha `periodo, custo = 60, 12` (de quantos
em quantos minutos cada agente entrega algo que exige decisão, e quantos minutos cada decisão
custa de verdade) e a constante `DIA` (minutos de atenção por dia).

## As regras do `fila.py`

| Regra | O que exige | De onde vem |
|---|---|---|
| E | endereço `nome · ref · projeto` resolvido para uma sessão viva; nome solto, ref inexistente, ref de outra sessão ou sessão caída são recusados | glossário do Maestro, "Ref de sessão" e "Endereçar por ref" |
| P1 | pedido de decisão tem prazo | glossário, "Pedido de decisão"; `decisionDueAt` obrigatório |
| P2 | pedido tem opções e recomendação | spec 072, "Pedido de decisão" |
| R1 | ruling responde a um pedido aceito e ainda aberto | spec 072 |
| R2 | ruling tem autor humano | glossário, "Ruling" e "Portão do regente" |
| R3 | ruling tem destino resolvível | glossário, "Ruling" |
| R4 | ruling não é anterior ao pedido | anti-regra 5 do desenho de interface do 066 ("não digita hora") |
| N | não existe "dispensar" | anti-regra 4 do desenho de interface do 066 |
| A | o registro só cresce (`seq` estritamente crescente) | ADR 0022 (eventos só-acréscimo) |

## Saída esperada — `gargalo.py`

```text
== um humano, 480 min de atenção, 12 min por decisão (capacidade: 40 decisões/dia)
   cada agente entrega 1 fatia por hora; colunas em fatias; espera em minutos

A  mais agentes, mesmo gate
  cenário                      prod decid  fila  esp.méd  esp.máx   ocup
   1 agente(s)                    8     8     0      0.0      0.0    20%
   2 agente(s)                   16    16     0      0.0      0.0    40%
   4 agente(s)                   32    32     0      0.0      0.0    80%
   5 agente(s)                   40    40     0      0.0      0.0   100%
   8 agente(s)                   64    40    24     87.8    180.0   100%
  16 agente(s)                  128    40    88    160.9    330.0   100%

B  8 agentes, gate mais barato (critério verificável, ação reversível)
  cenário                      prod decid  fila  esp.méd  esp.máx   ocup
  gate de 12 min                 64    40    24     87.8    180.0   100%
  gate de  8 min                 64    60     4     14.8     30.0   100%
  gate de  6 min                 64    64     0      0.0      0.0    80%

C  8 agentes, paralelizar DENTRO da feature (uma decisão por lote de fatias)
  cenário                      prod decid  fila  esp.méd  esp.máx   ocup
  1 decisão por fatia (12)       64    40    24     87.8    180.0   100%
  1 decisão por 4 fatias (20)    64    64     0      0.0      0.0    67%
  (no lote: 16 decisões de 20 min liberam 64 fatias)

== leitura
  de 4 para 8 agentes a produção dobra (32 → 64), as liberadas vão de 32 a 40 e 24 fatias dormem na fila
  o teto é o humano: 40 decisões/dia, com 4, 8 ou 16 agentes
```

Colunas: `prod` fatias produzidas no dia; `decid` fatias liberadas por uma decisão; `fila`
fatias que o humano não alcançou; `esp.méd` e `esp.máx` espera humana em minutos (a máxima
inclui a idade, no fim do dia, de quem ficou na fila); `ocup` fração do dia que o humano
passou decidindo.

## Saída esperada — `fila.py` (resumo; a íntegra está em `saida-esperada-fila.txt`)

```text
== frase-chave (derivada da fila, nunca digitada)
  14:00  você tem 3 decisões esperando; a mais antiga (D-01) há 6 h 56 min
  14:35  você tem 2 decisões esperando; a mais antiga (D-01) há 7 h 31 min
  16:00  você tem 1 decisão esperando; a mais antiga (D-08) há 55 min

== espera humana (do pedido ao ruling)
  D-01  07:04 → 15:20    8 h 16 min  (prazo estourado)
  D-02  07:30 → 12:10    4 h 40 min  (prazo estourado)
  D-07  11:40 → 14:31    2 h 51 min
  D-09  13:10 → 15:40    2 h 30 min
  média 4 h 34 min · máxima 8 h 16 min · 2 de 4 respondidos depois do prazo

== prova por mutação: reescrever uma linha do registro
  ✓ guarda A acusou: seq 2 depois de 4: o registro foi reescrito, não acrescido

resultado: 16/16 eventos com o veredito esperado; mutação acusada: 1/1
```

## O que o exemplo não prova

O modelo de fila é determinístico: chegadas em ritmo fixo e decisões de duração fixa. Filas
reais têm variabilidade, e com ela a espera começa a crescer antes de 100% de ocupação; o
exemplo, portanto, subestima a espera. Os dados de `sessoes.json` e `eventos.jsonl` são
fictícios, com a forma dos casos de outubro de 2026 descritos no capítulo.
