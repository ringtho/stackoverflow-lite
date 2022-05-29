import pytest
import json
from stackoverflow.routes import app
from stackoverflow.init_db import Database
from tests.get_token import GetTokenTests

class TestUsers():
    @classmethod
    def setup(cls):
        cls.test_client = app.test_client()
        cls.db = Database()
        cls.user = {
            "username":"user",
            "email":"usergmail",
            "firstname": "Smith",
            "lastname": "Ringtho",
            "gender": "male",
            "password": "Sr654321"
        }
        cls.user1 = {
            "username":"user",
            "email": 123,
            "firstname": "Smith",
            "lastname": "Ringtho",
            "gender": "male",
            "password": "Sr654321"
        }
        cls.user_password = {
            "username":"user",
            "email": "sringtho@gmail.com",
            "firstname": "Smith",
            "lastname": "Ringtho",
            "gender": "male",
            "password": 123
        }
        cls.user_password1 = {
            "username":"user",
            "email": "sringtho@gmail.com",
            "firstname": "Smith",
            "lastname": "Ringtho",
            "gender": "male",
            "password": "SR1234"
        }
        cls.login = {
            "username": "user",
            "password": "Sr654321"
        }
        cls.login_2 = {
            "username": "sringtho",
            "password": "Sr654321"
        }
        cls.password = {
            "old_password": "Sr654321",
            "new_password": "Sr654322"
        }
        cls.password_same = {
            "old_password": "Sr654321",
            "new_password": "Sr654321"
        }
        cls.password_old_incorrect = {
            "old_password": "Sr654322",
            "new_password": "Sr654321"
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

    def test_create_user_invalid_email(self):
        response = self.test_client.post("/auth/signup",json=self.user)
        data = json.loads(response.data.decode('utf-8'))
        assert type(data) is dict
        assert 'error' in data
        assert data['error'] == "Invalid Email Address!"
        assert response.status_code == 400

    def test_create_user_invalid_email_string(self):
        response = self.test_client.post("/auth/signup",json=self.user1)
        data = json.loads(response.data.decode('utf-8'))
        assert type(data) is dict
        assert 'error' in data
        assert data['error'] == "Email address must be a string!"
        assert response.status_code == 400

    def test_create_user_invalid_password_string(self):
        response = self.test_client.post("/auth/signup",json=self.user_password)
        data = json.loads(response.data.decode('utf-8'))
        assert type(data) is dict
        assert 'error' in data
        assert data['error'] == "Password should be a string"
        assert response.status_code == 400

    def test_create_user_password_validate(self):
        response = self.test_client.post("/auth/signup",json=self.user_password1)
        data = json.loads(response.data.decode('utf-8'))
        assert type(data) is dict
        assert 'error' in data
        assert 'Password must contain atleast one lowercase letter' in data['error']
        assert response.status_code == 400