# ==========================================
# Patient / Customer Repository
# ==========================================

from database.connection import Database


class CustomerRepository:

    def __init__(self):

        self.database = Database()

    # --------------------------------------
    # Get All Patients
    # --------------------------------------

    def get_all(self):

        query = """
            SELECT
                id,
                name,
                phone,
                email,
                address,
                age,
                gender,
                created_at
            FROM customers
            ORDER BY id DESC
        """

        return self.database.fetch_all(query)

    # --------------------------------------
    # Get Patient By ID
    # --------------------------------------

    def get_by_id(self, customer_id):

        query = """
            SELECT
                id,
                name,
                phone,
                email,
                address,
                age,
                gender,
                created_at
            FROM customers
            WHERE id = %s
        """

        return self.database.fetch_one(
            query,
            (customer_id,)
        )

    # --------------------------------------
    # Add Patient
    # --------------------------------------

    def create(
        self,
        name,
        phone,
        email,
        address,
        age,
        gender
    ):

        query = """
            INSERT INTO customers
            (
                name,
                phone,
                email,
                address,
                age,
                gender
            )
            VALUES
            (
                %s,
                %s,
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
                address,
                age,
                gender
            )
        )

    # --------------------------------------
    # Update Patient
    # --------------------------------------

    def update(
        self,
        customer_id,
        name,
        phone,
        email,
        address,
        age,
        gender
    ):

        query = """
            UPDATE customers
            SET
                name = %s,
                phone = %s,
                email = %s,
                address = %s,
                age = %s,
                gender = %s
            WHERE id = %s
        """

        return self.database.execute(
            query,
            (
                name,
                phone,
                email,
                address,
                age,
                gender,
                customer_id
            )
        )

    # --------------------------------------
    # Delete Patient
    # --------------------------------------

    def delete(self, customer_id):

        query = """
            DELETE FROM customers
            WHERE id = %s
        """

        return self.database.execute(
            query,
            (customer_id,)
        )