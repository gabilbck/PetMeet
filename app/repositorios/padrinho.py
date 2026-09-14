"""Acesso a dados de Padrinho (RF09-11)."""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modelos.padrinho import Padrinho


async def criar(sessao: AsyncSession, padrinho: Padrinho) -> Padrinho:
    sessao.add(padrinho)
    await sessao.commit()
    await sessao.refresh(padrinho)
    return padrinho


async def obter_por_id(sessao: AsyncSession, padrinho_id: int) -> Padrinho | None:
    return await sessao.get(Padrinho, padrinho_id)


async def obter_por_cpf(sessao: AsyncSession, cpf: str) -> Padrinho | None:
    resultado = await sessao.execute(select(Padrinho).where(Padrinho.cpf == cpf))
    return resultado.scalar_one_or_none()


async def listar(
    sessao: AsyncSession, pagina: int, tamanho_pagina: int
) -> tuple[list[Padrinho], int]:
    total = (await sessao.execute(select(func.count()).select_from(Padrinho))).scalar_one()
    consulta = (
        select(Padrinho)
        .order_by(Padrinho.criado_em.desc())
        .offset((pagina - 1) * tamanho_pagina)
        .limit(tamanho_pagina)
    )
    itens = (await sessao.execute(consulta)).scalars().all()
    return list(itens), total


async def salvar(sessao: AsyncSession, padrinho: Padrinho) -> Padrinho:
    await sessao.commit()
    await sessao.refresh(padrinho)
    return padrinho
