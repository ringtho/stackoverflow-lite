import pytest
import json
from app import app

question = {
    "id": 2,
    "question": "Django Rest Framework",
    "description": "Whenever I am logging in I get an error that affects my application",
    "stack": "Django, Python"
}

def test_get_questions():
    response = app.test_client().get('/questions')
    res = json.loads(response.data.decode('utf-8')).get('questions')
    assert type(res) is list
    assert res[0]['id'] == 1
    assert type(res[0]['answers']) is list
    assert type(res[0]) is dict
    assert response.status_code == 200

def test_get_single_question():
    response = app.test_client().get('/questions/1')
    res = json.loads(response.data.decode('utf-8'))
    assert type(res) is dict
    assert res['id'] == 1
    assert res['question'] == "Log in to use Flask"
    assert response.status_code == 200

def test_post_question_no_token():
    response = app.test_client().post('/questions', json=question)
    res = json.loads(response.data.decode('utf-8'))
    assert type(res) is dict
    assert res['error'] == "Invalid token. Please provide a valid token"
    assert response.status_code == 401

