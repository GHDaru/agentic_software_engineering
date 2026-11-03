# Exemplo do capítulo 8 — a linguagem ubíqua que a máquina lê

O que este exemplo prova, em nove passos, sobre um domínio pequeno (uma central de atendimento
com três contextos: atendimento, mensageria, faturamento):

- três sessões de agente que nomeiam a mesma tarefa produzem quatro nomes para o mesmo conceito,
  e um catálogo com quatro decisões (REUSE, ALIAS, EXTEND, CREATE) os reduz a um identificador;
- um *lint* lido do mesmo modelo acusa sigla nua, palavra de família escrita nua ("fila",
  "prazo") e apelido no lugar do termo do modelo;
- o plano que não declara o domínio, ou que põe uma regra na borda sem motivo, reprova;
- endereço ambíguo ou morto é recusado, nunca adivinhado;
- o glossário é gerado do modelo, e qualquer divergência (edição à mão, modelo mudado sem
  regerar) é apontada pela linha;
- cada régua tem fixture boa e ruim, e discrimina.

Requisito: Python 3.8+ (só biblioteca padrão) e bash. Nada pago, nada de rede.

## Como rodar

```bash
cd livro/08-ddd-para-agentes/exemplo
bash rodar.sh                               # imprime a saída
bash rodar.sh | diff - saida-esperada.txt   # confere: nenhuma linha de diferença
```

No Windows, rode no Git Bash. O script procura `python3`, `python` e `py`, nessa ordem, e usa o
primeiro que for Python 3.8+ de verdade. Para forçar: `PYTHON=... bash rodar.sh`.

Opcional: `bash medir_maestro.sh /caminho/do/clone/maestro` reproduz os números do Maestro citados
no capítulo (só lê o clone, com `git show`; em Git Bash no Windows pode levar alguns minutos).

## Os arquivos

| Arquivo | Papel |
|---|---|
| `modelo.json` | o modelo único: contextos, termos (tela → identificador, contexto, definição, apelidos), famílias que nunca se escrevem nuas, siglas |
| `propostas.json` | dez nomes propostos por três sessões para a mesma tarefa |
| `catalogo.py` | `decidir`, `lint`, `plano`, `endereco`, `glossario gerar/conferir`, `mutacao` |
| `glossario-gerado.md` | o glossário gerado do modelo (`python catalogo.py glossario gerar modelo.json`) |
| `sessoes.json` | sessões vivas e mortas, para o passo de endereço |
| `casos/tela-ruim.md`, `casos/tela-boa.md` | o mesmo texto de tela antes e depois do catálogo |
| `casos/plan-*.md` | planos sem declaração, com borda sem motivo, correto e com três defeitos |
| `rodar.sh` | os nove passos |
| `saida-esperada.txt` | a saída de `bash rodar.sh`, conferida em 02/11/2026 |
| `medir_maestro.sh` | opcional: os números do Maestro (`19823c2`) |

## Saída esperada

Os passos 1, 2, 4, 5, 7, 8b e 8c saem com código 1 **de propósito**: é o vermelho que o capítulo
descreve. O carimbo `sha256` é calculado sobre o modelo em forma canônica (chaves ordenadas), então
não muda com a quebra de linha do sistema operacional.

```text

== 1. três sessões nomeiam a mesma tarefa: cada nome recebe REUSE, ALIAS, EXTEND ou CREATE
tarefa: avisar o atendente quando um chamado estoura o prazo de resposta
  ✓ sessão A  Ticket                 REUSE     já existe: Chamado (Ticket, atendimento)
  ✓ sessão A  Request                ALIAS     apelido de Chamado (Ticket): use o termo do modelo
  ✗ sessão A  Fila                   RECUSADO  termo nu — sempre qualificada: fila de atendimento ou fila de saída
  ✓ sessão B  Chamado                REUSE     já existe: Chamado (Ticket, atendimento)
  ✓ sessão B  Ocorrência             ALIAS     apelido de Chamado (Ticket): use o termo do modelo
  ✓ sessão B  Prazo de resposta      REUSE     já existe: Prazo de resposta (responseDueAt, atendimento)
  ✓ sessão B  Prazo de reabertura    EXTEND    nova forma qualificada da família 'prazo' em atendimento: entra no modelo antes do código
  ✓ sessão C  Client                 ALIAS     apelido de Cliente (Customer): use o termo do modelo
  ✓ sessão C  Alerta de estouro      CREATE    termo novo em atendimento, com definição: entra no modelo antes do código
  ✗ sessão C  Status                 RECUSADO  termo novo sem definição nem contexto — nome que ninguém definiu é o sinônimo de amanhã
resumo: REUSE 3 · ALIAS 3 · EXTEND 1 · CREATE 1 · RECUSADO 2
  10 nomes propostos por 3 sessões → 5 identificadores (2 novos, com definição)
  4 nomes para Ticket: Chamado, Ocorrência, Request, Ticket
(exit 1)
```

A saída completa dos nove passos está em [`saida-esperada.txt`](saida-esperada.txt). Os trechos
mais importantes dos demais passos:

```text
== 2. o texto de tela que a sessão A escreveu sem o catálogo
lint tela-ruim.md
  ✗ linha 3: sigla nua na 1ª ocorrência: SLA — escreva 'Service Level Agreement (SLA)'
  ✗ linha 3: apelido 'Request' — o termo do modelo é 'Chamado' (Ticket)
  ✗ linha 4: termo nu: 'fila' — sempre qualificada: fila de atendimento ou fila de saída
  ✗ linha 4: termo nu: 'prazo' — sempre qualificado: prazo de resposta ou prazo de pagamento
  ✗ linha 5: sigla nua na 1ª ocorrência: API — escreva 'Application Programming Interface (API)'
  ✗ linha 5: apelido 'Client' — o termo do modelo é 'Cliente' (Customer)
✗ 6 achado(s).

== 5. o plano que pôs uma regra na borda sem dizer por quê
plano plan-edge-sem-motivo.md
  ✗ invariants: 'alerta_sai_uma_vez=edge' é borda sem motivo — escreva alerta_sai_uma_vez=edge(por que não pode ser domínio)

== 7. endereço: ambíguo ou morto é recusado, nunca adivinhado
  ✗ 'Gerente' → RECUSADO: ambíguo (2 sessões vivas: [a1b2c3] · loja, [d4e5f6] · site); diga nome [ref] · projeto
  ✓ 'Gerente · loja' → entrega a Gerente [a1b2c3] · loja
  ✓ 'Revisor · loja' → entrega a Revisor [7f7f7f] · loja
  ✗ 'Revisor [0a0a0a] · loja' → RECUSADO: ref morto ou inexistente; não cai para o nome

== 8b. alguém 'corrige' o glossário à mão
  ✗ linha 7 difere do que o modelo gera:
      no arquivo: | Cliente | `Customer` | atendimento | Quem paga o contrato. |
      do modelo : | Cliente | `Customer` | atendimento | Quem abre o chamado e recebe a resposta. |

== 9. as réguas discriminam? (fixture boa limpa, fixture ruim pega)
  lint   boa 0 achado(s) · ruim 6 achado(s) · discrimina: sim
  plano  boa 0 achado(s) · ruim 3 achado(s) · discrimina: sim
✓ as duas réguas discriminam.
```

## O que o exemplo não faz

Não decide se um termo novo deveria mesmo ser novo, nem se o motivo de uma borda é bom: garante
que a pergunta foi feita e que a resposta ficou escrita. A qualidade da resposta é do revisor. As
heurísticas do classificador (casamento exato, apelido conhecido, primeira palavra de família) são
deliberadamente simples; um catálogo real precisa de revisão humana para os casos de fronteira,
como um apelido que, com o tempo, virou um conceito distinto.
