# ==========================================
# User Repository
# ==========================================

from database.connection import Database


class UserRepository:

    def __init__(self):

        self.database = Database()

    # --------------------------------------
    # Find User By Username
    # --------------------------------------

    def find_by_username(self, username):

        query = """
            SELECT
                id,
                username,
                password_hash,
                full_name,
                role,
                active,
                created_at
            FROM users
            WHERE username = %s
            AND active = 1
            LIMIT 1
        """

        return self.database.fetch_one(
            query,
            (username,)
        )

    # --------------------------------------
    # Create User
    # --------------------------------------

    def create_user(
        self,
        username,
        password_hash,
        full_name,
        role
    ):

        query = """
            INSERT INTO users
            (
                username,
                password_hash,
                full_name,
                role
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
                username,
                password_hash,
                full_name,
                role
            )
        )

    # --------------------------------------
    # Check Username
    # --------------------------------------

    def username_exists(self, username):

        query = """
            SELECT id
            FROM users
            WHERE username = %s
            LIMIT 1
        """

        user = self.database.fetch_one(
            query,
            (username,)
        )

        return user is not None