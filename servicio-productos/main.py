from fastapi import FastAPI, Depends, status, HTTPException
from router import router as products_router
from contextlib import asynccontextmanager
from database import connect_db, disconnect_db
from auth import verify_token

import logging

# Configuracion de logs 
logging.basicConfig (
    level= logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s "
)

# Funcion que maneja el pool de conexiones 
@asynccontextmanager
async def lifespan (app:FastAPI):
    await connect_db ()
    yield
    await disconnect_db ()

# Creamos la api 
app = FastAPI (title="Productos Service", 
               lifespan=lifespan,
               dependencies= [Depends(verify_token)]
)
app.include_router (products_router)
