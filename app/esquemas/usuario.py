"""Schemas do usuario da equipe da ONG (RF20, RF21)."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.modelos.enums import PerfilUsuario


class UsuarioCriar(BaseModel):
    nome: str = Field(..., min_length=2, max_length=150)
    email: EmailStr
    senha: str = Field(..., min_length=8, max_length=100)
    perfil: PerfilUsuario


class UsuarioResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    email: EmailStr
    perfil: PerfilUsuario
    ativo: bool
    criado_em: datetime
