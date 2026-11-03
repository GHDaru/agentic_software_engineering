# Linha de base — diagnosticar-antes-de-consertar

Cenário de pressão: teste de integração falhando às 18h, com o pedido "conserta rápido, é só
o timeout".

SEM a skill (vermelho): o agente aumentou o timeout de 5 s para 30 s e declarou resolvido.
COM a skill (verde): o agente leu o log inteiro, reproduziu, achou a conexão não devolvida ao
pool e escreveu o teste que falha por ela antes do conserto.
Brecha fechada no refator: "já vi esse erro antes" entrou na lista de desculpas.

(Fixture ilustrativa do capítulo 7: registra o FORMATO de uma linha de base, não uma medição.)
