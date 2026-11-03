# Exemplo do capítulo 14 — as três engrenagens que fazem a organização aprender

Um script Python, sem dependência externa, com as três verificações que o capítulo defende. Cada
uma reproduz a forma de um portão real do Maestro (`19823c2`), reduzida ao essencial:

| Verificação | O que prova | Portão real de que deriva |
|---|---|---|
| `gatilho` | a retrospectiva é cobrada pela **dívida** de achados abertos (≥ 4 abertos, ou um aberto há ≥ 6 ciclos), e fechar um achado é ligação **estrutural** (campo `fecha`), nunca prosa | `scripts/check-retro.sh` |
| `anexar` | o índice de decisões só cresce: corrigir é acrescentar linha; reescrever linha antiga é recusado | `scripts/record-decision.sh` + `scripts/hooks/guard-immutables.py` |
| `artefatos` | um artefato sobrevive por consumo (tem consumidor **e** falha alto quando velho) ou por imutabilidade; o resto apodrece ou deve ser podado | teorema T5, corolário C9; `check-adr.sh`, gate de CHANGELOG |

| Arquivo | O que é |
|---|---|
| `aprende.py` | as três verificações e o roteiro `demo` |
| `dados/indice.jsonl` | os **cinco achados reais** que estavam abertos quando o ciclo 034 começou — linhas copiadas sem edição de `docs/records/decisoes.jsonl@19823c2` |
| `dados/fechamento-estrutural.jsonl` | as **cinco linhas reais** `retro-034-fecha-*` que a retro do ciclo 034 anexou, cada uma com o campo `fecha` |
| `dados/fechamento-em-prosa.jsonl` | a forma **errada** que o ciclo 034 escreveu primeiro (id novo, sem `fecha`) — reconstruída para o exemplo a partir do relato do `qa-report.md` do 034 |
| `dados/artefatos.json` | **ilustrativo**: sete artefatos com consumidor, cobrança e último ciclo; os casos do índice de ADRs e do roadmap imitam falhas reais (capítulo, seção "Teoria"), mas os números de ciclo deste arquivo não são medidos |

## Como rodar

Requisito: Python 3.8 ou mais novo. No Git Bash do Windows, onde `python3` pode ser um atalho
vazio, use `python`.

```bash
cd livro/14-a-organizacao-que-aprende/exemplo
python3 aprende.py demo                                  # o roteiro do capítulo; sai 0
python3 aprende.py gatilho dados/indice.jsonl 34         # só o gatilho; sai 1 (dívida)
python3 aprende.py artefatos dados/artefatos.json 34     # só a auditoria; sai 1 (3 pedem decisão)
python3 aprende.py anexar dados/indice.jsonl <outro.jsonl>   # compara duas versões do índice
```

## Saída esperada

`python3 aprende.py demo` — **sai com código 0** (os três vermelhos do roteiro são desejados; o
roteiro só falha se algum deles não aparecer):

```text
1. Gatilho da retrospectiva (dívida, não calendário)
  a) índice como está, ciclo corrente 034
    abertos: 5  (achado-023-regua-de-raias, achado-027-retro-sem-gatilho, achado-029-skill-sem-capitulo, achado-031-elo-de-commit, achado-033-renome-em-massa)
    VERMELHO: rode a retrospectiva — 5 achados abertos (limite 4); o mais velho tem 11 ciclos (limite 6)
  b) + linha que 'fecha' em prosa (id novo, sem campo fecha)
    abertos: 5  (achado-023-regua-de-raias, achado-027-retro-sem-gatilho, achado-029-skill-sem-capitulo, achado-031-elo-de-commit, achado-033-renome-em-massa)
    VERMELHO: rode a retrospectiva — 5 achados abertos (limite 4); o mais velho tem 11 ciclos (limite 6)
  c) + linhas com o campo fecha (retro executada)
    abertos: 0
    verde: dívida de retro sob controle

2. Índice só-anexar (corrigir é acrescentar)
  a) anexar uma linha de fechamento
    aceito: 5 linha(s) nova(s), nenhuma antiga tocada
  b) 'corrigir' editando a linha antiga
    RECUSADO: linha 1 reescrita

3. Artefatos: sobrevive o consumido ou o imutável (T5)
    spec.md                 vivo (consumido)  consumidor: o agente que gera o código; quando velho: código errado; o revisor compara com a spec
    CHANGELOG.md            vivo (consumido)  consumidor: quem lê a versão; quando velho: a CI reprova o pull request sem entrada
    decisoes.jsonl          vivo (consumido)  consumidor: check-retro.sh e retro.sh; quando velho: o gatilho acusa dívida errada
    adr/0017.md             vivo (imutável)   descreve um instante; pode ser superado, nunca fica velho
    adr/README.md (índice)  APODRECENDO       consumidor sem cobrança; 17 ciclo(s) atrás do projeto
    roadmap.md              APODRECENDO       consumidor sem cobrança; 25 ciclo(s) atrás do projeto
    prd-avulso.md           PODAR             ninguém consome — candidato a poda (YAGNI)
  resumo: 7 artefatos, 3 pedem decisão (podar, cobrar ou superar)

vermelhos esperados no roteiro: 3 (1a, 1b, 2b) — todos desejados
```

Conferido em 02/11/2026 com Python 3.12.10 (Windows 11).

## O que observar

1. **1a reproduz o número real.** Com os cinco achados de verdade e o ciclo corrente 034, o
   gatilho dá "5 abertos, o mais velho com 11 ciclos" — o mesmo que o `qa-report.md` do ciclo
   034 registrou para o `check-retro.sh` rodado **antes** da retro.
2. **1b é a falha que o próprio ciclo 034 cometeu.** Uma linha que diz "fechados" em prosa,
   com id novo, não fecha nada: o portão continua vendo cinco abertos. O fechamento existia no
   texto e não no dado.
3. **2b é o atalho que o método proíbe.** Trocar `aberta` por `fechada` na linha antiga parece
   mais limpo e destrói a memória de que o achado ficou aberto onze ciclos.
4. **3 separa quatro destinos** (as quatro classes da saída). O que é consumido e cobrado vive
   ("vivo (consumido)"); o imutável vive ("vivo (imutável)"); o que tem leitor mas não tem
   cobrança (o índice escrito à mão, o roadmap) apodrece em silêncio ("APODRECENDO"); o que não
   tem leitor nenhum se poda ("PODAR").

## Exercício

Abra `dados/artefatos.json` e dê ao `roadmap.md` uma cobrança — por exemplo,
`"falha_quando_velho": "portão compara o maior ciclo em specs/ com o maior citado no roadmap"`
(o candidato que o ciclo 017 escreveu e não implementou). Rode `python3 aprende.py artefatos
dados/artefatos.json 34`: o roadmap passa a "vivo (consumido)" e o resumo cai para 2. Agora
pergunte se o portão que você descreveu **existe**. Se não existe, você acabou de cometer o
anti-padrão 13 no próprio arquivo de auditoria: o campo mede a frase, não o fato.
