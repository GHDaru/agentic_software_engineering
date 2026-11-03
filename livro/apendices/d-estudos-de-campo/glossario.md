# Glossário do apêndice D

Termos novos deste apêndice. Termos já definidos em outros capítulos (ADR, SDD, EARS, MCP,
YAGNI, DoD) não se repetem aqui.

| termo | definição |
|---|---|
| estudo de campo | Avaliação datada de trabalho de terceiros (ferramenta, framework, plataforma) feita para decidir o que atravessa a fronteira do método; tem pergunta, versão observada, vereditos e destino. |
| varredura | Estudo de campo por fontes primárias, sem instalar nada; decide bem o que é descartável por princípio e mal o que depende de mecanismo. |
| estudo com a mão no código | Estudo de campo sobre o repositório real, numa versão ou commit fixado, lido arquivo por arquivo; acha o mecanismo que a varredura não vê. |
| panorama (triagem) | Varredura larga que só classifica cada item como candidato a estudo com gatilho, observar ou fora do problema, sem repetir veredito já dado. |
| funil de avaliação | Sequência varredura → gatilho → estudo com a mão no código → absorção por portão humano; cada etapa custa mais e só se passa adiante com motivo escrito. |
| catálogo do ecossistema | Registro de estudos de campo em três peças: fontes (com licença), cards de ideia (imutáveis) e índice de estado (só acrescenta). |
| card de ideia | Registro imutável e datado de uma ideia vista numa fonte: o que é, o veredito daquele momento, o destino, o gatilho e as sete dimensões. |
| índice de estado | Arquivo JSONL só de acréscimo com o veredito corrente de cada ideia; vale a última linha de cada id. |
| momento × estado | Separação entre o que se julgou num dia (card) e o que vale hoje (índice); misturar os dois obriga a reescrever a história ou a mentir sobre o presente. |
| vocabulário fechado de veredito | `adotar` (a ferramenta vira dependência), `absorver` (a ideia é reimplementada), `observar` (não agora, com gatilho), `descartar` (não entra, com motivo). |
| absorção fantasma | Ideia registrada como absorvida cujo destino não existe no disco ou não contém a ideia; intenção registrada como fato. |
| gatilho de reavaliação | Condição observável escrita que, quando acontece, reabre um veredito `observar`; "quando doer" não conta. |
| prova (do destino) | Texto literal que tem de estar dentro do arquivo de destino de uma absorção, para que apontar para um arquivo qualquer não satisfaça o portão. |
| citável, não copiável | Marca da fonte cuja licença permite ler e citar, mas não redistribuir (proprietária, comercial, sem licença declarada, não comercial). |
| dimensão que reprova sozinha | Critério de avaliação que decide sem compensação por outros: conflito insanável com princípio e licença incompatível. |
| confronto | Etapa de uma pesquisa de mercado em que cada funcionalidade é cruzada com o estado do método e decidida como `ENTRA`, `NÃO PRECISA` ou `DEPOIS`, com fonte. |
| "não encontrado na documentação lida" | Forma obrigatória de registrar uma célula sem fonte; proíbe ler ausência de evidência como lacuna de mercado. |
| wave-engine | Mecanismo do `maestro-02` que roda um comando em fases tipadas com um resultado de validação entre cada fase. |
| context-slicer | Mecanismo do `maestro-02` que injeta só as seções relevantes do contexto e reporta a economia de tokens contra o contexto inteiro. |
| Product Requirement Prompt (PRP) | Documento de requisitos acrescido do contexto curado do codebase (arquivos, convenções, armadilhas) e do roteiro do agente. |
| Memory Bank | Padrão de memória de sessão em arquivos markdown estruturados que o agente relê a cada sessão, com um arquivo curto de contexto ativo. |
