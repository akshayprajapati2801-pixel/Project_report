class Employee:

    def __init__(
        self,
        id=None,
        name="",
        phone="",
        email="",
        department="",
        salary=0
    ):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email
        self.department = department
        self.salary = salary

    def __str__(self):
        return f"{self.name} - {self.department}"