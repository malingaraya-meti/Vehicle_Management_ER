class Vehicle:
    def __init__(self, vehicle_id, brand, model, year, price, color):
        self.vehicle_id = vehicle_id
        self.brand = brand
        self.model = model
        self.year = year
        self.price = price
        self.color = color

    def __repr__(self):
        return f"Vehicle({self.vehicle_id}, {self.brand}, {self.model}, {self.year}, {self.price}, {self.color})"

    def to_dict(self):
        return {
            "vehicle_id": self.vehicle_id,
            "brand": self.brand,
            "model": self.model,
            "year": self.year,
            "price": self.price,
            "color": self.color
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            vehicle_id=data.get("vehicle_id"),
            brand=data.get("brand"),
            model=data.get("model"),
            year=data.get("year"),
            price=data.get("price"),
            color=data.get("color")
        )