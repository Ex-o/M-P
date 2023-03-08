from .db_context import DBConn as db


# TODO: prevent sql injection


def register_user(telegram_id, full_name, chat_id):
    with db() as db_ctx:
        db_ctx.execute(
            'INSERT INTO users (id, full_name, chat_id) '
            f'VALUES(\'{telegram_id}\', \'{full_name}\', \'{chat_id}\') '
            f'ON CONFLICT (id) DO UPDATE SET full_name = EXCLUDED.full_name;')


def get_user(user_id):
    with db() as db_ctx:
        db_ctx.execute(
            f'SELECT id, full_name, last_offer FROM users WHERE id = \'{user_id}\';')
        return db_ctx.fetchone()


def set_order_details(id, json):
    with db() as db_ctx:
        db_ctx.execute(
            f'UPDATE offers SET details = \'{json}\' WHERE id = \'{id}\';'
        )


def get_order_by_hash(food_hash):
    with db() as db_ctx:
        db_ctx.execute(
            f'SELECT id, user_id FROM offers WHERE food_hash = \'{food_hash}\';')
        return db_ctx.fetchone()


def add_pending_food_offer(user_id, food_hash, loc_destination, loc_source):
    with db() as db_ctx:
        db_ctx.execute(
            'INSERT INTO offers (loc_destination, loc_source, food_hash, user_id) '
            f'VALUES (\'{loc_destination}\', \'{loc_source}\', \'{food_hash}\', \'{user_id}\');')


def set_offer(loc_destination, loc_source, cost, user_id):
    with db() as db_ctx:
        db_ctx.execute(
            'INSERT INTO offers (loc_destination, loc_source, cost, user_id) '
            f'VALUES (\'{loc_destination}\', \'{loc_source}\', \'{cost}\', \'{user_id}\');')


def get_own_offers(user_id):
    with db() as db_ctx:
        db_ctx.execute(
            f"SELECT * FROM offers WHERE user_id = '{user_id}' AND status != 'completed';"
        )
        return db_ctx.fetchall()


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
            f'JOIN offers ON matched_offers.offer_id = offers.id '
            f'JOIN users ON matched_offers.user_id = users.id '
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


def add_filter(user_id, lat, lon, link, info=""):
    with db() as db_ctx:
        db_ctx.execute(
            'INSERT INTO filters (user_id, lat, lon, link, info) '
            f'VALUES (\'{user_id}\', \'{lat}\', \'{lon}\', \'{link}\', \'{info}\');'
        )


async def get_filters(user_id):
    with db() as db_ctx:
        db_ctx.execute(
            'SELECT id, user_id, lat, lon, link, info FROM filters WHERE '
            f'user_id=\'{user_id}\''
        )
        return db_ctx.fetchall()


async def delete_filter(filter_id):
    with db() as db_ctx:
        db_ctx.execute(
            'DELETE FROM filters WHERE '
            f'id=\'{filter_id}\''
        )
