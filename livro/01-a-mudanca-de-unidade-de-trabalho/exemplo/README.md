# Exemplo do capítulo 1 — o custo por mudança aceita

Um modelo de valor esperado, determinístico, que responde à pergunta do capítulo com números
que você pode mudar: **se gerar ficou barato, para onde foi o custo?**

## O que tem aqui

| Arquivo | O que é |
|---|---|
| `economia.py` | o modelo (só biblioteca padrão, Python 3.8+) |
| `cenarios.json` | os parâmetros de seis cenários e da análise de sensibilidade |
| `saida-esperada.txt` | a saída que o modelo produz com os parâmetros deste repositório |

## O modelo

Por mudança, em horas-equivalentes:

```text
gerar     = g * (1 + p*d)        o que a verificação recusou é gerado de novo
verificar = v * (1 + p*d)        e verificado de novo
desfazer  = p * (1 - d) * u * b  o erro que escapou arrasta o lote inteiro
total     = gerar + verificar + desfazer
```

`g` gerar · `v` verificar · `p` chance de a mudança estar errada (defeito ou intenção errada) ·
`d` fração dos erros que a verificação pega antes de integrar · `u` custo de desfazer um erro
que escapou · `b` tamanho do lote integrado de uma vez.

**Os parâmetros são ilustrativos, não medidos.** O modelo não diz quanto custa o seu time;
diz *como o custo se redistribui* quando `g` cai. Troque os números pelos seus.

## Como rodar

```bash
cd livro/01-a-mudanca-de-unidade-de-trabalho/exemplo
python economia.py               # imprime a tabela
python economia.py --conferir    # 0 = bate com saida-esperada.txt; 1 = diverge (mostra a linha)
python economia.py --cenarios meus-cenarios.json   # seus parâmetros
```

No Git Bash do Windows, `python3` pode ser um atalho vazio: use `python`.

## Saída esperada

```text
CUSTO POR MUDANCA ACEITA (horas-equivalentes; parametros ilustrativos)

   cenario                                   gerar  verif   desf  total  %gerar
A  humano digita, revisao comum               8.84   1.10   0.81  10.76   82.2%
B  agente sem verificacao, lote grande        0.25   0.00  18.00  18.25    1.4%
C  agente + verificacao, lote grande          0.30   1.21   5.40   6.91    4.4%
D  agente + spec + verificacao, lote de 1     0.28   1.10   0.27   1.65   16.7%
E  D, mas a acao e irreversivel               0.28   1.10   2.70   4.08    6.8%
F  E + gate humano antes de agir              0.29   1.71   0.45   2.45   11.7%

gerar ficou 32x mais barato (A -> D); o total caiu 6.5x.
sem verificacao (B) o total e 1.7x o do humano digitando (A).

SENSIBILIDADE: o cenario D com g variando
  g =  8.00  ->  total = 10.21
  g =  2.00  ->  total =  3.58
  g =  0.50  ->  total =  1.93
  g =  0.10  ->  total =  1.49
  g =  0.01  ->  total =  1.39
  piso (g = 0) = 1.38: o que sobra e verificar e desfazer.
```

## Como ler

1. **A → D**: gerar caiu 32 vezes, o total caiu 6,5. A diferença é o que não ficou barato:
   verificar e desfazer.
2. **B**: o agente sem verificação, em lote grande, sai *mais caro* que o humano digitando. É
   o extremo "IA sem método" do capítulo, em número.
3. **C → D**: mesma verificação; o lote de 1 (e uma spec que baixa `p`) derruba o desfazer.
4. **E → F**: quando desfazer custa dez vezes mais (axioma A5), pagar mais verificação — um
   gate humano — compensa. O gate é função da irreversibilidade, não uniforme.
5. **Sensibilidade**: com `g` tendendo a zero, o total tende a um piso que só verificação e
   reversibilidade movem. A unidade de trabalho deixou de ser a mudança *escrita* e passou a
   ser a mudança *aceita*.

## Prove que a conferência acusa

Um check que nunca falhou não é check. Mude `"v": 1.0` do cenário D para `0.5` numa cópia de
`cenarios.json` e rode `python economia.py --cenarios <cópia> --conferir`: a saída diz
`DIVERGE` nas linhas 7, 11 e 15 a 20 (o cenário D é a base da sensibilidade) e o código de
saída é 1.
