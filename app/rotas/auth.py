"""Rota de login (RF20)."""

from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencias import SessaoAsync
from app.esquemas.auth import TokenResposta
from app.servicos import auth as servico_auth

roteador = APIRouter(prefix="/auth", tags=["Autenticacao"])


@roteador.post("/login", response_model=TokenResposta)
async def login(
    sessao: SessaoAsync,
    formulario: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> TokenResposta:
    usuario = await servico_auth.autenticar(sessao, formulario.username, formulario.password)
    token = servico_auth.gerar_token_para_usuario(usuario)
    return TokenResposta(access_token=token)
