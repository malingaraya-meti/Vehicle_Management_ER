import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

# ------- LOGIN/REGISTRATION WINDOW -------
class LoginRegisterWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login/Registration - Vehicle Management System")
        self.root.geometry("400x380")
        self.root.configure(bg='#34495e')
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '720438',
            'database': 'vehicle_management_er'
        }
        self.connection = None
        self.connect_to_database()
        self.create_tables()
        tk.Label(root, text="Login/Register", font=('Arial',18,'bold'), bg='#34495e', fg='white').pack(pady=18)
        tk.Label(root, text="Username:", font=('Arial',12), bg='#34495e', fg='white').pack(pady=2)
        self.username_entry = tk.Entry(root, font=('Arial',12), width=25)
        self.username_entry.pack(pady=2)
        tk.Label(root, text="Password:", font=('Arial',12), bg='#34495e', fg='white').pack(pady=2)
        self.password_entry = tk.Entry(root, font=('Arial',12), show='*', width=25)
        self.password_entry.pack(pady=2)
        tk.Label(root, text="Role:", font=('Arial',12), bg='#34495e', fg='white').pack(pady=2)
        self.role_var = tk.StringVar(value='Customer')
        self.role_combo = ttk.Combobox(root, textvariable=self.role_var, values=['Customer','Admin'], state='readonly', width=22)
        self.role_combo.pack(pady=2)
        tk.Button(root, text="Login", command=self.login, bg='#27ae60', fg='white', font=('Arial',12,'bold'), padx=8, pady=5).pack(pady=10)
        tk.Button(root, text="Register", command=self.register, bg='#2980b9', fg='white', font=('Arial',12,'bold'), padx=8, pady=5).pack()

    def connect_to_database(self):
        try:
            self.connection = mysql.connector.connect(**self.db_config)
        except Error as e:
            messagebox.showerror("DB Error", f"Cannot connect: {e}")
            self.root.quit()

    def create_tables(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    username VARCHAR(100) UNIQUE,
                    password VARCHAR(100),
                    role VARCHAR(15)
                )
            """)
            self.connection.commit()
            cursor.close()
        except Error as e:
            messagebox.showerror("DB Error", f"Cannot create user table: {e}")
            self.root.quit()

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_var.get()
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s AND role=%s", (username, password, role))
            result = cursor.fetchone()
            cursor.close()
            if result:
                self.root.destroy()
                main_interface(role, username)
            else:
                messagebox.showerror("Login Error", "Invalid username, password, or role")
        except Error as e:
            messagebox.showerror("DB Error", f"Login issue: {e}")

    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_var.get()
        if not username or not password:
            messagebox.showwarning("Missing Info", "Username and password required for registration.")
            return
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
            exists = cursor.fetchone()
            if exists:
                messagebox.showerror("Registration Error", "Username already taken.")
                cursor.close()
                return
            cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
            self.connection.commit()
            cursor.close()
            messagebox.showinfo("Success", "Registration successful. You may login now.")
        except Error as e:
            messagebox.showerror("DB Error", f"Registration issue: {e}")

def main_interface(role, username):
    root = tk.Tk()
    VehicleManagementGUI(root, role, username)
    root.mainloop()

# ------- VEHICLE MANAGEMENT GUI - WITH ACCESS CONTROL & LOGOUT -------
class VehicleManagementGUI:
    def __init__(self, root, role, username):
        self.root = root
        self.role = role
        self.username = username
        self.root.title("Vehicle Management System - Final Project")
        self.root.geometry("1400x800")
        self.root.configure(bg='#2c3e50')
        self.db_config = {
            'host': 'localhost',
            'user': 'root', 
            'password': '720438',
            'database': 'vehicle_management_er'
        }
        self.connection = None
        self.connect_to_database()
        self.create_main_interface()

    def connect_to_database(self):
        try:
            self.connection = mysql.connector.connect(**self.db_config)
            if self.connection.is_connected():
                print("Successfully connected to database")
        except Error as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {e}")
            self.root.quit()

    def create_main_interface(self):
        title_frame = tk.Frame(self.root, bg='#34495e', height=60)
        title_frame.pack(fill='x', pady=(0, 10))
        title_label = tk.Label(
            title_frame,
            text=f"⚙️ VEHICLE MANAGEMENT: CRUD, FUNCTIONS, PROCEDURES ⚙️  | Logged in as: {self.username} ({self.role})",
            font=('Arial', 20, 'bold'), bg='#34495e', fg='white'
        )
        title_label.pack(pady=10, side='left')
        # Logout Button
        logout_btn = tk.Button(
            title_frame, text="Logout", font=('Arial', 11, 'bold'),
            bg='#e74c3c', fg='white', padx=12, pady=2,
            command=self.logout
        )
        logout_btn.pack(side='right', padx=18)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#2c3e50', borderwidth=0)
        style.configure('TNotebook.Tab', padding=[20,10], font=('Arial',10,'bold'))
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        self.create_crud_tab()
        self.create_functions_tab()
        self.create_procedures_tab()

    def logout(self):
        self.root.destroy()
        main()

    # ---- CRUD OPERATIONS ----
    def create_crud_tab(self):
        crud_frame = tk.Frame(self.notebook, bg='#ecf0f1')
        self.notebook.add(crud_frame, text='📝 CRUD Operations (R/W Data)')
        top_frame = tk.Frame(crud_frame, bg='#34495e', height=60)
        top_frame.pack(fill='x', pady=(0, 10))
        tk.Label(top_frame, text="Select Table:", font=('Arial', 12, 'bold'), bg='#34495e', fg='white').pack(side='left', padx=20, pady=10)
        tables = ['address', 'appointment', 'customer', 'features', 'insurance', 'payment', 'payment_log', 'sale', 'sales_executive', 'services', 'showroom', 'tax', 'vehicles']
        self.selected_table = tk.StringVar(value='customer')
        table_menu = ttk.Combobox(top_frame, textvariable=self.selected_table, values=tables, state='readonly', width=20, font=('Arial', 11))
        table_menu.pack(side='left', padx=10, pady=10)
        table_menu.bind('<<ComboboxSelected>>', lambda e: self.load_table_data())
        btn_frame = tk.Frame(top_frame, bg='#34495e')
        btn_frame.pack(side='right', padx=20)
        self.btn_refresh = tk.Button(btn_frame, text="🔄 REFRESH DATA", command=self.load_table_data, bg='#f1c40f', fg='black', font=('Arial', 10, 'bold'), padx=15, pady=5)
        self.btn_refresh.pack(side='left', padx=15)
        self.btn_create = tk.Button(btn_frame, text="➕ CREATE", command=self.create_record, bg='#27ae60', fg='white', font=('Arial', 10, 'bold'), padx=15, pady=5)
        self.btn_create.pack(side='left', padx=5)
        self.btn_read = tk.Button(btn_frame, text="📖 READ", command=self.load_table_data, bg='#3498db', fg='white', font=('Arial', 10, 'bold'), padx=15, pady=5)
        self.btn_read.pack(side='left', padx=5)
        self.btn_update = tk.Button(btn_frame, text="✏️ UPDATE", command=self.update_record, bg='#f39c12', fg='white', font=('Arial', 10, 'bold'), padx=15, pady=5)
        self.btn_update.pack(side='left', padx=5)
        self.btn_delete = tk.Button(btn_frame, text="🗑️ DELETE", command=self.delete_record, bg='#e74c3c', fg='white', font=('Arial', 10, 'bold'), padx=15, pady=5)
        self.btn_delete.pack(side='left', padx=5)
        if self.role != "Admin":
            self.btn_create.config(state='disabled')
            self.btn_update.config(state='disabled')
            self.btn_delete.config(state='disabled')
        data_frame = tk.Frame(crud_frame, bg='white', relief='raised', bd=2)
        data_frame.pack(fill='both', expand=True, padx=10, pady=10)
        scroll_y = tk.Scrollbar(data_frame, orient='vertical')
        scroll_x = tk.Scrollbar(data_frame, orient='horizontal')
        self.crud_tree = ttk.Treeview(data_frame, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set, selectmode='browse')
        scroll_y.config(command=self.crud_tree.yview)
        scroll_x.pack(side='bottom', fill='x')
        scroll_y.pack(side='right', fill='y')
        self.crud_tree.pack(fill='both', expand=True)
        self.load_table_data()

    def load_table_data(self):
        try:
            table = self.selected_table.get()
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM {table}")
            self.crud_tree.delete(*self.crud_tree.get_children())
            columns = [desc[0] for desc in cursor.description]
            self.crud_tree['columns'] = columns
            self.crud_tree['show'] = 'headings'
            for col in columns:
                self.crud_tree.heading(col, text=col)
                self.crud_tree.column(col, width=120, anchor='center')
            rows = cursor.fetchall()
            for row in rows:
                self.crud_tree.insert('', 'end', values=row)
            cursor.close()
        except Error as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")

    def create_record(self):
        if self.role != 'Admin':
            messagebox.showerror("Access Denied", "Only Admins can add records.")
            return
        table = self.selected_table.get()
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Create New {table} Record")
        dialog.geometry("500x600")
        dialog.configure(bg='#ecf0f1')
        tk.Label(dialog, text=f"Add New {table}", font=('Arial', 16, 'bold'), bg='#ecf0f1').pack(pady=10)
        cursor = self.connection.cursor()
        cursor.execute(f"DESCRIBE {table}")
        columns = cursor.fetchall()
        cursor.close()
        entries = {}
        input_frame = tk.Frame(dialog, bg='#ecf0f1')
        input_frame.pack(fill='both', expand=True, padx=20, pady=10)
        canvas = tk.Canvas(input_frame, bg='#ecf0f1')
        scrollbar = tk.Scrollbar(input_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#ecf0f1')
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        for col in columns:
            col_name = col[0]
            frame = tk.Frame(scrollable_frame, bg='#ecf0f1')
            frame.pack(fill='x', pady=5)
            tk.Label(frame, text=col_name + ":", font=('Arial',10), bg='#ecf0f1', width=20, anchor='w').pack(side='left')
            entry = tk.Entry(frame, font=('Arial',10), width=30)
            entry.pack(side='left', padx=10)
            entries[col_name] = entry
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        def save_record():
            try:
                input_data = {}
                for col_name, entry in entries.items():
                    value = entry.get().strip()
                    input_data[col_name] = None if value == '' else value
                cols = ', '.join([col for col, val in input_data.items() if val is not None])
                values = [val for val in input_data.values() if val is not None]
                placeholders = ', '.join(['%s'] * len(values))
                cursor = self.connection.cursor()
                query = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
                cursor.execute(query, values)
                self.connection.commit()
                cursor.close()
                messagebox.showinfo("Success", f"Record added to {table}")
                dialog.destroy()
                self.load_table_data()
            except Error as e:
                messagebox.showerror("Error", f"Failed to create record: {e}")
        tk.Button(dialog, text="Save", command=save_record, bg='#27ae60', fg='white', font=('Arial',12,'bold'), padx=30, pady=10).pack(pady=20)

    def update_record(self):
        if self.role != 'Admin':
            messagebox.showerror("Access Denied", "Only Admins can update records.")
            return
        selected = self.crud_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a record to update")
            return
        table = self.selected_table.get()
        values = self.crud_tree.item(selected[0])['values']
        columns = self.crud_tree['columns']
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Update {table} Record")
        dialog.geometry("500x600")
        dialog.configure(bg='#ecf0f1')
        tk.Label(dialog, text=f"Update {table}", font=('Arial', 16, 'bold'), bg='#ecf0f1').pack(pady=10)
        entries = {}
        input_frame = tk.Frame(dialog, bg='#ecf0f1')
        input_frame.pack(fill='both', expand=True, padx=20, pady=10)
        canvas = tk.Canvas(input_frame, bg='#ecf0f1')
        scrollbar = tk.Scrollbar(input_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#ecf0f1')
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        pk_column = columns[0]
        pk_value = values[0]
        is_composite_key = (table in ['payment','address','appointment'])
        for i, col in enumerate(columns):
            frame = tk.Frame(scrollable_frame, bg='#ecf0f1')
            frame.pack(fill='x', pady=5)
            tk.Label(frame, text=col + ":", font=('Arial',10), bg='#ecf0f1', width=20, anchor='w').pack(side='left')
            entry = tk.Entry(frame, font=('Arial',10), width=30)
            entry.insert(0, str(values[i] if values[i] is not None else ''))
            if (not is_composite_key and col==pk_column) or (is_composite_key and i<2): 
                entry.config(state='readonly')
            entry.pack(side='left', padx=10)
            entries[col] = entry
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        def save_update():
            try:
                set_clause = ', '.join([f"{col} = %s" for col in columns])
                new_values = [entries[col].get() for col in columns]
                if is_composite_key:
                    where_clause = f"{columns[0]} = %s AND {columns[1]} = %s"
                    new_values.append(pk_value)
                    new_values.append(values[1])
                else:
                    where_clause = f"{pk_column} = %s"
                    new_values.append(pk_value)
                cursor = self.connection.cursor()
                query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
                cursor.execute(query, new_values)
                self.connection.commit()
                cursor.close()
                messagebox.showinfo("Success", f"Record updated in {table}")
                dialog.destroy()
                self.load_table_data()
            except Error as e:
                messagebox.showerror("Error", f"Failed to update record: {e}")
        tk.Button(dialog, text="Update", command=save_update, bg='#f39c12', fg='white', font=('Arial',12,'bold'), padx=30, pady=20).pack(pady=20)

    def delete_record(self):
        if self.role != 'Admin':
            messagebox.showerror("Access Denied", "Only Admins can delete records.")
            return
        selected = self.crud_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a record to delete")
            return
        table = self.selected_table.get()
        values = self.crud_tree.item(selected[0])['values']
        columns = self.crud_tree['columns']
        is_composite_key = (table in ['payment','address','appointment'])
        pk_column = columns[0]
        pk_value = values[0]
        if is_composite_key:
            where_clause = f"{columns[0]} = %s AND {columns[1]} = %s"
            where_values = (pk_value, values[1])
            deletion_label = f"{columns[0]}={pk_value}, {columns[1]}={values[1]}"
        else:
            where_clause = f"{pk_column} = %s"
            where_values = (pk_value,)
            deletion_label = f"{pk_column}={pk_value}"
        if messagebox.askyesno("Confirm", f"Delete record ({deletion_label}) from {table}?"):
            try:
                cursor = self.connection.cursor()
                query = f"DELETE FROM {table} WHERE {where_clause}"
                cursor.execute(query, where_values)
                self.connection.commit()
                cursor.close()
                messagebox.showinfo("Success", "Record deleted")
                self.load_table_data()
            except Error as e:
                messagebox.showerror("Error", f"Failed to delete record: {e}")

    # ------ FUNCTIONS TAB ------
    def create_functions_tab(self):
        func_frame = tk.Frame(self.notebook, bg='#ecf0f1')
        self.notebook.add(func_frame, text='⚙️ Functions (Calculations)')
        tk.Label(func_frame, text="DATABASE FUNCTIONS", font=('Arial', 16, 'bold'), bg='#9b59b6', fg='white').pack(fill='x', pady=10)
        func1_frame = tk.LabelFrame(func_frame, text="1. Get Total Payment By Sale", font=('Arial', 12, 'bold'), bg='white', relief='raised', bd=3)
        func1_frame.pack(fill='x', padx=20, pady=10)
        tk.Label(func1_frame, text="Sale ID:", font=('Arial',11), bg='white').grid(row=0,column=0,padx=10,pady=10,sticky='w')
        self.sale_id_entry = tk.Entry(func1_frame, font=('Arial',11), width=20)
        self.sale_id_entry.grid(row=0,column=1,padx=10,pady=10)
        tk.Button(func1_frame, text="Calculate Total", command=self.get_total_payment, bg='#9b59b6', fg='white', font=('Arial', 10, 'bold'), padx=20, pady=5).grid(row=0,column=2,padx=10,pady=10)
        self.total_payment_label = tk.Label(func1_frame, text="Result: --", font=('Arial',11,'bold'), bg='white', fg='#e74c3c')
        self.total_payment_label.grid(row=0,column=3,padx=10,pady=10)
        func2_frame = tk.LabelFrame(func_frame, text="2. Get Age Category", font=('Arial', 12, 'bold'), bg='white', relief='raised', bd=3)
        func2_frame.pack(fill='x', padx=20, pady=10)
        tk.Label(func2_frame, text="Customer Age:", font=('Arial',11), bg='white').grid(row=0,column=0,padx=10,pady=10,sticky='w')
        self.age_entry = tk.Entry(func2_frame, font=('Arial',11), width=20)
        self.age_entry.grid(row=0,column=1,padx=10,pady=10)
        tk.Button(func2_frame, text="Get Category", command=self.get_age_category, bg='#9b59b6', fg='white', font=('Arial', 10, 'bold'), padx=20, pady=5).grid(row=0,column=2,padx=10,pady=10)
        self.age_category_label = tk.Label(func2_frame, text="Result: --", font=('Arial',11,'bold'), bg='white', fg='#e74c3c')
        self.age_category_label.grid(row=0,column=3,padx=10,pady=10)
        func3_frame = tk.LabelFrame(func_frame, text="3. Get Total Tax for Vehicle", font=('Arial', 12, 'bold'), bg='white', relief='raised', bd=3)
        func3_frame.pack(fill='x', padx=20, pady=10)
        tk.Label(func3_frame, text="Vehicle ID:", font=('Arial',11), bg='white').grid(row=0,column=0,padx=10,pady=10,sticky='w')
        self.vehicle_id_entry = tk.Entry(func3_frame, font=('Arial',11), width=20)
        self.vehicle_id_entry.grid(row=0,column=1,padx=10,pady=10)
        tk.Button(func3_frame, text="Calculate Tax", command=self.get_total_tax, bg='#9b59b6', fg='white', font=('Arial', 10, 'bold'), padx=20, pady=5).grid(row=0,column=2,padx=10,pady=10)
        self.total_tax_label = tk.Label(func3_frame, text="Result: --", font=('Arial',11,'bold'), bg='white', fg='#e74c3c')
        self.total_tax_label.grid(row=0,column=3,padx=10,pady=10)

    def get_total_payment(self):
        try:
            sale_id = self.sale_id_entry.get()
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT SUM(Amount) FROM payment WHERE Sale_ID = {sale_id}")
            result = cursor.fetchone()[0]
            cursor.close()
            self.total_payment_label.config(text=f"Result: ₹{result:,.2f}" if result is not None else "Result: ₹0.00")
        except Error as e:
            messagebox.showerror("Error", f"Failed to execute function: {e}")

    def get_age_category(self):
        try:
            age = self.age_entry.get()
            cursor = self.connection.cursor()
            cursor.execute(f"""
                SELECT 
                    CASE 
                        WHEN {age} < 25 THEN 'Young' 
                        WHEN {age} BETWEEN 25 AND 50 THEN 'Middle-aged' 
                        ELSE 'Senior' 
                    END
            """)
            result = cursor.fetchone()[0]
            cursor.close()
            self.age_category_label.config(text=f"Result: {result}")
        except Error as e:
            messagebox.showerror("Error", f"Failed to execute function: {e}")

    def get_total_tax(self):
        try:
            vehicle_id = self.vehicle_id_entry.get()
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT (Vehicle_Tax + Road_Tax) FROM tax WHERE Vehicle_ID = {vehicle_id}")
            result = cursor.fetchone()[0]
            cursor.close()
            self.total_tax_label.config(text=f"Result: ₹{result:,.2f}" if result is not None else "Result: ₹0.00")
        except Error as e:
            messagebox.showerror("Error", f"Failed to execute function: {e}")

    # ------ PROCEDURE TAB ------
    def create_procedures_tab(self):
        proc_frame = tk.Frame(self.notebook, bg='#ecf0f1')
        self.notebook.add(proc_frame, text='📋 Procedures (Transactional Logic)')
        tk.Label(proc_frame, text="STORED PROCEDURES", font=('Arial', 16, 'bold'), bg='#e67e22', fg='white').pack(fill='x', pady=10)
        # Restrict for non-admins:
        if self.role != "Admin":
            tk.Label(proc_frame, text="Only Admins can perform these operations.", font=('Arial', 14, 'bold'), bg='#ecf0f1', fg='#e74c3c').pack(pady=20)
            return

        proc1_frame = tk.LabelFrame(proc_frame, text="1. Finalize Sale Payment", font=('Arial',12,'bold'), bg='white', relief='raised', bd=3)
        proc1_frame.pack(fill='x', padx=20, pady=10)
        fields = ['Sale ID', 'Amount']
        self.payment_entries = {}
        for i, field in enumerate(fields):
            tk.Label(proc1_frame, text=field + ":", font=('Arial', 10), bg='white').grid(row=i, column=0, padx=10, pady=5, sticky='w')
            entry = tk.Entry(proc1_frame, font=('Arial', 10), width=30)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.payment_entries[field] = entry
        tk.Label(proc1_frame, text="*Procedure finds next Payment_sequence_no*", font=('Arial',9,'italic'), bg='white', fg='gray').grid(row=2, column=0, columnspan=2, pady=(0,5))
        tk.Button(proc1_frame, text="Record Payment (Call FinalizeSalePayment)", command=self.call_finalize_payment, bg='#e67e22', fg='white', font=('Arial',11,'bold'), padx=20, pady=8).grid(row=3,column=0,columnspan=2,pady=15)

        proc2_frame = tk.LabelFrame(proc_frame, text="2. Get Showroom Sales Summary", font=('Arial',12,'bold'), bg='white', relief='raised', bd=3)
        proc2_frame.pack(fill='both', expand=True, padx=20, pady=10)
        control_frame = tk.Frame(proc2_frame, bg='white')
        control_frame.pack(fill='x', pady=10)
        tk.Label(control_frame, text="Showroom ID (1-4):", font=('Arial',11), bg='white').pack(side='left', padx=10)
        self.showroom_id_entry = tk.Entry(control_frame, font=('Arial',11), width=15)
        self.showroom_id_entry.pack(side='left', padx=10)
        tk.Button(control_frame, text="Get Summary (Call GetShowroomSalesSummary)", command=self.get_showroom_sales, bg='#e67e22', fg='white', font=('Arial',10,'bold'), padx=20, pady=5).pack(side='left', padx=10)
        result_frame = tk.Frame(proc2_frame, bg='white')
        result_frame.pack(fill='both', expand=True, padx=10, pady=10)
        scroll_y = tk.Scrollbar(result_frame, orient='vertical')
        scroll_y.pack(side='right', fill='y')
        self.proc_tree = ttk.Treeview(result_frame, yscrollcommand=scroll_y.set, selectmode='browse', height=8)
        self.proc_tree.pack(fill='both', expand=True)
        scroll_y.config(command=self.proc_tree.yview)

    def call_finalize_payment(self):
        try:
            sale_id = self.payment_entries['Sale ID'].get()
            amount = self.payment_entries['Amount'].get()
            if not sale_id or not amount:
                messagebox.showwarning("Warning", "Sale ID and Amount are required.")
                return
            cursor = self.connection.cursor()
            cursor.callproc('FinalizeSalePayment', [sale_id, amount]) 
            self.connection.commit()
            cursor.close()
            messagebox.showinfo("Success", f"Payment recorded for Sale ID {sale_id}. Sequence number automatically determined by the Stored Procedure.")
        except Error as e:
            messagebox.showerror("Error", f"Failed to execute procedure: {e}")

    def get_showroom_sales(self):
        try:
            showroom_id = self.showroom_id_entry.get()
            if not showroom_id:
                messagebox.showwarning("Warning", "Showroom ID is required.")
                return
            self.proc_tree.delete(*self.proc_tree.get_children())
            cursor = self.connection.cursor()
            cursor.callproc('GetShowroomSalesSummary', [showroom_id])
            for result in cursor.stored_results():
                rows = result.fetchall()
                columns = [desc[0] for desc in result.description]
                self.proc_tree['columns'] = columns
                self.proc_tree['show'] = 'headings'
                for col in columns:
                    self.proc_tree.heading(col, text=col)
                    self.proc_tree.column(col, width=150)
                for row in rows:
                    self.proc_tree.insert('', 'end', values=row)
            cursor.close()
        except Error as e:
            messagebox.showerror("Error", f"Failed to get sales summary. Ensure procedure and data exist: {e}")

    def __del__(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")

# ------- MAIN PROGRAM -------
def main():
    login_root = tk.Tk()
    LoginRegisterWindow(login_root)
    login_root.mainloop()

if __name__ == "__main__":
    main()
