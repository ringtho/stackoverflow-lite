
import pytest
import json
from stackoverflow.routes import app
from stackoverflow.init_db import Database
from .get_token import GetTokenTests

class TestQuestions():
    @classmethod
    def setup(cls):
        cls.test_client = app.test_client()
        cls.db = Database()
        cls.question = {
            "title": "Autocommit in psycopg2",
            "description": "Does Autocommit also close the connection after",
            "stack": "HTML, CSS"
        }

    @classmethod
    def teardown(cls):
        cls.db.empty_tables()

    def test_get_questions_empty_db(self):
        response = self.test_client.get('/questions')
        res = json.loads(response.data.decode('utf-8'))
        assert type(res) is dict
        assert 'error' in res
        assert res['error']=="No questions currently in the database"
        assert response.status_code == 404

    def test_get_question_empty_db(self):
        response = self.test_client.get('/questions/1')
        res = json.loads(response.data.decode('utf-8'))
        assert type(res) is dict
        assert 'error' in res
        assert res['error']=="Question not found"
        assert response.status_code == 404

    def test_post_question(self):
        access_token = GetTokenTests().get_user_post()
        token = "Bearer " + access_token
        response = self.test_client.post('/questions', json=self.question, 
        headers=dict(Authorization=token))
        res = json.loads(response.data.decode('utf-8'))
        assert type(res) is dict
        assert res['data']['title'] == "Autocommit in psycopg2"
        assert res['success'] == "Successfully created a new question"
        assert response.status_code == 201
    
    def test_get_questions(self):
        self.test_post_question()
        response = self.test_client.get('/questions')
        res = json.loads(response.data.decode('utf-8')).get('questions')
        print(res)
        assert type(res) is list
        assert res[0]['author'] == 'user'
        assert type(res[0]) is dict
        assert response.status_code == 200

    def test_get_single_question(self):
        access_token = GetTokenTests().get_user_post()
        token = "Bearer " + access_token
        question = self.test_client.post('/questions', json=self.question, 
        headers=dict(Authorization=token))
        data = json.loads(question.data.decode('utf-8'))
        print(data)
        question_id = data['data']['id']

        response = self.test_client.get(f'/questions/{question_id}')
        res = json.loads(response.data.decode('utf-8'))
        assert type(res['answers']) is list
        assert type(res) is dict
        assert res['question']['title'] == "Autocommit in psycopg2"
        assert response.status_code == 200



