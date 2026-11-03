"""medir_maestro.py — reproduz os números do capítulo 6 a partir de um clone do Maestro.

Opcional: precisa de git e de um clone de https://github.com/GHDaru/maestro. Só LÊ o
repositório (git ls-tree / git cat-file); não escreve nada nele.

Uso:  python medir_maestro.py <caminho-do-clone> [ref]      (ref padrão: 19823c2)
"""
import json
import re
import subprocess
import sys
from collections import Counter

CAP025 = "c47ea48"   # commit do ciclo 025 (capítulo de orquestração do handbook)
CHECKBOX = re.compile(r"^\s*- \[[ xX]\]", re.M)
IDEIAS = ["worktree-por-task", "grafo-de-dependencias", "decomposicao-tres-passadas",
          "padroes-de-fatiamento", "fatia-vertical-invest", "contrato-por-fatia",
          "decompose-feature-em-issues"]
COSTURA = ["361070a", "78a1945", "79d8076", "6cba79b", "c3d2e55", "692bf8c"]


def git(repo, *args, check=True):
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True, check=check)
    return r.stdout.decode("utf-8", "replace"), r.returncode


def ler_varios(repo, objetos):
    """Lê muitos blobs numa chamada só (git cat-file --batch)."""
    entrada = "".join(f"{o}\n" for o in objetos).encode()
    saida = subprocess.run(["git", "-C", repo, "cat-file", "--batch"], input=entrada,
                           capture_output=True, check=True).stdout
    textos, i = {}, 0
    for o in objetos:
        fim = saida.index(b"\n", i)
        cab = saida[i:fim].decode().split()
        if cab[-1] == "missing":
            textos[o], i = None, fim + 1
            continue
        n = int(cab[2])
        textos[o] = saida[fim + 1:fim + 1 + n].decode("utf-8", "replace")
        i = fim + 1 + n + 1
    return textos


def main():
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    repo, ref = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "19823c2")
    print(f"Maestro @ {ref}")

    # 1. numeração em linhas paralelas: prefixos repetidos e pasta sem número
    pastas = [p.split("/", 1)[1] for p in git(repo, "ls-tree", "-d", "--name-only", ref, "specs/")[0].split()]
    pref = Counter(p[:3] for p in pastas)
    gemeas = {k: sorted(p for p in pastas if p.startswith(k)) for k, v in pref.items() if v > 1}
    print(f"\n[numeração] {len(pastas)} pastas em specs/")
    for k, v in sorted(gemeas.items()):
        print(f"  prefixo {k} usado {len(v)} vezes: {', '.join(v)}")
    print(f"  pastas sem número (NNN-*): {sum(p.startswith('NNN') for p in pastas)}")

    dec, _ = git(repo, "show", f"{ref}:docs/records/decisoes.jsonl")
    linhas = {}
    for l in dec.splitlines():
        try:
            o = json.loads(l)
        except ValueError:
            continue
        linhas[o.get("id")] = o
    for i in ["ciclo-065-renumerado", "ciclo-066-integra-painel-controle", "decisao-066-sessoes-via-gateway"]:
        print(f"  decisão {i}: {'registrada em ' + linhas[i]['data'] if i in linhas else 'AUSENTE'}")

    # 2. encadeamento fixo: comandos versionados
    for r in (CAP025, ref):
        cmds = [c for c in git(repo, "ls-tree", "--name-only", r, ".claude/commands/")[0].split() if c.endswith(".md")]
        print(f"\n[comandos] {len(cmds)} arquivos em .claude/commands/ @ {r}")

    # 3. avaliador-otimizador: relatórios com portão provado falhando (exceto o do próprio 025)
    out, _ = git(repo, "grep", "-l", "-i", "-E", "prova.* falhando", CAP025, "--", "specs/*/qa-report.md", check=False)
    achados = [l.split(":", 1)[1] for l in out.split() if "025-" not in l]
    print(f"\n[avaliador-otimizador] qa-reports com 'prova... falhando' @ {CAP025} (fora o 025): {len(achados)}")
    for a in achados:
        print(f"  {a}")

    # 4. tamanho das listas de tarefas (gatilho da ideia 011: >20 tasks paralelas)
    arqs = [a for a in git(repo, "ls-tree", "-r", "--name-only", ref, "specs/")[0].split()
            if re.fullmatch(r"specs/[^/]+/tasks\.md", a)]
    textos = ler_varios(repo, [f"{ref}:{a}" for a in arqs])
    contagem = sorted(((len(CHECKBOX.findall(t or "")), a.split("/")[1]) for a, t in
                       zip(arqs, (textos[f"{ref}:{a}"] for a in arqs))), reverse=True)
    acima = [c for c in contagem if c[0] > 20]
    print(f"\n[tarefas] {len(arqs)} tasks.md; {len(acima)} com mais de 20 caixas de tarefa")
    for n, d in contagem[:3]:
        print(f"  {n:4d}  {d}")

    # 5. worktree: o código e o catálogo
    ms, _ = git(repo, "show", f"{ref}:scripts/multi-session.py")
    print(f"\n[worktree] scripts/multi-session.py cria worktree por Worker: "
          f"{'sim' if 'worktree' in ms and 'def worktree_for' in ms else 'não'}")
    est, _ = git(repo, "show", f"{ref}:docs/ecosystem/estado.jsonl")
    ultimo = {}
    for l in est.splitlines():
        try:
            o = json.loads(l)
        except ValueError:
            continue
        ultimo[o["ideia"]] = o
    print("[catálogo] estado corrente (última linha) das ideias de divisão:")
    for i in IDEIAS:
        o = ultimo.get(i, {})
        print(f"  {i:30s} {o.get('estado', '?'):10s} {o.get('data', '')}")

    # 6. a costura do 074: os commits existem e estão na linha de {ref}
    print("\n[costura 074] commits da fatia «um número só»:")
    for c in COSTURA:
        s, rc = git(repo, "log", "-1", "--format=%h %ad %s", "--date=short", c, check=False)
        _, anc = git(repo, "merge-base", "--is-ancestor", c, ref, check=False)
        onde = "na linha (cherry-pick do Gerente)" if anc == 0 else "ponta do Worker"
        print(f"  {s.strip()[:60] if rc == 0 else c + ' AUSENTE'}  [{onde}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
