from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from controller.clientes import router as router_cliente
from controller.produtos import router as router_produto

FRONTEND_DIR = Path(__file__).with_name("frontend")

app = FastAPI(
    title="Mercearia - API de Clientes",
    description="CRUD de clientes com PostgreSQL local.",
)

app.include_router(router_cliente)
app.include_router(router_produto)
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/", include_in_schema=False)
def exibir_frontend() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")
