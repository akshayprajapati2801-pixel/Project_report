
from database.connection import Database


class ProductRepository:

    def __init__(self):
        self.database = Database()

    def get_all(self):
        query = """
            SELECT
                p.id,
                p.name,
                p.category,
                p.price,
                p.purchase_price,
                p.quantity,
                p.supplier_id,
                p.expiry_date,
                p.is_active,
                s.name AS supplier_name
            FROM products p
            LEFT JOIN suppliers s
                ON p.supplier_id = s.id
            ORDER BY p.id DESC
        """
        return self.database.fetch_all(query)

    def get_by_id(self, product_id):
        query = """
            SELECT
                id,
                name,
                category,
                price,
                purchase_price,
                quantity,
                supplier_id,
                expiry_date,
                is_active
            FROM products
            WHERE id = %s
        """
        return self.database.fetch_one(query, (product_id,))

    def get_suppliers(self):
        query = """
            SELECT id, name
            FROM suppliers
            ORDER BY name
        """
        return self.database.fetch_all(query)

    def create(
        self,
        name,
        category,
        price,
        purchase_price,
        quantity,
        supplier_id,
        expiry_date=None
    ):
        query = """
            INSERT INTO products (
                name,
                category,
                price,
                purchase_price,
                quantity,
                supplier_id,
                expiry_date,
                is_active
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, 1)
        """

        return self.database.execute(
            query,
            (
                name,
                category,
                price,
                purchase_price,
                quantity,
                supplier_id,
                expiry_date
            )
        )

    def update(
        self,
        product_id,
        name,
        category,
        price,
        purchase_price,
        quantity,
        supplier_id,
        expiry_date=None
    ):
        query = """
            UPDATE products
            SET
                name = %s,
                category = %s,
                price = %s,
                purchase_price = %s,
                quantity = %s,
                supplier_id = %s,
                expiry_date = %s
            WHERE id = %s
        """

        return self.database.execute(
            query,
            (
                name,
                category,
                price,
                purchase_price,
                quantity,
                supplier_id,
                expiry_date,
                product_id
            )
        )

    def set_active_status(self, product_id, is_active):
        query = """
            UPDATE products
            SET is_active = %s
            WHERE id = %s
        """

        return self.database.execute(
            query,
            (1 if is_active else 0, product_id)
        )

    def delete(self, product_id):
        sales_result = self.database.fetch_one(
            """
            SELECT COUNT(*) AS total
            FROM sale_items
            WHERE product_id = %s
            """,
            (product_id,)
        )

        if sales_result and sales_result["total"] > 0:
            raise ValueError(
                "This medicine has sales history and cannot be deleted. "
                "Mark it inactive instead."
            )

        purchases_result = self.database.fetch_one(
            """
            SELECT COUNT(*) AS total
            FROM purchase_items
            WHERE product_id = %s
            """,
            (product_id,)
        )

        if purchases_result and purchases_result["total"] > 0:
            raise ValueError(
                "This medicine has purchase history and cannot be deleted. "
                "Mark it inactive instead."
            )

        return self.database.execute(
            "DELETE FROM products WHERE id = %s",
            (product_id,)
        )