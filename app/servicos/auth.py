"""Regras de autenticacao (RF20)."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.excecoes import CredenciaisInvalidasError
from app.core.seguranca import criar_token_acesso, verificar_senha
from app.modelos.usuario import Usuario
from app.repositorios import usuario as repo_usuario


async def autenticar(sessao: AsyncSession, email: str, senha: str) -> Usuario:
    usuario = await repo_usuario.obter_por_email(sessao, email)
    if usuario is None or not usuario.ativo or not verificar_senha(senha, usuario.senha_hash):
        raise CredenciaisInvalidasError("Email ou senha invalidos.")
    return usuario


def gerar_token_para_usuario(usuario: Usuario) -> str:
    return criar_token_acesso({"sub": usuario.email})
