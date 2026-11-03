#!/usr/bin/env python3
"""checa_catalogo.py — portão mínimo de um catálogo do ecossistema.

Inspirado no check-ecosystem.sh do Maestro (maestro@19823c2:scripts/check-ecosystem.sh),
reescrito do zero, em Python sem dependências, para o apêndice D do livro.

O que mede (e só isto): que todo julgamento sobre trabalho alheio está ANCORADO.
  1. toda fonte tem licença; licença que impede cópia diz "citável, não copiável";
  2. todo card de ideia tem id, fonte conhecida, data, veredito do vocabulário fechado
     e as sete dimensões;
  3. todo id do índice de estado tem card, data AAAA-MM-DD e estado do vocabulário;
  4. o estado CORRENTE de cada ideia é a ÚLTIMA linha com o seu id;
  5. adotar/absorver: o destino é um ARQUIVO que existe e contém o texto da `prova`;
  6. observar: o gatilho de reavaliação está escrito;
  7. (com --anterior) o índice é append-only: o novo começa com o antigo, linha a linha.

O que NÃO mede: se o veredito é sábio, se a descrição da fonte é verdadeira, se um
gatilho já disparou. Isso é julgamento humano (ver "Contraexemplo" no apêndice).

Uso:
  python checa_catalogo.py catalogo --estado catalogo/estado-1-migracao.jsonl
  python checa_catalogo.py catalogo --estado catalogo/estado-2-corrigido.jsonl \
         --anterior catalogo/estado-1-migracao.jsonl
Saída: 0 = ancorado · 1 = achados · 2 = erro de uso.
"""
import argparse
import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

VOCAB = {"adotar", "absorver", "observar", "descartar"}
SEM_COPIA = re.compile(r"proprietária|comercial|sem licença|CC BY-NC", re.I)
MARCA = "citável, não copiável"
DATA = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def campo(texto, nome):
    m = re.search(r"^- \*\*" + re.escape(nome) + r"\*\*:\s*(.+)$", texto, re.M)
    return m.group(1).strip().strip("`") if m else ""


def ler_fontes(caminho, achados):
    fontes = {}
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        if not linha.startswith("|") or re.match(r"^\|\s*:?-", linha):
            continue
        cel = [c.strip() for c in linha.strip().strip("|").split("|")]
        if cel[0] in ("Fonte", "") or len(cel) < 4:
            continue
        nome, _, licenca, data = cel[0].strip("`"), cel[1], cel[2], cel[3]
        fontes[nome] = licenca
        if not licenca:
            achados.append(f"fonte {nome}: sem licença")
        elif SEM_COPIA.search(licenca) and MARCA not in licenca:
            achados.append(f"fonte {nome}: licença '{licenca}' impede cópia e não diz '{MARCA}'")
        if not DATA.match(data[:10]):
            achados.append(f"fonte {nome}: sem data de observação")
    return fontes


def ler_cards(pasta, fontes, achados):
    ids = set()
    for card in sorted(pasta.glob("*.md")):
        t = card.read_text(encoding="utf-8")
        i, f, d, v = campo(t, "Id"), campo(t, "Fonte"), campo(t, "Observado em"), campo(t, "Veredito no momento")
        if not i:
            achados.append(f"card {card.name}: sem Id")
            continue
        ids.add(i)
        if f not in fontes:
            achados.append(f"card {card.name}: fonte '{f}' não é uma linha de fontes.md")
        if not DATA.match(d):
            achados.append(f"card {card.name}: data '{d}' não é AAAA-MM-DD")
        if v not in VOCAB:
            achados.append(f"card {card.name}: veredito '{v}' fora do vocabulário fechado")
        dims = set(re.findall(r"^\|\s*([1-7])\s*\|", t, re.M))
        if dims != {str(n) for n in range(1, 8)}:
            achados.append(f"card {card.name}: dimensões presentes {sorted(dims)}, faltam as sete")
    return ids


def ler_estado(caminho, achados):
    linhas = [l for l in caminho.read_text(encoding="utf-8").splitlines() if l.strip()]
    registros = []
    for n, l in enumerate(linhas, 1):
        try:
            registros.append(json.loads(l))
        except json.JSONDecodeError:
            achados.append(f"{caminho.name}:{n}: linha não é JSON")
    return linhas, registros


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("catalogo", type=Path)
    ap.add_argument("--estado", type=Path, required=True)
    ap.add_argument("--anterior", type=Path)
    a = ap.parse_args()
    if not (a.catalogo / "fontes.md").is_file() or not a.estado.is_file():
        print("✗ catálogo ilegível: falta fontes.md ou o arquivo de estado", file=sys.stderr)
        return 2

    achados = []
    fontes = ler_fontes(a.catalogo / "fontes.md", achados)
    ids_card = ler_cards(a.catalogo / "ideias", fontes, achados)
    linhas, registros = ler_estado(a.estado, achados)
    raiz = (a.catalogo / "repo").resolve()

    corrente = {}
    for r in registros:
        i, e, d = r.get("ideia", ""), r.get("estado", ""), r.get("data", "")
        if i not in ids_card:
            achados.append(f"estado: '{i}' não tem card")
        if e not in VOCAB:
            achados.append(f"estado: '{i}' com estado '{e}' fora do vocabulário")
        if not DATA.match(d):
            achados.append(f"estado: '{i}' com data '{d}' que não é AAAA-MM-DD")
        corrente[i] = r  # a última linha manda

    for i, r in corrente.items():
        e = r.get("estado")
        if e in ("adotar", "absorver"):
            destino, prova = r.get("destino", ""), r.get("prova", "")
            alvo = (raiz / destino).resolve()
            if not destino:
                achados.append(f"{i}: '{e}' sem destino")
            elif raiz not in alvo.parents:
                achados.append(f"{i}: destino '{destino}' fora do repositório")
            elif not alvo.is_file():
                tipo = "é pasta, não arquivo" if alvo.is_dir() else "não existe no disco"
                achados.append(f"{i}: '{e}' com destino '{destino}' que {tipo}")
            elif not prova:
                achados.append(f"{i}: '{e}' em '{destino}' sem 'prova' (texto que tem de estar lá)")
            elif prova not in alvo.read_text(encoding="utf-8"):
                achados.append(f"{i}: a prova '{prova}' não está em '{destino}'")
        if e == "observar" and not r.get("gatilho", "").strip():
            achados.append(f"{i}: 'observar' sem gatilho — esquecer com cerimônia")

    if a.anterior:
        antigas = [l for l in a.anterior.read_text(encoding="utf-8").splitlines() if l.strip()]
        for n, velha in enumerate(antigas, 1):
            if n > len(linhas) or linhas[n - 1] != velha:
                achados.append(f"append-only: a linha {n} de {a.anterior.name} foi reescrita ou apagada")
                break

    contagem = {}
    for r in corrente.values():
        contagem[r.get("estado")] = contagem.get(r.get("estado"), 0) + 1
    resumo = " · ".join(f"{k} {contagem[k]}" for k in sorted(contagem))
    print(f"── catálogo: {len(fontes)} fontes · {len(ids_card)} cards · {len(linhas)} linhas de estado")
    print(f"   estado corrente: {resumo}")
    for x in achados:
        print(f"  ✗ {x}")
    if achados:
        print(f"✗ {len(achados)} achado(s): há julgamento sem âncora.")
        return 1
    print("✓ todo julgamento está ancorado.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
