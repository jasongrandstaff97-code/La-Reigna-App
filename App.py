import streamlit as st
import os
import random
import time

# ==========================================
# 1. PAGE CONFIGURATION
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
# This section forces the 380px width, massive text, and light mode contrast.
st.markdown("""
    <style>
    /* Force total white background */
    .stApp {
        background-color: #FFFFFF !important;
    }

    /* TOP TAB NAVIGATION (Menu, Rewards, Cart) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        justify-content: center;
        background-color: #f8f9fa;
        padding: 12px;
        border-radius: 15px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 75px;
        background-color: #ffffff;
        border-radius: 12px;
        padding: 10px 50px;
        font-size: 24px !important;
        font-weight: 800;
        color: #444444;
        border: 2px solid #eeeeee;
    }
    .stTabs [aria-selected="true"] {
        background-color: #D4AF37 !important;
        color: #FFFFFF !important;
        border: 2px solid #B8860B !important;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    }

    /* MEGA-PILLS: The 380px Force Fix */
    div[data-testid="stPill"] {
        gap: 20px !important;
        justify-content: center !important;
    }
    div[data-testid="stPill"] button {
        background-color: #ffffff !important;
        color: #8B6B00 !important;           /* Deep Gold for visibility */
        border: 3.5px solid #D4AF37 !important; /* High contrast border */
        padding: 30px 40px !important;
        font-size: 28px !important;
        font-weight: 900 !important;
        border-radius: 20px !important;
        min-width: 380px !important;         /* LOCKED AT 380PX */
        margin-bottom: 20px !important;
        transition: all 0.2s ease-in-out;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.05);
    }
    div[data-testid="stPill"] button[aria-pressed="true"] {
        background-color: #D4AF37 !important;
        color: #FFFFFF !important;
        box-shadow: 0px 8px 25px rgba(212, 175, 55, 0.45) !important;
        transform: translateY(-6px);
    }

    /* THE GREEN 'ADD' BUTTONS */
    div[data-testid="stBaseButton-secondary"] {
        background-color: #84bd00 !important;
        color: white !important;
        font-size: 26px !important;
        font-weight: 900 !important;
        border-radius: 15px !important;
        padding: 18px !important;
        width: 100% !important;
        border: none !important;
        box-shadow: 0px 4px 0px #5a8200;
    }
    div[data-testid="stBaseButton-secondary"]:active {
        transform: translateY(3px);
        box-shadow: 0px 1px 0px #5a8200;
    }

    /* REWARDS CARD BOX */
    .rewards-container {
        border: 4px solid #D4AF37;
        padding: 40px;
        border-radius: 25px;
        text-align: center;
        background-color: #fffdf9;
        margin-bottom: 30px;
    }

    /* TYPOGRAPHY */
    .stMarkdown h1 { font-size: 50px !important; color: #111 !important; text-align: center; }
    .stMarkdown h3 { font-size: 38px !important; color: #8B6B00 !important; margin-bottom: 5px !important; font-weight: 900 !important; }
    .stMarkdown p { font-size: 24px !important; color: #333333 !important; line-height: 1.5 !important; }
    .price-tag { font-size: 32px !important; color: #5a8200 !important; font-weight: 900 !important; }
    
    /* Global Spacing and Dividers */
    hr { border: 2px solid #f0f0f0 !important; margin: 40px 0 !important; }
    </style>

    <script>
    // Kitchen Bump Bar Listener (Spacebar Logic for Fire TV)
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
# 3. SESSION STATE (Brain of the App)
# ==========================================
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'user_points' not in st.session_state:
    st.session_state.user_points = 580 # Sample points balance

# ==========================================
# 4. HEADER & LOGO (With Anti-Crash Logic)
# ==========================================
_, cent_co, _ = st.columns([1, 7, 1])

with cent_co:
    # FILENAME MUST MATCH GITHUB EXACTLY: la_reina_horizontal.png
    logo_path = "la_reina_horizontal.png"
    
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        # Fallback to prevent app crash if GitHub hasn't updated the file yet
        st.markdown("<h1 style='color: #8B6B00; text-align: center; letter-spacing: 2px;'>LA REINA MARGARITAS</h1>", unsafe_allow_html=True)
        st.warning(f"⚠️ Error: '{logo_path}' not found. Please check GitHub file naming.")

st.divider()

# ==========================================
# 5. MAIN NAVIGATION (The 3 Global Tabs)
# ==========================================
tab_menu, tab_rewards, tab_cart = st.tabs([
    "🍴 OUR MENU", 
    "🎁 REWARDS", 
    f"🛒 MY CART ({len(st.session_state.cart)})"
])

# ------------------------------------------
# TAB 1: MENU SELECTION
# ------------------------------------------
with tab_menu:
    st.markdown("<h2 style='text-align: center; color: #666; font-size: 28px;'>Browse Our Authentic Dishes</h2>", unsafe_allow_html=True)
    
    # Category Pills (380px wide via CSS)
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

    # FULL PRODUCTION MENU DATA
    MENU_DATA = {
        "Lunch Specials (11am-3pm)": [
            {"name": "Lunch Fajitas", "price": 13.75, "desc": "Sizzling Steak or Chicken, grilled onions & peppers. Served with rice, beans, and tortillas."},
            {"name": "Fajita Chimichanga", "price": 12.75, "desc": "Deep-fried flour burrito stuffed with steak and chicken, smothered in queso sauce."},
            {"name": "Sopes (3)", "price": 11.50, "desc": "Three thick corn tortillas topped with beans, meat, lettuce, queso fresco, and cream."}
        ],
        "Antojitos & Botanas": [
            {"name": "Guacamole Dip", "price": 8.50, "desc": "Fresh avocado mixed with lime, onions, cilantro, and serrano peppers. Made fresh hourly."},
            {"name": "Queso Fundido", "price": 10.99, "desc": "Melted Oaxaca cheese blended with spicy Mexican chorizo. Served with warm tortillas."},
            {"name": "Nachos Supremos", "price": 12.50, "desc": "Crispy chips topped with seasoned beef, beans, melted cheese, and sour cream."}
        ],
        "Taqueria / Tacos": [
            {"name": "Street Tacos (4)", "price": 12.00, "desc": "Authentic mini corn tortillas with your choice of meat, onions, cilantro, and lime."},
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
            {"name": "Steak Fajitas", "price": 19.99, "desc": "A sizzling skillet of marinated steak, colorful peppers, and onions. The signature Queen's platter."},
            {"name": "Seafood Molcajete", "price": 24.50, "desc": "Volcanic stone bowl with shrimp, scallops, and white fish in a spicy tomato broth."}
        ],
        "Vegetarian": [
            {"name": "Veggie Burrito", "price": 11.00, "desc": "Large flour tortilla packed with grilled zucchini, mushrooms, beans, and cheese."},
            {"name": "Spinach Enchiladas", "price": 12.50, "desc": "Two corn tortillas filled with sautéed spinach and onions, topped with white queso."}
        ],
        "Drinks & Desserts": [
            {"name": "The Queen's Margarita", "price": 10.00, "desc": "Signature top-shelf tequila, fresh lime juice, and organic agave."},
            {"name": "Flan Mexicano", "price": 6.50, "desc": "Traditional Mexican custard with a sweet caramel glaze and whipped cream."},
            {"name": "Horchata", "price": 4.50, "desc": "Refreshing chilled rice milk flavored with cinnamon and vanilla."}
        ]
    }

    if category in MENU_DATA:
        st.markdown(f"## {category}")
        for item in MENU_DATA[category]:
            c_info, c_btn = st.columns([3, 1])
            with c_info:
                st.markdown(f"### {item['name']}")
                st.write(item['desc'])
                st.markdown(f"<span class='price-tag'>${item['price']:.2f}</span>", unsafe_allow_html=True)
            with c_btn:
                st.write("") # Alignment padding
                st.write("")
                if st.button("＋ ADD", key=f"add_{item['name']}"):
                    st.session_state.cart.append(item)
                    st.toast(f"Added {item['name']}!")
                    time.sleep(0.4)
                    st.rerun()
            st.divider()
    else:
        st.markdown("<p style='text-align: center; font-size: 26px; color: #999; margin-top: 80px;'>Tap a gold button above to view our authentic Mexican menu.</p>", unsafe_allow_html=True)

# ------------------------------------------
# TAB 2: REWARDS SYSTEM (LOYALTY)
# ------------------------------------------
with tab_rewards:
    pts = st.session_state.user_points
    goal = 1000
    prog = min(pts / goal, 1.0)
    
    st.markdown(f"""
        <div class="rewards-container">
            <h1 style="color: #8B6B00; font-size: 45px; margin-bottom: 0;">{pts} POINTS</h1>
            <p style="text-transform: uppercase; letter-spacing: 2px; color: #777;">Current Loyalty Balance</p>
            <div style="background-color: #eee; height: 30px; border-radius: 15px; margin: 30px 0; overflow: hidden; border: 1px solid #ddd;">
                <div style="background-color: #D4AF37; width: {prog*100}%; height: 100%;"></div>
            </div>
            <p style="font-size: 24px; color: #222;">You are <b>{goal - pts} points</b> away from a <b>FREE ENTREE!</b></p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### Rewards Dashboard")
    st.write("🥤 **100 Pts:** Free Horchata or Soda")
    st.write("🥑 **250 Pts:** Free Large Queso or Guacamole")
    st.write("🌮 **500 Pts:** Free Order of Street Tacos")
    st.write("👑 **1000 Pts:** Any Fajita or Entree on the House")

# ------------------------------------------
# TAB 3: CHECKOUT & CART
# ------------------------------------------
with tab_cart:
    st.markdown("<h1 style='color: #111;'>Your Order Summary</h1>", unsafe_allow_html=True)
    
    if not st.session_state.cart:
        st.info("Your cart is empty. Explore our menu to add your favorite dishes!")
    else:
        total_val = 0
        for i, cart_item in enumerate(st.session_state.cart):
            row1, row2, row3 = st.columns([2, 1, 1])
            with row1:
                st.markdown(f"**{cart_item['name']}**")
            with row2:
                st.write(f"${cart_item['price']:.2f}")
            with row3:
                if st.button("❌ Remove", key=f"del_{i}"):
                    st.session_state.cart.pop(i)
                    st.rerun()
            total_val += cart_item['price']
        
        st.divider()
        st.markdown(f"### Order Total: ${total_val:.2f}")
        
        pts_earned = int(total_val)
        st.markdown(f"✨ **You'll earn {pts_earned} Loyalty Points with this order!**")
        
        st.write("") 
        if st.button("🚀 SUBMIT ORDER & SEND TO KITCHEN", use_container_width=True):
            with st.spinner("Processing transaction..."):
                time.sleep(1.5)
                st.session_state.user_points += pts_earned
                st.balloons()
                st.success(f"Success! Your order is being prepared. Your new points balance: {st.session_state.user_points}")
                st.session_state.cart = []
                time.sleep(1.2)
                st.rerun()

# ==========================================
# 6. KITCHEN CONTROL (SIDEBAR ADMIN)
# ==========================================
with st.sidebar:
    st.image("la_reina_horizontal.png", use_container_width=True)
    st.markdown("---")
    st.header("Admin / Kitchen View")
    st.write("Fire TV Bump Bar Controls")
    
    if st.button("CLEAR ACTIVE ORDERS (BUMP)"):
        st.error("All pending orders have been cleared.")
    
    st.write("---")
    st.caption(f"System Online: {time.strftime('%H:%M:%S')}")
