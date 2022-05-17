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
        cls.answer = {
            "answer":"Lorem Ipsum is simply dummy text of the printing and"
        }

    @classmethod
    def teardown(cls):
        cls.db.empty_tables()

    def get_user_token(self):
        access_token = GetTokenTests().get_user_post()
        token = "Bearer " + access_token
        return token

    def get_second_user_token(self):
        access_token = GetTokenTests().get_second_user_post()
        token = "Bearer " + access_token
        return token

    def get_question_id(self):
        token = self.get_user_token()
        question = self.test_client.post('/questions', json=self.question, 
        headers=dict(Authorization=token))
        data = json.loads(question.data.decode('utf-8'))
        question_id = data['data']['id']
        return question_id

    def test_post_answer(self):
        question_id = self.get_question_id()
        token = self.get_second_user_token()
        response = self.test_client.post(f'/questions/{question_id}/answers',
        json=self.answer, headers=dict(Authorization=token))
        res = json.loads(response.data.decode('utf-8'))
        assert 'success' in res
        assert type(res) is dict
        assert 'answer' in res['data']
        assert res['success'] == 'Successfully provided an answer'
        assert 'author' in res['data']
        assert res['data']['preferred'] == False
        assert response.status_code == 201


    def test_get_answer(self):
        question_id = self.get_question_id()
        token = self.get_second_user_token()
        response = self.test_client.post(f'/questions/{question_id}/answers',
        json=self.answer, headers=dict(Authorization=token))
        res = json.loads(response.data.decode('utf-8'))
        answer_id = res['data']['id']
        response = self.test_client.get(f'/questions/{question_id}/answers/{answer_id}',
        headers=dict(Authorization=token))
        res = json.loads(response.data.decode('utf-8'))
        assert type(res) is dict
        assert 'answer' in res
        assert response.status_code == 200