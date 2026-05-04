import json
import os
import datetime
import streamlit as st

# ==========================================
# CENTRAL SYSTEM CONFIGURATION
# ==========================================
class SystemConfig:
    RESTAURANT_NAME = "La Reina"
    PRIMARY_COLOR = "#FFD700"  # Gold
    ACCENT_COLOR = "#7FFF00"   # Poblano Green
    BG_COLOR = "#000000"       # Deep Black
    LOGO_PATH = "la_reina_dark.png" 
    TAX_RATE = 0.085           # 8.5% Tax
    DB_FILE = "la_reina_db.json"      # User/Rewards Ledger
    SALES_DB = "la_reina_sales.json"  # Financial/Ticket Ledger
    ADMIN_CODE = "9999999999"         # God Mode Unlock

# ==========================================
# REWARDS & USER DATABASE OPERATIONS
# ==========================================
def load_db():
    if os.path.exists(SystemConfig.DB_FILE):
        with open(SystemConfig.DB_FILE, 'r') as f:
            return json.load(f)
    return {} 

def save_db(db_data):
    with open(SystemConfig.DB_FILE, 'w') as f:
        json.dump(db_data, f, indent=4)

def sync_user_data(phone_number):
    db = load_db()
    if phone_number not in db:
        db[phone_number] = {"points": 0, "lifetime_orders": 0}
        save_db(db)
    st.session_state.reward_points = db[phone_number]["points"]

def update_user_points(phone_number, points_to_add):
    db = load_db()
    if phone_number in db:
        db[phone_number]["points"] += points_to_add
        db[phone_number]["lifetime_orders"] += 1
        save_db(db)
        st.session_state.reward_points = db[phone_number]["points"]

# ==========================================
# FINANCIAL & KITCHEN TICKET OPERATIONS
# ==========================================
def log_transaction(order_num, order_type, cart_items, total_price):
    if os.path.exists(SystemConfig.SALES_DB):
        with open(SystemConfig.SALES_DB, 'r') as f:
            sales = json.load(f)
    else:
        sales = []
    
    new_order = {
        "order_id": order_num,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": order_type,
        "items": [item['name'] for item in cart_items],
        "total": total_price,
        "status": "PENDING"  # Flags for the KDS
    }
    
    sales.append(new_order)
    with open(SystemConfig.SALES_DB, 'w') as f:
        json.dump(sales, f, indent=4)

def get_sales_data():
    if os.path.exists(SystemConfig.SALES_DB):
        with open(SystemConfig.SALES_DB, 'r') as f:
            return json.load(f)
    return []

def bump_kitchen_ticket(order_id):
    if os.path.exists(SystemConfig.SALES_DB):
        with open(SystemConfig.SALES_DB, 'r') as f:
            sales = json.load(f)
            
        for order in sales:
            if order["order_id"] == order_id:
                order["status"] = "COMPLETED"
                break
                
        with open(SystemConfig.SALES_DB, 'w') as f:
            json.dump(sales, f, indent=4)
