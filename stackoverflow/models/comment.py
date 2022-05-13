from ..init_db import get_db_connection
from psycopg2.extras import RealDictCursor

class Comment:

    def create_comment(self,answer_id,comment,author):
        conn = get_db_connection()
        cur = conn.cursor()
        query = f"""
        INSERT INTO comments (answer_id, comment, author) 
        VALUES ('{answer_id}','{comment}','{author}')
        """
        comment = cur.execute(query)
        conn.commit()
        cur.close()
        conn.close()
        return comment