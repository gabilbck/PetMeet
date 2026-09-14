"""Cadastro de usuarios da equipe da ONG. Restrito a administradores (RF21)."""

from fastapi import APIRouter, Depends, status

from app.dependencias import SessaoAsync, requer_perfil
from app.esquemas.usuario import UsuarioCriar, UsuarioResposta
from app.modelos.enums import PerfilUsuario
from app.servicos import usuario as servico_usuario

roteador = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"],
    dependencies=[Depends(requer_perfil(PerfilUsuario.ADMIN))],
)


@roteador.post("", response_model=UsuarioResposta, status_code=status.HTTP_201_CREATED)
async def criar_usuario(sessao: SessaoAsync, dados: UsuarioCriar) -> UsuarioResposta:
    usuario = await servico_usuario.criar_usuario(sessao, dados)
    return UsuarioResposta.model_validate(usuario)
