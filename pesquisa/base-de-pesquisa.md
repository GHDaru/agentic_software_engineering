# Base de pesquisa para o livro (resumo de 01/11/2026)

> Resumo do documento «Engenharia de Software Orientada por Agentes: base de pesquisa para o
> livro Maestro», colado pelo Darú em 01/11/2026. O texto integral não foi salvo: se for
> preciso, cole-o em `pesquisa/base-de-pesquisa-integral.md`.

## Tese

O Maestro não é mais um framework de agentes: é um sistema de **governança operacional** para
engenharia de software agêntica — constituição, raias, papéis, artefatos, gates, ADRs, skills,
scripts e hooks — que roda sobre diferentes harnesses e modelos. A pergunta do livro: por que
agentes mudam a economia da engenharia, que problemas novos trazem, como governá-los, como
testar uma metodologia para agentes e que evidência sustenta as afirmações.

Conceitos centrais: instrução não é enforcement · quem executa não verifica (revisão em
contexto fresco) · autonomia proporcional à irreversibilidade × raio · o check mede o proxy e
não o fato (a qualidade migra de «o agente errou» para «o gate mede a coisa errada») · contexto
é recurso finito (seleção, compressão, persistência, transferência) · catálogo semântico
(Ubiquitous Language operacional: REUSE / EXTEND / ALIAS / CREATE antes de criar objeto).

## Quatro corpora

1. Método normativo (Maestro `docs/governance`). 2. Handbook do método (por versão).
3. **Livro** (argumento durável). 4. **Pesquisa** (protocolo, runs, datasets, replication).

## Sumário proposto (16 capítulos)

1. A mudança de unidade de trabalho · 2. O problema da confiança · 3. Um humano, muitos agentes ·
4. A spec como partitura · 5. Engenharia de contexto · 6. Como dividir o trabalho ·
7. Papéis, skills e ferramentas · 8. DDD para agentes · 9. Arquitetura que se defende ·
10. Quality Gates que provam fatos · 11. Risco, reversibilidade e autonomia ·
12. MCP e o ecossistema de ferramentas · 13. Observabilidade e economia ·
14. A organização que aprende · 15. Validando o Maestro · 16. O futuro da engenharia agêntica.

Anatomia: pergunta central, resultado de aprendizagem, falha real antes da regra, teoria,
alternativas, padrão Maestro, exemplo executável, contraexemplo, evidência, checklist,
referências.

## Agenda de pesquisa

- Hipóteses H1–H10: spec reduz retrabalho; revisão fresca acha mais defeito; contexto seletivo
  reduz custo sem perder qualidade; multiagente só ajuda com cortes independentes; gate com teste
  de mutação reduz escapes; catálogo semântico reduz duplicação; glossário reduz inconsistência;
  reversibilidade permite mais autonomia; modelo menor basta em tarefa estruturada;
  retrospectiva→regra reduz recorrência.
- Desenho: baseline A (prompt) · B (spec) · C (spec + gates) · tratamento (Maestro completo);
  repetições com distribuição e intervalo; ambiente congelado (commit, modelo, harness, hashes).
- Corpora: ciclos históricos do Maestro; SWE-bench e SWE-Bench Pro; um benchmark de governança
  (ASEG-Bench, GOV-001 a GOV-010: feature sem spec, componente duplicado, dependência proibida,
  ADR reescrito, só caminho feliz, gate que mede texto, ação irreversível sem rollback, ferramenta
  desnecessária, autor que aprova a si mesmo, prompt injection na documentação).
- Métricas: custo por tarefa aceita, custo do retrabalho, tokens por tarefa, tempo de ciclo,
  espera humana, overhead de coordenação, aceitação na primeira passada, retrabalho, escape de
  gate, rendimento da revisão independente; métricas DORA (cinco).
- No repositório: `protocol.md` + `runs/` com schema imutável; gate mutation estruturado
  (propriedade, fixture positiva, fixture negativa, resultado esperado); `CLAIMS.md` (nenhum
  número sem claim ID); tags e releases reproduzíveis; telemetria compatível com OpenTelemetry,
  com minimização (LGPD); comando `maestro inspect-context <ciclo>`.

## Riscos e regulação

OWASP GenAI Top 10 (prompt injection, excessive agency…), NIST AI RMF e perfil generativo,
AI Act (aplicação escalonada), LGPD e o sandbox da ANPD. Regra: tracing não é retenção
indiscriminada.

## Referências-base

SWE-bench (Jimenez et al.), SWE-agent (Yang et al.), MetaGPT (Hong et al.), He/Treude/Lo
(TOSEM 2025), SWE-Bench Pro (Deng et al.), Evans/Fowler (DDD), ADR/MADR, OMG BPMN 2.0.2,
DORA 2025, GitHub Spec Kit, Model Context Protocol, Archify, Claude Code, LangGraph, CrewAI,
Google ADK, Microsoft Agent Framework, OpenAI Agents SDK, NIST AI RMF, OWASP GenAI, AI Act,
LGPD/ANPD.
