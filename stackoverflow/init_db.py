import psycopg2
import os


conn = psycopg2.connect(
    host="localhost",
    database="stackoverflow",
    user=os.environ['DB_USERNAME'],
    password=os.environ['DB_PASSWORD']
)

cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS books;')
cur.execute('CREATE TABLE books (id serial PRIMARY KEY,'
                                 'title varchar (150) NOT NULL,'
                                 'author varchar (50) NOT NULL,'
                                 'pages_num integer NOT NULL,'
                                 'review text,'
                                 'date_added date DEFAULT CURRENT_TIMESTAMP);'
                                 )
cur.execute('CREATE TABLE IF NOT EXISTS users (id serial PRIMARY KEY,'
                                'username varchar (150) NOT NULL,'
                                'email varchar (150) NOT NULL,'
                                'firstname varchar (150) NOT NULL,'
                                'lastname varchar(150) NOT NULL,'
                                'gender varchar (150),'
                                'password varchar (150) NOT NULL,'
                                'created_on timestamp DEFAULT CURRENT_TIMESTAMP);'
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