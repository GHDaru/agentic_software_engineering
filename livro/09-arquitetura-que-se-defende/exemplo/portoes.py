"""Portões de arquitetura (fitness functions) do capítulo 9.

Cada portão recebe a raiz de um projeto e devolve a lista de violações. Lista vazia = verde.
Só biblioteca padrão. Os portões leem o DISCO e a declaração (`fronteira.json`), nunca uma
lista própria: a fonte da regra é uma só.

Há portões "ingênuos" de propósito, cada um na forma de um portão real antes de alguém o
quebrar. O harness (`provar.py`) mostra que eles passam no caminho feliz e deixam mutações
vivas — são a lição, não o modelo.
"""
from __future__ import annotations

import ast
import json
import os
import re

# --------------------------------------------------------------------------- utilidades


def arquivos(raiz: str) -> list[str]:
    """Todo arquivo do projeto, com caminho relativo e barra normal, em ordem estável."""
    out = []
    for pasta, subpastas, nomes in os.walk(raiz):
        subpastas[:] = sorted(d for d in subpastas if d != "__pycache__")
        for nome in sorted(nomes):
            if nome.endswith(".pyc"):
                continue
            out.append(os.path.relpath(os.path.join(pasta, nome), raiz).replace(os.sep, "/"))
    return out


def _json(raiz: str, caminho: str):
    with open(os.path.join(raiz, caminho), encoding="utf-8") as f:
        return json.load(f)


def dono(caminho: str, dominios: dict) -> str | None:
    """O domínio que reivindica o caminho. Prefixo mais longo vence; empate é AMBIGUO."""
    achados = []
    for nome, dom in dominios.items():
        for prefixo in dom["possui"]:
            if caminho == prefixo or caminho.startswith(prefixo):
                achados.append((len(prefixo), nome))
    if not achados:
        return None
    maior = max(n for n, _ in achados)
    vencedores = {d for n, d in achados if n == maior}
    return "AMBIGUO" if len(vencedores) > 1 else vencedores.pop()


# --------------------------------------------------------------- 1. a fronteira decidível


def _paginas_por_nome(sumario: dict, canais: tuple[str, ...]) -> list[str]:
    """Páginas publicadas, lidas pelos NOMES de canal que o portão conhece."""
    paginas = []
    if "itens" in canais:
        paginas += [i["arquivo"] for p in sumario.get("partes", []) for i in p.get("itens", [])]
    if "materiais" in canais:
        paginas += [m["arquivo"] for m in sumario.get("materiais", [])]
    return paginas


def _paginas_por_fato(no) -> list[str]:
    """Páginas publicadas, lidas pelo FATO: todo campo `arquivo`, em qualquer canal."""
    if isinstance(no, dict):
        achadas = [no["arquivo"]] if isinstance(no.get("arquivo"), str) else []
        for valor in no.values():
            achadas += _paginas_por_fato(valor)
        return achadas
    if isinstance(no, list):
        return [p for item in no for p in _paginas_por_fato(item)]
    return []


def _fronteira(raiz: str, ler_paginas) -> list[str]:
    decl = _json(raiz, "fronteira.json")
    dominios, compartilhado = decl["dominios"], decl["compartilhado"]
    erros = []
    # invariante 1: todo arquivo tem exatamente um dono
    for f in arquivos(raiz):
        d = dono(f, dominios)
        if d is None:
            erros.append(f"órfão (nenhum domínio o reivindica): {f}")
        elif d == "AMBIGUO":
            erros.append(f"reivindicado pelos dois domínios: {f}")
    # invariante 2: caminho compartilhado tem dono, e o dono é o toolkit
    for c in compartilhado:
        if dono(c, dominios) != "toolkit":
            erros.append(f"compartilhado sem dono no toolkit: {c} (dono: {dono(c, dominios)})")
    # invariante 3: toda página publicada vem do guia ou de caminho compartilhado
    for p in ler_paginas(_json(raiz, "publicar/sumario.json")):
        if dono(p, dominios) == "guia" or any(p.startswith(c) for c in compartilhado):
            continue
        erros.append(f"publicada sem origem declarada: {p} (dono: {dono(p, dominios)})")
    return erros


def fronteira_um_canal(raiz: str) -> list[str]:
    """Ingênuo nº 1: lê só `itens` (a forma do portão antes do segundo canal)."""
    return _fronteira(raiz, lambda s: _paginas_por_nome(s, ("itens",)))


def fronteira_dois_canais(raiz: str) -> list[str]:
    """Ingênuo nº 2: lê `itens` e `materiais` pelo nome (a correção pontual)."""
    return _fronteira(raiz, lambda s: _paginas_por_nome(s, ("itens", "materiais")))


def fronteira(raiz: str) -> list[str]:
    """O portão: lê toda página publicada, por qualquer canal, pelo campo `arquivo`."""
    return _fronteira(raiz, _paginas_por_fato)


# ------------------------------------------------------- 2. a direção das dependências

IO_PROIBIDO = {"os", "sqlite3", "socket", "subprocess", "urllib", "http", "shutil",
               "tempfile", "pathlib", "requests", "io", "time"}


def _importados(caminho: str, pacote: str) -> set[str]:
    """Módulos importados, com import relativo resolvido para o nome absoluto."""
    with open(caminho, encoding="utf-8") as f:
        arvore = ast.parse(f.read(), filename=caminho)
    nomes: set[str] = set()
    for no in ast.walk(arvore):
        if isinstance(no, ast.Import):
            nomes.update(a.name for a in no.names)
        elif isinstance(no, ast.ImportFrom):
            base = no.module or ""
            if no.level:
                partes = pacote.split(".")
                partes = partes[: len(partes) - (no.level - 1)]
                base = ".".join(partes + ([no.module] if no.module else []))
                if not no.module:  # from .. import x
                    nomes.update(f"{base}.{a.name}" for a in no.names)
            nomes.add(base)
        elif isinstance(no, ast.Call) and getattr(no.func, "id", "") == "__import__":
            if no.args and isinstance(no.args[0], ast.Constant):
                nomes.add(str(no.args[0].value))
    return nomes


def _modulos(raiz: str, camada: str):
    base = os.path.join(raiz, "servidor", camada)
    for f in arquivos(base):
        if f.endswith(".py"):
            pacote = "servidor." + camada + ("." + os.path.dirname(f).replace("/", ".")
                                              if os.path.dirname(f) else "")
            yield os.path.join(base, f), f"servidor/{camada}/{f}", pacote


def dependencias_por_texto(raiz: str) -> list[str]:
    """Ingênuo nº 3: procura a LINHA `import <io>` ou `adaptadores` no texto do domínio."""
    erros = []
    padrao = re.compile(r"^import (%s)\b" % "|".join(sorted(IO_PROIBIDO)), re.M)
    for caminho, rel, _ in _modulos(raiz, "dominio"):
        texto = open(caminho, encoding="utf-8").read()
        if padrao.search(texto) or "from servidor.adaptadores" in texto:
            erros.append(f"domínio fala com o mundo: {rel}")
    return erros


def dependencias(raiz: str) -> list[str]:
    """O portão: lê a árvore sintática. O domínio não importa I/O nem porta nem adaptador;
    a porta não importa adaptador. A seta aponta para dentro, sempre."""
    erros = []
    for camada, proibidos in (("dominio", ("servidor.portas", "servidor.adaptadores")),
                              ("portas", ("servidor.adaptadores",))):
        for caminho, rel, pacote in _modulos(raiz, camada):
            for nome in sorted(_importados(caminho, pacote)):
                if camada == "dominio" and nome.split(".")[0] in IO_PROIBIDO:
                    erros.append(f"{rel} importa I/O: {nome}")
                if any(nome == p or nome.startswith(p + ".") for p in proibidos):
                    erros.append(f"{rel} importa camada de fora: {nome}")
    return erros


# --------------------------------------------------- 3. o registro que só cresce


def _modo(chamada: ast.Call) -> str:
    modo = "r"
    if len(chamada.args) >= 2 and isinstance(chamada.args[1], ast.Constant):
        modo = str(chamada.args[1].value)
    for kw in chamada.keywords:
        if kw.arg == "mode":
            modo = str(kw.value.value) if isinstance(kw.value, ast.Constant) else "?"
    return modo


def so_acrescenta(raiz: str) -> list[str]:
    """O portão: o adaptador do registro abre só para ler ou acrescentar, e nunca trunca
    nem reposiciona. Modo que não é constante conta como violação: não dá para provar."""
    rel = "servidor/adaptadores/registro_arquivo.py"
    with open(os.path.join(raiz, rel), encoding="utf-8") as f:
        arvore = ast.parse(f.read())
    erros, acrescenta = [], False
    for no in ast.walk(arvore):
        if not isinstance(no, ast.Call):
            continue
        nome = getattr(no.func, "id", None) or getattr(no.func, "attr", None)
        if nome == "open":
            m = _modo(no)
            if m == "?" or any(c in m for c in "wx") or m.startswith("r+"):
                erros.append(f"{rel}:{no.lineno} abre em modo que reescreve: {m!r}")
            acrescenta |= "a" in m
        elif nome in ("truncate", "seek"):
            erros.append(f"{rel}:{no.lineno} chama {nome}(): o passado deixa de ser imutável")
    if not acrescenta:
        erros.append(f"{rel}: nenhum open em modo de acréscimo")
    return erros


# ------------------------------------------- 4. porta com dois adaptadores (contando o falso)


def porta_com_dois_adaptadores(raiz: str) -> list[str]:
    """Porta só existe onde há dois adaptadores hoje, contando o falso de teste."""
    erros = []
    adaptadores = [os.path.basename(f) for f in arquivos(os.path.join(raiz, "servidor", "adaptadores"))]
    for f in arquivos(os.path.join(raiz, "servidor", "portas")):
        porta = os.path.basename(f)[:-3]
        if porta == "__init__":
            continue
        n = sum(1 for a in adaptadores if a.startswith(porta + "_") and a.endswith(".py"))
        if n < 2:
            erros.append(f"porta '{porta}' com {n} adaptador(es): porta sem segundo adaptador é cerimônia")
    return erros


PORTOES = {
    "fronteira/um-canal": fronteira_um_canal,
    "fronteira/dois-canais": fronteira_dois_canais,
    "fronteira/fato": fronteira,
    "dependencias/texto": dependencias_por_texto,
    "dependencias/fato": dependencias,
    "registro/fato": so_acrescenta,
    "portas/fato": porta_com_dois_adaptadores,
}
