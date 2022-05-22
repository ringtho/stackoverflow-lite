from werkzeug.security import check_password_hash
from stackoverflow.resources.auth_token import get_username_from_token
from stackoverflow.init_db import Database
class User:

    def create_user(self, user, password):
        cur = Database().get_cursor()
        query =f"""
        INSERT INTO users (username,email,firstname,lastname,gender,password) 
        VALUES ('{user['username']}','{user['email']}','{user['firstname']}',
        '{user['lastname']}','{user['gender']}','{password}')
        """
        user = cur.execute(query)
        return user

    def get_user_auth_details(self, username, password):
        cur = Database().get_cursor()
        query =f"""
        SELECT * FROM users WHERE username='{username}'
        """
        cur.execute(query)
        user = cur.fetchone()
        if user and check_password_hash(user['password'], password):
            return user

    def get_user(self, username):
        cur = Database().get_cursor()
        query=f"""
        SELECT username,email,firstname,lastname,gender 
        FROM users WHERE username='{username}'
        """
        cur.execute(query)
        user = cur.fetchone()
        return user

    def update_user_password(self, username, password):
        cur = Database().get_cursor()
        query=f"""
        UPDATE users SET password='{password}' WHERE username='{username}'
        """
        cur.execute(query)
        rows = cur.rowcount
        return rows


    def get_current_user_from_token(self):
        cur = Database().get_cursor()
        username = get_username_from_token()
        query=f"""
        SELECT username FROM users WHERE username='{username}'
        """
        cur.execute(query)
        user = cur.fetchone()
        return user


