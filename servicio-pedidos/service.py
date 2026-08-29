from repository import OrderRepository
from schemas import OrderCreate
import httpx, logging, asyncio
from circuit_breaker import CircuitBreaker
from config import PRODUCT_URL, PAYMENT_URL, PAYMENT_JWT_SECRET, PRODUCT_JWT_SECRET, PRODUCT_AUDIENCE, PAYMENT_AUDIENCE
from jwt_utils import generate_jwt

logger = logging.getLogger (f"order-{__name__}")

# vaiables que nos ayudaran a trabajar con 
products_breaker = CircuitBreaker ()
payment_breaker = CircuitBreaker ()

class OrderService:

    def __init__(self, repository: OrderRepository):
        self._repository = repository

    # Funcion que se encarga de reintentar la conexion
    async def _request_with_retry (self, 
        client:httpx.AsyncClient, 
        method:str, 
        url:str,
        breaker:CircuitBreaker, 
        **kwargs):

        max_attempts = 3

        if not breaker.can_request ():
            logger.warning (
                f"Se desabilito el servidor. No se realiza la peticion a {url}"
            )

            raise ValueError(
                "Error!! Servicio temporalmente no disponible"
            )

        for attempt in range (1, max_attempts +1):
            
            try:
                response = await client.request (method, url, **kwargs)
                breaker.record_success ()
                return response

            except (httpx.ConnectError, httpx.ConnectTimeout):

                logger.warning (
                    f"Fallo en peticion HTTP. Intento={attempt}/{max_attempts}"
                )

                if attempt == max_attempts:

                    logger.error (
                        f"Se agotaron los intentos para {url}"
                    )
                    breaker.record_failure ()
                    raise ValueError (
                        "ERROR!! No se pudo conectar con el servicio"
                    )

                await asyncio.sleep (1)

    # Creamos el pedido
    async def create_order (self, order:OrderCreate):

        logger.info (
            f"Iniciando creacion de pedido con {len(order.items)} productos"
        )

        processed_items = []
        total = 0.0

        product_token = generate_jwt (PRODUCT_JWT_SECRET, PRODUCT_AUDIENCE)
        PRODUCT_HEADER = {
                    "Authorization": f"Bearer {product_token}"
                    }

        # Hacemos la peticion a producto para armar la orden
        async with httpx.AsyncClient () as client:

            for item in order.items:

                product_id = item.product_id
                quantity = item.quantity 

                URL = f"{PRODUCT_URL}/products/{product_id}"

                response = await self._request_with_retry (
                    client, 
                    "GET", 
                    URL, 
                    products_breaker,
                    headers=PRODUCT_HEADER
                    )

                if response.status_code != 200:
                    logger.warning (
                        f"No se pudo obtener producto id={product_id}. Status-code={response.status_code}"
                    )
                    raise ValueError ("ERROR!! Producto no encontrado")

                product = response.json ()
                stock = product["stock"]

                if quantity > stock:
                    logger.warning (
                        f"Stock insuficiente para producto id={product_id}, solicitado={quantity}, disponible={stock}"
                    )
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

            URL= f"{PAYMENT_URL}/pagos/"
            payment_token = generate_jwt (PAYMENT_JWT_SECRET, PAYMENT_AUDIENCE)

            HEADERS= {
                "Authorization": f"Bearer {payment_token}"
                }
            json = {
                "order_id": order_id,
                "amount"  : total,
                "method"  : order.method
            }

            payment_response = await self._request_with_retry (
                    client,
                    "POST",
                    URL,
                    payment_breaker,
                    headers=HEADERS,
                    json=json
                )

            if payment_response.status_code != 201:
                logger.error(
                    f"Error procesando pago. order_id={order_id}, Status_code={payment_response.status_code}"
                )
                raise ValueError ("ERROR!! No se pudo procesar el pago")

            payment = payment_response.json ()

            payment_status = payment["status"]

            if payment_status == "APPROVED":

                for item in processed_items:

                    URL= f"{PRODUCT_URL}/products/{item['product_id']}/stock"

                    json={
                        "quantity":item["quantity"]
                    }

                    #Modificamos el stock 
                    stock_response = await self._request_with_retry (
                        client, 
                        "PATCH", 
                        URL,
                        products_breaker, 
                        headers= PRODUCT_HEADER, 
                        json= json)

                    if stock_response.status_code != 200:
                        logger.error (
                            f"Error actualizando stock. order_id={order_id}, product_id={item['product_id']}, status_code={stock_response.status_code}"
                        )

                        raise ValueError (
                            "ERROR!! No se pudo actualizar el stock"
                        )

                order_status = "PAID"

                updated_order = await self._repository.update_status (
                    order_id,
                    order_status
                )

            else:

                logger.warning (
                    f"Pago rechazado. order_id={order_id}"
                )

                order_status = "REJECTED"

                updated_order = await self._repository.update_status (
                    order_id,
                    order_status
                )

        logger.info (
            f"Pedido finalizado correctamente. order_id={order_id}, status={order_status}"
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

    # Accedemos a todos los productos
    async def get_products (self):
        async with httpx.AsyncClient () as client:
            URL= f"{PRODUCT_URL}/products/"
            product_token = generate_jwt (PRODUCT_JWT_SECRET, PRODUCT_AUDIENCE)

            HEADERS= {
                "Authorization": f"Bearer {product_token}"
            }
            
            response = await self._request_with_retry (
                client, 
                "GET", 
                URL,
                products_breaker,
                headers= HEADERS)

            if response.status_code != 200:
                raise ValueError (
                    "ERROR!! No se pudiron obtener los productos"
                )

            return response.json ()
