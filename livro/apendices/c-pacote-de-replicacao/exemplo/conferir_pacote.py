"""conferir_pacote.py — o roteiro de reprodução do apêndice C, num script só.

Dois modos, Python 3.8+ e Git, sem dependências e sem rede:

  python conferir_pacote.py --conferir [--maestro <clone>] [--livro <raiz>]
      Roda as evidências do apêndice: a versão de referência existe no clone, um claim medido
      do prefácio (oito princípios), as versões do CHANGELOG, as tags, o veredito de oito campos,
      e os ids de claim do próprio apêndice nos dois sentidos (citado = registrado).
      Saída 0 = tudo bate · 1 = alguma evidência não reproduz · 2 = erro de uso.

  python conferir_pacote.py --validar-run <pasta-ou-run.json>
      Confere se um run.json traz o ambiente congelado do protocolo 0.1 (§3): commits, modelo
      pedido e resolvido, harness com versão, commit-base do cenário, SHA-256 das entradas,
      sistema e semente. Recalcula o SHA-256 do prompt.txt quando ele está na mesma pasta.
      Saída 0 = entra na análise (talvez com marca) · 1 = não entra.

Só lê: `git cat-file`, `git show`, `git tag`; nunca muda o clone.
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

REF = "19823c2"
AQUI = Path(__file__).resolve().parent
LIVRO_PADRAO = AQUI.parents[3]          # exemplo -> c-... -> apendices -> livro -> raiz

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass


def git(clone, *args):
    r = subprocess.run(["git", "-C", str(clone), *args], capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    return r.returncode, r.stdout


def linha(ok, rotulo, obtido, esperado):
    marca = "OK   " if ok is True else ("PULA " if ok is None else "FALHA")
    print(f"{marca} {rotulo:<44} obtido: {obtido}   esperado: {esperado}")
    return ok


def conferir(maestro, livro):
    res = []
    if maestro is None:
        for rot in (f"{REF} existe no clone", "CLAIM-00-008 princípios",
                    "CLAIM-93-013 versões do CHANGELOG", "CLAIM-93-013 tags v*"):
            res.append(linha(None, rot, "sem --maestro", "-"))
    else:
        cod, out = git(maestro, "cat-file", "-t", REF)
        tem = cod == 0 and out.strip() == "commit"
        res.append(linha(tem, f"{REF} existe no clone", out.strip() or "ausente", "commit"))
        if tem:
            _, txt = git(maestro, "show", f"{REF}:docs/governance/principles.md")
            n = len(re.findall(r"^### [IVX]+\.", txt, re.M))
            res.append(linha(n == 8, "CLAIM-00-008 princípios (### I.–VIII.)", n, 8))
            _, txt = git(maestro, "show", f"{REF}:CHANGELOG.md")
            versoes = re.findall(r"^## \[([^\]]+)\]", txt, re.M)
            esp = ["Unreleased", "0.3.0", "0.2.0", "0.1.0"]
            res.append(linha(versoes == esp, "CLAIM-93-013 versões do CHANGELOG",
                             ",".join(versoes), ",".join(esp)))
        else:
            print("      o clone não tem o commit de referência; veja o README (clone sem 19823c2)")
        _, out = git(maestro, "tag", "-l", "v*")
        n = len(out.split())
        res.append(linha(n == 0, "CLAIM-93-013 tags v* no clone", n, 0))

    ver = livro / "pesquisa/benchmarks/aseg-bench/execucoes/2026-11-02-GOV-004-01/veredito.json"
    if ver.exists():
        n = len(json.loads(ver.read_text(encoding="utf-8")))
        res.append(linha(n == 8, "CLAIM-93-007 campos do veredito.json", n, 8))
    else:
        res.append(linha(False, "CLAIM-93-007 campos do veredito.json", "arquivo ausente", 8))

    pasta = livro / "livro/apendices/c-pacote-de-replicacao"
    cap = re.sub(r"```.*?```", "", (pasta / "capitulo.md").read_text(encoding="utf-8"), flags=re.S)
    citados = set(re.findall(r"CLAIM-[0-9A-Z]{2}-\d{3}", " ".join(re.findall(r"\[[^\[\]]*CLAIM-[^\[\]]*\]", cap))))
    registrados = set()
    for l in (pasta / "claims.md").read_text(encoding="utf-8").splitlines():
        if l.startswith("|"):
            registrados |= set(re.findall(r"CLAIM-[0-9A-Z]{2}-\d{3}", l.strip("|").split("|")[0]))
    mal = sorted(x for x in citados | registrados if not re.fullmatch(r"CLAIM-\d{2}-\d{3}", x))
    res.append(linha(not mal, "ids do apêndice no formato CLAIM-NN-NNN", len(mal) and mal or "todos", "todos"))
    res.append(linha(citados == registrados, "ids citados = ids registrados",
                     f"{len(citados)} citados, {len(registrados)} registrados", "iguais"))

    falhas = sum(1 for r in res if r is False)
    pulos = sum(1 for r in res if r is None)
    print(f"\n{len(res)} conferências, {falhas} falha(s), {pulos} pulada(s)")
    return 1 if falhas else 0


CAMPOS = {
    "metodo.commit": "commit_ou_nulo", "livro.commit": "commit",
    "modelo.pedido": "texto", "modelo.resolvido": "texto_ou_nulo",
    "harness.nome": "texto", "harness.versao": "texto", "cenario.base": "commit",
    "sistema.os": "texto", "sistema.python": "texto", "semente": "inteiro",
}
HASHES = ["prompt.txt", "instrucoes", "ficha", "runner", "avaliador"]


def pega(d, caminho):
    for parte in caminho.split("."):
        if not isinstance(d, dict) or parte not in d:
            return KeyError
        d = d[parte]
    return d


def validar_run(alvo):
    arq = alvo / "run.json" if alvo.is_dir() else alvo
    run = json.loads(arq.read_text(encoding="utf-8"))
    faltas, marcas = [], []
    for campo, tipo in CAMPOS.items():
        v = pega(run, campo)
        if v is KeyError:
            faltas.append(f"{campo}: ausente")
        elif tipo == "commit" and not (isinstance(v, str) and re.fullmatch(r"[0-9a-f]{7,40}", v)):
            faltas.append(f"{campo}: não é um commit ({v!r})")
        elif tipo == "commit_ou_nulo" and v is not None and not re.fullmatch(r"[0-9a-f]{7,40}", str(v)):
            faltas.append(f"{campo}: não é um commit nem null ({v!r})")
        elif tipo == "texto" and not (isinstance(v, str) and v.strip()):
            faltas.append(f"{campo}: vazio")
        elif tipo == "inteiro" and not isinstance(v, int):
            faltas.append(f"{campo}: não é inteiro ({v!r})")
    if pega(run, "modelo.resolvido") is None:
        marcas.append("modelo_nao_verificado (o harness não relatou o modelo resolvido)")
    hs = run.get("hashes") if isinstance(run.get("hashes"), dict) else None
    if hs is None:
        faltas.append("hashes: ausente")
    else:
        for k in HASHES:
            v = hs.get(k, KeyError)
            if v is KeyError:
                faltas.append(f"hashes.{k}: ausente")
            elif v is None and k == "instrucoes":
                continue                     # braço A: nenhum arquivo de instruções
            elif not (isinstance(v, str) and re.fullmatch(r"sha256:[0-9a-f]{64}", v)):
                faltas.append(f"hashes.{k}: não é sha256:<64 hex> ({v!r})")
        p = arq.parent / "prompt.txt"
        if p.exists() and isinstance(hs.get("prompt.txt"), str):
            real = "sha256:" + hashlib.sha256(p.read_bytes()).hexdigest()
            if real != hs["prompt.txt"]:
                faltas.append("hashes.prompt.txt: não confere com o prompt.txt da pasta")
    print(f"run: {arq}")
    for f in faltas:
        print(f"  FALTA  {f}")
    for m in marcas:
        print(f"  MARCA  {m}")
    if faltas:
        print(f"NÃO ENTRA na análise: {len(faltas)} campo(s) do ambiente congelado")
        return 1
    print("ENTRA na análise" + (" (com marca)" if marcas else ""))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    modo = ap.add_mutually_exclusive_group(required=True)
    modo.add_argument("--conferir", action="store_true")
    modo.add_argument("--validar-run", type=Path, metavar="PASTA_OU_JSON")
    ap.add_argument("--maestro", type=Path, help="clone do Maestro (opcional)")
    ap.add_argument("--livro", type=Path, default=LIVRO_PADRAO, help="raiz do repositório do livro")
    a = ap.parse_args()
    if a.validar_run:
        return validar_run(a.validar_run)
    return conferir(a.maestro, a.livro)


if __name__ == "__main__":
    sys.exit(main())
