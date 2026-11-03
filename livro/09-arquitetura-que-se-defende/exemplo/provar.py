"""Prova por mutação dos portões de arquitetura do capítulo 9.

Para cada portão: roda no projeto como está (tem de ficar verde), em fixtures legítimas
(o mundo certo de um jeito incômodo — tem de ficar verde) e em cada mutação da sua família
(o mundo quebrado de propósito — tem de ficar vermelho). Portão que deixa mutação viva, ou
que reprova o mundo certo, é DECORAÇÃO.

Cada mutação roda numa CÓPIA temporária do projeto; a pasta `projeto/` nunca é alterada.

Uso:  python3 provar.py          (no Git Bash do Windows, `python provar.py`)
Saída: 0 quando os portões "/fato" são todos PORTÃO e os ingênuos são todos DECORAÇÃO
       (é isso que o capítulo afirma); 1 em qualquer outro caso.
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile

from portoes import PORTOES

AQUI = os.path.dirname(os.path.abspath(__file__))
PROJETO = os.path.join(AQUI, "projeto")


# ----------------------------------------------------------------- ferramentas de mutação


def _editar_json(raiz, caminho, fn):
    p = os.path.join(raiz, caminho)
    with open(p, encoding="utf-8") as f:
        dado = json.load(f)
    fn(dado)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(dado, f, ensure_ascii=False, indent=2)


def _trocar(raiz, caminho, antes, depois):
    p = os.path.join(raiz, caminho)
    with open(p, encoding="utf-8") as f:
        texto = f.read()
    assert antes in texto, f"mutação não se aplica: {antes!r} ausente em {caminho}"
    with open(p, "w", encoding="utf-8") as f:
        f.write(texto.replace(antes, depois, 1))


def _criar(raiz, caminho, texto):
    p = os.path.join(raiz, caminho)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(texto)


PEDIDO = "servidor/dominio/pedido.py"
ANCORA = "from .erros import TransicaoInvalida\n"
REGISTRO = "servidor/adaptadores/registro_arquivo.py"

# (família, nome, função que muta a cópia)
MUTACOES = [
    ("fronteira", "arquivo novo que nenhum domínio reivindica",
     lambda r: _criar(r, "notas/rascunho.md", "# rascunho\n")),
    ("fronteira", "o mesmo caminho reivindicado pelos dois domínios",
     lambda r: _editar_json(r, "fronteira.json",
                            lambda d: d["dominios"]["guia"]["possui"].append("docs/governanca/"))),
    ("fronteira", "caminho compartilhado sem dono",
     lambda r: _editar_json(r, "fronteira.json", lambda d: d["compartilhado"].append("docs/rascunhos/"))),
    ("fronteira", "arquivo do toolkit publicado pelo canal de itens",
     lambda r: _editar_json(r, "publicar/sumario.json",
                            lambda d: d["partes"][0]["itens"].append({"arquivo": "scripts/interno.html"}))),
    ("fronteira", "arquivo do toolkit publicado pelo 2º canal (materiais)",
     lambda r: _editar_json(r, "publicar/sumario.json",
                            lambda d: d["materiais"].append({"arquivo": "scripts/interno.html"}))),
    ("fronteira", "arquivo do toolkit publicado por um 3º canal (anexos)",
     lambda r: _editar_json(r, "publicar/sumario.json",
                            lambda d: d.setdefault("anexos", []).append({"arquivo": "scripts/interno.html"}))),
    ("dependencias", "domínio faz import sqlite3",
     lambda r: _trocar(r, PEDIDO, ANCORA, ANCORA + "import sqlite3\n")),
    ("dependencias", "domínio faz from sqlite3 import connect",
     lambda r: _trocar(r, PEDIDO, ANCORA, ANCORA + "from sqlite3 import connect\n")),
    ("dependencias", "domínio importa o adaptador por import relativo",
     lambda r: _trocar(r, PEDIDO, ANCORA, ANCORA + "from ..adaptadores import registro_arquivo\n")),
    ("dependencias", "domínio usa __import__('sqlite3')",
     lambda r: _trocar(r, PEDIDO, ANCORA, ANCORA + "_banco = __import__('sqlite3')\n")),
    ("dependencias", "porta importa o adaptador",
     lambda r: _trocar(r, "servidor/portas/registro.py", "from servidor.dominio.pedido import Pedido\n",
                       "from servidor.dominio.pedido import Pedido\n"
                       "from servidor.adaptadores.registro_falso import RegistroFalso\n")),
    ("registro", "registro aberto em modo 'w'",
     lambda r: _trocar(r, REGISTRO, 'open(self.caminho, "a", encoding="utf-8")',
                       'open(self.caminho, "w", encoding="utf-8")')),
    ("registro", "registro aberto com mode='w' por palavra-chave",
     lambda r: _trocar(r, REGISTRO, 'open(self.caminho, "a", encoding="utf-8")',
                       'open(self.caminho, mode="w", encoding="utf-8")')),
    ("registro", "registro truncado antes de escrever",
     lambda r: _trocar(r, REGISTRO, 'arquivo.write(linha + "\\n")',
                       'arquivo.truncate(0)\n            arquivo.write(linha + "\\n")')),
    ("portas", "a porta perde o adaptador falso",
     lambda r: os.remove(os.path.join(r, "servidor/adaptadores/registro_falso.py"))),
]

# o mundo certo, de um jeito incômodo: nenhum portão pode reprovar
LEGITIMAS = [
    ("página compartilhada publicada como material",
     lambda r: _editar_json(r, "publicar/sumario.json",
                            lambda d: d["materiais"].append({"arquivo": "docs/governanca/principios.md"}))),
    ("domínio importa json e um módulo irmão",
     lambda r: _trocar(r, PEDIDO, ANCORA, ANCORA + "import json\nfrom . import erros\n")),
    ("adaptador abre o registro em 'a+' para ler e acrescentar",
     lambda r: _trocar(r, REGISTRO, 'open(self.caminho, "a", encoding="utf-8")',
                       'open(self.caminho, "a+", encoding="utf-8")')),
]


def cenario(muta=None) -> dict:
    """Monta UMA cópia do projeto (mutada ou não) e roda nela todos os portões.
    Os portões só leem, então uma cópia serve a todos."""
    with tempfile.TemporaryDirectory() as tmp:
        copia = os.path.join(tmp, "projeto")
        shutil.copytree(PROJETO, copia, ignore=shutil.ignore_patterns("__pycache__"))
        if muta:
            muta(copia)
        return {nome: portao(copia) for nome, portao in PORTOES.items()}


def main() -> int:
    base = cenario()
    legitimas = [(desc, cenario(muta)) for desc, muta in LEGITIMAS]
    mutadas = [(familia, desc, cenario(muta)) for familia, desc, muta in MUTACOES]
    tudo_certo = True
    resumo = {"PORTÃO": 0, "DECORAÇÃO": 0}
    for nome in PORTOES:
        familia = nome.split("/")[0]
        problemas = []
        if base[nome]:
            problemas.append(f"vermelho no projeto como está: {base[nome][0]}")
        for desc, res in legitimas:
            if res[nome]:
                problemas.append(f"falso vermelho em '{desc}': {res[nome][0]}")
        da_familia = [(desc, res) for f, desc, res in mutadas if f == familia]
        mortas = 0
        for desc, res in da_familia:
            if res[nome]:
                mortas += 1
            else:
                problemas.append(f"mutação sobreviveu: '{desc}'")
        veredito = "PORTÃO" if not problemas else "DECORAÇÃO"
        resumo[veredito] += 1
        print(f"{nome:22s} mutações mortas {mortas}/{len(da_familia)}  →  {veredito}")
        for p in problemas:
            print(f"    ✗ {p}")
        esperado = "PORTÃO" if nome.endswith("/fato") else "DECORAÇÃO"
        tudo_certo &= veredito == esperado
    print(f"resumo: {len(PORTOES)} portões provados, {resumo['PORTÃO']} portão(ões), "
          f"{resumo['DECORAÇÃO']} decoração(ões)")
    print("✓ o resultado bate com o capítulo" if tudo_certo else "✗ o resultado NÃO bate com o capítulo")
    return 0 if tudo_certo else 1


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
