#!/usr/bin/env python3
"""aprende.py — as três engrenagens de uma organização que aprende sem inchar.

Exemplo do capítulo 14 do livro "Engenharia de Software Orientada por Agentes".
Sem dependência externa; Python 3.8+.

Três verificações, cada uma reproduzindo a forma de um portão real do Maestro (19823c2):

  gatilho    a retrospectiva é cobrada pela DÍVIDA de achados abertos, não pelo calendário
             (forma do scripts/check-retro.sh: >= 4 abertos, ou um aberto há >= 6 ciclos).
             Fechar é ligação ESTRUTURAL (campo "fecha"), nunca prosa.
  anexar     o índice de decisões só cresce: a versão nova tem de começar pela antiga,
             linha a linha (forma do guard-immutables.py + record-decision.sh).
  artefatos  um artefato sobrevive por consumo (tem consumidor e falha alto quando velho)
             ou por imutabilidade; o resto apodrece (teorema T5, corolário C9).

Uso:
  python3 aprende.py demo                         # roda os cenários do capítulo
  python3 aprende.py gatilho  <indice.jsonl> <ciclo-corrente>
  python3 aprende.py anexar   <antes.jsonl> <depois.jsonl>
  python3 aprende.py artefatos <artefatos.json> <ciclo-corrente>
Cada subcomando sai 0 (verde) ou 1 (vermelho).
"""
import json
import re
import sys
from pathlib import Path

MAX_ABERTOS = 4
MAX_IDADE = 6
AQUI = Path(__file__).resolve().parent / "dados"


# ---------------------------------------------------------------- gatilho da retro
def ler_indice(caminho):
    linhas = []
    for n, bruta in enumerate(Path(caminho).read_text(encoding="utf-8").splitlines(), 1):
        if bruta.strip():
            linhas.append(json.loads(bruta))
    return linhas


def achados_abertos(linhas):
    """Aberto = id 'achado-NNN-*', status 'aberta' e nenhuma linha com fecha == id."""
    fechados = {d["fecha"] for d in linhas if d.get("fecha")}
    abertos = []
    for d in linhas:
        i = d["id"]
        if not i.startswith("achado-") or i in fechados:
            continue
        if not d.get("status", "").startswith("aberta"):
            continue
        m = re.match(r"achado-(\d{3})", i)
        abertos.append((i, int(m.group(1)) if m else 0))
    return abertos


def gatilho(linhas, ciclo):
    abertos = achados_abertos(linhas)
    motivos = []
    if len(abertos) >= MAX_ABERTOS:
        motivos.append(f"{len(abertos)} achados abertos (limite {MAX_ABERTOS})")
    idade = max((ciclo - c for _, c in abertos), default=0)
    if idade >= MAX_IDADE:
        motivos.append(f"o mais velho tem {idade} ciclos (limite {MAX_IDADE})")
    return abertos, motivos


def relatar_gatilho(titulo, linhas, ciclo):
    abertos, motivos = gatilho(linhas, ciclo)
    print(f"  {titulo}")
    print(f"    abertos: {len(abertos)}" + (f"  ({', '.join(i for i, _ in abertos)})" if abertos else ""))
    if motivos:
        print("    VERMELHO: rode a retrospectiva — " + "; ".join(motivos))
        return 1
    print("    verde: dívida de retro sob controle")
    return 0


# ---------------------------------------------------------------- só anexar
def anexar(antes, depois):
    """Devolve lista de violações. A versão nova tem de ter a antiga como prefixo exato."""
    a = [l for l in antes.splitlines() if l.strip()]
    d = [l for l in depois.splitlines() if l.strip()]
    erros = []
    for n, linha in enumerate(a, 1):
        if n > len(d):
            erros.append(f"linha {n} apagada")
        elif d[n - 1] != linha:
            erros.append(f"linha {n} reescrita")
    ids = [json.loads(l)["id"] for l in d]
    repetidos = sorted({i for i in ids if ids.count(i) > 1})
    if repetidos:
        erros.append("id repetido: " + ", ".join(repetidos))
    return erros, len(d) - len(a)


# ---------------------------------------------------------------- artefatos (T5)
def classificar(art, ciclo):
    if art.get("imutavel"):
        if art.get("commits_no_merito", 1) > 1:
            return "REESCRITO", "imutável por declaração, mas o mérito mudou depois de nascer"
        return "vivo (imutável)", "descreve um instante; pode ser superado, nunca fica velho"
    consumidor = art.get("consumidor")
    forca = art.get("falha_quando_velho")
    atraso = ciclo - art.get("ultimo_ciclo", ciclo)
    if consumidor and forca:
        return "vivo (consumido)", f"consumidor: {consumidor}; quando velho: {forca}"
    if not consumidor:
        return "PODAR", "ninguém consome — candidato a poda (YAGNI)"
    return "APODRECENDO", f"consumidor sem cobrança; {atraso} ciclo(s) atrás do projeto"


def relatar_artefatos(lista, ciclo):
    ruins = 0
    largura = max(len(a["nome"]) for a in lista)
    for a in lista:
        estado, porque = classificar(a, ciclo)
        if estado.startswith(("PODAR", "APODRECENDO", "REESCRITO")):
            ruins += 1
        print(f"    {a['nome']:<{largura}}  {estado:<17} {porque}")
    return ruins


# ---------------------------------------------------------------- demo
def demo():
    falhas_esperadas = 0
    print("1. Gatilho da retrospectiva (dívida, não calendário)")
    base = ler_indice(AQUI / "indice.jsonl")
    r = relatar_gatilho("a) índice como está, ciclo corrente 034", base, 34)
    falhas_esperadas += r
    prosa = base + [json.loads((AQUI / "fechamento-em-prosa.jsonl").read_text(encoding="utf-8"))]
    r = relatar_gatilho("b) + linha que 'fecha' em prosa (id novo, sem campo fecha)", prosa, 34)
    falhas_esperadas += r
    estrutural = base + [json.loads(l) for l in (AQUI / "fechamento-estrutural.jsonl")
                         .read_text(encoding="utf-8").splitlines() if l.strip()]
    r = relatar_gatilho("c) + linhas com o campo fecha (retro executada)", estrutural, 34)
    falhas_esperadas += r

    print("\n2. Índice só-anexar (corrigir é acrescentar)")
    antes = (AQUI / "indice.jsonl").read_text(encoding="utf-8")
    for rotulo, arq in [("a) anexar uma linha de fechamento", "fechamento-estrutural.jsonl"),
                        ("b) 'corrigir' editando a linha antiga", None)]:
        if arq:
            depois = antes + (AQUI / arq).read_text(encoding="utf-8")
        else:
            depois = antes.replace('"status":"aberta"', '"status":"fechada"', 1)
        erros, novas = anexar(antes, depois)
        print(f"  {rotulo}")
        if erros:
            print("    RECUSADO: " + "; ".join(erros))
            falhas_esperadas += 1
        else:
            print(f"    aceito: {novas} linha(s) nova(s), nenhuma antiga tocada")

    print("\n3. Artefatos: sobrevive o consumido ou o imutável (T5)")
    lista = json.loads((AQUI / "artefatos.json").read_text(encoding="utf-8"))
    ruins = relatar_artefatos(lista, 34)
    print(f"  resumo: {len(lista)} artefatos, {ruins} pedem decisão (podar, cobrar ou superar)")

    print(f"\nvermelhos esperados no roteiro: {falhas_esperadas} (1a, 1b, 2b) — todos desejados")
    return 0 if falhas_esperadas == 3 else 1


def main(argv):
    if len(argv) < 2 or argv[1] == "demo":
        return demo()
    cmd = argv[1]
    if cmd == "gatilho" and len(argv) == 4:
        return relatar_gatilho(argv[2], ler_indice(argv[2]), int(argv[3]))
    if cmd == "anexar" and len(argv) == 4:
        erros, novas = anexar(Path(argv[2]).read_text(encoding="utf-8"),
                              Path(argv[3]).read_text(encoding="utf-8"))
        print("RECUSADO: " + "; ".join(erros) if erros else f"aceito: {novas} linha(s) nova(s)")
        return 1 if erros else 0
    if cmd == "artefatos" and len(argv) == 4:
        lista = json.loads(Path(argv[2]).read_text(encoding="utf-8"))
        return 1 if relatar_artefatos(lista, int(argv[3])) else 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    sys.exit(main(sys.argv))
