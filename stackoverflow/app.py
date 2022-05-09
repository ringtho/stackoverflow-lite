from datetime import timedelta
from flask import Flask, jsonify, request
from flask_jwt import JWT, jwt_required
from security import authenticate, identity, users, userid_mapping



app = Flask(__name__)
app.secret_key = 'sringtho'

app.config['JWT_AUTH_URL_RULE'] = '/auth/login'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

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

# @app.route('/auth/profile/<int:id>', methods=["PUT"])
# @jwt_required()
# def update_profile(id):
#     data = request.get_json()
#     user = next(filter(lambda x: x['id'] == id, users), None)
#     if user:
#         user.update(data)
#         return user
#     return jsonify({"error" : "User not found"})


# @app.route('/auth/profile/<int:id>')
# @jwt_required()
# def get_user_profile(id):
#     user = userid_mapping.get(id, None)
#     if user is None:
#         return jsonify({"error":"User not found!"}), 404
#     return user


@app.route('/auth/signup', methods=["POST"])
def signup():
    data = request.get_json()
    user = next(filter(lambda x: x['username'] == data['username'], users), None)
    if user:
        return jsonify(
            {"error": f"A user with the username '{data['username']}' already exists"}
            ), 400
    user = next(filter(lambda x: x['email'] == data['email'], users), None)
    if user:
        return jsonify(
            {"error": f"A user with the email '{data['email']}' already exists"}
            ), 400
    new_user = {
        "id": data["id"],
        "username": data["username"],
        "email": data["email"],
        "fullname": data["fullname"],
        "sex": data["sex"],
        "password": data["password"]
    }
    # new_user = User(data['id'],data['username'],data['email'],data['fullname'],data['sex'],data['password'])
    users.append(new_user)
    return new_user, 201



@app.route('/questions')
def get_questions():
    return jsonify({"questions": questions})

@app.route('/questions', methods=["POST"])
# @jwt_required()
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
# @jwt_required()
def edit_question(id):
    data = request.get_json()
    question = next(filter(lambda x: x['id'] == id, questions), None)
    if question:
        question.update(data)
        return question
    return jsonify({"error" : "Question not found"})

@app.route('/questions/<int:id>', methods=["DELETE"])
# @jwt_required()
def delete_question(id):
    global questions
    question = next(filter(lambda x: x['id'] == id, questions), None)
    if not question:
        return jsonify({"error" : "Question not found"}), 404
    questions = list(filter(lambda x: x['id'] != id, questions))
    return jsonify({"message": "Question successfully deleted"})

@app.route('/questions/<int:id>/answers', methods=["POST"])
# @jwt_required()
def add_answer(id):
    data = request.get_json()
    question = next(filter(lambda x: x['id'] == id, questions), None)
    if question:
        new_answer = {
            "id": data['id'],
            "answer": data['answer'],
            "preferred": False,
            "comments": []
        }
        answer = next(filter(lambda x : x['id'] == data['id'], question['answers']),None)
        if answer:
            return jsonify({"error": f"The id {data['id']} already exists!"}), 400
        question['answers'].append(new_answer)
        return question, 201
    return jsonify({"error" : "Question not found"}), 404

@app.route('/questions/<int:id>/answers/<int:answer_id>', methods=["PUT"])
# @jwt_required()
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

@app.route('/questions/<int:id>/answers/<int:answer_id>/comments', methods=["POST"])
# @jwt_required()
def comment_on_answer(id, answer_id):
    data = request.get_json()
    question = next(filter(lambda x: x['id'] == id, questions), None)
    if not question:
        return jsonify({"error" : "Question not found"}), 404
    answer = next(filter(lambda x : x['id'] == answer_id, question['answers']),None)
    if not answer:
        return jsonify({"error" : "Answer not found"}), 404
    comment = {"id": data["id"], "comment": data["comment"]}
    answer['comments'].append(comment)
    return answer, 201

    



if __name__ == '__main__':
    app.run(debug=True, port=5000)