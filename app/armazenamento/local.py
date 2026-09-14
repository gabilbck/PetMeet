"""Implementacao de armazenamento em disco local (padrao para desenvolvimento/ONG pequena)."""

import uuid
from pathlib import Path

from app.armazenamento.base import ArmazenamentoBase
from app.core.config import obter_configuracoes

configuracoes = obter_configuracoes()


class ArmazenamentoLocal(ArmazenamentoBase):
    def __init__(self, diretorio_base: str | None = None):
        self.diretorio_base = Path(diretorio_base or configuracoes.DIRETORIO_UPLOADS)
        self.diretorio_base.mkdir(parents=True, exist_ok=True)

    async def salvar(self, nome_arquivo: str, conteudo: bytes) -> str:
        extensao = Path(nome_arquivo).suffix
        nome_unico = f"{uuid.uuid4().hex}{extensao}"
        caminho = self.diretorio_base / nome_unico
        caminho.write_bytes(conteudo)
        return f"/{self.diretorio_base.as_posix()}/{nome_unico}"

    def excluir(self, url: str) -> None:
        nome_arquivo = Path(url).name
        caminho = self.diretorio_base / nome_arquivo
        caminho.unlink(missing_ok=True)
