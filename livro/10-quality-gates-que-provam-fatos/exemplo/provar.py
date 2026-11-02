"""Prova por mutação de portões: separa portão de decoração.

Para cada propriedade de casos.json e cada portão de portoes.py:
  - a fixture POSITIVA tem de passar        (senão: o portão nunca fica verde)
  - cada fixture LEGÍTIMA tem de passar     (senão: falso vermelho — aprende-se a ignorá-lo)
  - cada MUTAÇÃO tem de reprovar            (senão: a mutação sobreviveu — o portão mede proxy)

Um portão que cumpre as três é PORTÃO. Qualquer falha o rebaixa a DECORAÇÃO.

Uso:
  python3 provar.py               prova os seis portões; sai 1 se algum for decoração
  python3 provar.py --so fato     prova só os que medem o fato; sai 0 se todos forem portão
  python3 provar.py --so ingenua  prova só os que medem o proxy
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from portoes import PORTOES  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def rodar(portao, caso):
    if "consumo" in caso:
        return portao(caso["entrada"], caso["consumo"])
    return portao(caso["entrada"])


def provar(prop_id, prop, nome, portao):
    falhas = []
    for c in prop["positiva"]:
        if not rodar(portao, c):
            falhas.append(f"positiva '{c['nome']}' ficou vermelha")
    for c in prop["legitimas"]:
        if not rodar(portao, c):
            falhas.append(f"falso vermelho em '{c['nome']}'")
    mortas = 0
    for c in prop["mutacoes"]:
        if rodar(portao, c):
            falhas.append(f"mutação sobreviveu: '{c['nome']}'")
        else:
            mortas += 1
    total = len(prop["mutacoes"])
    veredito = "PORTÃO" if not falhas else "DECORAÇÃO"
    print(f"  {prop_id}/{nome:<8} mutações mortas {mortas}/{total}  →  {veredito}")
    for f in falhas:
        print(f"      ✗ {f}")
    return not falhas


def main(argv):
    so = None
    if "--so" in argv:
        so = argv[argv.index("--so") + 1]
        if so not in ("fato", "ingenua"):
            print("✗ --so aceita 'fato' ou 'ingenua'")
            return 2
    casos = json.loads(Path(__file__).with_name("casos.json").read_text(encoding="utf-8"))
    portoes, decoracoes = 0, 0
    for prop_id, por_nome in PORTOES.items():
        prop = casos[prop_id]
        print(f"{prop_id} — {prop['propriedade']}")
        for nome, portao in por_nome.items():
            if so and nome != so:
                continue
            portoes += 1
            if not provar(prop_id, prop, nome, portao):
                decoracoes += 1
    print(f"resumo: {portoes} portões provados, {portoes - decoracoes} portão(ões), "
          f"{decoracoes} decoração(ões)")
    return 1 if decoracoes else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
