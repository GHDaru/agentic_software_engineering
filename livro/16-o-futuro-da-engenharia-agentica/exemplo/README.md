# Exemplo do capítulo 16 — sensibilidade, gatilhos e calendário

Um script, `futuro.py`, em Python 3 (3.8 ou mais novo), sem dependência externa. Os dados estão
em `dados/`:

| Arquivo | O que é | Fonte |
|---|---|---|
| `axiomas.json` | de quais axiomas cada teorema deriva, e de quais teoremas/axiomas cada corolário | `maestro@19823c2:docs/governance/axioms.md` |
| `estado.jsonl` | o índice do catálogo do ecossistema, como está | `maestro@19823c2:docs/ecosystem/estado.jsonl` |
| `eventos.jsonl` | eventos que tocaram gatilhos, cada um com prova (proposta do livro) | spec do ciclo 065; commits `d5feef2` e `d71cee6` |
| `ai-act.json` | marcos do *AI Act*, data original e data alterada, com data da última conferência (`conferido_em`) e validade | Regulamento (UE) 2024/1689, art. 113, alterado pelo Regulamento (UE) 2026/1744 — conferido em eur-lex.europa.eu em 02/11/2026; material didático, não parecer jurídico |

## Como rodar

Da raiz do livro:

```bash
python livro/16-o-futuro-da-engenharia-agentica/exemplo/futuro.py demo
```

Outros comandos:

```bash
python futuro.py sensibilidade A3 A4                      # cenário: quais regras perdem apoio
python futuro.py gatilhos ESTADO.jsonl EVENTOS.jsonl      # sai 1 se algum gatilho disparou sem reavaliação
python futuro.py calendario 2027-12-02                    # o que do AI Act vale nessa data (sai 1 se o dado venceu)
```

Códigos de saída: 0 = conforme · 1 = achado · 2 = erro de uso.

## Saída esperada (`demo`, código 0)

```text
1. Sensibilidade do método à próxima geração de modelos
 a) cenário 'janela maior e que não degrada' (A3 enfraquece)
  axiomas enfraquecidos: A3
  teoremas expostos   3/7: T2 T5 T6
  teoremas sem apoio  0/7: -
  teoremas intactos   4/7: T1 T3 T4 T7
  corolários expostos 7/13; sem apoio 0/13: -
 b) cenário 'janela maior e memória persistente do fornecedor' (A3 e A4 enfraquecem)
  axiomas enfraquecidos: A3, A4
  teoremas expostos   6/7: T1 T2 T4 T5 T6 T7
  teoremas sem apoio  2/7: T5 T6
  teoremas intactos   1/7: T3
  corolários expostos 12/13; sem apoio 4/13: C1 C9 C10 C12
 c) cenário de controle: o que nenhum modelo muda (A1, A2, A5) segue de pé
  axiomas enfraquecidos: (nenhum)
  teoremas expostos   0/7: -
  teoremas sem apoio  0/7: -
  teoremas intactos   7/7: T1 T2 T3 T4 T5 T6 T7
  corolários expostos 0/13; sem apoio 0/13: -

2. Gatilhos de reavaliação: escritos × vigiados (índice real, maestro@19823c2)
 a) o índice como está
  ideias em 'observar': 16
  portão antigo (todo 'observar' tem gatilho?): VERDE
  portão novo (algum gatilho disparou sem reavaliação?): VERMELHO — 2
    ✗ trilha-com-custo: estado 'observar' desde 2026-07-31; gatilho: "alguem precisar responder quanto custou este ciclo com numero, e nao com estimativa"
        disparado em 2026-10-12: o humano pede o custo com número ('Quero ver quanto estou gastando') e o ciclo 065 constrói o livro de ponto [maestro@19823c2:specs/065-o-metodo-se-cobra-e-bate-o-ponto/spec.md; ADR 0021]
    ✗ worktree-por-task: estado 'observar' desde 2026-08-10; gatilho: "dois ou mais agentes escrevendo no mesmo repositorio ao mesmo tempo, com conflito observado"
        disparado em 2026-10-20: ciclo 066 entrega lançador de sessões por modelo e worktree (agentes em paralelo no mesmo repositório) [maestro commit d5feef2]
        disparado em 2026-10-25: ciclo 072 integra a worktree de um trabalhador com 'conflitos resolvidos' na mensagem do commit [maestro commit d71cee6]
 b) depois de anexar uma linha de reavaliação para cada ideia disparada
  ideias em 'observar': 15
  portão antigo (todo 'observar' tem gatilho?): VERDE
  portão novo (algum gatilho disparou sem reavaliação?): VERDE — nenhum

3. O relógio regulatório: AI Act
 a) em 2026-11-02
  data consultada: 2026-11-02
  frescor do dado: OK — conferido em 2026-11-02, válido até 2027-01-31
    proibições originais (art. 5) e letramento em IA (art. 4)
      original 2025-02-02 (aplica) · alterado 2025-02-02 (aplica) · conteúdo mudou? sim no art. 4: o 2026/1744 o reescreve como 'tomar medidas que apoiem' o letramento, sem exigir nível garantido
  ↻ proibições novas: imagem íntima sem consentimento e abuso sexual infantil (art. 5(1)(ba)(bb), 5(1a), 5(1b))
      original não existia · alterado 2026-12-02 (ainda não) · conteúdo mudou? sim: proibição nova, criada pelo 2026/1744
    modelos de IA de uso geral (cap. V), governança e penalidades (art. 113, alínea b)
      original 2025-08-02 (aplica) · alterado 2025-08-02 (aplica) · conteúdo mudou? pouco: arts. 51–55 intactos; mudam o art. 56(6) (códigos de prática) e o art. 99 (penalidades)
    transparência do art. 50 (avisar que se fala com IA; marcar conteúdo sintético)
      original 2026-08-02 (aplica) · alterado 2026-08-02 (aplica) · conteúdo mudou? pouco: só o art. 50(7) (códigos de prática) é reescrito
  ↻ marcação de conteúdo sintético (art. 50(2)) para sistema generativo no mercado antes de 2026-08-02
      original 2026-08-02 (aplica) · alterado 2026-12-02 (ainda não) · conteúdo mudou? não: o 2026/1744 dá prazo de transição (art. 111(4))
  ↻ alto risco do Anexo III (emprego, crédito, educação...): cap. III, seções 1 a 3
      original 2026-08-02 (aplica) · alterado 2027-12-02 (ainda não) · conteúdo mudou? sim, em parte: arts. 9, 12, 13, 14 e 15 intactos; arts. 6, 10 e 11 alterados; legado só entra se mudar de forma significativa (art. 111(2))
  ↻ alto risco embutido em produto regulado (art. 6(1), Anexo I)
      original 2027-08-02 (ainda não) · alterado 2028-08-02 (ainda não) · conteúdo mudou? sim, em parte: o mesmo das linhas acima, mais mudanças no Anexo I
  marcos com data alterada ou criados: 4 de 7
 b) o mesmo dado consultado em 2027-03-01, sem nova conferência
  frescor do dado: VENCIDO — conferido em 2026-11-02, vencido desde 2027-01-31: reconfira no Jornal Oficial

roteiro: OK — os resultados esperados apareceram
```

## O que o "OK" prova, e o que não prova

As partes 1 e 3 conferem a **coerência do script com os próprios dados**: `axiomas.json` foi
copiado à mão de `axioms.md`, e `ai-act.json` foi digitado a partir do Jornal Oficial. Um erro
de cópia passa verde. A parte 2 é a única independente, porque lê o índice real do catálogo.
O que a parte 3 acrescenta de não circular é o **frescor**: o dado carrega `conferido_em` e
`validade_dias`, e o script recusa responder (sai 1) quando a data consultada passou da
validade. Isso não prova que as datas estão certas; obriga alguém a reconferi-las.
