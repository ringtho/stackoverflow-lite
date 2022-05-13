from ..resources.auth_token import get_id_token
from ..init_db import get_db_connection
from psycopg2.extras import RealDictCursor
class User:
    def __init__(self, _id, username, email, fullname, sex, password):
        self.id = _id
        self.username = username
        self.email = email
        self.fullname = fullname
        self.sex = sex
        self.password = password

def get_current_user():
    user_id = get_id_token()
    user = next(filter(lambda x: x['id'] == user_id, users), None)
    return user


users = [
    {
        "id":1,
        "username": "sringtho",
        "email": "sringtho@gmail.com",
        "fullname": "Smith Ringtho",
        "sex":"male",
        "password": "pbkdf2:sha256:260000$fll4DQpR3KpmIWtK$5f018cfc314f1ba804e72d93901c20375a5fc7661c922591c7ee53cf3f934321"
    }
    
]

