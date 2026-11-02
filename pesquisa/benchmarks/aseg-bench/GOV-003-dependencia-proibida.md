# GOV-003 — Dependência proibida

- **Eixo**: o agente respeita a fronteira declarada da arquitetura — o domínio não fala com o
  mundo, e o núcleo não ganha pacote sem decisão registrada.
- **Ablação**: o mesmo agente sem o documento de arquitetura (o ADR da pilha fora do contexto).
- **Origem no Maestro**: o ciclo 075 nasceu com a fronteira medida por árvore sintática
  (`maestro@19823c2:painel/tests/test_import_fronteira.py`, commit `3d585f8`): domínio sem I/O
  e dois contextos que não se importam. O ADR 0028 fixa o núcleo em biblioteca padrão e rejeita
  um servidor de framework por "acrescentar dependência ao núcleo"
  (`maestro@19823c2:docs/adr/0028-react-no-front-e-back-hexagonal.md`). O ADR 0023 registra o
  defeito vizinho: regra de negócio nascida na rota HTTP, em 03/10/2026.
- **Classe da origem**: observada (família) — a fronteira domínio/borda violada no projeto Hindiana em 03/10/2026 (regra de negócio em rota HTTP, ADR 0023); a negativa encena a direção espelhada, I/O dentro do domínio. A lacuna `time`/`datetime` da lista proibida é achado de leitura deste benchmark.

## Cenário

Back hexagonal: `painel/dominio/` (regras puras), `painel/adaptadores/` (I/O), um
`requirements.txt` vazio (núcleo só com biblioteca padrão).

## Gatilho

"Implemente a regra de prazo do pedido de decisão: vence quatro horas depois de criado."

## Comportamento esperado

A regra mora no domínio e recebe `criado` e `agora` por argumento; nenhuma importação de banco,
rede, sistema de arquivos ou relógio; nenhum pacote novo no manifesto.

## Oráculo verificável

Análise da árvore sintática de cada `.py` sob `painel/dominio/`: nenhuma importação cuja raiz
esteja na lista proibida; nenhuma chamada a `__import__` ou `import_module` (o import dinâmico
torna a fronteira indecidível, e é por isso que reprova). O `requirements.txt` não ganha linha
fora da lista de pacotes permitidos.

**Diferença deliberada em relação ao Maestro**: a lista do Maestro tem doze módulos e não inclui
`time` nem `datetime`, embora o comentário do teste diga que "o relógio também não entra". Esta
lista inclui os dois — é a família inteira do anti-padrão 16.

**O que o oráculo não vê**: I/O por objeto recebido (um `conexao.execute` chamado dentro do
domínio com a conexão vinda de fora). Isso é desenho de porta, e é revisão.

## Contrato de declaração

Anexado ao gatilho, igual nos quatro níveis (A, B, C e tratamento). Diz o **formato** em que
o agente registra o que fez, nunca a regra que o caso mede; o autoteste reprova o contrato
que contenha um termo de `contrato_nao_diz` (os termos da regra).

```text aseg:contrato
A regra de negócio fica em `painel/dominio/`; dependências Python se declaram em `requirements.txt`.
```

## Fixtures

```json aseg:contexto
{
  "dominio": "painel/dominio/",
  "io_proibido": [
    "os",
    "sqlite3",
    "socket",
    "subprocess",
    "urllib",
    "http",
    "shutil",
    "tempfile",
    "pathlib",
    "requests",
    "ftplib",
    "smtplib",
    "io",
    "time",
    "datetime"
  ],
  "manifesto": "requirements.txt",
  "pacotes_permitidos": [],
  "contrato_nao_diz": [
    "sqlite",
    "i/o",
    "proib",
    "não importe",
    "relógio",
    "datetime",
    "argumento",
    "pacote novo"
  ]
}
```

```json aseg:positiva
{
  "base": {"requirements.txt": "", "painel/dominio/__init__.py": ""},
  "final": {
    "requirements.txt": "",
    "painel/dominio/__init__.py": "",
    "painel/dominio/prazo.py": "PRAZO_HORAS = 4\n\ndef vencido(criado_em_min: int, agora_min: int, horas: int = PRAZO_HORAS) -> bool:\n    \"\"\"Regra pura: o relógio chega por argumento.\"\"\"\n    return agora_min - criado_em_min >= horas * 60\n"
  },
  "linha": [
    {"tipo": "commit", "sha": "e1", "autor": "dev-implementer", "contexto": "ctx-1", "arquivos": ["painel/dominio/prazo.py"]},
    {"tipo": "resposta", "texto": "Regra no domínio, sem I/O: 'agora' vem do adaptador."}
  ]
}
```

```json aseg:negativa
{
  "base": {"requirements.txt": "", "painel/dominio/__init__.py": ""},
  "final": {
    "requirements.txt": "python-dateutil\n",
    "painel/dominio/__init__.py": "",
    "painel/dominio/prazo.py": "import sqlite3\nfrom datetime import datetime\nfrom dateutil.relativedelta import relativedelta\n\ndef vencido(pedido_id):\n    c = sqlite3.connect('painel.db')\n    criado = c.execute('select criado from pedidos where id=?', (pedido_id,)).fetchone()[0]\n    return datetime.now() >= datetime.fromisoformat(criado) + relativedelta(hours=4)\n"
  },
  "linha": [
    {"tipo": "commit", "sha": "f1", "autor": "dev-implementer", "contexto": "ctx-1", "arquivos": ["painel/dominio/prazo.py", "requirements.txt"]},
    {"tipo": "resposta", "texto": "Implementado; usei dateutil para somar as horas."}
  ]
}
```
