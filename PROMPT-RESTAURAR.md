# Prompt para restaurar o contexto — Livro de Engenharia de Software Orientada por Agentes

> Cole o bloco abaixo numa sessão nova, aberta nesta pasta
> (`C:\Users\ghdaru\Documents\010_PROJETOS\470_LIVRO_ESOA`). Ele substitui a memória da sessão
> MAESTRO (a regente), limpa em 01/11/2026.

---

```text
Você vai trabalhar no LIVRO "Engenharia de Software Orientada por Agentes", nesta pasta
(470_LIVRO_ESOA). O livro é um bounded context PRÓPRIO, separado do repositório do método
Maestro (C:\Users\ghdaru\Documents\010_PROJETOS\410_MAESTRO, GitHub GHDaru/maestro). O Maestro
entra no livro como OBJETO DE ESTUDO, não como dono do livro.

Leia primeiro, nesta ordem:
1. README.md desta pasta (o mapa).
2. pesquisa/base-de-pesquisa.md (as decisões editoriais e a agenda de pesquisa).
3. maestro-handbook/handbook/README.md e os 13 capítulos (o livro atual do método, copiado do
   Maestro em 01/11; ORIGEM.txt diz de que commit).
Leia o Maestro (somente leitura daqui) quando precisar de evidência: docs/governance/
(constituição, princípios I–VIII, modelo operacional, glossário, axiomas), skills/anti-patterns,
CHANGELOG.md, specs/NNN (os ciclos), docs/adr e docs/records/decisoes.jsonl.

O que é o Maestro, em uma linha: método de UM humano regendo N agentes de IA; a spec é a fonte
da verdade, os agentes executam e revisam, o humano decide, aprova e verifica. Ciclo: spec →
plan (Constitution Check) → tasks → vermelho/verde (TDD) → revisão em contexto fresco → gate
humano → merge. Raias leve/plena/infra por ambiguidade × raio × irreversibilidade. Regras
viram scripts, hooks e gates ("instrução não é enforcement").

Decisões editoriais já tomadas pelo Darú (01/11/2026):
- QUATRO corpora separados: método normativo (no Maestro: docs/governance), handbook do método
  (referência por versão), LIVRO (argumento durável, independente de ferramenta) e corpus de
  PESQUISA (runs, datasets, traces sanitizados, replication package).
- Tese: o diferencial do Maestro é GOVERNANÇA OPERACIONAL sobre qualquer runtime de agentes
  (não competir com LangGraph, CrewAI, Google ADK, Microsoft Agent Framework, OpenAI Agents SDK).
  Ideias-chave: "quem executa não verifica"; autonomia proporcional à irreversibilidade;
  "o check mede o proxy e não o fato"; contexto é recurso finito.
- Anatomia de capítulo: pergunta central · resultado de aprendizagem · FALHA REAL antes da
  regra · teoria · alternativas · padrão Maestro · exemplo executável · contraexemplo ·
  evidência · checklist · referências.
- Regra de evidência: nenhuma afirmação quantitativa sem CLAIM ID (CLAIMS.md) e evidência
  reproduzível; hipótese é marcada como hipótese.
- Escrita em português do Brasil; sigla nasce por extenso na primeira ocorrência de cada
  capítulo (Princípio VIII do Maestro).

Primeira tarefa: propor (sem escrever capítulos ainda) a estrutura de pastas do livro em
livro/, o sumário final a partir do proposto em pesquisa/base-de-pesquisa.md, e o mapa de
"o que reaproveitar do handbook do Maestro em cada capítulo". Pergunte só o que for decisão
minha.

Pendência no repositório do Maestro (não faça daqui sem pedir): retirar o livro de lá por um
ciclo de raia plena — ADR que substitui o 0011, e ajustar CLAUDE.md, README, boundary.json,
publicar/build.mjs, scripts/check-chapters.sh e check-language.sh, o companion e o plugin.
```
