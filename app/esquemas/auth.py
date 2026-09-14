"""Schemas de autenticacao (RF20)."""

from pydantic import BaseModel


class TokenResposta(BaseModel):
    access_token: str
    token_type: str = "bearer"
