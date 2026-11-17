
from repositories.purchase_repository import PurchaseRepository


class PurchaseService:

    def __init__(self):
        self.repository = PurchaseRepository()

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, purchase_id):
        return self.repository.get_by_id(purchase_id)

    def get_suppliers(self):
        return self.repository.get_suppliers()

    def get_products(self):
        return self.repository.get_products()

    def get_product_by_id(self, product_id):
        return self.repository.get_product_by_id(product_id)

    def get_purchase_items(self, purchase_id):
        return self.repository.get_purchase_items(purchase_id)

    def create_purchase(self, supplier_id, items):
        if supplier_id is None:
            return False, "Please select a supplier."

        if not items:
            return False, "Please add at least one medicine."

        total = 0

        for item in items:
            try:
                quantity = int(item["quantity"])
                price = float(item["price"])
            except (KeyError, TypeError, ValueError):
                return False, "Please enter valid medicine quantities and prices."

            if quantity <= 0:
                return False, "Quantity must be greater than zero."

            if price < 0:
                return False, "Purchase price cannot be negative."

            item["quantity"] = quantity
            item["price"] = price
            item["subtotal"] = quantity * price
            total += item["subtotal"]

        try:
            purchase_id = self.repository.create_purchase_with_items(
                supplier_id,
                total,
                items
            )
            return True, f"Purchase #{purchase_id} created successfully."

        except Exception as error:
            return False, str(error)

    def update_purchase(self, purchase_id, supplier_id, items):
        if not purchase_id:
            return False, "Please select a valid purchase."

        if supplier_id is None:
            return False, "Please select a supplier."

        if not items:
            return False, "Please add at least one medicine."

        for item in items:
            try:
                item["quantity"] = int(item["quantity"])
                item["price"] = float(item["price"])
            except (KeyError, TypeError, ValueError):
                return False, "Please enter valid medicine quantities and prices."

            if item["quantity"] <= 0:
                return False, "Quantity must be greater than zero."

            if item["price"] < 0:
                return False, "Purchase price cannot be negative."

        try:
            self.repository.update_purchase_with_items(
                purchase_id,
                supplier_id,
                items
            )
            return True, f"Purchase #{purchase_id} updated successfully."

        except Exception as error:
            return False, str(error)

    def delete_purchase(self, purchase_id):
        if not purchase_id:
            return False, "Please select a valid purchase."

        try:
            self.repository.delete_purchase(purchase_id)
            return True, f"Purchase #{purchase_id} deleted successfully."

        except Exception as error:
            return False, str(error)