# Glossário do capítulo 14

| termo | definição |
|---|---|
| achado | Defeito ou lição que não coube no ciclo em que apareceu; entra no índice de decisões como `achado-NNN-<slug>`, com status `aberta`, até uma linha posterior fechá-lo. |
| achado que morre em candidato | Anti-padrão 14 do Maestro: registrar "regra candidata" e nunca rodar a retrospectiva que a transformaria em regra. |
| ADR (*architecture decision record*) | Registro de decisão de arquitetura no formato de Nygard (contexto, decisão, consequências). Imutável: nunca fica desatualizado, só superado por um ADR novo. |
| apodrecimento | Envelhecimento silencioso de um artefato que ninguém consome ou que não falha quando fica velho; continua parecendo válido. |
| artefato que congela | Anti-padrão 15: roadmap, índice ou mapa que para de ser atualizado e continua sendo lido como verdade. |
| aprendizado de laço duplo (*double-loop learning*) | Termo de Argyris e Schön: o laço simples corrige o erro; o duplo muda a regra que o produziu. Com agentes, só o duplo deixa memória. |
| BPMN (*Business Process Model and Notation*) | Notação padrão de diagramas de processo; o Maestro desenha nela o próprio fluxo. |
| cerimônia sem gatilho | Anti-padrão 17: cerimônia recorrente sem condição mensurável que a dispare; acontece quando alguém lembra, isto é, raramente. |
| CI (*continuous integration*) | Integração contínua: a execução automática de testes e portões a cada mudança enviada ao repositório. |
| corolário C1 | Do Maestro: toda cerimônia tem gatilho, e o gatilho é mensurável. Deriva de T6. |
| corolário C9 | Do Maestro: documentação que nada consome apodrece, por melhor que seja. Deriva de T5. |
| dívida de retro | Número de achados abertos e idade do mais velho; quando passa do limite (quatro abertos ou seis ciclos, no Maestro), a retrospectiva é obrigatória. |
| DoD (*Definition of Done*) | Definição de pronto: critérios verificáveis que um trabalho cumpre antes de ser dado como concluído. |
| `fecha` (campo) | Campo estrutural de uma linha do índice de decisões que aponta o id do achado que ela fecha. O portão lê o campo, nunca a prosa. |
| função de força (*forcing function*) | Mecanismo que faz a regra ser cumprida sem depender de lembrança: um portão que falha, um hook que recusa. |
| guarda (hook) | Verificação que roda **antes** da ação e a recusa; o portão, ao contrário, audita depois. |
| índice de decisões | `docs/records/decisoes.jsonl` no Maestro: uma linha JSON por decisão, achado, gate ou retro; só cresce. |
| JSONL (*JSON Lines*) | Formato de arquivo com um objeto JSON (*JavaScript Object Notation*) por linha. |
| MADR (*Markdown Architectural Decision Records*) | Variante de ADR em Markdown com campos para as alternativas consideradas. |
| memória só-anexar (*append-only*) | Registro em que nada se reescreve: corrigir é acrescentar uma linha ou um ADR que supera o anterior. |
| ossificação | Modo de falha de quem só aprende: regras acumulam porque adicionar é barato e remover é caro, até ninguém saber quais estão vivas. |
| poda | Remoção ativa do que não paga o próprio custo, com gatilho e motivo escritos; inclui a lista do que não se adota. |
| PRD (*product requirements document*) | Documento de requisitos de produto; avulso, duplica a spec. |
| retrospectiva (retro) | Cerimônia que transforma correção repetida em regra versionada, poda a regra que não pagou o custo e transforma passo manual repetido em script ou skill. |
| RFC (*request for comments*) | Proposta escrita circulada para comentários antes da decisão; no Maestro, rejeitada como processo pesado. |
| SRE (*site reliability engineering*) | Engenharia de confiabilidade de sites, a disciplina do Google de onde vem o postmortem sem culpa. |
| Steward | No Maestro, o humano que responde pelo método. |
| teatro de cerimônia | Anti-padrão 11: processo que não muda decisão nenhuma; gate que nunca rejeita. |
| teorema T5 | Do Maestro (A3 + A4): um artefato sobrevive por consumo ou por imutabilidade. |
| teorema T6 | Do Maestro (A3 + A4): a correção que não vira regra versionada se repete. |
| YAGNI (*you aren't gonna need it*) | "Você não vai precisar disso": a complexidade além do necessário é justificada por escrito ou removida. |
