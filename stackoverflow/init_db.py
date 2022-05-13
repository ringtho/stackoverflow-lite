import psycopg2
import os


conn = psycopg2.connect(
    host="localhost",
    database="stackoverflow",
    user=os.environ['DB_USERNAME'],
    password=os.environ['DB_PASSWORD']
)

cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS users (id serial PRIMARY KEY,'
                                'username varchar (150) UNIQUE NOT NULL,'
                                'email varchar (150) UNIQUE NOT NULL,'
                                'firstname varchar (150) NOT NULL,'
                                'lastname varchar(150) NOT NULL,'
                                'gender varchar (150),'
                                'password varchar (150) NOT NULL,'
                                'created_on timestamp DEFAULT CURRENT_TIMESTAMP);'
                                )
cur.execute('CREATE TABLE IF NOT EXISTS questions (id serial PRIMARY KEY,'
                                'title varchar (150) NOT NULL,'
                                'description text,'
                                'stack varchar (150) NOT NULL,'
                                'author varchar(150) NOT NULL,'
                                'created_on timestamp DEFAULT NOW(),'
                                'FOREIGN KEY (author) REFERENCES users (username)'
                                'ON DELETE CASCADE);'
                                )
cur.execute('CREATE TABLE IF NOT EXISTS answers (id serial PRIMARY KEY,'
                                'question_id INTEGER NOT NULL,'
                                'answer text,'
                                'preferred boolean NOT NULL,'
                                'author varchar(150) NOT NULL,'
                                'created_on timestamp DEFAULT NOW(),'
                                'FOREIGN KEY (question_id) REFERENCES questions (id)'
                                'ON DELETE CASCADE);'
                                )
cur.execute('CREATE TABLE IF NOT EXISTS comments (id serial PRIMARY KEY,'
                                'answer_id INTEGER NOT NULL,'
                                'comment text,'
                                'author varchar(150) NOT NULL,'
                                'created_on timestamp DEFAULT NOW(),'
                                'FOREIGN KEY (answer_id) REFERENCES answers (id)'
                                'ON DELETE CASCADE);'
                                )

conn.commit()

cur.close()
conn.close()


def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="stackoverflow",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD']
    )
    return conn