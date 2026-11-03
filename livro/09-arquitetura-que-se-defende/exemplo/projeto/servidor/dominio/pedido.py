"""O agregado Pedido. Invariante: um pedido aprovado não volta a rascunho."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .erros import TransicaoInvalida

ESTADOS = ("rascunho", "aprovado", "cancelado")


@dataclass(frozen=True)
class Pedido:
    id: str
    estado: str = "rascunho"

    def aprovar(self, agora: datetime) -> "Pedido":
        # o relógio é argumento: o domínio não lê o ambiente
        if self.estado != "rascunho":
            raise TransicaoInvalida(f"{self.id}: {self.estado} -> aprovado")
        return Pedido(self.id, "aprovado")
