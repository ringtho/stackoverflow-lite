
from ..init_db import Database

class Question:

    def create_question(self,title,description,stack, author):
        cur = Database().get_cursor()
        query = f"""
        INSERT INTO questions (title, description, stack, author) 
        VALUES ('{title}','{description}','{stack}', '{author}')
        """
        question = cur.execute(query)
        return question


    def get_questions(self):
        cur = Database().get_cursor()
        query = """
        SELECT * FROM questions
        """
        cur.execute(query)
        questions = cur.fetchall()
        return questions

    def get_question_by_id(self, id):
        cur = Database().get_cursor()
        query = f"""
        SELECT * FROM questions WHERE id='{id}'
        """
        cur.execute(query)
        question = cur.fetchone()
        if question:
            return question  

    def update_question(self,id,author,title,description,stack):
        cur = Database().get_cursor()
        query = f"""
        UPDATE questions SET title='{title}', description='{description}', 
        stack='{stack}' WHERE author='{author}' AND id='{id}'
        """
        cur.execute(query)
        rows = cur.rowcount
        return rows

    def delete_question_by_id(self, id, author):
        cur = Database().get_cursor()
        query = f"""
        DELETE FROM questions WHERE id='{id}' AND author='{author}'
        """
        cur.execute(query)
        rows = cur.rowcount
        return rows

    def get_questions_by_author(self, author):
        cur = Database().get_cursor()
        query = f"""
        SELECT * FROM questions WHERE author='{author}'
        """
        cur.execute(query)
        question = cur.fetchall()
        return question

    def get_question_id(self):
        cursor = Database().get_cursor()
        query = "SELECT id FROM questions ORDER BY id DESC"
        cursor.execute(query)
        question_id = cursor.fetchone()["id"]
        return question_id
