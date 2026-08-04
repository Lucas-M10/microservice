from fastapi import APIRouter, HTTPException, Depends, status
from service import ProductService
from repository import ProductRepository
from schemas import ProductResponse

# Creamos la app que estara vinculada a la api central 
router = APIRouter (prefix="/products", tags=["products"])


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
