"""medir_maestro.py — reproduz os números do capítulo 4 a partir de um clone do Maestro.

Opcional: precisa de git e de um clone de https://github.com/GHDaru/maestro. Só LÊ o
repositório (git ls-tree / git show); não escreve nada nele.

Uso:  python medir_maestro.py <caminho-do-clone> [ref]      (ref padrão: 19823c2)
"""
import re
import subprocess
import sys
from collections import Counter

LANE = re.compile(r"(raia|lane)\*\*: *([A-Za-zç]+)", re.I)


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, check=True,
                          ).stdout.decode("utf-8", "replace")


def specs(repo, ref):
    nomes = git(repo, "ls-tree", "-r", "--name-only", ref, "specs/").splitlines()
    return sorted(n for n in nomes if re.fullmatch(r"specs/[^/]+/spec\.md", n))


def raia(texto):
    status = next((l for l in texto.splitlines() if l.startswith("- **Status**")), "")
    m = LANE.search(status)
    if not m:
        return "sem raia legível"
    valor = m.group(2).lower()
    return {"full": "plena", "light": "leve"}.get(valor, valor)


def medir(repo, ref):
    arquivos = specs(repo, ref)
    total, antes, depois, ears = Counter(), Counter(), Counter(), 0
    for arq in arquivos:
        texto = git(repo, "show", f"{ref}:{arq}")
        r = raia(texto)
        total[r] += 1
        num = arq.split("/")[1][:3]
        if num.isdigit():
            (antes if int(num) < 34 else depois)[r] += 1
        ears += "O SISTEMA DEVE" in texto
    pastas = len(git(repo, "ls-tree", "-d", "--name-only", ref, "specs/").splitlines())
    return arquivos, pastas, total, antes, depois, ears


def fmt(c):
    return " · ".join(f"{k}: {v}" for k, v in sorted(c.items(), key=lambda kv: (-kv[1], kv[0])))


def main():
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    repo, ref = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "19823c2")
    arquivos, pastas, total, antes, depois, ears = medir(repo, ref)
    print(f"Maestro @ {ref}")
    print(f"  pastas em specs/: {pastas} · com spec.md: {len(arquivos)}")
    print(f"  spec.md com 'O SISTEMA DEVE': {ears}")
    print(f"  raias (total): {fmt(total)}")
    print(f"  raias, ciclos 001–033: {fmt(antes)}")
    print(f"  raias, ciclos 034 em diante: {fmt(depois)}")
    print("  pasta specs/040-*: " + ("existe" if any("/040-" in a for a in arquivos) else "não existe"))
    a, p, t, _, _, e = medir(repo, "100a8af")
    print("Maestro @ 100a8af (véspera do ciclo 023)")
    print(f"  pastas em specs/: {p} · spec.md com 'O SISTEMA DEVE': {e} · raias: {fmt(t)}")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    sys.exit(main())
