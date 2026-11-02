"""frete.py — a implementação que a spec.md pede (e só ela).

O limite está escrito aqui como constante, de propósito: é o código "a jusante". Quando a
spec muda (casos/spec-v2.md), os testes, que leem o limite DA SPEC, ficam vermelhos até
alguém mudar esta linha. A obsolescência deixa de ser silenciosa.
"""

LIMITE_FRETE_GRATIS = 200.00
TABELA_POR_REGIAO = {"sul": 25.00, "sudeste": 20.00, "norte": 40.00}


def frete(subtotal, regiao):
    if subtotal < 0:
        raise ValueError("subtotal negativo")
    if subtotal >= LIMITE_FRETE_GRATIS:
        return 0.00
    return TABELA_POR_REGIAO[regiao]
