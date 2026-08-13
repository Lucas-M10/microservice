import asyncpg
from config import DATABASE_URL

pool: asyncpg.Pool | None = None

async def create_table ():
    async with pool.acquire () as connection:
        await connection.execute ("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id SERIAL PRIMARY KEY,
        status VARCHAR(100) NOT NULL,
        total DECIMAL (12, 2) NOT NULL,
        method VARCHAR (50) NOT NULL,
        created_at TIMESTAMPTZ NOT NULL DEFAULT now (),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT now ()
    );

    CREATE TABLE IF NOT EXISTS order_items (
        item_id SERIAL PRIMARY KEY,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        product_name VARCHAR (200) NOT NULL,
        unit_price DECIMAL (12, 2) NOT NULL ,
        quantity INTEGER NOT NULL CHECK (quantity > 0),
        sub_total DECIMAL (12, 2) NOT NULL CHECK (sub_total >0),
        FOREIGN KEY (order_id) REFERENCES orders (order_id)
    );
""")

async def connection_db ():
    global pool

    if not DATABASE_URL:
        raise RuntimeError (
            "Database is not conected"
        )

    pool = await asyncpg.create_pool (DATABASE_URL, min_size=1, max_size=5)
    await create_table ()

async def disconnect_db ():
    if pool: 
        await pool.close ()