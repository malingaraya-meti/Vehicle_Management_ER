from dataclasses import dataclass, field
from typing import Optional, List
import mysql.connector
from mysql.connector import Error

@dataclass
class Payment:
    payment_id: Optional[int] = field(default=None)
    sale_id: int
    amount: float
    payment_mode: str
    payment_status: str
    payment_method: Optional[str] = field(default=None)
    loan: Optional[str] = field(default=None)
    cash: Optional[float] = field(default=None)

    @staticmethod
    def create_payment(connection: mysql.connector.connection, payment: 'Payment') -> bool:
        try:
            cursor = connection.cursor()
            sql = """INSERT INTO Payment (Sale_ID, Amount, Payment_Mode, Payment_Status, Payment_Method, Loan, Cash)
                     VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (payment.sale_id, payment.amount, payment.payment_mode, payment.payment_status,
                                 payment.payment_method, payment.loan, payment.cash))
            connection.commit()
            return True
        except Error as e:
            print(f"Error creating payment: {e}")
            return False

    @staticmethod
    def get_payments_by_sale(connection: mysql.connector.connection, sale_id: int) -> List['Payment']:
        payments = []
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Payment WHERE Sale_ID = %s", (sale_id,))
            rows = cursor.fetchall()
            for row in rows:
                payments.append(Payment(payment_id=row[0], sale_id=row[1], amount=row[2],
                                        payment_mode=row[3], payment_status=row[4],
                                        payment_method=row[5], loan=row[6], cash=row[7]))
        except Error as e:
            print(f"Error fetching payments: {e}")
        return payments

    @staticmethod
    def update_payment(connection: mysql.connector.connection, payment: 'Payment') -> bool:
        try:
            cursor = connection.cursor()
            sql = """UPDATE Payment SET Amount = %s, Payment_Mode = %s, Payment_Status = %s,
                     Payment_Method = %s, Loan = %s, Cash = %s WHERE Payment_ID = %s"""
            cursor.execute(sql, (payment.amount, payment.payment_mode, payment.payment_status,
                                 payment.payment_method, payment.loan, payment.cash, payment.payment_id))
            connection.commit()
            return True
        except Error as e:
            print(f"Error updating payment: {e}")
            return False

    @staticmethod
    def delete_payment(connection: mysql.connector.connection, payment_id: int) -> bool:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Payment WHERE Payment_ID = %s", (payment_id,))
            connection.commit()
            return True
        except Error as e:
            print(f"Error deleting payment: {e}")
            return False