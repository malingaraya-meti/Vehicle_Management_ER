from src.db.repository import SaleRepository

class SaleController:
    def __init__(self):
        self.sale_repository = SaleRepository()

    def create_sale(self, sale_data):
        return self.sale_repository.insert_sale(sale_data)

    def get_all_sales(self):
        return self.sale_repository.fetch_all_sales()

    def get_sale_by_id(self, sale_id):
        return self.sale_repository.fetch_sale_by_id(sale_id)

    def update_sale(self, sale_id, updated_data):
        return self.sale_repository.update_sale(sale_id, updated_data)

    def delete_sale(self, sale_id):
        return self.sale_repository.delete_sale(sale_id)