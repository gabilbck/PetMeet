"""Acesso a dados de Adotante (RF06-08)."""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modelos.adotante import Adotante


async def criar(sessao: AsyncSession, adotante: Adotante) -> Adotante:
    sessao.add(adotante)
    await sessao.commit()
    await sessao.refresh(adotante)
    return adotante


async def obter_por_id(sessao: AsyncSession, adotante_id: int) -> Adotante | None:
    return await sessao.get(Adotante, adotante_id)


async def obter_por_cpf(sessao: AsyncSession, cpf: str) -> Adotante | None:
    resultado = await sessao.execute(select(Adotante).where(Adotante.cpf == cpf))
    return resultado.scalar_one_or_none()


async def listar(
    sessao: AsyncSession, pagina: int, tamanho_pagina: int
) -> tuple[list[Adotante], int]:
    total = (await sessao.execute(select(func.count()).select_from(Adotante))).scalar_one()
    consulta = (
        select(Adotante)
        .order_by(Adotante.criado_em.desc())
        .offset((pagina - 1) * tamanho_pagina)
        .limit(tamanho_pagina)
    )
    itens = (await sessao.execute(consulta)).scalars().all()
    return list(itens), total


async def salvar(sessao: AsyncSession, adotante: Adotante) -> Adotante:
    await sessao.commit()
    await sessao.refresh(adotante)
    return adotante
