
from ..init_db import get_db_connection
from psycopg2.extras import RealDictCursor

class Answer:

    def create_answer(self,question_id,answer,preferred,author):
        conn = get_db_connection()
        cur = conn.cursor()
        query = f"""
        INSERT INTO answers (question_id, answer, preferred, author) 
        VALUES ('{question_id}','{answer}','{preferred}','{author}')
        """
        answer = cur.execute(query)
        conn.commit()
        cur.close()
        conn.close()
        return answer
    
    def get_answers_for_question(self, question_id):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query = f"""
        SELECT * FROM answers WHERE question_id='{question_id}'
        """
        cur.execute(query)
        answers = cur.fetchall()
        cur.close()
        conn.close()
        return answers

    def get_answer_by_answer_id(self, question_id, answer_id):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query = f"""
        SELECT * FROM answers WHERE question_id='{question_id}'
        AND id='{answer_id}'
        """
        cur.execute(query)
        answer = cur.fetchone()
        cur.close()
        conn.close()
        return answer

    def get_answers_with_true_preferred(self, question_id):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        preferred = True
        query = f"""
        SELECT * FROM answers WHERE question_id='{question_id}'
        AND preferred='{preferred}'
        """
        cur.execute(query)
        answer = cur.fetchone()
        cur.close()
        conn.close()
        return answer


    def update_answer_preferred_option(self,question_id,answer_id,preferred):
        conn = get_db_connection()
        cur = conn.cursor()
        query = f"""
        UPDATE answers SET preferred='{preferred}' WHERE id='{answer_id}'
        AND question_id='{question_id}'
        """
        cur.execute(query)
        rows = cur.rowcount
        conn.commit()
        cur.close()
        conn.close()
        return rows

    def delete_answer_by_id(self, answer_id, author):
        conn = get_db_connection()
        cur = conn.cursor()
        query = f"""
        DELETE FROM answers WHERE id='{answer_id}' AND author='{author}'
        """
        cur.execute(query)
        rows = cur.rowcount
        conn.commit()
        cur.close()
        conn.close()
        return rows