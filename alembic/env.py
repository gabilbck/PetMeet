import asyncio

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# Garante que app/modelos/__init__.py seja executado, registrando todos os
# modelos em Base.metadata antes do autogenerate comparar o estado do banco.
from app.core.config import obter_configuracoes
from app.db.base import Base
from app.modelos import *  # noqa: F401,F403

config = context.config
configuracoes = obter_configuracoes()

# A URL de conexao vem sempre das variaveis de ambiente (.env), nunca do alembic.ini (RNF16).
config.set_main_option("sqlalchemy.url", configuracoes.DATABASE_URL)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=configuracoes.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def _executar_migracoes_sync(conexao) -> None:
    context.configure(connection=conexao, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    conectavel = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with conectavel.connect() as conexao:
        await conexao.run_sync(_executar_migracoes_sync)

    await conectavel.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
