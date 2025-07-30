# API de Gestão Escolar

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.x-black?style=for-the-badge&logo=flask)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13%2B-blue?style=for-the-badge&logo=postgresql)

Esta é uma API RESTful para um sistema de gestão escolar. Construída com Flask e Python, ela se conecta a um banco de dados PostgreSQL para realizar operações essenciais de uma instituição de ensino.

## ✨ Funcionalidades

A API foi projetada para ser o backend de um sistema que gerencia:

* **Estudantes:** Cadastro e informações dos alunos.
* **Disciplinas:** Gerenciamento das matérias oferecidas.
* **Turmas:** Organização de turmas por semestre.
* **Notas:** Lançamento de notas e controle de frequência.
* **Ementas:** Detalhamento do conteúdo programático das disciplinas.
* **Pagamentos:** Controle financeiro de mensalidades e taxas.

Para cada uma dessas áreas, a API oferece todas as operações básicas de criação, leitura, atualização e exclusão (CRUD).

---

## 🚀 Como Usar a API

### 1. Configuração do Ambiente

1.  **Clone o projeto** para a sua máquina local.
2.  **Crie e ative um ambiente virtual** Python (recomendado).
3.  **Instale as dependências** necessárias, que são `Flask` e `psycopg2-binary`. Você pode colocá-las em um arquivo `requirements.txt` e rodar `pip install -r requirements.txt`.
4.  **Configure o Banco de Dados:**
    * Crie um banco de dados no seu servidor PostgreSQL.
    * Crie as tabelas: `Estudante`, `Disciplina`, `Turma`, `Notas`, `Ementa` e `Pagamento`. As colunas e tipos de dados necessários podem ser identificados a partir das queries `INSERT` e `UPDATE` no arquivo principal da aplicação.
5.  **Configure a Conexão:** Crie um arquivo `bd.py` que contenha uma função `criar_conexao()`. Esta função deve usar suas credenciais para se conectar ao banco de dados PostgreSQL e retornar um objeto de conexão.

### 2. Executando a Aplicação

Com o ambiente configurado, inicie o servidor Flask com o comando:

```bash
flask run
```

A API estará rodando em `http://127.0.0.1:5000`. Agora você pode fazer requisições para os endpoints abaixo usando ferramentas como Postman, Insomnia ou `curl`.

---

## 📚 Endpoints da API

A seguir, a lista de todos os endpoints disponíveis e sua função.

### `/estudantes`
* `GET /estudantes`: Lista todos os estudantes.
* `GET /estudantes/<id>`: Busca um estudante específico pelo seu ID.
* `POST /estudantes`: Cria um novo estudante. Requer os campos: `nome`, `cpf`, `data_nascimento`, `email`, `telefone`, `curso`, `matricula`, `estado`.
* `PUT /estudantes/<id>`: Atualiza os dados de um estudante.
* `DELETE /estudantes/<id>`: Remove um estudante.

### `/disciplinas`
* `GET /disciplinas`: Lista todas as disciplinas.
* `POST /disciplinas`: Cria uma nova disciplina. Requer os campos: `nome_disciplina`, `carga_horaria`, `id_coordenador`, `curso_relacionado`.
* `PUT /disciplinas/<id>`: Atualiza os dados de uma disciplina.
* `DELETE /disciplinas/<id>`: Remove uma disciplina.

### `/turmas`
* `GET /turmas`: Lista todas as turmas.
* `GET /turmas/<id>`: Busca uma turma específica pelo seu ID.
* `POST /turmas`: Cria uma nova turma. Requer os campos: `id_disciplina`, `id_professor`, `semestre`, `ano_letivo`, `horario`, `sala`.
* `PUT /turmas/<id>`: Atualiza os dados de uma turma.
* `DELETE /turmas/<id>`: Remove uma turma.

### `/notas`
* `GET /notas`: Lista todos os registros de notas.
* `GET /notas/<id>`: Busca um registro de nota específico.
* `POST /notas`: Lança as notas de um aluno. Requer: `id_estudante`, `id_disciplina`, `id_turma`, `nota_1`, `nota_2`, `frequencia`. A média é calculada automaticamente.
* `PUT /notas/<id>`: Atualiza um registro de nota.
* `DELETE /notas/<id>`: Remove um registro de nota.

### `/ementas`
* `GET /ementas`: Lista todas as ementas.
* `GET /ementas/<id>`: Busca uma ementa específica.
* `POST /ementas`: Cria uma ementa para uma disciplina. Requer: `id_disciplina`, `descricao`, `objetivos`, `bibliografia`, `metodologia`, `avaliacao`.
* `PUT /ementas/<id>`: Atualiza uma ementa.
* `DELETE /ementas/<id>`: Remove uma ementa.

### `/pagamentos`
* `GET /pagamentos`: Lista todos os registros de pagamento.
* `GET /pagamentos/<id>`: Busca um pagamento específico.
* `POST /pagamentos`: Registra um novo pagamento. Requer: `id_estudante`, `data_pagamento`, `valor`, `tipo`, `estado`, `referente_a`.
* `PUT /pagamentos/<id>`: Atualiza um registro de pagamento.
* `DELETE /pagamentos/<id>`: Remove um registro de pagamento.
