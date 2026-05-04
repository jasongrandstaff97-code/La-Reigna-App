import streamlit as st
import random
import time
from database_engine import SystemConfig, sync_user_data, update_user_points, log_transaction, get_sales_data

# --- 1. SYSTEM INITIALIZATION ---
st.set_page_config(
    page_title=f"{SystemConfig.RESTAURANT_NAME} POS",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def inject_industrial_styles():
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;800&display=swap');
        
        /* Core Dark Engine */
        .stApp {{ background-color: #000000; color: #FFFFFF; font-family: 'JetBrains Mono', monospace; }}
        [data-testid="stHeader"] {{ background: rgba(0,0,0,0); }}
        
        /* The 6-Tab Mega-Pill Grid (2x3) */
        .mega-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 30px;
        }}
        
        /* Industrial Pill Styling */
        .stButton>button {{
            width: 100%;
            height: 75px !important;
            border-radius: 12px !important;
            border: 2px solid #333 !important;
            background-color: #1A1A1A !important;
            color: #D4AF37 !important;
            font-weight: 800 !important;
            text-transform: uppercase !important;
            font-size: 1rem !important;
            transition: all 0.2s ease-in-out;
        }}
        
        .stButton>button:hover {{
            border-color: #D4AF37 !important;
            transform: scale(1.02);
        }}

        /* Special Pill States */
        .active-red > div > button {{ background-color: #D32F2F !important; color: white !important; border: none !important; }}
        .active-reserva > div > button {{ background-color: #4A0404 !important; color: #D4AF37 !important; border: 2px solid #D4AF37 !important; }}
        .locked-pill > div > button {{ opacity: 0.5 !important; color: #444 !important; }}

        /* Current Order Manifest */
        .manifest-header {{ color: #D4AF37; font-weight: 800; font-size: 1.6rem; border-bottom: 2px solid #333; padding-bottom: 10px; margin-top: 40px; text-transform: uppercase; }}
        .manifest-row {{ display: flex; justify-content: space-between; padding: 10px 0; color: #AAA; font-size: 1.1rem; border-bottom: 1px solid #1A1A1A; }}
        .manifest-total {{ border-top: 2px dashed #444; padding-top: 20px; margin-top: 20px; display: flex; justify-content: space-between; font-size: 1.8rem; font-weight: 800; color: #D4AF37; }}
        
        /* Payment Triggers */
        .apple-pay-btn > div > button {{ background-color: #FFFFFF !important; color: #000000 !important; border: none !important; height: 60px !important; }}
        .google-pay-btn > div > button {{ background-color: #4285F4 !important; color: #FFFFFF !important; border: none !important; height: 60px !important; }}

        /* KDS Display Styles */
        .kds-card {{ background-color: #111; border-left: 10px solid #D4AF37; padding: 25px; border-radius: 8px; margin-bottom: 25px; min-height: 250px; }}
        .kds-badge {{ padding: 6px 15px; border-radius: 4px; font-weight: 800; font-size: 14px; text-transform: uppercase; margin-bottom: 15px; display: inline-block; }}
        .kds-dine-in {{ background-color: #2E7D32; color: white; }}
        .kds-to-go {{ background-color: #D32F2F; color: white; }}
        
        /* Utility */
        footer {{visibility: hidden;}} #MainMenu {{visibility: hidden;}}
        </style>
    """, unsafe_allow_html=True)

# --- 2. DATA LAYER ---
def load_menu():
    return {
        "Lunch Specials": [
            {"id": "L1", "name": "Speedy Gonzales", "desc": "One taco, one enchilada, choice of rice or beans.", "price": 7.99},
            {"id": "L2", "name": "Lunch Fajitas", "desc": "Steak or Chicken, peppers, onions, rice, beans.", "price": 10.50}
        ],
        "Appetizers": [
            {"id": "A1", "name": "Queso Blanco", "desc": "Creamy melted white cheese with jalapeño hints.", "price": 5.99},
            {"id": "A2", "name": "Fresh Guacamole", "desc": "Avocado, lime, cilantro, tomatoes. Made daily.", "price": 7.50}
        ],
        "Tacos": [
            {"id": "T1", "name": "Street Taco (Asada)", "desc": "Steak, cilantro, onion, lime on corn.", "price": 3.50},
            {"id": "T2", "name": "Al Pastor", "desc": "Marinated pork, pineapple, cilantro, onion.", "price": 3.75}
        ],
        "Entrees": [
            {"id": "E1", "name": "Burrito California", "desc": "Steak, fries, cheese, guac, sour cream inside.", "price": 14.50},
            {"id": "E2", "name": "Carne Asada", "desc": "Grilled steak, grilled onions, rice, beans.", "price": 17.50}
        ],
        "Drinks": [
            {"id": "D1", "name": "La Reina House Rita", "desc": "Gold tequila, fresh lime, agave.", "price": 8.99},
            {"id": "D2", "name": "Modelo Especial", "desc": "Draft or Bottle. Chilled with lime.", "price": 5.00}
        ],
        "La Reserva": [
            {"id": "R1", "name": "Wagyu Birria Tacos", "desc": "Elite Wagyu beef, consome, Oaxacan cheese.", "price": 24.00},
            {"id": "R2", "name": "Premium Reposado Flight", "desc": "Three rare tequilas, hand-selected.", "price": 35.00}
        ]
    }

# --- 3. STATE & ROUTING ---
def init_session():
    if 'view_mode' not in st.session_state: st.session_state.view_mode = "login"
    if 'cart' not in st.session_state: st.session_state.cart = []
    if 'current_cat' not in st.session_state: st.session_state.current_cat = "Lunch Specials"
    if 'order_type' not in st.session_state: st.session_state.order_type = "DINE-IN 🍽️"

# --- 4. THE PORTAL (FIBONACCI LOGIN) ---
def render_login():
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.image(SystemConfig.LOGO_PATH, use_container_width=True)
        phone = st.text_input("PHONE", placeholder="000-000-0000", label_visibility="collapsed")
        
        if phone:
            # The Fibonacci Sequence (First 10 digits)
            if phone == "0112358132":
                st.session_state.view_mode = "kds"
                st.rerun()
            elif len(phone) >= 10:
                sync_user_data(phone)
                st.session_state.view_mode = "customer"
                st.session_state.phone_number = phone
                st.rerun()

# --- 5. THE CUSTOMER CONCIERGE ---
def render_customer_ui():
    # A. Loyalty Dashboard
    pts = st.session_state.reward_points
    if pts < 500: tier, color, target, nxt = "POBLANO 🫑", "#7FFF00", 500, "JALAPEÑO"
    elif pts < 5000: tier, color, target, nxt = "JALAPEÑO 🌶️", "#FFA500", 5000, "HABANERO"
    else: tier, color, target, nxt = "HABANERO 🔥", "#D4AF37", 10000, "MAX HEAT"
    
    progress = min(int((pts/target)*100), 100)
    
    st.markdown(f"""
        <div style="border: 2px solid {color}; padding: 15px; border-radius: 10px; margin-bottom: 25px;">
            <div style="display: flex; justify-content: space-between; font-weight: 800; color: {color}; text-transform: uppercase;">
                <span>{tier}</span><span>{pts} / {target} PTS</span>
            </div>
            <div style="width: 100%; background: #222; height: 6px; border-radius: 3px; margin: 8px 0;">
                <div style="width: {progress}%; background: {color}; height: 100%; border-radius: 3px;"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # B. The 6-Tab Mega-Pill Grid
    categories = list(load_menu().keys())
    cols = st.columns(2)
    
    for i, cat in enumerate(categories):
        with cols[i % 2]:
            c_style = ""
            if cat == st.session_state.current_cat: c_style = "active-red"
            if cat == "La Reserva":
                if pts < 5000:
                    st.markdown('<div class="locked-pill">', unsafe_allow_html=True)
                    st.button(f"🔒 {cat}", disabled=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    continue
                c_style = "active-reserva"
            
            st.markdown(f'<div class="{c_style}">', unsafe_allow_html=True)
            if st.button(cat, key=f"tab_{cat}"):
                st.session_state.current_cat = cat
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # C. Item Catalog
    st.markdown(f"## {st.session_state.current_cat.upper()}")
    items = load_menu()[st.session_state.current_cat]
    i_cols = st.columns(2)
    for idx, item in enumerate(items):
        with i_cols[idx % 2]:
            st.markdown(f"""
                <div style="background: #111; padding: 20px; border-radius: 10px; border: 1px solid #333; margin-bottom: 10px; min-height: 120px;">
                    <div style="color: #D4AF37; font-weight: 800; font-size: 1.2rem;">{item['name']}</div>
                    <div style="color: #666; font-size: 0.9rem;">{item['desc']}</div>
                    <div style="color: #FFF; font-weight: 700; margin-top: 10px;">${item['price']:.2f}</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"+ ADD {item['name']}", key=f"add_{item['id']}"):
                st.session_state.cart.append(item)
                st.toast(f"Added {item['name']}")

    # D. CURRENT ORDER (CHECKOUT)
    st.markdown('<div class="manifest-header">CURRENT ORDER</div>', unsafe_allow_html=True)
    if not st.session_state.cart:
        st.write("MANIFEST EMPTY.")
    else:
        subtotal = 0
        for item in st.session_state.cart:
            st.markdown(f'<div class="manifest-row"><span>{item["name"]}</span><span>${item["price"]:.2f}</span></div>', unsafe_allow_html=True)
            subtotal += item["price"]
        
        st.markdown(f'<div class="manifest-total"><span>TOTAL</span><span>${subtotal:.2f}</span></div>', unsafe_allow_html=True)
        
        st.write("ORDER DESTINATION")
        st.session_state.order_type = st.radio("DEST", ["DINE-IN 🍽️", "TO-GO 🛍️"], horizontal=True, label_visibility="collapsed")

        # Payment Triggers
        st.markdown("<br>", unsafe_allow_html=True)
        pay_col1, pay_col2 = st.columns(2)
        with pay_col1: 
            st.markdown('<div class="apple-pay-btn">', unsafe_allow_html=True)
            if st.button(" Pay", key="ap"): pass
            st.markdown('</div>', unsafe_allow_html=True)
        with pay_col2:
            st.markdown('<div class="google-pay-btn">', unsafe_allow_html=True)
            if st.button("G Pay", key="gp"): pass
            st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("SECURE CHECKOUT (MFA)", use_container_width=True):
            st.success("MFA CHALLENGE SENT.")

# --- 6. THE KDS MANIFEST ---
def render_kds():
    st.markdown("<h1 style='color:#D4AF37;'>👨‍🍳 KDS COMMAND CENTER</h1>", unsafe_allow_html=True)
    st.markdown("---")
    k_cols = st.columns(3)
    # Mock data for demonstration
    mock_orders = [
        {"id": "501", "type": "DINE-IN 🍽️", "items": ["2x Street Tacos", "1x Queso Blanco"]},
        {"id": "502", "type": "TO-GO 🛍️", "items": ["1x Burrito California", "1x Large Rita"]}
    ]
    for i, order in enumerate(mock_orders):
        with k_cols[i % 3]:
            badge_class = "kds-dine-in" if "DINE-IN" in order["type"] else "kds-to-go"
            st.markdown(f"""
                <div class="kds-card">
                    <div class="kds-badge {badge_class}">{order['type']}</div>
                    <div style="font-size: 1.8rem; font-weight: 800; color: #D4AF37; margin-bottom: 10px;">ORDER #{order['id']}</div>
                    <div style="font-size: 1.3rem; color: #FFF; line-height: 1.6;">
                        {'<br>'.join(order['items'])}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("MARK COMPLETE", key=f"comp_{order['id']}"):
                st.toast(f"Order #{order['id']} Cleared.")

# --- 7. RUNTIME ---
def main():
    init_session()
    inject_industrial_styles()
    
    if st.session_state.view_mode == "login":
        render_login()
    elif st.session_state.view_mode == "kds":
        render_kds()
    elif st.session_state.view_mode == "customer":
        render_customer_ui()

if __name__ == "__main__":
    main()
