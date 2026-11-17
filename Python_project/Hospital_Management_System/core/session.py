# ==========================================
# User Session
# ==========================================


class Session:

    current_user = None

    # --------------------------------------
    # Login
    # --------------------------------------

    @classmethod
    def login(cls, user):

        cls.current_user = user

    # --------------------------------------
    # Logout
    # --------------------------------------

    @classmethod
    def logout(cls):

        cls.current_user = None

    # --------------------------------------
    # Check Login
    # --------------------------------------

    @classmethod
    def is_logged_in(cls):

        return cls.current_user is not None

    # --------------------------------------
    # Current User
    # --------------------------------------

    @classmethod
    def get_user(cls):

        return cls.current_user