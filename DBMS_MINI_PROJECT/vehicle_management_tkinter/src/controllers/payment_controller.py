from tkinter import messagebox
from src.db.repository import PaymentRepository
from src.models.payment import Payment

class PaymentController:
    def __init__(self):
        self.repository = PaymentRepository()

    def create_payment(self, payment_data):
        payment = Payment(**payment_data)
        success, error = self.repository.insert(payment)
        if not success:
            messagebox.showerror("Error", f"Failed to create payment: {error}")
        else:
            messagebox.showinfo("Success", "Payment created successfully")

    def update_payment(self, payment_id, payment_data):
        payment = Payment(**payment_data)
        payment.id = payment_id
        success, error = self.repository.update(payment)
        if not success:
            messagebox.showerror("Error", f"Failed to update payment: {error}")
        else:
            messagebox.showinfo("Success", "Payment updated successfully")

    def delete_payment(self, payment_id):
        success, error = self.repository.delete(payment_id)
        if not success:
            messagebox.showerror("Error", f"Failed to delete payment: {error}")
        else:
            messagebox.showinfo("Success", "Payment deleted successfully")

    def get_payment(self, payment_id):
        payment = self.repository.get(payment_id)
        if payment is None:
            messagebox.showwarning("Not Found", "Payment not found")
        return payment

    def get_all_payments(self):
        return self.repository.get_all()