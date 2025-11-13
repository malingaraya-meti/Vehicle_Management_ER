from tkinter import Tk, Menu, Frame, Label
from tkinter import ttk
from .views import CustomerView, VehicleView, SaleView
from .animations import animate_button
from .styles import apply_styles

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Vehicle Management System")
        self.root.geometry("1200x800")
        apply_styles(self.root)

        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        view_menu = Menu(menu_bar, tearoff=0)
        view_menu.add_command(label="Customers", command=self.show_customer_view)
        view_menu.add_command(label="Vehicles", command=self.show_vehicle_view)
        view_menu.add_command(label="Sales", command=self.show_sale_view)
        menu_bar.add_cascade(label="View", menu=view_menu)

    def create_widgets(self):
        self.main_frame = Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.label = Label(self.main_frame, text="Welcome to the Vehicle Management System", font=("Arial", 24))
        self.label.pack(pady=20)

        self.button = ttk.Button(self.main_frame, text="Click Me", command=animate_button)
        self.button.pack(pady=10)

    def show_customer_view(self):
        self.clear_main_frame()
        CustomerView(self.main_frame)

    def show_vehicle_view(self):
        self.clear_main_frame()
        VehicleView(self.main_frame)

    def show_sale_view(self):
        self.clear_main_frame()
        SaleView(self.main_frame)

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()