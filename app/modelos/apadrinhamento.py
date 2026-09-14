"""Associacao M:N entre Padrinho e Pet (RF10), com a frequencia da contribuicao (RF11)."""

from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.modelos.enums import FrequenciaContribuicao, coluna_enum


class Apadrinhamento(Base):
    __tablename__ = "apadrinhamentos"
    __table_args__ = (
        UniqueConstraint("padrinho_id", "pet_id", name="uq_apadrinhamento_padrinho_pet"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    padrinho_id: Mapped[int] = mapped_column(
        ForeignKey("padrinhos.id", ondelete="CASCADE"), index=True
    )
    pet_id: Mapped[int] = mapped_column(ForeignKey("pets.id", ondelete="CASCADE"), index=True)
    frequencia: Mapped[FrequenciaContribuicao] = mapped_column(
        coluna_enum(FrequenciaContribuicao, "frequencia_contribuicao"),
        nullable=False,
    )
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    data_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    padrinho: Mapped["Padrinho"] = relationship(back_populates="apadrinhamentos")  # noqa: F821
    pet: Mapped["Pet"] = relationship(back_populates="apadrinhamentos")  # noqa: F821
