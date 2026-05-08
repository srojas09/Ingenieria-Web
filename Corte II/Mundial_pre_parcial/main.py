from fastapi import FastAPI
from routers import equipos, jugadores

app = FastAPI(
    title="API Mundial de Fútbol",
    description="Gestión de equipos y jugadores para el mundial",
    version="1.0.0"
)

app.include_router(equipos.router, prefix="/equipos", tags=["Equipos"])
app.include_router(jugadores.router, prefix="/jugadores", tags=["Jugadores"])


@app.get("/")
def root():
    return {"mensaje": "API Mundial funcionando correctamente"}