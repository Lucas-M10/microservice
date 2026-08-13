from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from database import connect_db, disconnect_db
from router import router as payment_router
from auth import verify_token

# uvicorn main:app --reload --port 8003
@asynccontextmanager
async def lifespan (app:FastAPI):
    await connect_db ()
    yield
    await disconnect_db ()


app = FastAPI (
    title="Payment Service",
    lifespan=lifespan,
    dependencies= [Depends (verify_token)]
    )


app.include_router (payment_router)