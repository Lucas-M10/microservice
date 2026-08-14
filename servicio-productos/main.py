from fastapi import FastAPI, Depends, status, HTTPException
from router import router as products_router
from contextlib import asynccontextmanager
from database import connect_db, disconnect_db
from auth import verify_token

import logging

logging.basicConfig (
    level= logging.INFO,
    format=format="%(asctime)s | %(levelname)s | %(name)s | %(message)s "
)
#uvicorn main:app --reload --port 8001

@asynccontextmanager
async def lifespan (app:FastAPI):
    await connect_db ()
    yield
    await disconnect_db ()

app = FastAPI (title="Productos Service", 
               lifespan=lifespan,
               dependencies= [Depends(verify_token)]
)
app.include_router (products_router)
