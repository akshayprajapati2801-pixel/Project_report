# ==========================================
# Database Connection
# ==========================================

import mysql.connector
from mysql.connector import Error

from config import DB_CONFIG


class Database:

    def __init__(self):
        self.config = DB_CONFIG.copy()

    # --------------------------------------
    # Create MySQL Connection
    # --------------------------------------

    def get_connection(self):

        try:

            connection = mysql.connector.connect(
                host=self.config["host"],
                port=self.config["port"],
                user=self.config["user"],
                password=self.config["password"],
                database=self.config["database"]
            )

            return connection

        except Error as error:

            raise RuntimeError(
                f"MySQL connection failed: {error}"
            )

    # --------------------------------------
    # Fetch Multiple Records
    # --------------------------------------

    def fetch_all(self, query, params=None):

        connection = self.get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        try:

            cursor.execute(
                query,
                params or ()
            )

            result = cursor.fetchall()

            return result

        finally:

            cursor.close()
            connection.close()

    # --------------------------------------
    # Fetch One Record
    # --------------------------------------

    def fetch_one(self, query, params=None):

        connection = self.get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        try:

            cursor.execute(
                query,
                params or ()
            )

            result = cursor.fetchone()

            return result

        finally:

            cursor.close()
            connection.close()

    # --------------------------------------
    # INSERT / UPDATE / DELETE
    # --------------------------------------

    def execute(self, query, params=None):

        connection = self.get_connection()

        cursor = connection.cursor()

        try:

            cursor.execute(
                query,
                params or ()
            )

            connection.commit()

            return cursor.lastrowid

        except Exception:

            connection.rollback()

            raise

        finally:

            cursor.close()
            connection.close()

    # --------------------------------------
    # Execute Multiple Queries
    # --------------------------------------

    def execute_many(self, query, data):

        connection = self.get_connection()

        cursor = connection.cursor()

        try:

            cursor.executemany(
                query,
                data
            )

            connection.commit()

        except Exception:

            connection.rollback()

            raise

        finally:

            cursor.close()
            connection.close()