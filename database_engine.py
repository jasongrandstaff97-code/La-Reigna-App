# database_engine.py

class SystemConfig:
    RESTAURANT_NAME = "La Reina Margaritas"
    PRIMARY_COLOR = "#D4AF37"
    BG_COLOR = "#000000"
    LOGO_PATH = "logo.png"  # Make sure you have a logo.png in your folder!
    ADMIN_CODE = "9999999999"

def sync_user_data(phone):
    # In the future, this hooks into your Juskvi DB
    pass

def update_user_points(phone, points):
    pass

def log_transaction(order_id, order_type, cart, total):
    pass

def get_sales_data():
    # Mock data so the Executive Dashboard has something to display
    return [
        {"order_id": "1001", "type": "DINE-IN 🍽️", "items": ["Speedy Gonzales"], "total": 7.99, "status": "COMPLETED"},
        {"order_id": "1002", "type": "TO-GO 🛍️", "items": ["Wagyu Birria Tacos", "La Reina Rita"], "total": 32.99, "status": "PENDING"}
    ]
