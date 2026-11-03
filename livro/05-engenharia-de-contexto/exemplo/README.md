# Exemplo do capítulo 5 — as quatro operações do contexto, medidas

O que este exemplo prova, em doze passos, num projeto de brinquedo (uma loja que ganha cupom
de desconto no ciclo 007):

- **Seleção** — uma tarefa cortada pela fronteira carrega 10% do repositório; a tarefa que
  atravessa o código inteiro carrega 82%, e essa economia baixa é sinal de **corte errado**,
  não de janela pequena. A tarefa que não cita nada manda o executor procurar o contexto
  sozinho.
- **Compressão** — quando a janela compacta e só fica o `tasks.md` que o executor segue, o
  que morava na spec e na conversa (revisão independente, segurança, gate humano) é
  **apagado, não degradado**. Escritos como *token* no `tasks.md`, os mesmos fatos sobrevivem.
- **Persistência** — um índice de decisões só-acréscimo: o script recusa id repetido e
  registro que aponta para um marcador, e um comparador acusa a linha reescrita.
- **Transferência** — `CLAUDE.md` e `AGENTS.md` escritos à mão divergem do disco (uma skill
  invisível nas duas, a regra "skills primeiro" ausente numa). Com fonte única e o bloco de
  skills **gerado do disco**, a deriva fica impossível.
- **Rastreabilidade** — do gate até o porquê em quatro saltos (índice → commit → ciclo →
  ADR), e o commit sem citação que só a memória de alguém explica.
- **O quadro** — as quatro operações do ciclo numa tela: o que um comando de inspeção de
  contexto mostraria.

Requisito: Python 3.8+ (só biblioteca padrão) e bash. Nada pago, nada de rede.

## Como rodar

```bash
cd livro/05-engenharia-de-contexto/exemplo
bash rodar.sh                               # imprime a saída
bash rodar.sh | diff - saida-esperada.txt   # confere: nenhuma linha de diferença
```

No Windows, rode no Git Bash. O script procura `python3`, `python` e `py`, nessa ordem, e usa
o primeiro que for Python 3.8+. Para forçar: `PYTHON=... bash rodar.sh`. Nada em `projeto/` é
alterado: o registro de decisão (passos 6–8) roda numa cópia do índice, e a correção da
instrução (passo 10) roda numa cópia temporária do projeto. Na correção, `AGENTS.md` vira link
simbólico para `CLAUDE.md`; sem permissão de link simbólico (Windows comum), vira cópia gerada
do mesmo conteúdo, e a conferência é a mesma: igualdade de conteúdo.

Cada subcomando também roda sozinho; `python contexto.py` sem argumento imprime a ajuda.

## Os arquivos

| Arquivo | Papel |
|---|---|
| `contexto.py` | os subcomandos `selecionar`, `compactar`, `registrar`, `historico`, `transferir`, `rastrear`, `inspecionar` |
| `rodar.sh` | os doze passos, em ordem |
| `saida-esperada.txt` | a saída de `bash rodar.sh`, conferida em 02/11/2026 |
| `projeto/CLAUDE.md`, `projeto/AGENTS.md` | a instrução para a IA, em duas cópias escritas à mão que já divergiram |
| `projeto/skills/*/SKILL.md` | três skills no disco; uma (`jornada-viva`) não aparece em instrução nenhuma |
| `projeto/specs/007-cupom-de-desconto/` | spec (com invariantes e o fechamento do ciclo), plano, tarefas e relatório |
| `projeto/src/*.py` | o código: seis módulos de tamanhos diferentes, gerados para o exemplo |
| `projeto/registros/decisoes.jsonl` | o índice de decisões só-acréscimo (três linhas) |
| `projeto/registros/commits.txt` | o assunto de quatro commits, no formato `git log --format='%h %s'` |
| `projeto/docs/adr/0003-cupom-nao-acumula.md` | o porquê de uma regra de negócio |
| `casos/conversa.md` | o que existiu só na janela de contexto, e não em artefato |
| `casos/tasks-com-cauda.md` | o `tasks.md` reescrito: T3 autossuficiente, T4 fora (vira outro ciclo), cauda como token `TAIL:` |
| `casos/decisoes-reescrito.jsonl` | o índice com a linha 2 editada (de "aberta" para "fechada") |

A régua de tokens é **estimada** (caracteres ÷ 4, arredondado para cima) e está declarada no
código. Serve para a razão selecionado ÷ total, não para prever a fatura de um modelo.

## Saída esperada

Os passos 2, 3, 4, 7 (duas vezes), 8 (a segunda chamada), 9, 11 e 12 saem com código 1 **de
propósito**: são as falhas que o capítulo descreve.

```text

== 1. seleção: uma tarefa cortada pela fronteira carrega pouco do repositório
seleção 007/T2
  + spec.md (contexto integrador)        230 tokens
  + T2 (a linha da tarefa)                30 tokens
  + src/cupom.py                          99 tokens
  + src/carrinho.py                      105 tokens
  selecionado 464 de 4777 tokens do repositório inteiro → economia 90%
✓ corte por fronteira: a tarefa cabe no que ela mesma declara.
(exit 0)

== 2. seleção: a tarefa que atravessa o código inteiro — economia baixa é sinal de corte errado
seleção 007/T4
  + spec.md (contexto integrador)        230 tokens
  + T4 (a linha da tarefa)                57 tokens
  + src/cupom.py                          99 tokens
  + src/carrinho.py                      105 tokens
  + src/pagamento.py                     703 tokens
  + src/frete.py                         212 tokens
  + src/relatorios.py                   2152 tokens
  + src/usuarios.py                      337 tokens
  selecionado 3895 de 4777 tokens do repositório inteiro → economia 18%
✗ economia baixa: a tarefa atravessa fronteiras. Reveja o corte; não aumente a janela.
(exit 1)

== 3. seleção: a tarefa que não cita nada manda o executor procurar sozinho
seleção 007/T3
  + spec.md (contexto integrador)        230 tokens
  + T3 (a linha da tarefa)                18 tokens
  selecionado 248 de 4777 tokens do repositório inteiro → economia 94%
✗ a tarefa não cita arquivo: quem a executa vai procurar o contexto sozinho (ou na conversa).
(exit 1)

== 4. compressão: a janela compacta e só o tasks.md fica — a cauda morava na spec e na conversa
compactação 007: janela com spec.md, plan.md, tasks.md, conversa (573 tokens)
  → depois: só o que o executor segue, tasks.md (162 tokens)
  ✗ revisão em contexto fresco     APAGADO (estava em: spec.md, conversa)
  ✗ revisão de segurança           APAGADO (estava em: spec.md, conversa)
  ✗ gate humano antes do merge     APAGADO (estava em: spec.md, conversa)
  ✗ data dd/mm/aaaa na mensagem    APAGADO (estava em: conversa)
  ✗ T3 não se executa com contexto zero (sem arquivo/comando e critério →)
✗ 4 fato(s) apagado(s), 1 tarefa(s) presa(s) à conversa. O executor vai obedecer, com fidelidade, a versão truncada.
(exit 1)

== 5. compressão: a mesma janela, com a cauda como token no tasks.md
compactação 007: janela com spec.md, plan.md, tasks-com-cauda.md, conversa (607 tokens)
  → depois: só o que o executor segue, tasks-com-cauda.md (196 tokens)
  ✓ revisão em contexto fresco     sobrevive (está em tasks-com-cauda.md)
  ✓ revisão de segurança           sobrevive (está em tasks-com-cauda.md)
  ✓ gate humano antes do merge     sobrevive (está em tasks-com-cauda.md)
  ✓ data dd/mm/aaaa na mensagem    sobrevive (está em tasks-com-cauda.md)
✓ tudo o que importa está no artefato consumido: a compactação não apaga nada que conte.
(exit 0)

== 6. persistência: acrescentar uma decisão (numa cópia do índice)
✓ acrescentada como linha 4: achado-007-fecha-006
(exit 0)

== 7. persistência: o mesmo id de novo, e um registro que aponta para um marcador
✗ recusado: o id achado-006-mensagem-sem-data já existe. Corrigir é acrescentar uma linha nova com outro id (e o campo "fecha"), nunca reescrever.
(exit 1)
✗ recusado: o registro aponta um marcador (<pendente>), não uma evidência.
(exit 1)

== 8. persistência: o índice com uma linha acrescentada × o índice com uma linha reescrita
histórico: decisoes.jsonl (3 linhas) → decisoes.jsonl (4 linhas)
✓ só acréscimo: 1 linha(s) nova(s), nenhuma antiga tocada.
(exit 0)
histórico: decisoes.jsonl (3 linhas) → decisoes-reescrito.jsonl (3 linhas)
✗ linha 2 foi reescrita ou apagada: achado-006-mensagem-sem-data
  o que se pensava antes deixou de existir; a próxima sessão lê a versão nova como se sempre tivesse sido assim.
(exit 1)

== 9. transferência: CLAUDE.md e AGENTS.md escritos à mão, contra as skills do disco
transferência: a instrução que a IA lê × o disco (projeto)
  skills no disco: dod-verificavel, jornada-viva, revisar-diff
  ✗ CLAUDE.md  não cita jornada-viva
  ✗ AGENTS.md  não cita dod-verificavel, jornada-viva; sem a regra 'skills primeiro'
  ✗ CLAUDE.md e AGENTS.md divergem: duas cópias escritas à mão
✗ 4 deriva(s): a IA segue menos método do que o repositório declara.
(exit 1)

== 10. transferência: fonte única e bloco gerado do disco (numa cópia temporária)
transferência corrigida (numa cópia temporária do projeto):
  bloco de skills GERADO do disco:
    - `dod-verificavel` — Transforma critério vago em comando que passa ou falha.
    - `jornada-viva` — Documenta a jornada de tela com captura do build real e heurística datada.
    - `revisar-diff` — Revisão do diff em contexto fresco, só lacunas de correção.
  AGENTS.md passa a ter o conteúdo de CLAUDE.md
  skills no disco: dod-verificavel, jornada-viva, revisar-diff
  ✓ CLAUDE.md  cita toda skill e manda consultá-las
  ✓ AGENTS.md  cita toda skill e manda consultá-las
  ✓ CLAUDE.md e AGENTS.md: mesmo conteúdo (fonte única)
✓ instrução coerente: skill nova sem entrada na instrução passa a ser impossível.
(exit 0)

== 11. rastreabilidade: do gate ao porquê, de trás para frente
rastreio, de trás para frente, a partir de gate-main-b7e41c2
  1. índice     gate-main-b7e41c2 (2026-09-05) → commit b7e41c2
  2. commit     b7e41c2 feat(carrinho): cupom de desconto substitui, nunca soma (ciclo 007, ADR 0003)
  3. ciclo      specs/007-cupom-de-desconto/ (spec.md · plan.md · tasks.md · qa-report.md)
  4. porquê     docs/adr/0003-cupom-nao-acumula.md
  elos: 3 de 4 commits citam ciclo ou ADR
  ✗ sem citação: 41c88e0 fix: ajusta mensagem  (de onde veio? só a memória de alguém sabe)
(exit 1)

== 12. o quadro: as quatro operações do ciclo 007 numa tela
inspeção de contexto do ciclo 007-cupom-de-desconto
  seleção       T1:   263/4777 tokens, economia 94%  ok
  seleção       T2:   464/4777 tokens, economia 90%  ok
  seleção       T3:   248/4777 tokens, economia 94%  presa à conversa
  seleção       T4:  3895/4777 tokens, economia 18%  corte errado?
  seleção       T5:   246/4777 tokens, economia 94%  ok
  compressão    4 fato(s) apagado(s) se a janela compactar agora  ✗
  persistência  3 decisão(ões) no índice; a última: gate-main-b7e41c2
  transferência deriva na instrução  ✗
  rastreio      há commit sem citação  ✗
(exit 1)
```
