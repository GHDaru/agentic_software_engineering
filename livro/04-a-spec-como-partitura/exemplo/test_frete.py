"""test_frete.py — os testes leem os números DA SPEC, não do código.

A spec lida vem da variável de ambiente SPEC (padrão: spec.md). Cada teste se chama
test_frN_* para que `partitura.py rastreio` ligue requisito e teste nos dois sentidos.
Runner próprio, sem tempo na saída, para a saída esperada do README ser estável.
"""
import os
import sys

from frete import frete
from partitura import valor

SPEC = os.environ.get("SPEC", "spec.md")


def test_fr1_frete_zero_a_partir_do_limite():
    limite = valor(SPEC, "FR1")
    obtido = frete(limite, "sul")
    assert obtido == 0.00, f"subtotal {limite:.2f}: esperado 0.00, obtido {obtido:.2f}"


def test_fr2_tabela_abaixo_do_limite():
    limite = valor(SPEC, "FR2")
    obtido = frete(round(limite - 0.01, 2), "sul")
    assert obtido == 25.00, f"subtotal {limite - 0.01:.2f}: esperado 25.00, obtido {obtido:.2f}"


def test_fr3_subtotal_negativo_recusado():
    try:
        frete(-1.00, "sul")
    except ValueError:
        return
    raise AssertionError("subtotal -1.00 foi aceito")


def main():
    for s in (sys.stdout,):
        try:
            s.reconfigure(encoding="utf-8")
        except AttributeError:
            pass
    testes = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_")]
    falhas = 0
    print(f"testes contra {SPEC}")
    for nome, f in testes:
        try:
            f()
            print(f"  ok      {nome}")
        except AssertionError as e:
            falhas += 1
            print(f"  FALHOU  {nome}: {e}")
    if falhas:
        print(f"✗ {falhas} de {len(testes)} falharam: a spec andou e o código ficou para trás.")
        return 1
    print(f"✓ {len(testes)} de {len(testes)} passaram.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
