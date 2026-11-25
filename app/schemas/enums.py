from enum import Enum


class StatusTarefa(str, Enum):
    pendente = "Pendente"
    em_andamento = "Em Andamento"
    concluida = "Concluída"
    cancelada = "Cancelada"


class Prioridade(str, Enum):
    alta = "Alta"
    media = "Média"
    baixa = "Baixa"


class StatusProjeto(str, Enum):
    planejado = "Planejado"
    em_andamento = "Em Andamento"
    concluido = "Concluído"
    cancelado = "Cancelado"

class StatusEntrega(str, Enum):
    pendente = "Pendente"
    concluida = "Concluída"
    atrasada = "Atrasada"
    cancelada = "Cancelada"