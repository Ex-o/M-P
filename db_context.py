import psycopg2 as db


class DBConn:
    def __init__(self, dsn):
        self.connection = db.connect(dsn)

    def __enter__(self):
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.commit()
        self.connection.close()
