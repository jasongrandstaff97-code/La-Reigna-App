import streamlit as st
import random

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="La Reina Margaritas",
    page_icon="👑",
    layout="centered"
)

# 2. THE "HEAVYWEIGHT" CSS & JS
# We are forcing the UI to be dark, the buttons to be huge, and the layout to stay clean.
st.markdown("""
    <style>
    /* Force total black background for the whole app */
    .stApp {
        background-color: #000000 !important;
    }

    /* MEGA-PILLS: Removing the white bars and making them massive targets */
    div[data-testid="stPill"] {
        gap: 20px !important;
        justify-content: center !important;
    }

    div[data-testid="stPill"] button {
        background-color: #1a1a1a !important; /* Dark Gray button */
        color: #D4AF37 !important;           /* Gold Text */
        border: 2px solid #D4AF37 !important; /* Gold Border */
        padding: 25px 45px !important;       /* Deep vertical padding */
        font-size: 26px !important;           /* Huge readable text */
        font-weight: 900 !important;
        border-radius: 15px !important;      /* Blocky modern look */
        min-width: 380px !important;         /* THE FIX: Definitely not 145. Massive width for long titles */
        transition: all 0.2s ease-in-out !important;
        margin-bottom: 10px !important;
    }

    /* Active/Selected Pill State with Glow */
    div[data-testid="stPill"] button[aria-pressed="true"] {
        background-color: #D4AF37 !important; /* Gold Background */
        color: #000000 !important;           /* Black Text */
        box-shadow: 0px 0px 30px #D4AF37 !important; /* The 'Genius' Glow */
        transform: translateY(-5px);
    }

    /* Hover effect for better UX */
    div[data-testid="stPill"] button:hover {
        border-color: #ffffff !important;
        color: #ffffff !important;
    }

    /* The Green 'Add' Buttons (Matching your photo exactly) */
    div[data-testid="stBaseButton-secondary"] {
        background-color: #84bd00 !important;
        color: white !important;
        font-size: 24px !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 15px !important;
        width: 100% !important;
        transition: 0.2s !important;
    }

    div[data-testid="stBaseButton-secondary"]:hover {
        background-color: #6a9600 !important;
        transform: scale(1.02);
    }

    /* Typography Polish for Readability */
    .stMarkdown h3 { font-size: 38px !important; color: #D4AF37 !important; margin-bottom: 5px !important; }
    .stMarkdown p { font-size: 22px !important; color: #ffffff !important; line-height: 1.4 !important; }
    .price-tag { font-size: 28px !important; color: #84bd00 !important; font-weight: 900 !important; }
    
    /* Clean up the sidebar */
    section[data-testid="stSidebar"] {
        background-color: #111 !important;
    }
    </style>

    <script>
    // USB Keyboard Spacebar Listener (The Bump Bar hack for the RV)
    const doc = window.parent.document;
    doc.addEventListener('keydown', function(e) {
        if (e.code === 'Space') {
            const buttons = Array.from(doc.querySelectorAll('button'));
            // Look for a button that contains 'CLEAR' or 'BUMP'
            const bumpBtn = buttons.find(el => el.innerText.includes('BUMP') || el.innerText.includes('CLEAR'));
            if (bumpBtn) { bumpBtn.click(); }
        }
    });
    </script>
""", unsafe_allow_html=True)

# 3. HEADER LOGO
# This keeps the widescreen logo centered and prominent
_, cent_co, _ = st.columns([1, 5, 1])
with cent_co:
    # This calls your dark-theme logo file
    st.image("la_reina_dark.png", use_container_width=True)

st.markdown("<h2 style='text-align: center; color: white; letter-spacing: 5px; font-weight: 300;'>MENU SELECTION</h2>", unsafe_allow_html=True)
st.divider()

# 4. SESSION STATE (Cart Logic)
if 'cart' not in st.session_state:
    st.session_state.cart = []

# 5. NAVIGATION (Full Categories List)
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

# 6. FULL MENU DATA
MENU_DATA = {
    "Lunch Specials (11am-3pm)": [
        {"name": "Lunch Fajitas", "price": 13.75, "desc": "Sizzling Steak or Chicken, grilled onions & peppers. With rice, beans & tortillas."},
        {"name": "Fajita Chimichanga", "price": 12.75, "desc": "Steak & Chicken deep-fried burrito smothered in queso sauce. With rice & beans."},
        {"name": "Sopes (3)", "price": 11.50, "desc": "Three thick corn tortillas topped with beans, meat, lettuce, cheese, and cream."}
    ],
    "Antojitos & Botanas": [
        {"name": "Guacamole Dip", "price": 8.50, "desc": "Fresh avocado mixed with onions, cilantro, and lime juice."},
        {"name": "Queso Fundido", "price": 10.99, "desc": "Melted cheese blended with spicy chorizo. Served with warm tortillas."},
        {"name": "Nachos Supremos", "price": 12.50, "desc": "Topped with beef, beans, cheese, lettuce, tomatoes, and sour cream."}
    ],
    "Taqueria / Tacos": [
        {"name": "Tacos al Pastor", "price": 14.00, "desc": "Three soft corn tortillas with marinated pork, pineapple, onion, and cilantro."},
        {"name": "Street Tacos (4)", "price": 12.00, "desc": "Mini corn tortillas with your choice of meat, topped with salsa verde."}
    ],
    "Platos Fuertes / Entrees": [
        {"name": "Enchiladas Suizas", "price": 15.50, "desc": "Three chicken enchiladas topped with creamy salsa verde and melted cheese."},
        {"name": "Carne Asada", "price": 18.99, "desc": "Grilled skirt steak served with rice, beans, and fresh guacamole."}
    ],
    "Sizzling Platters & Seafood": [
        {"name": "Camarones al Mojo de Ajo", "price": 17.50, "desc": "Large shrimp sautéed in garlic butter and served with lime rice."},
        {"name": "Steak Fajitas", "price": 19.99, "desc": "A sizzling skillet of marinated steak, peppers, and onions."}
    ],
    "Vegetarian": [
        {"name": "Veggie Burrito", "price": 11.00, "desc": "Large flour tortilla filled with grilled veggies, beans, and cheese."},
        {"name": "Cheese Quesadilla", "price": 9.50, "desc": "Grilled flour tortilla stuffed with melted Oaxaca cheese."}
    ],
    "Drinks & Desserts": [
        {"name": "House Margarita", "price": 9.00, "desc": "Our signature blend of tequila, lime, and agave."},
        {"name": "Flan", "price": 6.50, "desc": "Classic Mexican custard with a sweet caramel glaze."}
    ]
}

# 7. DISPLAY MENU ITEMS
if category and category in MENU_DATA:
    for item in MENU_DATA[category]:
        col_text, col_btn = st.columns([3, 1])
        with col_text:
            st.markdown(f"### {item['name']}")
            st.write(item['desc'])
            st.markdown(f"<span class='price-tag'>${item['price']:.2f}</span>", unsafe_allow_html=True)
        with col_btn:
            st.write("") # Padding for alignment
            if st.button("＋ Add", key=f"add_{item['name']}"):
                st.session_state.cart.append(item)
                st.toast(f"Added {item['name']} to order!")
        st.divider()
else:
    st.markdown("<p style='text-align: center; color: #D4AF37; font-size: 24px; margin-top: 50px;'>Please select a category to view our authentic Mexican dishes.</p>", unsafe_allow_html=True)

# 8. SIDEBAR CHECKOUT
with st.sidebar:
    st.image("la_reina_dark.png", use_container_width=True)
    st.header("🛒 Current Order")
    
    if not st.session_state.cart:
        st.write("Your cart is empty.")
    else:
        for i, cart_item in enumerate(st.session_state.cart):
            st.write(f"**{cart_item['name']}** - ${cart_item['price']}")
        
        total_price = sum(item['price'] for item in st.session_state.cart)
        st.divider()
        st.subheader(f"Total: ${total_price:.2f}")
        
        if st.button("SUBMIT ORDER", use_container_width=True):
            st.success("Order sent to the kitchen!")
            # Logic for Fire TV kitchen view would trigger here
            st.session_state.cart = []
