from werkzeug.security import check_password_hash
from ..resources.auth_token import get_id_token
from ..init_db import get_db_connection
from psycopg2.extras import RealDictCursor
class User:

    def create_user(self,username,email,firstname,lastname,gender,password):
        conn = get_db_connection()
        cur = conn.cursor()
        query =f"""
        INSERT INTO users (username,email,firstname,lastname,gender,password) 
        VALUES ('{username}','{email}','{firstname}','{lastname}','{gender}','{password}')
        """
        user = cur.execute(query)
        conn.commit()
        cur.close()
        conn.close()
        return user

    def login_user(self, username, password):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query =f"""
        SELECT * FROM users WHERE username='{username}'
        """
        cur.execute(query)
        user = cur.fetchone()
        cur.close()
        conn.close()
        if check_password_hash(user['password'], password):
            return user

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

