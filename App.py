import streamlit as st
from streamlit_pills import pills
from streamlit_autorefresh import st_autorefresh
import random
from database_engine import SystemConfig, sync_user_data, update_user_points, log_transaction, get_sales_data

# --- SYSTEM CONFIG ---
st.set_page_config(
    page_title=f"{SystemConfig.RESTAURANT_NAME} POS",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def inject_custom_styles():
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;800&display=swap');
        
        /* Core Aesthetic */
        .stApp {{ background-color: {SystemConfig.BG_COLOR}; color: #FFFFFF; font-family: 'JetBrains Mono', monospace; }}
        
        /* THE STATUS ENGINE */
        .status-engine {{ 
            background: linear-gradient(90deg, #111, #222); 
            border: 2px solid {SystemConfig.ACCENT_COLOR}; 
            padding: 15px 20px; border-radius: 12px; margin: 20px 0; 
            box-shadow: 0 0 15px rgba(127, 255, 0, 0.1); 
        }}
        .status-header {{ display: flex; justify-content: space-between; color: {SystemConfig.ACCENT_COLOR}; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 10px; font-size: 14px; }}
        
        /* THE 6-PILL GRID (Stretched Tiles) */
        .mega-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-bottom: 25px;
        }}
        
        /* Re-styling stButton to be a "Mega-Pill" */
        .stButton>button {{
            width: 100%;
            height: 70px !important;
            background-color: #111 !important;
            border: 2px solid #333 !important;
            color: {SystemConfig.PRIMARY_COLOR} !important;
            border-radius: 12px !important;
            font-weight: 800 !important;
            text-transform: uppercase;
            transition: 0.3s;
        }}
        .stButton>button:hover {{ border-color: {SystemConfig.PRIMARY_COLOR} !important; transform: translateY(-2px); }}

        /* Category Special States */
        .active-red > div > button {{ background-color: #D32F2F !important; color: white !important; border: none !important; }}
        .active-reserva > div > button {{ background-color: #4A0404 !important; color: {SystemConfig.PRIMARY_COLOR} !important; border: 2px solid {SystemConfig.PRIMARY_COLOR} !important; }}

        /* MENU CARDS */
        .menu-card {{ background: rgba(255, 255, 255, 0.03); border: 1px solid #333; border-radius: 12px; padding: 20px; height: 180px; display: flex; flex-direction: column; justify-content: space-between; margin-bottom: 15px; }}
        .item-title {{ color: {SystemConfig.PRIMARY_COLOR}; font-size: 20px; font-weight: 800; }}
        .price-tag {{ color: {SystemConfig.PRIMARY_COLOR}; font-size: 22px; font-weight: 700; }}

        /* CURRENT ORDER MANIFEST */
        .manifest-container {{ background: #111; border: 1px solid #333; border-radius: 12px; padding: 25px; }}
        .manifest-header {{ color: {SystemConfig.PRIMARY_COLOR}; font-weight: 800; font-size: 1.5rem; border-bottom: 1px solid #333; padding-bottom: 10px; margin-bottom: 15px; text-transform: uppercase; }}
        .manifest-total {{ border-top: 2px dashed #444; padding-top: 15px; margin-top: 15px; font-size: 24px; font-weight: bold; color: {SystemConfig.PRIMARY_COLOR}; display: flex; justify-content: space-between; }}
        
        /* EXPRESS PAYMENTS */
        .apple-pay-btn > div > button {{ background-color: #FFFFFF !important; color: #000 !important; border: none !important; height: 55px !important; }}
        .google-pay-btn > div > button {{ background-color: #4285F4 !important; color: #FFF !important; border: none !important; height: 55px !important; }}

        /* KDS STATION STYLES */
        .kds-card {{ background-color: #080808; border-left: 8px solid {SystemConfig.PRIMARY_COLOR}; padding: 20px; border-radius: 8px; margin-bottom: 15px; }}
        .kds-badge {{ padding: 4px 10px; border-radius: 4px; font-weight: 800; font-size: 12px; text-transform: uppercase; margin-bottom: 10px; display: inline-block; }}
        .kds-dine-in {{ background-color: #2E7D32; color: white; }}
        .kds-to-go {{ background-color: #D32F2F; color: white; }}

        footer {{visibility: hidden;}} #MainMenu {{visibility: hidden;}}
        </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIC INITIALIZATION ---
def init_session():
    if 'view_mode' not in st.session_state: st.session_state.view_mode = "login"
    if 'cart' not in st.session_state: st.session_state.cart = []
    if 'current_cat' not in st.session_state: st.session_state.current_cat = "Lunch Specials"

def get_tier_info(pts):
    if pts < 500: return "POBLANO 🫑", 500, "JALAPEÑO 🌶️", "#7FFF00"
    elif pts < 5000: return "JALAPEÑO 🌶️", 5000, "HABANERO 🔥", "#FFA500"
    else: return "HABANERO 🔥", 10000, "EL REY 👑", "#D4AF37"

# --- 3. THE PORTAL (FIBONACCI ACCESS) ---
def render_login():
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        try: st.image(SystemConfig.LOGO_PATH, use_container_width=True)
        except: st.markdown(f"<h1 style='text-align:center; color:{SystemConfig.PRIMARY_COLOR};'>{SystemConfig.RESTAURANT_NAME}</h1>", unsafe_allow_html=True)
        
        st.markdown("<h4 style='text-align:center; color:#888; letter-spacing: 2px;'>IDENTITY VERIFICATION</h4>", unsafe_allow_html=True)
        phone_input = st.text_input("PHONE", placeholder="10-DIGIT SEQUENCE", label_visibility="collapsed")
        
        if phone_input:
            # 0, 1, 1, 2, 3, 5, 8, 13, 21 -> 0112358132
            if phone_input == "0112358132":
                st.session_state.view_mode = "kds"
                st.rerun()
            elif len(phone_input) >= 10:
                sync_user_data(phone_input)
                st.session_state.view_mode = "customer"
                st.session_state.phone_number = phone_input
                st.rerun()

# --- 4. THE CUSTOMER CONCIERGE ---
def render_customer_os():
    # Centered Logo
    _, logo_col, _ = st.columns([1, 2, 1])
    with logo_col: st.image(SystemConfig.LOGO_PATH, use_container_width=True)

    # Status Engine (Points Bar)
    pts = st.session_state.reward_points
    tier, target, next_t, t_color = get_tier_info(pts)
    progress = min(int((pts / target) * 100), 100)

    st.markdown(f"""
        <div class="status-engine" style="border-color: {t_color};">
            <div class="status-header">
                <span style="color: {t_color};">TIER: {tier}</span>
                <span style="color: #fff;">CART: {len(st.session_state.cart)} ITEMS</span>
                <span>ID: {st.session_state.phone_number}</span>
            </div>
            <div style="width: 100%; background: #222; height: 10px; border-radius: 5px; overflow: hidden; border: 1px solid #333;">
                <div style="width: {progress}%; background: {t_color}; height: 100%; box-shadow: 0 0 10px {t_color};"></div>
            </div>
            <div style="text-align: right; color: #888; font-size: 11px; font-weight: bold; margin-top: 5px;">
                {pts} / {target} PTS — <span style="color: {t_color};">{target - pts} PTS TO {next_t}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # THE 6-TAB MEGA-GRID
    menu_data = {
        "Lunch Specials": "active-red",
        "Appetizers": "",
        "Tacos": "",
        "Entrees": "",
        "Drinks": "",
        "La Reserva": "active-reserva"
    }
    
    t1, t2 = st.columns(2)
    categories = list(menu_data.keys())
    
    # Render the 2x3 grid
    for i, cat in enumerate(categories):
        target_col = t1 if i % 2 == 0 else t2
        with target_col:
            style_class = menu_data[cat] if cat == st.session_state.current_cat or cat == "La Reserva" else ""
            if cat == "La Reserva" and pts < 5000:
                st.button(f"🔒 {cat}", disabled=True)
            else:
                st.markdown(f'<div class="{style_class}">', unsafe_allow_html=True)
                if st.button(cat, key=f"btn_{cat}"):
                    st.session_state.current_cat = cat
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    # THE CATALOG
    st.markdown(f"<h2 style='color:{SystemConfig.PRIMARY_COLOR};'>{st.session_state.current_cat.upper()}</h2>", unsafe_allow_html=True)
    # (Note: In production, pull this from your master_menu dictionary)
    m1, m2 = st.columns(2)
    with m1:
        st.markdown(f"""<div class="menu-card"><div><div class="item-title">Speedy Gonzales</div><div class="item-meta">One taco, one enchilada, choice of rice or beans.</div></div><div class="price-tag">$7.99</div></div>""", unsafe_allow_html=True)
        if st.button("+ ADD SPEEDY GONZALES"):
            st.session_state.cart.append({"name": "Speedy Gonzales", "price": 7.99})
            st.rerun()

    # THE CURRENT ORDER (CHECKOUT SECTION)
    st.markdown('<div class="manifest-container">', unsafe_allow_html=True)
    st.markdown('<div class="manifest-header">CURRENT ORDER</div>', unsafe_allow_html=True)
    
    if not st.session_state.cart:
        st.write("NO ITEMS SELECTED.")
    else:
        subtotal = sum(item['price'] for item in st.session_state.cart)
        for item in st.session_state.cart:
            st.markdown(f'<div class="receipt-row"><span>{item["name"]}</span><span>${item["price"]:.2f}</span></div>', unsafe_allow_html=True)
        
        st.markdown(f'<div class="manifest-total"><span>TOTAL</span><span>${subtotal:.2f}</span></div>', unsafe_allow_html=True)
        
        # Payment Integration
        st.markdown("<br>", unsafe_allow_html=True)
        p1, p2 = st.columns(2)
        with p1: 
            st.markdown('<div class="apple-pay-btn">', unsafe_allow_html=True)
            st.button(" Pay", key="apple")
            st.markdown('</div>', unsafe_allow_html=True)
        with p2:
            st.markdown('<div class="google-pay-btn">', unsafe_allow_html=True)
            st.button("G Pay", key="google")
            st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("SECURE CHECKOUT (MFA)", use_container_width=True):
            st.success("Identity Challenge Sent.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. THE KITCHEN DATA SCREEN (KDS) ---
def render_kds():
    st.markdown(f"<h1 style='color:{SystemConfig.PRIMARY_COLOR};'>👨‍🍳 KITCHEN DATA SCREEN</h1>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#333;'>", unsafe_allow_html=True)
    
    k1, k2, k3 = st.columns(3)
    # Placeholder for live DB orders
    mock_orders = [{"id": "901", "type": "TO-GO 🛍️", "items": ["3x Street Tacos", "1x Queso"]}, {"id": "902", "type": "DINE-IN 🍽️", "items": ["1x Fajitas", "2x Ritas"]}]
    
    for i, order in enumerate(mock_orders):
        target_k = [k1, k2, k3][i % 3]
        with target_k:
            b_class = "kds-dine-in" if "DINE-IN" in order["type"] else "kds-to-go"
            st.markdown(f"""
                <div class="kds-card">
                    <div class="kds-badge {b_class}">{order['type']}</div>
                    <div style="font-size: 1.8rem; font-weight: 800; color: {SystemConfig.PRIMARY_COLOR};">#{order['id']}</div>
                    <div style="margin: 15px 0; font-size: 1.2rem; color: #ccc;">
                        {'<br>'.join(order['items'])}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("COMPLETE", key=f"kds_{order['id']}"):
                st.toast(f"Order {order['id']} Cleared.")

# --- RUNTIME ---
def main():
    init_session()
    inject_custom_styles()
    if st.session_state.view_mode == "login":
        render_login()
    elif st.session_state.view_mode == "kds":
        render_kds()
    else:
        render_main_os() # Logic to switch between render_customer_os and admin

if __name__ == "__main__":
    main()
