"""Acesso a dados de ProcessoAdocao (RF14-18)."""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modelos.processo_adocao import ProcessoAdocao


async def criar(sessao: AsyncSession, processo: ProcessoAdocao) -> ProcessoAdocao:
    sessao.add(processo)
    await sessao.flush()
    return processo


async def obter_por_id(sessao: AsyncSession, processo_id: int) -> ProcessoAdocao | None:
    return await sessao.get(ProcessoAdocao, processo_id)


async def listar(
    sessao: AsyncSession,
    pagina: int,
    tamanho_pagina: int,
    pet_id: int | None = None,
    adotante_id: int | None = None,
) -> tuple[list[ProcessoAdocao], int]:
    consulta = select(ProcessoAdocao)
    if pet_id is not None:
        consulta = consulta.where(ProcessoAdocao.pet_id == pet_id)
    if adotante_id is not None:
        consulta = consulta.where(ProcessoAdocao.adotante_id == adotante_id)

    total = (
        await sessao.execute(select(func.count()).select_from(consulta.subquery()))
    ).scalar_one()

    consulta = (
        consulta.order_by(ProcessoAdocao.criado_em.desc())
        .offset((pagina - 1) * tamanho_pagina)
        .limit(tamanho_pagina)
    )
    itens = (await sessao.execute(consulta)).scalars().all()
    return list(itens), total
