"""dividir.py — onde cortar para que agentes em paralelo não colidam (capítulo 6).

Só biblioteca padrão do Python 3.8+. Subcomandos:

  colisao  <plano.json>                 acusa arquivo com dois escritores, conceito com dois
                                         donos e contrato consumido sem dono (exit 1 se houver)
  ondas    <plano.json>                 ordena as fatias: o dono do contrato antes de quem consome
  custo    <plano.json> [--handoff N]   tempo sequencial × paralelo, com o custo de coordenação
  autonomia <casos.json>                a menor autonomia que resolve, caso a caso
  numerar  <linhas.json>                numeração alocada em linhas paralelas: colisão e recusa

Formato do plano: {"nome", "criterio", "custo_handoff",
                   "fatias": [{"id", "escreve": [...], "define": [...], "consome": [...],
                               "custo": n}]}
"""
import json
import sys
from collections import defaultdict


def carregar(caminho):
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------- colisão
def colisoes(plano):
    escritores, donos, consumidores = defaultdict(list), defaultdict(list), defaultdict(list)
    for f in plano["fatias"]:
        for a in f.get("escreve", []):
            escritores[a].append(f["id"])
        for c in f.get("define", []):
            donos[c].append(f["id"])
        for c in f.get("consome", []):
            consumidores[c].append(f["id"])
    externos = set(plano.get("contratos_existentes", []))
    achados = []
    for a, quem in sorted(escritores.items()):
        if len(quem) > 1:
            achados.append(("arquivo com dois escritores", a, quem))
    for c, quem in sorted(donos.items()):
        if len(quem) > 1:
            achados.append(("conceito com mais de um dono", c, quem))
    for c, quem in sorted(consumidores.items()):
        if c not in donos and c not in externos:
            achados.append(("contrato consumido sem dono", c, quem))
    return achados


def cmd_colisao(caminho):
    plano = carregar(caminho)
    print(f"plano: {plano['nome']}  (critério do corte: {plano['criterio']})")
    achados = colisoes(plano)
    for tipo, alvo, quem in achados:
        print(f"  ✗ {tipo}: {alvo}  ← {', '.join(quem)}")
    if achados:
        print(f"✗ {len(achados)} colisão(ões): a reconciliação vai custar o que o paralelo economizou.")
        return 1
    print(f"✓ {len(plano['fatias'])} fatias, cada arquivo e cada conceito com um dono só.")
    return 0


# ---------------------------------------------------------------- ondas
def ondas(plano):
    dono = {}
    for f in plano["fatias"]:
        for c in f.get("define", []):
            dono.setdefault(c, f["id"])
    deps = {f["id"]: {dono[c] for c in f.get("consome", []) if c in dono and dono[c] != f["id"]}
            for f in plano["fatias"]}
    feitas, resultado = set(), []
    while len(feitas) < len(deps):
        onda = sorted(i for i, d in deps.items() if i not in feitas and d <= feitas)
        if not onda:
            resto = sorted(set(deps) - feitas)
            raise ValueError(f"dependência circular entre {', '.join(resto)}")
        resultado.append(onda)
        feitas |= set(onda)
    return resultado, deps


def cmd_ondas(caminho):
    plano = carregar(caminho)
    try:
        lista, deps = ondas(plano)
    except ValueError as e:
        print(f"✗ {e}: nenhuma ordem serve; recorte antes de distribuir.")
        return 1
    for n, onda in enumerate(lista, 1):
        detalhe = [f"{i} (espera {', '.join(sorted(deps[i]))})" if deps[i] else i for i in onda]
        print(f"  onda {n}: {' · '.join(detalhe)}")
    print(f"✓ {len(lista)} onda(s); dentro de uma onda as fatias correm em paralelo.")
    return 0


# ---------------------------------------------------------------- custo
def custo(plano, handoff=None):
    h = plano.get("custo_handoff", 1) if handoff is None else handoff
    por_id = {f["id"]: f for f in plano["fatias"]}
    sequencial = sum(f["custo"] for f in plano["fatias"])
    try:
        lista, deps = ondas(plano)
    except ValueError:
        lista, deps = [sorted(por_id)], {i: set() for i in por_id}
    caminho = sum(max(por_id[i]["custo"] for i in onda) for onda in lista)
    passagens = sum(len(d) for d in deps.values())
    cols = colisoes(plano)
    # reconciliar uma colisão = refazer as fatias envolvidas (nenhum reduce salva o corte errado)
    retrabalho = sum(sum(por_id[i]["custo"] for i in set(quem)) for _, _, quem in cols)
    coordenacao = passagens * h + retrabalho
    paralelo = caminho + coordenacao
    return sequencial, caminho, passagens, len(cols), retrabalho, coordenacao, paralelo, h


def cmd_custo(caminho, handoff=None):
    plano = carregar(caminho)
    seq, cam, pas, col, ret, coord, par, h = custo(plano, handoff)
    print(f"plano: {plano['nome']}")
    print(f"  um agente, em sequência ......... {seq}")
    print(f"  caminho crítico das ondas ....... {cam}")
    print(f"  passagens entre fatias .......... {pas} × {h} = {pas * h}")
    print(f"  colisões → retrabalho ........... {col} colisão(ões) = {ret}")
    print(f"  paralelo (caminho + coordenação)  {par}")
    print(f"  overhead de coordenação ......... {coord}/{par} = {100 * coord // par if par else 0}% do tempo paralelo")
    if par < seq:
        print(f"✓ paralelizar compensa: {seq} → {par}")
        return 0
    print(f"✗ paralelizar NÃO compensa: {par} ≥ {seq}. Um agente só, ou um corte melhor.")
    return 1


# ---------------------------------------------------------------- autonomia
def menor_autonomia(c):
    """Sobe um degrau só quando o anterior não resolve; o autônomo exige evidência."""
    if c.get("pede_autonomo") and not c.get("simples_falhou_com_evidencia"):
        return "encadeamento", "autônomo pedido sem evidência de que o simples falhou: recusado"
    if c.get("simples_falhou_com_evidencia"):
        return "autônomo (com guarda-corpos)", f"evidência: {c['simples_falhou_com_evidencia']}"
    if not c.get("corte_predefinivel", True):
        return "orquestrador-trabalhadores", "as fatias só se conhecem lendo o problema; o reduce é humano"
    if c.get("partes_independentes") and c.get("fronteira_declarada"):
        base = ("paralelização", "fatias por fronteira, cada uma com dono e contrato")
    elif c.get("partes_independentes"):
        base = ("encadeamento", "partes 'independentes' sem fronteira declarada: corte antes de paralelizar")
    elif c.get("entradas_de_tipos_diferentes"):
        base = ("roteamento", "classificar a entrada e escolher o caminho fixo")
    else:
        base = ("encadeamento", "passos conhecidos: fluxo fixo, barato e depurável")
    if c.get("criterio_executavel"):
        return base[0] + " + avaliador-otimizador", base[1] + "; o laço para quando o critério passa"
    return base


def cmd_autonomia(caminho):
    casos = carregar(caminho)
    for c in casos:
        padrao, motivo = menor_autonomia(c)
        print(f"  {c['caso']}")
        print(f"    → {padrao}  ({motivo})")
    return 0


# ---------------------------------------------------------------- numerar
def cmd_numerar(caminho):
    d = carregar(caminho)
    usados = defaultdict(list)
    for linha, pastas in d["linhas"].items():
        for p in pastas:
            usados[p[:3]].append(f"{linha}:{p}")
    colid = {n: q for n, q in sorted(usados.items()) if len(q) > 1}
    for n, quem in colid.items():
        print(f"  ✗ número {n} alocado {len(quem)} vezes: {' × '.join(quem)}")
    for pedido in d.get("resolver", []):
        alvos = usados.get(pedido, [])
        if len(alvos) == 1:
            print(f"  ✓ 'ciclo {pedido}' → {alvos[0]}")
        elif not alvos:
            print(f"  ✗ 'ciclo {pedido}' → recusado: nenhum destino")
        else:
            print(f"  ✗ 'ciclo {pedido}' → recusado: {len(alvos)} destinos (endereço ambíguo não se resolve, se recusa)")
    # renumeração: a linha principal fica; a outra recebe o próximo número livre, na ordem dada
    principal = d["principal"]
    ocupados = {int(p[:3]) for p in d["linhas"][principal]}
    prox, mapa = max(ocupados) + 1, []
    for linha, pastas in d["linhas"].items():
        if linha == principal:
            continue
        for p in pastas:
            while prox in ocupados:
                prox += 1
            mapa.append((p, f"{prox:03d}{p[3:]}"))
            ocupados.add(prox)
    print(f"  renumeração (a linha '{principal}' fica; a outra ganha o próximo livre):")
    for velho, novo in mapa:
        print(f"    {velho:24s} → {novo}")
    return 1 if colid else 0


def main(argv):
    if len(argv) < 3:
        print(__doc__, file=sys.stderr)
        return 2
    cmd, arq = argv[1], argv[2]
    if cmd == "colisao":
        return cmd_colisao(arq)
    if cmd == "ondas":
        return cmd_ondas(arq)
    if cmd == "custo":
        h = int(argv[argv.index("--handoff") + 1]) if "--handoff" in argv else None
        return cmd_custo(arq, h)
    if cmd == "autonomia":
        return cmd_autonomia(arq)
    if cmd == "numerar":
        return cmd_numerar(arq)
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
