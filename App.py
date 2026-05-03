import streamlit as st
import random
from datetime import datetime

# ==========================================
# 1. PAGE SETUP & THEME
# ==========================================
st.set_page_config(
    page_title="La Reina Margaritas",
    page_icon="👑",
    layout="wide"
)

# ==========================================
# 2. THE "GENIUS" CSS (Industrial UX)
# ==========================================
st.markdown("""
    <style>
    /* Global Background */
    .stApp {
        background-color: #000000;
    }

    /* MEGA-PILLS: The 120px tall targets for seniors */
    button[data-testid="stBaseButton-secondaryPill"] {
        min-height: 120px !important;
        min-width: 350px !important;
        font-size: 26px !important;
        font-weight: 900 !important;
        border-radius: 20px !important;
        border: 4px solid #D4AF37 !important;
        background-color: #111111 !important;
        color: #D4AF37 !important;
        margin: 15px !important;
        line-height: 1.2 !important;
        transition: all 0.2s ease-in-out !important;
    }

    /* Active Category Glow */
    button[data-testid="stBaseButton-secondaryPill"][aria-pressed="true"] {
        background-color: #D4AF37 !important;
        color: #000000 !important;
        box-shadow: 0px 0px 40px #D4AF37 !important;
        transform: translateY(-5px);
    }

    /* Green 'Add' Buttons (High-Visibility) */
    div[data-testid="stBaseButton-secondary"] {
        background-color: #84bd00 !important;
        color: white !important;
        font-size: 24px !important;
        font-weight: bold !important;
        height: 75px !important;
        width: 100% !important;
        border-radius: 15px !important;
        border: none !important;
    }

    /* Typography Overhaul */
    .stMarkdown h2 { font-size: 45px !important; color: white; text-align: center; }
    .stMarkdown h3 { font-size: 38px !important; color: #D4AF37; margin-bottom: 5px; }
    .stMarkdown p { font-size: 22px !important; color: #ffffff; line-height: 1.4; }
    
    /* Custom Scrollbar for the Kitchen */
    ::-webkit-scrollbar { width: 10px; }
    ::-webkit-scrollbar-thumb { background: #D4AF37; border-radius: 10px; }

    /* Hide Streamlit Clutter */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>

    <script>
    // JS Listener for USB Keyboard (Spacebar = BUMP)
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
# 3. DATA INITIALIZATION
# ==========================================
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'orders' not in st.session_state:
    st.session_state.orders = []

# Full Menu Dictionary (This builds the 'length' and logic)
MENU_DATA = {
    "Lunch Specials (11am-3pm)": [
        {"name": "Lunch Fajitas", "price": 13.75, "desc": "Sizzling Steak or Chicken, grilled onions & peppers. With rice, beans & tortillas."},
        {"name": "Fajita Chimichanga", "price": 12.75, "desc": "Steak & Chicken deep-fried burrito smothered in queso sauce. With rice & beans."},
        {"name": "Sopes (3)", "price": 11.50, "desc": "Three thick corn tortillas topped with beans, meat, lettuce, cheese, and cream."}
    ],
    "Antojitos & Botanas": [
        {"name": "Guacamole Dip", "price": 8.50, "desc": "Fresh avocado mixed with onions, cilantro, and lime."},
        {"name": "Queso Fundido", "price": 10.99, "desc": "Melted cheese with delicious chorizo and warm tortillas."},
        {"name": "Nachos Supremos", "price": 14.25, "desc": "Loaded with beans, cheese, jalapeños, and your choice of meat."}
    ],
    "Taqueria / Tacos": [
        {"name": "Street Tacos (3)", "price": 10.50, "desc": "Choice of Asada, Al Pastor, or Pollo with onions and cilantro."},
        {"name": "Tacos de Birria", "price": 15.00, "desc": "Slow-cooked beef with melted cheese and consomé for dipping."}
    ],
    "Platos Fuertes / Entrees": [
        {"name": "Carne Asada", "price": 18.99, "desc": "Grilled skirt steak served with rice, beans, and grilled onions."},
        {"name": "Enchiladas Verdes", "price": 14.50, "desc": "Three chicken enchiladas topped with spicy green sauce and cream."}
    ],
    "Sizzling Platters & Seafood": [
        {"name": "Camarones al Mojo", "price": 17.75, "desc": "Shrimp sautéed in garlic butter and lime."},
        {"name": "Fajitas Texanas", "price": 21.00, "desc": "Steak, chicken, and shrimp sizzling on a hot platter."}
    ],
    "Vegetarian": [
        {"name": "Veggie Burrito", "price": 11.00, "desc": "Beans, rice, lettuce, and avocado wrapped in a large flour tortilla."},
        {"name": "Spinach Enchiladas", "price": 12.50, "desc": "Fresh spinach and cheese topped with white queso."}
    ],
    "Drinks & Desserts": [
        {"name": "House Margarita", "price": 9.00, "desc": "Our signature blend of tequila, lime, and agave."},
        {"name": "Churros con Cajeta", "price": 7.50, "desc": "Fried dough pastry dusted in cinnamon sugar."}
    ]
}

# ==========================================
# 4. HEADER & LOGO
# ==========================================
_, logo_col, _ = st.columns([1, 4, 1])
with logo_col:
    st.image("la_reina_dark.png", use_container_width=True)

st.markdown("---")

# ==========================================
# 5. MAIN NAVIGATION (MEGA PILLS)
# ==========================================
st.markdown("## BROWSE OUR MENU")
selected_cat = st.pills(
    label="Categories",
    options=list(MENU_DATA.keys()),
    label_visibility="collapsed"
)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 6. MENU DISPLAY LOGIC
# ==========================================
if selected_cat:
    for item in MENU_DATA[selected_cat]:
        item_col, action_col = st.columns([3, 1])
        
        with item_col:
            st.markdown(f"### {item['name']}")
            st.write(item['desc'])
            st.markdown(f"**${item['price']:.2f}**")
        
        with action_col:
            st.write("<br>", unsafe_allow_html=True)
            if st.button(f"＋ ADD", key=f"add_{item['name']}"):
                st.session_state.cart.append(item)
                st.toast(f"Added {item['name']} to cart!")
        
        st.divider()
else:
    st.info("Select a category above to view our authentic Mexican dishes.")

# ==========================================
# 7. SIDEBAR CART & KITCHEN (THE LOGIC)
# ==========================================
with st.sidebar:
    st.markdown("<h1 style='color: #D4AF37;'>🛒 Your Order</h1>", unsafe_allow_html=True)
    
    if not st.session_state.cart:
        st.write("Your cart is empty.")
    else:
        cart_total = 0
        for i, item in enumerate(st.session_state.cart):
            c1, c2 = st.columns([4, 1])
            c1.write(f"**{item['name']}**")
            c2.write(f"${item['price']}")
            cart_total += item['price']
        
        st.divider()
        st.subheader(f"Total: ${cart_total:.2f}")
        
        if st.button("🚀 SEND TO KITCHEN", use_container_width=True):
            order_id = random.randint(1000, 9999)
            new_order = {
                "id": order_id,
                "time": datetime.now().strftime("%H:%M"),
                "items": st.session_state.cart.copy()
            }
            st.session_state.orders.append(new_order)
            st.session_state.cart = []
            st.success(f"Order #{order_id} Sent!")

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<h1 style='color: #84bd00;'>👨‍🍳 Kitchen View</h1>", unsafe_allow_html=True)
    
    if st.session_state.orders:
        next_order = st.session_state.orders[0]
        st.write(f"**CURRENT ORDER: #{next_order['id']}**")
        for oi in next_order['items']:
            st.write(f"- {oi['name']}")
        
        if st.button("🔔 BUMP ORDER (SPACEBAR)", use_container_width=True):
            st.session_state.orders.pop(0)
            st.balloons()
    else:
        st.write("No pending orders.")
