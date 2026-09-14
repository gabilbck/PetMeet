"""Engine assincrono e fabrica de sessoes do SQLAlchemy."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import obter_configuracoes

configuracoes = obter_configuracoes()

engine: AsyncEngine = create_async_engine(configuracoes.DATABASE_URL, pool_pre_ping=True)

FabricaSessao = async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)


async def obter_sessao() -> AsyncGenerator[AsyncSession, None]:
    """Dependencia do FastAPI: entrega uma sessao por requisicao e garante o fechamento."""
    async with FabricaSessao() as sessao:
        yield sessao
