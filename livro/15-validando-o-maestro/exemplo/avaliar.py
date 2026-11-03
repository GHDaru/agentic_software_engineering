#!/usr/bin/env python3
"""avaliar.py — saúde de um corpus de avaliação e prova de discriminação por ablação.

Exemplo executável do capítulo 15 ("Validando o Maestro"). Reproduz, em miniatura e sem
modelo nenhum no laço, as duas metades da disciplina que o Maestro tirou do teorema T7:

  1. SAÚDE DO CORPUS (o que o check-evals.sh do Maestro mede): cada caso nomeia um alvo
     que existe, tem eixo (Axis), tem asserção positiva E negativa, e a linha de base
     ainda se refere ao alvo como ele é hoje (aqui: hash do arquivo do alvo).
  2. DISCRIMINAÇÃO (o que o comando /eval faz com um modelo): a resposta do alvo real
     tem de passar e a resposta do alvo ABLADO tem de reprovar. Se o ablado passa, o caso
     não mede o eixo que declara.

AVISO HONESTO: as respostas em respostas/*.md são fixtures escritas à mão, e o "juiz"
abaixo casa palavras-sinal. Isso é um PROXY (anti-padrão 13 do Maestro): serve para
mostrar a mecânica, não substitui o julgamento de um modelo em contexto fresco.

Uso:  python avaliar.py [pasta-do-corpus]      (padrão: ./corpus)
Sai 0 só quando todo caso ativo está saudável e discrimina.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

try:  # o console do Windows pode não ser UTF-8
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass

AQUI = Path(__file__).resolve().parent
CAMPOS_BASELINE = ("Date", "Target-hash", "First-red", "Verdict", "Ablation", "Premise-checked")


def campos(arquivo: Path) -> dict[str, str]:
    """Lê linhas 'Chave: valor' do topo de um arquivo."""
    saida: dict[str, str] = {}
    for linha in arquivo.read_text(encoding="utf-8").splitlines():
        if ":" in linha and not linha.startswith((" ", "#", "-")):
            chave, valor = linha.split(":", 1)
            saida.setdefault(chave.strip(), valor.strip())
    return saida


def assercoes(expect: Path) -> tuple[list[tuple[str, list[str]]], list[tuple[str, list[str]]]]:
    """MUST-FIND / MUST-NOT-CLAIM no formato '<texto> :: sinal1; sinal2'."""
    achar, negar = [], []
    for linha in expect.read_text(encoding="utf-8").splitlines():
        for prefixo, destino in (("MUST-FIND:", achar), ("MUST-NOT-CLAIM:", negar)):
            if linha.startswith(prefixo):
                corpo = linha[len(prefixo):]
                texto, _, sinais = corpo.partition("::")
                destino.append((texto.strip(), [s.strip().lower() for s in sinais.split(";") if s.strip()]))
    return achar, negar


def julgar(resposta: str, achar, negar) -> tuple[bool, list[str]]:
    """Juiz didático: passa se acha cada MUST-FIND e não afirma nenhum MUST-NOT-CLAIM."""
    r = resposta.lower()
    motivos = []
    for texto, sinais in achar:
        if not any(s in r for s in sinais):
            motivos.append(f"não achou: {texto}")
    for texto, sinais in negar:
        if any(s in r for s in sinais):
            motivos.append(f"afirmou o proibido: {texto}")
    return (not motivos), motivos


def hash_curto(arquivo: Path) -> str:
    # Normaliza o fim de linha: um checkout com CRLF não é "o alvo mudou".
    texto = arquivo.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(texto).hexdigest()[:8]


def avaliar_caso(pasta: Path, raiz: Path) -> tuple[bool, bool]:
    """Devolve (saudável, aposentado)."""
    print(f"• {pasta.name}")
    erros = []

    def ruim(msg: str) -> None:
        erros.append(msg)
        print(f"  ✗ {msg}")

    faltando = [f for f in ("case.md", "expect.md", "baseline.md") if not (pasta / f).is_file()]
    if faltando:
        ruim(f"faltam {', '.join(faltando)}")
        return False, False

    caso = campos(pasta / "case.md")
    if caso.get("Status") == "retired":
        motivo = caso.get("Retired-because", "")
        if not motivo:
            ruim("aposentado sem 'Retired-because:' — aposentar sem motivo é apagar")
            return False, True
        print(f"  APOSENTADO — {motivo}")
        return True, True

    alvo = raiz / caso.get("Target", "")
    if not caso.get("Target") or not alvo.is_file():
        ruim(f"alvo inexistente: {caso.get('Target', '(sem Target:)')}")
        return False, False
    print(f"  alvo: {caso['Target']}")
    if not caso.get("Axis"):
        ruim("sem 'Axis:' — caso sem eixo não tem o que ablar")

    achar, negar = assercoes(pasta / "expect.md")
    if not achar:
        ruim("sem MUST-FIND: — nada diz o que a resposta certa contém")
    if not negar:
        ruim("sem MUST-NOT-CLAIM: — sem lado negativo o caso não discrimina")
    if achar and negar:
        print(f"  asserções: {len(achar)} must-find / {len(negar)} must-not-claim")

    base = campos(pasta / "baseline.md")
    for campo in CAMPOS_BASELINE:
        if campo not in base:
            ruim(f"baseline.md sem '{campo}:'")
    if base.get("First-red") == "pending":
        ruim("nunca visto reprovando (First-red: pending) — rode o caso contra o ablado")
    atual = hash_curto(alvo)
    registrado = base.get("Target-hash", "")
    if registrado and registrado != atual:
        ruim(f"linha de base defasada — o alvo mudou {registrado} → {atual}; avalie de novo")
    elif registrado:
        print(f"  linha de base atual ({atual})")

    # Discriminação: só faz sentido com os dois lados das asserções.
    if achar and negar:
        for papel in ("alvo", "ablado"):
            arq = pasta / "respostas" / f"{papel}.md"
            if not arq.is_file():
                ruim(f"sem respostas/{papel}.md")
                continue
            passou, motivos = julgar(arq.read_text(encoding="utf-8"), achar, negar)
            veredito = "PASSA" if passou else "REPROVA"
            detalhe = f" ({'; '.join(motivos)})" if motivos else ""
            print(f"  {papel:<6} {veredito}{detalhe}")
            if papel == "alvo" and not passou:
                ruim("o alvo real reprova — regressão ou caso mal escrito; leia antes de mexer")
            if papel == "ablado" and passou:
                ruim(f"o ablado PASSA — o caso não mede o eixo '{caso.get('Axis', '?')}'; "
                     "aposente com motivo, não ajuste a fixture até ficar vermelho")
    return (not erros), False


def main() -> int:
    raiz = AQUI
    corpus = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else AQUI / "corpus"
    if not corpus.is_dir():
        print(f"✗ {corpus} não existe — não há corpus para manter honesto.")
        return 1
    print("── Corpus de avaliação (T7 / C11) ──")
    casos = sorted(p for p in corpus.iterdir() if p.is_dir())
    saudaveis = aposentados = 0
    for pasta in casos:
        ok, aposentado = avaliar_caso(pasta, raiz)
        saudaveis += ok
        aposentados += aposentado
    print("──")
    print(f"casos: {len(casos)} · saudáveis: {saudaveis} · aposentados: {aposentados}")
    if saudaveis < len(casos):
        print("✗ o corpus não está saudável (veja acima).")
        return 1
    if not casos:
        print("✓ corpus bem formado — e vazio. Nada aqui está avaliado ainda.")
        return 0
    print("✓ todo caso nomeia um alvo real, discrimina e está atual.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
