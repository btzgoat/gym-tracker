from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

exercises_db = []
next_exercise_id = 1

@app.route('/exercises', methods=['GET'])
def get_exercises():
    """
    Retorna a lista de todos os exercícios armazenados.
    Exemplo de requisição: GET /exercises
    Exemplo de resposta: [{"id": 1, "name": "Supino", "sets": 3, "reps": 10}]
    """
    return jsonify(exercises_db)

@app.route('/exercises', methods=['POST'])
def add_exercise():
    """
    Adiciona um novo exercício à lista.
    Espera um JSON no corpo da requisição com o campo 'name'.
    Exemplo de requisição: POST /exercises
    Corpo: {"name": "Agachamento"}
    Exemplo de resposta: {"id": 1, "name": "Agachamento", "sets": 0, "reps": 0}
    """
    global next_exercise_id
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Nome do exercício é obrigatório"}), 400

    new_exercise = {
        "id": next_exercise_id,
        "name": data['name'],
        "sets": 0,
        "reps": 0
    }
    exercises_db.append(new_exercise)
    next_exercise_id += 1
    return jsonify(new_exercise), 201

@app.route('/exercises/<int:exercise_id>', methods=['PUT'])
def update_exercise(exercise_id):
    """
    Atualiza um exercício existente pelo ID.
    Espera um JSON no corpo da requisição com os campos 'sets' e/ou 'reps'.
    Exemplo de requisição: PUT /exercises/1
    Corpo: {"sets": 4, "reps": 12}
    Exemplo de resposta: {"id": 1, "name": "Agachamento", "sets": 4, "reps": 12}
    """
    data = request.get_json()
    exercise = next((e for e in exercises_db if e['id'] == exercise_id), None)

    if not exercise:
        return jsonify({"error": "Exercício não encontrado"}), 404

    if 'sets' in data:
        exercise['sets'] = data['sets']
    if 'reps' in data:
        exercise['reps'] = data['reps']

    return jsonify(exercise)

@app.route('/exercises/<int:exercise_id>', methods=['DELETE'])
def delete_exercise(exercise_id):
    """
    Deleta um exercício existente pelo ID.
    Exemplo de requisição: DELETE /exercises/1
    Exemplo de resposta: {"message": "Exercício deletado com sucesso"}
    """
    global exercises_db
    initial_len = len(exercises_db)
    exercises_db = [e for e in exercises_db if e['id'] != exercise_id]

    if len(exercises_db) < initial_len:
        return jsonify({"message": "Exercício deletado com sucesso"})
    else:
        return jsonify({"error": "Exercício não encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)