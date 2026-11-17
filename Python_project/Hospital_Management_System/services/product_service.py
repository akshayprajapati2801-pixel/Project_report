
from datetime import date

from repositories.product_repository import ProductRepository


class ProductService:

    def __init__(self):
        self.repository = ProductRepository()

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, product_id):
        return self.repository.get_by_id(product_id)

    def get_suppliers(self):
        return self.repository.get_suppliers()

    def validate_expiry_date(self, expiry_date):
        if expiry_date is None or expiry_date == "":
            return None

        if isinstance(expiry_date, date):
            return expiry_date

        try:
            return date.fromisoformat(str(expiry_date))
        except ValueError:
            raise ValueError(
                "Expiry date must use YYYY-MM-DD format."
            )

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
        name = name.strip()

        if not name:
            return False, "Medicine name is required."

        if price < 0:
            return False, "Selling price cannot be negative."

        if purchase_price < 0:
            return False, "Purchase price cannot be negative."

        if quantity < 0:
            return False, "Quantity cannot be negative."

        try:
            expiry_date = self.validate_expiry_date(expiry_date)

            product_id = self.repository.create(
                name,
                category,
                price,
                purchase_price,
                quantity,
                supplier_id,
                expiry_date
            )

            return True, (
                f"Medicine #{product_id} created successfully."
            )

        except Exception as error:
            return False, str(error)

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
        name = name.strip()

        if not name:
            return False, "Medicine name is required."

        if price < 0:
            return False, "Selling price cannot be negative."

        if purchase_price < 0:
            return False, "Purchase price cannot be negative."

        if quantity < 0:
            return False, "Quantity cannot be negative."

        try:
            expiry_date = self.validate_expiry_date(expiry_date)

            self.repository.update(
                product_id,
                name,
                category,
                price,
                purchase_price,
                quantity,
                supplier_id,
                expiry_date
            )

            return True, "Medicine updated successfully."

        except Exception as error:
            return False, str(error)

    def set_active_status(self, product_id, is_active):
        try:
            product = self.repository.get_by_id(product_id)

            if not product:
                return False, "Medicine not found."

            self.repository.set_active_status(
                product_id,
                bool(is_active)
            )

            if is_active:
                return True, "Medicine activated successfully."

            return True, (
                "Medicine deactivated successfully. "
                "Its sales and purchase history is preserved."
            )

        except Exception as error:
            return False, str(error)

    def delete(self, product_id):
        try:
            self.repository.delete(product_id)
            return True, "Medicine deleted successfully."

        except Exception as error:
            return False, str(error)