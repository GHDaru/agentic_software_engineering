"""Adaptador real da porta Registro: um arquivo JSON Lines, só de acréscimo."""
from __future__ import annotations

import json
import threading

from servidor.dominio.pedido import Pedido

_TRAVA = threading.Lock()


class RegistroEmArquivo:
    def __init__(self, caminho: str) -> None:
        self.caminho = caminho

    def acrescenta(self, pedido: Pedido, evento: str) -> None:
        linha = json.dumps({"pedido": pedido.id, "evento": evento}, ensure_ascii=False)
        with _TRAVA, open(self.caminho, "a", encoding="utf-8") as arquivo:
            arquivo.write(linha + "\n")

    def eventos(self) -> list[str]:
        with open(self.caminho, encoding="utf-8") as arquivo:
            return [json.loads(l)["evento"] for l in arquivo if l.strip()]
