# Inventário do capítulo 8

Gerado de `pesquisa/inventario/itens.json` (02/11/2026).

## Itens PRINCIPAIS (31) — cada um tem de estar coberto neste capítulo

| id | fonte | resumo | falha real |
|---|---|---|---|
| CICLOS-B-039 | maestro:specs/067-trava-de-dominio-no-plan/spec.md | Ciclo 067 (retroativo): plan.md exige modelo de domínio declarado (linguagem ubíqua, agregados, invariantes), nunca omitido; o painel mostra quem pulou o plano. |  |
| CICLOS-B-040 | maestro:specs/067-trava-de-dominio-no-plan/spec.md · commit 14f77a5 (Hindiana, citado na spec) | No Hindiana uma rodada inteira entregou regras de negócio dentro de rotas porque o plano foi pulado; pular o plano não produzia sintoma. | sim |
| CICLOS-B-050 | maestro:specs/074-prototipo-navegavel/spec.md | Ciclo 074: protótipo navegável com ramo de interface (papel semântico, ux-design, gate de UX, jornada viva); verifica-navegacao.py --mutacao discrimina (boa 0, ruim 24). |  |
| CICLOS-A-001 | maestro:specs/001-governanca-didatica/spec.md @ abe1c1e | Ciclo 001 (raia plena): camada didática de onboarding nascida da queixa de governança 'amontoado de siglas sem dicionário e sem storytelling' — guia 'Comece por aqui' (dor → jornada → sistema) e glossário cobrindo 100% das siglas. Único ciclo da faixa sem qa-report.md. |  |
| DECISOES-007 | maestro:docs/adr/0010-principio-viii-comunicacao-inteligivel.md | ADR 0010: cria o Princípio VIII (sigla por extenso na primeira ocorrência de cada resposta/documento), brechas fechadas explicitamente; constituição sobe para 1.1.0. |  |
| DECISOES-011 | maestro:docs/adr/0014-ingles-no-instalavel.md | ADR 0014: a superfície instalável é escrita em inglês porque é lida por agentes em qualquer repositório; livro, receitas e site em português; check-language.sh guarda a fronteira. |  |
| DECISOES-020 | maestro:docs/adr/0023-modelo-de-dominio-declarado-no-plan.md | ADR 0023: o plan declara DOM:aggregate, DOM:invariants, DOM:glossary e DOM:ports com motivo; check-conformance lê a partir do 067 com piso que só aperta. |  |
| DECISOES-026 | maestro:docs/adr/0029-tela-em-portugues-codigo-em-ingles.md | ADR 0029 (emenda o 0014): interface em português, identificadores em inglês; model.yaml liga termo de tela ao identificador; camada anticorrupção quando o sentido não é 1:1. |  |
| DECISOES-066 | maestro:docs/records/decisoes.jsonl#achado-055-linguagem-ubiqua-prometida-e-ausente · commit 0e82c8c | plan-architect instruído a consumir linguagem ubíqua inexistente; promessa retirada — vocabulário pertence ao domínio. | sim |
| DECISOES-162 | maestro:docs/ecosystem/ideias/038-tecnicas-de-descoberta.md | Ideia 038: técnicas de descoberta e fronteira de domínio — observar. |  |
| LIVRO-METODO-116 | livro:maestro-handbook/handbook/13-decisoes-de-engenharia.md §5.6 | Corte por fronteira (DDD / arquitetura hexagonal): paralelizar por bounded context gera independencia; cortar bem e dificil e corte ruim aparece como economia baixa ou retrabalho. |  |
| LIVRO-METODO-167 | livro:maestro-handbook/handbook/apresentacao-desenvolvimento-maestro.html | check-language: residuo de portugues na superficie instalavel (ADR 0014). |  |
| LIVRO-METODO-203 | livro:maestro-handbook/diagramas/04-sipoc.md | SIPOC do ciclo de entrega; registra que a linguagem ubiqua entra como input so se o projeto mantiver uma, porque o metodo nao entrega nenhuma. |  |
| LIVRO-METODO-205 | livro:maestro-handbook/diagramas/05-bpmn-processo.md | Ramo de interface obrigatorio quando ha tela: papel semantico antes do componente (ux-semantics), ux-design.md, gate de UX, captura do build real e heuristica datada. |  |
| LIVRO-METODO-227 | maestro:docs/jornada/074-prototipo-navegavel.md | H3/H4: a constante QUEBRA_NAVEGACAO = 768 validada no build (rotulo cabe) e a barra construida sem o icone que o desenho previa. |  |
| LIVRO-METODO-237 | maestro:docs/livro/guia-editorial.md §3 | Regras de escrita permanentes: sigla nunca nasce nua (Principio VIII), evidencia por caminho, tabela so para fato enumeravel, uma ideia por secao. |  |
| LIVRO-METODO-247 | livro:pesquisa/base-de-pesquisa.md §Tese | Conceito: catalogo semantico como Ubiquitous Language operacional, com REUSE / EXTEND / ALIAS / CREATE antes de criar objeto. |  |
| LIVRO-METODO-302 | livro:pesquisa/base-de-pesquisa.md §Referencias | Evans / Fowler (Domain-Driven Design). |  |
| GOV-009 | maestro:docs/governance/principles.md | Princípio VIII, comunicação inteligível: Iron Law de que toda sigla nasce por extenso na primeira ocorrência de cada resposta ou documento, com as desculpas típicas fechadas; termo novo entra no glossário. |  |
| GOV-011 | maestro:docs/governance/principles.md | Regra de idioma (ADR 0014): o método instalável (agentes, skills, scripts, comandos, templates, governança) é em inglês porque é lido por agentes em qualquer repositório; o livro e o site são em português. |  |
| GOV-034 | maestro:docs/governance/axioms.md | Corolário C10: o que é instalado é lido por máquina; o que é publicado é lido por gente (ADR 0014: toolkit em inglês, livro em português), de A4. |  |
| GOV-062 | maestro:docs/governance/glossary.md | Glossário como linguagem ubíqua do método: cada sigla expandida, com o significado no Maestro e onde aparece; termo novo entra aqui (Princípio VIII). |  |
| GOV-063 | maestro:docs/governance/glossary.md | Colisão de nomes: cinco colisões vivas mapeadas ('fila', 'caixa de entrada', 'livro de ponto', 'sessão' x 'agente', 'portão'); regra operativa de que 'fila' e 'portão' nunca são escritos nus. |  |
| GOV-064 | maestro:docs/governance/glossary.md | Colisão de endereço: o mesmo identificador apontando para duas sessões ou nenhuma; invariante de que endereço ambíguo é recusado, nunca resolvido, porque entrega ao par errado não se desfaz. |  |
| GOV-067 | maestro:docs/governance/glossary.md; maestro:.specify/templates/plan-template.md | Modelo de domínio declarado (ciclo 067, ADR 0023): o plan declara raiz de agregado, onde moram as invariantes, mudanças de linguagem ubíqua e portas/adaptadores (DOM:aggregate/invariants/glossary/ports), lidos por check-conformance.sh; silêncio não é decisão. |  |
| GOV-092 | maestro:skills/fight-the-pile-up/SKILL.md | Skill fight-the-pile-up: Iron Law 'nenhuma sigla nua'; checklist editorial que transforma documento denso (siglas sem dicionário, tudo numa página, sem narrativa) em texto claro sem mudar o conteúdo técnico. |  |
| GOV-127 | maestro:.claude/agents/ux-semantics.md | Agente ux-semantics: define ux-design.md antes de qualquer tela: o papel semântico de cada objeto derivado do catálogo e a jornada que serve; não implementa componentes. |  |
| GOV-128 | maestro:.claude/agents/didactics-editor.md | Agente didactics-editor: storytelling, glossário e clareza contra a 'amontoação'; muda a forma, não as decisões técnicas. |  |
| GOV-158 | maestro:scripts/check-language.sh | check-language.sh: mede resíduo de português na superfície instalável (ADR 0014), não 'detecta inglês'; livro, specs/ e o índice append-only ficam fora de propósito. |  |
| GOV-175 | maestro:scripts/check-docs-generated.sh | check-docs-generated.sh (ciclo 076): a seção de Documentação do app é gerada do modelo de domínio (model.yaml); sha256 registrado na seção e na projeção, e a CI regera os textos e compara byte a byte. |  |
| GOV-192 | maestro:.specify/templates/ux-design-template.md | Template de ux-design: papéis semânticos consumidos e introduzidos antes do componente. |  |

## Itens SECUNDÁRIOS (16) — o capítulo principal é outro; cite ou remeta quando servir ao argumento

| id | fonte | resumo | principal |
|---|---|---|---|
| CICLOS-B-054 | maestro:specs/075-protocolo-entre-sessoes/spec.md | Ciclo 075: protocolo próprio entre sessões (envelope interno, identidade nome · projeto, ref como localizador, contextId só na borda A2A, SSE), redesenhado pela V2 das bancas. | 6 |
| CICLOS-B-058 | maestro:specs/076-padroes-de-engenharia-e-react/critica-t035b-documentacao.md · commit d9f82f9 | Crítica às cegas reprovou a T035b: CI não regerava do modelo, referências internas no visível, mapa de contextos ausente; o cego perdeu para o ddd-by-examples/library. | 2 |
| CICLOS-B-059 | maestro:specs/076-padroes-de-engenharia-e-react/critica-t035c-t036-documentacao.md · commit a655b75 | Crítica conjunta reprovou T035c+T036: Sessão sem resposta de operador, o cego perdeu de novo, CI vermelha pelo check-language. | 2 |
| CICLOS-B-062 | maestro:specs/076-padroes-de-engenharia-e-react/ux-design.md · commit 103604f | Regra do Darú: o agente ux-semantics define o papel semântico de derrubar sessão (confirmação irreversível, pedido de decisão com prazo) antes do verde da T047. | 7 |
| DECISOES-028 | maestro:docs/adr/0031-abas-de-contexto-no-topo.md | ADR 0031: vistas irmãs viram abas no topo (SectionTabs) e a regra (ag) do verificador do 074 deixa de valer, com dívida legada declarada. | 3 |
| DECISOES-085 | maestro:docs/records/decisoes.jsonl#decisao-073-gauntlet-area-administrativa | Gauntlet do 073: 25 plataformas × 26 funcionalidades, confronto 16/5/11, wireframes e três juízes em contexto fresco. | D |
| DECISOES-088 | maestro:docs/records/decisoes.jsonl#decisao-074-prototipo-navegavel | Abertura do 074: protótipo clicável por contexto delimitado com contrato de ações simuladas e DoD verifica-navegacao.py. | 3 |
| LIVRO-METODO-046 | livro:maestro-handbook/handbook/05-orquestracao.md §5.1 | O corte e mais traicoeiro que o reduce: paralelizar por fronteira (contexto delimitado, contrato, camada), nunca por quantidade; nenhuma reconciliacao salva fatia cortada fora da costura. | 6 |
| LIVRO-METODO-170 | livro:maestro-handbook/handbook/apresentacao-desenvolvimento-maestro.html | check-boundary: todo arquivo pertence a exatamente um dominio (ADR 0018). | 9 |
| LIVRO-METODO-224 | maestro:docs/jornada/074-prototipo-navegavel.md | Jornada do prototipo navegavel: sete capturas do build real (seis rotas do menu e 360 px) com fixtures reais, uma rota por pagina limpa; nao substitui a banca em contexto fresco. | 10 |
| LIVRO-METODO-225 | maestro:docs/jornada/074-prototipo-navegavel.md; maestro commit 0653e9d | H1: o ux-design dizia que seis itens cabiam na barra a ~360 px; medido, o menu precisa de 399 px e 'Mensageria' transborda 38,8 px. | 10 |
| LIVRO-METODO-255 | livro:pesquisa/base-de-pesquisa.md §Agenda H6 | H6: catalogo semantico reduz duplicacao. | 15 |
| LIVRO-METODO-256 | livro:pesquisa/base-de-pesquisa.md §Agenda H7 | H7: glossario reduz inconsistencia. | 15 |
| LIVRO-METODO-266 | livro:pesquisa/base-de-pesquisa.md §Agenda GOV-002 | GOV-002: componente duplicado. | B |
| GOV-065 | maestro:docs/governance/glossary.md | Ref de sessão expira ao reiniciar; por isso a identidade de sessão é escrita 'nome · ref · projeto' e endereçar é por ref, nunca pelo 'mais provável'. | 3 |
| GOV-066 | maestro:docs/governance/glossary.md | Agente (perfil) x sessão de agente: o perfil é o par arquivo em .claude/agents + executável, sem ref; a sessão é uma execução, unidade de administração que o humano sobe, observa e derruba. | 7 |
