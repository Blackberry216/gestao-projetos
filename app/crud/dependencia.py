from sqlalchemy.orm import Session
from app.models.tarefa import Tarefa, dependencia_tarefa


def listar_dependencias(db: Session, tarefa_id: int):
    return (
        db.query(Tarefa)
        .join(dependencia_tarefa, dependencia_tarefa.c.depende_de_id == Tarefa.id)
        .filter(dependencia_tarefa.c.tarefa_id == tarefa_id)
        .order_by(Tarefa.id)
        .all()
    )


def dependencia_existe(db: Session, tarefa_id: int, depende_de_id: int):
    linha = (
        db.query(dependencia_tarefa)
        .filter(
            dependencia_tarefa.c.tarefa_id == tarefa_id,
            dependencia_tarefa.c.depende_de_id == depende_de_id,
        )
        .first()
    )
    return linha is not None


def cria_ciclo(db: Session, tarefa_id: int, depende_de_id: int):
    visitadas = set()
    pendentes = [depende_de_id]

    while pendentes:
        atual = pendentes.pop()

        if atual == tarefa_id:
            return True
        if atual in visitadas:
            continue

        visitadas.add(atual)
        linhas = (
            db.query(dependencia_tarefa.c.depende_de_id)
            .filter(dependencia_tarefa.c.tarefa_id == atual)
            .all()
        )
        pendentes.extend(linha[0] for linha in linhas)

    return False


def adicionar_dependencia(db: Session, tarefa_id: int, depende_de_id: int):
    db.execute(
        dependencia_tarefa.insert().values(
            tarefa_id=tarefa_id,
            depende_de_id=depende_de_id,
        )
    )
    db.commit()


def remover_dependencia(db: Session, tarefa_id: int, depende_de_id: int):
    resultado = db.execute(
        dependencia_tarefa.delete().where(
            dependencia_tarefa.c.tarefa_id == tarefa_id,
            dependencia_tarefa.c.depende_de_id == depende_de_id,
        )
    )
    db.commit()
    return resultado.rowcount > 0