from .db_context import DBConn as db


def register_user(telegram_id, full_name):
    with db() as db_ctx:
        db_ctx.execute(
            'INSERT INTO users (id, full_name) '
            f'VALUES(\'{telegram_id}\', \'{full_name}\') '
            f'ON CONFLICT (id) DO UPDATE SET full_name = EXCLUDED.full_name;')


def get_user(user_id):
    with db() as db_ctx:
        db_ctx.execute(
            f'SELECT id, full_name, last_offer FROM users WHERE id = \'{user_id}\';')
        return db_ctx.fetchall()[0]


def set_offer(loc_destination, loc_source, cost):
    with db() as db_ctx:
        db_ctx.execute(
            'INSERT INTO offers (loc_destination, loc_source, cost) '
            f'VALUES (\'{loc_destination}\', \'{loc_source}\', \'{cost}\');')


def get_offers(last_id):
    with db() as db_ctx:
        db_ctx.execute(
            f'SELECT loc_destination, loc_source, cost, id FROM offers WHERE id > \'{last_id}\';')
        return db_ctx.fetchall()


def update_last_offer_of_user(user_id, last_offer_id):
    with db() as db_ctx:
        db_ctx.execute(
            f'UPDATE users SET last_offer = \'{last_offer_id}\' WHERE id = \'{user_id}\';'
        )


def set_offer_match(user_id, offer_id):
    with db() as db_ctx:
        db_ctx.execute(
            'INSERT INTO matched_offers (user_id, offer_id) '
            f'VALUES (\'{user_id}\', \'{offer_id}\');'
        )
