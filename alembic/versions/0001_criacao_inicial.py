"""criacao inicial do schema PetMeet

Revision ID: 0001
Revises:
Create Date: 2026-09-13

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "usuarios",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nome", sa.String(length=150), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("senha_hash", sa.String(length=255), nullable=False),
        sa.Column(
            "perfil",
            sa.Enum("admin", "voluntario", name="perfil_usuario"),
            nullable=False,
        ),
        sa.Column("ativo", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("email", name="uq_usuarios_email"),
    )
    op.create_index("ix_usuarios_email", "usuarios", ["email"])

    op.create_table(
        "pets",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nome", sa.String(length=100), nullable=False),
        sa.Column(
            "especie", sa.Enum("cachorro", "gato", "outro", name="especie_pet"), nullable=False
        ),
        sa.Column("idade", sa.Integer(), nullable=False),
        sa.Column("data_resgate", sa.Date(), nullable=False),
        sa.Column(
            "status_saude",
            sa.Enum("saudavel", "em_tratamento_medico", "em_recuperacao", name="status_saude_pet"),
            nullable=False,
        ),
        sa.Column("doenca_atual", sa.String(length=255), nullable=True),
        sa.Column(
            "situacao_adocao",
            sa.Enum("disponivel", "em_processo_adocao", "adotado", name="situacao_adocao_pet"),
            nullable=False,
        ),
        sa.Column("foto_url", sa.String(length=500), nullable=True),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column(
            "atualizado_em",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
    )
    op.create_index("ix_pets_situacao_adocao", "pets", ["situacao_adocao"])
    op.create_index("ix_pets_status_saude", "pets", ["status_saude"])

    op.create_table(
        "adotantes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nome", sa.String(length=150), nullable=False),
        sa.Column("cpf", sa.String(length=11), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("telefone", sa.String(length=20), nullable=False),
        sa.Column("endereco", sa.String(length=255), nullable=False),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("cpf", name="uq_adotantes_cpf"),
    )
    op.create_index("ix_adotantes_cpf", "adotantes", ["cpf"])

    op.create_table(
        "padrinhos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nome", sa.String(length=150), nullable=False),
        sa.Column("cpf", sa.String(length=11), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("telefone", sa.String(length=20), nullable=False),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("cpf", name="uq_padrinhos_cpf"),
    )
    op.create_index("ix_padrinhos_cpf", "padrinhos", ["cpf"])

    op.create_table(
        "apadrinhamentos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "padrinho_id",
            sa.Integer(),
            sa.ForeignKey("padrinhos.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "pet_id", sa.Integer(), sa.ForeignKey("pets.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column(
            "frequencia",
            sa.Enum("pontual", "recorrente", name="frequencia_contribuicao"),
            nullable=False,
        ),
        sa.Column("ativo", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("data_inicio", sa.Date(), nullable=False),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("padrinho_id", "pet_id", name="uq_apadrinhamento_padrinho_pet"),
    )
    op.create_index("ix_apadrinhamentos_padrinho_id", "apadrinhamentos", ["padrinho_id"])
    op.create_index("ix_apadrinhamentos_pet_id", "apadrinhamentos", ["pet_id"])

    op.create_table(
        "processos_adocao",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "pet_id", sa.Integer(), sa.ForeignKey("pets.id", ondelete="RESTRICT"), nullable=False
        ),
        sa.Column(
            "adotante_id",
            sa.Integer(),
            sa.ForeignKey("adotantes.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column(
            "responsavel_id",
            sa.Integer(),
            sa.ForeignKey("usuarios.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "status",
            sa.Enum(
                "em_analise", "aprovado", "finalizado", "cancelado", name="status_processo_adocao"
            ),
            nullable=False,
        ),
        sa.Column(
            "acompanhamento_medico_em_dia",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column(
            "atualizado_em",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
    )
    op.create_index("ix_processos_adocao_pet_id", "processos_adocao", ["pet_id"])
    op.create_index("ix_processos_adocao_adotante_id", "processos_adocao", ["adotante_id"])
    op.create_index("ix_processos_adocao_status", "processos_adocao", ["status"])
    # RN02/RF17: garante no banco que um pet nunca tenha dois processos 'finalizado'
    # simultaneamente, mesmo sob concorrencia (RNF18).
    op.create_index(
        "uq_processo_adocao_pet_finalizado",
        "processos_adocao",
        ["pet_id"],
        unique=True,
        postgresql_where=sa.text("status = 'finalizado'"),
    )

    op.create_table(
        "doacoes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "padrinho_id",
            sa.Integer(),
            sa.ForeignKey("padrinhos.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("doador_nome", sa.String(length=150), nullable=True),
        sa.Column("valor", sa.Numeric(10, 2), nullable=False),
        sa.Column("data", sa.Date(), nullable=False),
        sa.Column("tipo", sa.Enum("pontual", "recorrente", name="tipo_doacao"), nullable=False),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.CheckConstraint("valor > 0", name="ck_doacao_valor_positivo"),
    )
    op.create_index("ix_doacoes_padrinho_id", "doacoes", ["padrinho_id"])
    op.create_index("ix_doacoes_data", "doacoes", ["data"])

    op.create_table(
        "logs_auditoria",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "usuario_id",
            sa.Integer(),
            sa.ForeignKey("usuarios.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("entidade", sa.String(length=100), nullable=False),
        sa.Column("entidade_id", sa.Integer(), nullable=False),
        sa.Column("acao", sa.String(length=50), nullable=False),
        sa.Column("dados_antigos", sa.JSON(), nullable=True),
        sa.Column("dados_novos", sa.JSON(), nullable=True),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("logs_auditoria")
    op.drop_table("doacoes")
    op.drop_index("uq_processo_adocao_pet_finalizado", table_name="processos_adocao")
    op.drop_table("processos_adocao")
    op.drop_table("apadrinhamentos")
    op.drop_table("padrinhos")
    op.drop_table("adotantes")
    op.drop_table("pets")
    op.drop_table("usuarios")

    for nome_enum in (
        "tipo_doacao",
        "status_processo_adocao",
        "frequencia_contribuicao",
        "situacao_adocao_pet",
        "status_saude_pet",
        "especie_pet",
        "perfil_usuario",
    ):
        op.execute(f"DROP TYPE IF EXISTS {nome_enum}")
