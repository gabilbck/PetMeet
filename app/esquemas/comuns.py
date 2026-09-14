"""Schemas reutilizaveis entre os modulos (paginacao - RNF08)."""

from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginaResposta(BaseModel, Generic[T]):
    itens: list[T]
    total: int
    pagina: int
    tamanho_pagina: int
