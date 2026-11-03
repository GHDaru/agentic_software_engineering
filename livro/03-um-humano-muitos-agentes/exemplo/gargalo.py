#!/usr/bin/env python3
"""gargalo.py — onde a vazão de um time de agentes para quando a capacidade deixa de ser o limite.

Simulação determinística (sem sorteio) de um dia de trabalho de um humano que rege N agentes.
Cada agente entrega, em ritmo fixo, um item que precisa de UMA decisão humana (aprovar a spec,
aceitar o merge, responder um pedido de decisão). O humano é um servidor só, atende em ordem de
chegada e gasta um tempo fixo por decisão. Nada aqui chama modelo de IA: o que se mede é a fila
que se forma na frente da única coisa que não se paraleliza, o julgamento de quem responde
(axioma A1 do Maestro: a intenção é humana).

Saída: uma tabela por cenário com fatias produzidas, fatias liberadas por decisão no dia, fatias
que dormem na fila, espera humana média e máxima (minutos entre o item ficar pronto e a decisão começar) e a
ocupação do humano. Três cenários:

  A  mais agentes, mesmo gate     — a vazão satura na capacidade do humano; a espera explode
  B  mesmo time, gate mais barato — o que o capítulo chama de "barateie o gate"
  C  paralelizar DENTRO da feature — várias fatias, uma decisão só sobre o lote

Uso:  python gargalo.py          Só biblioteca padrão; Python 3.8+.
Saída: 0 sempre que a simulação roda; o que importa é comparar com saida-esperada-gargalo.txt.
"""

DIA = 480  # minutos de atenção do humano num dia (8 h)


def chegadas(n_agentes, periodo, lote=1):
    """Instantes (min) em que um item fica pronto para decisão.

    Cada agente entrega um item a cada `periodo` minutos; os agentes começam defasados
    (periodo/n) para não chegarem todos juntos. Com `lote` > 1, as entregas de `lote`
    agentes da mesma feature viram UMA decisão, tomada quando a última fatia fica pronta.
    """
    tempos = []
    for i in range(n_agentes):
        t = i * periodo / n_agentes
        while t < DIA:
            tempos.append(t)
            t += periodo
    tempos.sort()
    if lote == 1:
        return tempos
    return [max(tempos[k:k + lote]) for k in range(0, len(tempos) - lote + 1, lote)]


def simula(n_agentes, periodo, custo_gate, lote=1):
    """Fila de um servidor só, FIFO, que trabalha até o fim do dia."""
    livre = 0.0
    esperas, ocupado, decididos = [], 0.0, 0
    fila_no_fim = []
    for t in chegadas(n_agentes, periodo, lote):
        inicio = max(t, livre)
        if inicio >= DIA:  # o dia acabou antes de o humano chegar a este item
            fila_no_fim.append(DIA - t)
            continue
        esperas.append(inicio - t)
        livre = inicio + custo_gate
        ocupado += custo_gate
        decididos += 1
    # contado em FATIAS de trabalho: com lote, uma decisão libera `lote` fatias
    return {
        "produzidos": (decididos + len(fila_no_fim)) * lote,
        "decididos": decididos * lote,
        "decisoes": decididos,
        "na_fila": len(fila_no_fim) * lote,
        "espera_media": sum(esperas) / len(esperas) if esperas else 0.0,
        "espera_max": max(esperas + fila_no_fim) if (esperas or fila_no_fim) else 0.0,
        "ocupacao": min(ocupado, DIA) / DIA,
    }


def linha(rotulo, r):
    return (f"  {rotulo:<28} {r['produzidos']:>4} {r['decididos']:>5} {r['na_fila']:>5}"
            f" {r['espera_media']:>8.1f} {r['espera_max']:>8.1f} {r['ocupacao']:>6.0%}")


CABECALHO = (f"  {'cenário':<28} {'prod':>4} {'decid':>5} {'fila':>5}"
             f" {'esp.méd':>8} {'esp.máx':>8} {'ocup':>6}")


def main():
    periodo, custo = 60, 12  # cada agente entrega 1 item/hora; cada decisão custa 12 min
    capacidade = DIA // custo
    print(f"== um humano, {DIA} min de atenção, {custo} min por decisão"
          f" (capacidade: {capacidade} decisões/dia)")
    print("   cada agente entrega 1 fatia por hora; colunas em fatias; espera em minutos\n")

    print("A  mais agentes, mesmo gate")
    print(CABECALHO)
    for n in (1, 2, 4, 5, 8, 16):
        print(linha(f"{n:>2} agente(s)", simula(n, periodo, custo)))

    print("\nB  8 agentes, gate mais barato (critério verificável, ação reversível)")
    print(CABECALHO)
    for c in (12, 8, 6):
        print(linha(f"gate de {c:>2} min", simula(8, periodo, c)))

    print("\nC  8 agentes, paralelizar DENTRO da feature (uma decisão por lote de fatias)")
    print(CABECALHO)
    print(linha("1 decisão por fatia (12)", simula(8, periodo, 12, lote=1)))
    c = simula(8, periodo, 20, lote=4)
    print(linha("1 decisão por 4 fatias (20)", c))
    print(f"  (no lote: {c['decisoes']} decisões de 20 min liberam {c['decididos']} fatias)")

    a8, a4 = simula(8, periodo, custo), simula(4, periodo, custo)
    print("\n== leitura")
    print(f"  de 4 para 8 agentes a produção dobra ({a4['produzidos']} → {a8['produzidos']}),"
          f" as liberadas vão de {a4['decididos']} a {a8['decididos']}"
          f" e {a8['na_fila']} fatias dormem na fila")
    print(f"  o teto é o humano: {capacidade} decisões/dia, com 4, 8 ou 16 agentes")


if __name__ == "__main__":
    main()
