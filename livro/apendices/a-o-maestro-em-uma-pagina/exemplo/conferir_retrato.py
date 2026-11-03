#!/usr/bin/env python3
"""Confere o retrato do Maestro contra o disco, numa versão dada.

Uso:  python conferir_retrato.py <clone-do-maestro> [commit ...]
Padrão de commits: 9be9c3f (ciclo 053) e 19823c2 (versão citada pelo livro).

Só lê (git ls-tree / git show). Não escreve nada no clone.
"""
import re
import subprocess
import sys


def git(repo, *args):
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True)
    if r.returncode != 0:
        return None
    return r.stdout.decode("utf-8", errors="replace")


def nomes(repo, commit, pasta):
    out = git(repo, "ls-tree", "--name-only", f"{commit}:{pasta}")
    return [] if out is None else [l for l in out.splitlines() if l]


def mostrar(repo, commit, caminho):
    return git(repo, "show", f"{commit}:{caminho}")


def retrato(repo, commit):
    linhas = {}
    linhas["agentes (.claude/agents/*.md)"] = len(
        [n for n in nomes(repo, commit, ".claude/agents") if n.endswith(".md")])
    linhas["comandos (.claude/commands)"] = len(nomes(repo, commit, ".claude/commands"))
    linhas["skills (pastas em skills/)"] = len(
        [n for n in nomes(repo, commit, "skills") if "." not in n])
    linhas["templates (.specify/templates)"] = len(nomes(repo, commit, ".specify/templates"))
    linhas["portoes (scripts/check-*.sh)"] = len(
        [n for n in nomes(repo, commit, "scripts") if re.fullmatch(r"check-.*\.sh", n)])
    bpmn = mostrar(repo, commit, "docs/diagramas/05-bpmn-processo.md") or ""
    linhas["raias no BPMN (bpmn-raia)"] = bpmn.count('class="bpmn-raia"')
    m = re.search(r"Port[õo]es</b><small>a DoD execut[áa]vel — (\d+) checks", bpmn)
    linhas["portoes que o BPMN anuncia"] = m.group(1) if m else "-"
    arch = mostrar(repo, commit, "docs/diagramas/maestro-workflow.archify.json")
    if arch:
        rev = re.search(r'"revision":\s*"([0-9a-f]{7})', arch)
        linhas["archify: retrato tirado em"] = rev.group(1) if rev else "?"
    else:
        linhas["archify: retrato tirado em"] = "(peça não existe)"
    return linhas


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    repo = sys.argv[1]
    commits = sys.argv[2:] or ["9be9c3f", "19823c2"]
    tabelas = {c: retrato(repo, c) for c in commits}
    chaves = list(next(iter(tabelas.values())).keys())
    larg = max(len(k) for k in chaves)
    print("medida".ljust(larg), *[c.rjust(10) for c in commits])
    for k in chaves:
        print(k.ljust(larg), *[str(tabelas[c][k]).rjust(10) for c in commits])
    return 0


if __name__ == "__main__":
    sys.exit(main())
