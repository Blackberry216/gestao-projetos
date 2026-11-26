import sys
import os
from datetime import date, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import SessionLocal, engine
from app.models.cliente import Cliente
from app.models.profissional import Profissional
from app.models.projeto import Projeto
from app.models.tarefa import Tarefa, dependencia_tarefa
from app.models.entrega import Entrega, entrega_tarefa
from app.models.projeto_profissional import ProjetoProfissional
from app.schemas.enums import StatusProjeto, StatusTarefa, Prioridade, StatusEntrega
from app.models.contrato import Contrato

def popular_banco():
    db = SessionLocal()
    
    try:
        print("Limpando o banco de dados...")
        db.query(entrega_tarefa).delete()
        db.query(Entrega).delete()
        db.query(dependencia_tarefa).delete()
        db.query(Tarefa).delete()
        db.query(ProjetoProfissional).delete()
        db.query(Projeto).delete()
        db.query(Profissional).delete()
        db.query(Cliente).delete()
        db.commit()

        hoje = date.today()

        c1 = Cliente(nome="TechCorp", setor="Tecnologia")
        c2 = Cliente(nome="Financeira XYZ", setor="Finanças")
        c3 = Cliente(nome="Varejo ABC", setor="Comércio")
        db.add_all([c1, c2, c3])
        db.commit()

        p1 = Profissional(nome="João Dev", email="joao@email.com", cargo="Desenvolvedor")
        p2 = Profissional(nome="Maria Gerente", email="maria@email.com", cargo="Gerente")
        p3 = Profissional(nome="Pedro QA", email="pedro@email.com", cargo="Testador")
        p4 = Profissional(nome="Ana Frontend", email="ana@email.com", cargo="Desenvolvedor")
        db.add_all([p1, p2, p3, p4])
        db.commit()

        proj1 = Projeto(
            titulo="App Mobile TechCorp", 
            objetivo="Criar app de vendas",
            data_inicio=hoje - timedelta(days=1),
            prazo_previsto=hoje + timedelta(days=30),
            status=StatusProjeto.em_andamento.value,
            cliente_id=c1.id
        )
        proj2 = Projeto(
            titulo="Portal Financeiro XYZ", 
            objetivo="Modernizar internet banking",
            data_inicio=hoje - timedelta(days=60),
            prazo_previsto=hoje + timedelta(days=10),
            status=StatusProjeto.em_andamento.value,
            cliente_id=c2.id
        )
        proj3 = Projeto(
            titulo="Sistema de Estoque", 
            objetivo="Controle de armazém",
            data_inicio=hoje + timedelta(days=5),
            prazo_previsto=hoje + timedelta(days=90),
            status=StatusProjeto.planejado.value,
            cliente_id=c3.id
        )
        db.add_all([proj1, proj2, proj3])
        db.commit()

        db.add_all([
            ProjetoProfissional(projeto_id=proj1.id, profissional_id=p1.id, responsabilidade="Dev Backend"),
            ProjetoProfissional(projeto_id=proj2.id, profissional_id=p1.id, responsabilidade="Dev Backend"),
            ProjetoProfissional(projeto_id=proj3.id, profissional_id=p1.id, responsabilidade="Consultor"),
            
            ProjetoProfissional(projeto_id=proj1.id, profissional_id=p2.id, responsabilidade="Gerente"),
            ProjetoProfissional(projeto_id=proj2.id, profissional_id=p2.id, responsabilidade="Gerente"),
            
            ProjetoProfissional(projeto_id=proj1.id, profissional_id=p3.id, responsabilidade="QA"),
        ])
        db.commit()

        
        t1 = Tarefa(titulo="Modelar Banco de Dados", prazo_previsto=hoje - timedelta(days=5), status=StatusTarefa.concluida.value, projeto_id=proj1.id, responsavel_id=p1.id, prioridade=Prioridade.alta.value)
        t2 = Tarefa(titulo="Criar API de Login", prazo_previsto=hoje + timedelta(days=10), status=StatusTarefa.em_andamento.value, projeto_id=proj1.id, responsavel_id=p1.id, prioridade=Prioridade.media.value)
        t3 = Tarefa(titulo="Testar Tela de Login", prazo_previsto=hoje + timedelta(days=15), status=StatusTarefa.pendente.value, projeto_id=proj1.id, responsavel_id=p3.id, prioridade=Prioridade.baixa.value)
        
        t4 = Tarefa(titulo="Corrigir Bug de Pagamento", prazo_previsto=hoje - timedelta(days=2), status=StatusTarefa.em_andamento.value, projeto_id=proj2.id, responsavel_id=p1.id, prioridade=Prioridade.alta.value)
        t5 = Tarefa(titulo="Atualizar Documentação", prazo_previsto=hoje - timedelta(days=10), status=StatusTarefa.pendente.value, projeto_id=proj2.id, responsavel_id=p2.id, prioridade=Prioridade.media.value)
        t6 = Tarefa(titulo="Reunião de Alinhamento", prazo_previsto=hoje - timedelta(days=1), status=StatusTarefa.cancelada.value, projeto_id=proj2.id, responsavel_id=p2.id, prioridade=Prioridade.baixa.value)
        
        t7 = Tarefa(titulo="Levantar Requisitos", prazo_previsto=hoje + timedelta(days=20), status=StatusTarefa.pendente.value, projeto_id=proj3.id, responsavel_id=p2.id, prioridade=Prioridade.alta.value)
        
        db.add_all([t1, t2, t3, t4, t5, t6, t7])
        db.commit()

        db.execute(dependencia_tarefa.insert().values(tarefa_id=t3.id, depende_de_id=t2.id))
        
        db.execute(dependencia_tarefa.insert().values(tarefa_id=t2.id, depende_de_id=t1.id))
        db.commit()

        e1 = Entrega(
            titulo="MVP Banco de Dados",
            data_prevista=hoje - timedelta(days=5),
            data_realizada=hoje - timedelta(days=4),
            status=StatusEntrega.concluida.value,
            projeto_id=proj1.id
        )
       
        e2 = Entrega(
            titulo="Versão Beta do App",
            data_prevista=hoje + timedelta(days=25),
            data_realizada=None,
            status=StatusEntrega.pendente.value,
            projeto_id=proj1.id
        )
        db.add_all([e1, e2])
        db.commit()

        db.execute(entrega_tarefa.insert().values(entrega_id=e1.id, tarefa_id=t1.id))
        
        db.execute(entrega_tarefa.insert().values(entrega_id=e2.id, tarefa_id=t2.id))
        db.execute(entrega_tarefa.insert().values(entrega_id=e2.id, tarefa_id=t3.id))
        
        db.commit()
        print("✅ Banco de dados populado com sucesso! Pronto para a apresentação.")

    except Exception as e:
        print(f"❌ Erro ao popular o banco: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    popular_banco()