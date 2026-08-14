from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from database import connect_db, disconnect_db
from router import router as payment_router
from auth import verify_token
import logging 

# Registramos los eventos que ocurren en la aplicacion
logging.basicConfig (
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

#lifespan que nos ayuda a 
@asynccontextmanager
async def lifespan (app:FastAPI):
    await connect_db ()
    yield
    await disconnect_db ()

#Creamos la app donde estaremos corriendo el servicio 
app = FastAPI (
    title="Payment Service",
    lifespan=lifespan,
    dependencies= [Depends (verify_token)]
    )


app.include_router (payment_router)