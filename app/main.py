from fastapi import FastAPI
from app.routers import projetos, clientes, profissionais, tarefas, dependencias

app = FastAPI(title="Sistema de Gestão de Projetos")
app.include_router(projetos.router)
app.include_router(clientes.router)
app.include_router(profissionais.router)
app.include_router(tarefas.router)
app.include_router(dependencias.router)


@app.get("/")
def root():
    return {"message": "API de Gestão de Projetos está rodando!"}