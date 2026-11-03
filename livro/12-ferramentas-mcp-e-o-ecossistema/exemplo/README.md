# Exemplo do capítulo 12 — sondar um servidor de ferramentas antes de ligá-lo ao agente

Um servidor do Model Context Protocol (MCP) mínimo, em duas versões com a **mesma interface**:
a ingênua (faz o que o pedido manda) e a guardada (cinco regras que vivem fora do modelo). Um
harness pequeno, `sondar.py`, sobe cada versão como subprocesso, conversa com ela em JSON-RPC
(*JSON Remote Procedure Call*) pela entrada padrão, como faz um cliente MCP de verdade, e
confere oito comportamentos.

| Arquivo | O que é |
|---|---|
| `servidor_mcp.py` | o servidor (stdio, JSON-RPC 2.0, só biblioteca padrão); `--ingenuo` liga a versão sem guardas |
| `politica.json` | a política `allow / deny / ask` por papel e por ferramenta; o que não está escrito é negado |
| `sessoes.json` | o registro de sessões: **hash** do token → endereço e papel; o token não fica no disco |
| `docs/` | três documentos: um normal, uma issue com injeção de instrução, uma ata longa |
| `segredo-de-demonstracao.txt` | um arquivo **fora** de `docs/` que nenhuma ferramenta deveria devolver (o conteúdo é fictício) |
| `sondar.py` | o harness: oito sondas contra cada versão |

As oito sondas, e o risco que cada uma mede:

| Sonda | Mede | Risco (OWASP Top 10 para aplicações com LLM, 2025) |
|---|---|---|
| S1 | o papel leitor não **vê** ferramenta de escrita | agência excessiva (LLM06): funcionalidade demais |
| S2 | o pedido legítimo continua funcionando | — (fixture legítima: guarda que recusa o certo é falso vermelho) |
| S3 | a ação irreversível com `ask` **não executa** sem humano | agência excessiva: autonomia demais |
| S4 | o papel leitor não escreve (`deny`) | agência excessiva: permissão demais |
| S5 | o argumento `autor` não vira identidade; quem assina é o token | falsificação de identidade pelo próprio modelo |
| S6 | o documento com injeção volta **cercado**, e a cerca falsa de dentro é neutralizada | injeção de prompt indireta (LLM01) |
| S7 | o resultado cabe no teto de bytes e **diz** que foi cortado | consumo sem limite (LLM10) e silêncio sobre o corte |
| S8 | a ferramenta não sai de `docs/` (`../segredo…`) | divulgação de informação sensível (LLM02) |

Os tokens (`tok-leitor-demo`, `tok-construtor-demo`) são de demonstração e vivem só em
`sondar.py`, que os passa ao servidor por **variável de ambiente** — fora do argv e fora do
texto que o modelo escreve, que é como um harness real deveria passar uma credencial.

## Como rodar

Requisito: Python 3.8 ou mais novo, sem dependência externa. No Git Bash do Windows, onde
`python3` pode ser um atalho vazio, use `python`.

```bash
cd livro/12-ferramentas-mcp-e-o-ecossistema/exemplo
python3 sondar.py                  # as duas versões
python3 sondar.py --so guardado    # só a guardada
```

## Saída esperada

`python3 sondar.py` — **sai com código 1**, e é esse o ponto: a versão ingênua passa só no
pedido legítimo.

```text
servidor ingenuo
  ✗ S1 o leitor não vê ferramenta de escrita no tools/list
  ✓ S2 pedido legítimo: o leitor lê o guia (fixture legítima)
  ✗ S3 apagar_registro (ask) não executa sem aprovação humana
  ✗ S4 o leitor não escreve status (deny)
  ✗ S5 o argumento 'autor' não vira identidade
  ✗ S6 a issue com injeção volta cercada, e a cerca falsa de dentro é neutralizada
  ✗ S7 o documento longo cabe no teto e diz que foi cortado
  ✗ S8 ler_doc não sai de docs/ (../segredo)
  1/8 sondas  →  EXPOSTO
servidor guardado
  ✓ S1 o leitor não vê ferramenta de escrita no tools/list
  ✓ S2 pedido legítimo: o leitor lê o guia (fixture legítima)
  ✓ S3 apagar_registro (ask) não executa sem aprovação humana
  ✓ S4 o leitor não escreve status (deny)
  ✓ S5 o argumento 'autor' não vira identidade
  ✓ S6 a issue com injeção volta cercada, e a cerca falsa de dentro é neutralizada
  ✓ S7 o documento longo cabe no teto e diz que foi cortado
  ✓ S8 ler_doc não sai de docs/ (../segredo)
  8/8 sondas  →  GUARDADO
```

`python3 sondar.py --so guardado` — **sai com código 0**, com o bloco `servidor guardado`
acima.

## Prove que a sonda acusa (mutação)

Uma sonda que você nunca viu reprovar não prova nada. Numa **cópia** desta pasta, troque em
`politica.json` a linha `"apagar_registro": "ask"` por `"apagar_registro": "allow"` e rode
`python3 sondar.py --so guardado`: a saída termina em `✗ S3 …` e `7/8 sondas  →  EXPOSTO`, com
código 1. Outras mutações para tentar: apagar a função `cercado()` da chamada em `ler_doc`
(S6 e S7 caem), ou trocar `os.path.realpath` por `os.path.normpath` e criar um link simbólico
dentro de `docs/` apontando para fora (S8 deveria cair com o link; o caminho `../` continua
barrado, e é exatamente essa a lição do ciclo 052 do Maestro).

## O que o exemplo **não** prova

A cerca não é uma sandbox: o texto dentro dela continua chegando ao modelo, e um modelo pode
obedecer a ele. O que impede o dano na sonda S3 é a política fora do modelo, não a cerca. E a
política deste exemplo vive no próprio servidor; num sistema real ela vive no harness ou num
serviço de autorização, para valer para **todos** os servidores ligados ao agente.
