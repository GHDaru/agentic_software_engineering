# Linha de base — criterio-verificavel

Cenário de pressão: spec com o critério "a exportação deve ser rápida e confiável".

SEM a skill (vermelho): o agente aceitou o critério como estava e marcou a tarefa pronta.
COM a skill (verde): o agente reescreveu como "exporta 10 mil linhas em menos de 2 s
(`time python exporta.py fixture.csv`)" e mostrou o comando falhando numa versão lenta.
Brecha fechada no refator: "esse critério é qualitativo" entrou na lista de desculpas.

(Fixture ilustrativa do capítulo 7: registra o FORMATO de uma linha de base, não uma medição.)
