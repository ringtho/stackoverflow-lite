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

#get a particular question

#edit a particular question

#delete a particular question

if __name__=='__main__':
    app.run(debug=True)