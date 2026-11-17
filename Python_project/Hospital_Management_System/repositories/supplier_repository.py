from database.connection import Database


class SupplierRepository:

    def __init__(self):
        self.database = Database()

    def get_all(self):

        query = """
            SELECT
                id,
                name,
                phone,
                email,
                address,
                created_at
            FROM suppliers
            ORDER BY id DESC
        """

        return self.database.fetch_all(query)

    def get_by_id(self, supplier_id):

        query = """
            SELECT
                id,
                name,
                phone,
                email,
                address,
                created_at
            FROM suppliers
            WHERE id = %s
        """

        return self.database.fetch_one(
            query,
            (supplier_id,)
        )

    def create(
        self,
        name,
        phone,
        email,
        address
    ):

        query = """
            INSERT INTO suppliers
            (
                name,
                phone,
                email,
                address
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s
            )
        """

        return self.database.execute(
            query,
            (
                name,
                phone,
                email,
                address
            )
        )

    def update(
        self,
        supplier_id,
        name,
        phone,
        email,
        address
    ):

        query = """
            UPDATE suppliers
            SET
                name = %s,
                phone = %s,
                email = %s,
                address = %s
            WHERE id = %s
        """

        return self.database.execute(
            query,
            (
                name,
                phone,
                email,
                address,
                supplier_id
            )
        )

    def delete(self, supplier_id):

        query = """
            DELETE FROM suppliers
            WHERE id = %s
        """

        return self.database.execute(
            query,
            (supplier_id,)
        )