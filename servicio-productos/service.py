from repository import ProductRepository
from schemas import ProductResponse, ProductCreate
import logging

logger = logging.getLogger (f"product-{__name__}")

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

        product = await self._repository.create_row (
            name=product.name,
            description=product.description,
            price=product.price,
            stock=product.stock
        )

        if product:
            logger.info (
                f"Se creo el poducto de manera correcta"
            )
            return product

        else:
            logger.warning (
                f""
            )


    async def decrease_stock (self, product_id:int, quantity: int ):

        product = await self._repository.get_by_id (product_id)

        if not product:

            logger.warning (
                f"Producto Inexistente. producto_id={product_id}"
            )

            raise ValueError (
                "Error!! Producto no encontrado"
            )

        stock =product.stock

        if quantity> stock:

            logger.warning (
                f"No hay stock suficiente. stock= {stock}, cantidad solicitada= {quantity}"
            )
            raise ValueError(
            "ERROR!! No se pudo realizar la compra, stock insuficiente"
        )

        updated_product = await self._repository.decrease_stock (product_id, quantity)

        if not updated_product:
            logger.warning (
                f"No se pudo actualizar el stock. product_id={product_id}"
            )

            raise ValueError(
            "ERROR!! No se pudo actualizar el stock"
        )

        logger.info(
                f"Stock descontado correctamente. product_id={product_id}"
            )

        return updated_product
