# Exemplo executável do capítulo 15 — um corpus de avaliação que se prova

Uma miniatura, em Python 3 sem dependências, das duas metades que o Maestro tirou do teorema
T7: a **saúde do corpus** (o que o `check-evals.sh` mede) e a **prova por ablação** (o que o
comando `/eval` faz com um modelo no laço).

> **Aviso honesto.** As respostas em `corpus/*/respostas/` foram escritas à mão e o "juiz" casa
> palavras-sinal. Isso é um *proxy* (anti-padrão 13 do Maestro): mostra a mecânica, não
> substitui o julgamento de um modelo em contexto fresco. No Maestro real, `alvo.md` e
> `ablado.md` seriam as respostas de dois subagentes, um com a instrução inteira e outro sem a
> linha que o `Axis:` nomeia — e **só** isso: a mesma entrada, o mesmo modelo. A rodada
> ablada real do caso 001 do Maestro também reteve o plano da entrada, e por isso não isola o
> efeito da instrução sozinha (ver o capítulo, "A falha real").

Nos casos, FR1 e FR2 são requisitos funcionais (FR, de *functional requirement*) numerados
no plano. `/eval` é um comando do Claude Code no Maestro; em outro *harness*, o equivalente é
qualquer forma de abrir dois agentes em contexto limpo — um com a instrução inteira, outro sem
a linha do eixo — e guardar as duas respostas como `alvo.md` e `ablado.md`. O `avaliar.py` não
depende de harness nenhum.

## Estrutura

```text
exemplo/
├── avaliar.py                  o verificador (saúde + discriminação)
├── alvos/revisor.md            instrução do agente de revisão (alvo dos casos 001 e 003)
├── alvos/guardiao.md           instrução do guardião do processo (alvo do caso 002)
└── corpus/<NNN-slug>/
    ├── case.md                 Target · Question · Axis · a entrada (fatos, sem conclusões)
    ├── expect.md               MUST-FIND e MUST-NOT-CLAIM, no formato "texto :: sinal1; sinal2"
    ├── baseline.md             Date · Target-hash · First-red · Verdict · Ablation · Premise-checked
    └── respostas/alvo.md, respostas/ablado.md
```

Diferença deliberada em relação ao Maestro: lá a linha de base registra `Target-commit` (o
último commit que tocou o alvo, via git); aqui registra `Target-hash` (8 primeiros caracteres
do SHA-256 do arquivo, com fim de linha normalizado), para o exemplo rodar fora de um
repositório.

## Como rodar

```bash
cd livro/15-validando-o-maestro/exemplo
python avaliar.py            # ou python3, conforme o sistema
echo $?                      # 1 — vermelho de propósito
```

## Saída esperada

```text
── Corpus de avaliação (T7 / C11) ──
• 001-revisor-perde-requisito
  alvo: alvos/revisor.md
  asserções: 2 must-find / 2 must-not-claim
  linha de base atual (7c670133)
  alvo   PASSA
  ablado REPROVA (não achou: o requisito FR2 do plano não foi implementado; não achou: o teste não verifica comportamento; afirmou o proibido: basta apagar o TODO)
• 002-guardiao-aceita-raia-errada
  alvo: alvos/guardiao.md
  asserções: 1 must-find / 1 must-not-claim
  ✗ nunca visto reprovando (First-red: pending) — rode o caso contra o ablado
  linha de base atual (3b37f7fc)
  alvo   PASSA
  ablado PASSA
  ✗ o ablado PASSA — o caso não mede o eixo 'conferir a raia declarada (a linha "Confira a raia declarada" do alvo)'; aposente com motivo, não ajuste a fixture até ficar vermelho
• 003-sem-lado-negativo
  alvo: alvos/revisor.md
  ✗ sem MUST-NOT-CLAIM: — sem lado negativo o caso não discrimina
  ✗ nunca visto reprovando (First-red: pending) — rode o caso contra o ablado
  linha de base atual (7c670133)
──
casos: 3 · saudáveis: 1 · aposentados: 0
✗ o corpus não está saudável (veja acima).
```

Código de saída: **1**. O corpus sai vermelho como o `check-evals.sh` saiu no ciclo 037 do
Maestro: dizer "verde" com dois casos que não discriminam seria mentir para o próprio portão.

## Exercícios (cada um muda a saída de um jeito previsível)

1. **Aposente o 002 com motivo.** Acrescente no topo de `corpus/002-.../case.md`:
   `Status: retired` e `Retired-because: o ablado passa; o eixo é sobredeterminado pelo
   Princípio III`. O caso passa a aparecer como `APOSENTADO — ...`: visível, nunca apagado.
   Tire a linha `Retired-because:` e ele volta a falhar ("aposentar sem motivo é apagar").
2. **Conserte ou retire o 003.** Sem o 003 e com o 002 aposentado, a saída termina em
   `✓ todo caso nomeia um alvo real, discrimina e está atual.` e o código de saída é **0**.
3. **Mude o alvo.** Acrescente qualquer linha em `alvos/revisor.md` e rode de novo: o caso 001
   acusa `linha de base defasada — o alvo mudou 7c670133 → <novo>; avalie de novo`. É o
   corolário C11: a avaliação envelhece quando o alvo muda.
4. **Afrouxe o lado negativo.** Apague as duas linhas `MUST-NOT-CLAIM:` do 001: o caso cai na
   mesma falha estrutural do 003, embora o alvo real continue passando.
5. **Vaze a conclusão.** Escreva na entrada do `case.md` do 001 "o FR2 não foi implementado".
   O verificador continua verde — o anti-padrão 20 (fixture que carrega o próprio veredito) só
   o pré-voo humano do `/eval` pega. Nenhum script mede isso aqui, e o exemplo não finge medir.

Testado em 02/11/2026 com Python 3 no Windows (Git Bash); a saída acima foi copiada da execução.
