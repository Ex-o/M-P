from .db_context import DBConn as db


async def set_trust_score(user_id, customer_type, new_value):
    async with await db() as db_ctx:
        db_ctx.execute(
            f'UPDATE users SET {customer_type}=\'{new_value}\' WHERE id=\'{user_id}\';')


async def change_by_delta_trust_score(user_id, customer_type, delta):
    async with await db() as db_ctx:
        db_ctx.execute(
            f'UPDATE users SET {customer_type}={customer_type}+{delta} WHERE id=\'{user_id}\';')


async def get_trust_score(user_id, customer_type):
    async with await db() as db_ctx:
        return await db_ctx.fetchrow(
            f'SELECT {customer_type} FROM users WHERE id=\'{user_id}\';')
