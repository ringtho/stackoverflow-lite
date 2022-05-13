from ..init_db import get_db_connection
from psycopg2.extras import RealDictCursor

class Question:

    def create_question(self,title,description,stack, author):
        conn = get_db_connection()
        cur = conn.cursor()
        query = f"""
        INSERT INTO questions (title, description, stack, author) 
        VALUES ('{title}','{description}','{stack}', '{author}')
        """
        question = cur.execute(query)
        conn.commit()
        cur.close()
        conn.close()
        return question


    def get_questions(self):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query = """
        SELECT * FROM questions
        """
        cur.execute(query)
        questions = cur.fetchall()
        cur.close()
        conn.close()
        return questions

    def get_question_by_id(self, id):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query = f"""
        SELECT * FROM questions WHERE id='{id}'
        """
        cur.execute(query)
        question = cur.fetchone()
        cur.close()
        conn.close()
        if question:
            return question  

    def update_question(self,id,author,title,description,stack):
        conn = get_db_connection()
        cur = conn.cursor()
        query = f"""
        UPDATE questions SET title='{title}', description='{description}', 
        stack='{stack}' WHERE author='{author}' AND id='{id}'
        """
        cur.execute(query)
        rows = cur.rowcount
        conn.commit()
        cur.close()
        conn.close()
        return rows

    def delete_question_by_id(self, id, author):
        conn = get_db_connection()
        cur = conn.cursor()
        query = f"""
        DELETE FROM questions WHERE id='{id}' AND author='{author}'
        """
        cur.execute(query)
        rows = cur.rowcount
        conn.commit()
        cur.close()
        conn.close()
        return rows

    def get_questions_by_author(self, id, author):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query = f"""
        SELECT * FROM questions WHERE author='{author}'
        """
        cur.execute(query)
        question = cur.fetchall()
        cur.close()
        conn.close()
        return question
