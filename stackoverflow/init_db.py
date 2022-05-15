import psycopg2
from psycopg2.extras import RealDictCursor
import os


class Database:

    def __init__(self):
        try:
            if os.getenv("STATE")=="Testing":
                dbname = "stackoverflowtest"
            else:
                dbname = "stackoverflow"
            self.conn = psycopg2.connect(
                host="localhost",
                database=dbname,
                user=os.environ['DB_USERNAME'],
                password=os.environ['DB_PASSWORD'])
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            # self.cur = self.conn.cursor()
            self.conn.autocommit = True
            self.create_users_table()
            self.create_questions_table()
            self.create_answers_table()
            self.create_comments_table()          
            print(f"connected to database '{dbname}'...")
        except (Exception, psycopg2.OperationalError) as e:
            print(e)

    def create_users_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS users 
        (id serial PRIMARY KEY,
        username varchar (150) UNIQUE NOT NULL,
        email varchar (150) UNIQUE NOT NULL,
        firstname varchar (150) NOT NULL,
        lastname varchar(150) NOT NULL,
        gender varchar (150),
        password varchar (150) NOT NULL,
        created_on timestamp DEFAULT CURRENT_TIMESTAMP);
        """
        self.cursor.execute(query)

    def create_questions_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS questions 
        (id serial PRIMARY KEY,
        title varchar (150) NOT NULL,
        description text,
        stack varchar (150) NOT NULL,
        author varchar(150) NOT NULL,
        created_on timestamp DEFAULT NOW(),
        FOREIGN KEY (author) REFERENCES users (username)
        ON DELETE CASCADE);
        """ 
        self.cursor.execute(query)

    def create_answers_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS answers 
        (id serial PRIMARY KEY,
        question_id INTEGER NOT NULL,
        answer text,
        preferred boolean NOT NULL,
        author varchar(150) NOT NULL,
        created_on timestamp DEFAULT NOW(),
        FOREIGN KEY (question_id) REFERENCES questions (id)
        ON DELETE CASCADE);
        """
        self.cursor.execute(query)

    def create_comments_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS comments 
        (id serial PRIMARY KEY,
        answer_id INTEGER NOT NULL,
        comment text,
        author varchar(150) NOT NULL,
        created_on timestamp DEFAULT NOW(),
        FOREIGN KEY (answer_id) REFERENCES answers (id)
        ON DELETE CASCADE);
        """
        self.cursor.execute(query)

    def get_db_connection(self):
        conn = psycopg2.connect(
            host="localhost",
            database="stackoverflow",
            user=os.environ['DB_USERNAME'],
            password=os.environ['DB_PASSWORD']
        )
        return conn

    def empty_tables(self):
        self.cursor.execute("TRUNCATE TABLE users CASCADE")
        self.cursor.execute("TRUNCATE TABLE questions CASCADE")
        self.cursor.execute("TRUNCATE TABLE answers CASCADE")
        self.cursor.execute("TRUNCATE TABLE comments CASCADE")

    def get_cursor(self):
        return self.cursor

if __name__ == '__main__':
    db = Database()

# cur.execute('CREATE TABLE IF NOT EXISTS users (id serial PRIMARY KEY,'
#                                 'username varchar (150) UNIQUE NOT NULL,'
#                                 'email varchar (150) UNIQUE NOT NULL,'
#                                 'firstname varchar (150) NOT NULL,'
#                                 'lastname varchar(150) NOT NULL,'
#                                 'gender varchar (150),'
#                                 'password varchar (150) NOT NULL,'
#                                 'created_on timestamp DEFAULT CURRENT_TIMESTAMP);'
#                                 )
# cur.execute('CREATE TABLE IF NOT EXISTS questions (id serial PRIMARY KEY,'
#                                 'title varchar (150) NOT NULL,'
#                                 'description text,'
#                                 'stack varchar (150) NOT NULL,'
#                                 'author varchar(150) NOT NULL,'
#                                 'created_on timestamp DEFAULT NOW(),'
#                                 'FOREIGN KEY (author) REFERENCES users (username)'
#                                 'ON DELETE CASCADE);'
#                                 )
# cur.execute('CREATE TABLE IF NOT EXISTS answers (id serial PRIMARY KEY,'
#                                 'question_id INTEGER NOT NULL,'
#                                 'answer text,'
#                                 'preferred boolean NOT NULL,'
#                                 'author varchar(150) NOT NULL,'
#                                 'created_on timestamp DEFAULT NOW(),'
#                                 'FOREIGN KEY (question_id) REFERENCES questions (id)'
#                                 'ON DELETE CASCADE);'
#                                 )
# cur.execute('CREATE TABLE IF NOT EXISTS comments (id serial PRIMARY KEY,'
#                                 'answer_id INTEGER NOT NULL,'
#                                 'comment text,'
#                                 'author varchar(150) NOT NULL,'
#                                 'created_on timestamp DEFAULT NOW(),'
#                                 'FOREIGN KEY (answer_id) REFERENCES answers (id)'
#                                 'ON DELETE CASCADE);'
#                                 )

# conn = psycopg2.connect(
#     host="localhost",
#     database="stackoverflow",
#     user=os.environ['DB_USERNAME'],
#     password=os.environ['DB_PASSWORD']
# )

# cur = conn.cursor()

# conn.commit()

# cur.close()
# conn.close()


        