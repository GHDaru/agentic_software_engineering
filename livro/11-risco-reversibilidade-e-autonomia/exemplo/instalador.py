#!/usr/bin/env python3
"""O instalador que ganhou o poder de apagar — o segundo exemplo do capítulo 11.

Reproduz, em miniatura e num diretório temporário, os defeitos que a revisão independente
achou no instalador do Maestro quando ele passou a ATUALIZAR e PODAR (ciclo 051), e a
correção de cada um. Cada cenário roda contra a versão ingênua (v1) e a corrigida (v2).

    python3 instalador.py

Sai com 0 quando a v2 preserva todos os invariantes e a v1 viola cada um deles
(o defeito precisa ser reproduzido, senão o cenário não prova nada).
"""
from __future__ import annotations

import hashlib
import shutil
import sys
import tempfile
from pathlib import Path

MANIFESTO = ".manifesto.tsv"


def h(texto: str) -> str:
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()[:12]


# --------------------------------------------------------------------------- flags
def flags_v1(argv: list[str]) -> dict:
    """Lia só o segundo argumento posicional, como o `$2` do script original."""
    flag = argv[1] if len(argv) > 1 else ""
    return {"force": flag == "--force", "dry": flag == "--dry-run"}


def flags_v2(argv: list[str]) -> dict:
    """Lê todas as flags; o freio (--dry-run) vence o acelerador (--force)."""
    resto = argv[1:]
    dry = "--dry-run" in resto
    return {"force": "--force" in resto and not dry, "dry": dry}


# --------------------------------------------------------------------------- instalador
def ler_manifesto(alvo: Path) -> dict[str, str]:
    m = alvo / MANIFESTO
    if not m.exists():
        return {}
    linhas = [l.split("\t") for l in m.read_text(encoding="utf-8").splitlines() if l]
    return {caminho: hsh for hsh, caminho in linhas}


def gravar_manifesto(alvo: Path, manifesto: dict[str, str]) -> None:
    texto = "".join(f"{hsh}\t{c}\n" for c, hsh in sorted(manifesto.items()))
    (alvo / MANIFESTO).write_text(texto, encoding="utf-8")


def dentro(alvo: Path, caminho: str) -> bool:
    """O destino resolvido fica dentro do alvo? (`..`, caminho absoluto e link ficam fora)."""
    try:
        (alvo / caminho).resolve().relative_to(alvo.resolve())
        return True
    except ValueError:
        return False


def instalar(origem: dict[str, str], alvo: Path, argv: list[str], versao: int) -> dict:
    flags = flags_v1(argv) if versao == 1 else flags_v2(argv)
    antes = ler_manifesto(alvo)
    depois: dict[str, str] = {}
    saida = {"escritos": 0, "mantidos": 0, "ao_lado": 0, "podados": 0, "recusados": 0}

    for caminho, conteudo in origem.items():
        destino = alvo / caminho
        if versao == 1:
            depois[caminho] = h(conteudo)  # v1: reivindica ANTES de decidir
        existe = destino.exists()
        atual = destino.read_text(encoding="utf-8") if existe else None
        if not existe:
            acao = "escrever"
        elif h(atual) == h(conteudo):
            acao = "igual"
        elif versao == 2 and caminho in antes and h(atual) != antes[caminho] and not flags["force"]:
            acao = "ao_lado"  # o projeto editou: mantém e oferece a versão nova ao lado
        elif versao == 2 and caminho not in antes and not flags["force"]:
            acao = "manter"   # não é nosso: não se toca
        else:
            acao = "escrever"
        if acao == "escrever":
            if not flags["dry"]:
                if existe and versao == 2:
                    shutil.copyfile(destino, destino.with_name(destino.name + ".maestro-old"))
                destino.parent.mkdir(parents=True, exist_ok=True)
                destino.write_text(conteudo, encoding="utf-8")
            depois[caminho] = h(conteudo)
            saida["escritos"] += 1
        elif acao == "ao_lado":
            if not flags["dry"]:
                destino.with_name(destino.name + ".maestro-new").write_text(conteudo, encoding="utf-8")
            depois[caminho] = antes[caminho]  # guarda o hash NOSSO, não adota a edição alheia
            saida["ao_lado"] += 1
        elif acao == "igual" and versao == 2 and caminho in antes:
            depois[caminho] = h(conteudo)
        else:
            saida["mantidos"] += 1

    # poda: o que o método deixou de enviar
    for caminho, hsh in antes.items():
        if caminho in origem:
            continue
        if versao == 2 and not dentro(alvo, caminho):
            print(f"      recusado: '{caminho}' resolve fora do alvo — o manifesto é dado, não comando")
            saida["recusados"] += 1
            continue
        destino = alvo / caminho
        if not destino.exists():
            continue
        if versao == 2 and h(destino.read_text(encoding="utf-8")) != hsh:
            saida["mantidos"] += 1
            continue
        if not flags["dry"]:
            destino.unlink()
        saida["podados"] += 1

    if not flags["dry"]:
        gravar_manifesto(alvo, depois)
    return saida


# --------------------------------------------------------------------------- cenários
def arvore(raiz: Path) -> str:
    partes = []
    for p in sorted(raiz.rglob("*")):
        if p.is_file():
            partes.append(f"{p.relative_to(raiz).as_posix()}:{h(p.read_text(encoding='utf-8'))}")
    return h("|".join(partes))


def cenario_flags(_: Path, versao: int) -> bool:
    f = flags_v1(["alvo", "--force", "--dry-run"]) if versao == 1 else flags_v2(["alvo", "--force", "--dry-run"])
    print(f"      --force --dry-run → force={int(f['force'])} dry={int(f['dry'])}")
    return f["dry"] and not f["force"]


def cenario_adocao(base: Path, versao: int) -> bool:
    alvo = base / "projeto"
    alvo.mkdir()
    # o projeto já tinha, por conta própria, um arquivo byte-idêntico ao nosso
    (alvo / "scripts").mkdir()
    (alvo / "scripts" / "comum.sh").write_text("echo comum\n", encoding="utf-8")
    instalar({"scripts/comum.sh": "echo comum\n", "agente.md": "v1\n"}, alvo, ["alvo"], versao)
    # release seguinte: o método deixa de enviar comum.sh
    instalar({"agente.md": "v2\n"}, alvo, ["alvo"], versao)
    vivo = (alvo / "scripts" / "comum.sh").exists()
    print(f"      arquivo do projeto, idêntico ao nosso, depois da poda: {'existe' if vivo else 'APAGADO'}")
    return vivo


def cenario_edicao(base: Path, versao: int) -> bool:
    alvo = base / "projeto"
    alvo.mkdir()
    instalar({"agente.md": "v1\n"}, alvo, ["alvo"], versao)
    (alvo / "agente.md").write_text("v1 + regra local do time\n", encoding="utf-8")
    # a saída do próprio instalador recomendava --force para pegar a versão nova
    instalar({"agente.md": "v2\n"}, alvo, ["alvo", "--force"], versao)
    velha = alvo / "agente.md.maestro-old"
    recuperavel = velha.exists() and "regra local" in velha.read_text(encoding="utf-8")
    print(f"      edição do time depois do --force: {'recuperável em .maestro-old' if recuperavel else 'PERDIDA, sem cópia'}")
    return recuperavel


def cenario_travessia(base: Path, versao: int) -> bool:
    alvo = base / "projeto"
    alvo.mkdir()
    fora = base / "fora.txt"
    fora.write_text("dado de outro repositório\n", encoding="utf-8")
    instalar({"agente.md": "v1\n"}, alvo, ["alvo"], versao)
    # o manifesto mora no repositório alheio e é comitável: qualquer um escreve nele
    with (alvo / MANIFESTO).open("a", encoding="utf-8") as m:
        m.write(f"{h('dado de outro repositório' + chr(10))}\t../fora.txt\n")
    instalar({"agente.md": "v1\n"}, alvo, ["alvo"], versao)
    vivo = fora.exists()
    print(f"      arquivo fora do alvo depois da poda: {'existe' if vivo else 'APAGADO'}")
    return vivo


def cenario_seco(base: Path, versao: int) -> bool:
    alvo = base / "projeto"
    alvo.mkdir()
    instalar({"agente.md": "v1\n", "velho.md": "x\n"}, alvo, ["alvo"], versao)
    (alvo / "agente.md").write_text("v1 + regra local do time\n", encoding="utf-8")
    antes = arvore(alvo)
    instalar({"agente.md": "v2\n"}, alvo, ["alvo", "--force", "--dry-run"], versao)
    igual = arvore(alvo) == antes
    print(f"      --force --dry-run mudou a árvore? {'não' if igual else 'SIM'}")
    return igual


CENARIOS = [
    ("C1 a flag destrutiva não vence o freio", cenario_flags),
    ("C2 reivindicar é consequência de escrever, não de olhar", cenario_adocao),
    ("C3 o --force guarda a edição do projeto antes de sobrescrever", cenario_edicao),
    ("C4 a poda não sai do alvo", cenario_travessia),
    ("C5 execução a seco não escreve nada", cenario_seco),
]


def main() -> int:
    falhas = 0
    for titulo, cenario in CENARIOS:
        print(titulo)
        resultado = {}
        for versao in (1, 2):
            print(f"   v{versao}:")
            with tempfile.TemporaryDirectory() as tmp:
                resultado[versao] = cenario(Path(tmp), versao)
        reproduz = not resultado[1]
        corrige = resultado[2]
        veredito = "ok" if (reproduz and corrige) else "FALHA"
        if veredito != "ok":
            falhas += 1
        print(f"   → defeito reproduzido na v1: {'sim' if reproduz else 'NÃO'}; "
              f"invariante na v2: {'sim' if corrige else 'NÃO'}  [{veredito}]")
    print(f"resumo: {len(CENARIOS)} cenários, {falhas} falha(s)")
    return 1 if falhas else 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
