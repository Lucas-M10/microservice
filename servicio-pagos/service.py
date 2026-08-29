from schemas import PayCreate, PayResponse
from repository import PaymentRepository
import random 
import logging

logger = logging.getLogger (f"payment-{__name__}")

class PaymentService:

    # Contrustor de nuestra clase 
    def __init__(self, repository:PaymentRepository):
        self._repository = repository


    # Funcion que se encarga de simular el estado del pago con 80% exito 
    def _simulate_processing (self)->tuple [str, str]:
        approved = random.random () > 0.2

        if approved:
              return "APPROVED", "Pago aprobado"
        
        return "REJECTED", "Pago Rechazado durante el procesamiento"


    # Creamos el pago y luego guardamos en la base de datos 
    async def payment_create (self, payment:PayCreate) ->PayResponse:
        logger.info (
             f"El pago se esta procesando, order_id={payment.order_id}, monto={payment.amount}"
        )
        
        if payment.amount <= 0:
            logger.warning (
                f"No se pudo realizar el pago, monto invalido"
            )
            
            raise ValueError ("ERROR!! El monto debe ser mayor a 0")

        method = payment.method.strip().upper()

        allowed_methods = {
            "CARD",
            "TRANSFER"
        }

        if method not in allowed_methods:
            logger.warning (
                f"No se pudo realizar el pago, metodo elegido no disponible"
            )
            raise ValueError ("ERROR!! Metodo de pago incorrecto")

        # Llamamos a la funcion para simular el estado del pago 
        status, message = self._simulate_processing ()

        if status=="APPROVED":
            logger.info (
                f"Pago aprobado. order_id={payment.order_id}"
            )

        else:
            logger.warning (
                f"Pago rechazado. order_id={payment.order_id}"
            )


        return await self._repository.payment_create (
            order_id=payment.order_id,
            amount=payment.amount,
            method=method,
            status=status,
            message=message
        )

    # Funcion donde podemos ver mediante el id del pago 
    async def get_payment_by_id (self, payment_id: int)->PayResponse | None:
        if payment_id <= 0:
            raise ValueError ("ERROR!! Id de pagos invalido")

        return await self._repository.get_by_id (payment_id)


    # Funcion que nos devuelve todos los pagos que hay en la base de datos 
    async def list_payments (self)->list[PayResponse]:
        return await self._repository.get_all ()

    