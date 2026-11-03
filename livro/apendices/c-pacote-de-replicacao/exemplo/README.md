# Exemplo do apêndice C — o roteiro de reprodução num script só

O apêndice diz que todo número do livro aponta para o comando que o refaz, e que uma execução
só entra numa análise se congelar o próprio ambiente. Este script faz as duas conferências sem
perguntar nada ao autor:

- `--conferir` roda a evidência de quatro claims (CLAIM-00-008, CLAIM-93-007, CLAIM-93-013,
  CLAIM-93-014) e confere os ids de claim do apêndice nos dois sentidos;
- `--validar-run` diz se um `run.json` traz os campos do ambiente congelado do protocolo 0.1
  (`pesquisa/protocolo.md`, §3) e recalcula o Secure Hash Algorithm de 256 bits (SHA-256) do
  `prompt.txt` da pasta.

## Requisitos

- Python 3.8+ e Git no `PATH`. Nada pago, nada de rede.
- Para a parte do Maestro, um clone: `git clone https://github.com/GHDaru/maestro.git`. Sem
  `--maestro`, essas conferências saem como `PULA`.

## Arquivos

```text
exemplo/
├── conferir_pacote.py      o script (só lê: git cat-file, git show, git tag)
├── run-modelo/             o molde para o seu time: run.json no schema 1 + prompt.txt
│   ├── run.json            hashes reais do prompt, da ficha, do runner e do avaliador de GOV-004
│   └── prompt.txt          cópia do prompt da primeira execução do ASEG-Bench
└── run-como-veio/
    └── run.json            cópia byte a byte do veredito.json dessa execução, como o runner gravou
```

No `run-modelo/run.json`, `livro.commit` é o *commit* do livro em que os arquivos de origem dos
*hashes* estão versionados; `sistema` é a máquina do autor; `metricas`, `inicio` e `fim` estão
vazios porque a ficha é preenchida **antes** de rodar. Troque tudo pelos valores do seu cenário.

## Como rodar

Da pasta `exemplo/` (no Windows, `python`; em Linux/macOS, `python3`):

```bash
python conferir_pacote.py --conferir --maestro /caminho/do/clone/maestro
python conferir_pacote.py --validar-run run-modelo
python conferir_pacote.py --validar-run run-como-veio
```

Saída do processo: `--conferir` sai com 0 quando nenhuma linha é `FALHA`; `--validar-run` sai
com 0 quando o *run* entra na análise (com ou sem marca) e 1 quando não entra.

## Saída esperada (conferida em 03/11/2026)

No clone do autor, que tem o *commit* `19823c2`:

```text
OK    19823c2 existe no clone                      obtido: commit   esperado: commit
OK    CLAIM-00-008 princípios (### I.–VIII.)       obtido: 8   esperado: 8
OK    CLAIM-93-013 versões do CHANGELOG            obtido: Unreleased,0.3.0,0.2.0,0.1.0   esperado: Unreleased,0.3.0,0.2.0,0.1.0
OK    CLAIM-93-013 tags v* no clone                obtido: 0   esperado: 0
OK    CLAIM-93-007 campos do veredito.json         obtido: 8   esperado: 8
OK    ids do apêndice no formato CLAIM-NN-NNN      obtido: todos   esperado: todos
OK    ids citados = ids registrados                obtido: 15 citados, 15 registrados   esperado: iguais

7 conferências, 0 falha(s), 0 pulada(s)
```

Num clone que **não** tem o `19823c2` — o caso de qualquer clone do repositório público até
03/11/2026, quando o *commit* estava só numa *branch* local do autor (CLAIM-93-014); desde então ele está em `livro-ref-19823c2` (CLAIM-93-016). Saída 1:

```text
FALHA 19823c2 existe no clone                      obtido: ausente   esperado: commit
      o clone não tem o commit de referência; veja o README (clone sem 19823c2)
OK    CLAIM-93-013 tags v* no clone                obtido: 0   esperado: 0
OK    CLAIM-93-007 campos do veredito.json         obtido: 8   esperado: 8
OK    ids do apêndice no formato CLAIM-NN-NNN      obtido: todos   esperado: todos
OK    ids citados = ids registrados                obtido: 15 citados, 15 registrados   esperado: iguais

5 conferências, 1 falha(s), 0 pulada(s)
```

Essa falha é o achado, não um defeito do script: enquanto o *commit* de referência não for
publicado, os claims ancorados em `git show 19823c2:…` só se conferem na máquina do autor.

Validar o molde (saída 0):

```text
run: run-modelo/run.json
  MARCA  modelo_nao_verificado (o harness não relatou o modelo resolvido)
ENTRA na análise (com marca)
```

Validar o registro da primeira execução real, tal como foi gravado (saída 1):

```text
run: run-como-veio/run.json
  FALTA  metodo.commit: ausente
  FALTA  livro.commit: ausente
  FALTA  modelo.pedido: ausente
  FALTA  modelo.resolvido: ausente
  FALTA  harness.nome: ausente
  FALTA  harness.versao: ausente
  FALTA  cenario.base: ausente
  FALTA  sistema.os: ausente
  FALTA  sistema.python: ausente
  FALTA  semente: ausente
  FALTA  hashes: ausente
NÃO ENTRA na análise: 11 campo(s) do ambiente congelado
```

(No Windows o caminho sai com `\`.) O `veredito.json` tem o modelo e o *commit*-base, mas com
outros nomes (`modelo`, `base`) e fora do *schema* do protocolo; o validador não adivinha
nomes, e é isso que o apêndice quer dizer com "serve para depurar o *runner*, não para afirmar
nada sobre um braço".

## O que o script não faz

Não roda a coluna de evidência de todos os claims do livro: confere quatro, como amostra, e a
forma dos ids deste apêndice. A forma do livro inteiro é com `scripts/check-claims.sh`, na raiz
do repositório do livro. Também não prova que um *run* válido mediu a coisa certa: prova só que
ele registrou o bastante para ser refeito.
