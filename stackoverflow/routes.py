from flask import Flask, jsonify, request
from .auth_token import required_token, encode_token, get_id_token
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from .models.user import users



app = Flask(__name__)


questions = [
    {
        "id": 1,
        "question": "Log in to use Flask",
        "description": "I would like to use Flask for authentication purpose",
        "stack":"Python, HTML, CSS",
        "answers": [],
        "author": "sringtho"
    }
]

def get_current_user():
    user_id = get_id_token()
    user = next(filter(lambda x: x['id'] == user_id, users), None)
    return user

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
        "password": generate_password_hash(data["password"]) 
    }
    users.append(new_user)
    return new_user, 201

@app.route('/auth/login', methods=["POST"])
def login():
    data = request.get_json()
    user = next(filter(lambda x: x['username'] == data['username'], users), None)
    if not user:
        return jsonify({"error" : "Invalid username"}), 404
    password = check_password_hash(user.get("password"), data["password"])
    if password:
        token = encode_token(user['id'], user['username'])
        return jsonify({
            "access_token": token,
            "username": user["username"],
            "email": user['email']
        })
    return jsonify({"error": "Incorrect password used"}), 400

@app.route('/auth/profile/<string:username>')
@required_token
def get_user_profile(username):
    current_user = get_current_user()
    if current_user is None:
        return jsonify({"error":"Please provide a token to continue"}), 401
    if current_user['username'] != username:
        return jsonify({"error": "You are unauthorized!"}), 401
    user = next(filter(lambda x: x['username'] == username, users), None)
    if user is None:
        return jsonify({"error":"User not found!"}), 404
    return user

@app.route('/auth/profile/<string:username>', methods=["PUT"])
@required_token
def update_profile(username):
    data = request.get_json()
    data["password"] = generate_password_hash(data['password'])
    current_user = get_current_user()
    if current_user is None:
        return jsonify({"error":"Please provide a token to continue"}), 401
    if current_user['username'] != username:
        return jsonify({"error": "You are unauthorized!"}), 401
    user = next(filter(lambda x: x['username'] == username, users), None)
    if user:
        user.update(data)
        return user
    return jsonify({"error" : "User not found"}), 404

@app.route('/questions')
def get_questions():
    return jsonify({"questions": questions})

@app.route('/questions', methods=["POST"])
@required_token
def add_question():
    current_user = get_current_user()
    if current_user is None:
        return jsonify({"error":"Please provide a token to continue"}), 401
    data = request.get_json()
    question = next(filter(lambda x: x['id'] == data['id'], questions), None)
    if question:
        return jsonify({"error": f"The id {data['id']} already exists!"}), 400
    new_question = {
        "id": data['id'],
        "question": data['question'],
        "description": data['description'],
        "stack": data['stack'],
        "answers": [],
        "author": current_user['username']
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
@required_token
def edit_question(id):
    current_user = get_current_user()
    if current_user is None:
        return jsonify({"error":"Please provide a token to continue"}), 401
    data = request.get_json()
    question = next(filter(lambda x: x['id'] == id, questions), None)
    if question:
        if current_user['username'] == question['author']:
            question.update(data)
            return question
        return jsonify({"error": "You are unauthorized!"}), 401
    return jsonify({"error" : "Question not found"})

@app.route('/questions/<int:id>', methods=["DELETE"])
@required_token
def delete_question(id):
    current_user = get_current_user()
    if current_user is None:
        return jsonify({"error":"Please provide a token to continue"}), 401
    global questions
    question = next(filter(lambda x: x['id'] == id, questions), None)
    if not question:
        return jsonify({"error" : "Question not found"}), 404
    if current_user['username'] == question['author']:
        questions = list(filter(lambda x: x['id'] != id, questions))
        return jsonify({"message": "Question successfully deleted"})
    return jsonify({"error": "You are unauthorized!"}), 401

@app.route('/questions/<int:id>/answers', methods=["POST"])
@required_token
def add_answer(id):
    current_user = get_current_user()
    if current_user is None:
        return jsonify({"error":"Please provide a token to continue"}), 401
    data = request.get_json()
    question = next(filter(lambda x: x['id'] == id, questions), None)
    if question:
        if current_user['username'] != question['author']:
            new_answer = {
                "id": data['id'],
                "author": current_user['username'],
                "answer": data['answer'],
                "preferred": False,
                "comments": []
            }
            answer = next(filter(lambda x : x['id'] == data['id'], question['answers']),None)
            if answer:
                return jsonify({"error": f"The id {data['id']} already exists!"}), 400
            question['answers'].append(new_answer)
            return question, 201
        return jsonify({'error': "You are not allowed to answer your own question"})
    return jsonify({"error" : "Question not found"}), 404

@app.route('/questions/<int:id>/answers/<int:answer_id>', methods=["PUT"])
@required_token
def update_answer_as_preferred(id, answer_id):
    current_user = get_current_user()
    if current_user is None:
        return jsonify({"error":"Please provide a token to continue"}), 401
    data = request.get_json()
    question = next(filter(lambda x: x['id'] == id, questions), None)
    if not question:
        return jsonify({"error" : "Question not found"}), 404
    answer = next(filter(lambda x : x['id'] == answer_id, question['answers']),None)
    if not answer:
        return jsonify({"error" : "Answer not found"}), 404
    if current_user['username'] == answer["author"]:
        answer['answer'] = data['answer']
        return answer
    elif current_user['username'] == question["author"]:
        answer['preferred'] = data['preferred']
        return answer
    else:
        return jsonify({"error": "You are unauthorized!"}), 401

@app.route('/questions/<int:id>/answers/<int:answer_id>/comments', methods=["POST"])
@required_token
def comment_on_answer(id, answer_id):
    current_user = get_current_user()
    if current_user is None:
        return jsonify({"error":"Please provide a token to continue"}), 401
    data = request.get_json()
    question = next(filter(lambda x: x['id'] == id, questions), None)
    if not question:
        return jsonify({"error" : "Question not found"}), 404
    answer = next(filter(lambda x : x['id'] == answer_id, question['answers']),None)
    if not answer:
        return jsonify({"error" : "Answer not found"}), 404
    comment = {
        "id": data["id"],
        "comment": data["comment"], 
        "author": current_user['username']
        }
    answer['comments'].append(comment)
    return comment, 201

    



