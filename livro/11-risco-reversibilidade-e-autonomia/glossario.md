# Glossário do capítulo 11

| termo | definição |
|---|---|
| classe de risco | Degrau (0 a 6) de uma escada que decide quanta autonomia o agente tem numa ação e que gate humano ela recebe: leitura, leitura sensível, criação reversível, alteração, exclusão ou efeito externo, financeira ou irreversível, lote/entre inquilinos/administrativa. |
| custo de desfazer | Quanto custa voltar ao estado anterior a uma ação: nada, trivial (`git revert`), barato (desmarcar uma exclusão lógica), caro (restaurar de *backup*) ou impossível (segredo lido, e-mail enviado, dado apagado sem cópia). Um dos dois eixos da classe. |
| raio de impacto (*blast radius*) | Até onde vai o efeito de uma ação: o ambiente do próprio agente, algo compartilhado com o time, algo externo (produção, terceiro) ou vários inquilinos. O outro eixo da classe. |
| gate uniforme | O mesmo rito de aprovação para toda ação. Falha de dois jeitos simétricos: pesado, vira funil e carimbo; leve, deixa o irreversível passar. |
| carimbo (*rubber stamp*) | Aprovação dada sem exame, por excesso de volume ou hábito; tem a aparência de controle e produz registro de uma decisão que ninguém tomou. |
| gate *ex-ante* / registro *ex-post* | O gate barra antes de executar; o registro descreve depois. Para ação irreversível, só o primeiro impede o dano. |
| reversibilidade engenheirada | Mecanismos construídos para tornar uma ação desfazível ou ensaiável — cópia de segurança, execução a seco, homologação, exclusão lógica, cópia ao lado — que rebaixam a classe de risco (corolário C4 do Maestro). |
| alavanca de reversibilidade | Cada um desses mecanismos, lido pelo eixo em que age: cópia de segurança e exclusão lógica no custo de desfazer, homologação no raio, execução a seco nos dois. |
| execução a seco (*dry run*) | Executar a ação sem efeito, só mostrando o que faria; a ação ensaiada é leitura. |
| exclusão lógica (*soft delete*) | Marcar como apagado em vez de apagar; desfazer é desmarcar. |
| cópia ao lado | Guardar a versão anterior de um arquivo junto dele (no Maestro, `.maestro-old` e `.maestro-new`) antes de sobrescrever ou para oferecer a versão nova sem sobrescrever. |
| porta de mão única / de mão dupla | Distinção de Bezos entre decisões irreversíveis, que pedem deliberação, e reversíveis, que devem ser rápidas. O capítulo defende que transformar a primeira na segunda é trabalho de engenharia. |
| política `permitir / perguntar / negar` | Regra declarativa, por classe de ação, que diz se o agente age sozinho, pede confirmação humana ou é impedido; vive fora do modelo, onde o agente não a reescreve. |
| ação administrativa (autoconcessão) | Ação que altera permissão, identidade ou política — inclusive a do próprio agente. Classe 6: bloqueada para agente. |
| manifesto por hash | Registro, gravado pelo instalador, do hash de cada arquivo que ele escreveu; permite distinguir versão velha (inalterada, pode atualizar) de arquivo editado pelo projeto (mantido). |
| delegação de política (gate por delegação) | Gate humano decidido por uma sessão que não executou o trabalho, com delegação escrita e revogável do humano, crítico independente em contexto fresco e uma linha de registro por gate (ADR 0026 do Maestro). O humano responde pela política, não por cada visto. |
| escape declarado | Saída legítima e documentada de um gate (no Maestro, o `--yes` do script de promoção) usada quando o humano já decidiu; evita que o gate seja contornado por fora, sem registro. |
| reclassificação por capacidade | Rever a classe de risco de um componente quando ele ganha um poder novo (apagar, publicar, chamar terceiro, mexer em permissão), no plano e antes de implementar. |
