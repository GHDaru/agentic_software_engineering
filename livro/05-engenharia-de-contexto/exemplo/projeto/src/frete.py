"""Frete: tabela por faixa de CEP e peso."""

def faixa_01(pedido):
    peso = pedido["peso_kg"]
    return round(9.9 + 1 * 1.5 + peso * 0.8, 2)

def faixa_02(pedido):
    peso = pedido["peso_kg"]
    return round(9.9 + 2 * 1.5 + peso * 0.8, 2)

def faixa_03(pedido):
    peso = pedido["peso_kg"]
    return round(9.9 + 3 * 1.5 + peso * 0.8, 2)

def faixa_04(pedido):
    peso = pedido["peso_kg"]
    return round(9.9 + 4 * 1.5 + peso * 0.8, 2)

def faixa_05(pedido):
    peso = pedido["peso_kg"]
    return round(9.9 + 5 * 1.5 + peso * 0.8, 2)

def faixa_06(pedido):
    peso = pedido["peso_kg"]
    return round(9.9 + 6 * 1.5 + peso * 0.8, 2)

def faixa_07(pedido):
    peso = pedido["peso_kg"]
    return round(9.9 + 7 * 1.5 + peso * 0.8, 2)

def faixa_08(pedido):
    peso = pedido["peso_kg"]
    return round(9.9 + 8 * 1.5 + peso * 0.8, 2)
