#!/usr/bin/env python3
"""rodada.py — roda a matriz do ASEG-Bench (casos × braços × repetições) sob o protocolo 0.1.

Cada execução vira uma pasta em `pesquisa/runs/` com o *schema* 1 do protocolo (§4):
run.json (ambiente congelado + métricas), prompt.txt, rastro.json, veredito.json. O log bruto
(log.jsonl) fica na pasta, mas é ignorado pelo git (descreve a máquina).

Braços (protocolo §1):
  A  gatilho + contrato de declaração;
  B  A + `instrucoes/B-<caso>.md`, se existir (senão a célula é pulada e o pulo é dito);
  C  B + `instrucoes/C-<caso>.md`, idem;
  T  A, num cenário com o Maestro instalado no commit congelado (`--maestro`, tag `livro-v1`).

A ordem das células é sorteada com `--semente` (registrada em cada run.json). Falha do harness
é registrada e conta na taxa de erro da célula; não se repete até dar certo.

Uso:
  python rodada.py --casos todos --bracos A,T --repeticoes 10 --modelo sonnet --semente 7
  python rodada.py --casos GOV-004 --bracos A --repeticoes 1 --dry-run
Só biblioteca padrão; precisa de `claude`, `git` e (braço T) do Git Bash.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import io
import json
import os
import platform
import random
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
from pathlib import Path

AQUI = Path(__file__).resolve().parent
LIVRO = AQUI.parents[2]
sys.path.insert(0, str(AQUI))
import adaptador_claude_code as ad  # noqa: E402
import aseg  # noqa: E402
import executar_claude_code as ex  # noqa: E402

PROTOCOLO = "0.1"
BASH = os.environ.get("ASEG_BASH") or next(
    (p for p in [Path(os.environ.get("LOCALAPPDATA", "")) / "Programs/Git/bin/bash.exe",
                 Path("C:/Program Files/Git/bin/bash.exe")] if p.exists()), "bash")


def sha(p: Path | None, texto: str | None = None) -> str | None:
    if texto is not None:
        return "sha256:" + hashlib.sha256(texto.encode("utf-8")).hexdigest()
    if p is None or not p.exists():
        return None
    return "sha256:" + hashlib.sha256(p.read_bytes()).hexdigest()


def rev(d: Path, ref="HEAD") -> str:
    return subprocess.run(["git", "-C", str(d), "rev-parse", ref], capture_output=True, text=True,
                          check=True).stdout.strip()


def maestro_congelado(maestro: Path, ref: str, destino: Path) -> str:
    """Extrai o Maestro em `ref` (sem tocar na árvore de trabalho dele) e devolve o commit."""
    commit = rev(maestro, ref + "^{commit}")
    tar = subprocess.run(["git", "-C", str(maestro), "archive", "--format=tar", commit],
                         capture_output=True, check=True).stdout
    with tarfile.open(fileobj=io.BytesIO(tar)) as t:
        t.extractall(destino)
    return commit


def instalar(maestro_dir: Path, repo: Path) -> str:
    """Instala o Maestro no cenário e commita a instalação: o diff do agente não a inclui."""
    r = subprocess.run([BASH, str(maestro_dir / "scripts/install-maestro.sh"), str(repo),
                        "--write-block"], capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    if r.returncode != 0:
        raise RuntimeError("instalação do Maestro falhou: " + (r.stderr or r.stdout)[-400:])
    ex.git(repo, "add", "-A")
    ex.git(repo, "commit", "-qm", "maestro instalado")
    return rev(repo)


def instrucoes(braco: str, caso: str) -> Path | None:
    if braco in ("A", "T"):
        return None
    p = AQUI / "instrucoes" / f"{braco}-{caso}.md"
    return p if p.exists() else None


def ler_log(log: Path) -> tuple[dict, dict]:
    init, res = {}, {}
    for linha in log.read_text(encoding="utf-8", errors="replace").splitlines():
        if not linha.startswith("{"):
            continue
        try:
            o = json.loads(linha)
        except json.JSONDecodeError:
            continue
        if o.get("type") == "system" and o.get("subtype") == "init":
            init = o
        elif o.get("type") == "result":
            res = o
    return init, res


def uma(caso, braco, rep, modelo, semente, raiz, maestro_dir, maestro_commit, versao, seco):
    dia = dt.date.today().isoformat()
    rid = f"{dia}-ASEG-{caso}-{braco}-{rep:02d}"
    pasta = raiz / rid
    n = 1
    while pasta.exists():  # nunca sobrescreve um run: o schema é imutável
        n += 1
        pasta = raiz / f"{rid}-r{n}"
    instr = instrucoes(braco, caso)
    if braco in ("B", "C") and instr is None:
        return {"id": rid, "pulado": f"sem instrucoes/{braco}-{caso}.md"}
    if seco:
        return {"id": pasta.name, "seco": True}
    base, b = ex.cenario(caso, pasta / "repo")
    if braco == "T":
        base = instalar(maestro_dir, pasta / "repo")
    prompt = ex.CASOS[caso] + "\n\n" + b["contrato"]
    (pasta / "prompt.txt").write_text(prompt, encoding="utf-8")
    cmd = ["claude", "-p", prompt, "--model", modelo, "--setting-sources", "project",
           "--no-session-persistence", "--permission-mode", "acceptEdits",
           "--output-format", "stream-json", "--verbose", "--allowedTools", *ex.FERRAMENTAS]
    if instr:
        cmd += ["--append-system-prompt-file", str(instr)]
    inicio = dt.datetime.now(dt.timezone.utc)
    t0 = time.monotonic()
    with open(pasta / "log.jsonl", "w", encoding="utf-8") as log:
        try:
            subprocess.run(cmd, cwd=pasta / "repo", stdout=log, stderr=subprocess.STDOUT, timeout=1800)
            timeout = None
        except subprocess.TimeoutExpired:
            timeout = "timeout de 1800 s"
    tempo = round(time.monotonic() - t0, 1)
    init, res = ler_log(pasta / "log.jsonl")
    erro = timeout or (res.get("result") if res.get("is_error") else None) or (None if res else "sem linha de resultado")
    rastro = ad.montar(pasta / "repo", base, [("agente", str(pasta / "log.jsonl"))], set(), "qa-report.md")
    (pasta / "rastro.json").write_text(json.dumps(rastro, ensure_ascii=False, indent=1), encoding="utf-8")
    inteiro = aseg.ORACULOS[caso](rastro, b["contexto"])
    resolvida = (not erro) and bool(aseg.alterados(rastro))
    v = {"caso": caso, "braco": braco, "modelo": modelo, "base": base, "tarefa_resolvida": resolvida,
         "erro_do_harness": erro, "violacoes": inteiro, "violacoes_so_estado": aseg.so_estado(inteiro)}
    (pasta / "veredito.json").write_text(json.dumps(v, ensure_ascii=False, indent=1), encoding="utf-8")
    uso = res.get("usage") or {}
    ficha = next(AQUI.glob(f"{caso}-*.md"))
    run = {
        "schema": 1, "id": pasta.name, "protocolo": PROTOCOLO, "hipotese": "ASEG", "tarefa": caso,
        "braco": braco, "repeticao": rep,
        "metodo": {"commit": maestro_commit if braco == "T" else None},
        "livro": {"commit": rev(LIVRO)},
        "modelo": {"pedido": modelo, "resolvido": init.get("model")},
        "modelo_nao_verificado": not init.get("model"),
        "harness": {"nome": "claude-code", "versao": versao},
        "cenario": {"base": base},
        "hashes": {"prompt.txt": sha(None, prompt), "instrucoes": sha(instr), "ficha": sha(ficha),
                   "runner": sha(Path(__file__)), "avaliador": sha(AQUI / "aseg.py")},
        "sistema": {"os": platform.platform(), "python": platform.python_version()},
        "semente": semente, "inicio": inicio.isoformat(), "fim": dt.datetime.now(dt.timezone.utc).isoformat(),
        "metricas": {
            "conforme": not inteiro, "conforme_so_estado": not aseg.so_estado(inteiro),
            "tarefa_resolvida": resolvida, "aceita_primeira_passada": resolvida and not inteiro,
            "retrabalho": None, "tokens_entrada": uso.get("input_tokens"),
            "tokens_saida": uso.get("output_tokens"), "custo": res.get("total_cost_usd"),
            "tempo_s": tempo, "turnos": res.get("num_turns")},
        "erro_do_harness": erro, "substitui": None,
    }
    (pasta / "run.json").write_text(json.dumps(run, ensure_ascii=False, indent=1), encoding="utf-8")
    shutil.rmtree(pasta / "repo", ignore_errors=True)  # o estado relevante está no rastro
    return run


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--casos", default="todos", help="'todos' ou lista: GOV-001,GOV-004")
    ap.add_argument("--bracos", default="A,T")
    ap.add_argument("--repeticoes", type=int, default=10)
    ap.add_argument("--modelo", default="sonnet")
    ap.add_argument("--semente", type=int, default=0)
    ap.add_argument("--saida", default=str(LIVRO / "pesquisa" / "runs"))
    ap.add_argument("--maestro", default=str(LIVRO.parent / "410_MAESTRO"))
    ap.add_argument("--maestro-ref", default="livro-v1")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    casos = sorted(ex.CASOS) if a.casos == "todos" else a.casos.split(",")
    bracos = a.bracos.split(",")
    celulas = [(c, b, r) for c in casos for b in bracos for r in range(1, a.repeticoes + 1)]
    random.Random(a.semente).shuffle(celulas)
    raiz = Path(a.saida)
    raiz.mkdir(parents=True, exist_ok=True)
    versao = None
    if not a.dry_run:
        if not shutil.which("claude"):
            raise SystemExit("✗ `claude` não está no PATH")
        versao = subprocess.run(["claude", "--version"], capture_output=True, text=True).stdout.split()[0]
    tmp = Path(tempfile.mkdtemp(prefix="aseg-maestro-"))
    mdir, mcommit = None, None
    if "T" in bracos and not a.dry_run:
        mdir = tmp / "maestro"
        mcommit = maestro_congelado(Path(a.maestro), a.maestro_ref, mdir)
    print(f"{len(celulas)} célula(s) · semente {a.semente} · modelo {a.modelo}"
          + (f" · Maestro {mcommit[:7]}" if mcommit else ""))
    for i, (c, b, r) in enumerate(celulas, 1):
        out = uma(c, b, r, a.modelo, a.semente, raiz, mdir, mcommit, versao, a.dry_run)
        if out.get("pulado") or out.get("seco"):
            print(f"[{i}/{len(celulas)}] {out['id']}: " + (out.get("pulado") or "dry-run"))
            continue
        m = out["metricas"]
        print(f"[{i}/{len(celulas)}] {out['id']}: resolvida={m['tarefa_resolvida']} "
              f"conforme={m['conforme']} só-estado={m['conforme_so_estado']}"
              + (f" · harness: {out['erro_do_harness'][:80]}" if out["erro_do_harness"] else ""))
    shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
