class Supplier:

    def __init__(
        self,
        id=None,
        name="",
        phone="",
        email="",
        address=""
    ):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address

    def __str__(self):
        return f"{self.name} - {self.phone}"