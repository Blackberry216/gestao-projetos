# Sistema de Gestão de Projetos

Trabalho Prático 2 da disciplina QXD0099 — Desenvolvimento de Software para Persistência, UFC Campus Quixadá, com o professor Francisco Victor da Silva Pinheiro.

## Integrantes
- Agenor Moraes Holanda Filho
- Atila Pereira Calisto
- Pedro Virgínio Maciel Alcântara Mendonça

## Tema Recebido
**Tema 7 — Sistema de Gestão de Projetos**

## Objetivo
O projeto consiste em uma API desenvolvida para substituir o uso de planilhas manuais no acompanhamento de projetos de software. A aplicação permite gerenciar clientes, projetos, alocação dinâmica de profissionais em equipes, registrar entregas e controlar tarefas. O sistema resolve o problema de falta de padronização ao calcular automaticamente o progresso real dos projetos com base no status das tarefas, além de gerenciar dependências de execução entre as atividades.

## Tecnologias Utilizadas
- **Python 3**
- **FastAPI** (Framework Web)
- **SQLAlchemy** (ORM)
- **Alembic** (Migrações de Banco de Dados)
- **PostgreSQL** (Banco de Dados Principal)
- **SQLite** (Banco de Dados de Desenvolvimento/Testes)
- **Pydantic** (Validação de Dados)

---

## Modelagem de Dados

### Descrição das Entidades
1. **Cliente:** Entidade que solicita e financia os projetos.
2. **Projeto:** A iniciativa central, contendo objetivos, prazos e status.
3. **Profissional:** Membros da empresa (desenvolvedores, gerentes, testadores) que executam o trabalho.
4. **EstatisticaProjeto:** Entidade dedicada a armazenar o progresso calculado e quantidade de pendências de um projeto.
5. **Tarefa:** Atividades que compõem o projeto, com prazos, prioridade e status (Pendente, Em Andamento, Concluída, Cancelada).
6. **Entrega:** Resultados concretos (protótipos, módulos) esperados em datas específicas.

### Descrição dos Relacionamentos
- **Cliente 1:N Projeto:** Um cliente pode possuir vários projetos.
- **Projeto 1:1 EstatisticaProjeto:** Cada projeto possui uma única métrica de acompanhamento de progresso.
- **Projeto N:N Profissional (Tabela Associativa `projeto_profissional`):** Organização das equipes. Um projeto tem vários profissionais, e um profissional atua em vários projetos, cada um com um "papel" específico.
- **Projeto 1:N Tarefa:** Um projeto é dividido em várias tarefas.
- **Projeto 1:N Entrega:** Um projeto possui várias entregas agendadas.
- **Profissional 1:N Tarefa:** Um profissional é responsável por várias tarefas.
- **Tarefa N:N Tarefa (Tabela Associativa `dependencia_tarefa`):** Relacionamento auto-referenciado onde uma tarefa pode depender da conclusão de outras.
- **Entrega N:N Tarefa (Tabela Associativa `entrega_tarefa`):** Uma entrega depende da conclusão de um grupo específico de tarefas.

### Representação do Modelo Relacional

```text
[Cliente] 1 ----- N [Projeto]
                       |
                       +-- 1 ----- 1 [EstatisticaProjeto]
                       |
                       +-- N ----- N [Profissional] (via projeto_profissional)
                       |
                       +-- 1 ----- N [Entrega]
                       |                |
                       |                +-- N ----- N [Tarefa] (via entrega_tarefa)
                       |
                       +-- 1 ----- N [Tarefa] --- N ----- 1 [Profissional]
                                        |
                                        +-- N ----- N [Tarefa] (via dependencia_tarefa)
```

---

## Instruções de Instalação e Execução

### 1. Criação do Ambiente e Instalação de Dependências
Clone o repositório e acesse a pasta do projeto:
```bash
git clone <url-do-repositorio>
cd sistema_gestao_projetos
```
Crie e ative o ambiente virtual:
```bash
python3 -m venv venv
source venv/bin/activate  # No Windows use: venv\Scripts\activate
```
Instale as dependências:
```bash
pip install -r requirements.txt
```

### 2. Configuração do Banco de Dados (DATABASE_URL)
O sistema suporta tanto SQLite quanto PostgreSQL, configurados através de variáveis de ambiente. Crie um arquivo `.env` na raiz do projeto.

**Configuração do PostgreSQL (Principal):**
Certifique-se de que o PostgreSQL está rodando e a base de dados foi criada. No `.env`, adicione:
```env
DATABASE_URL=postgresql+psycopg2://<usuario>:<senha>@localhost:5432/<nome_do_banco>
```

**Configuração do SQLite (Alternativo):**
Para rodar rapidamente com SQLite (o banco será criado como um arquivo local), use no `.env`:
```env
DATABASE_URL=sqlite:///./database.db
```

### 3. Execução das Migrações
A estrutura do banco de dados é gerenciada pelo Alembic. Para criar as tabelas no banco de dados configurado, execute:
```bash
alembic upgrade head
```

### 4. Execução do Povoamento Inicial
Para preencher o banco com dados de teste (clientes, projetos, profissionais e regras necessárias para demonstração), execute o script de seed:
```bash
python scripts/seed.py
```

### 5. Execução da Aplicação
Inicie o servidor local FastAPI:
```bash
uvicorn app.main:app --reload
```
Acesse a documentação interativa (Swagger UI) em: **http://localhost:8000/docs**

---

## API e Funcionalidades

### Principais Endpoints
- `POST /clientes`, `GET /clientes`, `PUT /clientes/{id}`, `DELETE /clientes/{id}`
- `POST /projetos`, `GET /projetos`, `PUT /projetos/{id}`, `DELETE /projetos/{id}`
- `POST /profissionais`, `GET /profissionais`, `PUT /profissionais/{id}`, `DELETE /profissionais/{id}`
- `POST /tarefas`, `GET /tarefas`, `PUT /tarefas/{id}`, `DELETE /tarefas/{id}`
- `POST /entregas`, `GET /entregas`
- `POST /projetos/{id}/equipe` (Aloca profissional em projeto)
- `POST /tarefas/{id}/dependencias` (Cria dependência entre tarefas)

*Nota: As listagens de Projetos e Tarefas (`GET /projetos` e `GET /tarefas`) possuem paginação implementada no banco de dados usando `page` e `size`.*

### Filtros Disponíveis
- **Tarefas:** Por status (`Pendente`, `Em Andamento`, etc.) e prioridade (`Alta`, `Média`, `Baixa`).
- **Projetos:** Por status e por ID de Cliente.
- **Profissionais:** Por cargo ou especialidade.

### Consultas Específicas e Complexas
1. **Tarefas de um Projeto:** Lista todas as tarefas associadas a um projeto específico.
2. **Projetos de um Profissional:** Lista onde um profissional está alocado.
3. **Tarefas Atrasadas (Consulta Complexa 1):** Filtra tarefas não concluídas com `prazo_previsto` menor que a data atual, ordenadas pelo prazo.
4. **Profissionais Sobrecarregados (Consulta Complexa 2):** Agrupa e identifica profissionais alocados em mais de "X" projetos simultaneamente utilizando `GROUP BY` e `COUNT`.
5. **Estatísticas (Agregação):** Quantidade de tarefas por status e o total de entregas realizadas vs previstas.

---

## Regras de Negócio Implementadas

- **RN001 - Bloqueio de Execução por Dependência:** O sistema impede que uma tarefa seja movida para "Em Andamento" ou "Concluída" se as tarefas das quais ela depende não estiverem concluídas.
- **RN003 - Restrição de Cancelamento:** Impede o cancelamento de uma tarefa se outras tarefas que dependem dela já estiverem em andamento ou concluídas.
- **RN004 - Integridade de Prazos:** Valida se o prazo da tarefa não ultrapassa a data final do projeto e se a data da entrega está dentro do período válido do projeto.

---

## Funcionalidade Específica do Tema (F17)

### Cálculo Automatizado de Andamento (Progresso do Projeto)
**Endpoint:** `GET /projetos/{id}/progresso`

**Descrição:** Em vez de depender de estimativas manuais das equipes, o sistema calcula o progresso real do projeto através de uma lógica dinâmica. 
- **Regra (RN002):** A fórmula aplica-se da seguinte maneira: `(Tarefas Concluídas / (Total de Tarefas - Tarefas Canceladas)) * 100`.
- O denominador ignora tarefas canceladas, garantindo que elas não prejudiquem o cálculo de progresso. Caso um projeto não possua tarefas válidas cadastradas, o sistema retorna automaticamente `0%`.