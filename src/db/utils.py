from .db_context import create_db as db


# TODO: prevent sql injection


async def register_user(telegram_id, full_name, chat_id):
    async with await db() as db_ctx:
        await db_ctx.execute(
            'INSERT INTO users (id, full_name, chat_id) '
            f'VALUES(\'{telegram_id}\', \'{full_name}\', \'{chat_id}\') '
            f'ON CONFLICT (id) DO UPDATE SET full_name = EXCLUDED.full_name;')


async def get_user(user_id):
    async with await db() as db_ctx:
        return await db_ctx.fetchrow(
            f'SELECT id, full_name, last_offer, trust_score_sender, trust_score_courier FROM users WHERE id = \'{user_id}\';')


async def delete_offer(offer_id):
    async with await db() as db_ctx:
        await db_ctx.execute(
            f'DELETE FROM offers where id = \'{offer_id}\';'
        )
        await db_ctx.execute(
            f'DELETE FROM matched_offers WHERE offer_id = \'{offer_id}\';'
        )


async def set_offer_details(id, json):
    async with await db() as db_ctx:
        await db_ctx.execute(
            f'UPDATE offers SET details = \'{json}\' WHERE id = \'{id}\';'
        )


async def get_order_by_hash(food_hash):
    async with await db() as db_ctx:
        return await db_ctx.fetchrow(
            f'SELECT id, user_id FROM offers WHERE food_hash = \'{food_hash}\';')


async def add_pending_food_offer(user_id, food_hash, loc_destination, loc_source):
    async with await db() as db_ctx:
        await db_ctx.execute(
            'INSERT INTO offers (loc_destination, loc_source, food_hash, user_id) '
            f'VALUES (\'{loc_destination}\', \'{loc_source}\', \'{food_hash}\', \'{user_id}\');')


async def set_offer(loc_destination, loc_source, cost, user_id):
    async with await db() as db_ctx:
        await db_ctx.execute(
            'INSERT INTO offers (loc_destination, loc_source, cost, user_id) '
            f'VALUES (\'{loc_destination}\', \'{loc_source}\', \'{cost}\', \'{user_id}\');')


async def set_offer_status(offer_id, new_status):
    async with await db() as db_ctx:
        await db_ctx.execute(
            f'UPDATE offers SET status = \'{new_status}\' WHERE id = \'{offer_id}\';'
        )


async def get_own_offers(user_id):
    async with await db() as db_ctx:
        return await db_ctx.fetch(
            f"SELECT * FROM offers WHERE user_id = '{user_id}' AND status != 'completed';"
        )


async def get_offers_by_status(status, user_id):
    async with await db() as db_ctx:
        return await db_ctx.fetch(
            f"SELECT offers.loc_destination, offers.loc_source, offers.cost, offers.id FROM offers "
            f"LEFT JOIN matched_offers ON offer_id = offers.id WHERE status = \'{status}\' "
            f"AND (matched_offers.user_id != {user_id} OR matched_offers.user_id IS NULL) "
            f"AND offers.user_id != {user_id};")


async def delete_other_matches(offer_id, user_id):
    async with await db() as db_ctx:
        await db_ctx.execute(
            f'DELETE FROM matched_offers WHERE offer_id = \'{offer_id}\' AND user_id != \'{user_id}\';'
        )
        await db_ctx.execute(
            f'UPDATE offers SET status = \'approved\' WHERE id = \'{offer_id}\';'
        )


async def add_temp_order(order_id, telegram_alias, offer):
    async with await db() as db_ctx:
        await db_ctx.execute(
            'INSERT INTO temp_orders (id, telegram_alias, order_json) '
            f'VALUES (\'{order_id}\', \'{telegram_alias}\', \'{offer}\');')


async def get_temp_order(order_id):
    async with await db() as db_ctx:
        return await db_ctx.fetch(
            f"SELECT * FROM temp_orders WHERE id = \'{order_id}\';"
        )


async def get_needs_approval_list(user_id):
    async with await db() as db_ctx:
        return await db_ctx.fetch(
            f'SELECT * '
            f'FROM matched_offers '
            f'JOIN offers ON matched_offers.offer_id = offers.id '
            f'JOIN users ON matched_offers.user_id = users.id '
            f'WHERE offers.user_id = \'{user_id}\' AND offers.status != \'approved\';'
        )


async def get_active_sender_offers(user_id):
    async with await db() as db_ctx:
        return await db_ctx.fetch(
            'SELECT loc_destination, loc_source, id '
            'FROM offers '
            'WHERE status != \'approved\' '
            f'AND offers.user_id = \'{user_id}\';'
        )


# TODO: better name pls
async def get_active_offers(user_id):
    async with await db() as db_ctx:
        return await db_ctx.fetch(
            'SELECT offers.loc_destination, offers.loc_source, offers.cost, offers.id FROM offers JOIN matched_offers '
            'ON offers.id = matched_offers.offer_id '
            f'WHERE matched_offers.user_id = \'{user_id}\';')


async def get_menu_items(id_list):
    async with await db() as db_ctx:
        values = ','.join(["'{0}'".format(x) for x in id_list])

        return await db_ctx.fetch(
            f'SELECT id, shop, title, price, currency FROM menu WHERE id IN ({values});'
        )


async def update_last_offer_of_user(user_id, last_offer_id):
    async with await db() as db_ctx:
        await db_ctx.execute(
            f'UPDATE users SET last_offer = \'{last_offer_id}\' WHERE id = \'{user_id}\';'
        )


async def set_offer_match(user_id, offer_id):
    async with await db() as db_ctx:
        await db_ctx.execute(
            'INSERT INTO matched_offers (user_id, offer_id) '
            f'VALUES (\'{user_id}\', \'{offer_id}\');'
        )


async def add_filter(user_id, lat, lon, link, info=""):
    async with await db() as db_ctx:
        await db_ctx.execute(
            'INSERT INTO filters (user_id, lat, lon, link, info) '
            f'VALUES (\'{user_id}\', \'{lat}\', \'{lon}\', \'{link}\', \'{info}\');'
        )


async def get_filters(user_id):
    async with await db() as db_ctx:
        return await db_ctx.fetch(
            'SELECT id, user_id, lat, lon, link, info FROM filters WHERE '
            f'user_id=\'{user_id}\''
        )


async def delete_filter(filter_id):
    async with await db() as db_ctx:
        await db_ctx.execute(
            'DELETE FROM filters WHERE '
            f'id=\'{filter_id}\''
        )
