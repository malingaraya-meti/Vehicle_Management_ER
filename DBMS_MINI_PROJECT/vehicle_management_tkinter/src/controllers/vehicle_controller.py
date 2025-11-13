from src.db.repository import VehicleRepository

class VehicleController:
    def __init__(self):
        self.repository = VehicleRepository()

    def add_vehicle(self, vehicle_data):
        return self.repository.insert_vehicle(vehicle_data)

    def update_vehicle(self, vehicle_id, vehicle_data):
        return self.repository.update_vehicle(vehicle_id, vehicle_data)

    def delete_vehicle(self, vehicle_id):
        return self.repository.delete_vehicle(vehicle_id)

    def get_all_vehicles(self):
        return self.repository.fetch_all_vehicles()

    def get_vehicle_by_id(self, vehicle_id):
        return self.repository.fetch_vehicle_by_id(vehicle_id)