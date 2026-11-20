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