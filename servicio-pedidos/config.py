from dotenv import load_dotenv
import os
load_dotenv ()

DATABASE_URL= os.getenv ("DATABASE_URL", "")

PORT= int(os.getenv ("PORT", "8002"))

PRODUCT_JWT_SECRET = os.getenv ('PRODUCT_JWT_SECRET', '')
PRODUCT_URL = os.getenv ('PRODUCT_URL', '')

PAYMENT_JWT_SECRET = os.getenv ('PAYMENT_JWT_SECRET', '')
PAYMENT_URL = os.getenv ('PAYMENT_URL', '')

JWT_ALGORITHM= "HS256"

PRODUCT_AUDIENCE="products-service"
PAYMENT_AUDIENCE="payment-service"

JWT_SUBJECT="orders-service"