import streamlit as st
import os
from datetime import datetime
import pandas as pd

# 1. SYSTEM CONFIGURATION
st.set_page_config(
    page_title="La Reina Margaritas",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. THE "GENIUS" CSS & JS ENGINE
# This section handles the UX for older users and the USB Keyboard listener
st.markdown("""
    <style>
    /* Dark Theme & Gold Accents */
    .stApp { background-color: #0E1117; }
    
    /* Mega-Pill Category Buttons (High-Visibility for Seniors) */
    div[data-testid="stBaseButton-secondaryPill"] {
        padding: 20px 40px !important;
        font-size: 24px !important;
        font-weight: 800 !important;
        border-radius: 60px !important;
        margin: 10px !important;
        border: 2px solid #D4AF37 !important;
        background-color: #1A1C23 !important;
        color: white !important;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
    }
    
    /* Selected Pill State */
    div[data-testid="stBaseButton-secondaryPill"][aria-pressed="true"] {
        background-color: #D4AF37 !important;
        color: black !important;
    }

    /* Green 'Add' Buttons (High-Contrast) */
    div[data-testid="stBaseButton-secondary"] {
        background-color: #84bd00 !important;
        color: white !important;
        font-size: 22px !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 15px !important;
    }

    /* Kitchen Card Design */
    .kds-card {
        background-color: #1E1E1E;
        border: 4px solid #D4AF37;
        padding: 25px;
        border-radius: 20px;
        margin-bottom: 20px;
    }
    
    /* Font Sizing */
    .stMarkdown h3 { font-size: 36px !important; color: #D4AF37 !important; }
    .stMarkdown p { font-size: 22px !important; color: #E0E0E0 !important; }
    </style>

    <script>
    /* USB Keyboard 'Spacebar' Bump Listener */
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

# 3. DATA PERSISTENCE (Orders & Cart)
if 'orders' not in st.session_state: st.session_state.orders = []
if 'cart' not in st.session_state: st.session_state.cart = []

# 4. SELF-HEALING HEADER (Prevents the MediaFileStorageError)
LOGO_FILE = "la_reina_horizontal.png"

def display_header():
    left, center, right = st.columns([1, 5, 1])
    with center:
        if os.path.exists(LOGO_FILE):
            st.image(LOGO_FILE, use_container_width=True)
        else:
            # Fallback if GitHub file naming is wrong
            st.markdown(f"<h1 style='text-align: center; color: #D4AF37;'>La Reina Margaritas</h1>", unsafe_allow_html=True)
            with st.expander("🛠️ DEBUG: LOGO NOT FOUND"):
                st.error(f"App is looking for: '{LOGO_FILE}'")
                st.write("Files found in your GitHub:")
                st.code(os.listdir("."))

# 5. SIDEBAR MODE SWITCH
with st.sidebar:
    st.header("Admin Panel")
    app_mode = st.radio("View Mode", ["Customer Menu", "Kitchen (KDS)"])
    st.divider()
    if app_mode == "Customer Menu":
        st.subheader("🛒 Current Cart")
        if not st.session_state.cart:
            st.write("Cart is empty")
        else:
            total = sum(i['price'] for i in st.session_state.cart)
            for item in st.session_state.cart:
                st.write(f"- {item['name']} (${item['price']})")
            st.divider()
            st.subheader(f"Total: ${total:.2f}")
            if st.button("🚀 SUBMIT ORDER"):
                new_order = {
                    "id": len(st.session_state.orders) + 1,
                    "items": [i['name'] for i in st.session_state.cart],
                    "time": datetime.now().strftime("%I:%M %p")
                }
                st.session_state.orders.append(new_order)
                st.session_state.cart = []
                st.success("Order Sent!")
                st.balloons()

# 6. APP MODES
if app_mode == "Customer Menu":
    display_header()
    st.divider()

    # Full Menu Data Structure
    MENU = {
        "Lunch Specials (11am-3pm)": [
            {"name": "Lunch Fajitas", "price": 13.75, "desc": "Sizzling Steak or Chicken, grilled onions & peppers. With rice, beans & tortillas."},
            {"name": "Fajita Chimichanga", "price": 12.75, "desc": "Deep-fried burrito smothered in queso sauce. With rice & beans."},
            {"name": "Sopes (3)", "price": 11.50, "desc": "Three thick corn tortillas topped with beans, meat, lettuce, and cream."}
        ],
        "Antojitos & Botanas": [
            {"name": "Guacamole Real", "price": 9.50, "desc": "Freshly made avocado dip with cilantro and lime."},
            {"name": "Nachos La Reina", "price": 14.00, "desc": "Loaded with queso, beans, jalapeños, and choice of meat."}
        ],
        "Taqueria / Tacos": [
            {"name": "Street Tacos (3)", "price": 12.00, "desc": "Choice of Asada, Pollo, or Al Pastor on corn tortillas."},
            {"name": "Tacos de Birria", "price": 15.00, "desc": "Three slow-cooked beef tacos with consome."}
        ]
        # Add Platos Fuertes, Seafood, Vegetarian, etc. here following the same pattern
    }

    # Navigation Pills
    category = st.pills("Categories", options=list(MENU.keys()), label_visibility="collapsed")

    if category:
        st.markdown(f"## {category}")
        for item in MENU[category]:
            c1, c2 = st.columns([4, 1])
            with c1:
                st.markdown(f"### {item['name']}")
                st.write(item['desc'])
                st.markdown(f"**${item['price']:.2f}**")
            with c2:
                st.write("###") # Vertical alignment
                if st.button("＋ Add", key=f"add_{item['name']}"):
                    st.session_state.cart.append(item)
                    st.toast(f"Added {item['name']}!")
            st.divider()
    else:
        st.info("Select a category above to view our menu.")

elif app_mode == "Kitchen (KDS)":
    st.title("👨‍🍳 Kitchen Queue")
    st.write("Commands: Use **Spacebar** to BUMP the oldest order.")
    
    if not st.session_state.orders:
        st.header("No pending orders. Good job!")
    else:
        # 3-Column Kitchen Grid
        k_cols = st.columns(3)
        for idx, order in enumerate(st.session_state.orders):
            with k_cols[idx % 3]:
                st.markdown(f"""
                    <div class="kds-card">
                        <h2 style='color:#D4AF37;'>ORDER #{order['id']}</h2>
                        <p style='font-size:18px;'><b>Received:</b> {order['time']}</p>
                        <hr>
                        <ul style='font-size:22px; font-weight:bold;'>
                            {''.join([f"<li>{i}</li>" for i in order['items']])}
                        </ul>
                    </div>
                """, unsafe_allow_html=True)
                
                # First order gets the SPACEBAR BUMP trigger
                button_label = f"BUMP #{order['id']}" if idx == 0 else f"Complete #{order['id']}"
                if st.button(button_label, key=f"kds_{order['id']}", use_container_width=True):
                    st.session_state.orders.pop(idx)
                    st.rerun()
