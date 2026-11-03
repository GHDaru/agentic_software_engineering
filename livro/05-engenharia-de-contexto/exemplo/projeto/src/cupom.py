"""Cupom de desconto: validação e cálculo (domínio, sem I/O)."""

def validar(cupom, hoje):
    if cupom["vence_em"] < hoje:
        raise ValueError(f"cupom vencido em {cupom['vence_em']}")
    return cupom

def desconto(subtotal, cupom):
    pct = cupom["percentual"]
    if not 0 < pct <= 100:
        raise ValueError("percentual fora de 1..100")
    return round(subtotal * pct / 100, 2)
