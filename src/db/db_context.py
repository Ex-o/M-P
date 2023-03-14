import asyncpg
import os

DSN = os.environ['DATABASE_DSN']


async def create_db():
    conn = DBConn()
    conn.connection = await asyncpg.connect(DSN)
    return conn


class DBConn:
    def __init__(self):
        self.connection = None

    async def __aenter__(self):
        return self.connection

    async def __aexit__(self, exc_type, exc_value, traceback):
        # self.connection.commit()
        await self.connection.close()
