
from database.connection import Database


class DashboardRepository:

    def __init__(self):
        self.database = Database()

    def get_summary(self):
        queries = {
            "patients": "SELECT COUNT(*) AS total FROM customers",
            "medicines": "SELECT COUNT(*) AS total FROM products",
            "employees": "SELECT COUNT(*) AS total FROM employees",
            "sales": "SELECT COUNT(*) AS total FROM sales",
            "purchases": "SELECT COUNT(*) AS total FROM purchases",
        }

        summary = {}

        for name, query in queries.items():
            result = self.database.fetch_one(query)
            summary[name] = int(result["total"]) if result else 0

        return summary