"""Testes de cadastro e consulta de pets (RF01-05, RF18, RN08)."""

from httpx import AsyncClient


async def test_criar_pet_com_dados_validos(
    client: AsyncClient, cabecalho_admin: dict, dados_pet_saudavel: dict
) -> None:
    resposta = await client.post("/pets", json=dados_pet_saudavel, headers=cabecalho_admin)

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["nome"] == "Rex"
    assert corpo["situacao_adocao"] == "disponivel"


async def test_criar_pet_em_tratamento_sem_doenca_e_rejeitado(
    client: AsyncClient, cabecalho_admin: dict
) -> None:
    # RF16/RN08: se esta em tratamento medico, a doenca precisa ser identificada.
    dados = {
        "nome": "Bolinha",
        "especie": "gato",
        "idade": 2,
        "data_resgate": "2025-02-01",
        "status_saude": "em_tratamento_medico",
    }
    resposta = await client.post("/pets", json=dados, headers=cabecalho_admin)
    assert resposta.status_code == 422


async def test_criar_pet_sem_campo_obrigatorio_e_rejeitado(
    client: AsyncClient, cabecalho_admin: dict
) -> None:
    dados = {"nome": "SemEspecie", "idade": 1, "data_resgate": "2025-01-01"}
    resposta = await client.post("/pets", json=dados, headers=cabecalho_admin)
    assert resposta.status_code == 422


async def test_listar_pets_retorna_paginado(
    client: AsyncClient, cabecalho_admin: dict, dados_pet_saudavel: dict
) -> None:
    await client.post("/pets", json=dados_pet_saudavel, headers=cabecalho_admin)

    resposta = await client.get("/pets?pagina=1&tamanho_pagina=10", headers=cabecalho_admin)

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["total"] == 1
    assert len(corpo["itens"]) == 1


async def test_atualizar_status_saude_do_pet(
    client: AsyncClient, cabecalho_admin: dict, dados_pet_saudavel: dict
) -> None:
    pet_criado = (
        await client.post("/pets", json=dados_pet_saudavel, headers=cabecalho_admin)
    ).json()

    resposta = await client.patch(
        f"/pets/{pet_criado['id']}/status-saude",
        json={"status_saude": "em_tratamento_medico", "doenca_atual": "Displasia coxo-femoral"},
        headers=cabecalho_admin,
    )

    assert resposta.status_code == 200
    assert resposta.json()["status_saude"] == "em_tratamento_medico"
    assert resposta.json()["doenca_atual"] == "Displasia coxo-femoral"
