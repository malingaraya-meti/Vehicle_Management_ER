from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Customer:
    customer_id: int
    name: str
    email: str
    phone: str
    address: str
    purchases: List[int] = field(default_factory=list)  # List of vehicle IDs purchased

    def add_purchase(self, vehicle_id: int):
        self.purchases.append(vehicle_id)

    def remove_purchase(self, vehicle_id: int):
        if vehicle_id in self.purchases:
            self.purchases.remove(vehicle_id)

    def update_contact_info(self, email: Optional[str] = None, phone: Optional[str] = None, address: Optional[str] = None):
        if email:
            self.email = email
        if phone:
            self.phone = phone
        if address:
            self.address = address

    def __str__(self):
        return f"Customer({self.customer_id}, {self.name}, {self.email}, {self.phone}, {self.address})"