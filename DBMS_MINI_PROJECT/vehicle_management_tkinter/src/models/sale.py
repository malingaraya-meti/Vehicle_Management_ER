from datetime import datetime

class Sale:
    def __init__(self, sale_id, customer_id, vehicle_id, sales_executive_id, date_of_sale, quantity, offer, amount):
        self.sale_id = sale_id
        self.customer_id = customer_id
        self.vehicle_id = vehicle_id
        self.sales_executive_id = sales_executive_id
        self.date_of_sale = date_of_sale or datetime.now()
        self.quantity = quantity
        self.offer = offer
        self.amount = amount

    def to_dict(self):
        return {
            "sale_id": self.sale_id,
            "customer_id": self.customer_id,
            "vehicle_id": self.vehicle_id,
            "sales_executive_id": self.sales_executive_id,
            "date_of_sale": self.date_of_sale,
            "quantity": self.quantity,
            "offer": self.offer,
            "amount": self.amount
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            sale_id=data.get("sale_id"),
            customer_id=data.get("customer_id"),
            vehicle_id=data.get("vehicle_id"),
            sales_executive_id=data.get("sales_executive_id"),
            date_of_sale=data.get("date_of_sale"),
            quantity=data.get("quantity"),
            offer=data.get("offer"),
            amount=data.get("amount")
        )