# -*- coding: utf-8 -*-
import streamlit as st
import streamlit.components.v1 as components
import time
import json
import os
import datetime
from streamlit_autorefresh import st_autorefresh

# ==========================================
# 1. DATABASE ENGINE & SYSTEM CONFIG
# ==========================================
class SystemConfig:
    RESTAURANT_NAME = "la Reina Margaritas"
    PRIMARY_COLOR = "#D4AF37"  
    ACCENT_COLOR = "#7FFF00"   
    PURPLE_GLOW = "#6A0DAD"    
    BG_COLOR = "#000000"       
    LOGO_PATH = "la_reina_dark.png" 
    TAX_RATE = 0.085           
    DB_FILE = "la_reina_db.json"      
    SALES_DB = "la_reina_sales.json"  

def load_db():
    if os.path.exists(SystemConfig.DB_FILE):
        with open(SystemConfig.DB_FILE, 'r') as f: return json.load(f)
    return {} 

def save_db(db_data):
    with open(SystemConfig.DB_FILE, 'w') as f: json.dump(db_data, f, indent=4)

def sync_user_data(phone_number):
    db = load_db()
    if phone_number not in db:
        db[phone_number] = {"points": 0, "lifetime_orders": 0}
        save_db(db)
    st.session_state.reward_points = db[phone_number]["points"]

def update_user_points(phone_number, points_to_add):
    if not phone_number or phone_number == "STAFF": return
    db = load_db()
    if phone_number in db:
        db[phone_number]["points"] += points_to_add
        db[phone_number]["lifetime_orders"] += 1
        save_db(db)
        st.session_state.reward_points = db[phone_number]["points"]

def log_transaction(order_num, order_type, cart_items, total_price, phone_number):
    sales = get_sales_data()
    new_order = {
        "order_id": order_num, 
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p"),
        "phone": phone_number if phone_number else "GUEST", 
        "type": order_type,
        "items": [item['name'] for item in cart_items], 
        "total": total_price, 
        "status": "PENDING"
    }
    sales.append(new_order)
    with open(SystemConfig.SALES_DB, 'w') as f: json.dump(sales, f, indent=4)

def get_sales_data():
    if os.path.exists(SystemConfig.SALES_DB):
        with open(SystemConfig.SALES_DB, 'r') as f: return json.load(f)
    return []

def bump_kitchen_ticket(order_id):
    sales = get_sales_data()
    for order in sales:
        if order["order_id"] == order_id:
            order["status"] = "COMPLETED"
            break
    with open(SystemConfig.SALES_DB, 'w') as f: json.dump(sales, f, indent=4)

# ==========================================
# 2. SYSTEM CONFIG & STYLES (Mobile-Native UI)
# ==========================================
st.set_page_config(page_title=f"{SystemConfig.RESTAURANT_NAME} OS", layout="wide", initial_sidebar_state="collapsed")

def inject_styles():
    # 1. MOBILE VIEWPORT LOCK (Forces scale to 1.0, prevents tiny text)
    st.markdown("""
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    """, unsafe_allow_html=True)

    is_mobile = st.session_state.get('layout_mode', 'Mobile') == 'Mobile'
    
    # STRICT MOBILE DEFAULTS FOR FLAGSHIP PHONES (S25 Ultra / iPhone)
    padding = "1rem 0.5rem" if is_mobile else "3rem 5rem"
    max_width = "480px" if is_mobile else "1600px"

    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;800&display=swap');
        
        /* THE FOUNDATION: Pure Black, Edge-to-Edge */
        body {{
            overscroll-behavior-y: none; /* Stops pull-to-refresh and bounce */
            background-color: #000000 !important;
        }}
        
        .stApp {{
            background-color: #000000 !important;
        }}
        
        [data-testid="stAppViewBlockContainer"] {{
            padding: {padding} !important;
            max-width: {max_width} !important;
            margin: 0 auto !important; /* Centers the mobile 480px column on larger screens */
            width: 100vw !important;
            font-family: 'JetBrains Mono', monospace;
        }}
        
        [data-testid="stHeader"] {{ display: none !important; }}
        
        /* MASSIVE TYPOGRAPHY OVERRIDE */
        h1, h2, h3, h4, p, div {{ color: #FFFFFF !important; }}

        /* NATIVE INPUT BAR (Forces phone keypad, huge target) */
        div[data-baseweb="input"] > div {{
            background-color: #111111 !important;
            border: 2px solid #333 !important;
            border-radius: 12px !important;
            height: 7rem !important;
            width: 80% !important;
            max-width: 320px !important;
            margin: 0 auto 1rem auto !important;
        }}
        div[data-baseweb="input"] input {{
            color: {SystemConfig.PRIMARY_COLOR} !important;
            font-size: 4rem !important;
            letter-spacing: 0.2rem;
            text-align: center !important;
            -webkit-text-security: disc;
        }}
        div[data-baseweb="input"] > div:focus-within {{
            border-color: {SystemConfig.PURPLE_GLOW} !important;
            box-shadow: 0 0 20px {SystemConfig.PURPLE_GLOW} !important;
        }}

        /* MASSIVE UNIVERSAL BUTTONS */
        div.stButton > button {{ 
            width: 100%; 
            height: 5rem !important; 
            background-color: #111 !important; 
            border: 2px solid #444 !important; 
            color: #FFF !important; 
            border-radius: 12px !important; 
            font-weight: 800 !important; 
            text-transform: uppercase; 
            transition: 0.1s ease-in-out; 
            font-size: 1.5rem !important; 
        }}
        
        /* UNIVERSAL PURPLE ACTION ZONE */
        div.stButton > button:active, 
        .active-tab > div > button {{ 
            background-color: {SystemConfig.PURPLE_GLOW} !important; 
            color: white !important; 
            border: 2px solid #9D50BB !important; 
            box-shadow: 0 0 25px rgba(106, 13, 173, 0.9) !important; 
            transform: scale(0.96) !important; 
        }}
        
        /* VIP RESERVA LOCK */
        .active-reserva > div > button {{ 
            background-color: {SystemConfig.PRIMARY_COLOR} !important; 
            color: black !important; 
            border: 2px solid {SystemConfig.PRIMARY_COLOR} !important; 
        }}
        
        /* MENU & MANIFEST CARDS */
        .menu-card {{ background: rgba(255, 255, 255, 0.03); border: 1px solid #333; border-radius: 12px; padding: 20px; margin-bottom: 15px; min-height: 140px; display: flex; flex-direction: column; justify-content: space-between; }}
        .item-title {{ font-size: 20px; font-weight: 800; color: {SystemConfig.PRIMARY_COLOR}; }}
        .item-desc {{ color: #888; font-size: 13px; margin: 10px 0; }}
        .price-tag {{ font-size: 20px; font-weight: 700; color: #FFF; }}
        
        .manifest-container {{ background: #0a0a0a; border: 1px solid #333; border-radius: 12px; padding: 25px; margin-top: 30px; }}
        .manifest-header {{ color: {SystemConfig.PRIMARY_COLOR}; font-weight: 800; font-size: 1.5rem; border-bottom: 1px solid #222; padding-bottom: 10px; margin-bottom: 15px; }}
        .receipt-row {{ display: flex; justify-content: space-between; padding: 8px 0; color: #888; font-size: 1.1rem; }}
        .manifest-total {{ border-top: 2px dashed #333; padding-top: 15px; margin-top: 15px; font-size: 26px; font-weight: 800; color: {SystemConfig.PRIMARY_COLOR}; display: flex; justify-content: space-between; }}

        /* KDS TICKET CARDS */
        .kds-card {{ background-color: #080808; padding: 30px; border-radius: 8px; margin-bottom: 20px; border-left: 10px solid #333; border-top: 1px solid #222; border-right: 1px solid #222; border-bottom: 1px solid #222; }}
        .ticket-id {{ font-size: 2.5rem; font-weight: 800; color: {SystemConfig.PRIMARY_COLOR}; display: flex; justify-content: space-between; align-items: center; }}
        .ticket-phone {{ font-size: 1.2rem; color: #888; font-weight: 400; }}
        .ticket-items {{ font-size: 1.6rem; color: #FFF; margin-top: 15px; line-height: 1.5; }}

        /* REWARDS ENGINE */
        .status-engine {{ background: linear-gradient(90deg, #111, #1a1a1a); border: 1px solid #333; padding: 20px; border-radius: 12px; margin: 20px 0; }}
        .status-header {{ display: flex; justify-content: space-between; color: {SystemConfig.PRIMARY_COLOR}; font-weight: 700; text-transform: uppercase; font-size: 14px; }}

        /* HIDE CLUTTER */
        footer, header, [data-testid="stSidebarNav"] {{ display: none !important; }}
        </style>
    """, unsafe_allow_html=True)

def inject_kds_keyboard_hack():
    # SPACEBAR HACK: Looks for the PRIMARY button (assigned only to "BUMP NEWEST")
    components.html("""<script>const doc = window.parent.document; if (!doc.getElementById('kds-spacebar-hack')) { const script = doc.createElement('script'); script.id = 'kds-spacebar-hack'; script.innerHTML = `document.addEventListener('keydown', function(e) { if (e.target.tagName.toLowerCase() === 'input') return; if (e.code === 'Space' || e.key === ' ') { e.preventDefault(); const bumpBtn = document.querySelector('button[kind="primary"]'); if (bumpBtn) { bumpBtn.click(); } } });`; doc.head.appendChild(script); } window.parent.focus();</script>""", height=0, width=0)

# ==========================================
# 3. MENU DATA (100% COMPLETE & INTACT)
# ==========================================
def get_master_menu():
    return {
        "Appetizers": [
            {"id": "A1", "name": "Famoso Queso Casero", "desc": "House-made queso with a hint of Hatch chili pepper.", "price": 8.00},
            {"id": "A2", "name": "Top Shelf Guacamole", "desc": "Fresh avocado dip, lime juice, garlic, onion, and cilantro.", "price": 9.00},
            {"id": "A3", "name": "Agua Chile de Camaron", "desc": "Jumbo butterfly cut shrimp marinated in serrano lime broth.", "price": 14.00},
            {"id": "A4", "name": "Tamale de Elote Trufado", "desc": "Sweet corn tamale, queso fresco, truffle oil, roasted poblano crema.", "price": 7.00},
            {"id": "A5", "name": "Esquites de la Casa", "desc": "Charred corn, epazote aioli, chile ash, queso fresco, tajin.", "price": 8.00},
            {"id": "A6", "name": "Empanadas", "desc": "Two flaky pastries filled with slow-cooked shredded beef.", "price": 9.00},
            {"id": "A7", "name": "Stuffed Avocados", "desc": "Avocados filled with cheese, jalapeño, chorizo, battered & fried.", "price": 13.00},
            {"id": "A8", "name": "Chilaquiles de la Casa", "desc": "Baked chips covered in house-made mole and sour cream drizzle.", "price": 12.00},
            {"id": "A9", "name": "Flor de Calabaza", "desc": "Two empanadas filled with queso and flor de calabaza.", "price": 14.00},
            {"id": "A10", "name": "Tres Cheese Tostadas", "desc": "Crisp tortillas, refried beans, three melted cheeses, pico.", "price": 9.00},
            {"id": "A11", "name": "Fried Calamari", "desc": "Lightly breaded calamari rings with house-made chipotle aioli.", "price": 14.00},
            {"id": "A12", "name": "Flautas", "desc": "Three rolled, deep-fried taquitos filled with shredded chicken.", "price": 10.00},
            {"id": "A13", "name": "Table Side Cart Special", "desc": "Appetizer trio: queso flameado, fresh guac, and roasted salsa.", "price": 17.00}
        ],
        "Soups & Salads": [
            {"id": "SS1", "name": "Ensalada Royal", "desc": "Spring mix, grape tomato, jicama, goat cheese, raspberry vinaigrette.", "price": 10.00},
            {"id": "SS2", "name": "Sopa de Tortilla", "desc": "Chipotle chicken broth, shredded chicken, crispy chips, avocado.", "price": 12.00},
            {"id": "SS3", "name": "Blackened Chicken Salad", "desc": "Crisp lettuce, blackened chicken, fire-roasted corn, black beans.", "price": 14.00},
            {"id": "SS4", "name": "El Rey Bowl", "desc": "Sautéed shrimp, greens, cucumber, corn, avocado over white rice.", "price": 15.00}
        ],
        "Entrees": [
            {"id": "E1", "name": "Tamale Plate", "desc": "Two tamales topped with chile con carne, cheese, sour cream sauce.", "price": 14.00},
            {"id": "E2", "name": "Puffy Tacos", "desc": "Three deep-fried puffy shells filled with beans and birria.", "price": 15.00},
            {"id": "E3", "name": "Rey Birria Nachos", "desc": "Crispy nachos topped with birria, queso sauce, corona sauce.", "price": 18.00},
            {"id": "E4", "name": "Reina Style Enchiladas", "desc": "Three Texas-style enchiladas with shredded chicken & melted cheese.", "price": 16.00},
            {"id": "E5", "name": "Ribeye Tacos", "desc": "Three ribeye tacos with cilantro, onion, salsa cruda, street corn.", "price": 24.00},
            {"id": "E6", "name": "Tampiqueña Real", "desc": "10 oz beef skirt, two quajillo and queso fresco enchiladas.", "price": 22.75},
            {"id": "E7", "name": "Birria Torta", "desc": "Hearty sandwich with slow-cooked birria beef on a soft telera.", "price": 16.00},
            {"id": "E8", "name": "Pollo Pibil", "desc": "Citrus & achiote marinated chicken cooked in banana leaves.", "price": 16.00},
            {"id": "E9", "name": "Mole Poblano", "desc": "Slow-cooked chicken smothered in rich mole sauce.", "price": 16.75},
            {"id": "E10", "name": "Milanesa Empanizada", "desc": "Crispy breaded chicken or beef cutlet served with Mexican rice.", "price": 16.00},
            {"id": "E11", "name": "Chile Relleno", "desc": "Roasted poblano pepper stuffed with cheese or seasoned meat.", "price": 14.75},
            {"id": "E12", "name": "Barbacoa Plate", "desc": "Slow-cooked shredded beef simmered in traditional spices.", "price": 16.00},
            {"id": "E13", "name": "Salsa Verde Carnitas", "desc": "Tender pork chunks cooked in a special house-made green sauce.", "price": 16.00},
            {"id": "E14", "name": "Burrito Mexicano", "desc": "Large tortilla, chicken fajita, sautéed onion, red bell pepper.", "price": 16.00},
            {"id": "E15", "name": "Mexican Enchiladas", "desc": "Three rolled tortillas: cheese, shredded chicken, beef.", "price": 14.75}
        ],
        "Sizzling Platters": [
            {"id": "P1", "name": "El Real Molcajete", "desc": "Sizzling molcajete with your choice of protein over smoking veggies.", "price": 19.00},
            {"id": "P2", "name": "Fajita Alambre", "desc": "Grilled beef or chicken, onions, peppers, bacon, melted cheese, pineapple.", "price": 17.75},
            {"id": "P3", "name": "Pollo a la Plancha", "desc": "Tender marinated chicken grilled on a plancha for a smoky finish.", "price": 16.75},
            {"id": "P4", "name": "Sizzling Fajitas", "desc": "Tender chicken or steak fajitas grilled over open flame.", "price": 18.75},
            {"id": "P5", "name": "Parrillada Nortena (For 2)", "desc": "Mexican-style mixed grill: Beef skirt, Chicken, Chorizo, Sausage.", "price": 39.00},
            {"id": "P6", "name": "Parrillada Nortena (For 4)", "desc": "Massive Mexican-style mixed grill served on a sizzling platter.", "price": 59.00}
        ],
        "Tacos": [
            {"id": "T1", "name": "Street Taco", "desc": "Asada, cilantro, onion, lime on corn tortillas.", "price": 3.50},
            {"id": "T2", "name": "Al Pastor", "desc": "Marinated pork, pineapple, cilantro, onion.", "price": 3.75}
        ],
        "Drinks": [
            {"id": "D1", "name": "La Reina Rita", "desc": "House gold tequila, fresh lime, agave. Rocks or Frozen.", "price": 8.99},
            {"id": "D2", "name": "Modelo Especial", "desc": "Draft or Bottle. Served chilled with a lime.", "price": 5.00}
        ],
        "Sides": [
            {"id": "S1", "name": "Street Corn", "desc": "Elote off the cob, mayo, cotija, tajin.", "price": 4.50},
            {"id": "S2", "name": "Rice & Beans", "desc": "House-made Mexican rice and refried beans.", "price": 3.99}
        ],
        "Desserts": [
            {"id": "DS1", "name": "Golden Churros", "desc": "Crispy churros tossed in cinnamon sugar.", "price": 6.50},
            {"id": "DS2", "name": "Tres Leches", "desc": "Classic sponge cake soaked in three milks.", "price": 7.00}
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

def init_session():
    if 'view_mode' not in st.session_state: st.session_state.view_mode = "kds" # Default to KDS
    if 'layout_mode' not in st.session_state: st.session_state.layout_mode = "Mobile"
    if 'cart' not in st.session_state: st.session_state.cart = []
    if 'current_cat' not in st.session_state: st.session_state.current_cat = "Appetizers"
    if 'phone_number' not in st.session_state: st.session_state.phone_number = "STAFF"
    if 'order_type' not in st.session_state: st.session_state.order_type = "DINE-IN 🍽️"

def process_order(payment_method, total_price):
    with st.spinner(f"Initiating Order Sequence..."):
        time.sleep(0.5)
        st.toast(f"Total ${total_price:.2f} Confirmed.")
    
    # FORMATTING LOGIC: 001, 002
    sales = get_sales_data()
    order_id = f"{len(sales) + 1:03}" 
    
    pts_earned = int(total_price)
    update_user_points(st.session_state.phone_number, pts_earned)
    log_transaction(order_id, st.session_state.order_type, st.session_state.cart, total_price, st.session_state.phone_number)
    st.session_state.cart = []
    st.success(f"Order #{order_id} sent to kitchen.")
    time.sleep(1)
    st.session_state.view_mode = "login"
    st.rerun()

# ==========================================
# 4. NATIVE MOBILE LOGIN ROUTER 
# ==========================================
def render_login():
    st.markdown("<br><br>", unsafe_allow_html=True)
    try: 
        st.image(SystemConfig.LOGO_PATH, use_container_width=True)
    except: 
        st.markdown(f"<h1 style='text-align:center; color:{SystemConfig.PRIMARY_COLOR}; font-family:serif; font-size: 4rem;'>{SystemConfig.RESTAURANT_NAME}</h1>", unsafe_allow_html=True)
        
    st.markdown("<h3 style='text-align:center; color:#FFF; font-size: 3.5rem; font-weight: 800; margin-bottom: 1rem; line-height: 1.2;'>ENTER<br>NUMBER</h3>", unsafe_allow_html=True)
        
    # Native Trigger: No clunky on-screen grid. Type password summons native numpad.
    entry = st.text_input("Login", key="login_entry", type="password", label_visibility="collapsed")
        
    if entry:
        if len(entry) == 6:
            if entry == "123789": # Admin Sweep
                st.session_state.view_mode = "admin"
                st.rerun()
            elif entry == "222333": # KDS Partition
                st.session_state.view_mode = "kds"
                st.rerun()
            elif entry == "111222": # Employee Triple-Tap
                st.session_state.view_mode = "ordering"
                st.session_state.phone_number = "STAFF"
                st.rerun()
            else:
                st.error("Invalid Code")
        elif len(entry) >= 10: # Customer VIP
            clean_num = entry[:10]
            sync_user_data(clean_num)
            st.session_state.phone_number = clean_num
            st.session_state.view_mode = "ordering"
            st.rerun()

# ==========================================
# 5. UNIFIED ORDERING UI (Rewards + Layout)
# ==========================================
def render_ordering_os():
    try: 
        st.image(SystemConfig.LOGO_PATH, use_container_width=True)
    except: 
        st.markdown(f"<h2 style='text-align:center; color:{SystemConfig.PRIMARY_COLOR}; margin-bottom:0;'>{SystemConfig.RESTAURANT_NAME}</h2>", unsafe_allow_html=True)

    is_mobile = st.session_state.get('layout_mode', 'Mobile') == 'Mobile'

    # STAFF PORTAL WITH DESKTOP TOGGLE INJECTION
    if st.session_state.phone_number == "STAFF":
        staff_c1, staff_c2 = st.columns([0.7, 0.3])
        with staff_c1:
            st.markdown("""<div style='background:#111; padding:15px; border-radius:8px; border:2px solid #333; margin-bottom:20px;'><h4 style='color:#D4AF37; margin:0; text-align:center;'>STAFF PORTAL</h4></div>""", unsafe_allow_html=True)
        with staff_c2:
            btn_text = "🖥️ DESKTOP VIEW" if is_mobile else "📱 MOBILE VIEW"
            if st.button(btn_text, key="staff_view_toggle", use_container_width=True):
                st.session_state.layout_mode = "Desktop" if is_mobile else "Mobile"
                st.rerun()
    else:
        pts = st.session_state.get('reward_points', 0)
        tier, target, next_t, t_color = get_tier_info(pts)
        progress = min(int((pts / target) * 100), 100)
        st.markdown(f"""
            <div class="status-engine" style="border-color: {t_color};">
                <div class="status-header"><span style="color: {t_color};">{tier} | {st.session_state.phone_number}</span><span>{pts} / {target} PTS</span></div>
                <div style="width: 100%; background: #222; height: 8px; border-radius: 4px; overflow: hidden; margin-top:10px;">
                    <div style="width: {progress}%; background: {t_color}; height: 100%;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    menu = get_master_menu()
    categories = list(menu.keys())
    
    # DYNAMIC GRID: 2 Columns for Mobile (thumb-friendly), 4 for Desktop
    num_cols = 2 if is_mobile else 4
    
    st.markdown('<div id="action-grid">', unsafe_allow_html=True)
    cols = st.columns(num_cols)
    for i, cat in enumerate(categories):
        with cols[i % num_cols]:
            style_class = "active-tab" if cat == st.session_state.current_cat else ""
            if cat == "La Reserva":
                pts = st.session_state.get('reward_points', 0)
                if pts < 5000 and st.session_state.phone_number != "STAFF":
                    st.button(f"🔒 {cat}", disabled=True, use_container_width=True); continue
                style_class = "active-reserva" if cat == st.session_state.current_cat else ""
            st.markdown(f'<div class="{style_class}">', unsafe_allow_html=True)
            if st.button(cat, key=f"tab_{cat}", use_container_width=True):
                st.session_state.current_cat = cat; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"<h3 style='margin-top: 1rem;'>{st.session_state.current_cat.upper()}</h3>", unsafe_allow_html=True)
    
    # Render Items
    for item in menu[st.session_state.current_cat]:
        st.markdown(f"""<div class="menu-card"><div><div class="item-title">{item['name']}</div><div class="item-desc">{item['desc']}</div></div><div class="price-tag">${item['price']:.2f}</div></div>""", unsafe_allow_html=True)
        if st.button(f"+ ADD {item['name']}", key=f"add_{item['id']}", use_container_width=True):
            st.session_state.cart.append(item); st.toast(f"Added {item['name']}"); st.rerun()

    # Cart Processing
    st.markdown('<div class="manifest-container"><div class="manifest-header">CURRENT ORDER</div>', unsafe_allow_html=True)
    if not st.session_state.cart: 
        st.write("YOUR SELECTIONS WILL APPEAR HERE.")
    else:
        subtotal = sum(i['price'] for i in st.session_state.cart)
        tax = subtotal * SystemConfig.TAX_RATE
        total = subtotal + tax
        for item in st.session_state.cart: 
            st.markdown(f'<div class="receipt-row"><span>{item["name"]}</span><span>${item["price"]:.2f}</span></div>', unsafe_allow_html=True)
        st.markdown(f"""<div style="margin-top: 15px; color: #666; font-size: 14px;"><div class="receipt-row"><span>Subtotal:</span><span>${subtotal:.2f}</span></div><div class="receipt-row"><span>Tax (8.5%):</span><span>${tax:.2f}</span></div></div><div class="manifest-total"><span>TOTAL</span><span>${total:.2f}</span></div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.session_state.order_type = st.radio("DESTINATION", ["DINE-IN 🍽️", "TO-GO 🛍️"], horizontal=True, label_visibility="collapsed")
        
        st.markdown("<br>", unsafe_allow_html=True)
        # Using specific styling for the final place order button
        st.markdown("""<style>div.stButton>button[key="btn_place_order"] { background-color: #6A0DAD !important; color: #FFFFFF !important; border: 2px solid #9D50BB !important; font-size: 1.8rem !important; height: 80px !important; box-shadow: 0 0 25px rgba(106, 13, 173, 0.6) !important; margin-top: 10px; }</style>""", unsafe_allow_html=True)
        if st.button("FIRE TO KITCHEN", key="btn_place_order", use_container_width=True): 
            process_order("In-Store POS", total)
            
    st.markdown('</div><br>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Clear Cart", type="secondary"): 
            st.session_state.cart = []; st.rerun()
    with col2:
        if st.button("Logout", key="btn_logout", type="secondary"): 
            st.session_state.cart = []; st.session_state.view_mode = "login"; st.rerun()

# ==========================================
# 6. KDS UI (With LIFO Spacebar Hack)
# ==========================================
def render_kds():
    inject_kds_keyboard_hack()
    
    try: 
        st.image(SystemConfig.LOGO_PATH, use_container_width=True)
    except: 
        st.markdown(f"<h2 style='text-align:center; color:{SystemConfig.PRIMARY_COLOR}; margin-bottom:0;'>{SystemConfig.RESTAURANT_NAME} KITCHEN</h2>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#333; margin-top:0;'>", unsafe_allow_html=True)
    
    all_sales = get_sales_data()
    live_tickets = [order for order in all_sales if order.get("status") == "PENDING"]
    dine_in_tickets = [t for t in live_tickets if "DINE-IN" in t['type']]
    to_go_tickets = [t for t in live_tickets if "TO-GO" in t['type']]
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("EXIT KDS", key="btn_exit_kds", type="secondary"): st.session_state.view_mode = "login"; st.rerun()
    with c2:
        is_mobile = st.session_state.get('layout_mode', 'Mobile') == 'Mobile'
        btn_text = "🖥️ DESKTOP VIEW" if is_mobile else "📱 MOBILE VIEW"
        if st.button(btn_text):
            st.session_state.layout_mode = "Desktop" if is_mobile else "Mobile"
            st.rerun()
        
    if not live_tickets: 
        st.markdown("<h2 style='text-align:center; color:#444; margin-top:50px;'>KITCHEN CLEAR. NO ACTIVE TICKETS.</h2>", unsafe_allow_html=True)
    else:
        # LIFO BUMP: Bumps the NEWEST ticket added to the array (the last one)
        newest_ticket = live_tickets[-1]
        
        # This button is explicitly marked type="primary" to be caught by the JS Spacebar Hack
        if st.button(f"BUMP NEWEST OVERALL (#{newest_ticket['order_id']}) [SPACE BAR]", key="btn_bump_newest", type="primary", use_container_width=True): 
            bump_kitchen_ticket(newest_ticket['order_id'])
            st.rerun()
            
        st.markdown("<br>", unsafe_allow_html=True)
        col_dine, col_togo = st.columns(2)
        
        with col_dine:
            st.markdown("<h3 style='color:#2E7D32; text-align:center; border-bottom: 2px solid #2E7D32; padding-bottom: 10px;'>🍽️ DINE-IN EXPO</h3>", unsafe_allow_html=True)
            if not dine_in_tickets: 
                st.markdown("<h4 style='text-align:center; color:#444; margin-top:30px;'>DINE-IN CLEAR</h4>", unsafe_allow_html=True)
            else:
                for order in dine_in_tickets:
                    item_counts = {}
                    for item in order['items']: item_counts[item] = item_counts.get(item, 0) + 1
                    formatted_items = [f"{count}x {name}" for name, count in item_counts.items()]
                    st.markdown(f"""<div class="kds-card" style="border-left-color: #2E7D32;"><div class="ticket-id"><span>#{order['order_id']}</span><span class="ticket-phone">{order.get('phone', 'UNKNOWN')}</span></div><div style="color:#888; font-size:14px; margin-bottom:10px;">{order['timestamp']}</div><div class="ticket-items">{'<br>'.join(formatted_items)}</div></div>""", unsafe_allow_html=True)
                    if st.button(f"DONE #{order['order_id']}", key=f"d_{order['order_id']}"): 
                        bump_kitchen_ticket(order['order_id'])
                        st.rerun()
                        
        with col_togo:
            st.markdown("<h3 style='color:#D32F2F; text-align:center; border-bottom: 2px solid #D32F2F; padding-bottom: 10px;'>🛍️ TO-GO BAGGING</h3>", unsafe_allow_html=True)
            if not to_go_tickets: 
                st.markdown("<h4 style='text-align:center; color:#444; margin-top:30px;'>TO-GO CLEAR</h4>", unsafe_allow_html=True)
            else:
                for order in to_go_tickets:
                    item_counts = {}
                    for item in order['items']: item_counts[item] = item_counts.get(item, 0) + 1
                    formatted_items = [f"{count}x {name}" for name, count in item_counts.items()]
                    st.markdown(f"""<div class="kds-card" style="border-left-color: #D32F2F;"><div class="ticket-id"><span>#{order['order_id']}</span><span class="ticket-phone">{order.get('phone', 'UNKNOWN')}</span></div><div style="color:#888; font-size:14px; margin-bottom:10px;">{order['timestamp']}</div><div class="ticket-items">{'<br>'.join(formatted_items)}</div></div>""", unsafe_allow_html=True)
                    if st.button(f"DONE #{order['order_id']}", key=f"t_{order['order_id']}"): 
                        bump_kitchen_ticket(order['order_id'])
                        st.rerun()
                        
    st_autorefresh(interval=10000, key="kds_refresh")

# ==========================================
# 7. ADMIN OS
# ==========================================
def render_admin_os():
    st.markdown(f"<h1 style='color:{SystemConfig.PRIMARY_COLOR};'>LA REINA // EXECUTIVE DASHBOARD</h1><hr style='border-color: #333;'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ EXIT SECURE SESSION", key="btn_exit_admin", type="secondary"): 
            st.session_state.view_mode = "login"
            st.rerun()
    with col2:
        is_mobile = st.session_state.get('layout_mode', 'Mobile') == 'Mobile'
        btn_text = "🖥️ DESKTOP VIEW" if is_mobile else "📱 MOBILE VIEW"
        if st.button(btn_text):
            st.session_state.layout_mode = "Desktop" if is_mobile else "Mobile"
            st.rerun()

    sales_data = get_sales_data()
    if not sales_data: 
        st.warning("No financial data found. The sales ledger is currently empty.")
        return

    total_rev = sum(order['total'] for order in sales_data)
    total_ords = len(sales_data)
    aov = total_rev / total_ords if total_ords > 0 else 0
    
    st.markdown("<br>", unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    with m1: st.markdown(f"""<div style='background: #1a1a1a; padding: 20px; border-radius: 8px; text-align: center; border: 1px solid #333;'><div style='color:#888;'>GROSS REVENUE</div><div style='font-size:2.5rem; font-weight:bold; color:{SystemConfig.PRIMARY_COLOR};'>${total_rev:.2f}</div></div>""", unsafe_allow_html=True)
    with m2: st.markdown(f"""<div style='background: #1a1a1a; padding: 20px; border-radius: 8px; text-align: center; border: 1px solid #333;'><div style='color:#888;'>TOTAL TICKETS</div><div style='font-size:2.5rem; font-weight:bold; color:#FFF;'>{total_ords}</div></div>""", unsafe_allow_html=True)
    with m3: st.markdown(f"""<div style='background: #1a1a1a; padding: 20px; border-radius: 8px; text-align: center; border: 1px solid #333;'><div style='color:#888;'>AVERAGE ORDER</div><div style='font-size:2.5rem; font-weight:bold; color:#FFF;'>${aov:.2f}</div></div>""", unsafe_allow_html=True)

    st.markdown(f"<h3 style='color: {SystemConfig.PRIMARY_COLOR}; margin-top: 40px;'>⚡ LIVE TRANSACTION LOG</h3><div style='background: #111; border: 1px solid #333; border-radius: 8px; padding: 20px; height: 400px; overflow-y: scroll;'>", unsafe_allow_html=True)
    for order in reversed(sales_data):
        sc = "#7FFF00" if order.get("status") == "COMPLETED" else "#FFD700"
        st.markdown(f"""<div style="border-bottom: 1px solid #222; padding-bottom: 15px; margin-bottom: 15px;"><div style="color: {SystemConfig.PRIMARY_COLOR}; font-weight: bold; font-size: 1.5rem;">ORDER #{order['order_id']} <span style="float:right; color: {sc}; font-size: 14px;">[{order.get('status', 'COMPLETED')}]</span></div><div style="color: #888; font-size: 16px; margin-top: 5px;">{order['type']} | {order.get('phone', 'N/A')} | {len(order['items'])} items | <strong style="color:#FFF;">${order['total']:.2f}</strong></div></div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st_autorefresh(interval=15000, key="admin_refresh")

# ==========================================
# 8. RUNTIME ROUTER
# ==========================================
def main():
    init_session()
    inject_styles()
    
    if st.session_state.view_mode == "login": 
        render_login()
    elif st.session_state.view_mode == "kds": 
        render_kds()
    elif st.session_state.view_mode == "admin": 
        render_admin_os()
    else: 
        render_ordering_os()

if __name__ == "__main__":
    main()
