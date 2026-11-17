
class Product:

    def __init__(
        self,
        id=None,
        name="",
        category="",
        price=0,
        purchase_price=0,
        quantity=0,
        supplier_id=None,
        expiry_date=None
    ):
        self.id = id
        self.name = name
        self.category = category
        self.price = price
        self.purchase_price = purchase_price
        self.quantity = quantity
        self.supplier_id = supplier_id
        self.expiry_date = expiry_date

    def __str__(self):
        return f"{self.name} - {self.quantity}"