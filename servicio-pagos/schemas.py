from pydantic import BaseModel, Field
from datetime import datetime


class PayCreate (BaseModel):
    order_id: int
    method: str
    amount: float = Field (gt=0)


class PayResponse (BaseModel):
    payment_id: int
    order_id: int 
    amount: float
    status: str
    method: str
    message: str 
    created_at: datetime
