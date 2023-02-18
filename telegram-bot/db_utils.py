from db_context import DBConn as db


def register_user(telegram_id):
    with db as db_ctx:
        db_ctx.execute(
            "INSERT INTO users (id) VALUES(%s)", (telegram_id,))
