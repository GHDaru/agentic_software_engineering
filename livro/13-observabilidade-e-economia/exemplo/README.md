# Exemplo do capítulo 13 — quanto custa uma tarefa aceita

Dois scripts e dois livros de ponto. O primeiro script deriva as métricas de economia do capítulo;
o segundo projeta o mesmo registro no formato do OpenTelemetry (OTel), com minimização provada
por mutação.

| Arquivo | O que é |
|---|---|
| `tarefas-064.jsonl` | cópia byte a byte de `docs/records/tarefas.jsonl` do Maestro na versão `19823c2` — o único ciclo que o livro de ponto mediu |
| `sintetico.jsonl` | livro pequeno e redondo (três tarefas, quatro revisões) para conferir a conta à mão |
| `economia.py` | custo por tipo, tokens com e sem *cache*, vereditos válidos e descartados, custo por tarefa aceita × ingênuo, retrabalho por tentativa × por linhagem, tempo de ciclo, órfãos |
| `projetar_otel.py` | *spans* no formato OTel, nomes `gen_ai.*`, lista de permissão de campos e o portão que reprova se algo fora da lista sair |

Proveniência da cópia (o *hash* tem de bater):

```bash
git -C <maestro> show 19823c2:docs/records/tarefas.jsonl | sha256sum
# 590ff5da4dcc8cf3d701f6ed359207d41628e76cea8e3bdd9e5a993b013f4c69
sha256sum tarefas-064.jsonl      # o mesmo valor
```

## Como rodar

Requisito: Python 3.8 ou mais novo, só biblioteca padrão. No Git Bash do Windows, onde `python3`
pode ser um atalho vazio, use `python`; se o console reclamar de codificação, exporte
`PYTHONUTF8=1`.

```bash
cd livro/13-observabilidade-e-economia/exemplo
python3 economia.py                      # o livro do Maestro
python3 economia.py sintetico.jsonl      # o livro sintético
python3 projetar_otel.py                 # projeção OTel, minimizada
python3 projetar_otel.py --sem-filtro    # a mutação: tem de reprovar
python3 projetar_otel.py --json          # todos os spans, para inspecionar
```

## Saída esperada

### `python3 economia.py` — sai com código 0

```text
livro: tarefas-064.jsonl · 52 eventos · 0 linha(s) inválida(s)
tentativas: 16 com stop (13 medidas, 3 sem medida: 064-T7#2, 064-F3#1, 064-F7#1)

1. Custo por tipo de tarefa (só tentativas medidas)
   review      2 tentativa(s)  US$  6.3429   51.3 %
   fix         4 tentativa(s)  US$  2.5580   20.7 %
   implement   5 tentativa(s)  US$  2.1450   17.4 %
   docs        2 tentativa(s)  US$  1.3102   10.6 %
   total      13               US$ 12.3561

2. Tokens por tentativa medida
   média total: 2,265,740 tokens · média sem cache (entrada+saída): 19,090 tokens
   taxa de cache (lido / entrada total): 96.7 %

3. Vereditos
   válidos (dados por tarefa review/audit, na sessão que a executou): 2
   descartados (dados por quem não julga): 5 -> 064-T2<-manager-claude-e8, 064-T3<-manager-claude-e8, 064-T4<-manager-claude-e8, 064-T5<-manager-claude-e8, 064-cycle<-064-R1

4. Custo por tarefa aceita
   ingênuo (custo ÷ tarefas executadas, sem juízes): 12 tarefa(s), US$ 1.0297 — não diz nada sobre o que foi aceito
   n/a: nenhuma TAREFA tem veredito válido — o número não é calculado, para não ser inventado
   ciclo aceito (064-cycle, por 064-R2): custo do ciclo inteiro US$ 12.3561

5. Retrabalho
   (a) por tentativa (attempt >= 2): 1 medida(s), US$ 0.1312
   (b) por linhagem (da 1ª reprovação até a aceitação): 5 tentativa(s), US$ 5.7457 medidos = 46.5 % do total (+1 sem medida: 064-F3#1)
   iniciadas depois dessa aceitação (fora da conta): 064-F6, 064-F7

6. Tempo de ciclo e órfãos
   do primeiro evento à aceitação: 42.9 min
   do primeiro ao último evento: 46.8 min
   órfãos (start sem stop = trabalho pago e não entregue): 0
```

Os números das seções 1, 2 e 5(a) e a contagem de vereditos descartados batem com o relatório
oficial do Maestro (`scripts/report-tasks.py` em `19823c2`, rodado sobre o mesmo arquivo:
US$ 12.3561, 96.7 %, US$ 0.1312, "verdicts from non-judges: 5"). O que o relatório oficial não
mostra é a linha 5(b): o retrabalho por linhagem — F1, F2, F3, F4 e a segunda revisão, R2 — é
cerca de 44 vezes o retrabalho por tentativa.

O "064-cycle<-064-R1" descartado é a cópia do veredito de R1 que a sessão gerente gravou "se
estivesse faltando"; o original, gravado na sessão de R1, é um dos dois válidos.

### `python3 economia.py sintetico.jsonl` — sai com código 0

```text
livro: sintetico.jsonl · 29 eventos · 0 linha(s) inválida(s)
tentativas: 8 com stop (8 medidas, 0 sem medida: -)

1. Custo por tipo de tarefa (só tentativas medidas)
   implement   4 tentativa(s)  US$  3.5000   81.4 %
   review      4 tentativa(s)  US$  0.8000   18.6 %
   total       8               US$  4.3000

2. Tokens por tentativa medida
   média total: 53,750 tokens · média sem cache (entrada+saída): 5,375 tokens
   taxa de cache (lido / entrada total): 98.6 %

3. Vereditos
   válidos (dados por tarefa review/audit, na sessão que a executou): 4
   descartados (dados por quem não julga): 1 -> 900-C<-gerente

4. Custo por tarefa aceita
   ingênuo (custo ÷ tarefas executadas, sem juízes): 3 tarefa(s), US$ 1.4333 — não diz nada sobre o que foi aceito
   2 tarefa(s) aceita(s): US$ 2.1500 por tarefa aceita (custo total do livro ÷ tarefas aceitas)

5. Retrabalho
   (a) por tentativa (attempt >= 2): 1 medida(s), US$ 0.5000
   (b) por linhagem (da 1ª reprovação até a aceitação): 2 tentativa(s), US$ 0.7000 medidos = 16.3 % do total
   iniciadas depois dessa aceitação (fora da conta): 900-C, 900-RC

6. Tempo de ciclo e órfãos
   do primeiro evento à aceitação: 20.0 min
   do primeiro ao último evento: 28.0 min
   órfãos (start sem stop = trabalho pago e não entregue): 0
```

A conta à mão. Implementações: A = 1,00; B#1 = 1,00 (reprovada); B#2 = 0,50 (aprovada); C = 1,00
(reprovada). Revisões: 4 × 0,20 = 0,80. Total = 4,30. Aceitas: A e B → 4,30 ÷ 2 = **2,15**.
Executadas: A, B, C → 4,30 ÷ 3 = **1,4333**. A diferença é o preço de C, que foi paga e não
aprovada. O "approved" que o gerente escreveu sobre C é descartado: gerente não é juiz. Retrabalho
por linhagem = B#2 + a revisão de B#2 = 0,50 + 0,20 = **0,70**.

Limite da linha 5(b), declarado: o script mede a linhagem a partir da **primeira** reprovação
válida do livro até a aceitação seguinte. Serve para um ciclo com uma revisão de ciclo (o caso do
Maestro); num livro com várias tarefas reprovadas em paralelo, a conta certa é por alvo, e fica
como exercício.

### `python3 projetar_otel.py` — sai com código 0

```text
52 eventos -> 1 trace(s), 19 span(s), 7 com veredito
ficaram para trás (minimização): cost_start_usd×13, note×7, reason×7, redoes×5, session×52, to×13, tokens_by_model×13, tokens_subagents×13
um span, por exemplo:
{
 "trace_id": "5e18d34a87ed6c9bea50e24d898c9c7b",
 "span_id": "1d50d04fd6f79c3f",
 "name": "064-T2#2",
 ...
 "attributes": {
  "esoa.task.kind": "implement",
  "esoa.task.attempt": 2,
  "gen_ai.request.model": "claude-sonnet-5-5",
  "gen_ai.operation.name": "invoke_agent",
  ...
  "gen_ai.usage.input_tokens": 12,
  "gen_ai.usage.output_tokens": 1672,
  ...
 },
 "events": [ { "name": "verdict", ... "esoa.verdict": "approved_with_notes", ... } ]
}
✓ nenhum atributo fora da lista de permissão
```

(O JSON do *span* sai inteiro; acima, abreviado com `...`.) Os 19 *spans* são as 16 tentativas
mais 3 *spans* sem duração para os vereditos do ciclo inteiro. Os textos livres (`reason`,
`note`), os identificadores de sessão e o destinatário (`to`) nunca saem.

### `python3 projetar_otel.py --sem-filtro` — sai com código 1

A mutação desliga a lista de permissão. A última linha tem de ser:

```text
✗ VAZOU atributo fora da lista de permissão: attempt×16, cost_start_usd×13, kind×16, note×4, reason×7, redoes×2, session×23, tokens_by_model×13, tokens_subagents×13
```

Se esta linha não aparecer, o portão de minimização é decoração (capítulo 10): ele não viu o
vazamento que você provocou de propósito.

## O que fazer com isto no seu time

Troque o livro pelo seu. O formato mínimo de cada linha é `ts`, `event` (`assigned`, `start`,
`stop`, `verdict`) e `task_id`; `stop` carrega `attempt`, `kind`, `cost_usd` e os tokens por
categoria; `verdict` carrega `verdict`, `by` (o id da tarefa de revisão) e `session`. Qualquer
*harness* que deixe ler o uso de tokens de uma sessão consegue gravar isso.
