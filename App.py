import streamlit as st
from streamlit_pills import pills
from streamlit_autorefresh import st_autorefresh
import random
from database_engine import SystemConfig, sync_user_data, update_user_points, log_transaction, get_sales_data

# FORCING SIDEBAR TO BE VISIBLE
st.set_page_config(
    page_title=f"{SystemConfig.RESTAURANT_NAME} POS",
    layout="wide",
    initial_sidebar_state="expanded" 
)

def inject_custom_styles():
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
        .stApp {{ background-color: {SystemConfig.BG_COLOR}; color: #FFFFFF; font-family: 'JetBrains Mono', monospace; }}
        .status-engine {{ background: linear-gradient(90deg, #111, #222); border: 2px solid {SystemConfig.ACCENT_COLOR}; padding: 15px 20px; border-radius: 8px; margin: 20px 0; box-shadow: 0 0 15px rgba(127, 255, 0, 0.15); }}
        .status-header {{ display: flex; justify-content: space-between; color: {SystemConfig.ACCENT_COLOR}; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 10px; font-size: 14px; }}
        .menu-card {{ background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(10px); border: 1px solid #333; border-radius: 12px; padding: 25px; transition: all 0.3s ease; height: 220px; display: flex; flex-direction: column; justify-content: space-between; margin-bottom: 15px; }}
        .menu-card:hover {{ border-color: {SystemConfig.PRIMARY_COLOR}; transform: translateY(-5px); }}
        .item-title {{ color: {SystemConfig.PRIMARY_COLOR}; font-size: 24px; font-weight: 800; margin-bottom: 5px; line-height: 1.2; }}
        .item-meta {{ color: #888; font-size: 13px; line-height: 1.4; }}
        .price-tag {{ color: {SystemConfig.PRIMARY_COLOR}; font-size: 22px; font-weight: 700; margin-top: 15px; }}
        .stButton>button {{ width: 100%; background-color: transparent !important; border: 2px solid #444 !important; color: white !important; height: 50px !important; border-radius: 8px !important; transition: 0.2s; font-weight: bold !important; text-transform: uppercase; }}
        .stButton>button:hover {{ border-color: {SystemConfig.PRIMARY_COLOR} !important; color: {SystemConfig.PRIMARY_COLOR} !important; background: rgba(255, 215, 0, 0.1) !important; }}
        .checkout-btn>button {{ background-color: {SystemConfig.ACCENT_COLOR} !important; color: #000 !important; font-size: 20px !important; height: 70px !important; border: none !important; }}
        .checkout-btn>button:hover {{ background-color: #fff !important; box-shadow: 0 0 20px rgba(127, 255, 0, 0.5) !important; }}
        .stTextInput>div>div>input {{ background-color: #111 !important; color: {SystemConfig.PRIMARY_COLOR} !important; border: 2px solid #333 !important; border-radius: 8px !important; font-size: 24px !important; text-align: center !important; height: 60px !important; letter-spacing: 2px; }}
        .stTextInput>div>div>input:focus {{ border-color: {SystemConfig.ACCENT_COLOR} !important; box-shadow: 0 0 10px rgba(127, 255, 0, 0.3) !important; }}
        .receipt-container {{ background: #111; border: 1px solid #333; border-radius: 8px; padding: 30px; font-family: 'JetBrains Mono', monospace; }}
        .receipt-row {{ display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 18px; }}
        .receipt-total {{ display: flex; justify-content: space-between; margin-top: 20px; padding-top: 20px; border-top: 2px dashed #444; font-size: 24px; font-weight: bold; color: {SystemConfig.PRIMARY_COLOR}; }}
        div[role="radiogroup"] {{ justify-content: center; margin-bottom: 20px; }}
        .tier-box {{ background: #111; border: 1px solid #333; border-radius: 8px; padding: 20px; text-align: center; height: 100%; }}
        div[data-testid="stMarkdownContainer"] p {{ font-weight: bold; font-size: 16px; }}
        
        /* RESTORED HEADER FOR SIDEBAR ACCESS */
        footer {{visibility: hidden;}} #MainMenu {{visibility: hidden;}}
        </style>
    """, unsafe_allow_html=True)

def initialize_session():
    if 'authenticated' not in st.session_state: st.session_state.authenticated = False
    if 'is_admin' not in st.session_state: st.session_state.is_admin = False
    if 'phone_number' not in st.session_state: st.session_state.phone_number = ""
    if 'cart' not in st.session_state: st.session_state.cart = [] 
    if 'order_type' not in st.session_state: st.session_state.order_type = "DINE-IN 🍽️"

def get_tier_info(pts):
    if pts < 100: return "POBLANO 🫑", 100, "JALAPEÑO 🌶️"
    elif pts < 300: return "JALAPEÑO 🌶️", 300, "HABANERO 🔥"
    else: return "HABANERO 🔥", 1000, "EL REY 👑" 

def load_master_menu():
    return {
        "Lunch Specials": [
            {"id": "L1", "name": "Speedy Gonzales", "desc": "One taco, one enchilada, choice of rice or beans.", "price": 7.99},
            {"id": "L2", "name": "Lunch Fajitas", "desc": "Steak or Chicken, peppers, onions, rice, beans, tortillas.", "price": 10.50},
        ],
        "Appetizers": [
            {"id": "A1", "name": "Queso Blanco", "desc": "Creamy melted white cheese dip with jalapeño hints.", "price": 5.99},
            {"id": "A2", "name": "Fresh Guacamole", "desc": "Avocado, lime, cilantro, tomatoes, onions. Made daily.", "price": 7.50},
        ],
        "Tacos": [
            {"id": "T1", "name": "Street Taco (Asada)", "desc": "Steak, cilantro, onion, lime on corn tortillas.", "price": 3.50},
            {"id": "T2", "name": "Al Pastor", "desc": "Marinated pork, pineapple, cilantro, onion.", "price": 3.75},
        ],
        "Entrees": [
            {"id": "E1", "name": "Burrito California", "desc": "Massive burrito: steak, fries, cheese, guac, sour cream inside.", "price": 14.50},
            {"id": "E3", "name": "Carne Asada", "desc": "Thinly sliced grilled steak, grilled onions, rice, beans, guac salad.", "price": 17.50},
        ],
        "Drinks": [
            {"id": "D1", "name": "La Reina House Rita", "desc": "Classic gold tequila, fresh lime, agave. Rocks or Frozen.", "price": 8.99},
            {"id": "D6", "name": "Modelo Especial", "desc": "Draft or Bottle. Serve chilled with a lime.", "price": 5.00}
        ],
        "Rewards 👑": [], "Checkout 🛒": [] 
    }

def render_login_screen():
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 2, 1])
    with col:
        try: st.image(SystemConfig.LOGO_PATH, use_container_width=True)
        except: st.markdown(f"<h1 style='text-align:center; color:{SystemConfig.PRIMARY_COLOR};'>{SystemConfig.RESTAURANT_NAME}</h1>", unsafe_allow_html=True)
        st.markdown(f"<h4 style='text-align:center; color:#888; margin-bottom: 20px;'>ENTER PHONE NUMBER TO UNLOCK</h4>", unsafe_allow_html=True)
        phone_input = st.text_input("PHONE", placeholder="10-DIGIT NUMBER", label_visibility="collapsed", max_chars=10)
        
        if phone_input:
            cleaned_phone = ''.join(filter(str.isdigit, phone_input))
            if len(cleaned_phone) >= 10: 
                if cleaned_phone == SystemConfig.ADMIN_CODE:
                    st.session_state.authenticated = True
                    st.session_state.is_admin = True
                    st.rerun()
                sync_user_data(cleaned_phone)
                st.session_state.authenticated = True
                st.session_state.phone_number = cleaned_phone
                st.rerun() 
            else:
                st.error("Access Denied. 10-digit sequence required.")

def render_admin_os():
    st.markdown(f"<h1 style='text-align:left; color:{SystemConfig.PRIMARY_COLOR}; margin-top: -20px;'>LA REINA // EXECUTIVE DASHBOARD</h1>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color: #333;'>", unsafe_allow_html=True)
    if st.button("⬅ LOGOUT SECURE SESSION", type="secondary"):
        st.session_state.authenticated = False
        st.session_state.is_admin = False
        st.rerun()

    sales_data = get_sales_data()
    if not sales_data: st.warning("No financial data found. The sales ledger is currently empty.")
    else:
        total_revenue = sum(order['total'] for order in sales_data)
        total_orders = len(sales_data)
        aov = total_revenue / total_orders if total_orders > 0 else 0
        all_items = []
        for order in sales_data: all_items.extend(order['items'])
        item_counts = {}
        for item in all_items: item_counts[item] = item_counts.get(item, 0) + 1
        top_items = sorted(item_counts.items(), key=lambda x: x[1], reverse=True)[:3]

        m1, m2, m3 = st.columns(3)
        with m1: st.metric("GROSS REVENUE (LIVE)", f"${total_revenue:.2f}")
        with m2: st.metric("TOTAL ORDERS", f"{total_orders}")
        with m3: st.metric("AVERAGE ORDER VALUE", f"${aov:.2f}")
            
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"<h3 style='color: {SystemConfig.ACCENT_COLOR};'>🔥 TOP SELLERS</h3>", unsafe_allow_html=True)
            st.markdown("<div class='receipt-container'>", unsafe_allow_html=True)
            if top_items:
                for idx, (item, count) in enumerate(top_items): st.markdown(f"<div style='font-size: 20px; margin-bottom: 10px;'><strong style='color:{SystemConfig.PRIMARY_COLOR};'>#{idx+1}</strong> {item} <span style='float:right; color:#888;'>({count} sold)</span></div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<h3 style='color: {SystemConfig.ACCENT_COLOR};'>⚡ LIVE TRANSACTION LOG</h3>", unsafe_allow_html=True)
            st.markdown("<div class='receipt-container' style='height: 300px; overflow-y: scroll;'>", unsafe_allow_html=True)
            for order in reversed(sales_data):
                status_color = "#7FFF00" if order.get("status") == "COMPLETED" else "#FFD700"
                st.markdown(f"""
                <div style="border-bottom: 1px solid #333; padding-bottom: 10px; margin-bottom: 10px;">
                    <div style="color: {SystemConfig.PRIMARY_COLOR}; font-weight: bold;">ORDER #{order['order_id']} <span style="float:right; color: {status_color}; font-size: 14px;">[{order.get('status', 'COMPLETED')}]</span></div>
                    <div style="color: #ccc; font-size: 14px;">{order['type']} | {len(order['items'])} items | <strong>${order['total']:.2f}</strong></div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    st_autorefresh(interval=10000, key="admin_sync") 

def render_main_os():
    _, logo_col, _ = st.columns([1, 2, 1])
    with logo_col:
        try: st.image(SystemConfig.LOGO_PATH, use_container_width=True)
        except: st.markdown(f"<h1 style='text-align:center; color:{SystemConfig.PRIMARY_COLOR};'>{SystemConfig.RESTAURANT_NAME}</h1>", unsafe_allow_html=True)

    pts = st.session_state.reward_points
    current_tier, target, next_tier = get_tier_info(pts)
    progress_percentage = min(int((pts / target) * 100), 100)
    pts_away = target - pts
    cart_items = len(st.session_state.cart)
    cart_subtotal = sum(item['price'] for item in st.session_state.cart)

    st.markdown(f"""
        <div class="status-engine">
            <div class="status-header">
                <span style="color: {SystemConfig.PRIMARY_COLOR};">TIER: {current_tier}</span>
                <span style="color: #fff;">CART: {cart_items} ITEMS | ${cart_subtotal:.2f}</span>
                <span>MEMBER: {st.session_state.phone_number}</span>
            </div>
            <div style="width: 100%; background-color: #222; height: 12px; border-radius: 6px; margin-bottom: 5px; overflow: hidden; border: 1px solid #333;">
                <div style="width: {progress_percentage}%; background-color: {SystemConfig.PRIMARY_COLOR}; height: 100%; box-shadow: 0 0 10px {SystemConfig.PRIMARY_COLOR}; border-radius: 6px;"></div>
            </div>
            <div style="text-align: right; color: #888; font-size: 12px; font-weight: bold;">
                {pts} / {target} PTS — <span style="color: {SystemConfig.PRIMARY_COLOR};">{pts_away} PTS AWAY FROM {next_tier}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    menu = load_master_menu()
    selected_category = pills("Navigation", list(menu.keys()), index=0)

    if selected_category == "Rewards 👑":
        st.markdown(f"<h2 style='color: {SystemConfig.PRIMARY_COLOR}; text-align: center;'>LA REINA LOYALTY TIERS</h2>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        t1, t2, t3 = st.columns(3)
        with t1: st.markdown("""<div class="tier-box"><h3 style="color:#7FFF00;">POBLANO 🫑</h3><p style="color:#888;">0 - 100 Points</p></div>""", unsafe_allow_html=True)
        with t2: st.markdown("""<div class="tier-box" style="border-color: #FFA500;"><h3 style="color:#FFA500;">JALAPEÑO 🌶️</h3><p style="color:#888;">100 - 300 Points</p></div>""", unsafe_allow_html=True)
        with t3: st.markdown("""<div class="tier-box" style="border-color: #FF4500;"><h3 style="color:#FF4500;">HABANERO 🔥</h3><p style="color:#888;">300+ Points</p></div>""", unsafe_allow_html=True)
        st.markdown("<hr style='border-color: #333;'><h3 style='text-align: center;'>📸 SCAN RECEIPT</h3>", unsafe_allow_html=True)
        receipt_img = st.camera_input("Scan Receipt", label_visibility="collapsed")
        if receipt_img:
            update_user_points(st.session_state.phone_number, 45)
            st.balloons() 
            st.rerun()

    elif selected_category == "Checkout 🛒":
        st.markdown(f"<h2 style='color: {SystemConfig.PRIMARY_COLOR}; text-align: center;'>YOUR TRAY</h2>", unsafe_allow_html=True)
        if len(st.session_state.cart) == 0: st.info("Your tray is empty.")
        else:
            _, col, _ = st.columns([1, 2, 1])
            with col:
                st.markdown("<div class='receipt-container'>", unsafe_allow_html=True)
                for item in st.session_state.cart: st.markdown(f"""<div class="receipt-row"><span>{item['name']}</span><span>${item['price']:.2f}</span></div>""", unsafe_allow_html=True)
                tax = cart_subtotal * SystemConfig.TAX_RATE
                total = cart_subtotal + tax
                st.markdown(f"""<div style="margin-top: 15px; color: #888; font-size: 16px;"><div class="receipt-row"><span>Subtotal:</span><span>${cart_subtotal:.2f}</span></div><div class="receipt-row"><span>Tax (8.5%):</span><span>${tax:.2f}</span></div></div><div class="receipt-total"><span>TOTAL:</span><span>${total:.2f}</span></div></div><br>""", unsafe_allow_html=True)
                
                st.markdown("<div style='text-align: center; color: #888; font-weight: bold;'>ORDER DESTINATION</div>", unsafe_allow_html=True)
                st.session_state.order_type = st.radio("Order Type", ["DINE-IN 🍽️", "TO-GO 🛍️"], horizontal=True, label_visibility="collapsed", index=0 if st.session_state.order_type == "DINE-IN 🍽️" else 1)
                
                st.markdown("<div class='checkout-btn'>", unsafe_allow_html=True)
                if st.button(f"PLACE {st.session_state.order_type} ORDER (${total:.2f})", use_container_width=True):
                    order_num = random.randint(1000, 9999)
                    points_earned = int(cart_subtotal)
                    update_user_points(st.session_state.phone_number, points_earned)
                    log_transaction(order_num, st.session_state.order_type, st.session_state.cart, total)
                    
                    st.session_state.cart = []
                    st.success(f"ORDER #{order_num} SENT TO KITCHEN.")
                    st.balloons()
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
                if st.button("Clear Cart", type="secondary"):
                    st.session_state.cart = []
                    st.rerun()

    elif selected_category:
        items = menu[selected_category]
        cols = st.columns(2)
        for idx, item in enumerate(items):
            with cols[idx % 2]:
                st.markdown(f"""<div class="menu-card"><div><div class="item-title">{item['name']}</div><div class="item-meta">{item['desc']}</div></div><div class="price-tag">${item['price']:.2f}</div></div>""", unsafe_allow_html=True)
                if st.button(f"+ ADD {item['name']}", key=f"btn_{item['id']}"):
                    st.session_state.cart.append(item)
                    st.toast(f"Added {item['name']} to your tray!")
                    st.rerun() 

def main():
    initialize_session()
    inject_custom_styles()
    if not st.session_state.authenticated: render_login_screen()
    elif st.session_state.is_admin: render_admin_os()
    else: render_main_os()

if __name__ == "__main__":
    main()
