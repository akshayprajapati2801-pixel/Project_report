# ==========================================
# User Model
# ==========================================


class User:

    def __init__(
        self,
        id=None,
        username="",
        password_hash="",
        full_name="",
        role="receptionist",
        active=True
    ):

        self.id = id

        self.username = username

        self.password_hash = password_hash

        self.full_name = full_name

        self.role = role

        self.active = active

    def __str__(self):

        return f"{self.username} - {self.role}"