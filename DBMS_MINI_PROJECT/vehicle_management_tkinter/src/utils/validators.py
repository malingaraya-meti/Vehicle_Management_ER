def is_valid_email(email):
    import re
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def is_valid_phone(phone):
    return phone.isdigit() and len(phone) in [10, 11]

def is_valid_vehicle_id(vehicle_id):
    return isinstance(vehicle_id, int) and vehicle_id > 0

def is_valid_sale_amount(amount):
    try:
        amount = float(amount)
        return amount > 0
    except ValueError:
        return False

def is_valid_payment_mode(payment_mode):
    valid_modes = ['Cash', 'Credit Card', 'Debit Card', 'Online']
    return payment_mode in valid_modes

def validate_customer_data(customer_data):
    errors = []
    if not is_valid_email(customer_data.get('email', '')):
        errors.append("Invalid email address.")
    if not is_valid_phone(customer_data.get('phone', '')):
        errors.append("Invalid phone number.")
    return errors

def validate_vehicle_data(vehicle_data):
    errors = []
    if not is_valid_vehicle_id(vehicle_data.get('vehicle_id', 0)):
        errors.append("Invalid vehicle ID.")
    return errors

def validate_sale_data(sale_data):
    errors = []
    if not is_valid_sale_amount(sale_data.get('amount', 0)):
        errors.append("Sale amount must be greater than zero.")
    if not is_valid_payment_mode(sale_data.get('payment_mode', '')):
        errors.append("Invalid payment mode.")
    return errors