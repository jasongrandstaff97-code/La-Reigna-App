import streamlit as st
import os
import time

# ==========================================
# 1. PAGE CONFIG & ASSETS
# ==========================================
st.set_page_config(page_title="La Reina Margaritas", page_icon="👑", layout="wide")

# Initialize Session States
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'total_spend' not in st.session_state:
    st.session_state.total_spend = 0.0
if 'orders_db' not in st.session_state:
    st.session_state.orders_db = []

# ==========================================
# 2. THE REWARDS LOGIC (Heat Scale)
# ==========================================
def get_status(spend):
    if spend < 50:
        return "Poblano 🫑", "#4CBB17", 33  # Mild Green
    elif spend < 150:
        return "Jalapeño 🌶️", "#FFD700", 66  # Spicy Gold
    else:
        return "Habanero 🔥", "#FF4500", 100 # Extreme Orange-Red

status_name, status_color, progress_val = get_status(st.session_state.total_spend)

# ==========================================
# 3. CSS & JS (The "Genius" UI)
# ==========================================
st.markdown(f"""
    <style>
    /* Global Pure Black */
    .stApp {{ background-color: #000000 !important; }}

    /* REWARDS BAR STYLING */
    .rewards-container {{
        background-color: #111;
        border: 2px solid {status_color};
        padding: 15px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0px 0px 15px {status_color}44;
    }}
    .status-text {{
        font-size: 24px;
        font-weight: 800;
        color: {status_color};
        text-transform: uppercase;
        letter-spacing: 2px;
    }}

    /* MEGA-PILLS */
    div[data-testid="stPill"] button {{
        background-color: #1a1a1a !important; 
        color: #D4AF37 !important;           
        border: 2px solid #D4AF37 !important; 
        padding: 15px 25px !important;       
        font-size: 18px !important;           
        border-radius: 50px !important;      
    }}

    /* GREEN ADD BUTTONS */
    div[data-testid="stBaseButton-secondary"] {{
        background-color: #84bd00 !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
        width: 100% !important;
    }}
    </style>

    <script>
    // The "Legendary" Spacebar Bump Bar Listener
    const doc = window.parent.document;
    doc.addEventListener('keydown', function(e) {{
        if (e.code === 'Space') {{
            const buttons = Array.from(doc.querySelectorAll('button'));
            const bumpBtn = buttons.find(el => el.innerText.includes('BUMP'));
            if (bumpBtn) {{ bumpBtn.click(); }}
        }}
    }});
    </script>
""", unsafe_allow_html=True)

# ==========================================
# 4. SIDEBAR (The Loyalty Dashboard)
# ==========================================
with st.sidebar:
    st.markdown(f"""
        <div class="rewards-container">
            <p style="color: white; margin-bottom: 5px;">Loyalty Status</p>
            <div class="status-text">{status_name}</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.progress(progress_val / 100)
    st.write(f"**Total Spend:** ${st.session_state.total_spend:.2f}")
    
    if st.session_state.total_spend < 150:
        next_tier = 50 if st.session_state.total_spend < 50 else 150
        st.caption(f"Spend ${next_tier - st.session_state.total_spend:.2f} more to level up your heat!")

    st.divider()
    st.header("🛒 Your Cart")
    if not st.session_state.cart:
        st.write("Cart is empty.")
    else:
        for item in st.session_state.cart:
            st.write(f"• {item['name']} (${item['price']})")
        
        if st.button("Submit Order", use_container_width=True):
            # Logic: Move cart to KDS and update spend
            new_order = {
                "id": int(time.time()),
                "items": [i['name'] for i in st.session_state.cart],
                "total": sum(i['price'] for i in st.session_state.cart)
            }
            st.session_state.orders_db.append(new_order)
            st.session_state.total_spend += new_order['total']
            st.session_state.cart = []
            st.balloons()
            st.rerun()

# ==========================================
# 5. MAIN MENU (Standardized Template)
# ==========================================
st.markdown("<h1 style='text-align: center; color: #D4AF37;'>LA REINA MARGARITAS</h1>", unsafe_allow_html=True)

category = st.pills("Menu", ["Tacos", "Entrees", "Drinks"], label_visibility="collapsed")

MENU = {
    "Tacos": [{"name": "Street Tacos", "price": 10.50, "desc": "Authentic corn tortilla mix."}],
    "Entrees": [{"name": "Carne Asada", "price": 18.99, "desc": "Grilled skirt steak."}],
    "Drinks": [{"name": "House Margarita", "price": 9.00, "desc": "The local legend."}]
}

if category:
    for item in MENU[category]:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### {item['name']}")
            st.write(f"{item['desc']} — **${item['price']}**")
        with col2:
            if st.button("＋ Add", key=f"add_{item['name']}"):
                st.session_state.cart.append(item)
                st.toast(f"Added {item['name']}!")

# ==========================================
# 6. KITCHEN DISPLAY (Toggle for Admin)
# ==========================================
if st.checkbox("Show KDS (Kitchen Display)"):
    st.divider()
    st.markdown("<h2 style='color: #84bd00;'>KITCHEN FEED</h2>", unsafe_allow_html=True)
    if not st.session_state.orders_db:
        st.info("No pending orders.")
    else:
        for idx, order in enumerate(st.session_state.orders_db):
            cols = st.columns([4, 1])
            cols[0].write(f"**ORDER #{idx+1}**: {', '.join(order['items'])}")
            if cols[1].button("BUMP", key=f"bump_{order['id']}"):
                st.session_state.orders_db.pop(idx)
                st.rerun()
