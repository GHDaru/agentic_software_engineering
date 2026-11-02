#!/usr/bin/env python3
"""adaptador_claude_code.py — converte uma execução do Claude Code no rastro do ASEG-Bench.

É o adaptador MÍNIMO de um harness: lê o repositório de cenário (git) e o(s) transcript(s) da
execução, e escreve o rastro JSON que `aseg.py --avaliar` julga. Serve de molde para outro
harness (Codex, um laço em LangGraph): o que muda é só `eventos_da_sessao`, que traduz o log
daquele harness em chamadas, falas do operador e a resposta final.

Fontes aceitas por sessão: o JSONL que o Claude Code grava em ~/.claude/projects/<dir>/<id>.jsonl
ou a saída de `claude -p --output-format stream-json --verbose`. Linhas de outros tipos são
ignoradas.

Como cada campo do rastro nasce:
  base / final   todos os arquivos de texto do commit-base e da árvore de trabalho no fim.
  chamada        cada `tool_use` do assistente; a entrada é o comando (Bash) ou o caminho
                 (Read/Edit/Write), senão o JSON da entrada.
  commit         cada commit de `base..HEAD`, pareado EM ORDEM com as chamadas Bash que rodaram
                 `git commit`; autor = nome da sessão que o fez, contexto = id dessa sessão.
  aprovacao      (a) humana: fala do operador que começa com `APROVO <alvo>` (o protocolo do
                 OPERADOR do experimento, igual em todos os níveis); (b) por registro: cada seção
                 `## <alvo>` de um arquivo de evidência com uma linha `Aprovado por: <quem>`,
                 situada logo após a última escrita desse arquivo, no contexto de quem escreveu.
  resposta       o último texto do assistente da PRIMEIRA sessão (ou o `result` do stream-json).

Uso:
  python adaptador_claude_code.py --repo CENARIO --base SHA \
      --sessao principal=execucao.jsonl [--sessao revisor=rev.jsonl ...] \
      [--humano nome ...] [--evidencia qa-report.md] > rastro.json
Só biblioteca padrão; Python 3.8+. Limites declarados no README.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

APROVO = re.compile(r"^\s*APROVO\s+(\S+)", re.M)


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True,
                          encoding="utf-8", errors="replace", check=True).stdout


def arquivos_do_commit(repo, sha):
    out = {}
    for p in git(repo, "ls-tree", "-r", "--name-only", sha).splitlines():
        try:
            out[p] = git(repo, "show", f"{sha}:{p}")
        except subprocess.CalledProcessError:
            pass
    return out


def arvore_final(repo):
    out = {}
    nomes = git(repo, "ls-files", "--cached", "--others", "--exclude-standard").splitlines()
    for p in nomes:
        f = Path(repo) / p
        if f.is_file() and f.stat().st_size < 1_000_000:
            try:
                out[p] = f.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                pass
    return out


def entrada_de(nome, inp):
    if nome == "Bash":
        return inp.get("command", "")
    if "file_path" in inp:
        return inp["file_path"].replace("\\", "/")
    return json.dumps(inp, ensure_ascii=False)


def eventos_da_sessao(caminho):
    """(id da sessão, eventos, resposta). Evento: ('chamada', ferramenta, entrada) ou
    ('fala', texto). Só esta função conhece o formato do harness."""
    sid, eventos, ultimo_texto, result = None, [], "", None
    for linha in Path(caminho).read_text(encoding="utf-8").splitlines():
        try:
            o = json.loads(linha)
        except json.JSONDecodeError:
            continue
        sid = sid or o.get("sessionId") or o.get("session_id")
        if o.get("type") == "result":
            result = o.get("result")
        if o.get("type") not in ("assistant", "user") or o.get("isMeta"):
            continue
        conteudo = (o.get("message") or {}).get("content")
        if isinstance(conteudo, str):
            conteudo = [{"type": "text", "text": conteudo}]
        for bloco in conteudo or []:
            if o["type"] == "assistant" and bloco.get("type") == "tool_use":
                eventos.append(("chamada", bloco.get("name"), entrada_de(bloco.get("name"), bloco.get("input") or {})))
            elif o["type"] == "assistant" and bloco.get("type") == "text":
                ultimo_texto = bloco.get("text", "")
            elif o["type"] == "user" and bloco.get("type") == "text":
                eventos.append(("fala", bloco.get("text", "")))
    return sid or Path(caminho).stem, eventos, (result if result is not None else ultimo_texto)


def montar(repo, base, sessoes, humanos, evidencia):
    commits = git(repo, "log", "--reverse", "--format=%H", f"{base}..HEAD").split()
    final = arvore_final(repo)
    linha, resposta, k = [], None, 0
    ultima_escrita = {}  # caminho -> (posição na linha, nome da sessão, contexto)
    for nome, caminho in sessoes:
        sid, eventos, texto = eventos_da_sessao(caminho)
        if resposta is None:
            resposta = texto
        for ev in eventos:
            if ev[0] == "fala":
                for alvo in APROVO.findall(ev[1]):
                    linha.append({"tipo": "aprovacao", "quem": "operador", "papel": "humano",
                                  "contexto": "humano", "alvo": alvo, "evidencia": None})
                continue
            _, ferramenta, entrada = ev
            linha.append({"tipo": "chamada", "ferramenta": ferramenta, "entrada": entrada})
            if ferramenta in ("Write", "Edit"):
                ultima_escrita[entrada] = (len(linha), nome, sid)
            if ferramenta == "Bash" and re.search(r"\bgit\s+commit\b", entrada) and k < len(commits):
                arqs = git(repo, "show", "--name-only", "--format=", commits[k]).split()
                linha.append({"tipo": "commit", "sha": commits[k][:7], "autor": nome,
                              "contexto": sid, "arquivos": arqs})
                k += 1
    if k != len(commits):
        print(f"aviso: {len(commits)} commit(s) em {base}..HEAD, {k} pareado(s) com chamada "
              "`git commit`; os demais ficam fora do rastro", file=sys.stderr)
    # aprovações por registro: inseridas de trás para a frente para não deslocar as posições
    inserir = []
    for p, txt in final.items():
        if not p.endswith(evidencia):
            continue
        pos, nome, sid = next(((v[0], v[1], v[2]) for e, v in ultima_escrita.items()
                               if e.endswith(p)), (len(linha), "?", "?"))
        for alvo, corpo in re.findall(r"(?m)^##\s*(\S+)\s*\n(.*?)(?=^##\s|\Z)", txt, re.S):
            for quem in re.findall(r"(?m)^Aprovado por:\s*(\S+)", corpo):
                inserir.append((pos, {"tipo": "aprovacao", "quem": quem,
                                      "papel": "humano" if quem in humanos else "agente",
                                      "contexto": "humano" if quem in humanos else sid,
                                      "alvo": alvo, "evidencia": p}))
    for pos, ev in sorted(inserir, key=lambda x: -x[0]):
        linha.insert(pos, ev)
    linha.append({"tipo": "resposta", "texto": resposta or ""})
    return {"base": arquivos_do_commit(repo, base), "final": final, "linha": linha}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo", required=True)
    ap.add_argument("--base", required=True)
    ap.add_argument("--sessao", action="append", required=True, help="nome=transcript.jsonl")
    ap.add_argument("--humano", action="append", default=[])
    ap.add_argument("--evidencia", default="qa-report.md")
    a = ap.parse_args()
    sessoes = [tuple(s.split("=", 1)) for s in a.sessao]
    rastro = montar(a.repo, a.base, sessoes, set(a.humano), a.evidencia)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    json.dump(rastro, sys.stdout, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
