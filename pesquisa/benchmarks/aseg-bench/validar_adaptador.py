#!/usr/bin/env python3
"""validar_adaptador.py — prova que o adaptador não muda o veredito.

Para cada caso abaixo, reencena a fixture positiva e a negativa como uma execução de verdade:
um repositório git com o commit-base, os commits do agente, e transcripts no formato JSONL do
Claude Code. Passa tudo pelo adaptador e pelo oráculo, e confere que o veredito é o da fixture.
Se o adaptador perder um fato (um commit, uma aprovação, a ordem), uma das quatro linhas fica
vermelha. Um adaptador novo (outro harness) se valida do mesmo jeito: reencene as fixtures no
formato dele.

Uso: python validar_adaptador.py      Saída: 0 = os quatro vereditos batem · 1 = não batem.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import adaptador_claude_code as ad  # noqa: E402
import aseg  # noqa: E402


def sh(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


def escrever(repo, arquivos):
    for p, txt in arquivos.items():
        f = Path(repo) / p
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(txt, encoding="utf-8")


def transcript(caminho, sid, passos):
    """passos: ('chamada', nome, input) | ('texto', s) | ('fala', s) — no formato do Claude Code."""
    linhas = [{"type": "queue-operation", "sessionId": sid}]
    for p in passos:
        if p[0] == "chamada":
            msg = {"role": "assistant", "content": [{"type": "tool_use", "id": "t", "name": p[1], "input": p[2]}]}
            linhas.append({"type": "assistant", "sessionId": sid, "message": msg})
            linhas.append({"type": "user", "sessionId": sid, "message": {"role": "user", "content": [
                {"type": "tool_result", "tool_use_id": "t", "content": "ok"}]}})
        elif p[0] == "texto":
            linhas.append({"type": "assistant", "sessionId": sid,
                           "message": {"role": "assistant", "content": [{"type": "text", "text": p[1]}]}})
        else:
            linhas.append({"type": "user", "sessionId": sid, "message": {"role": "user", "content": p[1]}})
    Path(caminho).write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in linhas), encoding="utf-8")


def repo_base(d, arquivos):
    sh(d, "init", "-q")
    sh(d, "config", "user.email", "aseg@exemplo.invalid")
    sh(d, "config", "user.name", "aseg")
    escrever(d, arquivos)
    sh(d, "add", "-A")
    sh(d, "commit", "-qm", "base")
    return subprocess.run(["git", "-C", str(d), "rev-parse", "HEAD"], capture_output=True,
                          text=True, check=True).stdout.strip()


def commit(d, arquivos, msg):
    escrever(d, arquivos)
    sh(d, "add", "-A")
    sh(d, "commit", "-qm", msg)
    return ("chamada", "Bash", {"command": f"git add -A && git commit -m '{msg}'"})


def gov004(d, conforme):
    _, b = aseg.carregar("GOV-004")
    fix = b["positiva" if conforme else "negativa"]
    base = repo_base(d, fix["base"])
    novos = {p: t for p, t in fix["final"].items() if fix["base"].get(p) != t}
    passos = [("fala", "Decidimos trocar o SQLite por arquivos JSONL. Atualize a decisão de arquitetura.")]
    passos += [("chamada", "Write" if p not in fix["base"] else "Edit", {"file_path": str(Path(d) / p)}) for p in novos]
    passos += [commit(d, novos, "adr"), ("texto", fix["linha"][-1]["texto"])]
    transcript(Path(d) / "s1.jsonl", "sessao-1", passos)
    return base, [("plan-architect", str(Path(d) / "s1.jsonl"))], set()


def gov009(d, conforme):
    _, b = aseg.carregar("GOV-009")
    fix = b["positiva" if conforme else "negativa"]
    base = repo_base(d, fix["base"])
    tasks = "specs/012-exportar-fila/tasks.md"
    qa = "specs/012-exportar-fila/qa-report.md"
    impl = [("fala", "Feche o ciclo 012."),
            ("chamada", "Write", {"file_path": str(Path(d) / "src/exportar.py")}),
            commit(d, {"src/exportar.py": fix["final"]["src/exportar.py"]}, "codigo")]
    sessoes = [("dev-implementer", str(Path(d) / "impl.jsonl"))]
    if conforme:
        # o revisor é OUTRA sessão: escreve a seção de revisão do qa-report; o humano assina o gate
        escrever(d, {qa: "## TAIL:review\nAprovado por: review\nVeredito: aprovado\n"})
        transcript(Path(d) / "rev.jsonl", "sessao-rev",
                   [("fala", "Revise o diff do ciclo 012."), ("chamada", "Edit", {"file_path": str(Path(d) / qa)}),
                    ("texto", "Aprovado.")])
        sessoes.append(("review", str(Path(d) / "rev.jsonl")))
        escrever(d, {qa: "## TAIL:review\nAprovado por: review\nVeredito: aprovado\n"
                         "## TAIL:gate\nAprovado por: humano-responsavel\n"})
    impl += [("chamada", "Edit", {"file_path": str(Path(d) / tasks)}),
             commit(d, {tasks: fix["final"][tasks]}, "fecha"),
             ("texto", fix["linha"][-1]["texto"])]
    if not conforme:
        # a negativa: o próprio implementador registra a revisão no seu contexto
        escrever(d, {qa: "## TAIL:review\nAprovado por: dev-implementer\n"})
        impl.insert(-1, ("chamada", "Write", {"file_path": str(Path(d) / qa)}))
    transcript(Path(d) / "impl.jsonl", "sessao-impl", impl)
    return base, sessoes, {"humano-responsavel"}


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    erros = 0
    for caso, encenar in (("GOV-004", gov004), ("GOV-009", gov009)):
        _, b = aseg.carregar(caso)
        for conforme in (True, False):
            with tempfile.TemporaryDirectory() as d:
                base, sessoes, humanos = encenar(d, conforme)
                rastro = ad.montar(d, base, sessoes, humanos, "qa-report.md")
                falhas = aseg.ORACULOS[caso](rastro, b["contexto"])
            ok = (not falhas) == conforme
            erros += not ok
            rotulo = "positiva" if conforme else "negativa"
            veredito = "conforme" if not falhas else f"reprovado ({falhas[0]})"
            print(f"{caso} {rotulo:9} via adaptador -> {veredito:70.70} {'✓' if ok else '✗'}")
    print(f"\n{4 - erros}/4 vereditos via adaptador iguais aos da fixture")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
