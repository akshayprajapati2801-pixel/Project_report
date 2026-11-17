
from database.connection import Database


class SalesRepository:

    def __init__(self):
        self.database = Database()

    def get_all(self):
        query = """
            SELECT
                s.*,
                s.total AS total_amount,
                c.name AS customer_name
            FROM sales s
            LEFT JOIN customers c ON s.customer_id = c.id
            ORDER BY s.id DESC
        """
        return self.database.fetch_all(query)

    def get_by_id(self, sale_id):
        query = """
            SELECT
                s.*,
                s.total AS total_amount,
                c.name AS customer_name
            FROM sales s
            LEFT JOIN customers c ON s.customer_id = c.id
            WHERE s.id = %s
        """
        return self.database.fetch_one(query, (sale_id,))

    def get_customers(self):
        return self.database.fetch_all(
            "SELECT id, name FROM customers ORDER BY name"
        )

    def get_products(self):
        query = """
            SELECT id, name, price, quantity, expiry_date, is_active
            FROM products
            WHERE quantity > 0
              AND is_active = 1
              AND (expiry_date IS NULL OR expiry_date >= CURDATE())
            ORDER BY name
        """
        return self.database.fetch_all(query)

    def get_sale_items(self, sale_id):
        query = """
            SELECT
                si.id,
                si.sale_id,
                si.product_id,
                p.name AS product_name,
                si.quantity,
                si.price,
                si.subtotal
            FROM sale_items si
            LEFT JOIN products p ON si.product_id = p.id
            WHERE si.sale_id = %s
            ORDER BY si.id
        """
        return self.database.fetch_all(query, (sale_id,))

    def create_sale_with_items(
        self, customer_id, total, payment_method, items
    ):
        connection = self.database.get_connection()
        cursor = connection.cursor()

        try:
            # Combine repeated medicine entries before validating stock.
            quantities = {}
            for item in items:
                product_id = int(item["product_id"])
                quantity = int(item["quantity"])

                if quantity <= 0:
                    raise ValueError(
                        "Medicine quantity must be greater than zero."
                    )

                quantities[product_id] = (
                    quantities.get(product_id, 0) + quantity
                )

            for product_id, quantity in quantities.items():
                cursor.execute(
                    """
                    SELECT quantity, expiry_date, is_active
                    FROM products
                    WHERE id = %s
                    FOR UPDATE
                    """,
                    (product_id,)
                )
                product = cursor.fetchone()

                if product is None:
                    raise ValueError(f"Medicine ID {product_id} was not found.")

                stock, expiry_date, is_active = product

                if not is_active:
                    raise ValueError(
                        f"Medicine ID {product_id} is inactive."
                    )

                if expiry_date is not None:
                    cursor.execute("SELECT CURDATE()")
                    today = cursor.fetchone()[0]
                    if expiry_date < today:
                        raise ValueError(
                            f"Medicine ID {product_id} has expired."
                        )

                if stock < quantity:
                    raise ValueError(
                        f"Insufficient stock for medicine ID {product_id}."
                    )

            cursor.execute(
                """
                INSERT INTO sales (customer_id, total, payment_method)
                VALUES (%s, %s, %s)
                """,
                (customer_id, total, payment_method)
            )
            sale_id = cursor.lastrowid

            for item in items:
                cursor.execute(
                    """
                    INSERT INTO sale_items
                        (sale_id, product_id, quantity, price, subtotal)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        sale_id,
                        item["product_id"],
                        item["quantity"],
                        item["price"],
                        item["subtotal"]
                    )
                )

            for product_id, quantity in quantities.items():
                cursor.execute(
                    """
                    UPDATE products
                    SET quantity = quantity - %s
                    WHERE id = %s
                    """,
                    (quantity, product_id)
                )

            connection.commit()
            return sale_id

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    def update_sale_with_items(
        self, sale_id, customer_id, total, payment_method, items
    ):
        connection = self.database.get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                "SELECT id FROM sales WHERE id = %s FOR UPDATE",
                (sale_id,)
            )
            if cursor.fetchone() is None:
                raise ValueError("Sale was not found.")

            cursor.execute(
                """
                SELECT product_id, quantity
                FROM sale_items
                WHERE sale_id = %s
                FOR UPDATE
                """,
                (sale_id,)
            )
            old_rows = cursor.fetchall()

            old_quantities = {}
            for product_id, quantity in old_rows:
                old_quantities[product_id] = (
                    old_quantities.get(product_id, 0) + quantity
                )

            new_quantities = {}
            for item in items:
                product_id = int(item["product_id"])
                quantity = int(item["quantity"])

                if quantity <= 0:
                    raise ValueError(
                        "Medicine quantity must be greater than zero."
                    )

                new_quantities[product_id] = (
                    new_quantities.get(product_id, 0) + quantity
                )

            affected_ids = sorted(
                set(old_quantities) | set(new_quantities)
            )
            product_rows = {}

            # Lock medicine rows in consistent order to reduce deadlocks.
            for product_id in affected_ids:
                cursor.execute(
                    """
                    SELECT quantity, expiry_date, is_active
                    FROM products
                    WHERE id = %s
                    FOR UPDATE
                    """,
                    (product_id,)
                )
                row = cursor.fetchone()
                if row is None:
                    raise ValueError(
                        f"Medicine ID {product_id} no longer exists."
                    )
                product_rows[product_id] = row

            cursor.execute("SELECT CURDATE()")
            today = cursor.fetchone()[0]

            for product_id in affected_ids:
                stock, expiry_date, is_active = product_rows[product_id]
                old_qty = old_quantities.get(product_id, 0)
                new_qty = new_quantities.get(product_id, 0)

                # Stock after reversing this sale, then applying its edit.
                resulting_stock = stock + old_qty - new_qty

                if resulting_stock < 0:
                    raise ValueError(
                        f"Insufficient stock for medicine ID {product_id}."
                    )

                if new_qty > 0:
                    if not is_active:
                        raise ValueError(
                            f"Medicine ID {product_id} is inactive."
                        )
                    if expiry_date is not None and expiry_date < today:
                        raise ValueError(
                            f"Medicine ID {product_id} has expired."
                        )

            cursor.execute(
                "DELETE FROM sale_items WHERE sale_id = %s",
                (sale_id,)
            )

            for product_id in affected_ids:
                old_qty = old_quantities.get(product_id, 0)
                new_qty = new_quantities.get(product_id, 0)
                stock, _, _ = product_rows[product_id]
                resulting_stock = stock + old_qty - new_qty

                cursor.execute(
                    "UPDATE products SET quantity = %s WHERE id = %s",
                    (resulting_stock, product_id)
                )

            for item in items:
                cursor.execute(
                    """
                    INSERT INTO sale_items
                        (sale_id, product_id, quantity, price, subtotal)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        sale_id,
                        item["product_id"],
                        item["quantity"],
                        item["price"],
                        item["subtotal"]
                    )
                )

            cursor.execute(
                """
                UPDATE sales
                SET customer_id = %s, total = %s, payment_method = %s
                WHERE id = %s
                """,
                (customer_id, total, payment_method, sale_id)
            )

            connection.commit()
            return True

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    def delete_sale(self, sale_id):
        connection = self.database.get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                "SELECT id FROM sales WHERE id = %s FOR UPDATE",
                (sale_id,)
            )
            if cursor.fetchone() is None:
                raise ValueError("Sale was not found.")

            cursor.execute(
                """
                SELECT product_id, quantity
                FROM sale_items
                WHERE sale_id = %s
                FOR UPDATE
                """,
                (sale_id,)
            )
            rows = cursor.fetchall()

            quantities = {}
            for product_id, quantity in rows:
                quantities[product_id] = (
                    quantities.get(product_id, 0) + quantity
                )

            for product_id in sorted(quantities):
                cursor.execute(
                    """
                    SELECT quantity
                    FROM products
                    WHERE id = %s
                    FOR UPDATE
                    """,
                    (product_id,)
                )
                row = cursor.fetchone()
                if row is None:
                    raise ValueError(
                        f"Medicine ID {product_id} no longer exists; "
                        "sale cannot safely be deleted."
                    )

            for product_id, quantity in quantities.items():
                cursor.execute(
                    """
                    UPDATE products
                    SET quantity = quantity + %s
                    WHERE id = %s
                    """,
                    (quantity, product_id)
                )

            cursor.execute(
                "DELETE FROM sale_items WHERE sale_id = %s",
                (sale_id,)
            )
            cursor.execute("DELETE FROM sales WHERE id = %s", (sale_id,))

            connection.commit()
            return True

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()