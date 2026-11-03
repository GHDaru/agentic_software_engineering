# Glossário

Consolidado dos glossários dos capítulos (429 termos). Gerado por `scripts/consolidar.py` — não edite à mão.

| Termo | Definição | Nasce em |
|---|---|---|
| "não encontrado na documentação lida" | Forma obrigatória de registrar uma célula sem fonte; proíbe ler ausência de evidência como lacuna de mercado. | apêndice D |
| A2A (Agent2Agent) | Protocolo de comunicação entre agentes; no Maestro, seus nomes entram no envelope de mensagem, sem adotar fio nem SDK. | 12-ferramentas-mcp-e-o-ecossistema |
| Ablação | Técnica de avaliação em que o mesmo caso roda contra o agente real e contra o agente menos uma instrução. Se o ablado falha onde o real passa, a instrução paga o contexto que custa; se os dois passam, ela é suspeita de redundância. | 07-papeis-e-skills |
| absorção fantasma | Ideia registrada como absorvida cujo destino não existe no disco. O `check-ecosystem.sh` do Maestro achou duas na primeira execução. | 12-ferramentas-mcp-e-o-ecossistema |
| Accountability | O dever de responder pelas consequências de um resultado. Diferente de capacidade: um agente pode raciocinar bem e não ter o que perder (axioma A2). | 02-o-problema-da-confianca |
| Accountable (A) | Na matriz RACI, a única pessoa que responde pelo resultado. Neste livro, sempre humano, e responsável pela política, pelos gates e pelos critérios, não por cada item. | 02-o-problema-da-confianca |
| aceitação na primeira passada | Fração de entregas aprovadas pela revisão independente sem reprovação. | 10-quality-gates-que-provam-fatos |
| achado | Defeito ou lição que não coube no ciclo em que apareceu; entra no índice de decisões como `achado-NNN-<slug>`, com status `aberta`, até uma linha posterior fechá-lo. | 14-a-organizacao-que-aprende |
| achado que morre em candidato | Anti-padrão 14 do Maestro: registrar "regra candidata" e nunca rodar a retrospectiva que a transformaria em regra. | 14-a-organizacao-que-aprende |
| ACP (Agent Client Protocol) | Protocolo entre um editor ou host e um agente de código; avaliado pelo Maestro como modo de harness. | 12-ferramentas-mcp-e-o-ecossistema |
| adaptador de rastro | Conversor do log de um harness específico para o rastro neutro; é onde mora a dependência de ferramenta. O pacote traz um mínimo para o Claude Code e um validador que reencena as fixtures como execuções reais. | apêndice B |
| ADR (architecture decision record) | Registro de decisão de arquitetura no formato de Nygard (contexto, decisão, consequências). Imutável: nunca fica desatualizado, só superado por um ADR novo. | 14-a-organizacao-que-aprende |
| Agent Client Protocol (ACP) | Protocolo aberto para a conversa entre editor e agente; no Maestro, um dos modos da porta de *harness*, com versão fixada. | 16-o-futuro-da-engenharia-agentica |
| Agent2Agent (A2A) | Protocolo aberto para conversa entre agentes; no Maestro, só os nomes de estado entram no envelope das mensagens. | 16-o-futuro-da-engenharia-agentica |
| Agente (perfil) | O par descrição ↔ arquivo executável de um papel (no Maestro, `.claude/agents/<nome>.md`), com escopo, ferramentas e contrato. Não tem identidade de execução; ocupa sessões. | 07-papeis-e-skills |
| agência excessiva (excessive agency) | Item LLM06 do OWASP Top 10 para aplicações com LLM: funcionalidade, permissão ou autonomia além do que a tarefa pede. | 12-ferramentas-mcp-e-o-ecossistema |
| alavanca de reversibilidade | Cada um desses mecanismos, lido pelo eixo em que age: cópia de segurança e exclusão lógica no custo de desfazer, homologação no raio, execução a seco nos dois. | 11-risco-reversibilidade-e-autonomia |
| alvo | O arquivo de instrução avaliado (agente, skill, prompt), nomeado por caminho no caso. | 15-validando-o-maestro |
| alvo ablado / ablação | O mesmo alvo sem a instrução que o eixo nomeia, com todo o resto igual; funciona como grupo de controle. O caso só vale se o ablado reprovar. Se a ablação remover mais de uma coisa (no caso 001 real do Maestro: a instrução **e** o plano da entrada), o vermelho não se atribui só à instrução. | 15-validando-o-maestro |
| ambiente congelado | Os campos que tornam um *run* refazível: *commit* do método, *commit* do cenário, modelo resolvido, versão do *harness* e *hashes*. | apêndice C |
| Amontoado (pile-up) | Documento denso: muitas siglas sem dicionário, tudo numa página, sem narrativa. Combatido pela regra "sigla nunca nasce nua". | 08-ddd-para-agentes |
| Apetite | O tempo que uma aposta merece, fixado antes de começar (Shape Up). O escopo varia dentro dele; quando o apetite acaba, corta-se escopo e o prazo não se estende. | 03-um-humano-muitos-agentes |
| aplicação escalonada | Entrada em vigor de uma lei em marcos datados diferentes por tipo de obrigação, como no art. 113 do Regulamento Europeu de Inteligência Artificial. | 16-o-futuro-da-engenharia-agentica |
| apodrecimento | Envelhecimento silencioso de um artefato que ninguém consome ou que não falha quando fica velho; continua parecendo válido. | 14-a-organizacao-que-aprende |
| aposentadoria com motivo | Retirar um caso que não discrimina deixando-o visível com `Retired-because:`; aposentar sem motivo equivale a apagar. | 15-validando-o-maestro |
| append-only mecânico | Garantia de que um registro só cresce imposta por mecanismo (modo de abertura verificado, gatilho no banco), e não por convenção. | 09-arquitetura-que-se-defende |
| aprendizado de laço duplo (double-loop learning) | Termo de Argyris e Schön: o laço simples corrige o erro; o duplo muda a regra que o produziu. Com agentes, só o duplo deixa memória. | 14-a-organizacao-que-aprende |
| aprovação vazia | Veredito "conforme" de uma execução que não fez nada: nada escrito, nada violado. Por isso cada veredito leva ao lado a coluna "tarefa resolvida". | apêndice B |
| Archify | Gerador de diagramas interativos a partir de JSON (raias, fases, nós, arestas); versão 3.2.0 na peça 07 do Maestro. | apêndice A |
| Armadilha do funil | Quando o humano é Accountable e também confere à mão cada saída de agente: recria o trabalho de fazer tudo sozinho, com uma etapa a mais de leitura, e vira o gargalo. | 02-o-problema-da-confianca |
| Arquivo de instrução | Arquivo que o *harness* lê no início de toda sessão (`CLAUDE.md`, `AGENTS.md`, regras de projeto). Custo fixo de contexto de todas as sessões. | 05-engenharia-de-contexto |
| Arquivo de proveniência | Registro (no Maestro, `UPSTREAM.md`) de onde veio cada peça vendorizada, em que versão, e se foi adaptada ou mantida igual. | 04-a-spec-como-partitura |
| Artefato condicional | Artefato do ciclo que só existe quando se aplica (`research.md`, `data-model.md`, `contracts/`, `checklist.md`, `ux-design.md`), mas que é sempre declarado no plano com um token como `ART:research=no` e o motivo. | 04-a-spec-como-partitura |
| artefato que congela | Anti-padrão 15: roadmap, índice ou mapa que para de ser atualizado e continua sendo lido como verdade. | 14-a-organizacao-que-aprende |
| ASEG-Bench | Benchmark de governança para engenharia de software com agentes: dez casos (GOV-001 a GOV-010), cada um com oráculo determinístico. Nome de trabalho da agenda de pesquisa; a expansão "governança para *Agentic Software Engineering*" é adotada por este apêndice, não fixada pela agenda. | apêndice B |
| Assimetria fazer × desfazer (A5) | Axioma do Maestro: produzir é barato e fica mais barato; desfazer (apagar, publicar, migrar, fazer deploy) não. | 01-a-mudanca-de-unidade-de-trabalho |
| atribuição que viaja | Licença e notas de terceiros que acompanham cada canal de redistribuição (instalador, plugin), renomeadas no destino para não afirmar que o projeto alheio inteiro tem aquela licença. | 12-ferramentas-mcp-e-o-ecossistema |
| Autor como revisor | Anti-padrão em que o agente (ou pessoa) que escreveu aprova o próprio trabalho. | 02-o-problema-da-confianca |
| autoteste | Execução do oráculo contra as próprias fixtures: prova que cada oráculo já foi visto reprovando (a "segunda lei" aplicada ao benchmark). | apêndice B |
| Avaliador-otimizador | Padrão de laço: gerar, criticar contra um critério, refinar até passar. | 06-como-dividir-o-trabalho |
| avaliação (eval) | Linha de base de julgamento: entrada fixa, asserções que discriminam (inclusive o lado negativo) e observação datada, presa ao alvo que mede. Não é teste (igualdade) nem benchmark (sistemas entre si). | 15-validando-o-maestro |
| axioma (no Maestro) | Verdade assumida sem prova, da qual o método deriva teoremas e regras; o Maestro tem cinco (A1–A5), em `docs/governance/axioms.md`. | 16-o-futuro-da-engenharia-agentica |
| Axioma / teorema / corolário | Na camada de derivação do Maestro: verdade assumida; regra derivada e demonstrável com evidência do repositório; consequência imediata que muda uma decisão. | 00-prefacio |
| Axioma, teorema, corolário | A camada de derivação do Maestro (`docs/governance/axioms.md`): cinco verdades assumidas (A1–A5), sete teoremas derivados delas com evidência no repositório (T1–T7) e treze corolários (C1–C13), de onde saem as regras do dia a dia. | apêndice A |
| ação administrativa (autoconcessão) | Ação que altera permissão, identidade ou política — inclusive a do próprio agente. Classe 6: bloqueada para agente. | 11-risco-reversibilidade-e-autonomia |
| Backward Design | Planejamento de trás para frente (Wiggins e McTighe): objetivos, depois verificação, só então conteúdo. | 15-validando-o-maestro |
| benchmark de capacidade | Conjunto de tarefas cujo veredito é "o agente resolveu?" (por exemplo, os testes da tarefa passam). SWE-bench e SWE-Bench Pro são exemplos. | apêndice B |
| benchmark de governança | Conjunto de tarefas cujo veredito é "o agente resolveu sem violar a regra do time?". Pressupõe capacidade e mede o custo de governança da solução. | apêndice B |
| Bloco gerado do disco | Trecho da instrução montado por script a partir do que existe (as skills), e não escrito à mão. | 05-engenharia-de-contexto |
| Bootstrap de enforcement | O parágrafo, na instrução que o agente lê primeiro, que manda consultar as skills antes de agir. No Maestro, gerado do disco pelo instalador e conferido por script. | 07-papeis-e-skills |
| Borda decidida × borda por descuido | A regra posta na borda com o motivo escrito (permitida) e a posta ali sem que ninguém decidisse (o defeito que o portão recusa). | 08-ddd-para-agentes |
| BPMN (Business Process Model and Notation) | Notação padrão de diagramas de processo; o Maestro desenha nela o próprio fluxo. | 14-a-organizacao-que-aprende |
| braço | Uma das condições comparadas pela agenda: A (prompt), B (spec), C (spec + portões) e T (Maestro completo). | apêndice C |
| Business Process Model and Notation (BPMN) | Notação padronizada pelo Object Management Group (OMG), versão 2.0.2, para desenhar processos com raias, tarefas, decisões e artefatos. | apêndice A |
| BYOK (bring your own key) | O usuário fornece a própria chave do provedor de modelo; no companion do Maestro, usada só na requisição e nunca persistida. | 12-ferramentas-mcp-e-o-ecossistema |
| Cadência de estudo | Profundidades de leitura com custo de tempo declarado: Entender (~20 min), Aprender (~2 h), Aplicar (~1 dia), Aprofundar (contínuo). | apêndice A |
| Caixa marcada sem testemunha | Item de checklist marcado como feito sem a evidência existir; no Maestro, a caixa da cauda de fechamento marcada antes da revisão. | 02-o-problema-da-confianca |
| Camada | Agrupamento dos elementos pela pergunta que respondem: fundamento (por quê), mecânica (como flui), estrutura (quem e quando), qualidade (o que se produz e como se prova), governança (como evolui). | apêndice A |
| Camada anticorrupção (anticorruption layer) | Adaptador que traduz o vocabulário de outro sistema para o seu, com um mapa escrito, para o termo estrangeiro não entrar no domínio quando o sentido não é 1:1. | 08-ddd-para-agentes |
| caminho compartilhado | Caminho possuído por um domínio e lido (ou publicado) por outro; declarado para que quem o edita saiba que a edição é pública. | 09-arquitetura-que-se-defende |
| canal de publicação | Cada via pela qual um arquivo chega ao leitor final (itens do sumário, materiais, anexos). Um portão de fronteira precisa ler todos. | 09-arquitetura-que-se-defende |
| canário | Cadeia única plantada numa instrução hostil (GOV-010); se aparece em ação ou escrita do agente, a instrução foi obedecida. | apêndice B |
| Capacidade de decisão | Quantas decisões por dia o humano consegue tomar com qualidade; o teto da vazão de um time de agentes. No exemplo do capítulo, 480 minutos ÷ 12 minutos por decisão = 40. | 03-um-humano-muitos-agentes |
| card de ideia | Registro imutável e datado de uma ideia vista numa fonte: o que é, o veredito daquele momento, o destino, o gatilho e as sete dimensões. | apêndice D |
| Carga cognitiva | Teoria de John Sweller: a memória de trabalho é limitada; uma ideia nova por vez, exemplo resolvido antes do exercício. | 05-engenharia-de-contexto |
| Carga de estado (SessionStart) | *Hook* de início de sessão que imprime fatos medidos agora (ciclo aberto, conformidade, achados); no Maestro dispara também após a compactação. "Carregado em vez de lembrado." | 05-engenharia-de-contexto |
| carimbo (rubber stamp) | Aprovação dada sem exame, por excesso de volume ou hábito; tem a aparência de controle e produz registro de uma decisão que ninguém tomou. | 11-risco-reversibilidade-e-autonomia |
| caso | Unidade do benchmark: eixo, hipótese, ablação, origem e sua classe, cenário, gatilho, comportamento esperado, oráculo, limite declarado, contrato de declaração e fixtures. | apêndice B |
| catálogo do ecossistema | Registro de avaliações de terceiros com a ideia como unidade, cartão datado e imutável por observação, e veredito corrente num índice append-only. | 12-ferramentas-mcp-e-o-ecossistema |
| Catálogo semântico | Linguagem ubíqua operacional: o lugar que se consulta antes de criar um nome ou um componente, com quatro saídas — REUSE, ALIAS, EXTEND, CREATE. | 08-ddd-para-agentes |
| Cauda de fechamento | As caixas `TAIL:review`, `TAIL:security`, `TAIL:mutation` e `TAIL:gate` no fim do `tasks.md` de um ciclo do Maestro, cada uma exigindo evidência escrita no relatório de qualidade. | 02-o-problema-da-confianca |
| cauda de fechamento (closing tail) | Os quatro passos finais de um ciclo no Maestro (`TAIL:review`, `TAIL:security`, `TAIL:mutation`, `TAIL:gate`), escritos como tokens no `tasks.md`, com evidência no `qa-report.md`. | 10-quality-gates-que-provam-fatos |
| cauda de fechamento (TAIL:) | Itens de fechamento do ciclo (revisão, segurança, mutação, gate) que precisam de evidência no relatório de qualidade. | 15-validando-o-maestro |
| Cauda do ciclo (closing tail) | Os passos de fechamento — revisão independente, segurança, mutação, gate humano — escritos no `tasks.md` como *tokens* `TAIL:` que um script procura. | 05-engenharia-de-contexto |
| cerca do dado | Marcas que delimitam o conteúdo de terceiros devolvido ao modelo, com teto de bytes, marca de corte e neutralização de marcas internas. Torna a fronteira visível; não é sandbox. | 12-ferramentas-mcp-e-o-ecossistema |
| Cerimônia por função | Critério para manter ou cortar uma cerimônia: perguntar que função ela cumpre no contexto de um humano com N agentes. Sem função, sem cerimônia. | 03-um-humano-muitos-agentes |
| cerimônia sem gatilho | Anti-padrão 17: cerimônia recorrente sem condição mensurável que a dispare; acontece quando alguém lembra, isto é, raramente. | 14-a-organizacao-que-aprende |
| Chamado (Hindiana) | Formato de outro projeto que usa o método: `00-chamado.md`, spec em EARS e um arquivo por veredito de portão (G0…G9). No Maestro, entra como evidência importada. | 04-a-spec-como-partitura |
| check negativo | Invariante escrito como busca pelo que não pode existir, com resultado esperado vazio. | 10-quality-gates-que-provam-fatos |
| CI (continuous integration) | Integração contínua: a execução automática de testes e portões a cada mudança enviada ao repositório. | 14-a-organizacao-que-aprende |
| Ciclo guarda-chuva | Ciclo que só coordena: abre ciclos filhos e registra as decisões, sem entregar código próprio. | 06-como-dividir-o-trabalho |
| citável, não copiável | Marca da fonte cuja licença permite ler e citar, mas não redistribuir (proprietária, comercial, sem licença declarada, não comercial). | apêndice D |
| CLAIM | Afirmação quantitativa ou factual do livro, com identificador `CLAIM-NN-NNN`, estado (medido, observado, hipótese) e evidência reproduzível registrada no `claims.md` do capítulo. | 00-prefacio |
| Clarify | Etapa e seção da spec em que a ambiguidade vira pergunta para o humano, em vez de requisito inventado. | 04-a-spec-como-partitura |
| classe da origem | *Observada* (um registro datado mostra uma falha da família do caso) ou *de risco* (origem em leitura de código ou referência externa, relatada em separado). | apêndice B |
| classe de risco | Degrau (0 a 6) de uma escada que decide quanta autonomia o agente tem numa ação e que gate humano ela recebe: leitura, leitura sensível, criação reversível, alteração, exclusão ou efeito externo, financeira ou irreversível, lote/entre inquilinos/administrativa. | 11-risco-reversibilidade-e-autonomia |
| Claude Code Project Manager (CCPM) | Ferramenta que põe a rastreabilidade e a coordenação nas *issues* da plataforma. | 05-engenharia-de-contexto |
| Colisão | Defeito do corte: arquivo com dois escritores, conceito com mais de um dono ou contrato consumido sem dono. | 06-como-dividir-o-trabalho |
| Colisão de endereço | O mesmo identificador apontando para dois destinos, ou para nenhum. Invariante do Maestro: endereço ambíguo é recusado, nunca resolvido. | 06-como-dividir-o-trabalho |
| Colisão de nomes | Uma palavra com dois sentidos em dois contextos ("fila" de decisões × fila de saída). Remédio: qualificar a palavra e separar os contextos. | 08-ddd-para-agentes |
| commit de referência | O *commit* `19823c2` do Maestro, contra o qual todo link e toda evidência do livro são lidos; rodar em outro *commit* mede outra coisa. | apêndice C |
| commit não publicado | *Commit* que existe só no clone do autor; enquanto não chega ao repositório público, a evidência ancorada nele só se confere na máquina de quem o escreveu. | apêndice C |
| Compactação | Compressão feita pelo *harness* quando a janela enche: ela escolhe o que fica, e o resto é apagado, não degradado (corolário C12). | 05-engenharia-de-contexto |
| Complexity Tracking | Registro, no plano, de uma violação de princípio inevitável: qual princípio, por que, o que a torna reversível. O portão humano decide. | 04-a-spec-como-partitura |
| Compressão | Operação que transforma o que já entrou em menos (plano como exploração destilada, resumo, compactação). | 05-engenharia-de-contexto |
| conferência com validade | Data em que um dado externo (como um calendário regulatório) foi comparado com a fonte oficial, mais o prazo depois do qual o dado não responde sem nova conferência. | 16-o-futuro-da-engenharia-agentica |
| conformidade | Primeira camada de validação: o método foi aplicado e sobreviveu nos artefatos? Responde-se com comando. | 15-validando-o-maestro |
| confronto | Etapa de uma pesquisa de mercado em que cada funcionalidade é cruzada com o estado do método e decidida como `ENTRA`, `NÃO PRECISA` ou `DEPOIS`, com fonte. | apêndice D |
| Constitution Check | Tabela, dentro do plano de um ciclo do Maestro, que confere o plano contra cada princípio da constituição do método antes de implementar; aprovar o plano com ela é um dos gates humanos. | 02-o-problema-da-confianca |
| consumo por agente | O grão mais fino do custo por sessão: tokens por agente, não só por sessão ou modelo. | 13-observabilidade-e-economia |
| context-slicer | Mecanismo do `maestro-02` que injeta só as seções relevantes do contexto e reporta a economia de tokens contra o contexto inteiro. | apêndice D |
| Contexto delimitado (bounded context) | Fronteira dentro da qual uma palavra tem um sentido só; é também a costura por onde o trabalho se corta para rodar em paralelo. | 08-ddd-para-agentes |
| Contexto fresco | Sessão de agente iniciada sem o histórico de quem executou: recebe o diff, a spec e o plano, e nada da conversa. | 02-o-problema-da-confianca |
| Contexto integrador | O que toda fatia de trabalho precisa carregar para que as fatias se encaixem: objetivo, invariantes e contratos — a spec (Princípio V). | 05-engenharia-de-contexto |
| Contexto tribal | Anti-padrão 2: intenção que só existe na cabeça do operador. | 05-engenharia-de-contexto |
| Contrato | O que uma fatia publica para as outras: função, formato, porta. Escrito antes de ser consumido. | 06-como-dividir-o-trabalho |
| contrato de declaração | Bloco de cada caso, anexado ao gatilho igual em todos os níveis, que diz o formato em que o agente registra o que fez (caminhos, linhas como `Aprovado por:`), nunca a regra medida. Existe para que o nível sem método não seja reprovado por desconhecer um formato. | apêndice B |
| Contrato do papel | A parte do perfil que diz o que o papel faz, o que não faz, o que consome, o que produz e a quem entrega. É o que distingue um papel de um prompt. | 07-papeis-e-skills |
| convenções semânticas GenAI | Nomes de atributos do OpenTelemetry para IA generativa (`gen_ai.request.model`, `gen_ai.usage.input_tokens`…), ainda em desenvolvimento. | 13-observabilidade-e-economia |
| Converge | Comando que compara o repositório real com spec, plano e tarefas e anexa tarefas para o que falta, sem reescrever as existentes. | 04-a-spec-como-partitura |
| corolário (no Maestro) | Regra do dia a dia derivada de um teorema ou axioma (C1–C13). | 16-o-futuro-da-engenharia-agentica |
| corolário C1 | Do Maestro: toda cerimônia tem gatilho, e o gatilho é mensurável. Deriva de T6. | 14-a-organizacao-que-aprende |
| corolário C9 | Do Maestro: documentação que nada consome apodrece, por melhor que seja. Deriva de T5. | 14-a-organizacao-que-aprende |
| Corte | Decisão humana de reduzir escopo ou realocar verificação para fechar uma versão; no Maestro, registrada com data e o que entra e sai. | 01-a-mudanca-de-unidade-de-trabalho |
| Corte por fronteira | Corte que dá a cada conceito um dono e a cada contrato um escritor; as fatias se tocam só por contratos declarados. | 06-como-dividir-o-trabalho |
| Corte por quantidade | Corte que reparte o trabalho por número de itens ou de arquivos, sem olhar o que eles compartilham. Produz colisões. | 06-como-dividir-o-trabalho |
| Crítica às cegas | Forma de revisão em que o juiz compara o resultado com uma referência externa sem saber qual é qual, e decide qual atende melhor à pergunta do usuário. | 02-o-problema-da-confianca |
| Crítico às cegas | Agente em contexto fresco que compara duas versões sem saber qual é a do time e aponta a melhor e a maior lacuna. | 01-a-mudanca-de-unidade-de-trabalho |
| crítico às cegas / gauntlet | Avaliador em contexto fresco que compara versões sem saber qual é qual; usado como barra de produto no ciclo 074. | 15-validando-o-maestro |
| custo de desfazer | Quanto custa voltar ao estado anterior a uma ação: nada, trivial (`git revert`), barato (desmarcar uma exclusão lógica), caro (restaurar de *backup*) ou impossível (segredo lido, e-mail enviado, dado apagado sem cópia). Um dos dois eixos da classe. | 11-risco-reversibilidade-e-autonomia |
| Custo fixo de contexto | O que um papel carrega para a janela a cada invocação: o próprio perfil, as skills que consome e o que a instrução do projeto importa por padrão. | 07-papeis-e-skills |
| Custo por mudança aceita | Soma esperada de gerar, verificar e desfazer, dividida pelas mudanças aceitas. Versão do capítulo para a métrica "custo por tarefa aceita" da agenda de pesquisa. | 01-a-mudanca-de-unidade-de-trabalho |
| custo por sessão | Contagem de tokens por sessão (e por minuto), lida dos transcritos de forma incremental; só contagens, nunca conteúdo. Mais grossa que o livro de ponto, mas não depende de etiqueta. | 13-observabilidade-e-economia |
| custo por tarefa aceita | Todo o custo de um período ou ciclo (tentativas entregues, bloqueadas, reprovadas e as revisões) dividido pelo número de tarefas cujo último veredito, dado por quem não as executou, é de aprovação. A unidade econômica proposta pelo capítulo. | 13-observabilidade-e-economia |
| custo por tarefa executada (ingênuo) | O mesmo custo dividido pelas tarefas executadas, aceitas ou não. Mede esforço, não resultado; fica abaixo do custo por tarefa aceita sempre que algo pago não é aprovado. | 13-observabilidade-e-economia |
| célula | A combinação de braço, cenário e modelo que recebe as repetições do protocolo. | apêndice C |
| cópia ao lado | Guardar a versão anterior de um arquivo junto dele (no Maestro, `.maestro-old` e `.maestro-new`) antes de sobrescrever ou para oferecer a versão nova sem sobrescrever. | 11-risco-reversibilidade-e-autonomia |
| cópia instalada | O método como chega ao repositório de destino, que pode diferir da fonte; é o que `check-installed.sh` exercita num diretório vazio. | apêndice C |
| declaração de artefato (ART:) | Token legível por máquina no plano que declara cada artefato condicional como `yes` ou `no` com motivo. | 15-validando-o-maestro |
| decoração | Portão que fica verde em pelo menos um mundo quebrado de propósito, ou vermelho num mundo certo: tem a forma de verificação sem proteger nada. | 10-quality-gates-que-provam-fatos |
| Definition of Done (DoD) | Definição de pronto: o conjunto de verificações executáveis (testes, portões, build) que um ciclo tem de passar para ser dado como feito. | 02-o-problema-da-confianca |
| Definition of Ready (DoR) | Portão humano antes da execução: critérios testáveis, ambiguidades resolvidas ou registradas, Constitution Check aprovado, `ux-design.md` se toca tela, apetite definido. A spec está pronta quando o agente executa sem adivinhar. | 04-a-spec-como-partitura |
| delegação de política (gate por delegação) | Gate humano decidido por uma sessão que não executou o trabalho, com delegação escrita e revogável do humano, crítico independente em contexto fresco e uma linha de registro por gate (ADR 0026 do Maestro). O humano responde pela política, não por cada visto. | 11-risco-reversibilidade-e-autonomia |
| Delta (modelo) | Descrever a mudança pelo que muda em relação ao comportamento atual, e não por uma spec inteira. Origem: OpenSpec; no Maestro virou a raia leve. | 04-a-spec-como-partitura |
| Deriva | Divergência silenciosa entre um documento escrito à mão e o fato que ele descreve (o disco, outra cópia). | 05-engenharia-de-contexto |
| Desculpa fechada | Racionalização listada e recusada explicitamente numa lei de ferro ("isto NÃO é desculpa: …"), para que o agente não a use. | 07-papeis-e-skills |
| Desejo | Critério que não se prova nem se refuta ("deve ser rápido"). Não entra como requisito. | 04-a-spec-como-partitura |
| Despejo de contexto (context dump) | Anti-padrão 1: colar a base inteira no *prompt*. | 05-engenharia-de-contexto |
| Digital Omnibus on AI | Nome do Regulamento (UE) 2026/1744, que alterou o *AI Act* (datas do alto risco, proibições novas, transições). | 16-o-futuro-da-engenharia-agentica |
| dimensão que reprova sozinha | Critério de avaliação que decide sem compensação por outros: conflito insanável com princípio e licença incompatível. | apêndice D |
| Divergência declarada | Regra de vendorização: quando uma peça vendorizada contradiz o método, a contradição é resolvida por spec e registrada; nunca fica silenciosa. | 04-a-spec-como-partitura |
| Diátaxis | Arcabouço de documentação de Daniele Procida: tutorial, explicação, como-fazer e referência, nunca misturados na mesma página. | 05-engenharia-de-contexto |
| DoD (Definition of Done) | Definição de pronto: critérios verificáveis que um trabalho cumpre antes de ser dado como concluído. | 14-a-organizacao-que-aprende |
| Domain-Driven Design (DDD) | Projeto dirigido pelo domínio (Evans, 2003): desenhar o software a partir do modelo do negócio e da língua que o negócio fala. | 08-ddd-para-agentes |
| domínio (de repositório) | No sentido do capítulo, uma das metades do repositório definidas pelo leitor: o que é lido por máquina (toolkit) e o que é lido por gente (guia). Não confundir com o domínio do DDD. | 09-arquitetura-que-se-defende |
| Dono do conceito | A única fatia que calcula ou define um conceito; as outras o consomem pelo contrato, sem recalcular. | 06-como-dividir-o-trabalho |
| dívida de retro | Número de achados abertos e idade do mais velho; quando passa do limite (quatro abertos ou seis ciclos, no Maestro), a retrospectiva é obrigatória. | 14-a-organizacao-que-aprende |
| Easy Approach to Requirements Syntax (EARS) | Conjunto de moldes de frase para requisito (ubíquo, por evento, por estado, indesejado, opcional), cada um com condição e comportamento observáveis. Em português: QUANDO ‹condição›, O SISTEMA DEVE ‹comportamento›. Mavin et al., 2009. | 04-a-spec-como-partitura |
| Economia de contexto | 1 − (o que a tarefa carrega ÷ o que o repositório tem). Economia consistentemente baixa é sinal de corte errado, não de janela pequena. | 05-engenharia-de-contexto |
| efeito | Terceira camada: aplicar o método produz resultado melhor do que não aplicá-lo? Só se responde com experimento comparativo. | 15-validando-o-maestro |
| eixo | A capacidade de governança que o caso afirma separar. | apêndice B |
| eixo (Axis) | A capacidade que o caso diz separar; é a linha que se remove para produzir o alvo ablado. | 15-validando-o-maestro |
| Elemento [n] | Uma das 12 peças do modelo operacional do Maestro, rotuladas `[1]`–`[12]`; o rótulo não coincide com o número do capítulo do handbook que a trata. | apêndice A |
| Elo por convenção | Ligação entre artefatos mantida por um formato combinado (o commit cita o ciclo); vive de hábito até um portão cobrá-la. | 05-engenharia-de-contexto |
| Encadeamento | Padrão de passos fixos em sequência, cada um consumindo a saída do anterior. | 06-como-dividir-o-trabalho |
| Endereço de sessão | A identidade de uma sessão de agente escrita em três partes, `nome · ref · projeto`. O nome se repete; a ref distingue homônimos e expira quando a sessão reinicia. Endereço ambíguo é recusado, nunca adivinhado. | 03-um-humano-muitos-agentes |
| enforcement (imposição) | Mecanismo que o agente não pode pular porque não passa por ele: permissão do harness, hook que recusa, portão da CI. Contrasta com instrução, que vale enquanto for seguida. | 12-ferramentas-mcp-e-o-ecossistema |
| Engenharia de contexto | Decidir, como prática de engenharia e não de *prompt*, o que um agente lê, o que descarta e o que tem de sobreviver fora dele. Quatro operações: seleção, compressão, persistência e transferência. | 05-engenharia-de-contexto |
| escape de gate | Defeito achado depois do merge com o portão verde no momento do merge; métrica de saúde dos portões. | 10-quality-gates-que-provam-fatos |
| escape declarado | Saída legítima e documentada de um gate (no Maestro, o `--yes` do script de promoção) usada quando o humano já decidiu; evita que o gate seja contornado por fora, sem registro. | 11-risco-reversibilidade-e-autonomia |
| escolha de agente declarada | O instalador recebe o agente-alvo (`--ai`) de uma tabela, grava a escolha e recusa id desconhecido, em vez de supor um harness. | 12-ferramentas-mcp-e-o-ecossistema |
| Espectro fluxo ↔ agente | Eixo entre o caminho fixado por você (*workflow*) e o caminho decidido pelo modelo na hora (*agent*). | 06-como-dividir-o-trabalho |
| Espera humana | O intervalo entre um pedido de decisão ficar pronto e a decisão ser registrada. Métrica do gargalo; só existe como dado se pedido e resposta tiverem carimbo de tempo. | 03-um-humano-muitos-agentes |
| Estado derivado | Estado calculado a partir de arquivos ou de eventos com carimbo, sob regras fixas, em vez de digitado por quem trabalha. O oposto do "Estado atual" que cada agente escrevia e que envelhecia em horas. | 03-um-humano-muitos-agentes |
| estado do claim | Quanto a afirmação aguenta: `medido` (um comando produz o número), `observado` (um arquivo ou *commit* registra o fato), `observado (autodeclarado)` (balanço escrito pelo autor) ou `hipótese`. | apêndice C |
| estudo com a mão no código | Estudo de campo sobre o repositório real, numa versão ou commit fixado, lido arquivo por arquivo; acha o mecanismo que a varredura não vê. | apêndice D |
| estudo de campo | Avaliação datada de trabalho de terceiros (ferramenta, framework, plataforma) feita para decidir o que atravessa a fronteira do método; tem pergunta, versão observada, vereditos e destino. | apêndice D |
| etiqueta [[TASK]] / [[DONE]] | Linha sozinha numa mensagem com que quem distribui abre uma tarefa e quem entrega a fecha; é o contrato entre a sessão gerente e as trabalhadoras. | 13-observabilidade-e-economia |
| exclusão lógica (soft delete) | Marcar como apagado em vez de apagar; desfazer é desmarcar. | 11-risco-reversibilidade-e-autonomia |
| execução a seco (dry run) | Executar a ação sem efeito, só mostrando o que faria; a ação ensaiada é leitura. | 11-risco-reversibilidade-e-autonomia |
| Execução contínua | Regra de o agente executar o plano até um bloqueio, uma ambiguidade real ou o fim, sem pedir licença a cada passo; a atenção humana se gasta em gates, não em acompanhar progresso. | 03-um-humano-muitos-agentes |
| Faixa de modelo | A classe de modelo (por exemplo pequeno, médio, grande) em que um papel roda, declarada no perfil com motivo e gatilho de revisão. Recomendação deste livro; ausente no Maestro na versão citada. | 07-papeis-e-skills |
| falhar aberto (fail open) | Comportamento de um guarda que, ao quebrar, deixa passar em vez de bloquear. O guarda do Maestro faz isso de propósito e delega a detecção ao portão. | 12-ferramentas-mcp-e-o-ecossistema |
| falso vermelho | Reprovação de um mundo certo. Repetido, ensina o time a ignorar o portão. | 10-quality-gates-que-provam-fatos |
| família (de um portão) | Conjunto de formatos, atributos, canais ou campos que um portão precisa cobrir para cobrir algum (corolário C5; anti-padrões 16 e 23). | 10-quality-gates-que-provam-fatos |
| Família que nunca se escreve nua | Palavra com mais de um sentido no domínio que só aparece qualificada ("prazo de resposta", nunca "prazo"); a lista mora no modelo, que um *lint* lê. | 08-ddd-para-agentes |
| Fatia | Parte de um trabalho entregue a um agente (ou a uma sessão) para ser feita sem olhar as outras. | 06-como-dividir-o-trabalho |
| Fatia vertical | Fatia que atravessa da interface ao dado e entrega valor sozinha. Regra entre entregas, não entre agentes dentro de um ciclo. | 06-como-dividir-o-trabalho |
| fecha (campo) | Campo estrutural de uma linha do índice de decisões que aponta o id do achado que ela fecha. O portão lê o campo, nunca a prosa. | 14-a-organizacao-que-aprende |
| fiação | A ligação entre o mecanismo e quem o chama (o `settings.json` que aponta para o hook). Provar o script sem provar a fiação é decoração. | 12-ferramentas-mcp-e-o-ecossistema |
| Fila de decisões | Lista dos pedidos de decisão abertos, ordenada por prazo, derivada de um registro só-acréscimo. Não tem "dispensar": um pedido sai só com ruling ou devolução. | 03-um-humano-muitos-agentes |
| fitness function (de arquitetura) | Verificação objetiva e executável de uma característica de arquitetura, rodada de forma contínua (em geral na integração contínua). Termo de Ford, Parsons e Kua. | 09-arquitetura-que-se-defende |
| fixture | Entrada fixa do caso; deve trazer fatos e nenhuma conclusão que o alvo deveria tirar. | 15-validando-o-maestro |
| fixture legítima | Entrada que representa o mundo certo de forma incômoda (a palavra proibida no meio de uma frase verdadeira, duas fontes numa linha); o portão tem de passar, senão é falso vermelho. | 10-quality-gates-que-provam-fatos |
| fixture negativa | Rastro que encena a violação da família do caso (observada ou de risco, conforme a classe da origem); o oráculo tem de reprová-lo, inteiro e só pelo estado. Carrega fatos, nunca o veredito. | apêndice B |
| fixture negativa (mutação) | Entrada que representa o mundo quebrado de propósito; o portão tem de reprovar. Mutação que passa "sobreviveu". | 10-quality-gates-que-provam-fatos |
| fixture positiva | Entrada que representa o mundo certo; o portão tem de passar. | 10-quality-gates-que-provam-fatos |
| Fonte única (da instrução) | Uma instrução só; outros nomes que a ferramenta lê são link simbólico ou cópia gerada, conferida por igualdade de conteúdo (ADR 0013 do Maestro). | 05-engenharia-de-contexto |
| Four-Component Instructional Design (4C/ID) | Modelo de van Merriënboer: a tarefa inteira como fio condutor, com informação de apoio e treino de partes. | 05-engenharia-de-contexto |
| FR (FR1, FR2) | Requisito funcional (*functional requirement*), numerado na spec. | 15-validando-o-maestro |
| Frase-chave | A frase de abertura da tela do regente ("você tem N decisões esperando, a mais antiga há X"), derivada da fila e nunca digitada; o contador baixa quando um ruling é registrado. | 03-um-humano-muitos-agentes |
| fronteira decidível | Fronteira em que uma máquina responde, para qualquer arquivo, a qual domínio ele pertence, sem julgamento: nenhum órfão, nenhuma dupla reivindicação, empate tratado como erro. | 09-arquitetura-que-se-defende |
| fronteira interna | Separação entre domínios declarada e verificada dentro de um único repositório, em vez de repositórios separados (ADR 0018 do Maestro). | 09-arquitetura-que-se-defende |
| funil de avaliação | Sequência varredura → gatilho → estudo com a mão no código → absorção por portão humano; cada etapa custa mais e só se passa adiante com motivo escrito. | apêndice D |
| função de força (forcing function) | Mecanismo que faz a regra ser cumprida sem depender de lembrança: um portão que falha, um hook que recusa. | 14-a-organizacao-que-aprende |
| gate ex-ante / registro ex-post | O gate barra antes de executar; o registro descreve depois. Para ação irreversível, só o primeiro impede o dano. | 11-risco-reversibilidade-e-autonomia |
| Gate humano | Ponto do fluxo em que um humano decide, com nome e registro, se o trabalho avança (spec, plano, merge, deploy ou migração). | 02-o-problema-da-confianca |
| Gate por delegação de política | Gate humano decidido por um agente regente que não executou o trabalho, sob delegação escrita e revogável do humano, depois do parecer de um crítico em contexto fresco (ADR 0026 do Maestro). | 02-o-problema-da-confianca |
| gate uniforme | O mesmo rito de aprovação para toda ação. Falha de dois jeitos simétricos: pesado, vira funil e carimbo; leve, deixa o irreversível passar. | 11-risco-reversibilidade-e-autonomia |
| gatilho | O pedido entregue ao agente, nas palavras de um humano, em geral com a pressão que levou à violação original. | apêndice B |
| Gatilho (de skill) | O trecho da `description` de uma skill que diz quando ela se aplica ("Use quando…"); é o que o harness lê para decidir carregá-la. | 07-papeis-e-skills |
| gatilho de evento / de relógio | De evento: dispara quando algo observável acontece (um pedido, um conflito, uma medida). De relógio: dispara numa data; certo quando quem publica a data é externo. | 16-o-futuro-da-engenharia-agentica |
| gatilho de reabertura | Condição observável, escrita na decisão, que manda reavaliá-la (por exemplo, "mais de 30 rotas"); substitui a data de revisão e a decisão eterna. | 09-arquitetura-que-se-defende |
| Gatilho de reavaliação | Condição observável escrita junto de uma decisão adiada ("observar"), que diz quando a decisão deve ser revista. | 06-como-dividir-o-trabalho |
| Gauntlet | Laço construtor × crítico às cegas contra uma barra, repetido até a versão do time vencer. | 01-a-mudanca-de-unidade-de-trabalho |
| Gerar / verificar / desfazer | Os três termos de custo de uma mudança: produzi-la; estabelecer que ela faz o que devia, inclusive a intenção; e reverter o erro que escapou. | 01-a-mudanca-de-unidade-de-trabalho |
| Gerente / Worker | No Maestro, a sessão que distribui e integra (Gerente) e as sessões que executam fatias, cada uma na sua worktree (Workers). | 06-como-dividir-o-trabalho |
| Glossário gerado | Glossário produzido a partir do modelo de domínio, com o carimbo do modelo; a integração contínua regera da fonte e recusa divergência. | 08-ddd-para-agentes |
| Governança operacional | A camada de regras, papéis, artefatos, portões, registros de decisão e automações que decide o que um agente pode fazer, quem verifica e quem aprova. Roda sobre qualquer *harness* e modelo. | 00-prefacio |
| guarda (hook) | Verificação que roda **antes** da ação e a recusa; o portão, ao contrário, audita depois. | 14-a-organizacao-que-aprende |
| Handoff | A passagem de trabalho de um papel ao seguinte, feita por artefato (spec, plano, diff, veredito), e não por conversa. | 07-papeis-e-skills |
| Harness | O programa que executa o agente: dá a ele ferramentas, contexto e permissões (um agente de linha de comando, um SDK, um orquestrador). O livro é independente dele. | 00-prefacio |
| hash (SHA-256) | Impressão digital de um arquivo calculada pelo Secure Hash Algorithm de 256 bits: mudou um byte, mudou o *hash*; congela a entrada de um *run*. | apêndice C |
| Hook | Comando que o *harness* executa em um ponto fixo do ciclo do agente (por exemplo, antes de cada chamada de ferramenta) e que pode recusar a ação. | 00-prefacio |
| hook (PreToolUse, SessionStart, Stop) | Gancho do harness executado em um evento da sessão; o `PreToolUse` roda antes de uma ferramenta e pode recusar a chamada. É mecanismo de um harness específico. | 12-ferramentas-mcp-e-o-ecossistema |
| Human-in-the-loop | Arranjo em que um humano confere ou aprova cada saída de um sistema automatizado. Aqui se distingue o humano em cada item (rejeitado como regra geral) do humano nos gates. | 02-o-problema-da-confianca |
| identidade pelo token | Regra de desenho: o autor de uma chamada vem da credencial do processo, nunca de um argumento que o modelo escreve. | 12-ferramentas-mcp-e-o-ecossistema |
| Iniciativa mista | Princípio de Horvitz para interfaces com agentes: humano e máquina alternam a iniciativa, e o humano entra no ponto de decisão das ações consequentes, não em cada passo. | 02-o-problema-da-confianca |
| injeção de prompt indireta | Instrução plantada em conteúdo que o modelo apenas lê (issue, página, resultado de ferramenta) e que ele pode obedecer como se viesse do operador. Item LLM01 do OWASP. | 12-ferramentas-mcp-e-o-ecossistema |
| Inspeção de contexto (inspect-context) | Comando proposto pela base de pesquisa (não existe no Maestro em `19823c2`) que mostraria, por ciclo, o que cada tarefa carrega, o que sobreviveria a uma compactação e o que não está ligado a nada. O exemplo traz uma versão de brinquedo. | 05-engenharia-de-contexto |
| instalador | `scripts/install-maestro.sh`: escreve o método em outro repositório sem sobrescrever o que o usuário alterou (`*.maestro-new`, `*.maestro-old`). | apêndice C |
| Instrução × enforcement | Instrução é o que se pede ao agente em texto; enforcement é o mecanismo (*hook*, script, permissão) que recusa a ação errada independentemente de o agente ter lido o pedido. | 00-prefacio |
| Invariante | Regra de negócio que precisa valer sempre. Mora no domínio (agregado, objeto de valor, serviço de domínio) ou, por exceção com motivo escrito, na borda (rota, adaptador, tela). | 08-ddd-para-agentes |
| INVEST | *Independent, Negotiable, Valuable, Estimable, Small, Testable*: os atributos de uma boa história de usuário. | 06-como-dividir-o-trabalho |
| Janela de contexto | O texto que o modelo lê de uma vez: instrução, conversa, arquivos, saídas de ferramenta. É finita e o desempenho cai à medida que ela enche (axioma A3). | 05-engenharia-de-contexto |
| jornada viva | Documento de jornada de tela com capturas geradas do build real por script versionado e heurística datada, no mesmo pull request. | 10-quality-gates-que-provam-fatos |
| JSON-RPC (JSON Remote Procedure Call) | Formato de chamada remota em JSON (*JavaScript Object Notation*): cada mensagem tem `method`, `params` e `id`; a resposta traz `result` ou `error`. | 12-ferramentas-mcp-e-o-ecossistema |
| JSONL (JSON Lines) | Formato de arquivo com um objeto JSON (*JavaScript Object Notation*) por linha. | 14-a-organizacao-que-aprende |
| Juiz com caneta | Papel que julga e também tem permissão de escrita; viola o corolário C3, porque o revisor que conserta vira coautor. | 02-o-problema-da-confianca |
| lado negativo (MUST-NOT-CLAIM) | Asserção sobre o que uma resposta errada, porém plausível, afirmaria; é o que impede uma resposta prolixa de passar. | 15-validando-o-maestro |
| Lei de ferro (Iron Law) | Regra inegociável que abre uma skill, em bloco de código, com a fórmula "violar a letra é violar o espírito" e as desculpas fechadas. Estreita: uma por skill. | 07-papeis-e-skills |
| Lei de Little | Num sistema estável, itens em curso = taxa de chegada × tempo no sistema (Little, 1961). Para a mesma vazão, mais itens em curso significam mais espera. | 03-um-humano-muitos-agentes |
| letramento em IA (AI literacy) | Obrigação do art. 4 do *AI Act*: desde o Regulamento (UE) 2026/1744, fornecedores e quem implanta sistemas de IA tomam medidas que apoiem o letramento da equipe, sem garantir nível individual. | 16-o-futuro-da-engenharia-agentica |
| limite de orçamento · emissor do aviso | Teto de consumo declarado de uma sessão ou projeto, lido como "declarar e avisar"; o emissor é quem compara o consumo medido com o limiar e enfileira o aviso. O corte (recusar, suspender) é decisão separada. | 13-observabilidade-e-economia |
| Linguagem ubíqua (ubiquitous language) | Vocabulário único de um contexto delimitado, acordado entre quem pede e quem constrói, usado literalmente no código, nos testes e na conversa. Para agentes, precisa ser um artefato que alguma máquina lê. | 08-ddd-para-agentes |
| linha de base (baseline) | Registro datado de uma execução do caso contra o alvo, com o commit do alvo, o veredito, a ablação e a premissa conferida. Envelhece quando o alvo muda. | 15-validando-o-maestro |
| Linha de base (de skill) | Registro de um cenário de pressão em que o agente falha sem a skill (vermelho) e cumpre com ela (verde), exigido antes de publicar uma skill original. | 07-papeis-e-skills |
| linha de base registrada | Critério para saída não comparável por igualdade (teorema T7): entrada fixa, asserções que discriminam (incluindo o que uma resposta errada afirmaria) e observação datada. | 10-quality-gates-que-provam-fatos |
| Livro de ponto | Registro só-acréscimo de eventos de tarefa (atribuída, iniciada, encerrada, custo). | 05-engenharia-de-contexto |
| livro de ponto de tarefas (task ledger) | Registro só-acréscimo, um evento por linha, de atribuição, início, fim (com tokens e custo) e veredito de cada tarefa. No Maestro, `docs/records/tarefas.jsonl`. | 13-observabilidade-e-economia |
| LLM-as-judge | Padrão em que um modelo de linguagem de grande porte (LLM, de *large language model*) avalia a saída de outro modelo. | 15-validando-o-maestro |
| lock-in | Dependência de um fornecedor que torna cara a saída; mede-se na dimensão de reversibilidade do cartão. | 16-o-futuro-da-engenharia-agentica |
| Losango (gate) | Ponto do desenho em que o fluxo para até uma decisão: humano (ouro, indelegável) ou mecânico (verde, a DoD). | apêndice A |
| MADR (Markdown Architectural Decision Records) | Variante de ADR em Markdown com campos para as alternativas consideradas. | 14-a-organizacao-que-aprende |
| Maestro | Método de engenharia de software em que um humano rege vários agentes de IA: a spec é a fonte de verdade, os agentes executam, o humano decide, aprova e verifica. Objeto de estudo deste livro. | apêndice A |
| manifesto de instalação | Registro, com hash, de cada arquivo que o instalador escreveu; permite distinguir versão antiga (renovar) de arquivo modificado pelo projeto (manter). | 12-ferramentas-mcp-e-o-ecossistema |
| manifesto por hash | Registro, gravado pelo instalador, do hash de cada arquivo que ele escreveu; permite distinguir versão velha (inalterada, pode atualizar) de arquivo editado pelo projeto (mantido). | 11-risco-reversibilidade-e-autonomia |
| Map-reduce cognitivo | Leitura do trabalho com agentes como *map* (as fatias, em paralelo) e *reduce* (a junção). O *reduce* não é concatenação: é julgamento com contexto global. | 06-como-dividir-o-trabalho |
| mapa da fragilidade | Leitura deste livro (hipótese) que cruza teoremas e axiomas para dizer quais regras dependem só da ferramenta. | 16-o-futuro-da-engenharia-agentica |
| Matriz RACI | Responsible, Accountable, Consulted, Informed: quem executa, quem responde, quem é consultado, quem é informado, por tarefa. | 02-o-problema-da-confianca |
| MCP (Model Context Protocol) | Protocolo aberto pelo qual um cliente (o harness do agente) descobre e chama capacidades de um servidor: ferramentas, recursos e prompts, em mensagens JSON-RPC 2.0 por stdio ou HTTP. Padroniza o encanamento; não decide permissão nem confiança. | 12-ferramentas-mcp-e-o-ecossistema |
| Medido / observado / hipótese | Estados de um claim: um comando reconta; um artefato registra e se confere lendo; o livro acredita e ainda não demonstrou. | 00-prefacio |
| Medir a frase em vez do fato | Defeito de verificação em que se confere o texto de uma afirmação, não o estado do disco que ela descreve. | apêndice A |
| Memory Bank | Padrão de memória de sessão em arquivos markdown estruturados que o agente relê a cada sessão, com um arquivo curto de contexto ativo. | apêndice D |
| Memória de sessão (memory bank) | Arquivos que o agente lê no início e atualiza no fim de cada sessão para atravessar o corte de contexto. | 05-engenharia-de-contexto |
| memória só-anexar (append-only) | Registro em que nada se reescreve: corrigir é acrescentar uma linha ou um ADR que supera o anterior. | 14-a-organizacao-que-aprende |
| Meta-agente | Agente cujo trabalho é construir ou evoluir o próprio método: projetar papéis, escrever skills, curar pesquisa, revisar a didática. | 07-papeis-e-skills |
| minimização | Princípio de coletar só o necessário: a telemetria do pacote guarda contagens e rastros revisados, não o log bruto que descreve a máquina. | apêndice C |
| minimização (lista de permissão) | Só sai do registro, ou da exportação, o que está explicitamente permitido; texto livre, conteúdo de mensagem e identificadores de sessão ficam para trás. Aplicação do princípio da necessidade da LGPD. | 13-observabilidade-e-economia |
| Modelo de domínio declarado | As quatro decisões que um plano torna explícitas, cada uma com motivo: raiz de agregado, onde moram as invariantes, mudanças de linguagem ubíqua, portas e adaptadores (`DOM:aggregate`, `DOM:invariants`, `DOM:glossary`, `DOM:ports`). Silêncio não é decisão. | 08-ddd-para-agentes |
| modelo de IA de uso geral (general-purpose AI model, GPAI) | No *AI Act*, modelo treinado para servir a muitas tarefas e ser integrado por terceiros; o fornecedor tem os deveres dos arts. 53 e 55. | 16-o-futuro-da-engenharia-agentica |
| modelonaoverificado | Marca de um *run* cujo *harness* não relatou o modelo resolvido, só o apelido pedido; o *run* entra na análise com a marca. | apêndice C |
| Modo de trabalho | Papel entendido como forma de trabalhar (decidir, executar, verificar), exercida por humano, agente ou ambos com um gate, e não como cargo. | 07-papeis-e-skills |
| momento × estado | Separação entre o que se julgou num dia (card) e o que vale hoje (índice); misturar os dois obriga a reescrever a história ou a mentir sobre o presente. | apêndice D |
| morte silenciosa | Portão que termina sem medir e é lido como verde — por exemplo, `grep -q` no fim de um pipe sob `pipefail` (anti-padrão 21). | 10-quality-gates-que-provam-fatos |
| Mudança aceita | Alteração que alguém especificou, um mecanismo independente verificou e um humano (ou política escrita por um humano) aceitou integrar. A unidade de trabalho deste livro. | 01-a-mudanca-de-unidade-de-trabalho |
| Mudança de escopo silenciosa | Anti-padrão em que o agente "aproveita" para fazer o que a spec não pediu. Trabalho novo vira pergunta ou registro, não tarefa escondida. | 04-a-spec-como-partitura |
| MUST-FIND / MUST-NOT-CLAIM | No corpus de avaliação do Maestro, o que uma resposta certa tem de achar e o que uma resposta errada diria. Origem do par positiva/negativa do ASEG-Bench. | apêndice B |
| mutante | Versão deliberadamente estragada de um código (GOV-005) ou de uma saída (GOV-006) que um teste ou gate correto tem de rejeitar. | apêndice B |
| Norma × executável | O par formado pelo documento que prescreve um papel ou artefato e pelo arquivo que o entrega. O defeito típico mora na distância entre os dois. | 07-papeis-e-skills |
| não medido | Tentativa cujo fim não traz tokens nem custo. É contada à parte; não vale zero. | 13-observabilidade-e-economia |
| níveis A, B, C e tratamento | Desenho de comparação da agenda: A só prompt, B com spec, C com spec e gates, tratamento com o método completo. | apêndice B |
| Onda | Grupo de fatias que podem correr ao mesmo tempo porque nenhuma consome contrato de outra do mesmo grupo. A ordem das ondas sai dos contratos. | 06-como-dividir-o-trabalho |
| operador do experimento | O humano que conduz a execução e dá as aprovações, com o protocolo `APROVO <alvo>`, igual em todos os níveis. | apêndice B |
| Orquestrador-trabalhadores | Padrão em que um orquestrador corta o trabalho na hora e junta as respostas. | 06-como-dividir-o-trabalho |
| oráculo | Função determinística que julga o rastro de uma execução e devolve a lista de violações (vazia = conforme). Roda sem modelo no laço. | apêndice B |
| Orçamento de contexto | A janela vista como recurso que se gasta: toda prática de trabalho com agentes é uma decisão de gasto. "Contexto é orçamento, não depósito." | 05-engenharia-de-contexto |
| ossificação | Modo de falha de quem só aprende: regras acumulam porque adicionar é barato e remover é caro, até ninguém saber quais estão vivas. | 14-a-organizacao-que-aprende |
| Outbox | Fila local (SQLite em modo WAL) por onde sessões da mesma máquina trocam mensagens sem servidor de mensageria. | 06-como-dividir-o-trabalho |
| Overhead de coordenação | Fração do tempo (ou dos tokens) de um trabalho paralelo gasta em passagens e reconciliação, e não em produzir as fatias. | 06-como-dividir-o-trabalho |
| pacote de replicação | O conjunto que permite a alguém de fora reproduzir ou refutar as afirmações do livro: método instalável, versão congelada, hipóteses e protocolo, dados dos *runs* e claims com evidência. | apêndice C |
| Painel de coordenação | Servidor local que projeta o estado de um time a partir dos arquivos do método; o banco é projeção reconstruível, a única escrita direta é uma tabela de eventos só-acréscimo, e o painel nunca promove. | 03-um-humano-muitos-agentes |
| Painel de regência | A vista do painel feita para o humano que rege: quadro por gate e fila de decisões. Lê e registra; não decide. | 03-um-humano-muitos-agentes |
| panorama (triagem) | Varredura larga que só classifica cada item como candidato a estudo com gatilho, observar ou fora do problema, sem repetir veredito já dado. | apêndice D |
| Papel de ocasião | Especialista convocado para uma decisão (por exemplo, uma banca em contexto fresco), consultado e descartado, sem perfil permanente. | 07-papeis-e-skills |
| Papel semântico | O que um objeto de tela **é** (ação primária, confirmação irreversível, ausência declarada), decidido antes do componente; a anatomia obrigatória deriva do papel. | 08-ddd-para-agentes |
| Papel órfão | Perfil executável que entrega um papel que a norma não prescreve; o espelho do papel prescrito sem executável. | 07-papeis-e-skills |
| par (comando, esperado) | Forma de critério estrutural: o comando e o resultado que prova o critério (`vazio`, `= N`, `exit 0`). | 10-quality-gates-que-provam-fatos |
| Par comando → esperado | Forma de critério para estrutura ou invariante: um comando e o resultado que prova o critério (saída vazia, contagem, código de saída). | 04-a-spec-como-partitura |
| Paralelizar dentro, não entre | Abrir trabalho paralelo só dentro de uma feature cuja spec e plano já foram aprovados; entre features ambíguas, cada frente multiplica os gates que passam pela mesma pessoa. | 03-um-humano-muitos-agentes |
| Paralelização | Padrão de fatias independentes (ou várias tentativas da mesma tarefa) executadas ao mesmo tempo. | 06-como-dividir-o-trabalho |
| Parecer | O veredito escrito de uma revisão independente (aprovar, aprovar com condições, reprovar), com os achados que o sustentam. | 02-o-problema-da-confianca |
| Passagem (handoff) | Cada vez que uma fatia depende de algo produzido por outra. Custa tempo e contexto. | 06-como-dividir-o-trabalho |
| Passo zero | A escolha da raia de trabalho antes de especificar: quanto processo a mudança merece, por ambiguidade × raio de impacto × irreversibilidade. | apêndice A |
| Pedido de decisão | Pergunta escalada ao humano com id, quem pediu, opções, recomendação, prazo, o que destrava e destino da resposta. Sem prazo, é recusado. | 03-um-humano-muitos-agentes |
| Persistência | Operação que garante que algo exista depois que a janela fecha: spec, plano, tarefas, relatório, índice de decisões, ADR. | 05-engenharia-de-contexto |
| piso | Primeiro ciclo a partir do qual uma regra nova vale; abaixo dele, a dívida fica declarada e não é rejulgada. | 10-quality-gates-que-provam-fatos |
| Piso de custo | O custo por mudança aceita quando gerar tende a zero; só verificação e reversibilidade o movem. | 01-a-mudanca-de-unidade-de-trabalho |
| plano de controle de agentes (agent control plane) | Camada que coordena, observa e governa vários agentes; no Maestro, decidiu-se construí-la com protocolos nas bordas. | 16-o-futuro-da-engenharia-agentica |
| Planta gerada | Diagrama produzido por ferramenta (no Maestro, o Archify) a partir de um arquivo JSON versionado, que registra a revisão de onde saiu. | apêndice A |
| poda | Remoção ativa do que não paga o próprio custo, com gatilho e motivo escritos; inclui a lista do que não se adota. | 14-a-organizacao-que-aprende |
| política allow / deny / ask | Decisão por papel e por ferramenta, fora do modelo: permitir, negar ou pedir aprovação humana antes de executar. O que não está escrito é negado. | 12-ferramentas-mcp-e-o-ecossistema |
| política permitir / perguntar / negar | Regra declarativa, por classe de ação, que diz se o agente age sozinho, pede confirmação humana ou é impedido; vive fora do modelo, onde o agente não a reescreve. | 11-risco-reversibilidade-e-autonomia |
| porta / adaptador | Na arquitetura hexagonal, a porta é a interface que o núcleo define para falar com o mundo; o adaptador é a implementação que fala com o mundo real (banco, rede) ou o substitui em teste (o falso). | 09-arquitetura-que-se-defende |
| Porta / adaptador (port/adapter) | A porta é a interface que o domínio expõe ou exige; o adaptador a implementa com tecnologia. Arranjo da arquitetura hexagonal (Cockburn). | 08-ddd-para-agentes |
| porta de mão única / de mão dupla | Distinção de Bezos entre decisões irreversíveis, que pedem deliberação, e reversíveis, que devem ser rápidas. O capítulo defende que transformar a primeira na segunda é trabalho de engenharia. | 11-risco-reversibilidade-e-autonomia |
| Porta inerte (seam inerte) | Contrato publicado cedo que não muda o comportamento enquanto ninguém o chama; deixa os consumidores trabalharem sem esperar o dono terminar. | 06-como-dividir-o-trabalho |
| porta nova, guarda antiga (anti-padrão 23) | Um ciclo abre um canal ou concede um poder novo e o portão que vigiava o canal velho continua lendo metade do mundo; o verde passa a significar "não olhei para lá". | 09-arquitetura-que-se-defende |
| portão antigo / portão novo | No exemplo do capítulo: o antigo confere que todo "observar" tem gatilho; o novo, que nenhum gatilho disparou sem reavaliação. | 16-o-futuro-da-engenharia-agentica |
| portão bloqueante / consultivo | Bloqueante impede o merge quando vermelho; consultivo só avisa. Portão que fica vermelho durante todo trabalho em andamento é consultivo na CI e bloqueante no ponto em que o trabalho termina. | 10-quality-gates-que-provam-fatos |
| Portão do regente | Os gates que só o humano registra (no Maestro, o aceite G7, a ordem de produção G8 e o fechamento `TAIL:gate`); para um agente, aparecem como somente leitura. | 03-um-humano-muitos-agentes |
| PRD (product requirements document) | Documento de requisitos de produto; avulso, duplica a spec. | 14-a-organizacao-que-aprende |
| prefixo mais longo | Regra de resolução de dono: entre as declarações que casam com um caminho, vence a mais específica; empate no mesmo comprimento é ambiguidade e falha. | 09-arquitetura-que-se-defende |
| premissa conferida (Premise-checked) | Registro de como a premissa da fixture foi reproduzida antes da execução. | 15-validando-o-maestro |
| premissa sobre a ferramenta | Axioma que descreve uma limitação do modelo ou do *harness* de hoje (A3, contexto finito; parte de A4, sessão que começa do zero); pode enfraquecer com a próxima geração. | 16-o-futuro-da-engenharia-agentica |
| primeira reprovação (First-red) | Registro de que o caso já foi visto reprovando; enquanto "pending", o portão fica vermelho. | 15-validando-o-maestro |
| Product Requirement Prompt (PRP) | Spec que empacota o contexto do codebase de que o agente vai precisar (arquivos, convenções, exemplos). | 05-engenharia-de-contexto |
| Progressive disclosure | Carregar o corpo de uma instrução (uma skill) só quando ela se aplica, em vez de sempre. | 05-engenharia-de-contexto |
| Projeção | Modelo de leitura que se apaga e se reconstrói a partir da fonte (arquivos, eventos). Pode ser descartada sem perda; nunca é a fonte. | 03-um-humano-muitos-agentes |
| projeção (telemetria como projeção) | Exportar o registro para outro formato (por exemplo, OpenTelemetry) como leitura derivada, sem que o domínio dependa do exportador. Desligar a projeção não muda nada no registro. | 13-observabilidade-e-economia |
| Proposta não vigente | Peça que descreve um processo desejado, não o em vigor, e se declara assim no título, no primeiro parágrafo e no índice. | apêndice A |
| protocolo | O documento que fixa, antes do primeiro dado, repetições, métricas, margens e intervalos; mudar depois de ver o resultado invalida a comparação. | apêndice C |
| prova (do destino) | Texto literal que tem de estar dentro do arquivo de destino de uma absorção, para que apontar para um arquivo qualquer não satisfaça o portão. | apêndice D |
| prova destrutiva | Verificação de uma propriedade de ciclo de vida provocando a falha de propósito (matar o servidor) e observando o que sobrevive. | 09-arquitetura-que-se-defende |
| Prova por mutação | Introduzir de propósito o defeito que um portão deveria acusar (uma mutação) e conferir que ele acusa; a contraprova é o caso legítimo que ele deve deixar passar. Prova que o portão sabe reprovar, não que mede a coisa certa. | 02-o-problema-da-confianca |
| prova por mutação de portão | Procedimento que testa o portão mutando o mundo que ele inspeciona: propriedade, fixture positiva, fixtures negativas, fixtures legítimas e resultado esperado. | 10-quality-gates-que-provam-fatos |
| proveniência | Registro de onde cada peça vendorizada veio, em que versão e em que estado (literal, adaptada); no Maestro, `.specify/UPSTREAM.md`. | 12-ferramentas-mcp-e-o-ecossistema |
| proxy (check que mede o proxy) | Algo que costuma andar junto com o fato que o portão deveria medir — a palavra, a linha, a existência do arquivo — e que pode estar presente com o fato ausente. Anti-padrão 13 do Maestro. | 10-quality-gates-que-provam-fatos |
| Proxy (de um check) | O que um portão de fato mede quando não mede o fato que diz medir: a presença de um arquivo, a ocorrência de uma palavra, a cobertura sem asserção que discrimine. | 00-prefacio |
| pré-registro | Registro datado da hipótese, do desenho e da análise antes de qualquer dado, para que nada disso mude depois de ver o resultado. | apêndice C |
| quality gate (portão) | Verificação automática ou humana que decide se um trabalho avança; no capítulo, quase sempre um script que sai com código zero (verde) ou diferente de zero (vermelho). | 10-quality-gates-que-provam-fatos |
| Quatro corpos de texto | Método normativo, *handbook* por versão, livro (argumento durável) e pesquisa (protocolo, execuções, dados). | 00-prefacio |
| Raia | Quanto processo uma mudança recebe (leve, plena, infra), em função de ambiguidade, raio de impacto e irreversibilidade. | 00-prefacio |
| Raia (de BPMN) | Faixa horizontal de um diagrama de processo (*swimlane*) que agrupa os passos de um mesmo executor. Não confundir com a raia de trabalho. | apêndice A |
| Raia (de trabalho) | Quanto processo uma mudança recebe: leve (o pull request é o artefato), plena (spec completa) ou infra (plena mais portões de reversibilidade). | apêndice A |
| Raia (regra de raia) | No Maestro, a classe de rigor de um ciclo, declarada no início: leve (o pull request é o artefato), plena (spec completa) ou infra (plena mais reversibilidade). A regra de raia fixa que cerimônia cada classe exige. | 02-o-problema-da-confianca |
| Raia infra | Infraestrutura, migração, implantação: sempre plena, mais portões de reversibilidade (backup, ensaio, homologação, plano de volta). | 04-a-spec-como-partitura |
| Raia leve (delta) | Mudança que cabe numa frase (erro de digitação, renomeação, log, bug óbvio): o pull request é o artefato; bug exige teste que o reproduz falhando antes; revisão e testes continuam obrigatórios. | 04-a-spec-como-partitura |
| Raia plena | Funcionalidade ambígua, contrato ou mudança que cruza funcionalidades: spec, plano, tarefas e relatório. | 04-a-spec-como-partitura |
| Raio de impacto | Quanto do sistema uma mudança alcança. | 04-a-spec-como-partitura |
| raio de impacto (blast radius) | Até onde vai o efeito de uma ação: o ambiente do próprio agente, algo compartilhado com o time, algo externo (produção, terceiro) ou vários inquilinos. O outro eixo da classe. | 11-risco-reversibilidade-e-autonomia |
| Raiz de agregado (aggregate root) | Entidade que guarda a consistência de um grupo de objetos; toda mudança entra por ela, e é ela quem garante as invariantes. | 08-ddd-para-agentes |
| Rastreabilidade para frente / para trás | Para frente: a intenção virou código e teste? (cobertura). Para trás: este sintoma vem de qual mudança, requisito e porquê? (recuperação, o sentido a otimizar). | 05-engenharia-de-contexto |
| Rastreio nos dois sentidos | Todo requisito tem teste, e todo teste tem requisito. Teste sem requisito é código que a spec não pediu. | 04-a-spec-como-partitura |
| rastro | O que sobra de uma execução, em formato neutro de ferramenta: arquivos antes (`base`) e depois (`final`) e a linha do tempo ordenada de commits, chamadas, aprovações e resposta. | apêndice B |
| reclassificação por capacidade | Rever a classe de risco de um componente quando ele ganha um poder novo (apagar, publicar, chamar terceiro, mexer em permissão), no plano e antes de implementar. | 11-risco-reversibilidade-e-autonomia |
| Reduce | A junção das fatias. Exige o contexto global que a divisão espalhou; pertence a quem responde pelo resultado (o humano, ou quem age sob política escrita dele). | 06-como-dividir-o-trabalho |
| Regente | Sessão de agente que coordena outras sessões e não executa o trabalho que distribui. | 02-o-problema-da-confianca |
| registro de eventos | Proposta do livro: arquivo anexável com uma linha por gatilho tocado (ideia, data, prova), conferido por um portão contra o estado corrente. | 16-o-futuro-da-engenharia-agentica |
| regra da dependência | O código-fonte só aponta para dentro, em direção ao domínio: o domínio não conhece porta nem adaptador; a porta não conhece o adaptador. | 09-arquitetura-que-se-defende |
| Regra da menor autonomia | Começar pelo padrão mais simples do espectro e só subir quando o simples comprovadamente falhar. | 06-como-dividir-o-trabalho |
| regra exposta | No mapa da fragilidade deste livro, regra que deriva de pelo menos uma premissa que enfraqueceu num cenário. | 16-o-futuro-da-engenharia-agentica |
| regra sem apoio | Regra cujas premissas enfraqueceram todas num cenário; precisa de outro motivo ou vira cerimônia. | 16-o-futuro-da-engenharia-agentica |
| Regras de desempate | Na dúvida entre leve e plena, plena; infraestrutura e migração nunca são leves. | 04-a-spec-como-partitura |
| regressão de julgamento | Segunda camada: os agentes continuam julgando como julgavam quando a linha de base foi registrada? | 15-validando-o-maestro |
| release | Versão numerada e etiquetada do método (por exemplo, 0.3.0), que comunica o que mudou; no Maestro, até 02/11/2026, existe só como seção do `CHANGELOG.md`. | apêndice C |
| Rendimento da revisão independente | Fração das revisões independentes, feitas antes do gate, que mudaram o resultado (reprovaram ou exigiram correção), lida no corpo do parecer e não no título ou no cabeçalho do relatório. Métrica da agenda de pesquisa do livro. | 02-o-problema-da-confianca |
| Repetição cega | Anti-padrão 5: repetir o mesmo *prompt* esperando outro resultado; falhou duas vezes, mude *prompt*, contexto ou tarefa. | 05-engenharia-de-contexto |
| reproduzir × replicar | Na terminologia da avaliação de artefatos da ACM (versão 1.1): reproduzir é outro time obter o resultado com os artefatos do autor; replicar é obtê-lo sem eles, refazendo o experimento a partir da descrição. | apêndice C |
| Requisito funcional (functional requirement, FR) | Item numerado da spec (FR1, FR2…) que descreve um comportamento esperado. | 04-a-spec-como-partitura |
| Reset preguiçoso | Anti-padrão 3: limpar a sessão por reflexo; o gatilho certo é a troca de papel, não o turno. | 05-engenharia-de-contexto |
| Resíduo de língua | O que um verificador de idioma mede de fato: palavras da língua errada sobrando num artefato. Não prova que o texto está na língua certa. | 08-ddd-para-agentes |
| retrabalho por linhagem | Custo de tudo o que começou depois da primeira reprovação e antes da aceitação, inclusive tarefas de correção com nomes novos e a revisão seguinte. | 13-observabilidade-e-economia |
| retrabalho por tentativa | Custo das tentativas com número ≥ 2 da mesma tarefa. Fácil de medir; subestima quando o conserto vem como tarefa nova. | 13-observabilidade-e-economia |
| Retrato | Resumo ou diagrama que descreve o método numa versão datada; envelhece quando o repositório anda e o retrato não. | apêndice A |
| Retrieval-Augmented Generation (RAG) | Geração aumentada por recuperação: buscar por similaridade o trecho relevante e pô-lo na janela. | 05-engenharia-de-contexto |
| retrospectiva (retro) | Cerimônia que transforma correção repetida em regra versionada, poda a regra que não pagou o custo e transforma passo manual repetido em script ou skill. | 14-a-organizacao-que-aprende |
| REUSE / ALIAS / EXTEND / CREATE | As quatro decisões do catálogo semântico para um nome proposto: usar o termo existente; redirecionar um apelido conhecido; qualificar uma família existente, com definição; criar um termo novo, com definição e contexto dono. Termo novo sem definição é recusado. | 08-ddd-para-agentes |
| Reversibilidade engenheirada | Mecanismos (backup, execução a seco, homologação, exclusão lógica) que barateiam desfazer e rebaixam a classe de risco de uma ação. | 00-prefacio |
| Revisão em contexto fresco | Verificação feita por um agente ou pessoa que não executou o trabalho e não carrega o histórico da sessão que o produziu. | 00-prefacio |
| RFC (request for comments) | Proposta escrita circulada para comentários antes da decisão; no Maestro, rejeitada como processo pesado. | 14-a-organizacao-que-aprende |
| Rodada / passo | Uma execução do fluxo gravada passo a passo; cada passo tem entrada, resumo e saída, e um passo sem saída bloqueia o seguinte (Maestro, ciclo 070). | 06-como-dividir-o-trabalho |
| Roteamento | Padrão que classifica a entrada e escolhe um tratamento fixo. | 06-como-dividir-o-trabalho |
| Ruling | A resposta registrada a um pedido de decisão: autor humano, data, destinatário e ligação ao que a cita. Sem autor ou sem destino, é recusada. | 03-um-humano-muitos-agentes |
| run | Uma execução de um braço do experimento num cenário, registrada num diretório de `pesquisa/runs/` com `run.json` de *schema* imutável. | apêndice C |
| SBOM (Software Bill of Materials) | Inventário de dependências de um artefato. No capítulo, citado como teatro quando a carga que importa é prosa que instrui agentes. | 12-ferramentas-mcp-e-o-ecossistema |
| Segregação de funções | Princípio de controle em que quem executa, quem confere e quem aprova são posições diferentes; aqui aplicado a agentes. | 02-o-problema-da-confianca |
| segunda lei | "Um check que você nunca viu acusar não é um check — é uma esperança": antes de confiar num portão, quebre o mundo de propósito e veja o vermelho (corolário C2). | 10-quality-gates-que-provam-fatos |
| Seleção | Operação que decide o que entra na janela de uma tarefa (agente estreito, subagente, tarefa que cita seus arquivos). | 05-engenharia-de-contexto |
| Sessão de agente | Uma execução de um perfil, que o humano sobe, observa e derruba; a unidade de administração. | 07-papeis-e-skills |
| Skill | Procedimento recorrente empacotado como `SKILL.md` (nome, descrição com gatilho, passos), que dispara pelo contexto. Diferente de comando (invocação explícita) e de agente (quem faz). | 07-papeis-e-skills |
| Skill invisível | Skill que existe no disco e não é citada na instrução; para a IA, não existe. | 05-engenharia-de-contexto |
| Skill órfã | Skill que nenhum papel consome (ou, na versão editorial do problema, que nenhum capítulo ensina). | 07-papeis-e-skills |
| Spec (especificação) | Documento que diz **o quê** e **por quê** de uma mudança: o problema, o valor e o que se observa quando o problema está resolvido. Não diz o como. | 04-a-spec-como-partitura |
| Spec a montante / a jusante | A montante: a spec alimenta algo (teste, verificador, revisão), e mudá-la quebra o que está abaixo. A jusante: o documento descreve o código depois e pode ficar errado sem que nada aconteça. | 04-a-spec-como-partitura |
| Spec-as-source | Tese (Tessl) em que a spec é reexecutada continuamente e o código é só saída. | 04-a-spec-como-partitura |
| Spec-Driven Development (SDD) | Desenvolvimento dirigido por especificação: a spec é a fonte de verdade e vem antes do código. | 04-a-spec-como-partitura |
| SPIDR | *Spike, Path, Interface, Data, Rules*: cinco linhas de corte de uma história, de Mike Cohn. | 06-como-dividir-o-trabalho |
| SRE (site reliability engineering) | Engenharia de confiabilidade de sites, a disciplina do Google de onde vem o postmortem sem culpa. | 14-a-organizacao-que-aprende |
| stdio | A entrada e a saída padrão de um processo; o transporte MCP em que o cliente sobe o servidor como subprocesso e conversa por linhas. | 12-ferramentas-mcp-e-o-ecossistema |
| Steward | No Maestro, o humano que responde pelo método. | 14-a-organizacao-que-aprende |
| superfície de ferramentas | O conjunto de ferramentas que um agente alcança numa sessão, cada uma com a classe de risco da ação que executa. É a unidade de governança quando o agente age no mundo. | 12-ferramentas-mcp-e-o-ecossistema |
| TAIL:mutation | Passo da cauda que exige que todo portão criado ou alterado no ciclo tenha sido visto reprovando; a dispensa é lida do diff. | 10-quality-gates-que-provam-fatos |
| Tamanho de lote (batch size) | Quantas mudanças são integradas juntas. Lote menor reduz o custo de desfazer e move as métricas do DevOps Research and Assessment (DORA) na mesma direção. | 01-a-mudanca-de-unidade-de-trabalho |
| Tarefa de contexto zero | Tarefa escrita para quem não viu a conversa: cita arquivo ou comando e tem critério de pronto. Absorvida do Superpowers ("assuma zero contexto"). | 05-engenharia-de-contexto |
| taxa de cache | Tokens de entrada lidos do *cache* de prompt divididos pelo total de entrada. Alta em sessões longas; faz "tokens por tarefa" parecer duas ordens de grandeza maior do que o texto novo. | 13-observabilidade-e-economia |
| teatro de cerimônia | Anti-padrão 11: processo que não muda decisão nenhuma; gate que nunca rejeita. | 14-a-organizacao-que-aprende |
| tentativa · desfecho · veredito | Três campos distintos: quantas vezes a tarefa foi tentada; se a sessão conseguiu fazê-la (`delivered`, `blocked`, `failed`…); se o trabalho foi aceito por um juiz independente (`approved`, `approved_with_notes`, `rejected`). | 13-observabilidade-e-economia |
| teorema (no Maestro) | Consequência dos axiomas, com evidência no próprio repositório (T1–T7); cada um declara de quais axiomas deriva. | 16-o-futuro-da-engenharia-agentica |
| teorema T5 | Do Maestro (A3 + A4): um artefato sobrevive por consumo ou por imutabilidade. | 14-a-organizacao-que-aprende |
| teorema T6 | Do Maestro (A3 + A4): a correção que não vira regra versionada se repete. | 14-a-organizacao-que-aprende |
| Teoria das Restrições (TOC) | *Theory of Constraints* (Goldratt): a vazão de um sistema é a vazão da sua restrição; melhorar fora dela não muda o resultado. Num time de agentes, a restrição é a decisão humana. | 03-um-humano-muitos-agentes |
| teste de caracterização | Teste que registra o comportamento atual de código existente antes de alterá-lo. | 10-quality-gates-que-provam-fatos |
| teste de contrato | Uma única bateria de casos rodada contra todos os adaptadores de uma porta, inclusive o falso, para que o dublê não seja mais frouxo que a produção. | 09-arquitetura-que-se-defende |
| Teste de pressão | Cenário escrito para que o agente tenha motivo para desobedecer a regra (pressa, conserto "óbvio"); é a fixture da linha de base de uma skill. | 07-papeis-e-skills |
| Token | Unidade em que o modelo mede texto. No exemplo do capítulo, estimado como caracteres ÷ 4 — régua grosseira, declarada. | 05-engenharia-de-contexto |
| Trabalho em curso (WIP) | *Work in progress*. Neste capítulo, medido em decisões humanas pendentes, e não em tarefas abertas ou agentes ativos. | 03-um-humano-muitos-agentes |
| Transferência | Operação que entrega à próxima sessão o que esta sabia: arquivo de instrução, carga de estado no início, revisor que começa do zero com diff e critério. | 05-engenharia-de-contexto |
| Trilha (do site) | Um dos cinco caminhos de leitura do site do Maestro, cada um de um tipo de documentação: Jornada, Capítulos, Receitas, Referência, Bastidores. | apêndice A |
| Unidade de trabalho | O que um time conta como "uma coisa feita" e usa para planejar e medir. Com agentes, desloca-se da mudança escrita para a mudança aceita. | 01-a-mudanca-de-unidade-de-trabalho |
| varredura | Estudo de campo por fontes primárias, sem instalar nada; decide bem o que é descartável por princípio e mal o que depende de mecanismo. | apêndice D |
| vazamento do contrato | Quando o contrato ensina a regra em vez de só o formato. Pego em parte por `contrato_nao_diz` (termos da regra) e, no resto, medido rodando o nível A com e sem o contrato. | apêndice B |
| Vendorizar | Trazer para dentro do repositório, como fonte própria e adaptada, o que se usa de uma ferramenta de terceiro, consultando o original por decisão e não por acidente. | 04-a-spec-como-partitura |
| veredito (absorver, adotar, descartar, observar) | Os quatro estados de uma ideia no catálogo: absorvida no método, adotada como ferramenta, descartada, ou em observação com gatilho. | 16-o-futuro-da-engenharia-agentica |
| veredito conferível | Evidência de gate com cabeçalho verificável por máquina: gate, objeto @ hash, veredito, autor, data. | 10-quality-gates-que-provam-fatos |
| veredito só de estado | Veredito com as violações de declaração descartadas (`--so-estado`); vale mesmo para execuções que não receberam o contrato. | apêndice B |
| vigília do futuro | O conjunto catálogo + gatilhos + portão + cadência com que um time percebe, sem depender de memória, que uma premissa mudou. | 16-o-futuro-da-engenharia-agentica |
| violação de estado / de declaração | Classes das violações que um oráculo emite: de estado vem dos arquivos e da linha do tempo; de declaração depende do formato do contrato e leva o prefixo `[declaração]`. | apêndice B |
| vocabulário fechado de veredito | `adotar` (a ferramenta vira dependência), `absorver` (a ideia é reimplementada), `observar` (não agora, com gatilho), `descartar` (não entra, com motivo). | apêndice D |
| válvula de escape declarada | Forma registrada de dispensar um portão (uma label, um `n/a:` com motivo), que mantém o desvio auditável. | 10-quality-gates-que-provam-fatos |
| wave-engine | Mecanismo do `maestro-02` que roda um comando em fases tipadas com um resultado de validação entre cada fase. | apêndice D |
| Worktree | Cópia de trabalho adicional de um repositório Git, com branch própria; isola as edições de um agente das de outro. | 06-como-dividir-o-trabalho |
| YAGNI (you aren't gonna need it) | "Você não vai precisar disso": a complexidade além do necessário é justificada por escrito ou removida. | 14-a-organizacao-que-aprende |
| YAGNI com gatilho | Decisão de não construir algo agora registrada junto com a condição observável que a reabre. | 13-observabilidade-e-economia |
| índice de decisões | `docs/records/decisoes.jsonl` no Maestro: uma linha JSON por decisão, achado, gate ou retro; só cresce. | 14-a-organizacao-que-aprende |
| índice de estado | Arquivo JSONL só de acréscimo com o veredito corrente de cada ideia; vale a última linha de cada id. | apêndice D |
| Índice só-acréscimo | Registro em que cada linha é um fato imutável; corrigir é acrescentar uma linha que "fecha" a anterior, nunca reescrever. | 05-engenharia-de-contexto |
| órfão | Tarefa com início e sem fim no registro: trabalho pago e não entregue. Nunca é fechado por inferência. | 13-observabilidade-e-economia |
| Ótimo local | Cada fatia perfeita e o conjunto quebrado, porque nenhum executor viu o todo; preço de cortar demais ou na costura errada. | 05-engenharia-de-contexto |
