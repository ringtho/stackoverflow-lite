
from stackoverflow.init_db import Database

class Answer:

    def create_answer(self,question_id,answer,preferred,author):
        cur = Database().get_cursor()
        query = f"""
        INSERT INTO answers (question_id, answer, preferred, author) 
        VALUES ('{question_id}','{answer}','{preferred}','{author}')
        """
        answer = cur.execute(query)
        return answer
    
    def get_answers_for_question(self, question_id):
        cur = Database().get_cursor()
        query = f"""
        SELECT * FROM answers WHERE question_id='{question_id}'
        """
        cur.execute(query)
        answers = cur.fetchall()
        return answers

    def get_answer_by_answer_id(self, question_id, answer_id):
        cur = Database().get_cursor()
        query = f"""
        SELECT * FROM answers WHERE question_id='{question_id}'
        AND id='{answer_id}'
        """
        cur.execute(query)
        answer = cur.fetchone()
        return answer

    def get_answers_with_true_preferred(self, question_id):
        cur = Database().get_cursor()
        preferred = True
        query = f"""
        SELECT * FROM answers WHERE question_id='{question_id}'
        AND preferred='{preferred}'
        """
        cur.execute(query)
        answer = cur.fetchone()
        return answer


    def update_answer_preferred_option(self,question_id,answer_id,preferred):
        cur = Database().get_cursor()
        query = f"""
        UPDATE answers SET preferred='{preferred}' WHERE id='{answer_id}'
        AND question_id='{question_id}'
        """
        cur.execute(query)
        rows = cur.rowcount
        return rows

    def delete_answer_by_id(self, answer_id, author):
        cur = Database().get_cursor()
        query = f"""
        DELETE FROM answers WHERE id='{answer_id}' AND author='{author}'
        """
        cur.execute(query)
        rows = cur.rowcount
        return rows

    def get_answer_id(self):
        cursor = Database().get_cursor()
        query = "SELECT id FROM answers ORDER BY id DESC"
        cursor.execute(query)
        answer_id = cursor.fetchone()["id"]
        return answer_id