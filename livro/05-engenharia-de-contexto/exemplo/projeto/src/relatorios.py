"""Relatórios gerenciais: vendas, descontos, devoluções, por período."""

def relatorio_01(pedido):
    linhas = [p for p in pedido["historico"] if p["tipo"] == "tipo_1"]
    total = sum(p["valor"] for p in linhas)
    desconto = sum(p.get("desconto", 0) for p in linhas)
    return {"relatorio": 1, "total": total, "desconto": desconto, "n": len(linhas)}

def relatorio_02(pedido):
    linhas = [p for p in pedido["historico"] if p["tipo"] == "tipo_2"]
    total = sum(p["valor"] for p in linhas)
    desconto = sum(p.get("desconto", 0) for p in linhas)
    return {"relatorio": 2, "total": total, "desconto": desconto, "n": len(linhas)}

def relatorio_03(pedido):
    linhas = [p for p in pedido["historico"] if p["tipo"] == "tipo_3"]
    total = sum(p["valor"] for p in linhas)
    desconto = sum(p.get("desconto", 0) for p in linhas)
    return {"relatorio": 3, "total": total, "desconto": desconto, "n": len(linhas)}

def relatorio_04(pedido):
    linhas = [p for p in pedido["historico"] if p["tipo"] == "tipo_4"]
    total = sum(p["valor"] for p in linhas)
    desconto = sum(p.get("desconto", 0) for p in linhas)
    return {"relatorio": 4, "total": total, "desconto": desconto, "n": len(linhas)}

def relatorio_05(pedido):
    linhas = [p for p in pedido["historico"] if p["tipo"] == "tipo_5"]
    total = sum(p["valor"] for p in linhas)
    desconto = sum(p.get("desconto", 0) for p in linhas)
    return {"relatorio": 5, "total": total, "desconto": desconto, "n": len(linhas)}

def relatorio_06(pedido):
    linhas = [p for p in pedido["historico"] if p["tipo"] == "tipo_6"]
    total = sum(p["valor"] for p in linhas)
    desconto = sum(p.get("desconto", 0) for p in linhas)
    return {"relatorio": 6, "total": total, "desconto": desconto, "n": len(linhas)}

def relatorio_07(pedido):
    linhas = [p for p in pedido["historico"] if p["tipo"] == "tipo_7"]
    total = sum(p["valor"] for p in linhas)
    desconto = sum(p.get("desconto", 0) for p in linhas)
    return {"relatorio": 7, "total": total, "desconto": desconto, "n": len(linhas)}

def relatorio_08(pedido):
    linhas = [p for p in pedido["historico"] if p["tipo"] == "tipo_8"]
    total = sum(p["valor"] for p in linhas)
    desconto = sum(p.get("desconto", 0) for p in linhas)
    return {"relatorio": 8, "total": total, "desconto": desconto, "n": len(linhas)}

def relatorio_09(pedido):
    linhas = [p for p in pedido["historico"] if p["tipo"] == "tipo_9"]
    total = sum(p["valor"] for p in linhas)
    desconto = sum(p.get("desconto", 0) for p in linhas)
    return {"relatorio": 9, "total": total, "desconto": desconto, "n": len(linhas)}

def relatorio_10(pedido):
    linhas = [p for p in pedido["historico"] if p["tipo"] == "tipo_10"]
    total = sum(p["valor"] for p in linhas)
    desconto = sum(p.get("desconto", 0) for p in linhas)
    return {"relatorio": 10, "total": total, "desconto": desconto, "n": len(linhas)}

def relatorio_11(pedido):
    linhas = [p for p in pedido["historico"] if p["tipo"] == "tipo_11"]
    total = sum(p["valor"] for p in linhas)
    desconto = sum(p.get("desconto", 0) for p in linhas)
    return {"relatorio": 11, "total": total, "desconto": desconto, "n": len(linhas)}

def relatorio_12(pedido):
    linhas = [p for p in pedido["historico"] if p["tipo"] == "tipo_12"]
    total = sum(p["valor"] for p in linhas)
    desconto = sum(p.get("desconto", 0) for p in linhas)
    return {"relatorio": 12, "total": total, "desconto": desconto, "n": len(linhas)}

def relatorio_13(pedido):
    linhas = [p for p in pedido["historico"] if p["tipo"] == "tipo_13"]
    total = sum(p["valor"] for p in linhas)
    desconto = sum(p.get("desconto", 0) for p in linhas)
    return {"relatorio": 13, "total": total, "desconto": desconto, "n": len(linhas)}

def relatorio_14(pedido):
    linhas = [p for p in pedido["historico"] if p["tipo"] == "tipo_14"]
    total = sum(p["valor"] for p in linhas)
    desconto = sum(p.get("desconto", 0) for p in linhas)
    return {"relatorio": 14, "total": total, "desconto": desconto, "n": len(linhas)}

def relatorio_15(pedido):
    linhas = [p for p in pedido["historico"] if p["tipo"] == "tipo_15"]
    total = sum(p["valor"] for p in linhas)
    desconto = sum(p.get("desconto", 0) for p in linhas)
    return {"relatorio": 15, "total": total, "desconto": desconto, "n": len(linhas)}

def relatorio_16(pedido):
    linhas = [p for p in pedido["historico"] if p["tipo"] == "tipo_16"]
    total = sum(p["valor"] for p in linhas)
    desconto = sum(p.get("desconto", 0) for p in linhas)
    return {"relatorio": 16, "total": total, "desconto": desconto, "n": len(linhas)}

def relatorio_17(pedido):
    linhas = [p for p in pedido["historico"] if p["tipo"] == "tipo_17"]
    total = sum(p["valor"] for p in linhas)
    desconto = sum(p.get("desconto", 0) for p in linhas)
    return {"relatorio": 17, "total": total, "desconto": desconto, "n": len(linhas)}

def relatorio_18(pedido):
    linhas = [p for p in pedido["historico"] if p["tipo"] == "tipo_18"]
    total = sum(p["valor"] for p in linhas)
    desconto = sum(p.get("desconto", 0) for p in linhas)
    return {"relatorio": 18, "total": total, "desconto": desconto, "n": len(linhas)}

def relatorio_19(pedido):
    linhas = [p for p in pedido["historico"] if p["tipo"] == "tipo_19"]
    total = sum(p["valor"] for p in linhas)
    desconto = sum(p.get("desconto", 0) for p in linhas)
    return {"relatorio": 19, "total": total, "desconto": desconto, "n": len(linhas)}

def relatorio_20(pedido):
    linhas = [p for p in pedido["historico"] if p["tipo"] == "tipo_20"]
    total = sum(p["valor"] for p in linhas)
    desconto = sum(p.get("desconto", 0) for p in linhas)
    return {"relatorio": 20, "total": total, "desconto": desconto, "n": len(linhas)}

def relatorio_21(pedido):
    linhas = [p for p in pedido["historico"] if p["tipo"] == "tipo_21"]
    total = sum(p["valor"] for p in linhas)
    desconto = sum(p.get("desconto", 0) for p in linhas)
    return {"relatorio": 21, "total": total, "desconto": desconto, "n": len(linhas)}

def relatorio_22(pedido):
    linhas = [p for p in pedido["historico"] if p["tipo"] == "tipo_22"]
    total = sum(p["valor"] for p in linhas)
    desconto = sum(p.get("desconto", 0) for p in linhas)
    return {"relatorio": 22, "total": total, "desconto": desconto, "n": len(linhas)}

def relatorio_23(pedido):
    linhas = [p for p in pedido["historico"] if p["tipo"] == "tipo_23"]
    total = sum(p["valor"] for p in linhas)
    desconto = sum(p.get("desconto", 0) for p in linhas)
    return {"relatorio": 23, "total": total, "desconto": desconto, "n": len(linhas)}

def relatorio_24(pedido):
    linhas = [p for p in pedido["historico"] if p["tipo"] == "tipo_24"]
    total = sum(p["valor"] for p in linhas)
    desconto = sum(p.get("desconto", 0) for p in linhas)
    return {"relatorio": 24, "total": total, "desconto": desconto, "n": len(linhas)}

def relatorio_25(pedido):
    linhas = [p for p in pedido["historico"] if p["tipo"] == "tipo_25"]
    total = sum(p["valor"] for p in linhas)
    desconto = sum(p.get("desconto", 0) for p in linhas)
    return {"relatorio": 25, "total": total, "desconto": desconto, "n": len(linhas)}

def relatorio_26(pedido):
    linhas = [p for p in pedido["historico"] if p["tipo"] == "tipo_26"]
    total = sum(p["valor"] for p in linhas)
    desconto = sum(p.get("desconto", 0) for p in linhas)
    return {"relatorio": 26, "total": total, "desconto": desconto, "n": len(linhas)}

def relatorio_27(pedido):
    linhas = [p for p in pedido["historico"] if p["tipo"] == "tipo_27"]
    total = sum(p["valor"] for p in linhas)
    desconto = sum(p.get("desconto", 0) for p in linhas)
    return {"relatorio": 27, "total": total, "desconto": desconto, "n": len(linhas)}

def relatorio_28(pedido):
    linhas = [p for p in pedido["historico"] if p["tipo"] == "tipo_28"]
    total = sum(p["valor"] for p in linhas)
    desconto = sum(p.get("desconto", 0) for p in linhas)
    return {"relatorio": 28, "total": total, "desconto": desconto, "n": len(linhas)}

def relatorio_29(pedido):
    linhas = [p for p in pedido["historico"] if p["tipo"] == "tipo_29"]
    total = sum(p["valor"] for p in linhas)
    desconto = sum(p.get("desconto", 0) for p in linhas)
    return {"relatorio": 29, "total": total, "desconto": desconto, "n": len(linhas)}

def relatorio_30(pedido):
    linhas = [p for p in pedido["historico"] if p["tipo"] == "tipo_30"]
    total = sum(p["valor"] for p in linhas)
    desconto = sum(p.get("desconto", 0) for p in linhas)
    return {"relatorio": 30, "total": total, "desconto": desconto, "n": len(linhas)}
