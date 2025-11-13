from tkinter import Frame, Label, Entry, Button, ttk, messagebox
from src.db.repository import get_customers, get_vehicles, get_sales

class CustomerView(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        Label(self, text="Customer Details", font=("Arial", 16)).pack(pady=10)
        self.customer_list = ttk.Treeview(self)
        self.customer_list.pack(fill="both", expand=True)
        self.customer_list["columns"] = ("ID", "Name", "Email")
        self.customer_list.heading("#0", text="ID")
        self.customer_list.heading("#1", text="Name")
        self.customer_list.heading("#2", text="Email")
        self.load_customers()

    def load_customers(self):
        self.customer_list.delete(*self.customer_list.get_children())
        customers = get_customers()
        for customer in customers:
            self.customer_list.insert("", "end", text=customer.id, values=(customer.name, customer.email))

class VehicleView(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        Label(self, text="Vehicle Information", font=("Arial", 16)).pack(pady=10)
        self.vehicle_list = ttk.Treeview(self)
        self.vehicle_list.pack(fill="both", expand=True)
        self.vehicle_list["columns"] = ("ID", "Brand", "Model")
        self.vehicle_list.heading("#0", text="ID")
        self.vehicle_list.heading("#1", text="Brand")
        self.vehicle_list.heading("#2", text="Model")
        self.load_vehicles()

    def load_vehicles(self):
        self.vehicle_list.delete(*self.vehicle_list.get_children())
        vehicles = get_vehicles()
        for vehicle in vehicles:
            self.vehicle_list.insert("", "end", text=vehicle.id, values=(vehicle.brand, vehicle.model))

class SaleView(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        Label(self, text="Sales Records", font=("Arial", 16)).pack(pady=10)
        self.sale_list = ttk.Treeview(self)
        self.sale_list.pack(fill="both", expand=True)
        self.sale_list["columns"] = ("ID", "Customer ID", "Vehicle ID", "Date")
        self.sale_list.heading("#0", text="ID")
        self.sale_list.heading("#1", text="Customer ID")
        self.sale_list.heading("#2", text="Vehicle ID")
        self.sale_list.heading("#3", text="Date")
        self.load_sales()

    def load_sales(self):
        self.sale_list.delete(*self.sale_list.get_children())
        sales = get_sales()
        for sale in sales:
            self.sale_list.insert("", "end", text=sale.id, values=(sale.customer_id, sale.vehicle_id, sale.date))