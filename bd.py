import psycopg2
from psycopg2 import OperationalError

def criar_conexao():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="projeto_bd1",
            user="postgres",
            password="161501-"
        )
        print("Conexão ao PostgreSQL bem-sucedida")
        return conn
    except OperationalError as e:
        print(f"Erro ao conectar ao PostgreSQL: {e}")
        return None

def criar_tabelas():
    conn = criar_conexao()
    cursor = conn.cursor()

    comandos = [
        """
        CREATE TABLE IF NOT EXISTS Estudante (
            Id_Estudante SERIAL PRIMARY KEY,
            Nome VARCHAR(50) NOT NULL,
            Cpf VARCHAR(11) NOT NULL UNIQUE,
            Data_Nascimento VARCHAR(8) NOT NULL,
            Email VARCHAR(50) NOT NULL,
            Telefone VARCHAR(11) NOT NULL,
            Curso VARCHAR(50) NOT NULL,
            Matricula VARCHAR(10) NOT NULL UNIQUE,
            Estado VARCHAR(50) NOT NULL,
            CONSTRAINT chk_nome_minimo CHECK(CHAR_LENGTH(Nome)>=3),
            CONSTRAINT chk_cpf CHECK(CHAR_LENGTH(Cpf)=11),
            CONSTRAINT chk_email CHECK(CHAR_LENGTH(Email)>=5),
            CONSTRAINT chk_telefone CHECK(CHAR_LENGTH(Telefone)>=10)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Disciplina (
            id_disciplina SERIAL PRIMARY KEY,
            nome_disciplina VARCHAR(50) NOT NULL,
            carga_horaria VARCHAR(10) NOT NULL,
            id_coordenador INT NOT NULL,
            curso_relacionado VARCHAR(50) NOT NULL,
            CONSTRAINT chk_disciplina CHECK(CHAR_LENGTH(nome_disciplina)>=3)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Turma (
            id_turma SERIAL PRIMARY KEY,
            id_disciplina INT NOT NULL,
            id_professor INT NOT NULL,
            semestre INT NOT NULL,
            ano_letivo INT NOT NULL,
            Horario VARCHAR(20) NOT NULL,
            Sala VARCHAR(30) NOT NULL,
            FOREIGN KEY(id_disciplina) REFERENCES Disciplina(id_disciplina)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Notas (
            id_nota SERIAL PRIMARY KEY,
            id_estudante INT NOT NULL,
            id_disciplina INT NOT NULL,
            id_turma INT NOT NULL,
            nota_1 DECIMAL(3,1) NOT NULL,
            nota_2 DECIMAL(3,1) NOT NULL,
            media_final DECIMAL(3,1) NOT NULL,
            frequencia DECIMAL(3,1) NOT NULL,
            estado VARCHAR(15),
            FOREIGN KEY(id_estudante) REFERENCES Estudante(Id_Estudante),
            FOREIGN KEY(id_disciplina) REFERENCES Disciplina(id_disciplina)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Ementa (
            id_ementa SERIAL PRIMARY KEY,
            id_disciplina INT NOT NULL,
            descricao VARCHAR(100) NOT NULL,
            objetivos VARCHAR(100) NOT NULL,
            bibliografia VARCHAR(100) NOT NULL,
            metodologia VARCHAR(200) NOT NULL,
            avaliacao VARCHAR(50) NOT NULL,
            FOREIGN KEY(id_disciplina) REFERENCES Disciplina(id_disciplina)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Pagamento (
            id_pagamento SERIAL PRIMARY KEY,
            id_estudante INT NOT NULL,
            data_pagamento VARCHAR(10) NOT NULL,
            valor DECIMAL(10,2) NOT NULL,
            tipo VARCHAR(20) NOT NULL,
            estado VARCHAR(15) NOT NULL,
            referente_a VARCHAR(20) NOT NULL,
            FOREIGN KEY(id_estudante) REFERENCES Estudante(Id_Estudante)
        )
        """
    ]

    try:
        for comando in comandos:
            cursor.execute(comando)
        conn.commit()
        print("Tabelas criadas com sucesso")
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

criar_tabelas()
