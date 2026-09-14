"""Interface de armazenamento de arquivos.

Hoje a unica implementacao e local (disco). Para trocar por um provedor em
nuvem (S3, MinIO, GCS) no futuro, basta criar uma nova classe que implemente
esta interface e ajustar a fabrica em app/armazenamento/__init__.py ou a
injecao de dependencia em app/dependencias.py -- os servicos que usam
armazenamento nao precisam mudar uma linha.
"""

from abc import ABC, abstractmethod


class ArmazenamentoBase(ABC):
    @abstractmethod
    async def salvar(self, nome_arquivo: str, conteudo: bytes) -> str:
        """Salva o conteudo e retorna a URL/caminho publico para acessa-lo."""

    @abstractmethod
    def excluir(self, url: str) -> None:
        """Remove um arquivo previamente salvo, a partir da URL/caminho retornado por salvar()."""
