from repository import ProductRepository
from schemas import ProductResponse, ProductCreate

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


    async def create_product (self, product:ProductCreate ):
        return await self._repository.create_row (
            name=product.name,
            description=product.description,
            price=product.price,
            stock=product.stock
        )

    async def decrease_stock (self, product_id:int, quantity: int ):

        product = await self._repository.decrease_stock (product_id, quantity)

        if not product:
            raise ValueError (
                "ERROR!! No se pudo realizar la compra, stock insuficiente"
            )

        return product