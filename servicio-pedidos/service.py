from repository import OrderRepository
from schemas import OrderCreate
from config import PRODUCT_TOKEN, PRODUCT_URL, PAYMENT_TOKEN, PAYMENT_URL
import httpx


class OrderService:

    def __init__(self, repository: OrderRepository):
        self._repository = repository

    # Creamos el pedido
    async def create_order (self, order:OrderCreate):
        processed_items = []
        total = 0.0

        # Hacemos la peticion a producto para armar la orden
        async with httpx.AsyncClient () as client:

            for item in order.items:

                product_id = item.product_id
                quantity = item.quantity 

                response = await client.get (
                    f"{PRODUCT_URL}/products/{product_id}",
                    headers={
                        "Authorization":f"Token {PRODUCT_TOKEN}"
                    }
                )

                if response.status_code != 200:
                    raise ValueError ("ERROR!! Producto no encontrado")

                product = response.json ()
                stock = product["stock"]

                if quantity > stock:
                    raise ValueError ("ERROR!! stock insuficiente")

                name_product = product["name"]
                unit_price = product["price"]

                sub_total = quantity * unit_price

                processed_items.append ({
                    "product_id":product_id,
                    "product_name": name_product,
                    "unit_price": unit_price,
                    "quantity": quantity,
                    "sub_total": sub_total
                })

                total += sub_total

        # Cargamos en la base de datos de orders y order_items
        order_row = await self._repository.create_order (
            status= "CREATED",
            total= total,
            method= order.method
        )

        order_id = order_row ["order_id"]

        for item in processed_items:

            await self._repository.create_order_item (
                order_id= order_id,
                product_id= item["product_id"],
                product_name=item["product_name"],
                unit_price=item["unit_price"],
                quantity= item["quantity"],
                sub_total=item["sub_total"]
            )

        # Hacemos la peticion a pagos para crear el pago 
        async with httpx.AsyncClient () as client:

            payment_response = await client.post (
                f"{PAYMENT_URL}/pagos/",
                headers={
                    "Authorization": f"Token {PAYMENT_TOKEN}"
                },
                json={
                    "order_id":order_id,
                    "amount":total,
                    "method": order.method
                }
            )

            if payment_response.status_code != 200:
                raise ValueError ("ERROR!! No se pudo procesar el pago")

            payment = payment_response.json ()

            payment_status = payment["status"]

            if payment_status == "APPROVED":

                for item in processed_items:

                    #Modificamos el stock 
                    stock_response = await client.patch (
                        f"{PRODUCT_URL}/products/{item['product_id']}/stock",
                        headers= {
                            "Authorization": f"Token {PRODUCT_TOKEN}"
                        },
                        json={
                            "quantity": item["quantity"]
                        }
                    )

                    if stock_response.status_code != 200:
                        raise ValueError (
                            "ERROR!! No se pudo actualizar el stock"
                        )

                order_status = "PAID"

                updated_order = await self._repository.update_status (
                    order_id,
                    order_status
                )

            else:
                order_status = "REJECTED"

                updated_order = await self._repository.update_status (
                    order_id,
                    order_status
                )

        return updated_order


    # Devolvemos todos los pedidos
    async def get_all (self):

        return await self._repository.get_all ()

    # Devolvemos un pedido por ID 
    async def get_by_id (self, order_id: int ):

        order = await self._repository.get_by_id (order_id)

        if not order:
            raise ValueError(
                "ERROR!! Pedido no encontrado"
            )

        return order


    async def get_products (self):
        async with httpx.AsyncClient() as client:

            response = await client.get (
                f"{PRODUCT_URL}/products/",
                headers= {
                    "Authorization": f"Token {PRODUCT_TOKEN}"
                }
            )

            if response.status_code != 200:
                raise ValueError (
                    "ERROR!! No se pudiron obtner los productos"
                )

            return response.json ()
