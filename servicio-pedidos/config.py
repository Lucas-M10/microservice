from dotenv import load_dotenv
import os
load_dotenv ()

DATABASE_URL= os.getenv ("DATABASE_URL", "")

PORT= int(os.getenv ("PORT", "8002"))

PRODUCT_TOKEN = os.getenv ('PRODUCT_TOKEN', '')
PRODUCT_URL = os.getenv ('PRODUCT_URL', '')

PAYMENT_TOKEN = os.getenv ('PAYMENT_TOKEN', '')
PAYMENT_URL = os.getenv ('PAYMENT_URL', '')

