from .db_context import DBConn as db


# TODO: prevent sql injection


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
        return db_ctx.fetchone()


def set_offer(loc_destination, loc_source, cost, user_id):
    with db() as db_ctx:
        db_ctx.execute(
            'INSERT INTO offers (loc_destination, loc_source, cost, user_id) '
            f'VALUES (\'{loc_destination}\', \'{loc_source}\', \'{cost}\', \'{user_id}\');')


def get_offers_since(last_id):
    with db() as db_ctx:
        db_ctx.execute(
            f'SELECT loc_destination, loc_source, cost, id FROM offers WHERE id > \'{last_id}\';')
        return db_ctx.fetchall()


def get_needs_approval_list(user_id):
    with db() as db_ctx:
        db_ctx.execute(
            f'SELECT * '
            f'FROM matched_offers '
            f'JOIN offers ON matcheed_offers.id = offers.id '
            f'JOIN users ON offers.user_id = matched_offers.user_id '
            f'WHERE offers.user_id = \'{user_id}\' AND offers.status != \'approved\';'
        )
        return db_ctx.fetchall()


def get_active_sender_offers(user_id):
    with db() as db_ctx:
        db_ctx.execute(
            'SELECT loc_destination, loc_source, id '
            'FROM offers '
            'WHERE status != \'approved\' '
            f'AND offers.user_id = \'{user_id}\';'
        )
        return db_ctx.fetchall()


# TODO: better name pls
def get_offers(user_id):
    with db() as db_ctx:
        db_ctx.execute(
            'SELECT offers.loc_destination, offers.loc_source, offers.cost, offers.id FROM offers JOIN matched_offers '
            'ON offers.id = matched_offers.offer_id '
            f'WHERE matched_offers.user_id = \'{user_id}\';')
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
