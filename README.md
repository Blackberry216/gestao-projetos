# Sistema de Gestão de Projetos

## Nome do Projeto
**Sistema de Gestão de Projetos** (`app.main:app`)

## Integrantes
* Agenor Moraes Holanda Filho
* Atila Pereira Calisto
* Pedro Virgínio Maciel Alcântara Mendonça

*(Universidade Federal do Ceará — Campus Quixadá | Disciplina: QXD0099 - Desenvolvimento de Software para Persistência | Prof. Francisco Victor da Silva Pinheiro)*

## Tema Recebido
**Sistema de Gestão de Projetos de Desenvolvimento de Software** — controle centralizado de clientes, projetos, profissionais alocados, tarefas, dependências entre atividades e entregas.

## Objetivo
Desenvolver uma API RESTful com persistência relacional capaz de substituir controles manuais em planilhas, permitindo o gerenciamento completo do ciclo de vida de projetos de software:
* Cadastrar, consultar, atualizar e remover/desativar clientes, projetos, profissionais, tarefas, dependências e entregas.
* Controlar a alocação de equipes com suas respectivas responsabilidades em cada projeto.
* Garantir a integridade da execução por meio de regras de negócio aplicadas no banco e na camada de serviços (bloqueio de status por dependência não concluída, bloqueio de cancelamento/exclusão com dependentes e validação de prazos).
* Disponibilizar consultas relacionais, filtros combinados, paginação diretamente no banco de dados, estatísticas agregadas e cálculo automatizado do progresso do projeto.

## Tecnologias Utilizadas
* **Linguagem:** Python 3.11+
* **Framework Web:** FastAPI (com roteamento modularizado via `APIRouter`)
* **ORM (Mapeamento Objeto-Relacional):** SQLAlchemy
* **Validação de Dados:** Pydantic
* **Banco de Dados Principal:** PostgreSQL (`psycopg` / `psycopg2`)
* **Banco de Dados Alternativo:** SQLite
* **Migrações de Banco de Dados:** Alembic
* **Servidor ASGI:** Uvicorn
* **Variáveis de Ambiente:** `python-dotenv`

## Descrição das Entidades
Com base nos modelos registrados em `app/models/` (`projeto.py`, `cliente.py`, `profissional.py`, `tarefa.py`, `entrega.py`) e nas tabelas de relacionamento do sistema:

1. **Cliente (`clientes`):** Entidade contratante dos projetos (identificador, nome/razão social, e-mail/contato e status).
2. **Projeto (`projetos`):** Iniciativa de software contratada por um cliente, contendo título, descrição, datas de início e término previsto, status e orçamento (`orcamento`).
3. **Profissional (`profissionais`):** Membro da equipe técnica ou de gestão (desenvolvedor, analista, testador, gerente), contendo nome, e-mail único, cargo/especialidade e status.
4. **Alocação de Equipe (`projeto_profissional`):** Tabela associativa entre projetos e profissionais que registra o papel/responsabilidade desempenhado pelo profissional no projeto.
5. **Tarefa (`tarefas`):** Atividade vinculada a um projeto e atribuída a um profissional, contendo título, descrição, prazo previsto, prioridade (`Baixa`, `Média`, `Alta`) e status (`Pendente`, `Em Andamento`, `Concluída`, `Cancelada`).
6. **Dependência (`dependencias`):** Registra o vínculo de pré-requisito entre duas tarefas (`tarefa_id` depende da conclusão de `dependencia_id`).
7. **Entrega (`entregas`):** Marco ou produto concreto esperado do projeto (documentação, protótipo, módulo ou versão), contendo título, descrição, data prevista, data de entrega e status, vinculada às tarefas necessárias por meio da tabela associativa `entrega_tarefa`.

## Descrição dos Relacionamentos
* **1:N — Cliente $\rightarrow$ Projetos:** Um cliente pode possuir vários projetos; cada projeto está vinculado a um único cliente (`projetos.cliente_id`).
* **1:N — Projeto $\rightarrow$ Tarefas:** Um projeto é composto por várias tarefas; cada tarefa pertence a um projeto (`tarefas.projeto_id`).
* **1:N — Profissional $\rightarrow$ Tarefas:** Um profissional pode ser responsável por várias tarefas em diferentes projetos (`tarefas.profissional_id`).
* **1:N — Projeto $\rightarrow$ Entregas:** Um projeto possui diversas entregas previstas ao longo de sua execução (`entregas.projeto_id`).
* **N:N — Projetos $\leftrightarrow$ Profissionais:** Um mesmo profissional pode participar de múltiplos projetos exercendo papéis distintos, e um projeto reúne vários profissionais (`projeto_profissional`).
* **N:N — Entregas $\leftrightarrow$ Tarefas:** Uma entrega pode depender de várias tarefas concluídas e uma tarefa pode compor mais de uma entrega (`entrega_tarefa`).
* **N:N (Autorrelacionamento) — Tarefas $\leftrightarrow$ Tarefas:** Uma tarefa pode depender de várias outras tarefas e também ser pré-requisito de múltiplas tarefas dependentes (`dependencias`).
* **1:1 — Projeto / Detalhamento Exclusivo:** Relacionamento um-para-um com chave estrangeira única (`unique=True`) para informações complementares exclusivas do registro principal.

## Diagrama / Representação do Modelo Relacional

```text
+---------------+       1:N       +-------------------+       1:N       +---------------+
|   clientes    |---------------->|     projetos      |---------------->|   entregas    |
+---------------+                 +-------------------+                 +---------------+
| PK id         |                 | PK id             |                 | PK id         |
|    nome       |                 | FK cliente_id     |                 | FK projeto_id |
|    email      |                 |    titulo         |                 |    titulo     |
+---------------+                 |    data_inicio    |                 |    data_prev  |
                                  |    data_fim       |                 |    status     |
                                  |    orcamento      |                 +---------------+
                                  |    status         |                         |
                                  +-------------------+                         | N:N
                                    |               |                           v
                                    | N:N           | 1:N              +----------------+
                                    v               v                  | entrega_tarefa |
                     +--------------------+   +---------------+        +----------------+
                     | projeto_profissional|  |    tarefas    |<-------| PK/FK entrega  |
                     +--------------------+   +---------------+        | PK/FK tarefa   |
                     | PK/FK projeto_id   |   | PK id         |        +----------------+
                     | PK/FK profissional |   | FK projeto_id |                 |
                     |    papel           |   | FK prof_id    |                 | N:N (Auto)
                     +--------------------+   |    titulo     |                 v
                                    ^         |    prazo      |        +----------------+
                                    |         |    prioridade |        |  dependencias  |
+---------------+                   |         |    status     |        +----------------+
| profissionais |-------------------+         +---------------+        | PK id          |
+---------------+                                                      | FK tarefa_id   |
| PK id         |                                                      | FK dep_id      |
|    nome       |                                                      +----------------+
|    cargo      |
+---------------+
```

## Instruções de Instalação
1. Clone o repositório do projeto e acesse a pasta raiz:
   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd <PASTA_DO_PROJETO>
   ```
2. Verifique a estrutura modular do projeto (`app/main.py`, `app/models/`, `app/schemas/`, `app/crud/`, `app/services/`, `app/routers/`, `alembic/` e `scripts/`).

## Criação do Ambiente
Crie e ative um ambiente virtual Python isolado na raiz do projeto:

```bash
python -m venv .venv
```

* **Windows (PowerShell / CMD):**
  ```bash
  .venv\Scripts\activate
  ```
* **Linux / macOS:**
  ```bash
  source .venv/bin/activate
  ```

## Instalação das Dependências
Com o ambiente virtual ativado, instale todos os pacotes listados em `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Configuração do PostgreSQL
1. Certifique-se de que o servidor **PostgreSQL** esteja instalado e em execução localmente (porta padrão `5432`).
2. Crie o banco de dados da aplicação no PostgreSQL:
   ```sql
   CREATE DATABASE gestao_projetos;
   ```
3. Utilize as credenciais do seu usuário PostgreSQL (`usuario`, `senha`, `host`, `porta` e `gestao_projetos`) para preencher a variável `DATABASE_URL` no arquivo `.env`.

## Configuração do SQLite
Para executar ou testar a aplicação utilizando **SQLite** sem alterar nenhum arquivo de código (`models`, `crud`, `services` ou `routers`):
1. Basta apontar a variável `DATABASE_URL` no arquivo `.env` para um arquivo local `.db` (ex.: `sqlite:///./database.db`).
2. O arquivo do banco SQLite será criado automaticamente na raiz do projeto ao rodar as migrações ou iniciar a aplicação.

## Configuração da Variável `DATABASE_URL`
Crie um arquivo `.env` na raiz do repositório (este arquivo não é versionado pelo Git) e defina `DATABASE_URL` conforme o banco escolhido:

* **Usando PostgreSQL (Banco Principal):**
  ```env
  DATABASE_URL=postgresql://usuario:senha@localhost:5432/gestao_projetos
  ```

* **Usando SQLite (Banco Alternativo):**
  ```env
  DATABASE_URL=sqlite:///./database.db
  ```

## Execução das Migrações
Com o `.env` configurado, execute as migrações do **Alembic** para criar toda a estrutura relacional e aplicar alterações estruturais versionadas (como a adição da coluna `orcamento` na tabela `projetos`):

```bash
alembic upgrade head
```

*(Caso crie novas alterações nos modelos em `app/models/`, gere uma nova revisão com `alembic revision --autogenerate -m "descricao"` e aplique com `alembic upgrade head`.)*

## Execução do Povoamento
Execute o script de povoamento inicial localizado em `scripts/` para popular o banco de dados com registros consistentes em todas as entidades principais (clientes, profissionais, projetos, alocações, tarefas, dependências e entregas):

```bash
python -m scripts.seed
```

## Execução da Aplicação
Inicie o servidor FastAPI com Uvicorn a partir da raiz do projeto:

```bash
uvicorn app.main:app --reload
```

* **Endpoint raiz:** `http://127.0.0.1:8000/`
* **Documentação interativa (Swagger UI):** `http://127.0.0.1:8000/docs`
* **Documentação alternativa (ReDoc):** `http://127.0.0.1:8000/redoc`

## Principais Endpoints
As rotas são modularizadas por domínio utilizando `APIRouter` e registradas em `app/main.py` (`projetos`, `clientes`, `profissionais`, `tarefas`, `dependencias`, `entregas`):

* **Status da API:**
  * `GET /` — Verifica se a API está em execução.
* **Clientes (`app/routers/clientes.py`):**
  * `POST /clientes` | `GET /clientes` | `GET /clientes/{id}` | `PUT /clientes/{id}` | `DELETE /clientes/{id}`
* **Projetos (`app/routers/projetos.py`):**
  * `POST /projetos` | `GET /projetos` | `GET /projetos/{id}` | `PUT /projetos/{id}` | `DELETE /projetos/{id}`
  * `GET /projetos/{id}/progresso` | `GET /projetos/{id}/estatisticas`
* **Profissionais (`app/routers/profissionais.py`):**
  * `POST /profissionais` | `GET /profissionais` | `GET /profissionais/{id}` | `PUT /profissionais/{id}` | `DELETE /profissionais/{id}`
* **Tarefas (`app/routers/tarefas.py`):**
  * `POST /tarefas` | `GET /tarefas` | `GET /tarefas/{id}` | `PUT /tarefas/{id}` | `DELETE /tarefas/{id}`
* **Dependências (`app/routers/dependencias.py`):**
  * `POST /dependencias` | `GET /dependencias` | `GET /dependencias/{id}` | `DELETE /dependencias/{id}`
* **Entregas (`app/routers/entregas.py`):**
  * `POST /entregas` | `GET /entregas` | `GET /entregas/{id}` | `PUT /entregas/{id}` | `DELETE /entregas/{id}`

*(As listagens principais suportam paginação diretamente no banco via parâmetros de consulta como `page` e `size` / `offset` e `limit`.)*

## Filtros Disponíveis
Os filtros são aplicados diretamente nas consultas SQL via SQLAlchemy e permitem combinação de critérios:
* **Tarefas (`GET /tarefas`):**
  * `status`: filtra por situação da tarefa (`Pendente`, `Em Andamento`, `Concluída`, `Cancelada`).
  * `prioridade`: filtra por nível de prioridade (`Baixa`, `Média`, `Alta`).
  * `projeto_id`: filtra tarefas de um projeto específico.
  * `profissional_id`: filtra tarefas atribuídas a um profissional específico.
* **Projetos (`GET /projetos`):**
  * `status`: filtra projetos pela situação atual.
  * `cliente_id`: filtra projetos vinculados a um cliente específico.
* **Profissionais (`GET /profissionais`):**
  * `cargo` / `especialidade`: filtra profissionais pela especialidade ou função.

## Consultas Específicas
* **Consultas Relacionais:**
  * Listar todas as tarefas pertencentes a um projeto específico (`GET /projetos/{id}/tarefas` ou `GET /tarefas?projeto_id={id}`).
  * Listar todos os projetos em que um profissional está alocado (`GET /profissionais/{id}/projetos`).
  * Listar as tarefas dependentes de uma tarefa específica (`GET /tarefas/{id}/dependentes`).
* **Consultas Complexas (JOIN, intervalos de data, ordenação e agrupamento):**
  * **Tarefas atrasadas por projeto:** consulta tarefas de um projeto cuja data de prazo previsto já expirou e cujo status não seja `"Concluída"` nem `"Cancelada"`, ordenadas por prazo.
  * **Carga de trabalho de profissionais:** identifica profissionais alocados em mais de $X$ projetos simultaneamente por meio de `JOIN`, `GROUP BY` e contagem de vínculos.
* **Estatísticas e Agregações (`GET /projetos/{id}/estatisticas`):**
  * Agrega no banco (`COUNT` / `GROUP BY`) o total de tarefas por status em um projeto e compara o total de entregas realizadas versus entregas previstas.

## Regras de Negócio
As regras de negócio estão implementadas na camada `app/services/` (como `app/services/tarefa_service.py`) e integradas às operações de escrita e exclusão:

1. **RN001 — Bloqueio de Execução por Dependência (`PUT /tarefas/{id}`):**
   * Impede que uma tarefa tenha seu status alterado para `"Em Andamento"` ou `"Concluída"` caso exista qualquer tarefa pré-requisito vinculada a ela que ainda não esteja com status `"Concluída"`. Retorna HTTP `409 Conflict`.
2. **RN002 — Cálculo de Progresso Consistente:**
   * Calcula o percentual de conclusão do projeto a partir das tarefas registradas, desconsiderando tarefas `"Cancelada"` no denominador:
     $$\text{Progresso (\%)} = \frac{\text{Tarefas Concluídas}}{\text{Total de Tarefas} - \text{Tarefas Canceladas}} \times 100$$
   * Caso não existam tarefas válidas, o percentual retornado é `0%`.
3. **RN003 — Restrição de Cancelamento e Exclusão com Dependentes (`PUT /tarefas/{id}` e `DELETE /tarefas/{id}`):**
   * Impede o cancelamento de uma tarefa quando existem outras tarefas dependentes ativas vinculadas a ela (`409 Conflict`), e bloqueia a exclusão (`DELETE`) de tarefas que possuam dependências cadastradas (`409 Conflict` — `"Não é possível excluir a tarefa porque ela possui dependências cadastradas"`).
4. **RN004 — Integridade de Prazos:**
   * Valida que o prazo previsto de uma tarefa não ultrapasse a data de término do projeto ao qual pertence e que o prazo previsto de uma entrega esteja dentro do período de vigência do projeto.

## Descrição da Funcionalidade Específica do Tema
A funcionalidade específica do tema **Gestão de Projetos** é o **Monitoramento Automatizado de Progresso e Controle de Cadeia de Dependências**:
* **Cálculo Automatizado de Progresso (`GET /projetos/{id}/progresso`):** consulta diretamente no banco as tarefas vinculadas ao projeto, isola as tarefas canceladas para evitar distorção de métricas e calcula em tempo real o percentual real de andamento do projeto junto ao resumo quantitativo por status.
* **Integridade Transacional de Cronograma (`PUT /tarefas/{id}` e `DELETE /tarefas/{id}`):** antes de atualizar o status ou remover uma tarefa, a camada de serviço (`tarefa_service.py`) verifica toda a cadeia de dependências no banco de dados (RN001 e RN003), garantindo que nenhuma etapa avance sem pré-requisitos concluídos nem seja cancelada/removida deixando tarefas dependentes inconsistentes.