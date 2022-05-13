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

    def get_question(self, id):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query = f"""
        SELECT * FROM questions WHERE id='{id}'
        """
        cur.execute(query)
        question = cur.fetchone()
        cur.close()
        conn.close()
        return question

questions = [
    {
        "id": 1,
        "question": "Log in to use Flask",
        "description": "I would like to use Flask for authentication purpose",
        "stack":"Python, HTML, CSS",
        "answers": [],
        "author": "sringtho"
    }
]