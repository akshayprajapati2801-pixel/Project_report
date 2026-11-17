# ==========================================
# Authentication Service
# ==========================================

from repositories.user_repository import UserRepository
from utils.password import PasswordManager
from core.session import Session


class AuthService:

    def __init__(self):

        self.user_repository = UserRepository()

    # --------------------------------------
    # Login
    # --------------------------------------

    def login(self, username, password):

        username = username.strip()

        if not username:

            return False, "Username is required"

        if not password:

            return False, "Password is required"

        user = self.user_repository.find_by_username(
            username
        )

        if user is None:

            return False, "Invalid username or password"

        password_valid = PasswordManager.verify_password(
            password,
            user["password_hash"]
        )

        if not password_valid:

            return False, "Invalid username or password"

        Session.login(user)

        return True, "Login successful"

    # --------------------------------------
    # Register User
    # --------------------------------------

    def register(
        self,
        username,
        password,
        full_name,
        role="receptionist"
    ):

        username = username.strip()

        full_name = full_name.strip()

        if not username:

            return False, "Username is required"

        if not password:

            return False, "Password is required"

        if not full_name:

            return False, "Full name is required"

        if self.user_repository.username_exists(username):

            return False, "Username already exists"

        password_hash = PasswordManager.hash_password(
            password
        )

        self.user_repository.create_user(
            username,
            password_hash,
            full_name,
            role
        )

        return True, "User created successfully"