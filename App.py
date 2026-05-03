import streamlit as st
import os
import random

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="La Reina Margaritas",
    page_icon="👑",
    layout="centered"
)

# ==========================================
# 2. THE "GENIUS" CSS & JS OVERHAUL
# ==========================================
st.markdown("""
    <style>
    /* Force pure black background */
    .stApp {
        background-color: #000000 !important;
    }

    /* MEGA-PILLS: Large targets for seniors and kitchen use */
    div[data-testid="stPill"] {
        gap: 15px !important;
        justify-content: center !important;
    }

    div[data-testid="stPill"] button {
        background-color: #1a1a1a !important; 
        color: #D4AF37 !important;           
        border: 2px solid #D4AF37 !important; 
        padding: 20px 30px !important;       
        font-size: 22px !important;           
        font-weight: 800 !important;
        border-radius: 50px !important;      
        min-width: 260px !important;
        transition: all 0.3s ease-in-out !important;
    }

    /* Active Pill Glow State */
    div[data-testid="stPill"] button[aria-pressed="true"] {
        background-color: #D4AF37 !important; 
        color: #000000 !important;           
        box-shadow: 0px 0px 25px #D4AF37 !important;
        transform: scale(1.05);
    }

    /* Green 'Add' Button (High Contrast) */
    div[data-testid="stBaseButton-secondary"] {
        background-color: #84bd00 !important;
        color: white !important;
        font-size: 22px !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 10px !important;
        width: 100% !important;
    }

    /* Menu Text Styling */
    .stMarkdown h3 { 
        font-size: 34px !important; 
        color: #D4AF37 !important; 
        margin-bottom: 5px !important; 
    }
    .stMarkdown p { 
        font-size: 22px !important; 
        color: #ffffff !important; 
    }
    .price-tag { 
        font-size: 26px !important; 
        color: #84bd00 !important; 
        font-weight: bold; 
    }
    
    /* Center text helper */
    .centered-header {
        text-align: center;
        color: white;
        letter-spacing: 2px;
        margin-top: 20px;
    }

    /* Clean Dividers */
    hr { border: 1px solid #333 !important; }
    </style>

    <script>
    // USB Keyboard Spacebar Listener for the Kitchen
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
# 3. HEADER LOGO & BRANDING
# ==========================================
_, cent_co, _ = st.columns([1, 5, 1])
with cent_co:
    # FILENAME MUST BE EXACTLY THIS ON GITHUB
    logo_file = "la_reina_dark.png" 
    
    if os.path.exists(logo_file):
        st.image(logo_file, use_container_width=True)
    else:
        st.markdown("<h1 style='text-align: center; color: #D4AF37;'>LA REINA MARGARITAS</h1>", unsafe_allow_html=True)
        st.warning(f"Note: '{logo_file}' not detected. Upload it to GitHub to see the logo.")

st.markdown("<h2 class='centered-header'>BROWSE OUR MENU</h2>", unsafe_allow_html=True)
st.divider()

# ==========================================
# 4. DATA & SESSION INITIALIZATION
# ==========================================
if 'cart' not in st.session_state:
    st.session_state.cart = []

# ==========================================
# 5. NAVIGATION (FULL PILL LIST)
# ==========================================
category = st.pills(
    label="Categories",
    options=[
        "Lunch Specials (11am-3pm)", 
        "Antojitos & Botanas", 
        "Taqueria / Tacos", 
        "Platos Fuertes / Entrees", 
        "Sizzling Platters & Seafood", 
        "Vegetarian", 
        "Drinks & Desserts"
    ],
    label_visibility="collapsed"
)

# ==========================================
# 6. MENU DATABASE
# ==========================================
MENU = {
    "Lunch Specials (11am-3pm)": [
        {"name": "Lunch Fajitas", "price": 13.75, "desc": "Sizzling Steak or Chicken, grilled onions & peppers. With rice, beans & tortillas."},
        {"name": "Fajita Chimichanga", "price": 12.75, "desc": "Steak & Chicken deep-fried burrito smothered in queso sauce. With rice & beans."},
        {"name": "Sopes (3)", "price": 11.50, "desc": "Three thick corn tortillas topped with beans, meat, lettuce, cheese, and cream."}
    ],
    "Antojitos & Botanas": [
        {"name": "Guacamole Dip", "price": 8.50, "desc": "Fresh avocado mixed with onions, cilantro, and lime."},
        {"name": "Queso Fundido", "price": 10.99, "desc": "Melted cheese with chorizo and warm tortillas."},
        {"name": "Nachos La Reina", "price": 12.50, "desc": "Chips topped with queso, beans, jalapeños, and your choice of meat."}
    ],
    "Taqueria / Tacos": [
        {"name": "Street Tacos (3)", "price": 10.50, "desc": "Choice of meat, onions, cilantro, and fresh salsa on corn tortillas."},
        {"name": "Tacos de Birria", "price": 13.99, "desc": "Slow-cooked beef with melted cheese and consommé for dipping."}
    ],
    "Platos Fuertes / Entrees": [
        {"name": "Carne Asada", "price": 18.99, "desc": "Grilled skirt steak served with rice, beans, and fresh tortillas."},
        {"name": "Enchiladas Verdes", "price": 14.50, "desc": "Three chicken enchiladas topped with salsa verde and crema."}
    ],
    "Sizzling Platters & Seafood": [
        {"name": "Shrimp Fajitas", "price": 19.50, "desc": "Large shrimp grilled with peppers and onions on a sizzling skillet."},
        {"name": "Camarones al Mojo de Ajo", "price": 17.99, "desc": "Shrimp sautéed in a garlic butter sauce."}
    ],
    "Vegetarian": [
        {"name": "Veggie Burrito", "price": 11.99, "desc": "Loaded with beans, rice, grilled veggies, and guacamole."},
        {"name": "Cheese Quesadilla", "price": 9.50, "desc": "Large flour tortilla with melted cheese and a side of sour cream."}
    ],
    "Drinks & Desserts": [
        {"name": "House Margarita", "price": 9.00, "desc": "Our signature blend of tequila, lime, and agave."},
        {"name": "Fried Ice Cream", "price": 6.50, "desc": "Vanilla ice cream with a crunchy coating, topped with chocolate syrup."}
    ]
}

# ==========================================
# 7. DISPLAY LOGIC
# ==========================================
if category:
    st.markdown(f"<h2 style='color: #D4AF37;'>{category}</h2>", unsafe_allow_html=True)
    for item in MENU[category]:
        col_info, col_act = st.columns([3, 1])
        with col_info:
            st.markdown(f"### {item['name']}")
            st.write(item['desc'])
            st.markdown(f"<span class='price-tag'>${item['price']:.2f}</span>", unsafe_allow_html=True)
        with col_act:
            st.write(" ") # Visual padding
            if st.button("＋ Add", key=f"btn_{item['name']}"):
                st.session_state.cart.append(item)
                st.toast(f"Added {item['name']} to cart!")
        st.divider()
else:
    st.markdown("<p style='text-align: center; color: #D4AF37; font-size: 24px; margin-top: 50px;'>Select a category above to begin your order.</p>", unsafe_allow_html=True)

# ==========================================
# 8. SIDEBAR CART & CHECKOUT
# ==========================================
with st.sidebar:
    if os.path.exists(logo_file):
        st.image(logo_file, use_container_width=True)
    st.header("🛒 Your Order")
    
    if not st.session_state.cart:
        st.write("Your cart is currently empty.")
    else:
        total = sum(i['price'] for i in st.session_state.cart)
        for i, item in enumerate(st.session_state.cart):
            st.write(f"**{item['name']}** - ${item['price']:.2f}")
        
        st.divider()
        st.subheader(f"Total: ${total:.2f}")
        
        if st.button("Submit Order", use_container_width=True):
            st.balloons()
            st.success("Order sent to the kitchen!")
            # Clear cart after submission
            st.session_state.cart = []

    st.divider()
    st.write("Questions? Ask the staff!")
