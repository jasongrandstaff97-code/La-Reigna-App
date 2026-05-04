import streamlit as st
import random
from database_engine import SystemConfig, sync_user_data, update_user_points, log_transaction, get_sales_data
from streamlit_autorefresh import st_autorefresh

# --- 1. ARCHITECTURAL CONFIG ---
st.set_page_config(
    page_title=f"{SystemConfig.RESTAURANT_NAME} OS",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def inject_styles():
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;800&display=swap');
        
        /* Base Engine */
        .stApp {{ background-color: #000000; color: #FFFFFF; font-family: 'JetBrains Mono', monospace; }}
        [data-testid="stHeader"] {{ background: rgba(0,0,0,0); }}
        
        /* Status Bar Glow */
        .status-engine {{ 
            background: linear-gradient(90deg, #111, #1a1a1a); 
            border: 1px solid #333; 
            padding: 20px; border-radius: 12px; margin: 20px 0; 
            box-shadow: 0 0 20px rgba(212, 175, 55, 0.05);
        }}
        
        /* 6-Tab Mega-Grid */
        .stButton>button {{
            width: 100%; height: 75px !important;
            background-color: #111 !important; border: 2px solid #333 !important;
            color: {SystemConfig.PRIMARY_COLOR} !important; border-radius: 12px !important;
            font-weight: 800 !important; text-transform: uppercase; transition: 0.2s;
        }}
        .stButton>button:hover {{ border-color: {SystemConfig.PRIMARY_COLOR} !important; background: #1a1a1a !important; transform: translateY(-2px); }}

        /* Pill Special States */
        .active-tab > div > button {{ background-color: #D32F2F !important; color: white !important; border: none !important; }}
        .active-reserva > div > button {{ background-color: #4A0404 !important; color: {SystemConfig.PRIMARY_COLOR} !important; border: 2px solid {SystemConfig.PRIMARY_COLOR} !important; }}

        /* Menu & Manifest */
        .menu-card {{ background: rgba(255, 255, 255, 0.03); border: 1px solid #333; border-radius: 12px; padding: 20px; margin-bottom: 15px; min-height: 160px; display: flex; flex-direction: column; justify-content: space-between; }}
        .manifest-container {{ background: #0a0a0a; border: 1px solid #333; border-radius: 12px; padding: 25px; margin-top: 40px; }}
        .manifest-header {{ color: {SystemConfig.PRIMARY_COLOR}; font-weight: 800; font-size: 1.5rem; border-bottom: 1px solid #222; padding-bottom: 10px; margin-bottom: 15px; }}
        .receipt-row {{ display: flex; justify-content: space-between; padding: 8px 0; color: #888; font-size: 1.1rem; }}
        .manifest-total {{ border-top: 2px dashed #333; padding-top: 15px; margin-top: 15px; font-size: 26px; font-weight: 800; color: {SystemConfig.PRIMARY_COLOR}; display: flex; justify-content: space-between; }}
        
        /* Payments */
        .apple-pay-btn > div > button {{ background-color: #FFFFFF !important; color: #000 !important; border: none !important; height: 60px !important; }}
        .google-pay-btn > div > button {{ background-color: #4285F4 !important; color: #FFF !important; border: none !important; height: 60px !important; }}

        /* KDS Display */
        .kds-card {{ background-color: #080808; border-left: 10px solid {SystemConfig.PRIMARY_COLOR}; padding: 30px; border-radius: 8px; margin-bottom: 20px; }}
        .kds-badge {{ padding: 6px 15px; border-radius: 4px; font-weight: 800; font-size: 14px; text-transform: uppercase; margin-bottom: 15px; display: inline-block; }}
        .kds-dine-in {{ background-color: #2E7D32; color: white; }}
        .kds-to-go {{ background-color: #D32F2F; color: white; }}

        footer {{visibility: hidden;}} #MainMenu {{visibility: hidden;}}
        </style>
    """, unsafe_allow_html=True)

# --- 2. THE MASTER MENU ---
def get_menu():
    return {
        "Lunch Specials": [
            {"id": "L1", "name": "Speedy Gonzales", "desc": "One taco, one enchilada, rice and beans.", "price": 7.99},
            {"id": "L2", "name": "Lunch Fajitas", "desc": "Steak or Chicken, peppers, onions, tortillas.", "price": 10.50}
        ],
        "Appetizers": [
            {"id": "A1", "name": "Queso Blanco", "desc": "Melted white cheese with a kick of jalapeño.", "price": 5.99},
            {"id": "A2", "name": "Fresh Guacamole", "desc": "Hand-smashed daily. Lime and cilantro.", "price": 7.50}
        ],
        "Tacos": [
            {"id": "T1", "name": "Street Taco", "desc": "Asada, cilantro, onion on corn tortillas.", "price": 3.50},
            {"id": "T2", "name": "Al Pastor", "desc": "Marinated pork, pineapple, and onions.", "price": 3.75}
        ],
        "Entrees": [
            {"id": "E1", "name": "Burrito California", "desc": "Steak, fries, cheese, and guac inside.", "price": 14.50},
            {"id": "E2", "name": "Carne Asada", "desc": "Thinly sliced grilled steak and onions.", "price": 17.50}
        ],
        "Drinks": [
            {"id": "D1", "name": "La Reina Rita", "desc": "House gold tequila, fresh lime, agave.", "price": 8.99},
            {"id": "D2", "name": "Modelo Especial", "desc": "Ice cold draft or bottle with lime.", "price": 5.00}
        ],
        "La Reserva": [
            {"id": "R1", "name": "Wagyu Birria", "desc": "Elite Wagyu beef and consome.", "price": 24.00},
            {"id": "R2", "name": "The Queen's Flight", "desc": "Three rare aged reposados.", "price": 35.00}
        ]
    }

# --- 3. SESSION CONTROL ---
def init_session():
    if 'view_mode' not in st.session_state: st.session_state.view_mode = "login"
    if 'cart' not in st.session_state: st.session_state.cart = []
    if 'current_cat' not in st.session_state: st.session_state.current_cat = "Lunch Specials"
    if 'is_admin' not in st.session_state: st.session_state.is_admin = False

def get_tier(pts):
    if pts < 500: return "POBLANO 🫑", 500, "JALAPEÑO", "#7FFF00"
    elif pts < 5000: return "JALAPEÑO 🌶️", 5000, "HABANERO", "#FFA500"
    else: return "HABANERO 🔥", 10000, "EL REY", "#D4AF37"

# --- 4. THE PORTAL (SANITZED) ---
def render_login():
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.image(SystemConfig.LOGO_PATH, use_container_width=True)
        st.markdown("<h4 style='text-align:center; color:#888;'>WELCOME. ENTER YOUR PHONE NUMBER.</h4>", unsafe_allow_html=True)
        
        phone_input = st.text_input("PHONE", placeholder="417-000-0000", label_visibility="collapsed")
        
        if phone_input:
            # SANITIZATION: Remove all formatting for the check
            clean_key = "".join(filter(str.isdigit, phone_input))
            
            # Fibonacci Portal: 0112358132
            if clean_key == "0112358132":
                st.session_state.view_mode = "kds"
                st.rerun()
            
            elif len(clean_key) >= 10:
                if clean_key == SystemConfig.ADMIN_CODE: st.session_state.is_admin = True
                sync_user_data(clean_key)
                st.session_state.view_mode = "customer"
                st.session_state.phone_number = clean_key
                st.rerun()

# --- 5. THE CUSTOMER INTERFACE ---
def render_customer_os():
    _, logo_col, _ = st.columns([1, 2, 1])
    with logo_col: st.image(SystemConfig.LOGO_PATH, use_container_width=True)

    # Status Engine
    pts = st.session_state.get('reward_points', 0)
    tier, target, next_t, t_color = get_tier(pts)
    progress = min(int((pts / target) * 100), 100)

    st.markdown(f"""
        <div class="status-engine" style="border-color: {t_color};">
            <div class="status-header">
                <span style="color: {t_color};">{tier}</span>
                <span>{pts} / {target} PTS</span>
            </div>
            <div style="width: 100%; background: #222; height: 8px; border-radius: 4px; overflow: hidden; margin-top:10px;">
                <div style="width: {progress}%; background: {t_color}; height: 100%;"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 6-Tab Grid
    menu = get_menu()
    categories = list(menu.keys())
    t1, t2 = st.columns(2)
    
    for i, cat in enumerate(categories):
        target_col = t1 if i % 2 == 0 else t2
        with target_col:
            style_class = ""
            if cat == st.session_state.current_cat: style_class = "active-tab"
            if cat == "La Reserva":
                if pts < 5000:
                    st.button(f"🔒 {cat}", disabled=True)
                    continue
                style_class = "active-reserva"
            
            st.markdown(f'<div class="{style_class}">', unsafe_allow_html=True)
            if st.button(cat, key=f"tab_{cat}"):
                st.session_state.current_cat = cat
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # Menu Display
    st.markdown(f"### {st.session_state.current_cat.upper()}")
    items = menu[st.session_state.current_cat]
    cols = st.columns(2)
    for idx, item in enumerate(items):
        with cols[idx % 2]:
            st.markdown(f"""<div class="menu-card"><div><div class="item-title">{item['name']}</div><div class="item-desc">{item['desc']}</div></div><div class="price-tag">${item['price']:.2f}</div></div>""", unsafe_allow_html=True)
            if st.button(f"+ ADD {item['name']}", key=f"add_{item['id']}"):
                st.session_state.cart.append(item)
                st.toast(f"Added {item['name']}")
                st.rerun()

    # Current Order Manifest
    st.markdown('<div class="manifest-container">', unsafe_allow_html=True)
    st.markdown('<div class="manifest-header">CURRENT ORDER</div>', unsafe_allow_html=True)
    if not st.session_state.cart:
        st.write("YOUR SELECTIONS WILL APPEAR HERE.")
    else:
        subtotal = sum(i['price'] for i in st.session_state.cart)
        for item in st.session_state.cart:
            st.markdown(f'<div class="receipt-row"><span>{item["name"]}</span><span>${item["price"]:.2f}</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="manifest-total"><span>TOTAL</span><span>${subtotal:.2f}</span></div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        p1, p2 = st.columns(2)
        with p1: 
            st.markdown('<div class="apple-pay-btn">', unsafe_allow_html=True)
            st.button(" Pay", key="ap")
            st.markdown('</div>', unsafe_allow_html=True)
        with p2:
            st.markdown('<div class="google-pay-btn">', unsafe_allow_html=True)
            st.button("G Pay", key="gp")
            st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("CREDIT / DEBIT (MFA SECURED)", use_container_width=True):
            st.success("Verification code sent.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 6. THE KDS STATION ---
def render_kds():
    st_autorefresh(interval=15000, key="kds_sync")
    st.markdown(f"<h1 style='color:{SystemConfig.PRIMARY_COLOR};'>👨‍🍳 KITCHEN DATA SCREEN</h1>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#333;'>", unsafe_allow_html=True)
    
    k1, k2, k3 = st.columns(3)
    # Placeholder for live orders
    mock = [{"id": "110", "type": "TO-GO 🛍️", "items": ["3x Street Tacos", "1x Queso"]}]
    for i, order in enumerate(mock):
        with [k1, k2, k3][i % 3]:
            b_class = "kds-dine-in" if "DINE-IN" in order["type"] else "kds-to-go"
            st.markdown(f'<div class="kds-card"><div class="kds-badge {b_class}">{order["type"]}</div><div style="font-size:1.8rem; font-weight:800; color:{SystemConfig.PRIMARY_COLOR};">#{order["id"]}</div><div style="font-size:1.3rem; color:#ccc; margin-top:15px;">{"<br>".join(order["items"])}</div></div>', unsafe_allow_html=True)
            if st.button("COMPLETE", key=f"k_{order['id']}"): st.toast("Ticket Cleared.")

# --- 7. RUNTIME ---
def render_main_os():
    if st.session_state.is_admin:
        st.title("EXECUTIVE DASHBOARD")
        if st.button("LOGOUT"): st.session_state.is_admin = False; st.rerun()
    else: render_customer_os()

def main():
    init_session()
    inject_styles()
    if st.session_state.view_mode == "login": render_login()
    elif st.session_state.view_mode == "kds": render_kds()
    else: render_main_os()

if __name__ == "__main__":
    main()
