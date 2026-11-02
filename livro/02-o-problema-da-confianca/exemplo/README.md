# Exemplo do capítulo 2 — confiança como estrutura verificável

Dois scripts, só com a biblioteca padrão do Python 3.8+. Nenhum chama modelo de IA: o que se
verifica é a **estrutura** que torna um resultado confiável, não o resultado.

| Arquivo | O que é |
|---|---|
| `papeis.json` | os papéis de um time humano + agentes: quem julga, que ferramentas tem, que delegações existem |
| `registros/*.json` | dez fechamentos de ciclo, um correto e os outros com um defeito cada; o campo `esperado` diz o veredito certo |
| `verifica.py` | aplica as regras R0–R5 a cada registro e prova, por mutação, que o portão acusa |
| `veredictos-042-063.csv` | para os ciclos 042–063 do Maestro em `19823c2`: o veredito do cabeçalho do `qa-report.md` e, lidos na evidência de `TAIL:review`, quando a revisão rodou e o que ela fez |
| `rendimento.py` | mede quantas vezes a revisão independente mudou o resultado |
| `saida-esperada-*.txt` | a saída de referência dos dois scripts |

## Como rodar

```bash
cd livro/02-o-problema-da-confianca/exemplo
python verifica.py   > /tmp/v.txt; diff /tmp/v.txt saida-esperada-verifica.txt   && echo "verifica: igual"
python rendimento.py > /tmp/r.txt; diff /tmp/r.txt saida-esperada-rendimento.txt && echo "rendimento: igual"
```

No Windows com Git Bash, use `python` (o `python3` do Git Bash pode ser um atalho vazio). O
`verifica.py` sai com código 0 quando todo registro teve o veredito esperado **e** as duas
mutações foram acusadas; 1 se não.

## As regras

| Regra | O que exige | De onde vem |
|---|---|---|
| R0 | papel que julga não tem `Write`/`Edit`; com `Bash`, só aviso | corolário C3 do Maestro; `scripts/check-agents.sh` |
| R1 | quem executou não é quem revisou, e houve revisão | teorema T2; anti-padrão 6 |
| R2 | quem revisou é um papel que julga, sem caneta | C3 aplicado ao registro |
| R3 | a revisão foi em contexto fresco | T2, pelo lado do axioma A3 |
| R4 | caixa marcada tem evidência; vazio, `<...>`, `[...]` e "pendente" sozinho não contam | ciclos 042, 043, 061, 062 |
| R5 | gate com dono humano, ou delegação escrita + quem decide não executou + crítico fresco | axioma A2; ADR 0026 |

## Saída esperada — `verifica.py`

```text
== configuração dos papéis (R0)
  aviso R0 'revisor' julga e tem Bash: o shell também escreve
  aviso R0 'seguranca' julga e tem Bash: o shell também escreve
  ✓ nenhum papel que julga tem Write/Edit

== registros de fechamento
  ✓ 01-integro: passa (esperado: passa)
  ✓ 02-autor-revisa: reprova (esperado: reprova)
      - R1 quem revisou ('implementador') é quem executou
      - R2 'implementador' não é papel que julga
      - R3 revisão em contexto herdado: o revisor carregou os becos do autor
      - R4 caixa marcada com evidência que é ausência: 'ok'
  ✓ 03-caixa-sem-testemunha: reprova (esperado: reprova)
      - R1 não há revisão: ninguém além do autor olhou
      - R4 caixa marcada com evidência que é ausência: '<pendente>'
  ✓ 04-pendente-como-prova: reprova (esperado: reprova)
      - R1 não há revisão: ninguém além do autor olhou
      - R4 caixa marcada com evidência que é ausência: 'pendente.'
  ✓ 05-juiz-com-caneta: reprova (esperado: reprova)
      - R2 'qa' não é papel que julga
  ✓ 06-contexto-herdado: reprova (esperado: reprova)
      - R3 revisão em contexto herdado: o revisor carregou os becos do autor
  ✓ 07-gate-por-agente: reprova (esperado: reprova)
      - R5 gate 'merge' aberto por 'regente' (agente) sem delegação escrita
  ✓ 08-gate-delegado: passa (esperado: passa)
  ✓ 09-gate-delegado-sem-critico: reprova (esperado: reprova)
      - R5 gate delegado sem crítico em contexto fresco
  ✓ 10-regente-executou: reprova (esperado: reprova)
      - R5 quem abre o gate por delegação executou o trabalho

== prova por mutação: o portão acusa quando a regra é violada?
  revisor ganha Edit -> R0 acusa
  delegação revogada -> 08-gate-delegado reprova

resultado: 10/10 registros com o veredito esperado; mutações acusadas: 2/2
✓ verificação de confiança OK
```

## Saída esperada — `rendimento.py` (últimas linhas)

```text
ciclos: 22 · revisão antes do gate: 20 · revisão só depois da promoção: 2
rendimento da revisão antes do gate: 19/20 = 95.0%
cobertura da revisão antes do gate: 20/22 = 90.9%
ciclos reprovados por um parecer, em qualquer momento: 21/22 = 95.5%
cabeçalho 'aguardando parecer' com parecer no corpo: 3 (061, 062, 063)
```

A listagem completa, ciclo a ciclo, está em `saida-esperada-rendimento.txt`.

## Como o CSV foi obtido (reproduzível)

No clone do Maestro (`https://github.com/GHDaru/maestro`), duas leituras por ciclo, de 042 a 063.

O cabeçalho (coluna `veredito_no_cabecalho`; asteriscos de ênfase retirados):

```bash
for d in $(git ls-tree --name-only 19823c2 specs/ | grep -E 'specs/0(4[2-9]|5[0-9]|6[0-3])-'); do
  printf '%s | ' "$(basename "$d")"
  git show "19823c2:$d/qa-report.md" | grep -m1 -iE 'veredito|verdict' | sed -E 's/.*(Veredito|Verdict)\*\*: *//I'
done
```

O corpo (colunas `linha_tail_review`, `revisao` e `resultado`): a entrada `TAIL:review` da
seção de fechamento, com as três linhas seguintes.

```bash
for d in $(git ls-tree --name-only 19823c2 specs/ | grep -E 'specs/0(4[2-9]|5[0-9]|6[0-3])-'); do
  echo "== $d"
  git show "19823c2:$d/qa-report.md" | grep -n -A3 -E '^- (\*\*)?TAIL:review'
done
```

As colunas `revisao` e `resultado` são **leitura humana** desse trecho, uma linha por ciclo; o
script só conta. Por isso o número fica registrado como *observado*, e não como *medido*. Três
casos pedem nota:

- **061 e 062**: a evidência diz "rodada depois da promoção" e "REPROVOU: 18 achados cobrindo os
  ciclos 061 e 062" — um parecer só, depois do gate, para os dois ciclos.
- **063**: o cabeçalho ficou em "aguardando parecer", mas a evidência registra a revisão do
  próprio ciclo, que reprovou com 18 defeitos (5 introduzidos por ele), e o gate depois dela.
- **052**: a evidência cita o parecer do 051 como origem do ciclo e não relata reprovação; o
  script conta "não mudou", que é a leitura que menos favorece a revisão.

A primeira versão deste exemplo classificava pelo cabeçalho e contava 061, 062 e 063 como
"sem revisão". O corpo desmente os três; é por isso que a última linha da saída existe.

## Experimente quebrar

- Dê `Write` ao `guardiao` em `papeis.json`: R0 passa a reprovar e o script sai com 1.
- Troque a evidência de `01-integro.json` por `"pendente."`: o registro reprova e deixa de
  bater com o `esperado`.
- Escreva um registro seu com o fechamento do último pull request do seu time.
