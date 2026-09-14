"""Fabrica do armazenamento de arquivos usado pela aplicacao.

Centraliza a escolha da implementacao (hoje: local em disco). Trocar para um
provedor em nuvem no futuro e alterar so esta funcao.
"""

from app.armazenamento.base import ArmazenamentoBase
from app.armazenamento.local import ArmazenamentoLocal

_instancia: ArmazenamentoBase | None = None


def obter_armazenamento() -> ArmazenamentoBase:
    global _instancia
    if _instancia is None:
        _instancia = ArmazenamentoLocal()
    return _instancia
