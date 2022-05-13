from ..init_db import get_db_connection
from psycopg2.extras import RealDictCursor

class Question:

    def get_questions(self):
        conn = get_db_connection()
        cur = conn.cursor()
        query = """
        SELECT * FROM questions
        """
        cur.execute(query)
        questions = cur.fetchmany()
        cur.close()
        conn.close()
        return questions

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