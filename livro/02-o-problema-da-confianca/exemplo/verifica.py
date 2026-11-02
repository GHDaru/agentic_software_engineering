#!/usr/bin/env python3
"""verifica.py — confere o fechamento de um ciclo contra as regras de confiança do capítulo 2.

Não há modelo de IA aqui: o que se verifica é a ESTRUTURA que torna um resultado confiável,
não o resultado. Cinco regras, cada uma com a origem no texto:

  R0  configuração: papel que julga não tem ferramenta de escrita (corolário C3)
  R1  quem executou não é quem revisou (teorema T2)
  R2  quem revisou é um papel que julga (C3, aplicado ao registro)
  R3  a revisão foi feita em contexto fresco (T2, pelo lado do axioma A3)
  R4  caixa marcada tem evidência, e "pendente" não é evidência (ciclos 042, 043, 061, 062)
  R5  o gate tem dono humano, ou uma delegação escrita com crítico fresco (A2; ADR 0026)

Uso:  python verifica.py            (roda os registros de registros/ e a prova por mutação)
Saída: 0 = todo registro teve o veredito esperado e a mutação foi acusada; 1 = não.
Só biblioteca padrão; Python 3.8+.
"""
import copy
import json
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ESCRITA = {"Write", "Edit"}
# Evidência que só declara ausência: vazio, marcador de gerador (<...> ou [...]) ou uma
# palavra de pendência SOZINHA. A frase "pendente" no meio de um parecer real não reprova
# (o erro espelhado que o ciclo 063 do Maestro evitou).
AUSENCIA = re.compile(r"^\s*(pendente|a fazer|todo|tbd|ok|feito)\s*\.?\s*$", re.I)


def placeholder(texto):
    t = (texto or "").strip()
    return t == "" or t[0] in "<[" or bool(AUSENCIA.match(t))


def regra_r0(papeis):
    """Retorna (erros, avisos) da configuração dos papéis."""
    erros, avisos = [], []
    for nome, p in sorted(papeis["papeis"].items()):
        if p["tipo"] == "agente" and p["julga"]:
            caneta = ESCRITA & set(p["ferramentas"])
            if caneta:
                erros.append(f"R0 papel que julga '{nome}' tem escrita: {', '.join(sorted(caneta))}")
            elif "Bash" in p["ferramentas"]:
                avisos.append(f"aviso R0 '{nome}' julga e tem Bash: o shell também escreve")
    return erros, avisos


def confere(reg, papeis):
    P = papeis["papeis"]
    erros = []
    executou = reg["executou"]
    rev = reg.get("revisao")

    if rev is None:
        erros.append("R1 não há revisão: ninguém além do autor olhou")
    else:
        if rev["por"] == executou:
            erros.append(f"R1 quem revisou ('{rev['por']}') é quem executou")
        papel = P.get(rev["por"])
        if papel is None or not papel["julga"]:
            erros.append(f"R2 '{rev['por']}' não é papel que julga")
        elif ESCRITA & set(papel["ferramentas"]):
            erros.append(f"R2 '{rev['por']}' julga com caneta na mão")
        if not rev.get("contexto_fresco"):
            erros.append("R3 revisão em contexto herdado: o revisor carregou os becos do autor")

    caixa = reg.get("cauda", {}).get("review", {})
    if caixa.get("marcada"):
        ev = caixa.get("evidencia", "")
        if placeholder(ev):
            erros.append(f"R4 caixa marcada com evidência que é ausência: {ev!r}")
        elif rev is None:
            erros.append("R4 caixa marcada aponta para revisão que não existe")

    gate = reg["gate"]
    dono = P.get(gate["por"], {})
    if dono.get("tipo") != "humano":
        d = papeis["delegacoes"].get(gate.get("delegacao") or "")
        if d is None:
            erros.append(f"R5 gate '{gate['tipo']}' aberto por '{gate['por']}' (agente) sem delegação escrita")
        else:
            if d["revogada"] or d["para"] != gate["por"] or gate["tipo"] not in d["gates"]:
                erros.append("R5 delegação não cobre este gate")
            if P.get(d["de"], {}).get("tipo") != "humano":
                erros.append("R5 delegação não vem de um humano")
            if gate["por"] == executou:
                erros.append("R5 quem abre o gate por delegação executou o trabalho")
            c = gate.get("critico")
            if not c:
                erros.append("R5 gate delegado sem crítico em contexto fresco")
            else:
                pc = P.get(c["por"], {})
                if not pc.get("julga") or ESCRITA & set(pc.get("ferramentas", [])):
                    erros.append(f"R5 crítico '{c['por']}' não é papel que julga sem escrita")
                if not c.get("contexto_fresco") or c["por"] == executou:
                    erros.append("R5 crítico não é independente")
    return erros


def main():
    papeis = json.loads((AQUI / "papeis.json").read_text(encoding="utf-8"))
    acertos, total = 0, 0

    print("== configuração dos papéis (R0)")
    erros0, avisos0 = regra_r0(papeis)
    for a in avisos0:
        print("  " + a)
    print("  ✗ " + "\n  ✗ ".join(erros0) if erros0 else "  ✓ nenhum papel que julga tem Write/Edit")

    print("\n== registros de fechamento")
    for arq in sorted((AQUI / "registros").glob("*.json")):
        reg = json.loads(arq.read_text(encoding="utf-8"))
        erros = confere(reg, papeis)
        veredito = "reprova" if erros else "passa"
        bate = veredito == reg["esperado"]
        total += 1
        acertos += bate
        marca = "✓" if bate else "✗ INESPERADO"
        print(f"  {marca} {arq.stem}: {veredito} (esperado: {reg['esperado']})")
        for e in erros:
            print(f"      - {e}")

    print("\n== prova por mutação: o portão acusa quando a regra é violada?")
    mutado = copy.deepcopy(papeis)
    mutado["papeis"]["revisor"]["ferramentas"].append("Edit")
    acusou = bool(regra_r0(mutado)[0])
    print(f"  revisor ganha Edit -> R0 {'acusa' if acusou else 'NÃO acusa'}")
    mutado = copy.deepcopy(papeis)
    mutado["delegacoes"]["deleg-2026-10-24"]["revogada"] = True
    reg8 = json.loads((AQUI / "registros" / "08-gate-delegado.json").read_text(encoding="utf-8"))
    acusou_rev = bool(confere(reg8, mutado))
    print(f"  delegação revogada -> 08-gate-delegado {'reprova' if acusou_rev else 'AINDA PASSA'}")

    ok = acertos == total and not erros0 and acusou and acusou_rev
    print(f"\nresultado: {acertos}/{total} registros com o veredito esperado; "
          f"mutações acusadas: {int(acusou) + int(acusou_rev)}/2")
    print("✓ verificação de confiança OK" if ok else "✗ verificação de confiança FALHOU")
    return 0 if ok else 1


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
