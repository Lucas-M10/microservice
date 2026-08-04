from fastapi import FastAPI, Depends, status, HTTPException
from router import router as products_router
from contextlib import asynccontextmanager
from database import connect_db, disconnect_db
#uvicorn main:app --reload --port 8001

@asynccontextmanager
async def lifespan (app:FastAPI):
    await connect_db ()
    yield
    await disconnect_db ()

app = FastAPI (title="Productos Service", lifespan=lifespan)

app.include_router (products_router)

    