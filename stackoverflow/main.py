from flask import Flask, jsonify, request


app = Flask(__name__)
questions = [
    {
        "id": 1,
        "question": "Log in to use Flask",
        "description": "I would like to use Flask for authentication purpose",
        "stack":"Python, HTML, CSS"
        }
]

@app.route('/api/v1/')
def hello():
    return 'Hello, Smith'

@app.route('/api/v1/questions', methods=['GET'])
def get_questions():
    return jsonify(questions)

@app.route('/api/v1/questions/', methods=['POST'])
def add_questions():
    data = request.get_json()
    questions.append(data)
    return jsonify({"data": data}), 201

@app.route('/api/v1/questions/<int:id>', methods=['GET'])
def get_question(id):
    for question in questions:
        if question['id'] == id:
            return jsonify(question), 200
    return jsonify({
        "error": f"A question with id {id} is non-existent"
        }), 404

@app.route('/api/v1/questions/<int:id>/', methods=['PATCH'])
def edit_question(id):
    data = request.get_json()
    for question in questions:
        if question['id'] == id:
            question['question']=data['question']
            question['description']=data['description']
            question['stack']=data['stack']
            return jsonify(question), 200
    return jsonify({
        "error": f"A question with id {id} is non-existent"
        }), 404

@app.route('/api/v1/questions/<int:id>', methods=['DELETE'])
def delete_question(id):
    for question in range(len(questions)):
        if questions[question]['id'] == id:
            del questions[question]
            return jsonify({"success": f"Question {id} deleted!"}), 200
    return jsonify({
        "error": f"A question with id {id} is non-existent"
        }), 404




if __name__=='__main__':
    app.run(debug=True)