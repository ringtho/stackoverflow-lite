from werkzeug.security import check_password_hash
from ..resources.auth_token import get_username_from_token
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

    def get_user_auth_details(self, username, password):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query =f"""
        SELECT * FROM users WHERE username='{username}'
        """
        cur.execute(query)
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user and check_password_hash(user['password'], password):
            return user

    def get_user(self, username):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query=f"""
        SELECT username,email,firstname,lastname,gender FROM users WHERE username='{username}'
        """
        cur.execute(query)
        user = cur.fetchone()
        cur.close()
        conn.close()
        return user

    def update_user_password(self, username, password):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query=f"""
        UPDATE users SET password='{password}' WHERE username='{username}'
        """
        cur.execute(query)
        rows = cur.rowcount
        conn.commit()
        cur.close()
        conn.close()
        return rows


    def get_current_user_from_token(self):
        username = get_username_from_token()
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query=f"""
        SELECT username FROM users WHERE username='{username}'
        """
        cur.execute(query)
        user = cur.fetchone()
        cur.close()
        conn.close()
        return user


