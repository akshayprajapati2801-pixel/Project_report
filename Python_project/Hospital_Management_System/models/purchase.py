class Purchase:

    def __init__(
        self,
        id=None,
        supplier_id=None,
        total=0
    ):
        self.id = id
        self.supplier_id = supplier_id
        self.total = total

    def __str__(self):
        return f"Purchase #{self.id} - {self.total}"