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
            "email":"user@gmail.com",
            "firstname": "Smith",
            "lastname": "Ringtho",
            "gender": "male",
            "password": "Sr654321"
        }
        cls.login = {
            "username": "user",
            "password": "Sr654321"
        }
        cls.login_2 = {
            "username": "sringtho",
            "password": "Sr654321"
        }
        

    @classmethod
    def teardown(cls):
        cls.db.empty_tables()
    
    def test_create_user(self):
        response = self.test_client.post("/auth/signup",json=self.user)
        data = json.loads(response.data.decode('utf-8'))
        assert type(data) is dict
        assert 'success' in data
        assert 'user' in data
        assert data['success'] == "User created successfully"
        assert response.status_code == 201

    def test_create_user_exists(self):
        self.test_create_user()
        response = self.test_client.post("/auth/signup",json=self.user)
        data = json.loads(response.data.decode('utf-8'))
        assert type(data) is dict
        assert 'error' in data
        assert data['error'] == "User with username 'user' already exists"
        assert response.status_code == 400

    def test_get_user_profile(self):
        access_token = GetTokenTests().get_user_post()
        token = "Bearer " + access_token
        response = self.test_client.get("/auth/profile/user", 
        headers={"Authorization":token})
        data = json.loads(response.data.decode('utf-8'))
        print(data)
        assert type(data) is dict
        assert 'username' in data
        assert data['username']=="user"
        assert response.status_code == 200

    def test_get_nonexistent_user_profile(self):
        access_token = GetTokenTests().get_user_post()
        token = "Bearer " + access_token
        response = self.test_client.get("/auth/profile/abc", 
        headers={"Authorization":token})
        data = json.loads(response.data.decode('utf-8'))
        print(data)
        assert type(data) is dict
        assert 'error' in data
        assert data['error']=="User not found!"
        assert response.status_code == 404

    def test_success_login(self):
        self.test_create_user()
        response = self.test_client.post("/auth/login",json=self.login)
        data = json.loads(response.data.decode('utf-8'))
        assert type(data) is dict
        assert 'access_token' in data
        assert 'username' in data
        assert data['username'] == "user"
        assert response.status_code == 200

    def test_incorrect_credentials_login(self):
        self.test_create_user()
        response = self.test_client.post("/auth/login",json=self.login_2)
        data = json.loads(response.data.decode('utf-8'))
        assert type(data) is dict
        assert 'error' in data
        assert 'username' not in data
        assert data['error'] == "Invalid username or password"
        assert response.status_code == 404