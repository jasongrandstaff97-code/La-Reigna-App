import streamlit as st
import pandas as pd
from datetime import datetime

# 1. PAGE SETUP
st.set_page_config(
    page_title="La Reina Margaritas | Ordering",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. THE "GENIUS" CSS (Branding, Accessibility, & High-UX)
st.markdown("""
    <style>
    /* Dark Theme Core */
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    
    /* Mega-Pills for Navigation */
    div[data-testid="stBaseButton-secondaryPill"] {
        padding: 15px 25px !important;
        font-size: 20px !important;
        font-weight: 800 !important;
        border-radius: 50px !important;
        border: 2px solid #D4AF37 !important;
        background-color: #1A1C23 !important;
        transition: 0.3s;
    }
    div[data-testid="stBaseButton-secondaryPill"]:hover {
        transform: scale(1.05);
        background-color: #D4AF37 !important;
        color: black !important;
    }

    /* Green 'Add' Buttons */
    .stButton > button {
        background-color: #84bd00 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        height: 3em !important;
        width: 100% !important;
    }

    /* Kitchen Card Styling */
    .kds-card {
        background-color: #1E1E1E;
        border: 3px solid #D4AF37;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 15px;
    }
    
    /* Header Text Styling */
    h1, h2, h3 { color: #D4AF37 !important; font-family: 'Georgia', serif; }
    </style>
    
    <script>
    /* USB Keyboard Listener for Kitchen 'Bump' Bar */
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

# 3. DATA INITIALIZATION (The "Engine")
if 'orders' not in st.session_state:
    st.session_state.orders = [] # Current active orders for the kitchen
if 'cart' not in st.session_state:
    st.session_state.cart = [] # User's current shopping cart

# Full Menu Dictionary
MENU = {
    "Lunch Specials (11am-3pm)": [
        {"name": "Lunch Fajitas", "price": 13.75, "desc": "Sizzling Steak or Chicken, grilled onions & peppers. With rice, beans & tortillas."},
        {"name": "Fajita Chimichanga", "price": 12.75, "desc": "Deep-fried burrito smothered in queso sauce. With rice & beans."},
        {"name": "Sopes (3)", "price": 11.50, "desc": "Three thick corn tortillas topped with beans, meat, lettuce, and cheese."}
    ],
    "Antojitos & Botanas": [
        {"name": "Guacamole Real", "price": 9.50, "desc": "Made fresh at your table with avocado, jalapeño, and lime."},
        {"name": "Queso Fundido", "price": 11.00, "desc": "Melted Chihuahua cheese with Mexican chorizo."},
        {"name": "Nachos La Reina", "price": 14.25, "desc": "Loaded with beans, cheese, jalapeños, and your choice of meat."}
    ],
    "Taqueria / Tacos": [
        {"name": "Street Tacos (3)", "price": 12.00, "desc": "Choice of Asada, Al Pastor, or Pollo. Topped with cilantro & onion."},
        {"name": "Tacos de Birria", "price": 15.50, "desc": "Three slow-cooked beef tacos with consome and melted cheese."}
    ],
    "Platos Fuertes / Entrees": [
        {"name": "Carne Asada", "price": 19.99, "desc": "Grilled skirt steak served with grilled onions and cactus."},
        {"name": "Enchiladas Verdes", "price": 16.50, "desc": "Three chicken enchiladas topped with salsa verde and crema."}
    ],
    "Sizzling Platters & Seafood": [
        {"name": "Camarones al Mojo", "price": 18.75, "desc": "Sautéed shrimp in a garlic butter sauce served with white rice."},
        {"name": "Fajitas Texanas", "price": 22.00, "desc": "Steak, Chicken, and Shrimp sizzling with peppers and onions."}
    ],
    "Vegetarian": [
        {"name": "Veggie Burrito", "price": 12.50, "desc": "Filled with grilled veggies, beans, and topped with salsa ranchera."},
        {"name": "Spinach Enchiladas", "price": 13.00, "desc": "Three spinach and mushroom enchiladas with white cheese sauce."}
    ],
    "Drinks & Desserts": [
        {"name": "The Queen Margarita", "price": 12.00, "desc": "House specialty with 100% Agave Tequila and fresh lime."},
        {"name": "Flan Casero", "price": 7.50, "desc": "Traditional Mexican vanilla custard with caramel glaze."}
    ]
}

# 4. SIDEBAR - Navigation Mode
with st.sidebar:
    st.image("la_reina_horizontal.png", use_container_width=True)
    mode = st.radio("System Mode", ["Customer Menu", "Kitchen Display (KDS)"])
    st.divider()
    
    if mode == "Customer Menu":
        st.subheader("🛒 Your Order")
        if not st.session_state.cart:
            st.info("Your cart is empty")
        else:
            total = 0
            for i, item in enumerate(st.session_state.cart):
                st.write(f"**{item['name']}** (${item['price']})")
                total += item['price']
            st.divider()
            st.subheader(f"Total: ${total:.2f}")
            if st.button("Place Order"):
                new_order = {
                    "id": len(st.session_state.orders) + 1,
                    "items": [i['name'] for i in st.session_state.cart],
                    "time": datetime.now().strftime("%H:%M")
                }
                st.session_state.orders.append(new_order)
                st.session_state.cart = []
                st.balloons()
                st.success("Sent to Kitchen!")

# 5. MAIN CONTENT - MODE SWITCHING
if mode == "Customer Menu":
    # Centered Header Logo
    _, center, _ = st.columns([1, 4, 1])
    with center:
        st.image("la_reina_horizontal.png", use_container_width=True)
    
    st.divider()

    # Category Selection
    selected_cat = st.pills(
        "Menu",
        options=list(MENU.keys()),
        label_visibility="collapsed"
    )

    # Menu Display
    if selected_cat:
        st.header(selected_cat)
        for item in MENU[selected_cat]:
            with st.container():
                col_info, col_act = st.columns([4, 1])
                with col_info:
                    st.subheader(item['name'])
                    st.write(item['desc'])
                    st.markdown(f"**${item['price']:.2f}**")
                with col_act:
                    st.write("###") # Vertical alignment
                    if st.button("＋ Add", key=f"add_{item['name']}"):
                        st.session_state.cart.append(item)
                        st.toast(f"Added {item['name']}!")
                st.divider()
    else:
        st.info("Select a category above to start your order.")

elif mode == "Kitchen Display (KDS)":
    st.title("👨‍🍳 Kitchen Queue")
    st.write("Press **SPACEBAR** on the USB keyboard to BUMP the oldest order.")
    
    if not st.session_state.orders:
        st.header("All clear! No pending orders.")
    else:
        # Create a grid for orders
        cols = st.columns(3)
        for idx, order in enumerate(st.session_state.orders):
            with cols[idx % 3]:
                st.markdown(f"""
                <div class="kds-card">
                    <h2>Order #{order['id']}</h2>
                    <p><b>Time:</b> {order['time']}</p>
                    <hr>
                    <ul>
                        {''.join([f"<li>{item}</li>" for item in order['items']])}
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                
                # The Bump Button (Hidden label, Spacebar triggers the first one)
                if idx == 0:
                    if st.button(f"BUMP ORDER #{order['id']}", type="primary"):
                        st.session_state.orders.pop(0)
                        st.rerun()
                else:
                    if st.button(f"Complete #{order['id']}", key=f"done_{idx}"):
                        st.session_state.orders.pop(idx)
                        st.rerun()
