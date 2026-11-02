# Exemplo do capítulo 4 — a spec como insumo

O que este exemplo prova, em sete passos: uma spec escrita em forma EARS (*Easy Approach to
Requirements Syntax*) é **verificável por máquina**; a mesma intenção escrita como prompt não
é; os testes leem os números **da spec**, de modo que, quando a spec muda primeiro, o código
fica vermelho em vez de ficar silenciosamente desatualizado; e a decisão de quanto processo
cada mudança merece sai de três fatores, não do tamanho do diff.

Requisito: Python 3.8+ (só biblioteca padrão) e bash. Nada pago, nada de rede.

## Como rodar

```bash
cd livro/04-a-spec-como-partitura/exemplo
bash rodar.sh                               # imprime a saída
bash rodar.sh | diff - saida-esperada.txt   # confere: nenhuma linha de diferença
```

No Windows, rode no Git Bash. O script procura `python3`, `python` e `py`, nessa ordem, e
usa o primeiro que for Python 3.8+ (no Git Bash o `python3` costuma ser um atalho que não
executa; o script detecta e passa adiante). Para forçar um interpretador: `PYTHON=... bash rodar.sh`.

## Os arquivos

| Arquivo | Papel |
|---|---|
| `spec.md` | a spec aprovada: três requisitos em EARS, fora de escopo, critérios como `comando` → esperado, clarify |
| `casos/spec-vaga.md` | a mesma intenção escrita como chega num prompt |
| `casos/spec-v2.md` | a spec depois de o comercial baixar o limite e pedir um requisito novo |
| `frete.py` | a implementação (o limite é uma constante — o código "a jusante") |
| `test_frete.py` | os testes; leem o limite da spec indicada em `SPEC` |
| `partitura.py` | `lint` (EARS × desejo), `rastreio` (requisito ↔ teste), `valor`, `raia` |
| `mudancas.json` | cinco mudanças para classificar por raia |
| `saida-esperada.txt` | a saída de `bash rodar.sh`, conferida em 02/11/2026 |
| `medir_maestro.py` | opcional: reproduz os números do capítulo num clone do Maestro |

## Saída esperada

Os passos 2, 5 e 6 saem com código 1 **de propósito**: são o vermelho que o capítulo descreve.

```text

== 1. a spec aprovada passa no lint (todo requisito é verificável)
lint spec.md
  ✓ FR1      EARS
  ✓ FR2      EARS
  ✓ FR3      EARS
  ✓ critério PAR
  ✓ critério PAR
✓ 5 item(ns), todos verificáveis.
(exit 0)

== 2. a mesma intenção escrita como prompt: três desejos e um requisito
lint casos/spec-vaga.md
  ✗ FR1      DESEJO  fora da forma EARS e sem comando que o prove
  ✓ FR2      EARS
  ✗ FR3      DESEJO  comportamento não observável ('rápid…')
  ✗ critério DESEJO  fora da forma EARS e sem comando que o prove
✗ 3 desejo(s): reescreva como QUANDO <condição>, O SISTEMA DEVE <comportamento observável>, ou como `comando` → esperado.
(exit 1)

== 3. cada requisito tem teste, e nenhum teste existe sem requisito
rastreio spec.md ↔ test_frete.py
  ✓ FR1 → test_fr1_*
  ✓ FR2 → test_fr2_*
  ✓ FR3 → test_fr3_*
✓ 3 requisito(s), cada um com teste; nenhum teste sem requisito.
(exit 0)

== 4. os testes leem o limite DA SPEC e passam
testes contra spec.md
  ok      test_fr1_frete_zero_a_partir_do_limite
  ok      test_fr2_tabela_abaixo_do_limite
  ok      test_fr3_subtotal_negativo_recusado
✓ 3 de 3 passaram.
(exit 0)

== 5. a spec muda primeiro (v2): o rastreio acusa o requisito novo sem teste
rastreio casos/spec-v2.md ↔ test_frete.py
  ✓ FR1 → test_fr1_*
  ✓ FR2 → test_fr2_*
  ✓ FR3 → test_fr3_*
  ✗ FR4 sem teste: requisito que ninguém prova
✗ 1 órfão(s) entre spec e teste.
(exit 1)

== 6. ... e os testes ficam vermelhos até o código seguir a spec
testes contra casos/spec-v2.md
  FALHOU  test_fr1_frete_zero_a_partir_do_limite: subtotal 150.00: esperado 0.00, obtido 25.00
  ok      test_fr2_tabela_abaixo_do_limite
  ok      test_fr3_subtotal_negativo_recusado
✗ 1 de 3 falharam: a spec andou e o código ficou para trás.
(exit 1)

== 7. quanto processo cada mudança merece (ambiguidade × raio × irreversibilidade)
raia mudancas.json
  leve   corrigir erro de digitação na mensagem do checkout
         amb=baixa · raio=baixo · irrev=baixa → o pull request é o artefato
  leve   bug: frete da região norte cobrado em dobro
         amb=baixa · raio=baixo · irrev=baixa → o pull request é o artefato; exige teste que reproduz o bug falhando antes
  plena  frete grátis acima de um valor (spec.md)
         amb=media · raio=baixo · irrev=baixa → na dúvida entre leve e plena, plena
  plena  trocar o formato da tabela de frete lida por três serviços
         amb=baixa · raio=alto · irrev=media → spec completa
  infra  mover a tabela de frete para outro banco (uma linha de configuração)
         amb=baixa · raio=baixo · irrev=alta → migracao nunca é leve: plena + reversibilidade
distribuição (visibilidade, nunca veredito): leve: 2 · plena: 2 · infra: 1
(exit 0)
```

## Para fechar o ciclo da v2 (exercício)

1. Escreva `test_fr4_regiao_desconhecida_recusada` em `test_frete.py`.
2. Mude `LIMITE_FRETE_GRATIS` para `150.00` e faça `frete()` levantar `ValueError` para
   região fora da tabela.
3. `python partitura.py rastreio casos/spec-v2.md test_frete.py` e
   `SPEC=casos/spec-v2.md python test_frete.py` devem sair 0. (Os passos 4 e 6 do
   `rodar.sh` mudam junto: a saída esperada é a da spec v1.)

## Os números do capítulo (opcional)

```bash
git clone https://github.com/GHDaru/maestro
python medir_maestro.py ./maestro 19823c2
```

Saída conferida em 02/11/2026:

```text
Maestro @ 19823c2
  pastas em specs/: 76 · com spec.md: 76
  spec.md com 'O SISTEMA DEVE': 48
  raias (total): plena: 54 · leve: 15 · infra: 5 · sem raia legível: 2
  raias, ciclos 001–033: plena: 20 · leve: 12
  raias, ciclos 034 em diante: plena: 33 · infra: 5 · leve: 3 · sem raia legível: 2
  pasta specs/040-*: não existe
Maestro @ 100a8af (véspera do ciclo 023)
  pastas em specs/: 21 · spec.md com 'O SISTEMA DEVE': 14 · raias: plena: 19 · leve: 2
```

`plena` soma as duas grafias do cabeçalho (`Raia: plena` e `Lane: full`). As duas specs
"sem raia legível" são `066-painel-de-regencia` (cabeçalho ainda com o marcador do template)
e `070-conferidor-ordem-veredito` (evidência importada de outro projeto, sem cabeçalho de
ciclo).

## O que o exemplo simplifica

- O `lint` reconhece a forma EARS e uma lista curta de palavras vagas; não entende
  português. Ele pega o desejo óbvio, não o sutil — um verificador de forma, não de mérito.
- A regra de raia trata irreversibilidade alta como infra mesmo fora de infraestrutura;
  no método, a raia infra é para infraestrutura, migração e implantação, e o bloco de
  reversibilidade é o que muda. A simplificação é do exemplo.
- Os testes leem um número da spec; não geram código a partir dela. O ponto não é gerar
  tudo automaticamente — é a spec estar **a montante**, de modo que mudá-la quebre algo.
