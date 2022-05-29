from flask import jsonify
import pytest
import json
from stackoverflow.routes import app
from stackoverflow.init_db import Database
from .get_token import GetTokenTests


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
        cls.comment = {
            "comment":"Lorem Ipsum is simply dummy text of the printing and"
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

    def get_comment_id(self):
        answer = self.get_answer_id()
        question_id = answer['question']
        answer_id = answer['id']
        token = self.get_user_token()
        response = self.test_client.post(
            f'/questions/{question_id}/answers/{answer_id}/comments',
        json=self.comment, headers=dict(Authorization=token))
        res = json.loads(response.data.decode('utf-8'))
        comment_id = res['comment'][0]['id']
        return comment_id


    def test_create_comment(self):
        answer = self.get_answer_id()
        answer_id = answer['id']
        question_id = answer['question']
        token = self.get_user_token()
        response = self.test_client.post(
            f'/questions/{question_id}/answers/{answer_id}/comments',
        json=self.comment, headers=dict(Authorization=token))
        res = json.loads(response.data.decode('utf-8'))
        assert response.content_type == 'application/json'
        assert 'answer' in res
        assert 'comment' in res
        assert res['comment'][0]['author'] == "user"
        assert response.status_code == 201

    def test_create_comment_missing_question(self):
        answer = self.get_answer_id()
        answer_id = answer['id']
        question_id = 111001
        token = self.get_user_token()
        response = self.test_client.post(
            f'/questions/{question_id}/answers/{answer_id}/comments',
        json=self.comment, headers=dict(Authorization=token))
        res = json.loads(response.data.decode('utf-8'))
        assert response.content_type == 'application/json'
        assert 'error' in res
        assert res['error'] == "Question not found"
        assert response.status_code == 404

    def test_create_comment_missing_answer(self):
        answer = self.get_answer_id()
        answer_id = 111001
        question_id = answer['question']
        token = self.get_user_token()
        response = self.test_client.post(
            f'/questions/{question_id}/answers/{answer_id}/comments',
        json=self.comment, headers=dict(Authorization=token))
        res = json.loads(response.data.decode('utf-8'))
        assert response.content_type == 'application/json'
        assert 'error' in res
        assert res['error'] == "Answer not found"
        assert response.status_code == 404

    def test_get_comment(self):
        answer = self.get_answer_id()
        answer_id = answer['id']
        question_id = answer['question']
        comment_id = self.get_comment_id()
        token = self.get_user_token()
        response = self.test_client.get(
            f'/questions/{question_id}/answers/{answer_id}/comments/{comment_id}',
        headers=dict(Authorization=token))
        res = json.loads(response.data.decode('utf-8'))
        assert response.content_type == 'application/json'
        assert 'answer' in res
        assert 'comment' in res
        assert res['comment']['id'] == comment_id
        assert response.status_code == 200

    def test_get_comment_missing_answer(self):
        answer = self.get_answer_id()
        answer_id = 11101
        question_id = answer['question']
        comment_id = self.get_comment_id()
        token = self.get_user_token()
        response = self.test_client.get(
            f'/questions/{question_id}/answers/{answer_id}/comments/{comment_id}',
        headers=dict(Authorization=token))
        res = json.loads(response.data.decode('utf-8'))
        assert response.content_type == 'application/json'
        assert 'error' in res
        assert res['error'] == "Answer not found"
        assert response.status_code == 404

    def test_get_comment_missing_question(self):
        answer = self.get_answer_id()
        answer_id = answer['id']
        question_id = 11101
        comment_id = self.get_comment_id()
        token = self.get_user_token()
        response = self.test_client.get(
            f'/questions/{question_id}/answers/{answer_id}/comments/{comment_id}',
        headers=dict(Authorization=token))
        res = json.loads(response.data.decode('utf-8'))
        assert response.content_type == 'application/json'
        assert 'error' in res
        assert res['error'] == "Question not found"
        assert response.status_code == 404

    def test_delete_comment(self):
        answer = self.get_answer_id()
        answer_id = answer['id']
        question_id = answer['question']
        comment_id = self.get_comment_id()
        token = self.get_user_token()
        response = self.test_client.delete(
            f'/questions/{question_id}/answers/{answer_id}/comments/{comment_id}',
        headers=dict(Authorization=token))
        res = json.loads(response.data.decode('utf-8'))
        assert response.content_type == 'application/json'
        assert 'success' in res
        assert res['success'] == "Comment successfully deleted"
        assert response.status_code == 200

    def test_delete_comment_missing_question(self):
        answer = self.get_answer_id()
        answer_id = answer['id']
        question_id = 11011
        comment_id = self.get_comment_id()
        token = self.get_user_token()
        response = self.test_client.delete(
            f'/questions/{question_id}/answers/{answer_id}/comments/{comment_id}',
        headers=dict(Authorization=token))
        res = json.loads(response.data.decode('utf-8'))
        assert response.content_type == 'application/json'
        assert 'error' in res
        assert res['error'] == "Question not found"
        assert response.status_code == 404

    def test_delete_comment_missing_answer(self):
        answer = self.get_answer_id()
        answer_id = 11101
        question_id = answer['question']
        comment_id = self.get_comment_id()
        token = self.get_user_token()
        response = self.test_client.delete(
            f'/questions/{question_id}/answers/{answer_id}/comments/{comment_id}',
        headers=dict(Authorization=token))
        res = json.loads(response.data.decode('utf-8'))
        assert response.content_type == 'application/json'
        assert 'error' in res
        assert res['error'] == "Answer not found"
        assert response.status_code == 404

    def test_delete_comment_missing_comment(self):
        answer = self.get_answer_id()
        answer_id = answer['id']
        question_id = answer['question']
        comment_id = 11001
        token = self.get_user_token()
        response = self.test_client.delete(
            f'/questions/{question_id}/answers/{answer_id}/comments/{comment_id}',
        headers=dict(Authorization=token))
        res = json.loads(response.data.decode('utf-8'))
        assert response.content_type == 'application/json'
        assert 'error' in res
        assert res['error'] == "Comment not found"
        assert response.status_code == 404

    def test_edit_comment(self):
        answer = self.get_answer_id()
        answer_id = answer['id']
        question_id = answer['question']
        comment_id = self.get_comment_id()
        token = self.get_user_token()
        response = self.test_client.put(
            f'/questions/{question_id}/answers/{answer_id}/comments/{comment_id}',
        headers=dict(Authorization=token),json=self.comment)
        res = json.loads(response.data.decode('utf-8'))
        assert response.content_type == 'application/json'
        assert 'success' in res
        assert res['success'] == "Comment successfully updated"
        assert response.status_code == 200

    def test_edit_comment_missing_question(self):
        answer = self.get_answer_id()
        answer_id = answer['id']
        question_id = 11101
        comment_id = self.get_comment_id()
        token = self.get_user_token()
        response = self.test_client.put(
            f'/questions/{question_id}/answers/{answer_id}/comments/{comment_id}',
        headers=dict(Authorization=token),json=self.comment)
        res = json.loads(response.data.decode('utf-8'))
        assert response.content_type == 'application/json'
        assert 'error' in res
        assert res['error'] == "Question not found"
        assert response.status_code == 404

    def test_edit_comment_missing_answer(self):
        answer = self.get_answer_id()
        answer_id = 110101
        question_id = answer['question']
        comment_id = self.get_comment_id()
        token = self.get_user_token()
        response = self.test_client.put(
            f'/questions/{question_id}/answers/{answer_id}/comments/{comment_id}',
        headers=dict(Authorization=token),json=self.comment)
        res = json.loads(response.data.decode('utf-8'))
        assert response.content_type == 'application/json'
        assert 'error' in res
        assert res['error'] == "Answer not found"
        assert response.status_code == 404

    def test_edit_comment_missing_comment(self):
        answer = self.get_answer_id()
        answer_id = answer['id']
        question_id = answer['question']
        comment_id = 11011
        token = self.get_user_token()
        response = self.test_client.put(
            f'/questions/{question_id}/answers/{answer_id}/comments/{comment_id}',
        headers=dict(Authorization=token),json=self.comment)
        res = json.loads(response.data.decode('utf-8'))
        assert response.content_type == 'application/json'
        assert 'error' in res
        assert res['error'] == "Comment not found"
        assert response.status_code == 404

    