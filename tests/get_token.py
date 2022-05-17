from stackoverflow.routes import app
from flask import json

class GetTokenTests:

    def get_user_post(self):
        user_details = {
            "username":"user",
            "email":"user@gmail.com",
            "firstname": "Smith",
            "lastname": "Ringtho",
            "gender": "male",
            "password":"Sr654321"
        }
    
        response = app.test_client().post('/auth/signup', json=user_details)

        user = {

                "username": "user",
                "password": "Sr654321"

            }

        response = app.test_client().post('/auth/login', json=user)
        token = json.loads(response.data.decode('utf-8'))['access_token']
        return token

    def get_second_user_post(self):
        user_details = {
            "username":"sringtho",
            "email":"sringtho@gmail.com",
            "firstname": "Smith",
            "lastname": "Ringtho",
            "gender": "male",
            "password":"Sr654321"
        }
    
        response = app.test_client().post('/auth/signup', json=user_details)

        user = {

                "username": "sringtho",
                "password": "Sr654321"

            }

        response = app.test_client().post('/auth/login', json=user)
        token = json.loads(response.data.decode('utf-8'))['access_token']
        return token


        
     
        
        

    