# ==========================================
# Patient / Customer Model
# ==========================================


class Customer:

    def __init__(
        self,
        id=None,
        name="",
        phone="",
        email="",
        address="",
        age=None,
        gender=""
    ):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        self.age = age
        self.gender = gender

    def __str__(self):
        return f"{self.name} - {self.phone}"