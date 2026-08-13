from pydantic import BaseModel, Field
from datetime import datetime

# Estructura de un producto que se envia (POST)
class ProductCreate (BaseModel):
    name: str = Field (min_length=1, max_length=100)
    description: str = Field (min_length=1, max_length=500)
    price: float = Field (gt=0)
    stock: int = Field (ge=0)

# Estructura que devolvera la Api (GET)
class ProductResponse (BaseModel):
    product_id: int 
    created_at: datetime
    name: str
    description: str
    price: float
    stock: int
    update_at: datetime

class StockUpdate (BaseModel):
    quantity: int 
