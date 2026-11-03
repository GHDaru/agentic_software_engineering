# Glossário do capítulo 8

| termo | definição |
|---|---|
| Domain-Driven Design (DDD) | Projeto dirigido pelo domínio (Evans, 2003): desenhar o software a partir do modelo do negócio e da língua que o negócio fala. |
| Linguagem ubíqua (*ubiquitous language*) | Vocabulário único de um contexto delimitado, acordado entre quem pede e quem constrói, usado literalmente no código, nos testes e na conversa. Para agentes, precisa ser um artefato que alguma máquina lê. |
| Contexto delimitado (*bounded context*) | Fronteira dentro da qual uma palavra tem um sentido só; é também a costura por onde o trabalho se corta para rodar em paralelo. |
| Raiz de agregado (*aggregate root*) | Entidade que guarda a consistência de um grupo de objetos; toda mudança entra por ela, e é ela quem garante as invariantes. |
| Invariante | Regra de negócio que precisa valer sempre. Mora no domínio (agregado, objeto de valor, serviço de domínio) ou, por exceção com motivo escrito, na borda (rota, adaptador, tela). |
| Borda decidida × borda por descuido | A regra posta na borda com o motivo escrito (permitida) e a posta ali sem que ninguém decidisse (o defeito que o portão recusa). |
| Porta / adaptador (*port/adapter*) | A porta é a interface que o domínio expõe ou exige; o adaptador a implementa com tecnologia. Arranjo da arquitetura hexagonal (Cockburn). |
| Camada anticorrupção (*anticorruption layer*) | Adaptador que traduz o vocabulário de outro sistema para o seu, com um mapa escrito, para o termo estrangeiro não entrar no domínio quando o sentido não é 1:1. |
| Modelo de domínio declarado | As quatro decisões que um plano torna explícitas, cada uma com motivo: raiz de agregado, onde moram as invariantes, mudanças de linguagem ubíqua, portas e adaptadores (`DOM:aggregate`, `DOM:invariants`, `DOM:glossary`, `DOM:ports`). Silêncio não é decisão. |
| Catálogo semântico | Linguagem ubíqua operacional: o lugar que se consulta antes de criar um nome ou um componente, com quatro saídas — REUSE, ALIAS, EXTEND, CREATE. |
| REUSE / ALIAS / EXTEND / CREATE | As quatro decisões do catálogo semântico para um nome proposto: usar o termo existente; redirecionar um apelido conhecido; qualificar uma família existente, com definição; criar um termo novo, com definição e contexto dono. Termo novo sem definição é recusado. |
| Colisão de nomes | Uma palavra com dois sentidos em dois contextos ("fila" de decisões × fila de saída). Remédio: qualificar a palavra e separar os contextos. |
| Colisão de endereço | Um identificador que aponta para duas coisas, ou para nenhuma (nome em dois projetos, referência que mudou ao reiniciar). Invariante: endereço ambíguo é recusado, nunca resolvido. |
| Família que nunca se escreve nua | Palavra com mais de um sentido no domínio que só aparece qualificada ("prazo de resposta", nunca "prazo"); a lista mora no modelo, que um *lint* lê. |
| Papel semântico | O que um objeto de tela **é** (ação primária, confirmação irreversível, ausência declarada), decidido antes do componente; a anatomia obrigatória deriva do papel. |
| Glossário gerado | Glossário produzido a partir do modelo de domínio, com o carimbo do modelo; a integração contínua regera da fonte e recusa divergência. |
| Resíduo de língua | O que um verificador de idioma mede de fato: palavras da língua errada sobrando num artefato. Não prova que o texto está na língua certa. |
| Amontoado (*pile-up*) | Documento denso: muitas siglas sem dicionário, tudo numa página, sem narrativa. Combatido pela regra "sigla nunca nasce nua". |
