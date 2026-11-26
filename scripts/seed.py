import sys
import os
from datetime import date, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import SessionLocal
from app.models.cliente import Cliente
from app.models.profissional import Profissional
from app.models.projeto import Projeto
from app.models.tarefa import Tarefa, dependencia_tarefa
from app.models.entrega import Entrega, entrega_tarefa
from app.models.projeto_profissional import ProjetoProfissional
from app.models.contrato import Contrato
from app.schemas.enums import StatusProjeto, StatusTarefa, Prioridade, StatusEntrega

def popular_banco():
    db = SessionLocal()
    
    try:
        print("Limpando o banco de dados...")
        db.query(entrega_tarefa).delete()
        db.query(Entrega).delete()
        db.query(dependencia_tarefa).delete()
        db.query(Tarefa).delete()
        
        db.query(Contrato).delete() 
        
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

        projetos = []
        for i in range(1, 13):
            status = StatusProjeto.em_andamento.value if i <= 3 else StatusProjeto.planejado.value
            prazo = hoje + timedelta(days=30 + i) if i <= 3 else hoje + timedelta(days=90)
            
            proj = Projeto(
                titulo=f"Projeto {i} - Iniciativa {c1.nome if i % 2 == 0 else c2.nome}",
                objetivo=f"Objetivo do projeto {i}",
                data_inicio=hoje - timedelta(days=10),
                prazo_previsto=prazo,
                status=status,
                cliente_id=c1.id if i % 2 == 0 else c2.id
            )
            projetos.append(proj)
            db.add(proj)
        db.commit()

        for i in range(5):
            contrato = Contrato(
                projeto_id=projetos[i].id,
                valor_total=10000.00 * (i + 1),
                data_assinatura=hoje - timedelta(days=15)
            )
            db.add(contrato)
        db.commit()

        for i in range(5):
            db.add(ProjetoProfissional(projeto_id=projetos[i].id, profissional_id=p1.id, responsabilidade="Dev Backend"))
        
        for i in range(3):
            db.add(ProjetoProfissional(projeto_id=projetos[i].id, profissional_id=p2.id, responsabilidade="Gerente"))
            
        for i in range(2):
            db.add(ProjetoProfissional(projeto_id=projetos[i].id, profissional_id=p3.id, responsabilidade="QA"))
            
        db.add(ProjetoProfissional(projeto_id=projetos[0].id, profissional_id=p4.id, responsabilidade="Frontend"))
        db.commit()

        tarefas = []
        t1 = Tarefa(titulo="Modelar Banco", prazo_previsto=hoje - timedelta(days=5), status=StatusTarefa.concluida.value, projeto_id=projetos[0].id, responsavel_id=p1.id, prioridade=Prioridade.alta.value)
        t2 = Tarefa(titulo="Criar API", prazo_previsto=hoje + timedelta(days=10), status=StatusTarefa.em_andamento.value, projeto_id=projetos[0].id, responsavel_id=p1.id, prioridade=Prioridade.media.value)
        t3 = Tarefa(titulo="Testar API", prazo_previsto=hoje + timedelta(days=15), status=StatusTarefa.pendente.value, projeto_id=projetos[0].id, responsavel_id=p3.id, prioridade=Prioridade.baixa.value)
        tarefas.extend([t1, t2, t3])

        t4 = Tarefa(titulo="Corrigir Bug Pagamento", prazo_previsto=hoje - timedelta(days=2), status=StatusTarefa.em_andamento.value, projeto_id=projetos[1].id, responsavel_id=p1.id, prioridade=Prioridade.alta.value)
        t5 = Tarefa(titulo="Atualizar Documentação", prazo_previsto=hoje - timedelta(days=10), status=StatusTarefa.pendente.value, projeto_id=projetos[1].id, responsavel_id=p2.id, prioridade=Prioridade.media.value)
        t6 = Tarefa(titulo="Reunião Cancelada", prazo_previsto=hoje - timedelta(days=1), status=StatusTarefa.cancelada.value, projeto_id=projetos[1].id, responsavel_id=p2.id, prioridade=Prioridade.baixa.value)
        tarefas.extend([t4, t5, t6])

        for i in range(2, 10):
            t = Tarefa(titulo=f"Tarefa Padrão {i}", prazo_previsto=hoje + timedelta(days=20+i), status=StatusTarefa.pendente.value, projeto_id=projetos[i].id, responsavel_id=p2.id, prioridade=Prioridade.media.value)
            tarefas.append(t)

        db.add_all(tarefas)
        db.commit()

        db.execute(dependencia_tarefa.insert().values(tarefa_id=t3.id, depende_de_id=t2.id))
        db.execute(dependencia_tarefa.insert().values(tarefa_id=t2.id, depende_de_id=t1.id))
        db.commit()

        e1 = Entrega(titulo="MVP Banco de Dados", data_prevista=hoje - timedelta(days=5), data_realizada=hoje - timedelta(days=4), status=StatusEntrega.concluida.value, projeto_id=projetos[0].id)
        e2 = Entrega(titulo="Versão Beta", data_prevista=hoje + timedelta(days=25), data_realizada=None, status=StatusEntrega.pendente.value, projeto_id=projetos[0].id)
        db.add_all([e1, e2])
        db.commit()

        db.execute(entrega_tarefa.insert().values(entrega_id=e1.id, tarefa_id=t1.id))
        db.execute(entrega_tarefa.insert().values(entrega_id=e2.id, tarefa_id=t2.id))
        db.execute(entrega_tarefa.insert().values(entrega_id=e2.id, tarefa_id=t3.id))
        
        db.commit()
        print("✅ Banco de dados populado com sucesso! Pronto para a apresentação.")
        print(f"   - {len(projetos)} Projetos criados (testa paginação)")
        print(f"   - {len(tarefas)} Tarefas criadas (testa filtros)")
        print("   - 5 Contratos criados (testa 1:1)")
        print("   - João alocado em 5 projetos (testa sobrecarga)")

    except Exception as e:
        print(f"❌ Erro ao popular o banco: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    popular_banco()