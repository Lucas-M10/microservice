from schemas import ProductResponse
import database

#Repository trabaja con los datos 

# Clase que manejara los productos 
class ProductRepository:

    # ver todos los productos
    async def get_all (self) -> list[ProductResponse]:
        async with database.pool.acquire () as connection:
            rows = await connection.fetch ("""
        SELECT *
        FROM products
        ORDER BY product_id;
        """)

        return [self._to_product(row) for row in rows]

    # Ver producto por id
    async def get_by_id (self, product_id: int) -> ProductResponse:
        async with database.pool.acquire () as connection:
            row = await connection.fetchrow ("""
        SELECT * 
        FROM products
        WHERE product_id = $1;""",
        product_id )

        return self._to_product (row) if row else None


    # Creamos los productos
    async def create_row (self, 
    name: str, description:str, price:float, stock:int):
        async with database.pool.acquire () as connection:
            row = await connection.fetchrow ("""
        INSERT INTO products (name, description, price, stock)
        VALUES ($1, $2, $3, $4)
        RETURNING *;""",
        name,
        description,
        price,
        stock)

        return self._to_product (row)
    

    # Convierte lo devuelto por el database a un objeto ProductResponse
    def _to_product (self, row) -> ProductResponse:
        return ProductResponse (
            product_id=row["product_id"],
            name=row["name"],
            description=row["description"],
            price=float(row["price"]),
            stock=row["stock"],
            active=row["active"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )