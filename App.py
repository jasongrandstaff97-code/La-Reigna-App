import streamlit as st
import random
import time

# ==========================================
# 1. PAGE CONFIGURATION & THEME
# ==========================================
st.set_page_config(
    page_title="La Reina Margaritas",
    page_icon="👑",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. THE "HEAVYWEIGHT" CSS & JS (WHITE THEME)
# ==========================================
st.markdown("""
    <style>
    /* Global White Background */
    .stApp {
        background-color: #FFFFFF !important;
    }

    /* TOP TAB NAVIGATION (Menu, Rewards, Cart) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        justify-content: center;
        background-color: #f9f9f9;
        padding: 10px;
        border-radius: 15px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 70px;
        background-color: #ffffff;
        border-radius: 12px;
        padding: 10px 50px;
        font-size: 22px !important;
        font-weight: 800;
        color: #444444;
        border: 1px solid #eeeeee;
    }
    .stTabs [aria-selected="true"] {
        background-color: #D4AF37 !important;
        color: #FFFFFF !important;
        border: 2px solid #B8860B !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }

    /* MEGA-PILLS: 380px Wide Load targets */
    div[data-testid="stPill"] {
        gap: 20px !important;
        justify-content: center !important;
    }
    div[data-testid="stPill"] button {
        background-color: #ffffff !important;
        color: #8B6B00 !important;           /* Darker gold for readability on white */
        border: 3px solid #D4AF37 !important; /* Thick gold border */
        padding: 30px 40px !important;
        font-size: 26px !important;
        font-weight: 900 !important;
        border-radius: 20px !important;
        min-width: 380px !important;         /* THE FIXED WIDTH */
        margin-bottom: 20px !important;
        transition: all 0.2s ease-in-out;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.05);
    }
    div[data-testid="stPill"] button[aria-pressed="true"] {
        background-color: #D4AF37 !important;
        color: #FFFFFF !important;
        box-shadow: 0px 8px 20px rgba(212, 175, 55, 0.4) !important;
        transform: translateY(-5px);
    }

    /* GREEN ADD BUTTONS (Accessibility) */
    div[data-testid="stBaseButton-secondary"] {
        background-color: #84bd00 !important;
        color: white !important;
        font-size: 24px !important;
        font-weight: bold !important;
        border-radius: 15px !important;
        padding: 15px !important;
        width: 100% !important;
        border: 2px solid #6a9600 !important;
    }
    div[data-testid="stBaseButton-secondary"]:hover {
        background-color: #6a9600 !important;
        transform: scale(1.03);
    }

    /* REWARDS CARD DESIGN */
    .rewards-card {
        background: linear-gradient(135deg, #ffffff 0%, #fffbf0 100%);
        border: 3px solid #D4AF37;
        padding: 40px;
        border-radius: 25px;
        text-align: center;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.05);
        margin-bottom: 30px;
    }

    /* TYPOGRAPHY POLISH */
    .stMarkdown h1 { font-size: 50px !important; color: #222 !important; text-align: center; }
    .stMarkdown h3 { font-size: 36px !important; color: #8B6B00 !important; margin-bottom: 5px !important; }
    .stMarkdown p { font-size: 22px !important; color: #333333 !important; line-height: 1.5 !important; }
    .price-tag { font-size: 30px !important; color: #5a8200 !important; font-weight: 900 !important; }
    
    /* Clean dividers */
    hr { border: 1.5px solid #eeeeee !important; }
    </style>

    <script>
    // Kitchen Spacebar Listener (Fire TV 'Bump' Hack)
    const doc = window.parent.document;
    doc.addEventListener('keydown', function(e) {
        if (e.code === 'Space') {
            const buttons = Array.from(doc.querySelectorAll('button'));
            const bumpBtn = buttons.find(el => el.innerText.includes('BUMP') || el.innerText.includes('CLEAR'));
            if (bumpBtn) { bumpBtn.click(); }
        }
    });
    </script>
""", unsafe_allow_html=True)

# ==========================================
# 3. SESSION STATE (PERSISTENT DATA)
# ==========================================
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'user_points' not in st.session_state:
    st.session_state.user_points = 625  # Starting points for demo

# ==========================================
# 4. HEADER & LOGO
# ==========================================
_, cent_co, _ = st.columns([1, 6, 1])
with cent_co:
    # Since the screen is white, we use the original horizontal logo
    st.image("la_reina_horizontal.png", use_container_width=True)

st.divider()

# ==========================================
# 5. MAIN NAVIGATION TABS
# ==========================================
cart_count = len(st.session_state.cart)
tab_menu, tab_rewards, tab_cart = st.tabs([
    "🍴 OUR MENU", 
    "🎁 REWARDS", 
    f"🛒 MY CART ({cart_count})"
])

# ------------------------------------------
# TAB 1: MENU SELECTION
# ------------------------------------------
with tab_menu:
    st.markdown("<h1 style='font-size: 30px; color: #555;'>What are you craving?</h1>", unsafe_allow_html=True)
    
    category = st.pills(
        label="Menu Categories",
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

    # COMPREHENSIVE MENU DATA
    MENU_DATA = {
        "Lunch Specials (11am-3pm)": [
            {"name": "Lunch Fajitas", "price": 13.75, "desc": "Choice of Steak or Chicken, grilled with onions and bell peppers. Served with rice, beans, and warm tortillas."},
            {"name": "Fajita Chimichanga", "price": 12.75, "desc": "Deep-fried flour burrito stuffed with steak and chicken, smothered in our signature queso sauce."},
            {"name": "Sopes (3)", "price": 11.50, "desc": "Three thick corn tortillas topped with beans, choice of meat, fresh lettuce, queso fresco, and Mexican cream."}
        ],
        "Antojitos & Botanas": [
            {"name": "Guacamole Dip", "price": 8.50, "desc": "Hand-mashed avocado mixed with fresh lime, onions, cilantro, and serrano peppers."},
            {"name": "Queso Fundido", "price": 10.99, "desc": "Melted Oaxaca and Chihuahua cheese blended with spicy Mexican chorizo. Served with tortillas."},
            {"name": "Nachos Supremos", "price": 12.50, "desc": "Crispy chips topped with seasoned beef, beans, melted cheese, tomatoes, and sour cream."}
        ],
        "Taqueria / Tacos": [
            {"name": "Street Tacos (4)", "price": 12.00, "desc": "Authentic mini corn tortillas with your choice of meat, fresh onions, cilantro, and lime."},
            {"name": "Tacos al Pastor", "price": 14.50, "desc": "Three soft corn tortillas filled with marinated pork, grilled pineapple, and salsa roja."},
            {"name": "Tacos de Camaron", "price": 15.99, "desc": "Three flour tortillas with grilled shrimp, cabbage slaw, and chipotle crema."}
        ],
        "Platos Fuertes / Entrees": [
            {"name": "Enchiladas Suizas", "price": 15.50, "desc": "Three chicken enchiladas topped with creamy salsa verde and melted Monterey Jack cheese."},
            {"name": "Carne Asada", "price": 18.99, "desc": "Grilled tender skirt steak served with charro beans, Mexican rice, and roasted jalapeño."},
            {"name": "Pollo a la Crema", "price": 16.25, "desc": "Sliced chicken breast sautéed with mushrooms and onions in a rich cream sauce."}
        ],
        "Sizzling Platters & Seafood": [
            {"name": "Camarones al Mojo de Ajo", "price": 17.50, "desc": "Jumbo shrimp sautéed in a garlic butter sauce. Served with cilantro lime rice."},
            {"name": "Steak Fajitas", "price": 19.99, "desc": "A sizzling skillet of marinated steak, colorful peppers, and onions. The Queen's favorite."},
            {"name": "Seafood Molcajete", "price": 24.50, "desc": "A volcanic stone bowl filled with shrimp, scallops, and white fish in a spicy tomato broth."}
        ],
        "Vegetarian": [
            {"name": "Veggie Burrito", "price": 11.00, "desc": "Large flour tortilla packed with grilled zucchini, mushrooms, beans, and cheese."},
            {"name": "Spinach Enchiladas", "price": 12.50, "desc": "Two corn tortillas filled with sautéed spinach and onions, topped with white queso."}
        ],
        "Drinks & Desserts": [
            {"name": "The Queen's Margarita", "price": 10.00, "desc": "Our signature top-shelf tequila, fresh lime juice, and organic agave."},
            {"name": "Flan Mexicano", "price": 6.50, "desc": "Traditional Mexican custard with a sweet caramel glaze and whipped cream."},
            {"name": "Horchata", "price": 4.50, "desc": "Refreshing rice milk flavored with cinnamon and vanilla."}
        ]
    }

    if category in MENU_DATA:
        st.markdown(f"## {category}")
        for item in MENU_DATA[category]:
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"### {item['name']}")
                st.write(item['desc'])
                st.markdown(f"<span class='price-tag'>${item['price']:.2f}</span>", unsafe_allow_html=True)
            with c2:
                st.write("") # Padding for vertical centering
                if st.button("＋ ADD", key=f"add_{item['name']}"):
                    st.session_state.cart.append(item)
                    st.toast(f"Added {item['name']}!")
                    time.sleep(0.5)
                    st.rerun()
            st.divider()
    else:
        st.markdown("<p style='text-align: center; font-size: 24px; color: #888; margin-top: 50px;'>Select a category above to view our authentic Mexican dishes.</p>", unsafe_allow_html=True)

# ------------------------------------------
# TAB 2: REWARDS SYSTEM
# ------------------------------------------
with tab_rewards:
    st.markdown("<h1 style='color: #222;'>La Reina Loyalty</h1>", unsafe_allow_html=True)
    
    # Points Progress Math
    points = st.session_state.user_points
    goal = 1000
    progress = min(points / goal, 1.0)
    
    st.markdown(f"""
        <div class="rewards-card">
            <h2 style="color: #8B6B00; font-size: 40px; margin-bottom: 0;">{points}</h2>
            <p style="text-transform: uppercase; letter-spacing: 2px; color: #666;">Total Reward Points</p>
            <div style="background-color: #eee; height: 25px; border-radius: 15px; margin: 25px 0; overflow: hidden;">
                <div style="background-color: #D4AF37; width: {progress*100}%; height: 100%;"></div>
            </div>
            <p style="font-size: 22px; color: #444;">You are <b>{goal - points} points</b> away from a <b>FREE PLATO FUERTE!</b></p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### Reward Tiers")
    st.write("🥤 **100 Points:** Free Fountain Drink or Horchata")
    st.write("🥑 **250 Points:** Free Guacamole or Queso Fundido")
    st.write("🌮 **500 Points:** Free Order of Street Tacos")
    st.write("👑 **1000 Points:** Any Platos Fuertes or Fajitas Free")

# ------------------------------------------
# TAB 3: SHOPPING CART & CHECKOUT
# ------------------------------------------
with tab_cart:
    st.markdown("<h1 style='color: #222;'>Your Order</h1>", unsafe_allow_html=True)
    
    if not st.session_state.cart:
        st.info("Your cart is empty. Start adding items from the menu!")
    else:
        subtotal = 0
        for i, item in enumerate(st.session_state.cart):
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown(f"**{item['name']}**")
            with col2:
                st.write(f"${item['price']:.2f}")
            with col3:
                if st.button("❌ Remove", key=f"rem_{i}"):
                    st.session_state.cart.pop(i)
                    st.rerun()
            subtotal += item['price']
        
        st.divider()
        st.markdown(f"### Subtotal: ${subtotal:.2f}")
        
        earned = int(subtotal)
        st.markdown(f"✨ **You'll earn {earned} Points with this order!**")
        
        st.write("") # Spacer
        if st.button("🚀 SUBMIT ORDER & PAY AT PICKUP", use_container_width=True):
            with st.spinner("Sending order to kitchen..."):
                time.sleep(2) # Simulation of network delay
                st.session_state.user_points += earned
                st.balloons()
                st.success(f"Order Success! Points updated to {st.session_state.user_points}.")
                st.session_state.cart = []
                time.sleep(1)
                st.rerun()

# ==========================================
# 6. KITCHEN DISPLAY LOGIC (SIDEBAR HACK)
# ==========================================
# This section is for the Fire TV in the kitchen. 
# In a real app, this would pull from a database.
with st.sidebar:
    st.image("la_reina_horizontal.png", use_container_width=True)
    st.header("Kitchen View")
    st.info("Staff: Press SPACEBAR to clear orders.")
    
    if st.button("CLEAR ALL ORDERS (BUMP)"):
        st.warning("Orders Cleared.")
