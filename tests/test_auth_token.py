
import pytest
import json
from stackoverflow.routes import app
from stackoverflow.init_db import Database




class TestAuthToken():
    @classmethod
    def setup(cls):
        """initialise test client"""
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

    def test_post_question_no_token(self):
        response = self.test_client.post('/questions', json=self.question)
        res = json.loads(response.data.decode('utf-8'))
        assert type(res) is dict
        assert res['error'] == "Invalid token. Please provide a valid token"
        assert response.status_code == 401

    # def test_post_question_expired_token(self):
    #     token = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOjEsInVubSI6InNyaW5ndGhvIiwiZXhwIjoxNjUyNjA4MTg0fQ.Sp8Ir4HPVOlRnZ0pj0C7LxbXpebwgVi-uD6QBknNQpg"
    #     response = self.test_client.post('/questions', json=self.question, 
    #     headers=dict(Authorization=token))
    #     res = json.loads(response.data.decode('utf-8'))
    #     assert type(res) is dict
    #     assert res['error'] == "Token has expired!!"
    #     assert response.status_code == 401

    def test_post_question_invalid_token(self):
        token = "I6InNyaW5ndGhvIiwiZXhw"
        response = self.test_client.post('/questions', json=self.question, 
        headers=dict(Authorization=token))
        res = json.loads(response.data.decode('utf-8'))
        assert type(res) is dict
        assert res['error'] == "Invalid token. Please provide a valid token"
        assert response.status_code == 401