# Protocolo de execução da agenda H1–H10

> Versão 0.1 · 02/11/2026 · estado: **rascunho, não ratificado pelo Darú, nenhum *run* sob ele**.
> Origem: [`base-de-pesquisa.md`](base-de-pesquisa.md), seção «Agenda de pesquisa» (desenho,
> métricas e a linha «No repositório»: `protocol.md` + `runs/` com *schema* imutável, telemetria
> compatível com OpenTelemetry com minimização, LGPD). As hipóteses, as métricas e o critério de
> refutação de cada uma estão em [`hipoteses.md`](hipoteses.md); este arquivo diz **como** se roda.
> Apresentação no livro: [Apêndice C](../livro/apendices/c-pacote-de-replicacao/capitulo.md).

**Regra de congelamento deste arquivo.** Os parâmetros marcados *proposta* (repetições, nível do
intervalo, margens) congelam no *commit* que registrar o primeiro *run* em `pesquisa/runs/`.
Depois disso, mudar um parâmetro é uma versão nova do protocolo (0.2, 1.0…) e só vale para *runs*
posteriores; os anteriores continuam analisados pela versão sob a qual rodaram. Fixar margem
depois de ver o resultado é proibido pelo mesmo motivo que reescrever um ADR (Architecture
Decision Record).

## 1. Braços

| Braço | O agente recebe | Arquivo de instruções do *runner* |
|---|---|---|
| A — linha de base | só o *prompt* da tarefa | nenhum |
| B — spec | A + a tarefa como especificação escrita | `instrucoes/B-<tarefa>.md` |
| C — spec + portões | B + os portões automáticos executáveis no cenário (integração contínua, *fitness functions*) | `instrucoes/C-<tarefa>.md` + scripts dos portões |
| T — tratamento | o Maestro completo instalado no cenário (raias, papéis, revisão em contexto fresco, portões, ADRs, *skills*, *hooks*) | instalação do Maestro no *commit* congelado |

Cada braço contém o anterior; o contraste entre vizinhos isola uma camada (A×B, B×C, C×T).
Variações dentro de T (ligar/desligar uma peça: contexto seletivo, catálogo, glossário) são
**ablações** e levam o nome `T-sem-<peça>`. Os fatoriais da H4 (um × vários agentes, cortes
independentes × acoplados) e da H9 (modelo menor × maior, tarefa estruturada × aberta) usam os
mesmos braços como eixo fixo. A H10 é observacional e não usa braços (ver §7).

**Mesma tarefa em todos os braços.** Uma célula é *(tarefa, braço, modelo, harness)*. A tarefa
— o repositório de cenário no *commit*-base, o gatilho e o critério de aceitação — é idêntica em
todas as células comparadas; o que muda é só o que o braço acrescenta.

## 2. Repetições, distribuição e intervalo

O mesmo agente na mesma tarefa não produz a mesma saída duas vezes; por isso a unidade de
análise é a distribuição de cada célula, não um número.

| Parâmetro | Valor | Estado |
|---|---|---|
| repetições por célula (piloto) | 10 | proposta |
| repetições por célula (confirmatório) | fixadas pelo piloto, pela largura do intervalo, antes do confirmatório | proposta |
| métrica binária (aceitação na primeira passada, escape) | proporção com intervalo de Wilson a 95 % | proposta |
| métrica contínua (custo, *tokens*, tempo, retrabalho) | mediana e intervalo *bootstrap* percentil a 95 %, 10 000 reamostragens, semente registrada no *run* de análise | proposta |
| contraste entre braços | diferença (ou razão, para custo) com intervalo *bootstrap* pareado por tarefa | proposta |
| margem de não-inferioridade (H3, H9) | 5 pontos percentuais em aceitação na primeira passada | proposta |

Regras que não dependem dos valores:

- **Relatar a distribuição inteira**: n, mínimo, quartis, máximo e o intervalo. Média sozinha não
  entra no livro.
- **Falha do *harness* conta**. Um *run* em que o *harness* errou (autenticação, *timeout*) é
  registrado com `erro_do_harness` e excluído da métrica da tarefa, mas a taxa de erro por célula
  é relatada. Repetir até dar certo, sem registrar as falhas, é seleção de amostra.
- **Ordem sorteada**. As células rodam em ordem aleatória com semente registrada, para que
  mudança no provedor ao longo do dia não se confunda com efeito de braço.
- **Refutação**: a de [`hipoteses.md`](hipoteses.md) — o intervalo do contraste declarado inclui
  zero ou aponta contra; na não-inferioridade, o intervalo da perda passa da margem.

## 3. Congelamento do ambiente

Um *run* sem os campos abaixo não entra na análise. Todos vão no `run.json` (§4).

| Campo | O que registra | Como se obtém |
|---|---|---|
| `metodo.commit` | *commit* do Maestro instalado (braço T) ou `null` | `git -C <maestro> rev-parse HEAD`; para o livro, `19823c2` |
| `livro.commit` | *commit* deste repositório (fichas, *runner*, avaliador) | `git rev-parse HEAD` |
| `modelo.pedido` | o que se passou ao *harness* (pode ser apelido, ex.: `sonnet`) | argumento do *runner* |
| `modelo.resolvido` | o identificador versionado que o *harness* relatou ter usado | do log do *harness*; se ele não relata, `null` e o *run* é marcado `modelo_nao_verificado` |
| `harness.nome`, `harness.versao` | ex.: Claude Code e a versão do executável | `claude --version` (ou equivalente) |
| `cenario.base` | *commit*-base do repositório de cenário | o *runner* já registra (`base`) |
| `hashes` | SHA-256 de cada entrada: *prompt*, arquivo de instruções, ficha do caso, *runner*, avaliador | `sha256sum` (ou `hashlib`) antes de rodar |
| `sistema` | sistema operacional e versão do Python/Node usados pelo *runner* | `platform`, `sys.version` |
| `semente` | semente de sorteio de ordem (e do modelo, se o provedor aceitar) | registrada pelo *runner* |

Apelido de modelo não congela nada: o mesmo nome aponta para versões diferentes ao longo do
tempo. Por isso o campo que conta é `modelo.resolvido`.

## 4. `pesquisa/runs/` — *schema* imutável

Um diretório por *run*:

```text
pesquisa/runs/
  <AAAA-MM-DD>-<hipotese>-<tarefa>-<braco>-<NN>/
    run.json        ambiente congelado (§3) + resultado
    prompt.txt      exatamente o que o agente recebeu
    rastro.json     a saída do adaptador (ações, arquivos antes/depois)
    veredito.json   o julgamento do avaliador
    telemetria.jsonl  spans minimizados (§5), opcional
```

`run.json`, versão de *schema* 1:

```json
{
  "schema": 1,
  "id": "2026-11-15-H5-GOV-006-C-03",
  "protocolo": "0.1",
  "hipotese": "H5",
  "tarefa": "GOV-006",
  "braco": "C",
  "repeticao": 3,
  "metodo": {"commit": null},
  "livro": {"commit": "<sha>"},
  "modelo": {"pedido": "sonnet", "resolvido": "<id versionado ou null>"},
  "harness": {"nome": "claude-code", "versao": "<x.y.z>"},
  "cenario": {"base": "<sha>"},
  "hashes": {"prompt.txt": "sha256:<…>", "instrucoes": "sha256:<…>", "ficha": "sha256:<…>",
             "runner": "sha256:<…>", "avaliador": "sha256:<…>"},
  "sistema": {"os": "<…>", "python": "<…>"},
  "semente": 0,
  "inicio": "<ISO 8601 UTC>", "fim": "<ISO 8601 UTC>",
  "metricas": {"aceita_primeira_passada": null, "retrabalho": null, "tokens_entrada": null,
               "tokens_saida": null, "custo": null, "tempo_s": null},
  "erro_do_harness": null,
  "substitui": null
}
```

(O `id` acima é ilustrativo; nenhum *run* existe.)

**Imutável** significa:

1. Um diretório de *run*, uma vez commitado, não se edita nem se apaga.
2. *Run* errado se corrige com **outro** *run* cujo `substitui` aponta o `id` do errado; a análise
   usa o mais recente da cadeia e relata quantas substituições houve.
3. Campo novo exige `schema: 2`; *runs* de `schema: 1` continuam válidos e lidos como estão.
4. **A escrever** (ainda não existe): um portão `scripts/check-runs.sh` que confira, por *diff*
   contra o *commit* anterior, que nenhum arquivo sob `pesquisa/runs/` foi modificado ou removido,
   e que todo `run.json` tem os campos de §3. Até ele existir, a imutabilidade é regra, não fato.

**Relação com o que já existe.** O *runner* do ASEG-Bench
(`benchmarks/aseg-bench/executar_claude_code.py`) grava hoje `prompt.txt`, `rastro.json` e
`veredito.json` em `benchmarks/aseg-bench/execucoes/`, e o `veredito.json` tem oito campos (caso,
modelo, instruções, base, tarefa resolvida, erro do *harness*, violações, violações só de estado).
Faltam, para valer como *run* deste protocolo: versão do *harness* no próprio JSON (hoje só no
README da pasta), modelo resolvido, *commits* do método e do livro, hashes, semente e métricas de
custo. O *runner* aceita `--repeticoes` com padrão 1.

## 5. Telemetria compatível com OpenTelemetry, com minimização

A telemetria serve para medir custo, *tokens*, tempo e overhead de coordenação; não serve para
guardar o que o agente leu ou escreveu.

- **Formato**: *spans* exportáveis por OpenTelemetry (OTel), usando os nomes de atributo das
  convenções semânticas de IA generativa (`gen_ai.*`) quando existirem — por exemplo modelo
  pedido e resolvido, *tokens* de entrada e saída — e atributos próprios com prefixo `esoa.*`
  (braço, hipótese, tarefa, repetição, `id` do *run*). As convenções `gen_ai.*` ainda estão em
  desenvolvimento no projeto OpenTelemetry; o protocolo registra a versão das convenções usada.
- **Um *span* por**: *run*; chamada ao modelo; chamada de ferramenta; portão executado; espera
  humana; mensagem entre agentes (H4).
- **Minimização (Lei Geral de Proteção de Dados, LGPD, Lei 13.709/2018, art. 6º, III — princípio da
  necessidade)**. Por padrão **não** se registra: conteúdo de *prompt* ou de resposta, conteúdo de
  arquivo, saída de comando, caminhos absolutos da máquina, nome de usuário, e-mail, nomes de
  servidores e caminhos de memória do *harness*. Registra-se: contagens, durações, nomes de
  ferramenta, códigos de saída e hashes. O conteúdo necessário à auditoria já está, revisado, em
  `prompt.txt` e `rastro.json` (cenários sintéticos, sem dado pessoal).
- **Log bruto não se publica**. Como em `benchmarks/aseg-bench/execucoes/README.md`: a primeira
  linha do log do Claude Code descreve a máquina (servidores MCP, Model Context Protocol, e caminhos
  de memória). Quem quiser auditar o log refaz o *run* com o mesmo ambiente congelado.
- **Retenção**: *spans* brutos ficam na máquina de quem rodou e são descartados depois da análise;
  vai para o repositório só o `telemetria.jsonl` já minimizado. Tracing não é retenção
  indiscriminada.

## 6. Do *run* ao livro

1. Rodar as células (`--repeticoes` ≥ o valor do §2) com ordem sorteada.
2. Commitar os diretórios de `runs/` **antes** de rodar a análise.
3. Rodar a análise (script versionado, a escrever), que lê só `runs/` e grava o resultado com o
   `id` de cada *run* usado.
4. No capítulo, a afirmação entra com `[CLAIM-NN-NNN]` em estado `medido`, e a coluna «evidência
   reproduzível» aponta o comando da análise e o intervalo de `id`s de *run*.
5. Hipótese que o resultado refutou continua no livro, marcada refutada, com o *run* que a
   derrubou.

## 7. H10 (observacional)

Não há como sortear retrospectivas. A H10 usa o corpus de ciclos históricos do Maestro até
`19823c2`: para cada achado que virou regra (`docs/records/decisoes.jsonl`, *skill*
`anti-patterns`), conta-se a recorrência por ciclo antes e depois da data da regra. O resultado
é série temporal com intervalo, relatado como associação, nunca como efeito causal.

## Estado

| Item | Estado em 02/11/2026 |
|---|---|
| este protocolo | rascunho 0.1, não ratificado |
| `pesquisa/runs/` | não existe |
| `scripts/check-runs.sh` | não existe |
| script de análise | não existe |
| execuções reais anteriores ao protocolo | uma, em `benchmarks/aseg-bench/execucoes/2026-11-02-GOV-004-01/` (o *harness* recusou autenticação antes do primeiro passo; não conta como *run* deste protocolo) |
