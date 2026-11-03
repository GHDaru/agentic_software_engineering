# Exemplo do capítulo 7 — papéis e skills como arquivos que um portão confere

Dois scripts, só com a biblioteca padrão do Python 3.8+. Nenhum chama modelo de IA: o que se
confere é a **forma** que faz de um prompt um papel (escopo, contrato, permissões, faixa de
modelo, tamanho) e de um texto uma skill (gatilho, lei de ferro, dor de origem, linha de
base, consumidor). Se a forma não existe, o modelo nem chega a ter a chance de obedecer.

| Arquivo | O que é |
|---|---|
| `time/modelo-operacional.md` | a **norma**: a tabela de papéis de um time fictício (1 humano, 6 papéis de agente) |
| `time/papeis/*.md` | os **executáveis**: um perfil por papel, com front matter (`papel`, `ferramentas`, `julga`, `modelo`, `skills`) e o contrato Faz / Não faz / Consome / Produz / Entrega a |
| `time/skills/*/SKILL.md` | duas skills no formato `SKILL.md`, cada uma com `linha-de-base.md` (ilustrativa: registra o formato, não uma medição) |
| `confere.py` | aplica as dez regras (P1–P6 de papel, S1–S4 de skill) e prova, com dez mutações, que cada regra acusa |
| `mede.py` | mede uma pasta de perfis: linhas, bytes, ~tokens, ferramentas, se escreve, se declara modelo |
| `saida-esperada-*.txt` | as saídas de referência |

## Como rodar

```bash
cd livro/07-papeis-e-skills/exemplo
python confere.py      > /tmp/c.txt; diff /tmp/c.txt saida-esperada-confere.txt && echo "confere: igual"
python mede.py time/papeis > /tmp/m.txt; diff /tmp/m.txt saida-esperada-mede.txt && echo "mede: igual"
```

No Windows com Git Bash, use `python` (o `python3` do Git Bash pode ser um atalho vazio).
O `confere.py` sai com 0 quando o time está conforme **e** as dez mutações foram acusadas
pela regra certa; 1 se não.

Para medir os agentes do Maestro na versão citada pelo livro (precisa de um clone de
`https://github.com/GHDaru/maestro`):

```bash
mkdir -p /tmp/m19 && git -C <clone-do-maestro> archive 19823c2 .claude/agents | tar -x -C /tmp/m19
python mede.py /tmp/m19/.claude/agents > /tmp/mm.txt
diff /tmp/mm.txt saida-esperada-mede-maestro-19823c2.txt && echo "maestro: igual"
```

## As regras

| Regra | O que exige | De onde vem no Maestro (`19823c2`) |
|---|---|---|
| P1 | todo papel de agente que a norma prescreve tem um perfil que o entrega | `scripts/check-roles.sh` (nasceu no ciclo 018) |
| P2 | todo perfil entrega um papel que a norma prescreve (sem papel órfão) | idem, no sentido inverso (ciclo 039 fez o índice × disco nos dois sentidos) |
| P3 | papel que julga não tem `Write`/`Edit`; com `Bash`, aviso | corolário C3; `scripts/check-agents.sh` |
| P4 | o contrato tem Faz, Não faz, Consome, Produz, Entrega a | formato de `.claude/agents/*.md` (escopo, faz/não faz, consome/produz, *handoff*) |
| P5 | o perfil cabe no teto de 40 linhas | corolário C8 ("agente estreito é mais barato que agente capaz") |
| P6 | o papel declara a faixa de modelo (`pequeno`, `medio`, `grande`) | **não existe no Maestro** — é a recomendação do capítulo para a lacuna papel × modelo × custo |
| S1 | a `description` da skill traz o gatilho ("Use quando") | `skills/README.md`; agente `skill-author` |
| S2 | a skill abre com a lei de ferro em bloco, "Violar a letra…" e ≥ 2 desculpas fechadas | ciclo 011 (Iron Laws, absorvidas do Superpowers) |
| S3 | a skill diz de que dor nasceu e tem linha de base com SEM e COM a skill | regra de nascimento do `skills/README.md`; protocolo do `skill-author` |
| S4 | toda skill tem um papel que a consome; nenhum papel cita skill inexistente | a coluna "Consumed by" do `skills/README.md`; achado `achado-063-quatro-skills-sem-capitulo` (a mesma família: o que existe sem quem consuma) |

## Saída esperada — `confere.py`

```text
== papel × modelo × custo fixo de contexto
  perfil                  julga  modelo    linhas  ~tokens
  arquiteto               não    grande        21      180
  especificador           não    medio         21      184
  implementador           não    medio         21      176
  revisor                 sim    grande        21      203
  seguranca               sim    medio         21      164
  semantica-de-interface  não    medio         21      212
  total                                       126     1119

== o time como está
  ✓ dez regras conformes

== mutações (cada uma deve ser acusada pela SUA regra)
  ✓ M1 o papel de interface perde o agente: P1 acusou — 'Semântica de interface' é prescrito pelo modelo e nenhum perfil o entrega
  ✓ M2 o modelo deixa de citar a segurança: P2 acusou — perfil 'seguranca' entrega 'Segurança', que o modelo não prescreve
  ✓ M3 o revisor ganha caneta: P3 acusou — 'revisor' julga e tem Edit
  ✓ M4 o implementador perde o 'Não faz': P4 acusou — 'implementador' sem: Não faz:
  ✓ M5 o arquiteto incha: P5 acusou — 'arquiteto' tem 46 linhas (teto 40)
  ✓ M6 o especificador esquece o modelo: P6 acusou — 'especificador' não declara a faixa de modelo (pequeno|medio|grande)
  ✓ M7 a skill perde o gatilho: S1 acusou — skill 'criterio-verificavel' sem gatilho ('Use quando') na description
  ✓ M8 a lei vira sugestão: S2 acusou — skill 'diagnosticar-antes-de-consertar' sem lei de ferro completa (lei=sim, desculpas fechadas=3)
  ✓ M9 a skill nasce sem linha de base: S3 acusou — skill 'criterio-verificavel' sem linha de base (linha-de-base.md)
  ✓ M10 ninguém consome a skill: S4 acusou — skill 'diagnosticar-antes-de-consertar' não é consumida por nenhum papel (skill órfã)

resultado: time conforme · mutações acusadas: 10/10
```

O `~tokens` é bytes ÷ 4, uma aproximação grosseira e só comparativa; o total da tabela soma
os arredondamentos por linha, por isso difere em 1 do total do `mede.py`.

## Saída esperada — `mede.py` nos agentes do Maestro em `19823c2`

```text
perfil                 linhas  bytes  ~tok  escreve modelo  ferramentas
agent-designer             24   1493   373  sim     —       Read, Write, Edit, Grep
dev-implementer            22   1124   281  sim     —       Read, Write, Edit, Bash
didactics-editor           20    916   229  sim     —       Read, Write, Edit, Grep
plan-architect             23   1375   344  sim     —       Read, Write, Grep, Glob, WebFetch
process-guardian           21   1080   270  não     —       Read, Grep, Glob
qa                         18    754   188  sim     —       Read, Write, Bash
research-curator           18    966   242  sim     —       Read, Write, WebSearch, WebFetch
review                     19    936   234  não     —       Read, Grep, Glob, Bash
security                   18    813   203  não     —       Read, Grep, Glob, Bash
skill-author               30   1682   420  sim     —       Read, Write, WebFetch
spec-agent                 18    900   225  sim     —       Read, Write, Grep, Glob
tech-writer                18    875   219  sim     —       Read, Write, Edit, Grep
ux-semantics               36   1923   481  sim     —       Read, Write, Grep, Glob

perfis: 13 · linhas: 285 (média 21.9, menor 18, maior 36) · bytes: 14837 (~3709 tokens)
sem escrita (Write/Edit): 3 → process-guardian, review, security
com modelo declarado: 0 de 13
```

Duas leituras que o capítulo usa: os treze perfis somam 285 linhas, e não as 267 que o
corolário C8 ainda cita (o número envelheceu enquanto o `ux-semantics` ganhou a lei de ferro e
o `skill-author` o protocolo de teste); e nenhum perfil declara modelo.

## O que este exemplo não prova

Ele prova a **forma**, não o comportamento. Um perfil conforme pode ser ignorado pelo modelo;
uma lei de ferro pode ser racionalizada; uma linha de base pode ter sido escrita sem rodar
nada (as duas desta fixture são ilustrativas e dizem isso). O comportamento se prova com
avaliação contra uma linha de base e ablação — o capítulo 15 trata do desenho; o Maestro tem
dois casos em `evals/`.
