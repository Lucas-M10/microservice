from schemas import PayResponse
import database

class PaymentRepository:

    # Convertimos a la estructura requerida
    def _to_payment (self, row):

        return PayResponse (
            payment_id= row['payment_id'],
            order_id= row['order_id'],
            amount=row['amount'],
            status=row['status'],
            method=row['method'],
            message=row['message'],
            created_at=row['created_at']
        )

    # Insertamos los datos a la tabla 
    async def payment_create (self, 
        order_id: int, amount: float, method:str,
        status: str, message:str
    )->PayResponse:
        async with database.pool.acquire () as connection:
           row = await connection.fetchrow ("""
        INSERT INTO payments (
            order_id,
            amount,
            method,
            status,
            message)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING *;
        """,
        order_id,
        amount,
        method,
        status,
        message)
           
        return self._to_payment (row)

    # Busqueda por payment_id 
    async def get_by_id (self, payment_id)->PayResponse:
        async with database.pool.acquire () as connection:
            row = await connection.fetchrow ("""
        SELECT *
        FROM payments
        WHERE payment_id = $1    
        """, payment_id)

        return self._to_payment (row) if row else None

    # Devuelve los datos completos 
    async def get_all (self)->list[PayResponse]:
        async with database.pool.acquire () as connection:
            rows = await connection.fetch (
            """
            SELECT * 
            FROM payments
            ORDER BY payment_id
            """
            )

        return [self._to_payment (row) for row in rows ]
