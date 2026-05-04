import streamlit as st
import random
from database_engine import SystemConfig, sync_user_data, update_user_points, log_transaction, get_sales_data

# --- 1. SYSTEM CONFIG ---
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
        .stApp {{ background-color: #000000; color: #FFFFFF; font-family: 'JetBrains Mono', monospace; }}
        
        /* THE STATUS ENGINE (Member Bar) */
        .status-engine {{ 
            background: linear-gradient(90deg, #111, #1a1a1a); 
            border: 1px solid #333; 
            padding: 20px; border-radius: 12px; margin: 20px 0; 
        }}
        .status-header {{ display: flex; justify-content: space-between; color: {SystemConfig.PRIMARY_COLOR}; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; font-size: 14px; }}
        
        /* THE 6-PILL GRID (2x3 Layout) */
        .mega-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-bottom: 25px;
        }}
        
        /* Pill/Button Styling */
        .stButton>button {{
            width: 100%;
            height: 70px !important;
            background-color: #111 !important;
            border: 2px solid #333 !important;
            color: {SystemConfig.PRIMARY_COLOR} !important;
            border-radius: 12px !important;
            font-weight: 800 !important;
            text-transform: uppercase;
            transition: 0.2s;
        }}
        .stButton>button:hover {{ border-color: {SystemConfig.PRIMARY_COLOR} !important; background: #1a1a1a !important; }}

        /* Category Special States */
        .active-red > div > button {{ background-color: #D32F2F !important; color: white !important; border: none !important; }}
        .active-reserva > div > button {{ background-color: #4A0404 !important; color: {SystemConfig.PRIMARY_COLOR} !important; border: 2px solid {SystemConfig.PRIMARY_COLOR} !important; }}

        /* CURRENT ORDER MANIFEST */
        .manifest-container {{ background: #0a0a0a; border: 1px solid #333; border-radius: 12px; padding: 25px; margin-top: 30px; }}
        .manifest-header {{ color: {SystemConfig.PRIMARY_COLOR}; font-weight: 800; font-size: 1.5rem; border-bottom: 1px solid #222; padding-bottom: 10px; margin-bottom: 15px; }}
        .receipt-row {{ display: flex; justify-content: space-between; padding: 8px 0; color: #888; font-size: 1.1rem; }}
        .manifest-total {{ border-top: 2px dashed #333; padding-top: 15px; margin-top: 15px; font-size: 24px; font-weight: bold; color: {SystemConfig.PRIMARY_COLOR}; display: flex; justify-content: space-between; }}
        
        /* EXPRESS PAYMENTS */
        .apple-pay-btn > div > button {{ background-color: #FFFFFF !important; color: #000 !important; border: none !important; height: 55px !important; }}
        .google-pay-btn > div > button {{ background-color: #4285F4 !important; color: #FFF !important; border: none !important; height: 55px !important; }}

        /* KDS STATION STYLES */
        .kds-card {{ background-color: #080808; border-left: 8px solid {SystemConfig.PRIMARY_COLOR}; padding: 25px; border-radius: 8px; margin-bottom: 20px; min-height: 200px; }}
        .kds-badge {{ padding: 5px 12px; border-radius: 4px; font-weight: 800; font-size: 12px; text-transform: uppercase; margin-bottom: 15px; display: inline-block; }}
        .kds-dine-in {{ background-color: #2E7D32; color: white; }}
        .kds-to-go {{ background-color: #D32F2F; color: white; }}

        footer {{visibility: hidden;}} #MainMenu {{visibility: hidden;}}
        </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIC & DATA ---
def init_session():
    if 'view_mode' not in st.session_state: st.session_state.view_mode = "login"
    if 'cart' not in st.session_state: st.session_state.cart = []
    if 'current_cat' not in st.session_state: st.session_state.current_cat = "Lunch Specials"
    if 'is_admin' not in st.session_state: st.session_state.is_admin = False

def get_tier_info(pts):
    if pts < 500: return "POBLANO 🫑", 500, "JALAPEÑO 🌶️", "#7FFF00"
    elif pts < 5000: return "JALAPEÑO 🌶️", 5000, "HABANERO 🔥", "#FFA500"
    else: return "HABANERO 🔥", 10000, "EL REY 👑", "#D4AF37"

# --- 3. THE PORTAL (Casual Login + Fibonacci) ---
def render_login():
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.image(SystemConfig.LOGO_PATH, use_container_width=True)
        st.markdown("<h4 style='text-align:center; color:#888; font-weight:400;'>WELCOME BACK. ENTER YOUR NUMBER.</h4>", unsafe_allow_html=True)
        
        phone_input = st.text_input("PHONE", placeholder="417-000-0000", label_visibility="collapsed")
        
        if phone_input:
            # Fibonacci Trigger: 0112358132
            if phone_input == "0112358132":
                st.session_state.view_mode = "kds"
                st.rerun()
            elif len(phone_input) >= 10:
                if phone_input == SystemConfig.ADMIN_CODE:
                    st.session_state.is_admin = True
                sync_user_data(phone_input)
                st.session_state.view_mode = "customer"
                st.session_state.phone_number = phone_input
                st.rerun()

# --- 4. THE CUSTOMER UI ---
def render_customer_os():
    _, logo_col, _ = st.columns([1, 2, 1])
    with logo_col: st.image(SystemConfig.LOGO_PATH, use_container_width=True)

    # Status Bar
    pts = st.session_state.get('reward_points', 0)
    tier, target, next_t, t_color = get_tier_info(pts)
    progress = min(int((pts / target) * 100), 100)

    st.markdown(f"""
        <div class="status-engine" style="border-color: {t_color};">
            <div class="status-header">
                <span style="color: {t_color};">{tier} MEMBER</span>
                <span>{pts} / {target} PTS</span>
            </div>
            <div style="width: 100%; background: #222; height: 8px; border-radius: 4px; overflow: hidden;">
                <div style="width: {progress}%; background: {t_color}; height: 100%;"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 6-TAB GRID
    categories = ["Lunch Specials", "Appetizers", "Tacos", "Entrees", "Drinks", "La Reserva"]
    t1, t2 = st.columns(2)
    
    for i, cat in enumerate(categories):
        target_col = t1 if i % 2 == 0 else t2
        with target_col:
            style_class = ""
            if cat == st.session_state.current_cat: style_class = "active-red"
            if cat == "La Reserva":
                if pts < 5000:
                    st.button(f"🔒 {cat}", disabled=True)
                    continue
                style_class = "active-reserva"
            
            st.markdown(f'<div class="{style_class}">', unsafe_allow_html=True)
            if st.button(cat, key=f"btn_{cat}"):
                st.session_state.current_cat = cat
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # CURRENT ORDER (THE MANIFEST)
    st.markdown('<div class="manifest-container">', unsafe_allow_html=True)
    st.markdown('<div class="manifest-header">CURRENT ORDER</div>', unsafe_allow_html=True)
    
    if not st.session_state.cart:
        st.write("YOUR SELECTIONS WILL APPEAR HERE.")
    else:
        subtotal = sum(item['price'] for item in st.session_state.cart)
        for item in st.session_state.cart:
            st.markdown(f'<div class="receipt-row"><span>{item["name"]}</span><span>${item["price"]:.2f}</span></div>', unsafe_allow_html=True)
        
        st.markdown(f'<div class="manifest-total"><span>TOTAL</span><span>${subtotal:.2f}</span></div>', unsafe_allow_html=True)
        
        # Payment Grid
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
            st.success("A verification code has been sent to your device.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. THE KITCHEN VIEW (KDS) ---
def render_kds():
    st.markdown(f"<h1 style='color:{SystemConfig.PRIMARY_COLOR};'>👨‍🍳 KITCHEN DATA SCREEN</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    k1, k2, k3 = st.columns(3)
    mock_orders = [
        {"id": "701", "type": "TO-GO 🛍️", "items": ["3x Street Tacos", "1x Queso"]},
        {"id": "702", "type": "DINE-IN 🍽️", "items": ["1x Burrito California", "2x Ritas"]}
    ]
    
    for i, order in enumerate(mock_orders):
        target_k = [k1, k2, k3][i % 3]
        with target_k:
            b_class = "kds-dine-in" if "DINE-IN" in order["type"] else "kds-to-go"
            st.markdown(f"""
                <div class="kds-card">
                    <div class="kds-badge {b_class}">{order['type']}</div>
                    <div style="font-size: 1.8rem; font-weight: 800; color: {SystemConfig.PRIMARY_COLOR};">#{order['id']}</div>
                    <div style="font-size: 1.3rem; color: #ccc; margin-top: 15px;">
                        {'<br>'.join(order['items'])}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("MARK COMPLETE", key=f"kds_{order['id']}"):
                st.toast(f"Ticket {order['id']} cleared.")

# --- 6. ADMIN DASHBOARD STUB ---
def render_admin_os():
    st.title("EXECUTIVE DASHBOARD")
    if st.button("BACK TO CUSTOMER VIEW"):
        st.session_state.is_admin = False
        st.rerun()

# --- 7. ROUTING & RUNTIME ---
def render_main_os():
    if st.session_state.is_admin:
        render_admin_os()
    else:
        render_customer_os()

def main():
    init_session()
    inject_custom_styles()
    
    if st.session_state.view_mode == "login":
        render_login()
    elif st.session_state.view_mode == "kds":
        render_kds()
    else:
        render_main_os()

if __name__ == "__main__":
    main()
