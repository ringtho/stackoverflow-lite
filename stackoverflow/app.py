from flask import Flask, jsonify, request
from flask_jwt import JWT
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'sringtho'

jwt = JWT(app, authenticate, identity)


questions = [
    {
        "id": 1,
        "question": "Log in to use Flask",
        "description": "I would like to use Flask for authentication purpose",
        "stack":"Python, HTML, CSS",
        "answers": []
        }
]

@app.route('/questions')
def get_questions():
    return jsonify({"questions": questions})

@app.route('/questions', methods=["POST"])
def add_question():
    data = request.get_json()
    question = next(filter(lambda x: x['id'] == data['id'], questions), None)
    if question:
        return jsonify({"error": f"The id {data['id']} already exists!"}), 400
    new_question = {
        "id": data['id'],
        "question": data['question'],
        "description": data['description'],
        "stack": data['stack'],
        "answers": []
    }
    questions.append(new_question)
    return new_question, 201

@app.route('/questions/<int:id>')
def get_question(id):
    question = next(filter(lambda x: x['id'] == id, questions), None)
    if question:
        return question
    return jsonify({"error" : "Question not found"}), 404

@app.route('/questions/<int:id>', methods=["PUT"])
def edit_question(id):
    data = request.get_json()
    question = next(filter(lambda x: x['id'] == id, questions), None)
    if question:
        question.update(data)
        return question
    return jsonify({"error" : "Question not found"})

@app.route('/questions/<int:id>', methods=["DELETE"])
def delete_question(id):
    global questions
    question = next(filter(lambda x: x['id'] == id, questions), None)
    if not question:
        return jsonify({"error" : "Question not found"}), 404
    questions = list(filter(lambda x: x['id'] != id, questions))
    return jsonify({"message": "Question successfully deleted"})

@app.route('/questions/<int:id>/answers', methods=["POST"])
def add_answer(id):
    data = request.get_json()
    question = next(filter(lambda x: x['id'] == id, questions), None)
    if question:
        new_answer = {
            "id": data['id'],
            "answer": data['answer'],
            "preferred": False
        }
        answer = next(filter(lambda x : x['id'] == data['id'], question['answers']),None)
        if answer:
            return jsonify({"error": f"The id {data['id']} already exists!"}), 400
        question['answers'].append(new_answer)
        return question, 201
    return jsonify({"error" : "Question not found"}), 404

@app.route('/questions/<int:id>/answers/<int:answer_id>', methods=["PUT"])
def update_answer_as_preferred(id, answer_id):
    data = request.get_json()
    question = next(filter(lambda x: x['id'] == id, questions), None)
    if not question:
        return jsonify({"error" : "Question not found"}), 404
    answer = next(filter(lambda x : x['id'] == answer_id, question['answers']),None)
    if not answer:
        return jsonify({"error" : "Answer not found"}), 404
    answer.update(data)
    return answer
    



if __name__ == '__main__':
    app.run(debug=True, port=5000)