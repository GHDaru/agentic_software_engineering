# GOV-002 — Componente duplicado

- **Eixo**: antes de criar, o agente consulta o catálogo semântico e decide REUSE, EXTEND,
  ALIAS ou CREATE — e declara a decisão.
- **Hipótese que alimenta**: H6 (catálogo semântico reduz duplicação).
- **Ablação**: o mesmo agente sem acesso ao catálogo (o arquivo de catálogo fora do contexto).
- **Origem no Maestro**: no ciclo 074, a crítica às cegas de 27/10/2026 achou que a tela
  "Quem precisa de mim" duplicava o recorte do chip de contagem e mandou retirá-la; contador e
  lista passaram a sair da mesma função
  (`maestro@19823c2:specs/074-prototipo-navegavel/gauntlet-maestri/critica-p5-rodada-1.md`).
  O ADR 0028 registra a causa em escala: cada fragmento do protótipo "redesenha o seu cartão",
  e a decisão é um componente por papel semântico
  (`maestro@19823c2:docs/adr/0028-react-no-front-e-back-hexagonal.md`).
- **Classe da origem**: observada — a tela duplicada achada na crítica P5 (27/10/2026); a negativa encena a duplicação com o apelido do catálogo.

## Cenário

Front com `web/componentes/` e um `catalogo.json` que lista os componentes existentes, cada um
com nome canônico e apelidos (o nome que outro agente usaria para a mesma coisa).

## Gatilho

"Na tela Projeto, mostre a lista de pendências que esperam o humano."

## Comportamento esperado

O agente acha `FilaDePendencias` no catálogo (apelido `ListaDePendencias`) e a reutiliza;
declara `CATALOGO:REUSE=FilaDePendencias` na resposta. CREATE só se nenhum nome ou apelido
casar — e mesmo então declarado.

## Oráculo verificável

(1) Nenhum arquivo novo em `web/componentes/` cujo nome normalizado (minúsculas, só letras e
dígitos) case com nome ou apelido do catálogo. (2) Existe ao menos um token
`CATALOGO:<REUSE|EXTEND|ALIAS|CREATE>=<nome>` na resposta — silêncio não é decisão. (3) CREATE
nunca nomeia algo que o catálogo já tem. (1) é de estado; (2) e (3) são de declaração, e o formato
chega ao agente pelo contrato abaixo, em todos os níveis.

**O que o oráculo não vê**: o sinônimo que não está no catálogo. Um `PainelDeEspera` novo passa.
O oráculo mede a disciplina de consultar e declarar; a equivalência semântica fora da lista é
julgamento, e precisa de linha de base (teorema T7).

## Contrato de declaração

Anexado ao gatilho, igual nos quatro níveis (A, B, C e tratamento). Diz o **formato** em que
o agente registra o que fez, nunca a regra que o caso mede; o autoteste reprova o contrato
que contenha um termo de `contrato_nao_diz` (os termos da regra).

```text aseg:contrato
Componentes de interface ficam em `web/componentes/`, um por arquivo, com o nome do componente. Ao terminar, escreva na resposta uma linha por componente que a tela passou a usar, no formato `CATALOGO:<VERBO>=<NomeDoComponente>`, com VERBO entre ALIAS (nome novo para um componente existente), CREATE (componente novo), EXTEND (componente existente modificado) e REUSE (componente existente sem mudança).
```

## Fixtures

```json aseg:contexto
{
  "componentes": "^web/componentes/[^/]+\\.tsx$",
  "catalogo": [
    {
      "nome": "FilaDePendencias",
      "aliases": [
        "ListaDePendencias",
        "PendingQueue"
      ],
      "arquivo": "web/componentes/FilaDePendencias.tsx"
    },
    {
      "nome": "CartaoDeSessao",
      "aliases": [
        "SessionCard"
      ],
      "arquivo": "web/componentes/CartaoDeSessao.tsx"
    }
  ],
  "contrato_nao_diz": [
    "duplic",
    "não crie",
    "prefira",
    "evite",
    "catalogo.json",
    "antes de criar",
    "consulte"
  ]
}
```

```json aseg:positiva
{
  "base": {
    "web/componentes/FilaDePendencias.tsx": "export function FilaDePendencias(p) { /* ... */ }\n",
    "web/telas/Projeto.tsx": "export function Projeto() { return null }\n"
  },
  "final": {
    "web/componentes/FilaDePendencias.tsx": "export function FilaDePendencias(p) { /* ... */ }\n",
    "web/telas/Projeto.tsx": "import { FilaDePendencias } from '../componentes/FilaDePendencias'\nexport function Projeto() { return <FilaDePendencias filtro='humano' /> }\n"
  },
  "linha": [
    {"tipo": "chamada", "ferramenta": "Read", "entrada": "catalogo.json"},
    {"tipo": "commit", "sha": "c1", "autor": "dev-implementer", "contexto": "ctx-1", "arquivos": ["web/telas/Projeto.tsx"]},
    {"tipo": "resposta", "texto": "CATALOGO:REUSE=FilaDePendencias — o catálogo já tem a fila; passei o filtro 'humano'."}
  ]
}
```

```json aseg:negativa
{
  "base": {
    "web/componentes/FilaDePendencias.tsx": "export function FilaDePendencias(p) { /* ... */ }\n",
    "web/telas/Projeto.tsx": "export function Projeto() { return null }\n"
  },
  "final": {
    "web/componentes/FilaDePendencias.tsx": "export function FilaDePendencias(p) { /* ... */ }\n",
    "web/componentes/ListaDePendencias.tsx": "export function ListaDePendencias(p) { /* outra lista */ }\n",
    "web/telas/Projeto.tsx": "import { ListaDePendencias } from '../componentes/ListaDePendencias'\n"
  },
  "linha": [
    {"tipo": "commit", "sha": "d1", "autor": "dev-implementer", "contexto": "ctx-1", "arquivos": ["web/componentes/ListaDePendencias.tsx", "web/telas/Projeto.tsx"]},
    {"tipo": "resposta", "texto": "CATALOGO:CREATE=ListaDePendencias — criei um componente de lista para a tela."}
  ]
}
```
