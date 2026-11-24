from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.crud import dependencia as crud_dependencia
from app.schemas.enums import StatusTarefa



def validar_rn001_dependencias_concluidas(db: Session, tarefa_id: int, novo_status: str):
    status_restritos = {
        StatusTarefa.em_andamento.value,
        StatusTarefa.concluida.value,
    }

    if novo_status not in status_restritos:
        return

    dependencias = crud_dependencia.listar_dependencias(db, tarefa_id=tarefa_id)
    nao_concluidas = [
        dep for dep in dependencias
        if dep.status != StatusTarefa.concluida.value
    ]

    if nao_concluidas:
        ids_pendentes = [dep.id for dep in nao_concluidas]
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"Não é possível alterar o status da tarefa {tarefa_id} para '{novo_status}' "
                f"porque existem dependências não concluídas (IDs: {ids_pendentes})."
            ),
        )



