import asyncpg
from config import DATABASE_URL


pool : asyncpg.Pool | None = None


async def connect_db ():
    global pool

    if not DATABASE_URL:
        raise RuntimeError (
            "DATABASE_URL no esta configurada"
        )
    pool = await asyncpg.create_pool (DATABASE_URL, min_size=1, max_size= 5 )
    await create_table ()


async def create_table ():
    async with pool.acquire () as connection:
        await connection.execute ("""
    CREATE TABLE IF NOT EXISTS products (
        product_id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        description VARCHAR(500) DEFAULT '',
        price DECIMAL (10,2) NOT NULL,
        stock INTEGER NOT NULL,
        active BOOLEAN NOT NULL DEFAULT TRUE,
        created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT now ()
    )
    """)

async def disconnect_db ():
    if pool:
        await pool.close ()