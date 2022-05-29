from stackoverflow.init_db import Database

class Comment:

    def create_comment(self,answer_id,comment,author):
        cur = Database().get_cursor()
        query = f"""
        INSERT INTO comments (answer_id, comment, author) 
        VALUES ('{answer_id}','{comment}','{author}')
        """
        comment = cur.execute(query)
        return comment

    def get_comments_by_answer_id(self,answer_id):
        cur = Database().get_cursor()
        query = f"""
        SELECT * FROM comments WHERE answer_id='{answer_id}'
        """
        cur.execute(query)
        comments = cur.fetchall()
        return comments

    def get_single_comment_by_id(self, comment_id):
        cur = Database().get_cursor()
        query = f"""
        SELECT * FROM comments WHERE id='{comment_id}'
        """
        cur.execute(query)
        comment = cur.fetchone()
        return comment
    
    def delete_comment(self, comment_id, author):
        cur = Database().get_cursor()
        query = f"""
        DELETE FROM comments WHERE id='{comment_id}'
        AND author='{author}'
        """
        cur.execute(query)
        rows = cur.rowcount
        return rows

    def update_comment(self,comment_id,comment,author):
        cur = Database().get_cursor()
        query = f"""
        UPDATE comments SET comment='{comment}' WHERE id='{comment_id}'
        AND author='{author}'
        """
        cur.execute(query)
        rows = cur.rowcount
        return rows

    def get_comment_id(self):
        cursor = Database().get_cursor()
        query = "SELECT id FROM comments ORDER BY id DESC"
        cursor.execute(query)
        comment_id = cursor.fetchone()["id"]
        return comment_id