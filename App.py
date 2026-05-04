import streamlit as st
import random
from database_engine import SystemConfig, sync_user_data, update_user_points, log_transaction, get_sales_data
from streamlit_autorefresh import st_autorefresh

# --- 1. SYSTEM CONFIG & STYLES ---
st.set_page_config(
    page_title=f"{SystemConfig.RESTAURANT_NAME} OS",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def inject_styles():
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;800&display=swap');
        
        .stApp {{ background-color: #000000; color: #FFFFFF; font-family: 'JetBrains Mono', monospace; }}
        [data-testid="stHeader"] {{ background: rgba(0,0,0,0); }}
        
        /* THE STATUS ENGINE */
        .status-engine {{ background: linear-gradient(90deg, #111, #1a1a1a); border: 1px solid #333; padding: 20px; border-radius: 12px; margin: 20px 0; }}
        .status-header {{ display: flex; justify-content: space-between; color: {SystemConfig.PRIMARY_COLOR}; font-weight: 700; text-transform: uppercase; font-size: 14px; }}
        
        /* THE 6-PILL GRID */
        .stButton>button {{ width: 100%; height: 75px !important; background-color: #111 !important; border: 2px solid #333 !important; color: {SystemConfig.PRIMARY_COLOR} !important; border-radius: 12px !important; font-weight: 800 !important; text-transform: uppercase; transition: 0.2s; }}
        .stButton>button:hover {{ border-color: {SystemConfig.PRIMARY_COLOR} !important; background: #1a1a1a !important; transform: translateY(-2px); }}
        
        .active-tab > div > button {{ background-color: #D32F2F !important; color: white !important; border: none !important; }}
        .active-reserva > div > button {{ background-color: #4A0404 !important; color: {SystemConfig.PRIMARY_COLOR} !important; border: 2px solid {SystemConfig.PRIMARY_COLOR} !important; }}
        
        /* MENU & MANIFEST */
        .menu-card {{ background: rgba(255, 255, 255, 0.03); border: 1px solid #333; border-radius: 12px; padding: 20px; margin-bottom: 15px; min-height: 180px; display: flex; flex-direction: column; justify-content: space-between; }}
        .item-title {{ font-size: 20px; font-weight: 800; color: {SystemConfig.PRIMARY_COLOR}; }}
        .item-desc {{ color: #888; font-size: 13px; margin: 10px 0; }}
        .price-tag {{ font-size: 20px; font-weight: 700; color: #FFF; }}
        
        .manifest-container {{ background: #0a0a0a; border: 1px solid #333; border-radius: 12px; padding: 25px; margin-top: 30px; }}
        .manifest-header {{ color: {SystemConfig.PRIMARY_COLOR}; font-weight: 800; font-size: 1.5rem; border-bottom: 1px solid #222; padding-bottom: 10px; margin-bottom: 15px; }}
        .receipt-row {{ display: flex; justify-content: space-between; padding: 8px 0; color: #888; font-size: 1.1rem; }}
        .manifest-total {{ border-top: 2px dashed #333; padding-top: 15px; margin-top: 15px; font-size: 26px; font-weight: 800; color: {SystemConfig.PRIMARY_COLOR}; display: flex; justify-content: space-between; }}
        
        /* EXPRESS PAYMENTS */
        .apple-pay-btn > div > button {{ background-color: #FFFFFF !important; color: #000 !important; border: none !important; height: 60px !important; font-size: 1.2rem !important; }}
        .google-pay-btn > div > button {{ background-color: #4285F4 !important; color: #FFF !important; border: none !important; height: 60px !important; font-size: 1.2rem !important; }}

        /* KDS STATION */
        .kds-card {{ background-color: #080808; border-left: 10px solid {SystemConfig.PRIMARY_COLOR}; padding: 30px; border-radius: 8px; margin-bottom: 20px; min-height: 250px; }}
        .kds-badge {{ padding: 6px 15px; border-radius: 4px; font-weight: 800; font-size: 14px; text-transform: uppercase; margin-bottom: 15px; display: inline-block; }}
        .kds-dine-in {{ background-color: #2E7D32; color: white; }}
        .kds-to-go {{ background-color: #D32F2F; color: white; }}
        .ticket-id {{ font-size: 2rem; font-weight: 800; color: {SystemConfig.PRIMARY_COLOR}; }}
        .ticket-items {{ font-size: 1.5rem; color: #FFF; margin-top: 20px; line-height: 1.5; }}

        /* ADMIN LOGS */
        .admin-log-container {{ background: #111; border: 1px solid #333; border-radius: 8px; padding: 20px; height: 400px; overflow-y: scroll; }}
        .metric-box {{ background: #1a1a1a; padding: 20px; border-radius: 8px; text-align: center; border: 1px solid #333; }}
        
        footer {{visibility: hidden;}} #MainMenu {{visibility: hidden;}}
        </style>

        <script>
        // Spacebar Bump Script for KDS
        document.addEventListener('keydown', function(e) {{
            if (e.code === 'Space') {{
                const bumpBtn = window.parent.document.querySelector('button[kind="primary"]');
                if (bumpBtn) bumpBtn.click();
            }}
        }});
        </script>
    """, unsafe_allow_html=True)

# --- 2. DATA LAYER ---
def get_master_menu():
    return {
        "Lunch Specials": [
            {"id": "L1", "name": "Speedy Gonzales", "desc": "One taco, one enchilada, choice of rice or beans.", "price": 7.99},
            {"id": "L2", "name": "Lunch Fajitas", "desc": "Steak or Chicken, peppers, onions, rice, beans.", "price": 10.50}
        ],
        "Appetizers": [
            {"id": "A1", "name": "Queso Blanco", "desc": "Creamy melted white cheese dip with jalapeño hints.", "price": 5.99},
            {"id": "A2", "name": "Fresh Guacamole", "desc": "Avocado, lime, cilantro, tomatoes, onions.", "price": 7.50}
        ],
        "Tacos": [
            {"id": "T1", "name": "Street Taco", "desc": "Asada, cilantro, onion, lime on corn tortillas.", "price": 3.50},
            {"id": "T2", "name": "Al Pastor", "desc": "Marinated pork, pineapple, cilantro, onion.", "price": 3.75}
        ],
        "Entrees": [
            {"id": "E1", "name": "Burrito California", "desc": "Massive burrito: steak, fries, cheese, guac, sour cream.", "price": 14.50},
            {"id": "E2", "name": "Carne Asada", "desc": "Thinly sliced grilled steak, grilled onions, rice, beans.", "price": 17.50}
        ],
        "Drinks": [
            {"id": "D1", "name": "La Reina Rita", "desc": "House gold tequila, fresh lime, agave. Rocks or Frozen.", "price": 8.99},
            {"id": "D2", "name": "Modelo Especial", "desc": "Draft or Bottle. Served chilled with a lime.", "price": 5.00}
        ],
        "La Reserva": [
            {"id": "R1", "name": "Wagyu Birria Tacos", "desc": "Elite Wagyu beef, consome, Oaxacan cheese.", "price": 24.00},
            {"id": "R2", "name": "The Queen's Flight", "desc": "Three rare aged reposados, hand-selected.", "price": 35.00}
        ]
    }

def get_tier_info(pts):
    if pts < 500: return "POBLANO 🫑", 500, "JALAPEÑO", "#7FFF00"
    elif pts < 5000: return "JALAPEÑO 🌶️", 5000, "HABANERO", "#FFA500"
    else: return "HABANERO 🔥", 10000, "EL REY", "#D4AF37"

# --- 3. STATE & LOGIC ---
def init_session():
    if 'view_mode' not in st.session_state: st.session_state.view_mode = "login"
    if 'cart' not in st.session_state: st.session_state.cart = []
    if 'current_cat' not in st.session_state: st.session_state.current_cat = "Lunch Specials"
    if 'is_admin' not in st.session_state: st.session_state.is_admin = False
    if 'order_type' not in st.session_state: st.session_state.order_type = "DINE-IN 🍽️"
    if 'kds_queue' not in st.session_state: st.session_state.kds_queue = []

def process_order(payment_method, total_price):
    order_id = str(random.randint(1000, 9999))
    
    # 1. Compile items for KDS
    # Tally identical items (e.g., 2x Street Taco)
    item_counts = {}
    for item in st.session_state.cart:
        item_counts[item['name']] = item_counts.get(item['name'], 0) + 1
    kds_item_list = [f"{count}x {name}" for name, count in item_counts.items()]

    # 2. Push to KDS Queue
    st.session_state.kds_queue.append({
        "id": order_id,
        "type": st.session_state.order_type,
        "items": kds_item_list
    })

    # 3. Database Engine Logs
    pts_earned = int(total_price)
    update_user_points(st.session_state.phone_number, pts_earned)
    log_transaction(order_id, st.session_state.order_type, st.session_state.cart, total_price)

    # 4. Clean Up
    st.session_state.cart = []
    st.success(f"Order #{order_id} sent to kitchen via {payment_method}.")
    st.balloons()
    st.rerun()

def complete_kds_ticket(index):
    if st.session_state.kds_queue:
        st.session_state.kds_queue.pop(index)
        st.rerun()

# --- 4. THE SANITIZED PORTAL ---
def render_login():
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.image(SystemConfig.LOGO_PATH, use_container_width=True)
        st.markdown("<h4 style='text-align:center; color:#888;'>WELCOME. ENTER YOUR PHONE NUMBER.</h4>", unsafe_allow_html=True)
        
        phone_input = st.text_input("PHONE", placeholder="417-000-0000", label_visibility="collapsed")
        
        if phone_input:
            clean_key = "".join(filter(str.isdigit, phone_input))
            
            # Fibonacci Portal
            if clean_key == "0112358132":
                st.session_state.view_mode = "kds"
                st.rerun()
            
            # Standard & Admin Portal
            elif len(clean_key) >= 10:
                if clean_key == SystemConfig.ADMIN_CODE: 
                    st.session_state.is_admin = True
                sync_user_data(clean_key)
                st.session_state.view_mode = "customer"
                st.session_state.phone_number = clean_key
                st.rerun()

# --- 5. THE CUSTOMER UI (WITH REAL CHECKOUT ROUTING) ---
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
                <span style="color: {t_color};">{tier}</span>
                <span>{pts} / {target} PTS</span>
            </div>
            <div style="width: 100%; background: #222; height: 8px; border-radius: 4px; overflow: hidden; margin-top:10px;">
                <div style="width: {progress}%; background: {t_color}; height: 100%;"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # The 6-Tab Grid
    menu = get_master_menu()
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

    # Dynamic Menu Iteration
    st.markdown(f"### {st.session_state.current_cat.upper()}")
    items = menu[st.session_state.current_cat]
    cols = st.columns(2)
    for idx, item in enumerate(items):
        with cols[idx % 2]:
            st.markdown(f"""
                <div class="menu-card">
                    <div>
                        <div class="item-title">{item['name']}</div>
                        <div class="item-desc">{item['desc']}</div>
                    </div>
                    <div class="price-tag">${item['price']:.2f}</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"+ ADD {item['name']}", key=f"add_{item['id']}"):
                st.session_state.cart.append(item)
                st.toast(f"Added {item['name']}")
                st.rerun()

    # The Checkout Manifest
    st.markdown('<div class="manifest-container">', unsafe_allow_html=True)
    st.markdown('<div class="manifest-header">CURRENT ORDER</div>', unsafe_allow_html=True)
    
    if not st.session_state.cart:
        st.write("YOUR SELECTIONS WILL APPEAR HERE.")
    else:
        subtotal = sum(i['price'] for i in st.session_state.cart)
        tax = subtotal * 0.085
        total = subtotal + tax

        for item in st.session_state.cart:
            st.markdown(f'<div class="receipt-row"><span>{item["name"]}</span><span>${item["price"]:.2f}</span></div>', unsafe_allow_html=True)
        
        st.markdown(f"""
            <div style="margin-top: 15px; color: #666; font-size: 14px;">
                <div class="receipt-row"><span>Subtotal:</span><span>${subtotal:.2f}</span></div>
                <div class="receipt-row"><span>Tax (8.5%):</span><span>${tax:.2f}</span></div>
            </div>
            <div class="manifest-total"><span>TOTAL</span><span>${total:.2f}</span></div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.session_state.order_type = st.radio("DESTINATION", ["DINE-IN 🍽️", "TO-GO 🛍️"], horizontal=True, label_visibility="collapsed")
        
        # ACTIVE PAYMENT ROUTING
        st.markdown("<br>", unsafe_allow_html=True)
        p1, p2 = st.columns(2)
        with p1: 
            st.markdown('<div class="apple-pay-btn">', unsafe_allow_html=True)
            if st.button(" Pay", key="ap_pay"): process_order("Apple Pay", total)
            st.markdown('</div>', unsafe_allow_html=True)
        with p2:
            st.markdown('<div class="google-pay-btn">', unsafe_allow_html=True)
            if st.button("G Pay", key="gp_pay"): process_order("Google Pay", total)
            st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("CREDIT / DEBIT (MFA SECURED)", use_container_width=True):
            process_order("Saved Card", total)

    st.markdown('</div>', unsafe_allow_html=True)

# --- 6. THE KITCHEN VIEW (LIVE KDS) ---
def render_kds():
    _, logo_col, _ = st.columns([1, 1, 1])
    with logo_col: st.image(SystemConfig.LOGO_PATH, use_container_width=True)
    st.markdown("<hr style='border-color:#333; margin-top:0;'>", unsafe_allow_html=True)
    
    if not st.session_state.kds_queue:
        st.markdown("<h2 style='text-align:center; color:#444; margin-top:50px;'>KITCHEN CLEAR. NO ACTIVE TICKETS.</h2>", unsafe_allow_html=True)
    else:
        # Spacebar bump targets this primary button
        if st.button("BUMP OLDEST (SPACE BAR)", type="primary", use_container_width=True):
            complete_kds_ticket(0)

        st.markdown("<br>", unsafe_allow_html=True)
        cols = st.columns(3)
        for i, order in enumerate(st.session_state.kds_queue):
            with cols[i % 3]:
                b_class = "kds-dine-in" if "DINE-IN" in order['type'] else "kds-to-go"
                st.markdown(f"""
                    <div class="kds-card">
                        <div class="kds-badge {b_class}">{order['type']}</div>
                        <div class="ticket-id">#{order['id']}</div>
                        <div class="ticket-items">
                            {'<br>'.join(order['items'])}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"DONE #{order['id']}", key=f"k_{order['id']}"):
                    complete_kds_ticket(i)
    
    st_autorefresh(interval=10000, key="kds_refresh")

# --- 7. THE RESTORED EXECUTIVE DASHBOARD (ADMIN) ---
def render_admin_os():
    st.markdown(f"<h1 style='color:{SystemConfig.PRIMARY_COLOR};'>LA REINA // EXECUTIVE DASHBOARD</h1>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color: #333;'>", unsafe_allow_html=True)
    
    if st.button("⬅ EXIT SECURE SESSION", type="secondary"):
        st.session_state.is_admin = False
        st.rerun()

    sales_data = get_sales_data()
    if not sales_data:
        st.warning("No financial data found. The sales ledger is currently empty.")
        return

    # Metrics Calculation
    total_revenue = sum(order['total'] for order in sales_data)
    total_orders = len(sales_data)
    aov = total_revenue / total_orders if total_orders > 0 else 0
    
    # Render Metrics
    st.markdown("<br>", unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    with m1: st.markdown(f"<div class='metric-box'><div style='color:#888;'>GROSS REVENUE</div><div style='font-size:2rem; font-weight:bold; color:{SystemConfig.PRIMARY_COLOR};'>${total_revenue:.2f}</div></div>", unsafe_allow_html=True)
    with m2: st.markdown(f"<div class='metric-box'><div style='color:#888;'>TOTAL TICKETS</div><div style='font-size:2rem; font-weight:bold; color:#FFF;'>{total_orders}</div></div>", unsafe_allow_html=True)
    with m3: st.markdown(f"<div class='metric-box'><div style='color:#888;'>AVERAGE ORDER</div><div style='font-size:2rem; font-weight:bold; color:#FFF;'>${aov:.2f}</div></div>", unsafe_allow_html=True)

    # Live Transaction Log
    st.markdown(f"<h3 style='color: {SystemConfig.PRIMARY_COLOR}; margin-top: 40px;'>⚡ LIVE TRANSACTION LOG</h3>", unsafe_allow_html=True)
    st.markdown("<div class='admin-log-container'>", unsafe_allow_html=True)
    for order in reversed(sales_data):
        status_color = "#7FFF00" if order.get("status") == "COMPLETED" else "#FFD700"
        st.markdown(f"""
            <div style="border-bottom: 1px solid #222; padding-bottom: 15px; margin-bottom: 15px;">
                <div style="color: {SystemConfig.PRIMARY_COLOR}; font-weight: bold; font-size: 1.2rem;">
                    ORDER #{order['order_id']} <span style="float:right; color: {status_color}; font-size: 14px;">[{order.get('status', 'COMPLETED')}]</span>
                </div>
                <div style="color: #888; font-size: 14px; margin-top: 5px;">
                    {order['type']} | {len(order['items'])} items | <strong style="color:#FFF;">${order['total']:.2f}</strong>
                </div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st_autorefresh(interval=15000, key="admin_refresh")

# --- 8. RUNTIME ROUTER ---
def render_main_os():
    if st.session_state.is_admin:
        render_admin_os()
    else:
        render_customer_os()

def main():
    init_session()
    inject_styles()
    
    if st.session_state.view_mode == "login":
        render_login()
    elif st.session_state.view_mode == "kds":
        render_kds()
    else:
        render_main_os()

if __name__ == "__main__":
    main()
