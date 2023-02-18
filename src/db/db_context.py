import psycopg2 as db
import os

DSN = os.environ['DATABASE_DSN']


class DBConn:
    def __init__(self):
        self.connection = db.connect(DSN)

    def __enter__(self):
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.commit()
        self.connection.close()
