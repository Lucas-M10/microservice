from schemas import PayCreate, PayResponse
from repository import PaymentRepository
import random 
import logging

logger = logging.getLogger (f"payment-{__name__}")

class PaymentService:

    def __init__(self, repository:PaymentRepository):
        self._repository = repository

    def _simulate_processing (self)->tuple [str, str]:
        approved = random.random () > 0.2

        if approved:
              return "APPROVED", "Pago aprobado"
        
        return "REJECTED", "Pago Rechazado durante el procesamiento"

    async def payment_create (self, payment:PayCreate) ->PayResponse:
        logger.info (
             f"El pago se esta procesando, order_id={payment.order_id}, monto={payment.amount}"
        )
        
        if payment.amount <= 0:
            logger.warning (
                f"No se pudo realizar el pago, monto invalido"
            )
            
            raise ValueError ("ERROR!! El monto debe ser mayor a 0")

        method = payment.method.strip ().upper ()

        allowed_methods = {
            "CARD",
            "TRANSFER"
        }

        if method not in allowed_methods:
            logger.warning (
                f"No se pudo realizar el pago, metodo elegido no disponible"
            )
            raise ValueError ("ERROR!! Metodo de pago incorrecto")

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

    async def get_payment_by_id (self, payment_id: int)->PayResponse | None:

        if payment_id <= 0:
            raise ValueError ("ERROR!! Id de pagos invalido")

        return await self._repository.get_by_id (payment_id)


    async def list_payments (self)->list[PayResponse]:

        return await self._repository.get_all ()

    