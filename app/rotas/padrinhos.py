"""Rotas de Padrinho (RF09-11). Dado pessoal sensivel: exige autenticacao (RN07/LGPD)."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.dependencias import SessaoAsync, requer_perfil
from app.esquemas.comuns import PaginaResposta
from app.esquemas.padrinho import PadrinhoAtualizar, PadrinhoCriar, PadrinhoResposta
from app.modelos.enums import PerfilUsuario
from app.servicos import padrinho as servico_padrinho

roteador = APIRouter(prefix="/padrinhos", tags=["Padrinhos"])

_requer_equipe = Depends(requer_perfil(PerfilUsuario.ADMIN, PerfilUsuario.VOLUNTARIO))


@roteador.post(
    "",
    response_model=PadrinhoResposta,
    status_code=status.HTTP_201_CREATED,
    dependencies=[_requer_equipe],
)
async def criar_padrinho(sessao: SessaoAsync, dados: PadrinhoCriar) -> PadrinhoResposta:
    padrinho = await servico_padrinho.criar_padrinho(sessao, dados)
    return PadrinhoResposta.model_validate(padrinho)


@roteador.get("", response_model=PaginaResposta[PadrinhoResposta], dependencies=[_requer_equipe])
async def listar_padrinhos(
    sessao: SessaoAsync,
    pagina: Annotated[int, Query(ge=1)] = 1,
    tamanho_pagina: Annotated[int, Query(ge=1, le=100)] = 20,
) -> PaginaResposta[PadrinhoResposta]:
    itens, total = await servico_padrinho.listar_padrinhos(sessao, pagina, tamanho_pagina)
    return PaginaResposta(
        itens=[PadrinhoResposta.model_validate(item) for item in itens],
        total=total,
        pagina=pagina,
        tamanho_pagina=tamanho_pagina,
    )


@roteador.get("/{padrinho_id}", response_model=PadrinhoResposta, dependencies=[_requer_equipe])
async def obter_padrinho(sessao: SessaoAsync, padrinho_id: int) -> PadrinhoResposta:
    padrinho = await servico_padrinho.obter_padrinho_ou_falhar(sessao, padrinho_id)
    return PadrinhoResposta.model_validate(padrinho)


@roteador.patch("/{padrinho_id}", response_model=PadrinhoResposta, dependencies=[_requer_equipe])
async def atualizar_padrinho(
    sessao: SessaoAsync, padrinho_id: int, dados: PadrinhoAtualizar
) -> PadrinhoResposta:
    padrinho = await servico_padrinho.atualizar_padrinho(sessao, padrinho_id, dados)
    return PadrinhoResposta.model_validate(padrinho)
