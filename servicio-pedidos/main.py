from fastapi import FastAPI
from contextlib import asynccontextmanager

from database import connection_db, disconnect_db
from router import router

import logging

logging.basicConfig (
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s "
)


@asynccontextmanager
async def lifespan (app:FastAPI):
    await connection_db ()
    yield 
    await disconnect_db ()


app = FastAPI (
    title="Order Service",
    lifespan=lifespan
    )

app.include_router (router)


