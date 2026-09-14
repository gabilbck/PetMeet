"""Configuracoes da aplicacao, lidas de variaveis de ambiente (RNF16)."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Configuracoes(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Banco de dados
    DATABASE_URL: str = "postgresql+asyncpg://petmeet:petmeet@localhost:5432/petmeet"
    DATABASE_URL_TESTE: str = "postgresql+asyncpg://petmeet:petmeet@localhost:5432/petmeet_teste"

    # Autenticacao
    SECRET_KEY: str = "chave-de-desenvolvimento-nao-usar-em-producao"
    ALGORITMO_JWT: str = "HS256"
    TOKEN_EXPIRACAO_MINUTOS: int = 60

    # CORS
    ORIGENS_PERMITIDAS: str = "http://localhost:3000,http://localhost:5173"

    # Upload de fotos
    DIRETORIO_UPLOADS: str = "uploads"
    TAMANHO_MAX_UPLOAD_MB: int = 5
    FORMATOS_IMAGEM_PERMITIDOS: tuple[str, ...] = ("image/jpeg", "image/png", "image/webp")

    # Ambiente
    AMBIENTE: str = "desenvolvimento"

    @property
    def lista_origens_permitidas(self) -> list[str]:
        return [origem.strip() for origem in self.ORIGENS_PERMITIDAS.split(",") if origem.strip()]


@lru_cache
def obter_configuracoes() -> Configuracoes:
    """Cache simples: le o .env uma unica vez por processo."""
    return Configuracoes()
