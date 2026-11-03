"""Porta Registro: acrescenta eventos e nunca os reescreve."""
from __future__ import annotations

from typing import Protocol

from servidor.dominio.pedido import Pedido


class Registro(Protocol):
    def acrescenta(self, pedido: Pedido, evento: str) -> None: ...
    def eventos(self) -> list[str]: ...
