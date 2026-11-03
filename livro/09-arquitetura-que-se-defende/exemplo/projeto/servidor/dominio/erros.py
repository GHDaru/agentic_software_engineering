"""Erros do domínio."""


class TransicaoInvalida(Exception):
    """A transição pedida viola a máquina de estados do agregado."""
