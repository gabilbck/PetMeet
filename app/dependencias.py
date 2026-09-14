"""Dependencias compartilhadas do FastAPI: sessao de banco, usuario autenticado e permissoes."""

from collections.abc import Callable, Coroutine
from typing import Annotated, Any

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.excecoes import CredenciaisInvalidasError, NaoAutorizadoError
from app.core.seguranca import decodificar_token_acesso
from app.db.sessao import obter_sessao
from app.modelos.enums import PerfilUsuario
from app.modelos.usuario import Usuario
from app.repositorios import usuario as repo_usuario

oauth2_esquema = OAuth2PasswordBearer(tokenUrl="/auth/login")

SessaoAsync = Annotated[AsyncSession, Depends(obter_sessao)]


async def obter_usuario_atual(
    token: Annotated[str, Depends(oauth2_esquema)],
    sessao: SessaoAsync,
) -> Usuario:
    """Decodifica o JWT e carrega o usuario correspondente (RF20)."""
    payload = decodificar_token_acesso(token)
    if payload is None or "sub" not in payload:
        raise CredenciaisInvalidasError("Token invalido ou expirado.")

    usuario = await repo_usuario.obter_por_email(sessao, payload["sub"])
    if usuario is None or not usuario.ativo:
        raise CredenciaisInvalidasError("Usuario invalido ou inativo.")
    return usuario


UsuarioAtual = Annotated[Usuario, Depends(obter_usuario_atual)]


def requer_perfil(
    *perfis_permitidos: PerfilUsuario,
) -> Callable[[UsuarioAtual], Coroutine[Any, Any, Usuario]]:
    """Fabrica de dependencia: bloqueia a rota para quem nao tiver um dos perfis informados
    (RN06/RF21). Uso: `usuario: Usuario = Depends(requer_perfil(PerfilUsuario.ADMIN))`.
    """

    async def _verificar(usuario: UsuarioAtual) -> Usuario:
        if usuario.perfil not in perfis_permitidos:
            raise NaoAutorizadoError("Usuario nao possui permissao para executar esta operacao.")
        return usuario

    return _verificar
