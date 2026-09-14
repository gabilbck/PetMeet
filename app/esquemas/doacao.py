"""Schemas de doacao (RF12, RF13, RN05)."""

from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.modelos.enums import FrequenciaContribuicao


class DoacaoCriar(BaseModel):
    padrinho_id: int | None = None
    doador_nome: str | None = Field(None, max_length=150)
    valor: Decimal = Field(..., gt=0, description="Valor da doacao, deve ser maior que zero (RN05)")
    data: date
    tipo: FrequenciaContribuicao

    @model_validator(mode="after")
    def validar_origem_doacao(self) -> "DoacaoCriar":
        # A doacao precisa ser rastreavel a alguem: um padrinho cadastrado ou um doador avulso.
        if self.padrinho_id is None and not self.doador_nome:
            raise ValueError("informe padrinho_id ou doador_nome")
        return self


class DoacaoResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    padrinho_id: int | None
    doador_nome: str | None
    valor: Decimal
    data: date
    tipo: FrequenciaContribuicao
    criado_em: datetime
