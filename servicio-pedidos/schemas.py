from pydantic import BaseModel
from datetime import datetime

# Datos que recibe por cada item
class OrderItemCreate (BaseModel):
    product_id: int 
    quantity: int 

# Datos para crear un pedido completo 
class OrderCreate (BaseModel):
    items: list [OrderItemCreate]
    method: str

# Estructura de cada producto que se devuelve dentro del pedido
class OrderItemResponse (BaseModel):
    product_id: int 
    product_name: str
    unit_price: float
    quantity: int 
    sub_total: float

# Estructura completa que la Api devuelve 
class OrderResponse (BaseModel):
    order_id: int 
    status: str
    total:float
    method: str
    created_at: datetime
    updated_at: datetime
    items: list [OrderItemResponse]
