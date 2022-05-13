from flask import Flask, jsonify, request
from .resources.auth_token import required_token, encode_token
from .resources.validator import QuestionValidator, UserValidator, LoginValidator
from werkzeug.security import generate_password_hash, check_password_hash
from .models.user import User
from .models.question import Question



app = Flask(__name__)

@app.route('/auth/signup', methods=["POST"])
def signup():
    data = request.get_json()
    validator = UserValidator(request)
    if validator.validate_user_data():
        password = generate_password_hash(data['password'])
        User().create_user(data['username'],data['email'],
        data['firstname'],data['lastname'],data['gender'],password)
        display_user = {
            "username": data["username"],
            "email": data["email"],
            "firstname": data["firstname"],
            "lastname": data["lastname"],
            "gender": data["gender"],
        }
        return jsonify({
            "success":"User created successfully", 
            "user": display_user}), 201
    return jsonify({"error": validator.error}), 400
    

@app.route('/auth/login', methods=["POST"])
def login():
    data = request.get_json()
    validator = LoginValidator(request)
    if not validator.validate_login_data():
        return jsonify({"error": validator.error}), 400
    user = User().get_user_auth_details(data['username'], data['password'])
    if not user:
        return jsonify({"error" : "Invalid username or password"}), 404
    token = encode_token(user['id'], user['username'])
    return jsonify({
        "access_token": token,
        "username": user["username"],
        "email": user['email']
    })

@app.route('/auth/profile/<string:username>')
@required_token
def get_user_profile(username):
    current_user = User().get_current_user_from_token()
    if current_user is None:
        return jsonify({"error":"Please provide a token to continue"}), 401
    user = User().get_user(username)
    if not user:
        return jsonify({"error":"User not found!"}), 404
    if current_user['username'] != user['username']:
        return jsonify({"error": "You are not authorized!"}), 401
    return user

@app.route('/auth/profile/<string:username>', methods=["PUT"])
@required_token
def update_password(username):
    current_user = User().get_current_user_from_token()
    if current_user is None:
        return jsonify({"error":"Please provide a token to continue"}), 401
    if current_user['username'] != username:
            return jsonify({"error": "You are not authorized!"}), 401
    data = request.get_json()
    validator = UserValidator(request)
    if validator.password_is_valid():
        user = User().get_user_auth_details(username, data['old_password'])
        if not user:
            return jsonify({"error": "Incorrect old password!"}), 401
        if check_password_hash(user['password'], data['new_password']):
            return jsonify({
                "error": "The new password cannot be the same as the old password"}
                ), 401
        password = generate_password_hash(data['new_password'])
        record = User().update_user_password(username, password)
        if record > 0:
            return jsonify({"success":"Password successfully updated"})    
        return jsonify({"error" : "User not found"}), 404
    return jsonify({"error": validator.error}), 400

@app.route('/questions')
def get_questions():
    questions = Question().get_questions()
    if questions:
        return jsonify({"questions": questions})
    return jsonify({"error": "No questions currently in the database"}), 404

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
    validator = QuestionValidator(request)
    if validator.question_is_valid():
        new_question = {
            "id": data['id'],
            "title": data['title'],
            "description": data['description'],
            "stack": data['stack'],
            "answers": [],
            "author": current_user['username']
        }
        questions.append(new_question)
        return new_question, 201
    return jsonify({"error": validator.error}), 400

@app.route('/questions/<int:id>')
def get_question(id):
    question = Question().get_question(id)
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

    



