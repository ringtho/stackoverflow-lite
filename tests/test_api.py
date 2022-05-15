import pytest
import json
from stackoverflow.routes import app

question = {
    "title": "Need to lesrn Flex",
    "description": "I need to learn more frontend",
    "stack": "HTML, CSS"
}

def test_get_questions():
    response = app.test_client().get('/questions')
    res = json.loads(response.data.decode('utf-8')).get('questions')
    assert type(res) is list
    assert res[0]['id'] == 2
    assert res[0]['author'] == 'sringtho'
    assert type(res[0]) is dict
    assert response.status_code == 200

def test_get_single_question():
    response = app.test_client().get('/questions/1')
    res = json.loads(response.data.decode('utf-8'))
    assert type(res['answers']) is list
    assert type(res) is dict
    assert res['question']['id'] == 1
    assert res['question']['title'] == "I think we try REact"
    assert response.status_code == 200

def test_post_question_no_token():
    response = app.test_client().post('/questions', json=question)
    res = json.loads(response.data.decode('utf-8'))
    assert type(res) is dict
    assert res['error'] == "Invalid token. Please provide a valid token"
    assert response.status_code == 401

