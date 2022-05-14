from flask import Flask, jsonify, request
from .resources.auth_token import required_token, encode_token
from .resources.validator import (QuestionValidator, 
UserValidator, LoginValidator, AnswerValidator, CommentValidator)
from werkzeug.security import generate_password_hash, check_password_hash
from .models.user import User
from .models.question import Question
from .models.answer import Answer
from .models.comment import Comment



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
    current_user = User().get_current_user_from_token()
    if current_user is None:
        return jsonify({"error":"Please provide a token to continue"}), 401
    data = request.get_json()
    validator = QuestionValidator(request)
    if validator.question_is_valid():
        Question().create_question(data['title'],data['description'],
        data['stack'], current_user['username'])
        new_question = {
            "title": data['title'],
            "description": data['description'],
            "stack": data['stack'],
            "author": current_user['username']
        }
        return jsonify({"success":"Successfully created a new question",
        "data": new_question}), 201
    return jsonify({"error": validator.error}), 400

@app.route('/questions/<int:id>')
def get_question(id):
    question = Question().get_question_by_id(id)
    if question:
        answers = Answer().get_answers_for_question(question['id'])
        return jsonify({
            "question": question,
            "answers": answers
            })
    return jsonify({"error" : "Question not found"}), 404

@app.route('/questions/<int:id>', methods=["PUT"])
@required_token
def edit_question(id):
    current_user = User().get_current_user_from_token()
    if current_user is None:
        return jsonify({"error":"Please provide a token to continue"}), 401
    data = request.get_json()
    validator = QuestionValidator(request)
    if not validator.question_is_valid():
        return jsonify({"error": validator.error}), 400
    record = Question().update_question(id,current_user['username'],
    data['title'],data['description'],data['stack'])
    if record > 0:
        return jsonify({"success":"Question successfully updated"})
    return jsonify({"error" : "Question not found"}), 404

@app.route('/questions/<int:id>', methods=["DELETE"])
@required_token
def delete_question(id):
    current_user = User().get_current_user_from_token()
    if current_user is None:
        return jsonify({"error":"Please provide a token to continue"}), 401
    question = Question().delete_question_by_id(id, current_user['username'])
    if question:
        return jsonify({"message": "Question successfully deleted"})
    return jsonify({"error" : "Question not found"}), 404

@app.route('/questions/<int:id>/answers', methods=["POST"])
@required_token
def add_answer(id):
    current_user = User().get_current_user_from_token()
    if current_user is None:
        return jsonify({"error":"Please provide a token to continue"}), 401
    data = request.get_json()
    question = Question().get_question_by_id(id)
    if question is None:
        return jsonify({"error" : "Question not found"}), 404
    validator = AnswerValidator(request)
    if not validator.answer_is_valid():
        return jsonify({"error": validator.error}), 400
    question_id = question['id']
    if current_user['username'] != question['author']:
        Answer().create_answer(question_id, data['answer'], 
        False, current_user['username'])
        new_answer = {
            "question": question_id,
            "author": current_user['username'],
            "answer": data['answer'],
            "preferred": False,
        }
        return jsonify({
        "success":"Successfully provided an answer",
        "data": new_answer
        }), 201
    return jsonify({'error': "You are not allowed to answer your own question"})

@app.route('/questions/<int:id>/answers/<int:answer_id>')
@required_token
def get_answer(id, answer_id):
    current_user = User().get_current_user_from_token()
    if current_user is None:
        return jsonify({"error":"Please provide a token to continue"}), 401
    question = Question().get_question_by_id(id)
    if question is None:
        return jsonify({"error" : "Question not found"}), 404
    answer = Answer().get_answer_by_answer_id(id, answer_id)
    if not answer:
        return jsonify({"error" : "Answer not found"}), 404
    comments = Comment().get_comments_by_answer_id(answer_id)
    return jsonify({"answer": answer, "comments": comments})

@app.route('/questions/<int:id>/answers/<int:answer_id>', methods=["DELETE"])
@required_token
def delete_answer(id,answer_id):
    current_user = User().get_current_user_from_token()
    if current_user is None:
        return jsonify({"error":"Please provide a token to continue"}), 401
    question = Question().get_question_by_id(id)
    if question is None:
        return jsonify({"error" : "Question not found"}), 404
    response = Answer().delete_answer_by_id(answer_id, current_user['username'])
    if response:
        return jsonify({"message": "Answer successfully deleted"})
    return jsonify({"error" : "Answer not found"}), 404

@app.route('/questions/<int:id>/answers/<int:answer_id>', methods=["PUT"])
@required_token
def update_answer_as_preferred(id, answer_id):
    current_user = User().get_current_user_from_token()
    if current_user is None:
        return jsonify({"error":"Please provide a token to continue"}), 401
    data = request.get_json()
    question = Question().get_question_by_id(id)
    if question is None:
        return jsonify({"error" : "Question not found"}), 404
    answer = Answer().get_answer_by_answer_id(id, answer_id)
    if not answer:
        return jsonify({"error" : "Answer not found"}), 404
    validator = AnswerValidator(request)
    if not validator.edit_prefered_answer_is_valid():
        return jsonify({"error": validator.error}), 400
    new_answer = {
                    "answer": answer["answer"],
                    "preferred": data['preferred']
                }
    if question['author'] == current_user['username']:
        current_preferred_answer = Answer().get_answers_with_true_preferred(id)
        if not current_preferred_answer:
            record = Answer().update_answer_preferred_option(id, 
            answer_id, data['preferred'])
            if record > 0:
                return jsonify({
                    "success": "Answer successfully updated",
                    "answer": new_answer})
            return jsonify({"error": "Answer not found!"}), 404
        Answer().update_answer_preferred_option(id, 
        current_preferred_answer['id'], False)
        record = Answer().update_answer_preferred_option(id, 
        answer_id, data['preferred'])
        if record > 0:
            return jsonify({
                    "success": "Answer successfully updated",
                    "answer": new_answer})
    return jsonify({"error": "You are not authorized"}), 401
    

@app.route('/questions/<int:id>/answers/<int:answer_id>/comments', methods=["POST"])
@required_token
def create_comment_on_answer(id, answer_id):
    current_user = User().get_current_user_from_token()
    if current_user is None:
        return jsonify({"error":"Please provide a token to continue"}), 401
    data = request.get_json()
    question = Question().get_question_by_id(id)
    if question is None:
        return jsonify({"error" : "Question not found"}), 404
    answer = Answer().get_answer_by_answer_id(id, answer_id)
    if not answer:
        return jsonify({"error" : "Answer not found"}), 404
    validator = CommentValidator(request)
    if not validator.comment_is_valid():
        return jsonify({"error": validator.error}), 400
    Comment().create_comment(answer_id, data['comment'], current_user['username'])
    comment = {
        "answer": answer,
        "comment": [
            {
                "comment": data["comment"], 
                "author": current_user['username']
            }]
        }
    return comment, 201

comment = '/questions/<int:id>/answers/<int:answer_id>/comments/<int:comment_id>'
@app.route(comment)
@required_token
def get_comment(id, answer_id, comment_id):
    current_user = User().get_current_user_from_token()
    if current_user is None:
        return jsonify({"error":"Please provide a token to continue"}), 401
    question = Question().get_question_by_id(id)
    if question is None:
        return jsonify({"error" : "Question not found"}), 404
    answer = Answer().get_answer_by_answer_id(id, answer_id)
    if not answer:
        return jsonify({"error" : "Answer not found"}), 404
    comment = Comment().get_single_comment_by_id(comment_id)
    return jsonify({"answer": answer, "comment": comment})

@app.route(comment, methods=['PUT'])
@required_token
def edit_comment(id, answer_id, comment_id):
    current_user = User().get_current_user_from_token()
    if current_user is None:
        return jsonify({"error":"Please provide a token to continue"}), 401
    data = request.get_json()
    question = Question().get_question_by_id(id)
    if question is None:
        return jsonify({"error" : "Question not found"}), 404
    answer = Answer().get_answer_by_answer_id(id, answer_id)
    if not answer:
        return jsonify({"error" : "Answer not found"}), 404
    validator = CommentValidator(request)
    if not validator.comment_is_valid():
        return jsonify({"error": validator.error}), 400
    record = Comment().update_comment(comment_id, data['comment'],
    current_user['username'])
    if record > 0:
        return jsonify({"success":"Comment successfully updated"})
    return jsonify({"error" : "Comment not found"}), 404

@app.route(comment, methods=['DELETE'])
@required_token
def delete_comment(id, answer_id, comment_id):
    current_user = User().get_current_user_from_token()
    if current_user is None:
        return jsonify({"error":"Please provide a token to continue"}), 401
    question = Question().get_question_by_id(id)
    if question is None:
        return jsonify({"error" : "Question not found"}), 404
    answer = Answer().get_answer_by_answer_id(id, answer_id)
    if not answer:
        return jsonify({"error" : "Answer not found"}), 404
    response = Comment().delete_comment(comment_id, current_user['username'])
    if response:
        return jsonify({"message": "Comment successfully deleted"})
    return jsonify({"error" : "Comment not found"}), 404

@app.route('/questions/<string:username>')
@required_token
def get_current_users_questions(username):
    current_user = User().get_current_user_from_token()
    if current_user is None:
        return jsonify({"error":"Please provide a token to continue"}), 401
    if current_user['username'] == username:
        questions = Question().get_questions_by_author(current_user['username'])
        if questions:
            return jsonify({"questions": questions})
        return jsonify({"error": "Questions not found"}), 404
    return jsonify({"error": "You are not authorised"}), 401
    






    



