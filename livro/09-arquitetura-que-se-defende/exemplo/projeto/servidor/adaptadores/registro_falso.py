"""Adaptador falso da porta Registro, para teste. Conta como segundo adaptador."""
from __future__ import annotations

from servidor.dominio.pedido import Pedido


class RegistroFalso:
    def __init__(self) -> None:
        self._linhas: list[str] = []

    def acrescenta(self, pedido: Pedido, evento: str) -> None:
        self._linhas.append(evento)

    def eventos(self) -> list[str]:
        return list(self._linhas)
