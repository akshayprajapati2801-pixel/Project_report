from database.connection import Database


class EmployeeRepository:

    def __init__(self):
        self.database = Database()

    def get_all(self):

        query = """
            SELECT
                id,
                name,
                phone,
                email,
                department,
                salary,
                created_at
            FROM employees
            ORDER BY id DESC
        """

        return self.database.fetch_all(query)

    def get_by_id(self, employee_id):

        query = """
            SELECT
                id,
                name,
                phone,
                email,
                department,
                salary
            FROM employees
            WHERE id = %s
        """

        return self.database.fetch_one(
            query,
            (employee_id,)
        )

    def create(
        self,
        name,
        phone,
        email,
        department,
        salary
    ):

        query = """
            INSERT INTO employees
            (
                name,
                phone,
                email,
                department,
                salary
            )
            VALUES
            (
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
                department,
                salary
            )
        )

    def update(
        self,
        employee_id,
        name,
        phone,
        email,
        department,
        salary
    ):

        query = """
            UPDATE employees
            SET
                name = %s,
                phone = %s,
                email = %s,
                department = %s,
                salary = %s
            WHERE id = %s
        """

        return self.database.execute(
            query,
            (
                name,
                phone,
                email,
                department,
                salary,
                employee_id
            )
        )

    def delete(self, employee_id):

        query = """
            DELETE FROM employees
            WHERE id = %s
        """

        return self.database.execute(
            query,
            (employee_id,)
        )