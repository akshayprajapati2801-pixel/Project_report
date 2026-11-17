from repositories.supplier_repository import SupplierRepository


class SupplierService:

    def __init__(self):
        self.repository = SupplierRepository()

    def get_all(self):

        return self.repository.get_all()

    def get_by_id(self, supplier_id):

        return self.repository.get_by_id(
            supplier_id
        )

    def create(
        self,
        name,
        phone,
        email,
        address
    ):

        name = name.strip()
        phone = phone.strip()
        email = email.strip()
        address = address.strip()

        if not name:
            return False, "Supplier name is required"

        try:

            self.repository.create(
                name,
                phone,
                email,
                address
            )

            return True, "Supplier added successfully"

        except Exception as error:

            return False, str(error)

    def update(
        self,
        supplier_id,
        name,
        phone,
        email,
        address
    ):

        name = name.strip()
        phone = phone.strip()
        email = email.strip()
        address = address.strip()

        if not name:
            return False, "Supplier name is required"

        try:

            self.repository.update(
                supplier_id,
                name,
                phone,
                email,
                address
            )

            return True, "Supplier updated successfully"

        except Exception as error:

            return False, str(error)

    def delete(self, supplier_id):

        try:

            self.repository.delete(
                supplier_id
            )

            return True, "Supplier deleted successfully"

        except Exception as error:

            return False, str(error)