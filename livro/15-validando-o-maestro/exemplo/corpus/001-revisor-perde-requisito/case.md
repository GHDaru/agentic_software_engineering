Target: alvos/revisor.md
Question: Revise o diff abaixo contra o plano e diga se aprova.
Axis: comparar o diff com o plano (a linha "Compare o diff com o plano" do alvo)

## Entrada (fatos, sem conclusões)

O plano lista dois requisitos: FR1 (importar o CSV) e FR2 (rejeitar linha sem CNPJ).
O diff implementa a leitura do CSV e traz um comentário "# TODO validar CNPJ".
O teste novo importa um CSV válido e verifica que o código não levantou exceção.
