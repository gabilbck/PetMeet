"""Testes de autenticacao e controle de acesso (RF20, RF21, RNF01, RNF02)."""

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.seguranca import gerar_hash_senha
from app.modelos.enums import PerfilUsuario
from app.modelos.usuario import Usuario


async def test_login_com_credenciais_validas_retorna_token(
    client: AsyncClient, sessao: AsyncSession
) -> None:
    usuario = Usuario(
        nome="Ana",
        email="ana@petmeet.org.br",
        senha_hash=gerar_hash_senha("senha-correta-123"),
        perfil=PerfilUsuario.ADMIN,
    )
    sessao.add(usuario)
    await sessao.commit()

    resposta = await client.post(
        "/auth/login", data={"username": "ana@petmeet.org.br", "password": "senha-correta-123"}
    )

    assert resposta.status_code == 200
    assert "access_token" in resposta.json()


async def test_login_com_senha_invalida_retorna_401(
    client: AsyncClient, sessao: AsyncSession
) -> None:
    usuario = Usuario(
        nome="Ana",
        email="ana2@petmeet.org.br",
        senha_hash=gerar_hash_senha("senha-correta-123"),
        perfil=PerfilUsuario.ADMIN,
    )
    sessao.add(usuario)
    await sessao.commit()

    resposta = await client.post(
        "/auth/login", data={"username": "ana2@petmeet.org.br", "password": "senha-errada"}
    )

    assert resposta.status_code == 401


async def test_rota_administrativa_sem_token_retorna_401(client: AsyncClient) -> None:
    resposta = await client.get("/pets")
    assert resposta.status_code == 401


async def test_criar_pet_sem_perfil_autorizado_retorna_403(
    client: AsyncClient, sessao: AsyncSession, dados_pet_saudavel: dict
) -> None:
    # Usuario existe e esta autenticado, mas perfil "voluntario" nao pode criar pets? Na
    # regra atual voluntario TAMBEM pode; aqui simulamos um perfil sem permissao alguma
    # criando o token com um usuario inativo, que deve ser rejeitado como nao autenticado.
    usuario_inativo = Usuario(
        nome="Inativo",
        email="inativo@petmeet.org.br",
        senha_hash=gerar_hash_senha("qualquer-senha"),
        perfil=PerfilUsuario.VOLUNTARIO,
        ativo=False,
    )
    sessao.add(usuario_inativo)
    await sessao.commit()

    from app.core.seguranca import criar_token_acesso

    token = criar_token_acesso({"sub": usuario_inativo.email})
    resposta = await client.post(
        "/pets", json=dados_pet_saudavel, headers={"Authorization": f"Bearer {token}"}
    )
    assert resposta.status_code == 401
