"""Acesso a dados de Usuario."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modelos.usuario import Usuario


async def obter_por_email(sessao: AsyncSession, email: str) -> Usuario | None:
    resultado = await sessao.execute(select(Usuario).where(Usuario.email == email))
    return resultado.scalar_one_or_none()


async def obter_por_id(sessao: AsyncSession, usuario_id: int) -> Usuario | None:
    return await sessao.get(Usuario, usuario_id)


async def criar(sessao: AsyncSession, usuario: Usuario) -> Usuario:
    sessao.add(usuario)
    await sessao.commit()
    await sessao.refresh(usuario)
    return usuario
