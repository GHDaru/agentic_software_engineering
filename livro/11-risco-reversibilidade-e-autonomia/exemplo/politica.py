#!/usr/bin/env python3
"""Política de autonomia por classe de risco — o exemplo do capítulo 11.

A classe de uma ação não vem do verbo ("ler", "apagar"), vem de dois eixos:
quanto custa DESFAZER e até onde vai o RAIO. Cada alavanca de reversibilidade
mexe em UM eixo, e por isso rebaixa a classe sem pedir mais aprovação.

Uso:
    python3 politica.py                  # classifica as ações de acoes.json
    python3 politica.py --funil          # compara gate uniforme com gate proporcional

Sem dependência externa. Código de saída 0 quando as expectativas de acoes.json
batem com a política; 1 quando alguma diverge (a política mudou sem o caso mudar).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# Os dois eixos, do mais leve ao mais pesado.
DESFAZER = ["nada", "trivial", "barato", "caro", "impossivel"]
RAIO = ["proprio", "compartilhado", "externo", "multi"]

# As sete classes (taxonomia do modelo operacional do Maestro, §8), com a política
# allow/ask/deny e o gate humano que cada uma recebe.
CLASSES = [
    ("leitura",                  "permitir",            "nenhum"),
    ("leitura sensível",         "permitir com máscara", "revisão"),
    ("criação reversível",       "permitir",            "no merge"),
    ("alteração",                "perguntar",           "aprovação com resumo"),
    ("exclusão / efeito externo", "perguntar",           "confirmação forte"),
    ("financeira / irreversível", "perguntar",           "dupla aprovação"),
    ("lote / administrativa",    "negar",               "fluxo humano formal"),
]

# Cada alavanca age num eixo só. Nenhuma delas é "mais uma aprovação".
ALAVANCAS = {
    # cópia de segurança: o que era impossível de desfazer passa a ser caro (restaurar)
    "backup":      ("desfazer", {"impossivel": "caro"}),
    # exclusão lógica: desfazer vira um UPDATE de volta
    "soft_delete": ("desfazer", {"impossivel": "barato", "caro": "barato"}),
    # cópia guardada ao lado (.maestro-old): a edição alheia volta com um mv
    "copia_ao_lado": ("desfazer", {"caro": "barato"}),
    # homologação: o raio sai da produção e fica no ambiente próprio
    "staging":     ("raio", {"externo": "proprio", "compartilhado": "proprio"}),
    # execução a seco: a ação ensaiada não tem efeito nenhum — vira leitura
    "dry_run":     ("desfazer", {d: "nada" for d in DESFAZER}),
}


def aplicar_alavancas(desfazer: str, raio: str, alavancas: list[str]) -> tuple[str, str]:
    for nome in alavancas:
        eixo, mapa = ALAVANCAS[nome]
        if eixo == "desfazer":
            desfazer = mapa.get(desfazer, desfazer)
        else:
            raio = mapa.get(raio, raio)
    return desfazer, raio


def classe(acao: dict) -> int:
    """Índice da classe (0..6) a partir dos eixos, depois das alavancas."""
    # Mexer na própria autorização (permissão, identidade, política) é administrativo:
    # o agente que escreve a regra que o julga se daria qualquer permissão.
    if acao.get("autoriza_a_si_mesmo"):
        return 6
    desfazer, raio = aplicar_alavancas(acao["desfazer"], acao["raio"], acao.get("alavancas", []))
    if raio == "multi":
        return 6
    if raio == "proprio" and desfazer != "nada":
        # No ambiente do próprio agente (branch, worktree, homologação descartável),
        # desfazer é recriar o ambiente: o custo não sai do raio.
        return 2
    if desfazer == "impossivel":
        return 5
    if desfazer == "nada":
        return 1 if acao.get("sensivel") else 0
    if desfazer == "caro":
        return 4
    # barato ou trivial, fora do raio próprio: alguém além do agente sente a mudança
    return 3


def classificar(acoes: list[dict]) -> int:
    divergencias = 0
    for a in acoes:
        c = classe(a)
        nome, politica, gate = CLASSES[c]
        alav = "+".join(a.get("alavancas", [])) or "—"
        marca = "ok"
        if a.get("espera") is not None and a["espera"] != c:
            marca = f"DIVERGE (esperava {a['espera']})"
            divergencias += 1
        print(f"[{c}] {a['nome']}")
        print(f"     alavancas: {alav:<22} classe: {nome:<26} política: {politica:<20} gate: {gate}  {marca}")
    print(f"resumo: {len(acoes)} ações, {divergencias} divergência(s)")
    return divergencias


def funil(dia: list[dict]) -> None:
    """Quantas decisões humanas um dia de trabalho pede, sob cada regime."""
    total = sum(item["vezes"] for item in dia)
    uniforme = total  # gate pesado em tudo: o humano decide cada ação
    proporcional = 0
    bloqueadas = 0
    por_classe: dict[int, int] = {}
    for item in dia:
        c = classe(item)
        por_classe[c] = por_classe.get(c, 0) + item["vezes"]
        if CLASSES[c][1] == "perguntar":
            proporcional += item["vezes"]
        elif CLASSES[c][1] == "negar":
            bloqueadas += item["vezes"]
    print(f"ações no dia (fictício): {total}")
    for c in sorted(por_classe):
        print(f"  classe {c} ({CLASSES[c][0]}): {por_classe[c]}")
    print(f"gate uniforme pesado : {uniforme} decisões humanas")
    print(f"gate proporcional    : {proporcional} decisões humanas, {bloqueadas} bloqueada(s) por política")
    print(f"gate uniforme leve   : 0 decisões humanas — e {por_classe.get(5, 0)} ação(ões) irreversível(is) sem ninguém olhar")


def main(argv: list[str]) -> int:
    aqui = Path(__file__).resolve().parent
    dados = json.loads((aqui / "acoes.json").read_text(encoding="utf-8"))
    if "--funil" in argv:
        funil(dados["dia"])
        return 0
    return 1 if classificar(dados["acoes"]) else 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main(sys.argv[1:]))
