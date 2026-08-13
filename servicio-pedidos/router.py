from fastapi import APIRouter, status, HTTPException, Depends
from repository import OrderRepository
from service import OrderService
from schemas import OrderCreate, OrderResponse

def get_service ():
    repository = OrderRepository ()
    return OrderService (repository) 


router = APIRouter (prefix="/orders", tags=["Orders"])

# Accede a todos los productos disponibles 
@router.get ("/")
async def get_products (service: OrderService = Depends (get_service)):
    return await service.get_products ()


# Accede a todas las ordenes disponibles
@router.get (
    "/all",
    response_model=list[OrderResponse]
        )
async def get_all (service:OrderService = Depends (get_service)):

    return await service.get_all ()


# Creamos una orden 
@router.post (
    "/",
    response_model=OrderResponse,
    status_code= status.HTTP_201_CREATED
    )
async def create_order (order: OrderCreate, service:OrderService = Depends (get_service)):
    try :
        return await service.create_order (order)
    except ValueError as error:
        raise HTTPException (
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= str (error)
        )

# Accedemos a una orden mediante el id 
@router.get (
    "/{order_id}",
    response_model=OrderResponse
    )
async def get_order_by_id (order_id: int, service: OrderService = Depends (get_service)):
    try:
        return await service.get_by_id (order_id)

    except ValueError as error:
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )




