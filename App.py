import streamlit as st
import os
import time
import datetime

# ==========================================
# 1. THE "GLOBAL BRAIN" (Shared Database)
# ==========================================
# st.cache_resource keeps this data alive across ALL users/devices
@st.cache_resource
def get_global_order_db():
    return []

orders_db = get_global_order_db()

# ==========================================
# 2. PAGE CONFIG & ASSETS
# ==========================================
st.set_page_config(page_title="La Reina Margaritas", page_icon="👑", layout="wide")

# Local User Assets (Personal Spend & Cart)
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'total_spend' not in st.session_state:
    st.session_state.total_spend = 0.0

# ==========================================
# 3. THE "GENIUS" UI & JS ENGINE
# ==========================================
st.markdown("""
    <style>
    /* Global Aesthetic */
    .stApp { background-color: #000000 !important; }
    
    /* REWARDS CONTAINER */
    .rewards-box {
        background-color: #111;
        border: 2px solid #D4AF37;
        padding: 15px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
    }

    /* KITCHEN CARD SYSTEM */
    .kds-card {
        background-color: #0a0a0a;
        border: 3px solid #84bd00;
        border-radius: 20px;
        padding: 25px;
        margin: 10px;
        box-shadow: 0px 5px 15px rgba(132, 189, 0, 0.2);
    }
    .kds-header { color: #84bd00; font-size: 32px; font-weight: 900; }
    .kds-items { color: #ffffff; font-size: 24px; font-family: monospace; }
    .kds-time { color: #555; font-size: 14px; }

    /* MEGA PILLS */
    div[data-testid="stPill"] button {
        background-color: #1a1a1a !important; 
        color: #D4AF37 !important;           
        border: 2px solid #D4AF37 !important; 
        font-size: 20px !important;           
        border-radius: 50px !important;
        padding: 10px 20px !important;      
    }
    </style>

    <script>
    // THE SPACEBAR BUMP LISTENER
    const doc = window.parent.document;
    doc.addEventListener('keydown', function(e) {
        if (e.code === 'Space') {
            const buttons = Array.from(doc.querySelectorAll('button'));
            const bumpBtn = buttons.find(el => el.innerText.includes('BUMP'));
            if (bumpBtn) { bumpBtn.click(); }
        }
    });
    </script>
""", unsafe_allow_html=True)

# ==========================================
# 4. SHARED FUNCTIONS
# ==========================================
def play_ding():
    audio_url = "https://www.soundjay.com/buttons/beep-07a.mp3" 
    st.components.v1.html(f'<audio autoplay><source src="{audio_url}"></audio>', height=0)

logo_file = "la_reina_dark.png"

# ==========================================
# 5. ROUTING LOGIC (Separate Entities)
# ==========================================
# Check if URL ends in ?view=kitchen
query_params = st.query_params

if query_params.get("view") == "kitchen":
    # ------------------------------------------
    # KITCHEN ENTITY (The Fire TV View)
    # ------------------------------------------
    st.markdown("<h1 style='color: #84bd00; text-align:center;'>LIVE KITCHEN FEED</h1>", unsafe_allow_html=True)
    
    # New Order Notification Logic
    if 'prev_count' not in st.session_state:
        st.session_state.prev_count = len(orders_db)
    
    if len(orders_db) > st.session_state.prev_count:
        play_ding()
        st.session_state.prev_count = len(orders_db)

    if not orders_db:
        st.info("Kitchen is clear. Good job team.")
    else:
        # Display orders in a 3-column grid for the TV
        cols = st.columns(3)
        for idx, order in enumerate(orders_db):
            col_idx = idx % 3
            with cols[col_idx]:
                st.markdown(f"""
                    <div class="kds-card">
                        <div class="kds-header">#{order['id']}</div>
                        <div class="kds-items">{order['items']}</div>
                        <div class="kds-time">{order['time']}</div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"BUMP #{order['id']}", key=f"bump_{order['time']}"):
                    orders_db.pop(idx)
                    st.session_state.prev_count -= 1
                    st.rerun()

    # Self-refresh every 10 seconds to pull new orders from the "Global Brain"
    time.sleep(10)
    st.rerun()

else:
    # ------------------------------------------
    # CUSTOMER ENTITY (The Phone View)
    # ------------------------------------------
    
    # Logo Fallback Logic
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        if os.path.exists(logo_file):
            st.image(logo_file, use_container_width=True)
        else:
            st.markdown("<h1 style='color: #D4AF37; text-align:center;'>LA REINA</h1>", unsafe_allow_html=True)
    
    # Rewards Bar Logic
    def get_heat_status(spend):
        if spend < 50: return "Poblano 🫑", "#4CBB17", 33
        if spend < 150: return "Jalapeño 🌶️", "#FFD700", 66
        return "Habanero 🔥", "#FF4500", 100

    h_name, h_color, h_val = get_heat_status(st.session_state.total_spend)
    
    st.markdown(f"""
        <div class="rewards-box" style="border-color: {h_color};">
            <span style="color: white; font-size: 14px;">STATUS:</span> 
            <span style="color: {h_color}; font-weight: bold; font-size: 20px;">{h_name}</span>
        </div>
    """, unsafe_allow_html=True)
    st.progress(h_val / 100)

    st.divider()

    # Menu Categories
    cat = st.pills("Menu", ["Tacos", "Entrees", "Drinks"], label_visibility="collapsed")
    MENU = {
        "Tacos": [{"n": "Street Tacos", "p": 10.50}, {"n": "Birria Tacos", "p": 13.99}],
        "Entrees": [{"n": "Carne Asada", "p": 18.99}],
        "Drinks": [{"n": "House Margarita", "p": 9.00}]
    }

    if cat:
        for item in MENU[cat]:
            c1, c2 = st.columns([4, 1])
            c1.markdown(f"**{item['n']}** — ${item['p']}")
            if c2.button("＋", key=f"add_{item['n']}"):
                st.session_state.cart.append(item)
                st.toast(f"{item['n']} added!")

    # Sidebar Cart
    with st.sidebar:
        st.header("🛒 Order Summary")
        if not st.session_state.cart:
            st.write("Cart is empty.")
        else:
            total = sum(i['p'] for i in st.session_state.cart)
            for i in st.session_state.cart:
                st.write(f"• {i['n']} (${i['p']})")
            
            st.subheader(f"Total: ${total:.2f}")
            if st.button("SEND TO KITCHEN", use_container_width=True):
                # Push order to Global Brain
                new_ticket = {
                    "id": len(orders_db) + 101,
                    "items": "<br>".join([i['n'] for i in st.session_state.cart]),
                    "time": datetime.datetime.now().strftime("%I:%M %p")
                }
                orders_db.append(new_ticket)
                st.session_state.total_spend += total
                st.session_state.cart = []
                st.balloons()
                st.rerun()
