import pytest
import json
from stackoverflow.routes import app
from stackoverflow.init_db import Database
from .get_token import GetTokenTests
from .test_questions import TestQuestions

class TestAnswers():
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

    def test_post_answer(self):
        access_token = GetTokenTests().get_user_post()
        token = "Bearer " + access_token
        question = self.test_client.post('/questions', json=self.question, 
        headers=dict(Authorization=token))
        data = json.loads(question.data.decode('utf-8'))
        question_id = data['data']['id']

        

    def test_get_answer(self):
        access_token = GetTokenTests().get_user_post()
        token = "Bearer " + access_token
        question = self.test_client.post('/questions', json=self.question, 
        headers=dict(Authorization=token))
        data = json.loads(question.data.decode('utf-8'))
        question_id = data['data']['id']

        response = self.test_client.get(f'/questions/{question_id}')
        res = json.loads(response.data.decode('utf-8'))
        assert type(res['answers']) is list
        assert type(res) is dict
        assert res['question']['title'] == "Autocommit in psycopg2"
        assert response.status_code == 200