from flask import Flask, jsonify, request

app = Flask(__name__)


questions = [
    {
        "id": 1,
        "question": "Log in to use Flask",
        "description": "I would like to use Flask for authentication purpose",
        "stack":"Python, HTML, CSS",
        "answers": []
        }
]

#get questions
@app.route('/questions')
def get_questions():
    return jsonify({"questions": questions})

#post a question
@app.route('/questions', methods=["POST"])
def add_question():
    data = request.get_json()
    question = {
        "id": data['id'],
        "question": data['question'],
        "description": data['description'],
        "stack": data['stack'],
        "answers": []
    }
    qn = next(filter(lambda x: x['id'] == data['id'], questions), None)
    if qn:
        return jsonify({"error": f"The id {data['id']} already exists!"}), 400
    questions.append(question)
    return question, 201




#get a particular question

#edit a particular question

#delete a particular question

if __name__ == '__main__':
    app.run(debug=True, port=5000)