import asyncpg
import asyncpg as db
from psycopg2.extras import RealDictCursor
import os

DSN = os.environ['DATABASE_DSN']


async def create_db():
    conn = DBConn()
    conn.connection = await asyncpg.connect(DSN)
    return conn


class DBConn:
    def __init__(self):
        self.connection = None

    def __enter__(self):
        return self.connection

    # def __exit__(self, exc_type, exc_value, traceback):
    #     self.connection.commit()
    #     self.connection.close()
