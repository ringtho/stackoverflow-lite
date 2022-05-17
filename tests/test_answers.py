from flask import jsonify
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
        cls.preferred = {
            "preferred": True
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

    def get_answer_id(self):
        question_id = self.get_question_id()
        token = self.get_second_user_token()
        response = self.test_client.post(f'/questions/{question_id}/answers',
        json=self.answer, headers=dict(Authorization=token))
        res = json.loads(response.data.decode('utf-8'))
        answer = res['data']
        return answer

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

    def test_post_answer_missing_question(self):
        question_id = 11100
        token = self.get_second_user_token()
        response = self.test_client.post(
            f'/questions/{question_id}/answers',
        json=self.answer, headers=dict(Authorization=token))
        res = json.loads(response.data.decode('utf-8'))
        assert 'error' in res
        assert type(res) is dict
        assert res['error'] == 'Question not found'
        assert response.status_code == 404

    def test_post_answer_user_answering_own_question(self):
        question_id = self.get_question_id()
        token = self.get_user_token()
        response = self.test_client.post(
            f'/questions/{question_id}/answers',
        json=self.answer, headers=dict(Authorization=token))
        res = json.loads(response.data.decode('utf-8'))
        assert 'error' in res
        assert type(res) is dict
        assert res['error'] == 'You are not allowed to answer your own question'
        assert response.status_code == 403


    def test_get_answer(self):
        answer = self.get_answer_id()
        question_id = answer['question']
        answer_id = answer['id']
        token = self.get_user_token()
        response = self.test_client.get(
            f'/questions/{question_id}/answers/{answer_id}',
        headers=dict(Authorization=token))
        res = json.loads(response.data.decode('utf-8'))
        assert type(res) is dict
        assert 'answer' in res
        assert response.status_code == 200

    def test_delete_answer(self):
        answer = self.get_answer_id()
        question_id = answer['question']
        answer_id = answer['id']
        token = self.get_second_user_token()
        response = self.test_client.delete(
            f'/questions/{question_id}/answers/{answer_id}',
        headers=dict(Authorization=token))
        res = json.loads(response.data.decode('utf-8'))
        assert type(res) is dict
        assert 'message' in res
        assert res['message'] == "Answer successfully deleted"
        assert response.status_code == 200

    def test_delete_answer_unauthorized_user(self):
        answer = self.get_answer_id()
        question_id = answer['question']
        answer_id = answer['id']
        token = self.get_user_token()
        response = self.test_client.delete(
            f'/questions/{question_id}/answers/{answer_id}',
        headers=dict(Authorization=token))
        res = json.loads(response.data.decode('utf-8'))
        assert type(res) is dict
        assert 'error' in res
        assert res['error'] == "Answer not found"
        assert response.status_code == 404

    def test_delete_answer_invalid_token(self):
        answer = self.get_answer_id()
        question_id = answer['question']
        answer_id = answer['id']
        response = self.test_client.delete(
            f'/questions/{question_id}/answers/{answer_id}')
        res = json.loads(response.data.decode('utf-8'))
        assert type(res) is dict
        assert 'error' in res
        assert res['error'] == "Invalid token. Please provide a valid token"
        assert response.status_code == 401

    def test_delete_answer_missing_question(self):
        answer = self.get_answer_id()
        question_id = 1000000
        answer_id = answer['id']
        token = self.get_second_user_token()
        response = self.test_client.delete(
            f'/questions/{question_id}/answers/{answer_id}',
        headers=dict(Authorization=token))
        res = json.loads(response.data.decode('utf-8'))
        assert type(res) is dict
        assert 'error' in res
        assert res['error'] == "Question not found"
        assert response.status_code == 404

    def test_update_preferred_answer(self):
        answer = self.get_answer_id()
        question_id = answer['question']
        answer_id = answer['id']
        token = self.get_user_token()
        response = self.test_client.put(
            f'/questions/{question_id}/answers/{answer_id}',
        headers=dict(Authorization=token), json=self.preferred)
        res = json.loads(response.data.decode('utf-8'))
        assert type(res) is dict
        assert 'success' in res
        assert 'answer' in res
        assert res['success'] == "Answer successfully updated"
        assert response.status_code == 200

    def test_update_preferred_answer_unauthorized_user(self):
        answer = self.get_answer_id()
        question_id = answer['question']
        answer_id = answer['id']
        token = self.get_second_user_token()
        response = self.test_client.put(
            f'/questions/{question_id}/answers/{answer_id}',
        headers=dict(Authorization=token), json=self.preferred)
        res = json.loads(response.data.decode('utf-8'))
        assert type(res) is dict
        assert 'error' in res
        assert res['error'] == "You are not authorized"
        assert response.status_code == 401

    def test_update_missing_question(self):
        answer = self.get_answer_id()
        question_id = 11101
        answer_id = answer['id']
        token = self.get_user_token()
        response = self.test_client.put(
            f'/questions/{question_id}/answers/{answer_id}',
        headers=dict(Authorization=token), json=self.preferred)
        res = json.loads(response.data.decode('utf-8'))
        assert type(res) is dict
        assert 'error' in res
        assert res['error'] == "Question not found"
        assert response.status_code == 404

    def test_update_missing_answer(self):
        answer = self.get_answer_id()
        question_id = answer["question"]
        answer_id = 11101
        token = self.get_user_token()
        response = self.test_client.put(
            f'/questions/{question_id}/answers/{answer_id}',
        headers=dict(Authorization=token), json=self.preferred)
        res = json.loads(response.data.decode('utf-8'))
        assert type(res) is dict
        assert 'error' in res
        assert res['error'] == "Answer not found"
        assert response.status_code == 404


