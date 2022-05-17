
import pytest
import json
from stackoverflow.routes import app
from stackoverflow.init_db import Database
from tests.get_token import GetTokenTests

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

    def get_user_token(self):
        access_token = GetTokenTests().get_user_post()
        token = "Bearer " + access_token
        return token

    def get_question_id(self):
        token = self.get_user_token()
        question = self.test_client.post('/questions', json=self.question, 
        headers=dict(Authorization=token))
        data = json.loads(question.data.decode('utf-8'))
        question_id = data['data']['id']
        return question_id

    def test_get_questions_empty_db(self):
        response = self.test_client.get('/questions')
        res = json.loads(response.data.decode('utf-8'))
        assert type(res) is dict
        assert 'error' in res
        assert res['error']=="No questions currently in the database"
        assert response.status_code == 404

    def test_get_question_empty_db(self):
        question_id = 1
        response = self.test_client.get(f'/questions/{question_id}')
        res = json.loads(response.data.decode('utf-8'))
        assert type(res) is dict
        assert 'error' in res
        assert res['error']=="Question not found"
        assert response.status_code == 404

    def test_post_question(self):
        token = self.get_user_token()
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
        assert type(res) is list
        assert res[0]['author'] == 'user'
        assert type(res[0]) is dict
        assert response.status_code == 200

    def test_get_single_question(self):
        question_id = self.get_question_id()
        response = self.test_client.get(f'/questions/{question_id}')
        res = json.loads(response.data.decode('utf-8'))
        assert type(res['answers']) is list
        assert type(res) is dict
        assert res['question']['title'] == "Autocommit in psycopg2"
        assert response.status_code == 200

    def test_get_single_question_missing(self):
        question_id = 11011
        response = self.test_client.get(f'/questions/{question_id}')
        res = json.loads(response.data.decode('utf-8'))
        assert type(res) is dict
        assert 'error' in res
        assert res['error'] == "Question not found"
        assert response.status_code == 404

    def test_delete_question(self):
        question_id = self.get_question_id()
        token = self.get_user_token()
        response = self.test_client.delete(f'/questions/{question_id}',
        headers=dict(Authorization=token))
        res = json.loads(response.data.decode('utf-8'))
        assert type(res) is dict
        assert 'success' in res
        assert res['success']=="Question successfully deleted"
        assert response.status_code == 200

    def test_delete_question_missing_question(self):
        question_id = 11101
        token = self.get_user_token()
        response = self.test_client.delete(f'/questions/{question_id}',
        headers=dict(Authorization=token))
        res = json.loads(response.data.decode('utf-8'))
        assert type(res) is dict
        assert 'error' in res
        assert res['error']=="Question not found"
        assert response.status_code == 404

    def test_update_question(self):
        question_id = self.get_question_id()
        token = self.get_user_token()
        response = self.test_client.put(f'/questions/{question_id}', 
        json=self.question, headers=dict(Authorization=token))
        res = json.loads(response.data.decode('utf-8'))
        assert type(res) is dict
        assert 'success' in res
        assert res['success']=="Question successfully updated"
        assert response.status_code == 200

    def test_update_question_missing_question(self):
        question_id = 11101
        token = self.get_user_token()
        response = self.test_client.put(f'/questions/{question_id}', 
        json=self.question, headers=dict(Authorization=token))
        res = json.loads(response.data.decode('utf-8'))
        assert type(res) is dict
        assert 'error' in res
        assert res['error']=="Question not found"
        assert response.status_code == 404

    def test_update_question_missing_token(self):
        question_id = self.get_question_id()
        token = ""
        response = self.test_client.put(f'/questions/{question_id}', 
        json=self.question, headers=dict(Authorization=token))
        res = json.loads(response.data.decode('utf-8'))
        assert type(res) is dict
        assert 'error' in res
        assert "Invalid token" in res['error']
        assert response.status_code == 401

    def test_get_current_users_questions(self):
        self.test_post_question()
        self.test_post_question()
        token = self.get_user_token()
        username = "user"
        response = self.test_client.get(f'/questions/{username}',
        headers=dict(Authorization=token))
        res = json.loads(response.data.decode('utf-8'))
        assert type(res) is dict
        assert 'questions' in res
        assert 'title' in res['questions'][0]
        assert res['questions'][0]['author']=="user"
        assert response.status_code == 200

    def test_get_current_users_questions_no_questions(self):
        token = self.get_user_token()
        username = "user"
        response = self.test_client.get(f'/questions/{username}',
        headers=dict(Authorization=token))
        res = json.loads(response.data.decode('utf-8'))
        assert type(res) is dict
        assert 'error' in res
        assert res['error']=="Questions not found"
        assert response.status_code == 404

    def test_get_current_users_questions_unauthorized(self):
        token = self.get_user_token()
        token = self.get_user_token()
        username = "sringtho"
        response = self.test_client.get(f'/questions/{username}',
        headers=dict(Authorization=token))
        res = json.loads(response.data.decode('utf-8'))
        assert type(res) is dict
        assert 'error' in res
        assert res['error']=="You are not authorised"
        assert response.status_code == 401


        









