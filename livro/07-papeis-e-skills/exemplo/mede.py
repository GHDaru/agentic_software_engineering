#!/usr/bin/env python3
"""mede.py — mede os perfis de agente de uma pasta (capítulo 7).

Para cada arquivo .md da pasta: linhas, bytes, ~tokens (bytes/4, aproximação grosseira),
ferramentas, se escreve (Write/Edit) e se declara modelo. Lê o front matter no formato de
subagente do Claude Code (tools:, model:) e no formato da fixture deste capítulo
(ferramentas:, modelo:). Só biblioteca padrão.

Uso:
  python mede.py time/papeis
  python mede.py <clone-do-maestro>/.claude/agents
Saída: sempre 0 (é medida, não portão).
"""
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def campo(texto, *chaves):
    for k in chaves:
        m = re.search(rf"^{k}:\s*(.*)$", texto, re.M)
        if m:
            return m.group(1).strip()
    return None


def main():
    pasta = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "time" / "papeis"
    linhas_tab = []
    for f in sorted(pasta.glob("*.md")):
        dados = f.read_bytes()
        texto = dados.decode("utf-8")
        tools = campo(texto, "tools", "ferramentas") or ""
        modelo = campo(texto, "model", "modelo")
        escreve = bool(re.search(r"\b(Write|Edit)\b", tools))
        linhas_tab.append((f.stem, len(texto.splitlines()), len(dados), tools, escreve, modelo))

    print(f"{'perfil':<22}{'linhas':>7}{'bytes':>7}{'~tok':>6}  {'escreve':<8}{'modelo':<8}ferramentas")
    for nome, ln, by, tools, esc, mod in linhas_tab:
        print(f"{nome:<22}{ln:>7}{by:>7}{round(by / 4):>6}  {'sim' if esc else 'não':<8}{mod or '—':<8}{tools}")
    n = len(linhas_tab)
    if not n:
        print("nenhum perfil .md na pasta")
        return
    ls = [x[1] for x in linhas_tab]
    bs = [x[2] for x in linhas_tab]
    print(f"\nperfis: {n} · linhas: {sum(ls)} (média {sum(ls) / n:.1f}, menor {min(ls)}, maior {max(ls)})"
          f" · bytes: {sum(bs)} (~{round(sum(bs) / 4)} tokens)")
    print(f"sem escrita (Write/Edit): {sum(1 for x in linhas_tab if not x[4])} → "
          + ", ".join(x[0] for x in linhas_tab if not x[4]))
    print(f"com modelo declarado: {sum(1 for x in linhas_tab if x[5])} de {n}")


if __name__ == "__main__":
    main()
