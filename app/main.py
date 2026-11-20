from fastapi import FastAPI
from app.routers import projetos
from app.database import engine, Base
from app.models import projeto, cliente, profissional, tarefa, projeto_profissional

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Gestão de Projetos")
app.include_router(projetos.router)


@app.get("/")
def root():
    return {"message": "API de Gestão de Projetos está rodando!"}