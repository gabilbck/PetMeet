from fastapi import Depends, FastAPI

from fastapi.responses import HTMLResponse
from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, users

app = FastAPI()

app.include_router(users.router, dependencies=[Depends(get_query_token)])
app.include_router(items.router, dependencies=[Depends(get_query_token)])
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header), Depends(get_query_token)],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/", response_class=HTMLResponse)
def ler_raiz():
    return """
    <html>
        <head>
            <title>Minha Página FastAPI</title>
        </head>
        <body>
            <h1>Olá, mundo!</h1>
            <p>Esta página foi criada com FastAPI.</p>
        </body>
    </html>
    """