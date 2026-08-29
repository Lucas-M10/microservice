import os
from dotenv import load_dotenv

# Leemos las variables dentro del archivo .env 
load_dotenv ()

# Variables que utilizaremos 

PRODUCTS_JWT_SECRET = os.getenv ("PRODUCTS_JWT_SECRET", "")
JWT_ALGORITHM = "HS256"
JWT_AUDIENCE= "products-service"
JWT_SUBJECT = "orders-service"

PORT= int (os.getenv("PORT", "8001"))
DATABASE_URL = os.getenv ("DATABASE_URL", "")
