# Inventário do capítulo A

Gerado de `pesquisa/inventario/itens.json` (02/11/2026).

## Itens PRINCIPAIS (16) — cada um tem de estar coberto neste capítulo

| id | fonte | resumo | falha real |
|---|---|---|---|
| CICLOS-B-014 | maestro:specs/053-pecas-de-apresentacao/spec.md | Ciclo 053 (leve): fluxo v5 como desenho proposto não vigente e caderno de desenvolvimento; revisão reprovou com oito grupos de defeito e check-retro vermelho por dívida anterior. |  |
| LIVRO-METODO-002 | livro:maestro-handbook/handbook/README.md | Os 12 elementos do modelo operacional ([1]..[12]) mapeados para 13 capitulos, com ordem de leitura = ordem de dependencia e rotulo do elemento distinto do numero do capitulo. |  |
| LIVRO-METODO-149 | livro:maestro-handbook/handbook/apresentacao-executiva-maestro.html | Deck executivo de 10 slides: dois extremos que falham, 12 elementos em 5 camadas, seis pilares e o metodo construido por ele mesmo. |  |
| LIVRO-METODO-164 | livro:maestro-handbook/handbook/apresentacao-desenvolvimento-maestro.html | Tres coisas a guardar: a intencao vive na spec; norma que ninguem confere nao existe (vira check-*.sh); reversibilidade compra velocidade. |  |
| LIVRO-METODO-165 | livro:maestro-handbook/handbook/apresentacao-prompts-imagens.md | Prompts de imagem do deck executivo com direcao de arte unica (maestro regendo orquestra de nos de luz), sem texto e com espaco negativo. |  |
| LIVRO-METODO-198 | livro:maestro-handbook/diagramas/01-definicao.md | Metafora do nome: a partitura (spec) diz o que tocar, o compasso (gates) marca o ritmo, os musicos (agentes) executam; um humano rege, muitos agentes executam. |  |
| LIVRO-METODO-199 | livro:maestro-handbook/diagramas/01-definicao.md | Tres ideias que costuram o metodo: spec como fonte de verdade, humano responde pela politica, reversibilidade compra velocidade. |  |
| LIVRO-METODO-201 | livro:maestro-handbook/diagramas/03-fluxo.md | Linha do tempo do ciclo com quem executa cada passo (Steward, spec-agent, plan-architect, dev-implementer, review/security/qa, tech-writer) e os gates humanos. |  |
| LIVRO-METODO-204 | livro:maestro-handbook/diagramas/05-bpmn-processo.md | BPMN em sete raias (Steward, agentes, ramo de interface, automacao, distribuicao, portoes, artefatos), navegavel: cada caixa e link para o capitulo que a define. |  |
| LIVRO-METODO-213 | livro:maestro-handbook/diagramas/maestro-workflow.archify.html | Ciclo em planta gerado pelo Archify (retrato de 22/10, commit 39a86ba), interativo em cinco raias e sem os portoes do ADR 0030. |  |
| LIVRO-METODO-214 | livro:maestro-handbook/diagramas/README.md | Codigo de cores das pecas 01-05 (violeta agente, ouro humano/gate, verde verificado) e PDFs renderizados de HTML por Playwright (render-pdf.mjs). |  |
| LIVRO-METODO-231 | maestro:docs/comece-por-aqui.md | O sistema em 12 elementos e 5 camadas (fundamento, mecanica, estrutura, qualidade, governanca). |  |
| LIVRO-METODO-232 | maestro:docs/comece-por-aqui.md | Mapa de leitura: principios, modelo operacional, handbook e pratica pelos templates (/speckit.specify, PR template, /dod), com glossario para toda sigla. |  |
| LIVRO-METODO-239 | maestro:docs/livro/guia-editorial.md §5-6 | Cinco trilhas do site (Jornada, Capitulos, Receitas, Referencia, Bastidores) e cadencia educacional (Entender 20 min, Aprender 2 h, Aplicar 1 dia, Aprofundar). |  |
| LIVRO-METODO-304 | livro:pesquisa/base-de-pesquisa.md §Referencias | OMG BPMN 2.0.2. |  |
| LIVRO-METODO-308 | livro:pesquisa/base-de-pesquisa.md §Referencias | Archify. |  |

## Itens SECUNDÁRIOS (28) — o capítulo principal é outro; cite ou remeta quando servir ao argumento

| id | fonte | resumo | principal |
|---|---|---|---|
| CICLOS-B-022 | maestro:specs/058-a-porta-da-frente/spec.md · commit 7bef06a | Ciclo 058 (infra): bin/maestro init, porta da frente interativa à moda do specify init, e portão check-flags. | 12 |
| CICLOS-A-028 | maestro:specs/019-distribuicao-e-templates/spec.md @ 93a05cd | Ciclo 019: distribuição em três camadas (script local, plugin do Claude Code empacotado das fontes, compatibilidade com npx skills add), portão empacotar-plugin.sh --verificar e ADR 0012 com o racional de não construir CLI próprio. | 12 |
| CICLOS-A-063 | maestro:specs/035-axiomas-e-bpmn-v4/spec.md @ c46cc33 | Ciclo 035: camada de derivação do método — cinco axiomas com teste de independência, teoremas com evidência do repositório (inclusive desfavorável) e corolários (ADR 0015) — e BPMN v4 com a raia de portões e a retro com gatilho. | 14 |
| DECISOES-012 | maestro:docs/adr/0015-axiomas-teoremas-corolarios.md | ADR 0015: axioms.md com 5 axiomas (A1–A5), 6 teoremas com evidência do repositório e 10 corolários; teorema que não pode ser mostrado falhando é crença. | 14 |
| DECISOES-096 | maestro:docs/roadmap.md | O roadmap: ordem de leitura, inventário, curadoria, fases F0–F35 (fase = ciclo = spec = gate) e a régua de avaliação. | 14 |
| DECISOES-101 | maestro:docs/roadmap.md#F8-F9 | F8–F9: método instalável (ux-semantics, living-journey, três camadas) e BPMN navegável. | 7 |
| DECISOES-118 | maestro:CHANGELOG.md#0.1.0 | v0.1.0: primeira linha de base após zero versões em 44 ciclos — 13 agentes, 6 skills, 22 anti-padrões, 11 portões, um eval provado por ablação. | 15 |
| LIVRO-METODO-004 | livro:maestro-handbook/handbook/01-principio-central.md | Principio operacional central: IA explora, propoe e escreve; humano especifica, decide e aprova; testes, gates e revisao independente validam. | 2 |
| LIVRO-METODO-007 | livro:maestro-handbook/handbook/01-principio-central.md §5.3 | Reversibilidade como alavanca: backup, dry-run, homologacao e soft-delete mudam a classe de risco e tornam a acao delegavel; reversibilidade compra velocidade. | 11 |
| LIVRO-METODO-026 | livro:maestro-handbook/handbook/03-spec-driven.md §5.3 | Raias leve/plena/infra decididas por ambiguidade x raio x irreversibilidade; na leve o PR e o artefato e bug exige teste que reproduz. | 4 |
| LIVRO-METODO-054 | livro:maestro-handbook/handbook/06-papeis-raci.md §5.1 | RACI adaptado a humano x agentes: R e C delegados a agentes, I ao registro, e exatamente um A por tarefa, sempre humano; o A nao migra. | 7 |
| LIVRO-METODO-074 | livro:maestro-handbook/handbook/08-entregaveis-artefatos.md §5.4 | Catalogo de artefatos avaliado: spec, plano, tarefas (efemero), codigo+testes, ADR, jornada, changelog, indice de decisoes e DoR/DoD essenciais; diagramas depois, painel de metricas YAGNI. | 14 |
| LIVRO-METODO-092 | livro:maestro-handbook/handbook/10-gates-classes-de-risco.md §5.2 | Taxonomia de sete classes de risco: leitura, leitura sensivel, criacao reversivel, alteracao, exclusao/efeito externo, financeira/irreversivel (dupla aprovacao) e lote/entre inquilinos/administrativa (bloqueada). | 11 |
| LIVRO-METODO-105 | livro:maestro-handbook/handbook/12-governanca-leve.md §5.2 | Camadas com velocidades diferentes: constituicao devagar (emenda versionada), modelo operacional e livro rapido, ADRs nunca, skills e scripts conforme a dor. | 14 |
| LIVRO-METODO-113 | livro:maestro-handbook/handbook/13-decisoes-de-engenharia.md §4.1 | Quadro das 14 decisoes de engenharia do Maestro com data e registro (Principio, ADR ou ciclo), mapa didatico dos ADRs. | 14 |
| LIVRO-METODO-200 | livro:maestro-handbook/diagramas/02-problema-solucao.md | Problema-solucao: sem IA o legado exige duzias de pessoas; com IA sem metodo o agente compila e erra a intencao; o Maestro e o metodo no meio. | 1 |
| LIVRO-METODO-203 | livro:maestro-handbook/diagramas/04-sipoc.md | SIPOC do ciclo de entrega; registra que a linguagem ubiqua entra como input so se o projeto mantiver uma, porque o metodo nao entrega nenhuma. | 8 |
| GOV-001 | maestro:docs/governance/principles.md | A constituição do método (v1.3.0): prevalece sobre qualquer prática, toda emenda passa por ADR e bump semântico (MAJOR remove/redefine, MINOR acrescenta, PATCH esclarece). | 14 |
| GOV-002 | maestro:docs/governance/principles.md | Princípio I, spec-driven: nenhum código nasce sem especificação; a spec é o insumo que gera o código (por isso não apodrece) e mudança de escopo volta à spec antes de virar código. | 4 |
| GOV-004 | maestro:docs/governance/principles.md | Princípio III (NÃO NEGOCIÁVEL), reversibilidade e gates proporcionais ao risco: o gate humano escala com irreversibilidade x raio de impacto; reversibilidade engenheirada (backup, dry run, staging, soft delete) rebaixa a classe de risco; política allow/deny/ask fora do modelo. | 11 |
| GOV-005 | maestro:docs/governance/principles.md | Princípio IV, test-first e DoD verificável ('prove it, don't claim it'): pronto é um pass/fail que o agente produz e um hook confirma; verde local não é certo global, e a coerência global fica com o humano. | 10 |
| GOV-012 | maestro:docs/governance/axioms.md | Camada de derivação (ADR 0015/0016/0019): axioma assumido, teorema provável no repositório, corolário que muda decisão; toda regra nova deve derivar de um axioma, senão é axioma novo (via ADR) ou cerimônia (podada). | 14 |
| GOV-038 | maestro:docs/governance/operating-model.md | Princípio operacional central (§2): IA para explorar, propor e escrever; humano para especificar, decidir e aprovar; testes, gates e revisão independente para validar. | 1 |
| GOV-039 | maestro:docs/governance/operating-model.md | Raias de trabalho (§3, ADR 0005): leve (o PR é o artefato), plena (spec completa) e infra (sempre plena + gates de reversibilidade); o valor da spec escala com ambiguidade x raio x irreversibilidade. | 4 |
| GOV-048 | maestro:docs/governance/operating-model.md | Definition of Done (§7) e DoD reduzida da raia leve: testes, fitness functions, lint/type, revisão independente, gate leve de segurança, docs vivas no mesmo PR, rastreabilidade e evidência anexada. | 10 |
| GOV-050 | maestro:docs/governance/operating-model.md | Mapa de classes de risco (§8): leitura, leitura sensível, criação reversível, alteração, exclusão/ação externa, financeira/irreversível e lote/cross-tenant/admin (bloqueada), cada uma com o gate humano correspondente. | 11 |
| GOV-164 | maestro:scripts/check-conformance.sh | check-conformance.sh: resposta executável a 'você está seguindo o Maestro?'; mede se o método sobreviveu nos artefatos que o executor consome (declarações ART/DOM, closing tail com evidência), não qualidade nem se o humano leu. | 15 |
| GOV-201 | maestro:CLAUDE.md | CLAUDE.md como instrução que a IA lê antes de trabalhar: constituição importada, skills primeiro, fluxo, raias, closing tail, protocolo de tags e 'não responda de memória: rode check-conformance.sh'. | 5 |
