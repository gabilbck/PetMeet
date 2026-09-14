"""Acesso a dados de Doacao (RF12, RF13)."""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modelos.doacao import Doacao


async def criar(sessao: AsyncSession, doacao: Doacao) -> Doacao:
    sessao.add(doacao)
    await sessao.commit()
    await sessao.refresh(doacao)
    return doacao


async def listar(
    sessao: AsyncSession, pagina: int, tamanho_pagina: int, padrinho_id: int | None = None
) -> tuple[list[Doacao], int]:
    consulta = select(Doacao)
    if padrinho_id is not None:
        consulta = consulta.where(Doacao.padrinho_id == padrinho_id)

    total = (
        await sessao.execute(select(func.count()).select_from(consulta.subquery()))
    ).scalar_one()

    consulta = (
        consulta.order_by(Doacao.data.desc())
        .offset((pagina - 1) * tamanho_pagina)
        .limit(tamanho_pagina)
    )
    itens = (await sessao.execute(consulta)).scalars().all()
    return list(itens), total
