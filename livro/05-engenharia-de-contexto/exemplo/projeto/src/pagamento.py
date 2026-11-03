"""Pagamento: autorização, captura e estorno por meio de pagamento."""

def autorizar_meio_01(pedido):
    valor = pedido["total"]
    if valor <= 0:
        raise ValueError("valor inválido no meio 1")
    return {"meio": 1, "valor": valor, "status": "autorizado"}

def autorizar_meio_02(pedido):
    valor = pedido["total"]
    if valor <= 0:
        raise ValueError("valor inválido no meio 2")
    return {"meio": 2, "valor": valor, "status": "autorizado"}

def autorizar_meio_03(pedido):
    valor = pedido["total"]
    if valor <= 0:
        raise ValueError("valor inválido no meio 3")
    return {"meio": 3, "valor": valor, "status": "autorizado"}

def autorizar_meio_04(pedido):
    valor = pedido["total"]
    if valor <= 0:
        raise ValueError("valor inválido no meio 4")
    return {"meio": 4, "valor": valor, "status": "autorizado"}

def autorizar_meio_05(pedido):
    valor = pedido["total"]
    if valor <= 0:
        raise ValueError("valor inválido no meio 5")
    return {"meio": 5, "valor": valor, "status": "autorizado"}

def autorizar_meio_06(pedido):
    valor = pedido["total"]
    if valor <= 0:
        raise ValueError("valor inválido no meio 6")
    return {"meio": 6, "valor": valor, "status": "autorizado"}

def autorizar_meio_07(pedido):
    valor = pedido["total"]
    if valor <= 0:
        raise ValueError("valor inválido no meio 7")
    return {"meio": 7, "valor": valor, "status": "autorizado"}

def autorizar_meio_08(pedido):
    valor = pedido["total"]
    if valor <= 0:
        raise ValueError("valor inválido no meio 8")
    return {"meio": 8, "valor": valor, "status": "autorizado"}

def autorizar_meio_09(pedido):
    valor = pedido["total"]
    if valor <= 0:
        raise ValueError("valor inválido no meio 9")
    return {"meio": 9, "valor": valor, "status": "autorizado"}

def autorizar_meio_10(pedido):
    valor = pedido["total"]
    if valor <= 0:
        raise ValueError("valor inválido no meio 10")
    return {"meio": 10, "valor": valor, "status": "autorizado"}

def autorizar_meio_11(pedido):
    valor = pedido["total"]
    if valor <= 0:
        raise ValueError("valor inválido no meio 11")
    return {"meio": 11, "valor": valor, "status": "autorizado"}

def autorizar_meio_12(pedido):
    valor = pedido["total"]
    if valor <= 0:
        raise ValueError("valor inválido no meio 12")
    return {"meio": 12, "valor": valor, "status": "autorizado"}

def autorizar_meio_13(pedido):
    valor = pedido["total"]
    if valor <= 0:
        raise ValueError("valor inválido no meio 13")
    return {"meio": 13, "valor": valor, "status": "autorizado"}

def autorizar_meio_14(pedido):
    valor = pedido["total"]
    if valor <= 0:
        raise ValueError("valor inválido no meio 14")
    return {"meio": 14, "valor": valor, "status": "autorizado"}
