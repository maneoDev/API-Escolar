from flask import Flask, request, jsonify
import psycopg2
from bd import criar_conexao

app = Flask(__name__)

def executar_query(query, params=None, fetch=False):
    conn = criar_conexao()
    if conn is None:
        return False
    
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        if fetch:
            result = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]
            return [dict(zip(colnames, row)) for row in result]
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro na query: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

@app.route('/estudantes', methods=['GET'])
def get_estudantes():
    query = "SELECT Id_Estudante, Nome, Email, Telefone, Curso, Estado FROM Estudante"
    estudantes = executar_query(query, fetch=True)
    return jsonify(estudantes)

@app.route('/estudantes/<int:id>', methods=['GET'])
def get_estudante(id):
    query = "SELECT Id_Estudante, Nome, Email, Telefone, Curso, Estado FROM Estudante WHERE Id_Estudante = %s"
    estudante = executar_query(query, (id,), fetch=True)
    if estudante:
        return jsonify(estudante)
    return jsonify({"erro": "Estudante não encontrado"}), 404

@app.route('/estudantes', methods=['POST'])
def add_estudante():
    dados = request.get_json()

    # Validações básicas
    if not dados.get('nome') or len(dados['nome']) < 3:
        return jsonify({"erro": "Nome inválido"}), 400

    query = """
    INSERT INTO Estudante (Nome, Cpf, Data_Nascimento, Email, Telefone, Curso, Matricula, Estado)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = (
        dados['nome'],
        dados['cpf'],
        dados['data_nascimento'],
        dados['email'],
        dados['telefone'],
        dados['curso'],
        dados['matricula'],
        dados['estado']
    )
    if executar_query(query, params):
        return jsonify({"mensagem": "Estudante adicionado com sucesso"}), 201
    return jsonify({"erro": "Falha ao adicionar estudante"}), 400

@app.route('/estudantes/<int:id>', methods=['PUT'])
def update_estudante(id):
    dados = request.get_json()

    query = """
    UPDATE Estudante
    SET Nome = %s, Cpf = %s, Data_Nascimento = %s, Email = %s, 
        Telefone = %s, Curso = %s, Matricula = %s, Estado = %s
    WHERE Id_Estudante = %s
    """
    params = (
        dados.get('nome'),
        dados.get('cpf'),
        dados.get('data_nascimento'),
        dados.get('email'),
        dados.get('telefone'),
        dados.get('curso'),
        dados.get('matricula'),
        dados.get('estado'),
        id
    )
    if executar_query(query, params):
        return jsonify({"mensagem": "Estudante atualizado com sucesso"})
    return jsonify({"erro": "Falha ao atualizar estudante"}), 400

@app.route('/estudantes/<int:id>', methods=['DELETE'])
def delete_estudante(id):
    query = "DELETE FROM Estudante WHERE Id_Estudante = %s"
    if executar_query(query, (id,)):
        return jsonify({"mensagem": "Estudante removido com sucesso"})
    return jsonify({"erro": "Falha ao remover estudante"}), 400

# Rotas para Disciplina (padrão similar aos estudantes)
@app.route('/disciplinas', methods=['GET'])
def get_disciplinas():
    query = "SELECT * FROM Disciplina"
    disciplinas = executar_query(query, fetch=True)
    return jsonify(disciplinas)

@app.route('/disciplinas', methods=['POST'])
def add_disciplina():
    dados = request.get_json()

    # Validação básica
    if not dados.get('nome_disciplina') or len(dados['nome_disciplina']) < 3:
        return jsonify({"erro": "Nome da disciplina inválido"}), 400

    query = """
    INSERT INTO Disciplina (nome_disciplina, carga_horaria, id_coordenador, curso_relacionado)
    VALUES (%s, %s, %s, %s)
    """
    params = (
        dados['nome_disciplina'],
        dados['carga_horaria'],
        dados['id_coordenador'],
        dados['curso_relacionado']
    )
    if executar_query(query, params):
        return jsonify({"mensagem": "Disciplina adicionada com sucesso"}), 201
    return jsonify({"erro": "Falha ao adicionar disciplina"}), 400

@app.route('/disciplinas/<int:id>', methods=['PUT'])
def update_disciplina(id):
    dados = request.get_json()

    query = """
    UPDATE Disciplina
    SET nome_disciplina = %s, carga_horaria = %s, id_coordenador = %s, curso_relacionado = %s
    WHERE id_disciplina = %s
    """
    params = (
        dados.get('nome_disciplina'),
        dados.get('carga_horaria'),
        dados.get('id_coordenador'),
        dados.get('curso_relacionado'),
        id
    )
    if executar_query(query, params):
        return jsonify({"mensagem": "Disciplina atualizada com sucesso"})
    return jsonify({"erro": "Falha ao atualizar disciplina"}), 400

@app.route('/disciplinas/<int:id>', methods=['DELETE'])
def delete_disciplina(id):
    query = "DELETE FROM Disciplina WHERE id_disciplina = %s"
    if executar_query(query, (id,)):
        return jsonify({"mensagem": "Disciplina removida com sucesso"})
    return jsonify({"erro": "Falha ao remover disciplina"}), 400

@app.route('/turmas', methods=['GET'])
def get_turmas():
    query = "SELECT * FROM Turma"
    turmas = executar_query(query, fetch=True)
    return jsonify(turmas)

@app.route('/turmas/<int:id>', methods=['GET'])
def get_turma(id):
    query = "SELECT * FROM Turma WHERE id_turma = %s"
    turma = executar_query(query, (id,), fetch=True)
    if turma:
        return jsonify(turma)
    return jsonify({"erro": "Turma não encontrada"}), 404

@app.route('/turmas', methods=['POST'])
def add_turma():
    dados = request.get_json()

    # Validação básica
    if not dados.get('horario') or len(dados['horario']) < 5:
        return jsonify({"erro": "Horário inválido"}), 400

    query = """
    INSERT INTO Turma (id_disciplina, id_professor, semestre, ano_letivo, Horario, Sala)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = (
        dados['id_disciplina'],
        dados['id_professor'],
        dados['semestre'],
        dados['ano_letivo'],
        dados['horario'],
        dados['sala']
    )
    if executar_query(query, params):
        return jsonify({"mensagem": "Turma adicionada com sucesso"}), 201
    return jsonify({"erro": "Falha ao adicionar turma"}), 400

@app.route('/turmas/<int:id>', methods=['PUT'])
def update_turma(id):
    dados = request.get_json()

    query = """
    UPDATE Turma
    SET id_disciplina = %s, id_professor = %s, semestre = %s, ano_letivo = %s, Horario = %s, Sala = %s
    WHERE id_turma = %s
    """
    params = (
        dados.get('id_disciplina'),
        dados.get('id_professor'),
        dados.get('semestre'),
        dados.get('ano_letivo'),
        dados.get('horario'),
        dados.get('sala'),
        id
    )
    if executar_query(query, params):
        return jsonify({"mensagem": "Turma atualizada com sucesso"})
    return jsonify({"erro": "Falha ao atualizar turma"}), 400

@app.route('/turmas/<int:id>', methods=['DELETE'])
def delete_turma(id):
    query = "DELETE FROM Turma WHERE id_turma = %s"
    if executar_query(query, (id,)):
        return jsonify({"mensagem": "Turma removida com sucesso"})
    return jsonify({"erro": "Falha ao remover turma"}), 400

@app.route('/notas', methods=['GET'])
def get_notas():
    query = "SELECT * FROM Notas"
    notas = executar_query(query, fetch=True)
    return jsonify(notas)

@app.route('/notas/<int:id>', methods=['GET'])
def get_nota(id):
    query = "SELECT * FROM Notas WHERE id_nota = %s"
    nota = executar_query(query, (id,), fetch=True)
    if nota:
        return jsonify(nota)
    return jsonify({"erro": "Nota não encontrada"}), 404

@app.route('/notas', methods=['POST'])
def add_nota():
    dados = request.get_json()

    # Validação básica
    if 'nota_1' not in dados or 'nota_2' not in dados or 'frequencia' not in dados:
        return jsonify({"erro": "Nota ou frequência não informada"}), 400

    query = """
    INSERT INTO Notas (id_estudante, id_disciplina, id_turma, nota_1, nota_2, media_final, frequencia, estado)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = (
        dados['id_estudante'],
        dados['id_disciplina'],
        dados['id_turma'],
        dados['nota_1'],
        dados['nota_2'],
        (dados['nota_1'] + dados['nota_2']) / 2,  # Calculando média automaticamente
        dados['frequencia'],
        dados.get('estado', 'Em análise')  # Estado padrão
    )
    if executar_query(query, params):
        return jsonify({"mensagem": "Nota adicionada com sucesso"}), 201
    return jsonify({"erro": "Falha ao adicionar nota"}), 400

@app.route('/notas/<int:id>', methods=['PUT'])
def update_nota(id):
    dados = request.get_json()

    query = """
    UPDATE Notas
    SET id_estudante = %s, id_disciplina = %s, id_turma = %s, nota_1 = %s, nota_2 = %s, 
        media_final = %s, frequencia = %s, estado = %s
    WHERE id_nota = %s
    """
    params = (
        dados.get('id_estudante'),
        dados.get('id_disciplina'),
        dados.get('id_turma'),
        dados.get('nota_1'),
        dados.get('nota_2'),
        (dados['nota_1'] + dados['nota_2']) / 2,  # Atualizando média automaticamente
        dados.get('frequencia'),
        dados.get('estado', 'Em análise'),
        id
    )
    if executar_query(query, params):
        return jsonify({"mensagem": "Nota atualizada com sucesso"})
    return jsonify({"erro": "Falha ao atualizar nota"}), 400

@app.route('/notas/<int:id>', methods=['DELETE'])
def delete_nota(id):
    query = "DELETE FROM Notas WHERE id_nota = %s"
    if executar_query(query, (id,)):
        return jsonify({"mensagem": "Nota removida com sucesso"})
    return jsonify({"erro": "Falha ao remover nota"}), 400

@app.route('/ementas', methods=['GET'])
def get_ementas():
    query = "SELECT * FROM Ementa"
    ementas = executar_query(query, fetch=True)
    return jsonify(ementas)

@app.route('/ementas/<int:id>', methods=['GET'])
def get_ementa(id):
    query = "SELECT * FROM Ementa WHERE id_ementa = %s"
    ementa = executar_query(query, (id,), fetch=True)
    if ementa:
        return jsonify(ementa)
    return jsonify({"erro": "Ementa não encontrada"}), 404

@app.route('/ementas', methods=['POST'])
def add_ementa():
    dados = request.get_json()

    # Validação básica
    if not dados.get('descricao') or len(dados['descricao']) < 5:
        return jsonify({"erro": "Descrição inválida"}), 400

    query = """
    INSERT INTO Ementa (id_disciplina, descricao, objetivos, bibliografia, metodologia, avaliacao)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = (
        dados['id_disciplina'],
        dados['descricao'],
        dados['objetivos'],
        dados['bibliografia'],
        dados['metodologia'],
        dados['avaliacao']
    )
    if executar_query(query, params):
        return jsonify({"mensagem": "Ementa adicionada com sucesso"}), 201
    return jsonify({"erro": "Falha ao adicionar ementa"}), 400

@app.route('/ementas/<int:id>', methods=['PUT'])
def update_ementa(id):
    dados = request.get_json()

    query = """
    UPDATE Ementa
    SET id_disciplina = %s, descricao = %s, objetivos = %s, bibliografia = %s, metodologia = %s, avaliacao = %s
    WHERE id_ementa = %s
    """
    params = (
        dados.get('id_disciplina'),
        dados.get('descricao'),
        dados.get('objetivos'),
        dados.get('bibliografia'),
        dados.get('metodologia'),
        dados.get('avaliacao'),
        id
    )
    if executar_query(query, params):
        return jsonify({"mensagem": "Ementa atualizada com sucesso"})
    return jsonify({"erro": "Falha ao atualizar ementa"}), 400

@app.route('/ementas/<int:id>', methods=['DELETE'])
def delete_ementa(id):
    query = "DELETE FROM Ementa WHERE id_ementa = %s"
    if executar_query(query, (id,)):
        return jsonify({"mensagem": "Ementa removida com sucesso"})
    return jsonify({"erro": "Falha ao remover ementa"}), 400

@app.route('/pagamentos', methods=['GET'])
def get_pagamentos():
    query = "SELECT * FROM Pagamento"
    pagamentos = executar_query(query, fetch=True)
    return jsonify(pagamentos)

@app.route('/pagamentos/<int:id>', methods=['GET'])
def get_pagamento(id):
    query = "SELECT * FROM Pagamento WHERE id_pagamento = %s"
    pagamento = executar_query(query, (id,), fetch=True)
    if pagamento:
        return jsonify(pagamento)
    return jsonify({"erro": "Pagamento não encontrado"}), 404

@app.route('/pagamentos', methods=['POST'])
def add_pagamento():
    dados = request.get_json()

    # Validação básica
    if not dados.get('valor') or dados['valor'] <= 0:
        return jsonify({"erro": "Valor inválido"}), 400

    query = """
    INSERT INTO Pagamento (id_estudante, data_pagamento, valor, tipo, estado, referente_a)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = (
        dados['id_estudante'],
        dados['data_pagamento'],
        dados['valor'],
        dados['tipo'],
        dados['estado'],
        dados['referente_a']
    )
    if executar_query(query, params):
        return jsonify({"mensagem": "Pagamento registrado com sucesso"}), 201
    return jsonify({"erro": "Falha ao registrar pagamento"}), 400

@app.route('/pagamentos/<int:id>', methods=['PUT'])
def update_pagamento(id):
    dados = request.get_json()

    query = """
    UPDATE Pagamento
    SET id_estudante = %s, data_pagamento = %s, valor = %s, tipo = %s, estado = %s, referente_a = %s
    WHERE id_pagamento = %s
    """
    params = (
        dados.get('id_estudante'),
        dados.get('data_pagamento'),
        dados.get('valor'),
        dados.get('tipo'),
        dados.get('estado'),
        dados.get('referente_a'),
        id
    )
    if executar_query(query, params):
        return jsonify({"mensagem": "Pagamento atualizado com sucesso"})
    return jsonify({"erro": "Falha ao atualizar pagamento"}), 400

@app.route('/pagamentos/<int:id>', methods=['DELETE'])
def delete_pagamento(id):
    query = "DELETE FROM Pagamento WHERE id_pagamento = %s"
    if executar_query(query, (id,)):
        return jsonify({"mensagem": "Pagamento removido com sucesso"})
    return jsonify({"erro": "Falha ao remover pagamento"}), 400

if __name__ == '__main__':
    app.run(debug=True)
