#!/usr/bin/env python3
"""fila.py — a fila de decisões de um humano que rege muitos agentes, derivada de um registro.

O padrão do capítulo 3 em miniatura: o estado NÃO é digitado; é calculado de um registro
só-acréscimo de eventos (pedidos de decisão e rulings). O script projeta, não decide:

  E   endereço: 'nome · ref · projeto', resolvido para UMA sessão viva; nome solto, ref velho,
      ref de outra sessão ou sessão caída são recusados (endereço ambíguo não se adivinha)
  P1  pedido de decisão sem prazo é recusado
  P2  pedido sem opções ou sem recomendação é recusado
  R1  ruling para pedido inexistente ou já respondido é recusado
  R2  ruling só tem autor humano (portão do regente: o agente lê, não registra)
  R3  ruling sem destino resolvível é recusado (a resposta precisa voltar a alguém)
  R4  hora do ruling anterior à do pedido é recusada
  N   não existe "dispensar": a pergunta fica na fila até ter ruling
  A   o registro é só-acréscimo: seq estritamente crescente, senão o script se recusa a projetar

Depois projeta a frase-chave ("você tem N decisões esperando, a mais antiga há ...") em três
instantes e mede a ESPERA HUMANA de cada pedido respondido. Por fim prova, por mutação, que a
guarda A acusa um registro reescrito.

Uso:  python fila.py        Só biblioteca padrão; Python 3.8+.
Saída: 0 = todo evento teve o veredito esperado e a mutação foi acusada; 1 = não.
"""
import copy
import json
import sys
from datetime import datetime
from pathlib import Path

AQUI = Path(__file__).resolve().parent
FMT = "%Y-%m-%dT%H:%M"


def hora(ts):
    return datetime.strptime(ts, FMT)


def duracao(minutos):
    h, m = divmod(int(round(minutos)), 60)
    return f"{h} h {m:02d} min" if h else f"{m} min"


def resolve(endereco, roster):
    """Devolve (sessao, None) ou (None, motivo). Nunca escolhe 'a mais provável'."""
    partes = [p.strip() for p in (endereco or "").split("·")]
    if len(partes) != 3 or not all(partes):
        return None, f"endereço incompleto '{endereco}': sem 'nome · ref · projeto' não se adivinha"
    nome, ref, projeto = partes
    achadas = [s for s in roster["sessoes"] if s["ref"] == ref]
    if not achadas:
        return None, f"ref '{ref}' não existe (o ref muda quando a sessão reinicia)"
    s = achadas[0]
    if s["nome"] != nome or s["projeto"] != projeto:
        return None, (f"ref '{ref}' é de '{s['nome']} · {s['projeto']}',"
                      f" não de '{nome} · {projeto}'")
    if not s["viva"]:
        return None, f"'{nome} · {ref}' está caída"
    return s, None


def confere_ordem(eventos):
    """Guarda A: o registro só cresce. Devolve o motivo da recusa, ou None."""
    anterior = 0
    for e in eventos:
        if e["seq"] <= anterior:
            return f"seq {e['seq']} depois de {anterior}: o registro foi reescrito, não acrescido"
        anterior = e["seq"]
    return None


def julga(eventos, roster):
    """Aplica as regras evento a evento. Devolve (vereditos, pedidos aceitos, rulings aceitos)."""
    humanos = set(roster["humanos"])
    pedidos, rulings, vereditos = {}, {}, []
    for e in eventos:
        motivos = []
        if e["tipo"] == "pedido":
            _, m = resolve(e.get("de"), roster)
            if m:
                motivos.append(f"E {m}")
            if not e.get("prazo"):
                motivos.append("P1 pedido sem prazo: sem prazo não há como ordenar nem envelhecer")
            if not e.get("opcoes") or not e.get("recomendacao"):
                motivos.append("P2 pedido sem opções ou sem recomendação")
            if not motivos:
                pedidos[e["id"]] = e
        elif e["tipo"] == "ruling":
            p = pedidos.get(e["pedido"])
            if p is None:
                motivos.append(f"R1 pedido '{e['pedido']}' não está na fila")
            elif e["pedido"] in rulings:
                motivos.append(f"R1 pedido '{e['pedido']}' já tem ruling")
            if e.get("autor") not in humanos:
                motivos.append(f"R2 '{e.get('autor')}' não é humano: portão do regente")
            if not e.get("destino"):
                motivos.append("R3 ruling sem destino: a resposta não volta a ninguém")
            else:
                _, m = resolve(e["destino"], roster)
                if m:
                    motivos.append(f"R3 destino: {m}")
            if p is not None and hora(e["ts"]) < hora(p["ts"]):
                motivos.append("R4 ruling anterior ao pedido: hora digitada")
            if not motivos:
                rulings[e["pedido"]] = e
        else:
            motivos.append(f"N '{e['tipo']}' não existe: responda ou devolva, nunca dispense")
        veredito = "recusado" if motivos else "aceito"
        vereditos.append((e, veredito, motivos))
    return vereditos, pedidos, rulings


def frase_chave(pedidos, rulings, agora):
    abertos = [p for pid, p in pedidos.items()
               if hora(p["ts"]) <= agora
               and not (pid in rulings and hora(rulings[pid]["ts"]) <= agora)]
    if not abertos:
        return "fila vazia: nenhuma decisão esperando por você", []
    mais_velho = min(abertos, key=lambda p: hora(p["ts"]))
    idade = (agora - hora(mais_velho["ts"])).total_seconds() / 60
    n = len(abertos)
    plural = "decisões esperando" if n > 1 else "decisão esperando"
    return (f"você tem {n} {plural}; a mais antiga ({mais_velho['id']}) há {duracao(idade)}",
            sorted(abertos, key=lambda p: hora(p["prazo"])))


def main():
    roster = json.loads((AQUI / "sessoes.json").read_text(encoding="utf-8"))
    linhas = (AQUI / "eventos.jsonl").read_text(encoding="utf-8").splitlines()
    eventos = [json.loads(l) for l in linhas if l.strip()]

    falha = confere_ordem(eventos)
    if falha:
        print(f"✗ A {falha}")
        return 1

    vereditos, pedidos, rulings = julga(eventos, roster)
    ok = 0
    print("== eventos do registro (só-acréscimo)")
    for e, v, motivos in vereditos:
        alvo = e.get("id") or e.get("pedido")
        marca = "✓" if v == e["esperado"] else "✗"
        ok += v == e["esperado"]
        print(f"  {marca} seq {e['seq']:>2} {e['ts'][11:]} {e['tipo']:<9} {alvo}: {v}"
              f" (esperado: {e['esperado']})")
        for m in motivos:
            print(f"      - {m}")

    print("\n== frase-chave (derivada da fila, nunca digitada)")
    for instante in ("2026-10-16T14:00", "2026-10-16T14:35", "2026-10-16T16:00"):
        agora = hora(instante)
        frase, abertos = frase_chave(pedidos, rulings, agora)
        print(f"  {instante[11:]}  {frase}")
        for p in abertos:
            atraso = (agora - hora(p["prazo"])).total_seconds() / 60
            prazo = (f"prazo vencido há {duracao(atraso)}" if atraso > 0
                     else f"prazo em {duracao(-atraso)}")
            print(f"           {p['id']} · {prazo} · destrava: {p['destrava']} · de {p['de']}")

    print("\n== espera humana (do pedido ao ruling)")
    esperas, estouros = [], 0
    for pid in sorted(rulings):
        p, r = pedidos[pid], rulings[pid]
        espera = (hora(r["ts"]) - hora(p["ts"])).total_seconds() / 60
        estourou = hora(r["ts"]) > hora(p["prazo"])
        estouros += estourou
        esperas.append(espera)
        print(f"  {pid}  {p['ts'][11:]} → {r['ts'][11:]}  {duracao(espera):>12}"
              f"{'  (prazo estourado)' if estourou else ''}")
    media = sum(esperas) / len(esperas)
    print(f"  média {duracao(media)} · máxima {duracao(max(esperas))}"
          f" · {estouros} de {len(esperas)} respondidos depois do prazo")

    print("\n== prova por mutação: reescrever uma linha do registro")
    mutado = copy.deepcopy(eventos)
    mutado[4]["seq"] = 2  # alguém "corrige" o pedido D-04 reescrevendo-o no lugar do D-02
    acusou = confere_ordem(mutado) is not None
    print(f"  {'✓' if acusou else '✗'} guarda A {'acusou' if acusou else 'NÃO acusou'}:"
          f" {confere_ordem(mutado)}")

    total = len(vereditos)
    print(f"\nresultado: {ok}/{total} eventos com o veredito esperado;"
          f" mutação acusada: {1 if acusou else 0}/1")
    return 0 if ok == total and acusou else 1


if __name__ == "__main__":
    sys.exit(main())
