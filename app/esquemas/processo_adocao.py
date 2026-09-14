"""Schemas do processo de adocao (RF14-18)."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.modelos.enums import StatusProcessoAdocao


class ProcessoAdocaoCriar(BaseModel):
    pet_id: int
    adotante_id: int


class ProcessoAdocaoAtualizarStatus(BaseModel):
    status: StatusProcessoAdocao
    # Usado apenas quando status == FINALIZADO e o pet esta em tratamento medico (RN01).
    acompanhamento_medico_em_dia: bool = False


class ProcessoAdocaoResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    pet_id: int
    adotante_id: int
    responsavel_id: int | None
    status: StatusProcessoAdocao
    acompanhamento_medico_em_dia: bool
    criado_em: datetime
    atualizado_em: datetime
