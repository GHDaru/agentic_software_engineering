# Glossário do capítulo 12

| termo | definição |
|---|---|
| MCP (*Model Context Protocol*) | Protocolo aberto pelo qual um cliente (o harness do agente) descobre e chama capacidades de um servidor: ferramentas, recursos e prompts, em mensagens JSON-RPC 2.0 por stdio ou HTTP. Padroniza o encanamento; não decide permissão nem confiança. |
| JSON-RPC (*JSON Remote Procedure Call*) | Formato de chamada remota em JSON (*JavaScript Object Notation*): cada mensagem tem `method`, `params` e `id`; a resposta traz `result` ou `error`. |
| stdio | A entrada e a saída padrão de um processo; o transporte MCP em que o cliente sobe o servidor como subprocesso e conversa por linhas. |
| superfície de ferramentas | O conjunto de ferramentas que um agente alcança numa sessão, cada uma com a classe de risco da ação que executa. É a unidade de governança quando o agente age no mundo. |
| agência excessiva (*excessive agency*) | Item LLM06 do OWASP Top 10 para aplicações com LLM: funcionalidade, permissão ou autonomia além do que a tarefa pede. |
| injeção de prompt indireta | Instrução plantada em conteúdo que o modelo apenas lê (issue, página, resultado de ferramenta) e que ele pode obedecer como se viesse do operador. Item LLM01 do OWASP. |
| *enforcement* (imposição) | Mecanismo que o agente não pode pular porque não passa por ele: permissão do harness, hook que recusa, portão da CI. Contrasta com instrução, que vale enquanto for seguida. |
| hook (`PreToolUse`, `SessionStart`, `Stop`) | Gancho do harness executado em um evento da sessão; o `PreToolUse` roda antes de uma ferramenta e pode recusar a chamada. É mecanismo de um harness específico. |
| falhar aberto (*fail open*) | Comportamento de um guarda que, ao quebrar, deixa passar em vez de bloquear. O guarda do Maestro faz isso de propósito e delega a detecção ao portão. |
| fiação | A ligação entre o mecanismo e quem o chama (o `settings.json` que aponta para o hook). Provar o script sem provar a fiação é decoração. |
| política `allow / deny / ask` | Decisão por papel e por ferramenta, fora do modelo: permitir, negar ou pedir aprovação humana antes de executar. O que não está escrito é negado. |
| cerca do dado | Marcas que delimitam o conteúdo de terceiros devolvido ao modelo, com teto de bytes, marca de corte e neutralização de marcas internas. Torna a fronteira visível; não é sandbox. |
| identidade pelo token | Regra de desenho: o autor de uma chamada vem da credencial do processo, nunca de um argumento que o modelo escreve. |
| vendorizar | Trazer o conteúdo de um upstream para dentro do repositório como fonte própria, adaptado, com proveniência registrada e atualização só por decisão. |
| proveniência | Registro de onde cada peça vendorizada veio, em que versão e em que estado (literal, adaptada); no Maestro, `.specify/UPSTREAM.md`. |
| atribuição que viaja | Licença e notas de terceiros que acompanham cada canal de redistribuição (instalador, plugin), renomeadas no destino para não afirmar que o projeto alheio inteiro tem aquela licença. |
| SBOM (*Software Bill of Materials*) | Inventário de dependências de um artefato. No capítulo, citado como teatro quando a carga que importa é prosa que instrui agentes. |
| catálogo do ecossistema | Registro de avaliações de terceiros com a ideia como unidade, cartão datado e imutável por observação, e veredito corrente num índice append-only. |
| absorção fantasma | Ideia registrada como absorvida cujo destino não existe no disco. O `check-ecosystem.sh` do Maestro achou duas na primeira execução. |
| gatilho de reavaliação | Condição escrita e verificável que reabre um veredito "observar"; sem ela, observar é esquecer com cerimônia. |
| manifesto de instalação | Registro, com hash, de cada arquivo que o instalador escreveu; permite distinguir versão antiga (renovar) de arquivo modificado pelo projeto (manter). |
| escolha de agente declarada | O instalador recebe o agente-alvo (`--ai`) de uma tabela, grava a escolha e recusa id desconhecido, em vez de supor um harness. |
| A2A (*Agent2Agent*) | Protocolo de comunicação entre agentes; no Maestro, seus nomes entram no envelope de mensagem, sem adotar fio nem SDK. |
| ACP (*Agent Client Protocol*) | Protocolo entre um editor ou host e um agente de código; avaliado pelo Maestro como modo de harness. |
| BYOK (*bring your own key*) | O usuário fornece a própria chave do provedor de modelo; no companion do Maestro, usada só na requisição e nunca persistida. |
