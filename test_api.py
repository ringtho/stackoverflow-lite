import pytest
import json
from app import app

{
    "id": 1,
    "question": "Log in to use Flask",
    "description": "I would like to use Flask for authentication purpose",
    "stack":"Python, HTML, CSS",
    "answers": []
}


def test_index_route():
    response = app.test_client().get('/')
    res = json.loads(response.data.decode('utf-8')).get('hello')

    assert response.status_code == 200
    assert res == "Hello World"
    assert type(res) is str

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

