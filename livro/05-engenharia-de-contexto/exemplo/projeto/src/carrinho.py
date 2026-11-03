"""Carrinho: itens, subtotal e cupom (um só)."""

def subtotal(itens):
    return round(sum(i["preco"] * i["qtd"] for i in itens), 2)

def aplicar_cupom(carrinho, cupom, hoje):
    from cupom import validar, desconto
    validar(cupom, hoje)
    carrinho["cupom"] = cupom  # substitui, nunca soma (ADR 0003)
    total = subtotal(carrinho["itens"]) - desconto(subtotal(carrinho["itens"]), cupom)
    return max(total, 0)
