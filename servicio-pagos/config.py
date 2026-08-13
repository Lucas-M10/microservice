import os 
from dotenv import load_dotenv 

# Cargamos los datos dele .env
load_dotenv ()

# variables que utilizaremos 
DATABASE_URL = os.getenv ("DATABASE_URL", "")

PORT= int (os.getenv ("PORT", "8003"))

SERVICE_TOKEN = os.getenv ("PAYMENT_SERVICE_TOKEN", "")


VALID_TOKEN ={ SERVICE_TOKEN: "orders-service" }