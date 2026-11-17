
from repositories.sales_repository import SalesRepository


class SalesService:

    def __init__(self):
        self.repository = SalesRepository()

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, sale_id):
        return self.repository.get_by_id(sale_id)

    def get_customers(self):
        return self.repository.get_customers()

    def get_products(self):
        return self.repository.get_products()

    def get_sale_items(self, sale_id):
        return self.repository.get_sale_items(sale_id)

    def create_sale(self, customer_id, total, payment_method, items):
        try:
            if not customer_id:
                return False, "Please select a customer."

            if not payment_method:
                return False, "Please select a payment method."

            if not items:
                return False, "Please add at least one medicine."

            if total <= 0:
                return False, "Total amount must be greater than zero."

            for item in items:
                if int(item["quantity"]) <= 0:
                    return False, "Medicine quantity must be greater than zero."

                if float(item["price"]) < 0:
                    return False, "Medicine price cannot be negative."

            sale_id = self.repository.create_sale_with_items(
                customer_id,
                total,
                payment_method,
                items
            )
            return True, f"Sale #{sale_id} saved successfully."

        except Exception as error:
            return False, str(error)

    def update_sale(self, sale_id, customer_id, total, payment_method, items):
        try:
            if not sale_id:
                return False, "Please select a sale to edit."

            if not customer_id:
                return False, "Please select a customer."

            if not payment_method:
                return False, "Please select a payment method."

            if not items:
                return False, "Please add at least one medicine."

            if float(total) <= 0:
                return False, "Total amount must be greater than zero."

            for item in items:
                if int(item["quantity"]) <= 0:
                    return False, "Medicine quantity must be greater than zero."

                if float(item["price"]) < 0:
                    return False, "Medicine price cannot be negative."

            self.repository.update_sale_with_items(
                sale_id,
                customer_id,
                total,
                payment_method,
                items
            )
            return True, f"Sale #{sale_id} updated successfully."

        except Exception as error:
            return False, str(error)

    def delete_sale(self, sale_id):
        try:
            if not sale_id:
                return False, "Please select a sale to delete."

            self.repository.delete_sale(sale_id)
            return True, f"Sale #{sale_id} deleted successfully."

        except Exception as error:
            return False, str(error)