from fastapi import APIRouter, HTTPException, Depends, status
from service import ProductService
from repository import ProductRepository
from schemas import ProductResponse, ProductCreate, StockUpdate
import database 
import asyncpg

# Creamos la app que estara vinculada a la api central 
router = APIRouter (prefix="/products", tags=["products", ])

# Creamos el objeto service que utilizaremos
def get_service () -> ProductService:
    repository = ProductRepository ()
    return ProductService (repository)


# Nos devuelve la lista de productos
@router.get ("/",
            response_model= list[ProductResponse])
async def list_products (service: ProductService = Depends (get_service)):
    return await service.list_products ()


# Nos devuelve el producto buscado por id 
@router.get ("/{product_id}",
             response_model=ProductResponse)
async def get_product( product_id: int, service: ProductService = Depends (get_service)):
    product = await service.get_product (product_id)

    if product is None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "Product not found"
        )

    return product

@router.post ("/",
              response_model= ProductResponse,
              status_code= status.HTTP_201_CREATED )
async def create_product (product: ProductCreate, service: ProductService = Depends (get_service)):
    return await service.create_product (product)


# Se encarga de modificar el stock del producto 
@router.patch (
    "/{product_id}/stock",
    response_model=ProductResponse
    )
async def decrease_stock (
    product_id:int,
    data: StockUpdate,
    service:ProductService = Depends (get_service)):

    try:
        return await service.decrease_stock (
            product_id,
            data.quantity
        )

    except ValueError as error:
        raise HTTPException (
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str (error)
        )

        



     