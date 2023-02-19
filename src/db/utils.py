from .db_context import DBConn as db


def register_user(telegram_id, full_name):
    with db() as db_ctx:
        db_ctx.execute(
            'INSERT INTO users (id, full_name) '
            f'VALUES(\'{telegram_id}\', \'{full_name}\') '
            f'ON CONFLICT (id) DO UPDATE SET full_name = EXCLUDED.full_name;')


def set_offer(loc_destination, loc_source, cost):
    with db() as db_ctx:
        db_ctx.execute(
            'INSERT INTO offers (loc_destination, loc_source, cost) '
            f'VALUES (\'{loc_destination}\', \'{loc_source}\', \'{cost}\');')


def get_offers():
    with db() as db_ctx:
        db_ctx.execute(
            'SELECT loc_destination, loc_source, cost FROM offers;')
        return db_ctx.fetchall()
