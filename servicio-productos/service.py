from repository import ProductRepository
from schemas import ProductResponse

#Service decide que hacer con los datos 

class ProductService:

    def __init__(self, repository: ProductRepository):
        self._repository = repository

    # Devuelve la lista de productos
    async def list_products (self) -> list[ProductResponse]:
        return await self._repository.get_all ()

    # Devuelve el producto por su id
    async def get_product (self, product_id: int) -> ProductResponse | None:
        return await self._repository.get_by_id (product_id)
        