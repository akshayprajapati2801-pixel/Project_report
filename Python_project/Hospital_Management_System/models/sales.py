class Sale:

    def __init__(
        self,
        id=None,
        customer_id=None,
        total=0,
        payment_method="Cash"
    ):
        self.id = id
        self.customer_id = customer_id
        self.total = total
        self.payment_method = payment_method

    def __str__(self):
        return f"Sale #{self.id} - {self.total}"