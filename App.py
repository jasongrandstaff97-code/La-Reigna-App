import streamlit as st
from streamlit_pills import pills
import time
import uuid
from datetime import datetime

# ==============================================================================
# 1. GLOBAL CONFIGURATION & BRANDING (THE "MOAT")
# ==============================================================================
# This section defines the entire visual identity. 
# Changing this dictionary allows you to clone the OS for any new client.
SYSTEM_CONFIG = {
    "app_name": "La Reina Margaritas",
    "version": "3.0.4-PRO",
    "branding": {
        "gold": "#D4AF37",
        "poblano": "#4CBB17",
        "black": "#000000",
        "card_bg": "#121212",
        "text_main": "#FFFFFF",
        "text_dim": "#888888"
    },
    "paths": {
        "logo": "logo.png"  # Ensure this file is in your GitHub folder
    }
}

# ==============================================================================
# 2. MASTER MENU INFRASTRUCTURE
# ==============================================================================
# A robust data structure that maps categories to specific product objects.
MENU_DB = {
    "Tacos": [
        {"id": "t1", "name": "Street Taco", "desc": "Fresh cilantro, onion, lime", "price": 3.50, "icon": "🌮"},
        {"id": "t2", "name": "Al Pastor", "desc": "Marinated pork, pineapple, spice", "price": 4.00, "icon": "🍍"},
        {"id": "t3", "name": "Barbacoa", "desc": "Slow-braised beef, tender & juicy", "price": 4.50, "icon": "🥩"},
        {"id": "t4", "name": "Carnitas", "desc": "Crispy pork, pickled onion", "price": 4.00, "icon": "🐷"}
    ],
    "Entrees": [
        {"id": "e1", "name": "Enchiladas Verdes", "desc": "3 chicken enchiladas, salsa verde", "price": 14.00, "icon": "🥘"},
        {"id": "e2", "name": "Burrito Grande", "desc": "Rice, beans, protein, smothered in queso", "price": 12.00, "icon": "🌯"},
        {"id": "e3", "name": "Fajita Platter", "desc": "Sizzling steak or chicken, peppers", "price": 18.00, "icon": "🔥"},
        {"id": "e4", "name": "Chimichanga", "desc": "Deep-fried burrito, cheese sauce", "price": 13.50, "icon": "📦"}
    ],
    "Appetizers": [
        {"id": "a1", "name": "Guacamole & Chips", "desc": "Hand-smashed daily", "price": 8.00, "icon": "🥑"},
        {"id": "a2", "name": "Queso Fundido", "desc": "Melted cheese with spicy chorizo", "price": 9.00, "icon": "🧀"},
        {"id": "a3", "name": "Street Corn", "desc": "Elote with cotija and tajin", "price": 6.00, "icon": "🌽"}
    ],
    "Drinks": [
        {"id": "d1", "name": "House Margarita", "desc": "Gold tequila, fresh lime, agave", "price": 9.00, "icon": "🍹"},
        {"id": "d2", "name": "Paloma", "desc": "Grapefruit, lime, tequila, soda", "price": 10.00, "icon": "🍊"},
        {"id": "d3", "name": "Agua Fresca", "desc": "Watermelon or Pineapple fresh", "price": 4.00, "icon": "🥤"},
        {"id": "d4", "name": "Jarritos", "desc": "Mexican soda, various flavors", "price": 3.00, "icon": "🍾"}
    ]
}

# ==============================================================================
# 3. ADVANCED STYLING (THE PSYCHOLOGICAL UI)
# ==============================================================================
def apply_custom_styles():
    st.markdown(f"""
        <style>
        /* Base Environment */
        .stApp {{
            background-color: {SYSTEM_CONFIG['branding']['black']};
            color: {SYSTEM_CONFIG['branding']['text_main']};
        }}
        
        /* The "Poblano" Status Bar */
        .status-bar {{
            background-color: {SYSTEM_CONFIG['branding']['poblano']};
            color: black;
            padding: 10px;
            text-align: center;
            font-weight: 900;
            border-radius: 6px;
            margin-bottom: 25px;
            letter-spacing: 1px;
            box-shadow: 0px 4px 15px rgba(76, 187, 23, 0.3);
        }}

        /* Mega-Pill Menu Cards */
        .menu-card {{
            background-color: {SYSTEM_CONFIG['branding']['card_bg']};
            border: 1px solid #333333;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 15px;
            transition: all 0.3s ease;
        }}
        .menu-card:hover {{
            border-color: {SYSTEM_CONFIG['branding']['gold']};
            transform: translateY(-3px);
        }}

        /* Gold Branding Elements */
        h1, h2, h3 {{
            color: {SYSTEM_CONFIG['branding']['gold']} !important;
        }}
        .price-text {{
            color: {SYSTEM_CONFIG['branding']['gold']};
            font-size: 1.4rem;
            font-weight: bold;
        }}
        
        /* Sidebar Cart Styling */
        [data-testid="stSidebar"] {{
            background-color: #0A0A0A;
            border-left: 1px solid #222;
        }}
        
        /* Buttons */
        .stButton>button {{
            background-color: {SYSTEM_CONFIG['branding']['gold']};
            color: black !important;
            border-radius: 8px;
            font-weight: bold;
            border: none;
            width: 100%;
        }}
        </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 4. SYSTEM STATE & LOGIC ENGINE
# ==============================================================================
class SystemState:
    @staticmethod
    def initialize():
        if 'cart' not in st.session_state: st.session_state.cart = []
        if 'orders' not in st.session_state: st.session_state.orders = []
        if 'phone' not in st.session_state: st.session_state.phone = None
        if 'view' not in st.session_state: st.session_state.view = "Customer"
        if 'points' not in st.session_state: st.session_state.points = 0

    @staticmethod
    def add_to_cart(item):
        st.session_state.cart.append(item)
        st.toast(f"Added {item['name']} 🌮")

    @staticmethod
    def submit_order():
        if not st.session_state.cart:
            return
        order_id = str(uuid.uuid4())[:5].upper()
        new_order = {
            "id": order_id,
            "items": st.session_state.cart,
            "time": datetime.now().strftime("%H:%M:%S"),
            "phone": st.session_state.phone
        }
        st.session_state.orders.append(new_order)
        # Point Calculation: $1 = 1pt
        subtotal = sum(item['price'] for item in st.session_state.cart)
        st.session_state.points += int(subtotal)
        st.session_state.cart = []
        # Sound trigger placeholder
        st.success(f"Order #{order_id} sent to kitchen!")
        st.balloons()

# ==============================================================================
# 5. UI COMPONENTS (MODULAR VIEWS)
# ==============================================================================

def render_branding_header():
    try:
        st.image(SYSTEM_CONFIG["paths"]["logo"], width=300)
    except:
        st.markdown(f"<h1>{SYSTEM_CONFIG['app_name']}</h1>", unsafe_allow_html=True)
        st.caption("AUTHENTIC MEXICAN KITCHEN & CANTINA")
    
    st.markdown('<div class="status-bar">STATUS: POBLANO 🫑 ONLINE</div>', unsafe_allow_html=True)

def render_customer_ui():
    render_branding_header()
    
    # Navigation Switchboard
    tabs = list(MENU_DB.keys()) + ["Rewards 👑"]
    selected = pills("", tabs, index=0, label_visibility="collapsed")
    
    st.write("---")
    
    if "Rewards" in selected:
        render_rewards_center()
    else:
        # Dynamic Menu Generator
        items = MENU_DB.get(selected, [])
        for item in items:
            with st.container():
                col_info, col_action = st.columns([4, 1])
                with col_info:
                    st.markdown(f"""
                        <div class="menu-card">
                            <h3>{item['icon']} {item['name']}</h3>
                            <p style="color:#888;">{item['desc']}</p>
                            <span class="price-text">${item['price']:.2f}</span>
                        </div>
                    """, unsafe_allow_html=True)
                with col_action:
                    st.write("") # Spacer
                    st.write("")
                    if st.button("➕", key=item['id']):
                        SystemState.add_to_cart(item)

def render_rewards_center():
    st.title("Loyalty & Rewards")
    st.write("### You do anything. You earn everything.")
    
    col_input, col_stats = st.columns(2)
    
    with col_input:
        st.markdown("#### Link Your Phone")
        phone = st.text_input("Mobile Number", placeholder="417-555-5555", 
                              value=st.session_state.phone if st.session_state.phone else "")
        if st.button("Access My Kingdom"):
            if len(phone) >= 10:
                st.session_state.phone = phone
                st.success("Synchronized. Welcome to the inner circle.")
            else:
                st.error("Please enter a valid 10-digit number.")
    
    with col_stats:
        if st.session_state.phone:
            st.metric("Total Points", f"{st.session_state.points} PTS")
            progress = (st.session_state.points % 50) / 50
            st.write(f"**Next Reward:** {50 - (st.session_state.points % 50)} points away")
            st.progress(progress)
            st.caption("50 Points = 1 Free Entree or Margarita")

def render_kds_ui():
    st.title("Kitchen Display System (KDS)")
    st.markdown('<div class="status-bar" style="background-color: #D4AF37;">STAFF VIEW ONLY</div>', unsafe_allow_html=True)
    
    if not st.session_state.orders:
        st.info("The kitchen is clear. Waiting for orders... 🔥")
        return

    # Grid layout for tickets
    cols = st.columns(3)
    for idx, order in enumerate(st.session_state.orders):
        with cols[idx % 3]:
            with st.expander(f"ORDER #{order['id']} - {order['time']}", expanded=True):
                for item in order['items']:
                    st.write(f"• **{item['name']}**")
                st.write("---")
                if st.button(f"DONE (Order {order['id']})", key=f"bump_{order['id']}"):
                    st.session_state.orders.pop(idx)
                    st.rerun()

# ==============================================================================
# 6. MAIN EXECUTION (THE BOOTLOADER)
# ==============================================================================
def main():
    SystemState.initialize()
    apply_custom_styles()
    
    # Sidebar Control Panel
    with st.sidebar:
        st.markdown(f"## System v{SYSTEM_CONFIG['version']}")
        mode = st.radio("Access Level", ["Ordering App", "Staff (KDS)", "Admin Metrics"])
        
        if mode == "Ordering App":
            st.write("---")
            st.header("Your Cart 🛒")
            if not st.session_state.cart:
                st.write("Your cart is empty.")
            else:
                for idx, item in enumerate(st.session_state.cart):
                    st.write(f"{item['name']} - ${item['price']:.2f}")
                
                total = sum(i['price'] for i in st.session_state.cart)
                st.markdown(f"### Total: **${total:.2f}**")
                
                if st.button("SEND TO KITCHEN", type="primary"):
                    SystemState.submit_order()

    # Route to selected view
    if mode == "Ordering App":
        render_customer_ui()
    elif mode == "Staff (KDS)":
        render_kds_ui()
    else:
        st.title("Admin Data Lake")
        st.write("Real-time revenue and behavioral tracking metrics under development.")

if __name__ == "__main__":
    main()
