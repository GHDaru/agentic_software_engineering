# Glossário do capítulo 5

| termo | definição |
|---|---|
| Engenharia de contexto | Decidir, como prática de engenharia e não de *prompt*, o que um agente lê, o que descarta e o que tem de sobreviver fora dele. Quatro operações: seleção, compressão, persistência e transferência. |
| Janela de contexto | O texto que o modelo lê de uma vez: instrução, conversa, arquivos, saídas de ferramenta. É finita e o desempenho cai à medida que ela enche (axioma A3). |
| *Token* | Unidade em que o modelo mede texto. No exemplo do capítulo, estimado como caracteres ÷ 4 — régua grosseira, declarada. |
| Orçamento de contexto | A janela vista como recurso que se gasta: toda prática de trabalho com agentes é uma decisão de gasto. "Contexto é orçamento, não depósito." |
| Seleção | Operação que decide o que entra na janela de uma tarefa (agente estreito, subagente, tarefa que cita seus arquivos). |
| Compressão | Operação que transforma o que já entrou em menos (plano como exploração destilada, resumo, compactação). |
| Compactação | Compressão feita pelo *harness* quando a janela enche: ela escolhe o que fica, e o resto é apagado, não degradado (corolário C12). |
| Persistência | Operação que garante que algo exista depois que a janela fecha: spec, plano, tarefas, relatório, índice de decisões, ADR. |
| Transferência | Operação que entrega à próxima sessão o que esta sabia: arquivo de instrução, carga de estado no início, revisor que começa do zero com diff e critério. |
| Contexto integrador | O que toda fatia de trabalho precisa carregar para que as fatias se encaixem: objetivo, invariantes e contratos — a spec (Princípio V). |
| Ótimo local | Cada fatia perfeita e o conjunto quebrado, porque nenhum executor viu o todo; preço de cortar demais ou na costura errada. |
| Economia de contexto | 1 − (o que a tarefa carrega ÷ o que o repositório tem). Economia consistentemente baixa é sinal de corte errado, não de janela pequena. |
| Despejo de contexto (*context dump*) | Anti-padrão 1: colar a base inteira no *prompt*. |
| Contexto tribal | Anti-padrão 2: intenção que só existe na cabeça do operador. |
| Reset preguiçoso | Anti-padrão 3: limpar a sessão por reflexo; o gatilho certo é a troca de papel, não o turno. |
| Repetição cega | Anti-padrão 5: repetir o mesmo *prompt* esperando outro resultado; falhou duas vezes, mude *prompt*, contexto ou tarefa. |
| Tarefa de contexto zero | Tarefa escrita para quem não viu a conversa: cita arquivo ou comando e tem critério de pronto. Absorvida do Superpowers ("assuma zero contexto"). |
| Cauda do ciclo (*closing tail*) | Os passos de fechamento — revisão independente, segurança, mutação, gate humano — escritos no `tasks.md` como *tokens* `TAIL:` que um script procura. |
| Arquivo de instrução | Arquivo que o *harness* lê no início de toda sessão (`CLAUDE.md`, `AGENTS.md`, regras de projeto). Custo fixo de contexto de todas as sessões. |
| Fonte única (da instrução) | Uma instrução só; outros nomes que a ferramenta lê são link simbólico ou cópia gerada, conferida por igualdade de conteúdo (ADR 0013 do Maestro). |
| Bloco gerado do disco | Trecho da instrução montado por script a partir do que existe (as skills), e não escrito à mão. |
| Skill invisível | Skill que existe no disco e não é citada na instrução; para a IA, não existe. |
| Deriva | Divergência silenciosa entre um documento escrito à mão e o fato que ele descreve (o disco, outra cópia). |
| *Hook* | Comando que o *harness* dispara num evento (início de sessão, antes de usar uma ferramenta, fim do turno), sem ninguém pedir. |
| Carga de estado (*SessionStart*) | *Hook* de início de sessão que imprime fatos medidos agora (ciclo aberto, conformidade, achados); no Maestro dispara também após a compactação. "Carregado em vez de lembrado." |
| Índice só-acréscimo | Registro em que cada linha é um fato imutável; corrigir é acrescentar uma linha que "fecha" a anterior, nunca reescrever. |
| Livro de ponto | Registro só-acréscimo de eventos de tarefa (atribuída, iniciada, encerrada, custo). |
| Rastreabilidade para frente / para trás | Para frente: a intenção virou código e teste? (cobertura). Para trás: este sintoma vem de qual mudança, requisito e porquê? (recuperação, o sentido a otimizar). |
| Elo por convenção | Ligação entre artefatos mantida por um formato combinado (o commit cita o ciclo); vive de hábito até um portão cobrá-la. |
| *Progressive disclosure* | Carregar o corpo de uma instrução (uma skill) só quando ela se aplica, em vez de sempre. |
| *Retrieval-Augmented Generation* (RAG) | Geração aumentada por recuperação: buscar por similaridade o trecho relevante e pô-lo na janela. |
| *Product Requirement Prompt* (PRP) | Spec que empacota o contexto do codebase de que o agente vai precisar (arquivos, convenções, exemplos). |
| Claude Code Project Manager (CCPM) | Ferramenta que põe a rastreabilidade e a coordenação nas *issues* da plataforma. |
| Memória de sessão (*memory bank*) | Arquivos que o agente lê no início e atualiza no fim de cada sessão para atravessar o corte de contexto. |
| Inspeção de contexto (`inspect-context`) | Comando proposto pela base de pesquisa (não existe no Maestro em `19823c2`) que mostraria, por ciclo, o que cada tarefa carrega, o que sobreviveria a uma compactação e o que não está ligado a nada. O exemplo traz uma versão de brinquedo. |
| Diátaxis | Arcabouço de documentação de Daniele Procida: tutorial, explicação, como-fazer e referência, nunca misturados na mesma página. |
| Carga cognitiva | Teoria de John Sweller: a memória de trabalho é limitada; uma ideia nova por vez, exemplo resolvido antes do exercício. |
| *Four-Component Instructional Design* (4C/ID) | Modelo de van Merriënboer: a tarefa inteira como fio condutor, com informação de apoio e treino de partes. |
