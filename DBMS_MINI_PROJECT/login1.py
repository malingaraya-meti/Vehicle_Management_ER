# login1.py (Final Version - Dark Mode + Role-Based DB Access)
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

# === CONFIG - Edit these to match your environment ===
ADMIN_DB_CONFIG = {
    "host": "localhost",
    "user": "vm_admin",
    "password": "Admin@123",
    "database": "Vehicle_Management_ER"
}

VIEWER_DB_CONFIG = {
    "host": "localhost",
    "user": "vm_user",
    "password": "vm_password",
    "database": "Vehicle_Management_ER"
}
# =====================================================

def connect_db(config):
    try:
        return mysql.connector.connect(**config)
    except Error:
        return None


# -------------------- Theme and Style --------------------
DARK_BG = "#2c3e50"
PANEL_BG = "#34495e"
CARD_BG = "#263840"
ACCENT = "#e67e22"
BTN_PRIMARY = "#27ae60"
BTN_SECOND = "#2980b9"
TEXT_FG = "#ffffff"

def apply_ttk_dark_style():
    style = ttk.Style()
    try:
        style.theme_use('clam')
    except:
        pass
    style.configure('TFrame', background=DARK_BG)
    style.configure('TLabel', background=DARK_BG, foreground=TEXT_FG, font=("Arial", 11))
    style.configure('Header.TLabel', font=("Arial", 16, "bold"), background=PANEL_BG, foreground=TEXT_FG)
    style.configure('Accent.TButton', background=ACCENT, foreground=TEXT_FG, font=("Arial", 11, "bold"))
    style.configure('Primary.TButton', background=BTN_PRIMARY, foreground=TEXT_FG, font=("Arial", 11, "bold"))
    style.configure('Secondary.TButton', background=BTN_SECOND, foreground=TEXT_FG, font=("Arial", 11, "bold"))
    style.map('TNotebook.Tab', background=[('selected', PANEL_BG)], foreground=[('selected', TEXT_FG)])
    style.configure("Treeview",
                    background=CARD_BG,
                    fieldbackground=CARD_BG,
                    foreground=TEXT_FG,
                    rowheight=22,
                    font=("Arial", 10))
    style.configure("Treeview.Heading",
                    background=PANEL_BG,
                    foreground=TEXT_FG,
                    font=("Arial", 10, "bold"))


# -------------------- LOGIN / REGISTRATION WINDOW --------------------
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Vehicle Management System")
        self.root.geometry("440x420")
        self.root.configure(bg=DARK_BG)
        apply_ttk_dark_style()

        card = tk.Frame(root, bg=PANEL_BG, padx=20, pady=20)
        card.place(relx=0.5, rely=0.5, anchor="c")

        tk.Label(card, text="VEHICLE MANAGEMENT LOGIN", font=("Arial", 18, "bold"), bg=PANEL_BG, fg=TEXT_FG).pack(pady=(0, 15))
        tk.Label(card, text="Username:", bg=PANEL_BG, fg=TEXT_FG, font=("Arial", 11)).pack(anchor="w", pady=(5, 2))
        self.user_e = tk.Entry(card, width=32, font=("Arial", 10))
        self.user_e.pack()

        tk.Label(card, text="Password:", bg=PANEL_BG, fg=TEXT_FG, font=("Arial", 11)).pack(anchor="w", pady=(8, 2))
        self.pass_e = tk.Entry(card, show="*", width=32, font=("Arial", 10))
        self.pass_e.pack()

        tk.Label(card, text="Role:", bg=PANEL_BG, fg=TEXT_FG, font=("Arial", 11)).pack(anchor="w", pady=(8, 2))
        self.role_var = tk.StringVar(value="customer")
        self.role_cb = ttk.Combobox(card, textvariable=self.role_var,
                                    values=["admin", "employee", "customer"], state="readonly", width=30)
        self.role_cb.pack(pady=(0, 10))

        btn_frame = tk.Frame(card, bg=PANEL_BG)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Login", bg=BTN_PRIMARY, fg=TEXT_FG, font=("Arial", 11, "bold"), width=14,
                  command=self.login).grid(row=0, column=0, padx=6)
        tk.Button(btn_frame, text="Register", bg=BTN_SECOND, fg=TEXT_FG, font=("Arial", 11, "bold"), width=14,
                  command=self.register).grid(row=0, column=1, padx=6)

        self.status = tk.Label(card, text="", bg=PANEL_BG, fg="#f1c40f", font=("Arial", 10))
        self.status.pack(pady=(10, 0))

        self.ensure_users_table()

    def ensure_users_table(self):
        conn = connect_db(ADMIN_DB_CONFIG)
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(100) NOT NULL,
                    role ENUM('admin','employee','customer') NOT NULL
                )
            """)
            conn.commit()
            cur.close()
        finally:
            conn.close()

    def login(self):
        username = self.user_e.get().strip()
        password = self.pass_e.get().strip()
        role = self.role_var.get().strip()

        if not username or not password:
            messagebox.showwarning("Input required", "Enter username and password.")
            return

        conn = connect_db(ADMIN_DB_CONFIG)
        if not conn:
            messagebox.showerror("DB Error", "Cannot connect to database.")
            return

        try:
            cur = conn.cursor()
            cur.execute("SELECT username, role FROM users WHERE username=%s AND password=%s AND role=%s",
                        (username, password, role))
            row = cur.fetchone()
            cur.close()
            conn.close()

            if not row:
                messagebox.showerror("Login Failed", "Invalid username, password, or role.")
                return

            if role == "admin":
                db_conf = ADMIN_DB_CONFIG
            else:
                db_conf = VIEWER_DB_CONFIG

            self.root.destroy()
            root2 = tk.Tk()
            VehicleApp(root2, username, role, db_conf)
            root2.mainloop()

        except Error as e:
            messagebox.showerror("DB Error", f"Login error: {e}")

    def register(self):
        username = self.user_e.get().strip()
        password = self.pass_e.get().strip()
        role = self.role_var.get().strip()

        if not username or not password:
            messagebox.showwarning("Missing Info", "Username and password required.")
            return

        conn = connect_db(ADMIN_DB_CONFIG)
        if not conn:
            messagebox.showerror("DB Error", "Cannot connect to database.")
            return

        try:
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM users WHERE username=%s", (username,))
            if cur.fetchone():
                messagebox.showerror("Exists", "Username already exists.")
                cur.close()
                conn.close()
                return

            cur.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                        (username, password, role))
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Success", "Registration successful! You may login now.")
        except Error as e:
            messagebox.showerror("DB Error", f"Registration failed: {e}")


# -------------------- VEHICLE MANAGEMENT APP --------------------
class VehicleApp:
    def __init__(self, root, username, role, db_conf):
        self.root = root
        self.user = username
        self.role = role
        self.db_conf = db_conf
        self.conn = None
        apply_ttk_dark_style()
        self.connect_db()
        self.root.title(f"Vehicle Management System — {self.user} ({self.role})")
        self.root.geometry("1280x760")
        self.root.configure(bg=DARK_BG)
        self.create_ui()

    def connect_db(self):
        self.conn = connect_db(self.db_conf)
        if not self.conn:
            messagebox.showerror("DB Error", "Cannot connect to database with selected role credentials.")
            self.root.destroy()

    def create_ui(self):
        top = tk.Frame(self.root, bg=PANEL_BG, height=60)
        top.pack(fill="x")
        tk.Label(top, text=f"VEHICLE MANAGEMENT | Logged in as: {self.user} ({self.role})",
                 font=("Arial", 14, "bold"), bg=PANEL_BG, fg=TEXT_FG).pack(side="left", padx=10, pady=10)
        tk.Button(top, text="Logout", bg="#c0392b", fg=TEXT_FG, font=("Arial", 10, "bold"),
                  command=self.logout, padx=10, pady=5).pack(side="right", padx=10, pady=10)

        style = ttk.Style()
        style.configure('TNotebook.Tab', padding=[12, 8], font=("Arial", 11, "bold"))
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.build_crud_tab()
        self.build_functions_tab()
        self.build_procedures_tab()

    def logout(self):
        if self.conn:
            self.conn.close()
        self.root.destroy()
        main()

    # --- CRUD TAB ---
    def build_crud_tab(self):
        crud = tk.Frame(self.notebook, bg=DARK_BG)
        self.notebook.add(crud, text="CRUD Operations")
        top = tk.Frame(crud, bg=PANEL_BG)
        top.pack(fill="x", pady=6)
        tk.Label(top, text="Select Table:", bg=PANEL_BG, fg=TEXT_FG, font=("Arial", 12, "bold")).pack(side="left", padx=10)
        self.table_var = tk.StringVar(value="customer")
        tables = ['address','appointment','customer','features','insurance','payment','payment_log','sale','sales_executive','services','showroom','tax','vehicles']
        self.table_cb = ttk.Combobox(top, textvariable=self.table_var, values=tables, state="readonly", width=25)
        self.table_cb.pack(side="left", padx=6)
        self.table_cb.bind("<<ComboboxSelected>>", lambda e: self.load_table())

        btn_frame = tk.Frame(top, bg=PANEL_BG)
        btn_frame.pack(side="right", padx=6)
        self.btn_refresh = tk.Button(btn_frame, text="Refresh", bg=ACCENT, fg=TEXT_FG, command=self.load_table)
        self.btn_create = tk.Button(btn_frame, text="Add", bg=BTN_PRIMARY, fg=TEXT_FG, command=self.add_record)
        self.btn_update = tk.Button(btn_frame, text="Update", bg="#f39c12", fg=TEXT_FG, command=self.update_record)
        self.btn_delete = tk.Button(btn_frame, text="Delete", bg="#c0392b", fg=TEXT_FG, command=self.delete_record)

        for b in (self.btn_refresh, self.btn_create, self.btn_update, self.btn_delete):
            b.pack(side="left", padx=5)

        if self.role != "admin":
            self.btn_create.config(state="disabled")
            self.btn_update.config(state="disabled")
            self.btn_delete.config(state="disabled")

        frame = tk.Frame(crud, bg=DARK_BG)
        frame.pack(fill="both", expand=True, padx=6, pady=6)
        vs = ttk.Scrollbar(frame, orient="vertical")
        vs.pack(side="right", fill="y")
        self.tree = ttk.Treeview(frame, yscrollcommand=vs.set)
        vs.config(command=self.tree.yview)
        self.tree.pack(fill="both", expand=True, side="left")
        self.load_table()

    def load_table(self):
        table = self.table_var.get()
        if not table:
            return
        try:
            cur = self.conn.cursor()
            cur.execute(f"SELECT * FROM {table}")
            rows = cur.fetchall()
            cols = [d[0] for d in cur.description]
            self.tree.delete(*self.tree.get_children())
            self.tree["columns"] = cols
            self.tree["show"] = "headings"
            for c in cols:
                self.tree.heading(c, text=c)
                self.tree.column(c, width=120, anchor="center")
            for r in rows:
                self.tree.insert("", "end", values=r)
            cur.close()
        except Error as e:
            messagebox.showerror("DB Error", f"Failed to load table: {e}")

    def add_record(self):
        table = self.table_var.get()
        if not table:
            return
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Add into {table}")
        dialog.geometry("500x500")
        dialog.configure(bg=DARK_BG)
        cur = self.conn.cursor()
        cur.execute(f"DESCRIBE {table}")
        cols = cur.fetchall()
        cur.close()

        entries = {}
        for i, col in enumerate(cols):
            tk.Label(dialog, text=col[0], bg=DARK_BG, fg=TEXT_FG).grid(row=i, column=0, padx=8, pady=5, sticky="w")
            e = tk.Entry(dialog, width=40)
            e.grid(row=i, column=1, padx=8, pady=5)
            entries[col[0]] = e

        def do_insert():
            data = {k: (v.get().strip() or None) for k, v in entries.items()}
            cols_nonnull = [k for k, v in data.items() if v is not None]
            vals = [data[c] for c in cols_nonnull]
            if not cols_nonnull:
                messagebox.showwarning("Input", "No values provided.")
                return
            try:
                cur = self.conn.cursor()
                cur.execute(f"INSERT INTO {table} ({', '.join(cols_nonnull)}) VALUES ({', '.join(['%s'] * len(vals))})", vals)
                self.conn.commit()
                cur.close()
                messagebox.showinfo("Inserted", "Record inserted successfully.")
                dialog.destroy()
                self.load_table()
            except Error as e:
                messagebox.showerror("DB Error", str(e))

        tk.Button(dialog, text="Save", bg=BTN_PRIMARY, fg=TEXT_FG, command=do_insert).grid(row=len(cols)+1, column=0, columnspan=2, pady=10)

    def update_record(self):
        sel = self.tree.focus()
        if not sel:
            messagebox.showwarning("Select", "Select a record first.")
            return
        values = self.tree.item(sel, "values")
        cols = list(self.tree["columns"])
        table = self.table_var.get()
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Update {table}")
        dialog.geometry("500x500")
        dialog.configure(bg=DARK_BG)

        entries = {}
        for i, col in enumerate(cols):
            tk.Label(dialog, text=col, bg=DARK_BG, fg=TEXT_FG).grid(row=i, column=0, padx=8, pady=5, sticky="w")
            e = tk.Entry(dialog, width=40)
            e.insert(0, values[i])
            e.grid(row=i, column=1, padx=8, pady=5)
            entries[col] = e

        def do_update():
            try:
                pk_col = cols[0]
                pk_val = values[0]
                set_clause = ", ".join([f"{c}=%s" for c in cols])
                vals = [entries[c].get() for c in cols]
                vals.append(pk_val)
                cur = self.conn.cursor()
                cur.execute(f"UPDATE {table} SET {set_clause} WHERE {pk_col}=%s", vals)
                self.conn.commit()
                cur.close()
                messagebox.showinfo("Updated", "Record updated successfully.")
                dialog.destroy()
                self.load_table()
            except Error as e:
                messagebox.showerror("DB Error", str(e))

        tk.Button(dialog, text="Update", bg="#f39c12", fg=TEXT_FG, command=do_update).grid(row=len(cols)+1, column=0, columnspan=2, pady=10)

    def delete_record(self):
        sel = self.tree.focus()
        if not sel:
            messagebox.showwarning("Select", "Select a record first.")
            return
        values = self.tree.item(sel, "values")
        table = self.table_var.get()
        pk_col = self.tree["columns"][0]
        pk_val = values[0]
        if not messagebox.askyesno("Confirm", f"Delete record {pk_col}={pk_val}?"):
            return
        try:
            cur = self.conn.cursor()
            cur.execute(f"DELETE FROM {table} WHERE {pk_col}=%s", (pk_val,))
            self.conn.commit()
            cur.close()
            self.load_table()
            messagebox.showinfo("Deleted", "Record deleted successfully.")
        except Error as e:
            messagebox.showerror("DB Error", str(e))

    # --- FUNCTIONS TAB ---
    def build_functions_tab(self):
        frm = tk.Frame(self.notebook, bg=DARK_BG)
        self.notebook.add(frm, text="Functions")
        self._add_function(frm, "GetTotalPaymentBySale", "Sale ID", self.fn_total_payment)
        self._add_function(frm, "GetAgeCategory (local)", "Age", self.fn_age_category)
        self._add_function(frm, "GetTotalTax", "Vehicle ID", self.fn_total_tax)

    def _add_function(self, parent, title, label_text, command):
        frame = tk.LabelFrame(parent, text=title, bg=CARD_BG, fg=TEXT_FG)
        frame.pack(fill="x", padx=10, pady=6)
        tk.Label(frame, text=label_text, bg=CARD_BG, fg=TEXT_FG).pack(side="left", padx=6, pady=8)
        entry = tk.Entry(frame, width=15)
        entry.pack(side="left", padx=6)
        result_lbl = tk.Label(frame, text="", bg=CARD_BG, fg="#f1c40f", font=("Arial", 10, "bold"))
        result_lbl.pack(side="left", padx=10)
        tk.Button(frame, text="Execute", bg=ACCENT, fg=TEXT_FG,
                  command=lambda: command(entry.get(), result_lbl)).pack(side="left", padx=6)

    def fn_total_payment(self, val, lbl):
        self.call_fn("SELECT GetTotalPaymentBySale(%s)", val, lbl)

    def fn_age_category(self, val, lbl):
        self.call_fn("SELECT GetAgeCategory(%s)", val, lbl)

    def fn_total_tax(self, val, lbl):
        self.call_fn("SELECT GetTotalTax(%s)", val, lbl)

    def call_fn(self, query, val, lbl):
        try:
            cur = self.conn.cursor()
            cur.execute(query, (val,))
            res = cur.fetchone()
            cur.close()
            lbl.config(text=f"Result: {res[0] if res else 'None'}")
        except Error as e:
            messagebox.showerror("DB Error", f"Function call failed: {e}")

    # --- PROCEDURES TAB ---
    def build_procedures_tab(self):
        frm = tk.Frame(self.notebook, bg=DARK_BG)
        self.notebook.add(frm, text="Procedures")
        self._add_procedure(frm, "InsertServiceDetails", ["Service ID", "Service Name", "Cost"], self.proc_insert_service)
        self._add_procedure(frm, "UpdateVehiclePrice", ["Vehicle ID", "New Price"], self.proc_update_price)
        self._add_procedure(frm, "DeletePaymentLog", ["Payment Log ID"], self.proc_delete_payment_log)

    def _add_procedure(self, parent, title, fields, callback):
        frame = tk.LabelFrame(parent, text=title, bg=CARD_BG, fg=TEXT_FG)
        frame.pack(fill="x", padx=10, pady=6)
        entries = []
        for f in fields:
            tk.Label(frame, text=f, bg=CARD_BG, fg=TEXT_FG).pack(side="left", padx=6, pady=8)
            e = tk.Entry(frame, width=15)
            e.pack(side="left", padx=6)
            entries.append(e)
        tk.Button(frame, text="Execute", bg=ACCENT, fg=TEXT_FG,
                  command=lambda: callback(entries)).pack(side="left", padx=6)

    def proc_insert_service(self, entries):
        vals = [e.get() for e in entries]
        self.call_proc("InsertServiceDetails", vals)

    def proc_update_price(self, entries):
        vals = [e.get() for e in entries]
        self.call_proc("UpdateVehiclePrice", vals)

    def proc_delete_payment_log(self, entries):
        vals = [e.get() for e in entries]
        self.call_proc("DeletePaymentLog", vals)

    def call_proc(self, name, vals):
        try:
            cur = self.conn.cursor()
            cur.callproc(name, vals)
            self.conn.commit()
            cur.close()
            messagebox.showinfo("Executed", f"Procedure {name} executed successfully.")
        except Error as e:
            messagebox.showerror("DB Error", f"Procedure failed: {e}")


# -------------------- MAIN --------------------
def main():
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
