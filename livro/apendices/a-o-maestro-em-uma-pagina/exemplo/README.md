# Exemplo do apêndice A — conferir o retrato contra o disco

O apêndice diz que todo resumo do método é um **retrato** com data, e que o retrato envelhece
mais devagar do que o repositório. Este script mede isso: conta, em duas versões do Maestro,
os números que as peças de apresentação afirmam (agentes, comandos, skills, templates,
portões, raias do BPMN) e mostra onde o desenho parou e o disco andou.

## Requisitos

- Python 3.8+ e Git no `PATH`. Nada pago, nada de rede.
- Um clone do Maestro: `git clone https://github.com/GHDaru/maestro.git`

## Como rodar

```bash
python conferir_retrato.py /caminho/do/clone/maestro            # 9be9c3f e 19823c2
python conferir_retrato.py /caminho/do/clone/maestro 0fe0e7e 19823c2   # outras versões
```

O script só lê (`git ls-tree`, `git show`); não muda o clone.

**Tempo.** O script faz poucas chamadas ao Git por versão, e o tempo é quase todo do Git.
Em 02/11/2026, num Windows com Git Bash, levou 11 s; numa execução da revisão crítica do
apêndice, também no Windows, cerca de 78 s. Se demorar, não está travado.

**Acentos no console do Windows.** Se a última linha sair com `pe�a n�o existe`, é o console
em página de código antiga; rode com `PYTHONIOENCODING=utf-8` ou ignore: os números não mudam.

**O que o script reproduz.** O CLAIM-91-018 inteiro e, de passagem, as sete raias do
CLAIM-91-004. Os outros claims `medido` do apêndice se conferem um a um pelo comando de
[claims.md](../claims.md).

## Saída esperada (conferida em 02/11/2026)

```text
medida                            9be9c3f    19823c2
agentes (.claude/agents/*.md)          13         13
comandos (.claude/commands)            12         12
skills (pastas em skills/)              6          6
templates (.specify/templates)         12         12
portoes (scripts/check-*.sh)           16         19
raias no BPMN (bpmn-raia)               7          7
portoes que o BPMN anuncia              8          8
archify: retrato tirado em     (peça não existe)    39a86ba
```

## Como ler

- `9be9c3f` é o commit do ciclo 053 (14/08/2026), o que escreveu o caderno de
  desenvolvimento dizendo "16 portões". O disco tinha 16.
- `19823c2` é a versão que o livro cita (01/11/2026). O disco tem 19 scripts de portão; o
  BPMN continua anunciando 8 nas duas versões. A peça 07 (Archify) existe só na segunda, e
  declara ter sido tirada em `39a86ba`, de 22/10.
- O exercício: escolha um número de um slide do seu próprio time e escreva o comando que o
  confere. Se não houver comando, o número é opinião com data.
