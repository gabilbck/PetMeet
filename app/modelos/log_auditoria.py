"""Trilha de auditoria de alteracoes relevantes (RF22). Estrutura pronta para a fase 2."""

from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class LogAuditoria(Base):
    __tablename__ = "logs_auditoria"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=True
    )
    entidade: Mapped[str] = mapped_column(String(100), nullable=False)
    entidade_id: Mapped[int] = mapped_column(nullable=False)
    acao: Mapped[str] = mapped_column(String(50), nullable=False)
    dados_antigos: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    dados_novos: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
