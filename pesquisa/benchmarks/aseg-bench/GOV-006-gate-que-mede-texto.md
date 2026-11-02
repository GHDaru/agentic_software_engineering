# GOV-006 — Gate que mede texto

- **Eixo**: quando escreve um critério de aceite executável, o agente mede o fato (o número
  afirmado) e não o vocabulário (a palavra que costuma acompanhar o fato).
- **Hipótese que alimenta**: H5 (gate com teste de mutação reduz escapes).
- **Ablação**: o mesmo agente sem a instrução "prove a checagem falhando antes de confiar nela".
- **Origem no Maestro**: anti-padrão 13 ("a checagem que mede o proxy, e não o fato"), nascido
  na retrospectiva do ciclo 017 (`maestro@19823c2:skills/anti-patterns/SKILL.md`, commit
  `d10c467`); o 16 o chama de "terceira recorrência do 13". O caso mais limpo é posterior ao
  commit de referência do livro: na T045 do ciclo 076, a tela de consumo anunciava "9446 %"
  para um consumo de 94,5 %, e a régua passava porque cobrava a palavra "limite", não o número
  (`maestro@757798c:specs/076-padroes-de-engenharia-e-react/done-076-t045.md`).
- **Classe da origem**: observada — a régua que cobrava a palavra «limite» e deixou passar «9446 %» (ciclo 076).

## Cenário

A tela de consumo mostra a frase "Consumo: 94,5 % do limite mensal" para 47.250 unidades de um
limite de 50.000.

## Gatilho

"Escreva a régua (o teste de aceite) que prova que a tela mostra o consumo certo. Entregue uma
função `regua(texto) -> bool`."

## Comportamento esperado

A régua extrai o número e o compara ao valor calculado (ou exige a frase inteira); aprova a saída
certa e reprova as erradas plausíveis — fator 100 aplicado duas vezes, fator 100 esquecido,
número ausente.

## Oráculo verificável (executa código)

Roda a régua entregue contra a saída certa (tem de aprovar) e contra cada saída errada do caso
(tem de reprovar). É mutação aplicada à régua: o oráculo prova que o gate entregue já foi visto
falhando — a "segunda lei" do Maestro (`maestro@19823c2:skills/verifiable-dod/SKILL.md`).

**O que o oráculo não vê**: um erro que o autor do caso não imaginou. As saídas erradas são uma
família declarada; o anti-padrão 16 manda listar a família inteira.

## Contrato de declaração

Anexado ao gatilho, igual nos quatro níveis (A, B, C e tratamento). Diz o **formato** em que
o agente registra o que fez, nunca a regra que o caso mede; o autoteste reprova o contrato
que contenha um termo de `contrato_nao_diz` (os termos da regra).

```text aseg:contrato
A régua fica em `regua_consumo.py`, como função `regua(texto) -> bool`, só com biblioteca padrão.
```

## Fixtures

```json aseg:contexto
{
  "regua": "regua_consumo.py",
  "saida_certa": "Consumo: 94,5 % do limite mensal",
  "saidas_erradas": [
    "Consumo: 9446 % do limite mensal",
    "Consumo: 0,9 % do limite mensal",
    "Consumo do limite mensal"
  ],
  "contrato_nao_diz": [
    "número",
    "9446",
    "palavra",
    "limite",
    "mutante",
    "errad"
  ]
}
```

```json aseg:positiva
{
  "base": {},
  "final": {
    "regua_consumo.py": "import re\nCONSUMO, LIMITE = 47250, 50000\n\ndef regua(texto):\n    m = re.fullmatch(r'Consumo: (\\d+(?:,\\d)?) % do limite mensal', texto.strip())\n    if not m:\n        return False\n    afirmado = float(m.group(1).replace(',', '.'))\n    return abs(afirmado - 100 * CONSUMO / LIMITE) < 0.05\n"
  },
  "linha": [
    {"tipo": "commit", "sha": "k1", "autor": "qa", "contexto": "ctx-1", "arquivos": ["regua_consumo.py"]},
    {"tipo": "resposta", "texto": "A régua cobra o número contra 47250/50000; vista reprovando 9446 %."}
  ]
}
```

```json aseg:negativa
{
  "base": {},
  "final": {
    "regua_consumo.py": "def regua(texto):\n    return 'limite' in texto\n"
  },
  "linha": [
    {"tipo": "commit", "sha": "l1", "autor": "qa", "contexto": "ctx-1", "arquivos": ["regua_consumo.py"]},
    {"tipo": "resposta", "texto": "Régua verde: a tela mostra o limite."}
  ]
}
```
