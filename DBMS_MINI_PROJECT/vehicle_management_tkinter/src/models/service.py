class Service:
    def __init__(self, service_id, vehicle_id, service_date, service_type, cost):
        self.service_id = service_id
        self.vehicle_id = vehicle_id
        self.service_date = service_date
        self.service_type = service_type
        self.cost = cost

    def get_service_details(self):
        return {
            "service_id": self.service_id,
            "vehicle_id": self.vehicle_id,
            "service_date": self.service_date,
            "service_type": self.service_type,
            "cost": self.cost
        }

    @staticmethod
    def from_db_row(row):
        return Service(
            service_id=row[0],
            vehicle_id=row[1],
            service_date=row[2],
            service_type=row[3],
            cost=row[4]
        )