import unittest
from src.models.customer import Customer
from src.models.vehicle import Vehicle
from src.models.sale import Sale
from src.models.payment import Payment
from src.models.service import Service

class TestCustomerModel(unittest.TestCase):
    def test_customer_creation(self):
        customer = Customer(name="John Doe", email="john@example.com")
        self.assertEqual(customer.name, "John Doe")
        self.assertEqual(customer.email, "john@example.com")

class TestVehicleModel(unittest.TestCase):
    def test_vehicle_creation(self):
        vehicle = Vehicle(brand="Toyota", model="Camry", year=2020)
        self.assertEqual(vehicle.brand, "Toyota")
        self.assertEqual(vehicle.model, "Camry")
        self.assertEqual(vehicle.year, 2020)

class TestSaleModel(unittest.TestCase):
    def test_sale_creation(self):
        sale = Sale(customer_id=1, vehicle_id=1, amount=25000)
        self.assertEqual(sale.customer_id, 1)
        self.assertEqual(sale.vehicle_id, 1)
        self.assertEqual(sale.amount, 25000)

class TestPaymentModel(unittest.TestCase):
    def test_payment_creation(self):
        payment = Payment(sale_id=1, amount=25000, payment_mode="Credit Card")
        self.assertEqual(payment.sale_id, 1)
        self.assertEqual(payment.amount, 25000)
        self.assertEqual(payment.payment_mode, "Credit Card")

class TestServiceModel(unittest.TestCase):
    def test_service_creation(self):
        service = Service(vehicle_id=1, service_type="Oil Change", cost=100)
        self.assertEqual(service.vehicle_id, 1)
        self.assertEqual(service.service_type, "Oil Change")
        self.assertEqual(service.cost, 100)

if __name__ == '__main__':
    unittest.main()