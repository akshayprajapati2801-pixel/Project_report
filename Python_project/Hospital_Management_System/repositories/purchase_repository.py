
from database.connection import Database


class PurchaseRepository:

    def __init__(self):
        self.database = Database()

    def get_all(self):
        query = """
            SELECT
                p.id,
                p.supplier_id,
                s.name AS supplier_name,
                p.total,
                p.purchase_date
            FROM purchases p
            LEFT JOIN suppliers s
                ON p.supplier_id = s.id
            ORDER BY p.id DESC
        """
        return self.database.fetch_all(query)

    def get_by_id(self, purchase_id):
        query = """
            SELECT
                p.id,
                p.supplier_id,
                s.name AS supplier_name,
                p.total,
                p.purchase_date
            FROM purchases p
            LEFT JOIN suppliers s
                ON p.supplier_id = s.id
            WHERE p.id = %s
        """
        return self.database.fetch_one(query, (purchase_id,))

    def get_suppliers(self):
        query = """
            SELECT id, name
            FROM suppliers
            ORDER BY name
        """
        return self.database.fetch_all(query)

    def get_products(self):
        query = """
            SELECT
                id,
                name,
                purchase_price,
                quantity,
                expiry_date,
                is_active
            FROM products
            WHERE is_active = 1
            ORDER BY name
        """
        return self.database.fetch_all(query)

    def get_product_by_id(self, product_id):
        query = """
            SELECT
                id,
                name,
                purchase_price,
                quantity,
                expiry_date,
                is_active
            FROM products
            WHERE id = %s
        """
        return self.database.fetch_one(query, (product_id,))

    def get_purchase_items(self, purchase_id):
        query = """
            SELECT
                pi.id,
                pi.purchase_id,
                pi.product_id,
                p.name AS product_name,
                pi.quantity,
                pi.price,
                pi.subtotal
            FROM purchase_items pi
            LEFT JOIN products p
                ON pi.product_id = p.id
            WHERE pi.purchase_id = %s
            ORDER BY pi.id
        """
        return self.database.fetch_all(query, (purchase_id,))

    def create_purchase_with_items(
        self,
        supplier_id,
        total,
        items
    ):
        connection = self.database.get_connection()
        cursor = connection.cursor()

        try:
            # Validate and lock medicine rows.
            for item in items:
                cursor.execute(
                    """
                    SELECT is_active
                    FROM products
                    WHERE id = %s
                    FOR UPDATE
                    """,
                    (item["product_id"],)
                )
                product = cursor.fetchone()

                if product is None:
                    raise ValueError(
                        f"Medicine not found: {item['product_name']}"
                    )

                if int(product[0] or 0) != 1:
                    raise ValueError(
                        f"Medicine '{item['product_name']}' is inactive."
                    )

                if int(item["quantity"]) <= 0:
                    raise ValueError(
                        "Purchase quantity must be greater than zero."
                    )

                if float(item["price"]) < 0:
                    raise ValueError(
                        "Purchase price cannot be negative."
                    )

            cursor.execute(
                """
                INSERT INTO purchases (supplier_id, total)
                VALUES (%s, %s)
                """,
                (supplier_id, total)
            )
            purchase_id = cursor.lastrowid

            for item in items:
                cursor.execute(
                    """
                    UPDATE products
                    SET quantity = quantity + %s
                    WHERE id = %s AND is_active = 1
                    """,
                    (item["quantity"], item["product_id"])
                )

                if cursor.rowcount != 1:
                    raise ValueError(
                        f"Unable to update medicine: {item['product_name']}"
                    )

                cursor.execute(
                    """
                    INSERT INTO purchase_items (
                        purchase_id,
                        product_id,
                        quantity,
                        price,
                        subtotal
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        purchase_id,
                        item["product_id"],
                        item["quantity"],
                        item["price"],
                        item["subtotal"]
                    )
                )

            connection.commit()
            return purchase_id

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    def update_purchase_with_items(
        self,
        purchase_id,
        supplier_id,
        items
    ):
        """
        Replace purchase items and adjust stock by the difference.
        Reject changes that would reduce stock below zero.
        """
        if not items:
            raise ValueError(
                "A purchase must contain at least one medicine."
            )

        connection = self.database.get_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT id
                FROM purchases
                WHERE id = %s
                FOR UPDATE
                """,
                (purchase_id,)
            )
            if cursor.fetchone() is None:
                raise ValueError("Purchase not found.")

            cursor.execute(
                """
                SELECT product_id, quantity
                FROM purchase_items
                WHERE purchase_id = %s
                """,
                (purchase_id,)
            )
            old_rows = cursor.fetchall()

            old_quantities = {}
            for row in old_rows:
                product_id = int(row["product_id"])
                old_quantities[product_id] = (
                    old_quantities.get(product_id, 0)
                    + int(row["quantity"])
                )

            new_quantities = {}
            total = 0.0

            for item in items:
                product_id = int(item["product_id"])
                quantity = int(item["quantity"])
                price = float(item["price"])

                if quantity <= 0:
                    raise ValueError(
                        "Purchase quantity must be greater than zero."
                    )
                if price < 0:
                    raise ValueError(
                        "Purchase price cannot be negative."
                    )

                new_quantities[product_id] = (
                    new_quantities.get(product_id, 0) + quantity
                )
                item["subtotal"] = quantity * price
                total += item["subtotal"]

            product_ids = sorted(
                set(old_quantities) | set(new_quantities)
            )
            product_rows = {}

            # Lock products in consistent ID order.
            for product_id in product_ids:
                cursor.execute(
                    """
                    SELECT id, quantity, is_active
                    FROM products
                    WHERE id = %s
                    FOR UPDATE
                    """,
                    (product_id,)
                )
                product = cursor.fetchone()

                if product is None:
                    raise ValueError(
                        f"Medicine ID {product_id} no longer exists."
                    )

                product_rows[product_id] = product

            # Check the resulting stock before changing anything.
            for product_id in product_ids:
                product = product_rows[product_id]
                current_stock = int(product["quantity"] or 0)
                old_qty = old_quantities.get(product_id, 0)
                new_qty = new_quantities.get(product_id, 0)

                resulting_stock = current_stock - old_qty + new_qty

                if resulting_stock < 0:
                    raise ValueError(
                        f"Cannot edit this purchase: medicine ID "
                        f"{product_id} has insufficient remaining stock "
                        "to reverse its original purchase quantity."
                    )

                if (
                    new_qty > 0
                    and int(product["is_active"] or 0) != 1
                ):
                    raise ValueError(
                        f"Medicine ID {product_id} is inactive."
                    )

            cursor.execute(
                """
                DELETE FROM purchase_items
                WHERE purchase_id = %s
                """,
                (purchase_id,)
            )

            for product_id in product_ids:
                old_qty = old_quantities.get(product_id, 0)
                new_qty = new_quantities.get(product_id, 0)
                adjustment = new_qty - old_qty

                if adjustment:
                    cursor.execute(
                        """
                        UPDATE products
                        SET quantity = quantity + %s
                        WHERE id = %s
                        """,
                        (adjustment, product_id)
                    )

            for item in items:
                cursor.execute(
                    """
                    INSERT INTO purchase_items (
                        purchase_id,
                        product_id,
                        quantity,
                        price,
                        subtotal
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        purchase_id,
                        item["product_id"],
                        item["quantity"],
                        item["price"],
                        item["subtotal"]
                    )
                )

            cursor.execute(
                """
                UPDATE purchases
                SET supplier_id = %s, total = %s
                WHERE id = %s
                """,
                (supplier_id, total, purchase_id)
            )

            connection.commit()
            return total

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    def delete_purchase(self, purchase_id):
        """
        Delete a purchase only if its quantities can safely
        be reversed without making stock negative.
        """
        connection = self.database.get_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT id
                FROM purchases
                WHERE id = %s
                FOR UPDATE
                """,
                (purchase_id,)
            )
            if cursor.fetchone() is None:
                raise ValueError("Purchase not found.")

            cursor.execute(
                """
                SELECT product_id, quantity
                FROM purchase_items
                WHERE purchase_id = %s
                """,
                (purchase_id,)
            )
            items = cursor.fetchall()

            quantities = {}
            for item in items:
                product_id = int(item["product_id"])
                quantities[product_id] = (
                    quantities.get(product_id, 0)
                    + int(item["quantity"])
                )

            # Lock and validate every affected medicine.
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
                product = cursor.fetchone()

                if product is None:
                    raise ValueError(
                        f"Medicine ID {product_id} no longer exists. "
                        "Purchase cannot be safely deleted."
                    )

                current_stock = int(product["quantity"] or 0)
                if current_stock < quantities[product_id]:
                    raise ValueError(
                        f"Purchase cannot be deleted because medicine "
                        f"ID {product_id} no longer has enough stock "
                        "to reverse this purchase."
                    )

            # Reverse the stock added by this purchase.
            for product_id, quantity in quantities.items():
                cursor.execute(
                    """
                    UPDATE products
                    SET quantity = quantity - %s
                    WHERE id = %s
                    """,
                    (quantity, product_id)
                )

            # Remove details first, then the purchase header.
            cursor.execute(
                """
                DELETE FROM purchase_items
                WHERE purchase_id = %s
                """,
                (purchase_id,)
            )

            cursor.execute(
                """
                DELETE FROM purchases
                WHERE id = %s
                """,
                (purchase_id,)
            )

            connection.commit()
            return True

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()