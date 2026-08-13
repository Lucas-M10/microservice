import os
from dotenv import load_dotenv

load_dotenv ()

SERVICE_TOKEN= os.getenv ("PRODUCTS_SERVICE_TOKEN", "")
PORT= int (os.getenv("PORT", "8001"))
DATABASE_URL = os.getenv ("DATABASE_URL", "")

VALID_TOKEN = {SERVICE_TOKEN: "orders-service"}
