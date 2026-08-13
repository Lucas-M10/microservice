import asyncpg 
from config import DATABASE_URL


pool: asyncpg.Pool | None = None

async def connect_db ():
    global pool

    if not DATABASE_URL:
        raise RuntimeError(
            "Database is not conected"
        )
    
    pool = await asyncpg.create_pool (DATABASE_URL, min_size=1, max_size=5)
    await create_table ()


async def create_table ():
    async with pool.acquire () as connection:
        await connection.execute ("""
    CREATE TABLE IF NOT EXISTS payments (
        payment_id SERIAL PRIMARY KEY,
        order_id INT NOT NULL,
        amount DECIMAL (12, 2) NOT NULL,
        method VARCHAR (50) NOT NULL,
        status VARCHAR (20) NOT NULL DEFAULT 'PENDING' 
            CHECK (status IN ('PENDING', 'APPROVED', 'REJECTED')),
        message VARCHAR (255),
        created_at TIMESTAMPTZ NOT NULL DEFAULT now (),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT now ()
    );
""")

async def disconnect_db ():
    if pool:
        await pool.close ()

