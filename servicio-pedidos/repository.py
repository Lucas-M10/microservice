from schemas import OrderItemResponse, OrderResponse
import database

class OrderRepository ():

    # Arma cada elemento de la lista 
    def _to_order_item (self, row) -> OrderItemResponse:
        return OrderItemResponse (
            product_id= row["product_id"],
            product_name= row["product_name"],
            unit_price= float (row["unit_price"]),
            quantity= row["quantity"], 
            sub_total= float (row["sub_total"])
        )

    
    # Arma el pedido completo
    def _to_order (self, row, items) -> OrderResponse:
        return OrderResponse (
            order_id= row["order_id"],
            status= row["status"],
            total= float (row["total"]),
            method= row["method"],
            created_at= row["created_at"],
            updated_at= row["updated_at"],
            items= items
        )


    # Guardamos el pedido 
    async def create_order (self, status, total, method):
        async with  database.pool.acquire () as connection:
           row = await connection.fetchrow ("""
        INSERT INTO orders (
        status, total, method
        )    
        VALUES ($1, $2, $3)
        RETURNING *;""",
        status,
        total,
        method
        )
        return row


    # Guardamos productos que pertenecen a un pedido
    async def create_order_item (self,
        order_id: int, product_id:int , product_name:str, 
        unit_price: float, quantity:int , sub_total:float):

        async with database.pool.acquire () as connection:
            row= await connection.fetchrow ("""
        INSERT INTO order_items (
        order_id, product_id, product_name, 
        unit_price, quantity, sub_total
        )
        VALUES ($1, $2, $3, $4, $5, $6)
        RETURNING *;""",
        order_id,
        product_id,
        product_name,
        unit_price,
        quantity,
        sub_total
        )

        return self._to_order_item (row)
        
    # Buscamos los productos que pertenecen a una orden 
    async def get_items_by_order_id (self, order_id):
        async with database.pool.acquire () as connection:
            rows = await connection.fetch ("""
            SELECT * 
            FROM order_items
            WHERE order_id = $1;""",
            order_id)

            return [self._to_order_item (row) for row in rows ]

    
    # Mostramos todos los pedidos 
    async def get_all (self):
        orders = []
        async with database.pool.acquire () as connection:
            rows = await connection.fetch ("""
        SELECT * 
        FROM orders
        ORDER BY order_id;
    """)
        for row in rows:
            items = await self.get_items_by_order_id (row["order_id"])

            orders.append (self._to_order (row, items))

        return orders


    # Buscamos un pedido especifico por su id 
    async def get_by_id (self, order_id):
        async with database.pool.acquire () as connection:
            row = await connection.fetchrow ("""
        SELECT *
        FROM orders
        WHERE order_id = $1;
        """,
        order_id
        )

        if not row:
            return None

        items = await self.get_items_by_order_id (order_id)

        return self._to_order (row, items)


    # Cambiamos el estado de un pedido
    async def update_status (self, order_id: int, status:str):
        async with database.pool.acquire () as connection:

            row = await connection.fetchrow ("""
        UPDATE orders
        SET status = $1,
            updated_at = now ()
        WHERE order_id = $2
        RETURNING *;""",
        status,
        order_id
        )

        if not row:
            return None

        items = await self.get_items_by_order_id (order_id)

        return self._to_order (row, items) 
