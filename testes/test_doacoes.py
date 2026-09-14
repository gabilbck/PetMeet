"""Testes de doacao (RF12, RF13, RN05)."""

from httpx import AsyncClient


async def test_criar_doacao_de_doador_avulso_com_valor_valido(
    client: AsyncClient, cabecalho_admin: dict
) -> None:
    dados = {
        "doador_nome": "Fulano da Silva",
        "valor": "50.00",
        "data": "2025-05-10",
        "tipo": "pontual",
    }

    resposta = await client.post("/doacoes", json=dados, headers=cabecalho_admin)

    assert resposta.status_code == 201
    assert resposta.json()["valor"] == "50.00"


async def test_criar_doacao_com_valor_zero_e_rejeitada(
    client: AsyncClient, cabecalho_admin: dict
) -> None:
    # RN05: o valor da doacao deve ser maior que zero.
    dados = {
        "doador_nome": "Fulano da Silva",
        "valor": "0",
        "data": "2025-05-10",
        "tipo": "pontual",
    }

    resposta = await client.post("/doacoes", json=dados, headers=cabecalho_admin)

    assert resposta.status_code == 422


async def test_criar_doacao_com_valor_negativo_e_rejeitada(
    client: AsyncClient, cabecalho_admin: dict
) -> None:
    dados = {
        "doador_nome": "Fulano da Silva",
        "valor": "-10.00",
        "data": "2025-05-10",
        "tipo": "pontual",
    }

    resposta = await client.post("/doacoes", json=dados, headers=cabecalho_admin)

    assert resposta.status_code == 422


async def test_criar_doacao_sem_padrinho_e_sem_doador_e_rejeitada(
    client: AsyncClient, cabecalho_admin: dict
) -> None:
    dados = {"valor": "10.00", "data": "2025-05-10", "tipo": "pontual"}

    resposta = await client.post("/doacoes", json=dados, headers=cabecalho_admin)

    assert resposta.status_code == 422
