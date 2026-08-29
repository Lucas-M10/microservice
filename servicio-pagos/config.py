import os 
from dotenv import load_dotenv 

# Cargamos los datos dele .env
load_dotenv ()

# variables que utilizaremos 
DATABASE_URL = os.getenv ("DATABASE_URL", "")

PORT= int (os.getenv ("PORT", "8003"))

PAYMENT_JWT_SECRET = os.getenv ("PAYMENT_JWT_SECRET", "")
JWT_ALGORITHM = "HS256"
JWT_AUDIENCE= "payment-service"
JWT_SUBJECT = "orders-service"
