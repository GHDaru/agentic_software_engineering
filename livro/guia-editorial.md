# Guia editorial do livro

> Contrato de escrita de todo capítulo. Os portões em `scripts/` conferem o que está aqui.
> Herdeiro do guia editorial do Maestro (`maestro@19823c2:docs/livro/guia-editorial.md`),
> adaptado para um livro independente de ferramenta.

## Leitor

**Tech lead** — engenheiro sênior que responde por um time e agora rege agentes de IA. Sabe
programar, conhece Git, CI, revisão de código e Scrum/Kanban; não precisa saber o que é o
Maestro. Quer decidir o que adotar segunda-feira, com argumento e evidência.

## Anatomia de capítulo (11 seções, nesta ordem, com estes títulos de nível 2)

1. `## Pergunta central` — uma pergunta, em uma frase, que o capítulo responde.
2. `## Resultado de aprendizagem` — 3 a 5 itens "ao final, você consegue…" (verbos observáveis).
3. `## A falha real` — uma falha **datada e verificável** antes da regra: ciclo, commit, achado
   ou retrospectiva do Maestro (ou caso público citado). Narrada como história curta.
4. `## Teoria` — o conceito, sua origem e por que vale; o axioma/teorema de que deriva.
5. `## Alternativas` — o que mais existe (frameworks, práticas), comparado com veredito.
6. `## O padrão Maestro` — como o Maestro resolve, **citado por versão** (`maestro@19823c2:caminho`),
   não copiado. Diga o que é regra, o que é script e o que é hook.
7. `## Exemplo executável` — aponta para `exemplo/` do capítulo: algo que o leitor **roda** e cuja
   saída esperada está escrita. Sem dependência paga; bash, Python 3 ou Node.
8. `## Contraexemplo` — quando a regra **não** se aplica ou atrapalha; o custo dela.
9. `## Evidência` — o que sustenta o capítulo, com `[CLAIM-NN-NNN]`; hipótese marcada como
   hipótese (H1–H10 da `pesquisa/base-de-pesquisa.md`).
10. `## Checklist` — itens verificáveis que o leitor aplica no próprio time.
11. `## Referências` — fontes citadas, com data de acesso quando web.

Abertura antes da seção 1: título `# NN — Título`, uma linha de epígrafe opcional e um parágrafo
de 3–5 linhas que diga ao tech lead por que ler este capítulo.

## Regras

- **Português do Brasil.** Termos técnicos consagrados em inglês podem ficar (pull request,
  harness), em itálico na primeira vez.
- **Sigla nasce por extenso** na primeira ocorrência de cada capítulo: "Definition of Done (DoD)".
  Termo novo vai para `glossario.md` do capítulo.
- **Independente de ferramenta.** Claude Code, Spec Kit, LangGraph etc. aparecem como exemplos,
  nunca como premissa. O argumento sobrevive à troca do harness.
- **Regra de evidência.** Nenhuma afirmação quantitativa sem `[CLAIM-NN-NNN]` (NN = capítulo).
  Cada claim é registrado em `claims.md` do capítulo: id, afirmação, estado (`medido` |
  `observado` | `hipótese`), evidência reproduzível (caminho + commit no Maestro, comando, ou
  referência). Número que não se reproduz vira hipótese ou sai.
- **Nada inventado.** Ciclo, ADR, commit, achado e citação precisam existir. Na dúvida, abra o
  arquivo. Referência externa sem certeza da existência não entra.
- **Tamanho.** 4.000 a 8.000 palavras por capítulo; uma ideia por seção; exemplo antes de
  generalização.
- **Links** relativos entre capítulos (`../05-engenharia-de-contexto/capitulo.md`); fora do livro,
  URL completa (`https://github.com/GHDaru/maestro/blob/19823c2/...`).

## Arquivos de cada capítulo

```text
livro/NN-slug/
├── capitulo.md     o texto
├── claims.md       os claims do capítulo (tabela)
├── glossario.md    termos novos do capítulo (tabela termo | definição)
├── cobertura.md    itens do inventário cobertos → seção onde estão
└── exemplo/        README.md (como rodar + saída esperada) e os arquivos executáveis
```

Apêndices (`livro/apendices/x-slug/`) têm estrutura livre, mas seguem as regras acima.
