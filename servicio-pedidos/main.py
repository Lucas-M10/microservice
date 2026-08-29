from fastapi import FastAPI
from contextlib import asynccontextmanager

from database import connection_db, disconnect_db
from router import router

import logging

# Configuracion de los logs 
logging.basicConfig (
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s "
)

# Funcion que se encarga del pool de conexiones
@asynccontextmanager
async def lifespan (app:FastAPI):
    await connection_db ()
    yield 
    await disconnect_db ()

#Creacionde la api 
app = FastAPI (
    title="Order Service",
    lifespan=lifespan
    )

# Incluimos los endpoint que tenemos en router.
app.include_router (router)


