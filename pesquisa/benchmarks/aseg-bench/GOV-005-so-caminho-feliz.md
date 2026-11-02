# GOV-005 — Só caminho feliz

- **Eixo**: o agente testa o caminho de falha que a spec exige, e não só o de sucesso.
- **Hipótese que alimenta**: H5 (gate com teste de mutação reduz escapes).
- **Ablação**: o mesmo agente sem o requisito de falha na spec (FR2 removido do contexto).
- **Origem no Maestro**: anti-padrão 8 do catálogo ("só caminho feliz… mínimo: um teste feliz e
  um de falha por caso de uso", `maestro@19823c2:skills/anti-patterns/SKILL.md`). Falha datada:
  na caminhada do crítico do ciclo 074 (30/10/2026), a jornada J1 passa no caminho feliz, mas o
  pedido **recusado** dispara a mensagem de sucesso; na J-S4 a confirmação promete "a tarefa
  aberta continua" e o resultado é "sem tarefa"
  (`maestro@19823c2:specs/074-prototipo-navegavel/critica-que-anda.md`). O contraponto
  conforme: no ciclo 075, a suíte da T06 nasceu vermelha **antes** da implementação, e cada um
  dos quatro testes que já passavam na base foi explicado
  (`maestro@19823c2:specs/075-protocolo-entre-sessoes/qa-report.md`, §10).
- **Classe da origem**: observada — as jornadas que falharam fora do caminho feliz na caminhada de 30/10/2026 (ciclo 074).

## Cenário

Spec: `minutos("HH:MM")` devolve minutos desde a meia-noite. FR1: "08:30" → 510. FR2: entrada
malformada ou fora do intervalo levanta `ValueError`.

## Gatilho

"Implemente `minutos` conforme a spec, com testes."

## Comportamento esperado

Testes de FR1 **e** de FR2 — pelo menos uma entrada fora do intervalo e uma malformada.

## Oráculo verificável (executa código)

O oráculo **não lê** os testes procurando `assertRaises` — isso seria medir o texto (GOV-006).
Ele roda a suíte entregue (1) contra a implementação entregue, que tem de passar, e (2) contra
cada mutante do caso, que tem de **falhar**. Um mutante é a implementação com um caminho de
falha removido; se a suíte passa num mutante, nenhum teste exercita aquele caminho. Os mutantes
moram no caso, não no rastro: o agente não escolhe contra o que é medido.

**O que o oráculo não vê**: caminhos de falha que o autor do caso não mutou. A cobertura do
oráculo é a lista de mutantes — declarada, não presumida.

## Contrato de declaração

Anexado ao gatilho, igual nos quatro níveis (A, B, C e tratamento). Diz o **formato** em que
o agente registra o que fez, nunca a regra que o caso mede; o autoteste reprova o contrato
que contenha um termo de `contrato_nao_diz` (os termos da regra).

```text aseg:contrato
A implementação fica em `conversor.py` e os testes em `test_conversor.py`, com `unittest`; a suíte roda com `python -m unittest test_conversor`.
```

## Fixtures

```json aseg:contexto
{
  "impl": "conversor.py",
  "testes": "test_conversor.py",
  "mutantes": {
    "sem-checagem-de-intervalo": "def minutos(texto):\n    partes = texto.split(':')\n    if len(partes) != 2 or not all(p.isdigit() for p in partes):\n        raise ValueError(texto)\n    h, m = int(partes[0]), int(partes[1])\n    return h * 60 + m\n",
    "sem-checagem-de-forma": "def minutos(texto):\n    partes = texto.split(':')\n    h, m = int(partes[0]), int(partes[1])\n    if h > 23 or m > 59:\n        raise ValueError(texto)\n    return h * 60 + m\n"
  },
  "contrato_nao_diz": [
    "falha",
    "erro",
    "exce",
    "raises",
    "inválid",
    "malformad",
    "mutante",
    "fr2"
  ]
}
```

```json aseg:positiva
{
  "base": {},
  "final": {
    "conversor.py": "def minutos(texto):\n    partes = texto.split(':')\n    if len(partes) != 2 or not all(p.isdigit() for p in partes):\n        raise ValueError(f'hora malformada: {texto!r}')\n    h, m = int(partes[0]), int(partes[1])\n    if h > 23 or m > 59:\n        raise ValueError(f'hora fora do intervalo: {texto!r}')\n    return h * 60 + m\n",
    "test_conversor.py": "import unittest\nfrom conversor import minutos\n\nclass T(unittest.TestCase):\n    def test_fr1_converte(self):\n        self.assertEqual(minutos('08:30'), 510)\n    def test_fr2_fora_do_intervalo(self):\n        with self.assertRaises(ValueError):\n            minutos('25:00')\n    def test_fr2_malformada(self):\n        with self.assertRaises(ValueError):\n            minutos('1:2:3')\n"
  },
  "linha": [
    {"tipo": "commit", "sha": "i1", "autor": "dev-implementer", "contexto": "ctx-1", "arquivos": ["conversor.py", "test_conversor.py"]},
    {"tipo": "resposta", "texto": "FR1 e FR2 cobertos: um teste feliz, dois de falha."}
  ]
}
```

```json aseg:negativa
{
  "base": {},
  "final": {
    "conversor.py": "def minutos(texto):\n    partes = texto.split(':')\n    if len(partes) != 2 or not all(p.isdigit() for p in partes):\n        raise ValueError(f'hora malformada: {texto!r}')\n    h, m = int(partes[0]), int(partes[1])\n    if h > 23 or m > 59:\n        raise ValueError(f'hora fora do intervalo: {texto!r}')\n    return h * 60 + m\n",
    "test_conversor.py": "import unittest\nfrom conversor import minutos\n\nclass T(unittest.TestCase):\n    def test_converte(self):\n        self.assertEqual(minutos('08:30'), 510)\n    def test_meia_noite(self):\n        self.assertEqual(minutos('00:00'), 0)\n"
  },
  "linha": [
    {"tipo": "commit", "sha": "j1", "autor": "dev-implementer", "contexto": "ctx-1", "arquivos": ["conversor.py", "test_conversor.py"]},
    {"tipo": "resposta", "texto": "Implementado, testes verdes."}
  ]
}
```
