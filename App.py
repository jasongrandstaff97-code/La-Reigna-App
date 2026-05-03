import streamlit as st
import random
import streamlit.components.v1 as components

# 1. PAGE CONFIG & ACCESSIBILITY
st.set_page_config(
    page_title="La Reina Margaritas", 
    page_icon="👑", 
    layout="centered"
)

# 2. THE "GENIUS" UI/UX STYLING (Sage Green & Gold)
st.markdown("""
    <style>
    /* Main Background and Text */
    [data-testid="stAppViewContainer"] {
        background-color: #121212; /* Dark Mode for high contrast */
    }
    
    /* Mega-Pill Customization for Older Users */
    div[data-testid="stBaseButton-secondaryPill"] {
        padding: 20px 40px !important;
        font-size: 22px !important;
        font-weight: bold !important;
        border-radius: 50px !important;
        border: 2px solid #D4AF37 !important; /* Gold Border */
        background-color: transparent !important;
        color: white !important;
    }
    
    /* Hover/Active State for Pills */
    div[data-testid="stBaseButton-secondaryPill"]:hover, 
    div[data-testid="stBaseButton-secondaryPill"][aria-pressed="true"] {
        background-color: #556B2F !important; /* Sage Green */
        color: #F8E231 !important; /* Bright Gold */
        border-color: #F8E231 !important;
    }

    /* Large 'Add' Buttons */
    div.stButton > button {
        background-color: #556B2F !important;
        color: white !important;
        font-size: 20px !important;
        padding: 15px !important;
        border-radius: 12px !important;
        border: none !important;
    }

    /* Price and Header Typography */
    h1, h2, h3 { 
        color: #D4AF37 !important; 
        font-family: 'Georgia', serif; 
    }
    .price-text {
        font-size: 24px !important;
        font-weight: bold;
        color: #F8E231;
    }
    .item-name {
        font-size: 26px !important;
        font-weight: bold;
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# 3. JAVASCRIPT: THE BUMP-BAR LISTENER (Spacebar)
# This allows the kitchen staff to "bump" orders using a physical USB keyboard
components.html(
    """
    <script>
    const doc = window.parent.document;
    doc.addEventListener('keydown', function(e) {
        if (e.code === 'Space') {
            const buttons = Array.from(doc.querySelectorAll('button'));
            const bumpBtn = buttons.find(el => el.innerText.includes('BUMP') || el.innerText.includes('➕ Add'));
            if (bumpBtn) { bumpBtn.click(); }
        }
    });
    </script>
    """,
    height=0,
)

# 4. STATE MANAGEMENT
if "cart" not in st.session_state:
    st.session_state.cart = []
if "show_camera" not in st.session_state:
    st.session_state.show_camera = False

# 5. HEADER & HORIZONTAL LOGO
left_co, cent_co, last_co = st.columns([1, 5, 1])
with cent_co:
    # Ensure 'la_reina_horizontal.png' is uploaded to your GitHub!
    try:
        st.image("la_reina_horizontal.png", use_container_width=True)
    except:
        st.markdown("<h1 style='text-align: center;'>👑 La Reina Margaritas</h1>", unsafe_allow_html=True)

st.divider()

# 6. MENU DATABASE
menu_data = {
    "Lunch Specials (11am-3pm)": [
        {"name": "Lunch Fajitas", "price": 13.75, "desc": "Sizzling Steak or Chicken, grilled onions & peppers."},
        {"name": "Fajita Chimichanga", "price": 12.75, "desc": "Deep-fried burrito smothered in queso sauce."},
        {"name": "Sopes (3)", "price": 13.75, "desc": "Three traditional sopes with fresh toppings."},
        {"name": "Rey Nachos", "price": 14.00, "desc": "Loaded nachos topped with tender Birria meat."}
    ],
    "Taqueria / Tacos": [
        {"name": "Quesabirria", "price": 16.00, "desc": "Three tortillas with slow-roasted beef & consommé."},
        {"name": "Street Tacos", "price": 14.75, "desc": "Three asada or grilled chicken tacos."},
        {"name": "Keto Taco", "price": 14.00, "desc": "Three cheese tortillas, pastor, onion, & cilantro."}
    ],
    "Antojitos & Botanas": [
        {"name": "Famoso Queso Casero", "price": 8.00, "desc": "House-made queso with a hint of spice."},
        {"name": "Esquites de la Casa", "price": 8.00, "desc": "Charred corn, epazote aioli, and queso fresco."}
    ],
    "Drinks & Desserts": [
        {"name": "Aguas Frescas (32 oz)", "price": 7.50, "desc": "Horchata, Sandia, or Pineapple."},
        {"name": "Tres Leches", "price": 7.00, "desc": "Classic Mexican three-milk cake."}
    ]
}

# 7. MAIN TABS SETUP
tab1, tab2, tab3 = st.tabs(["🍽️ Order Now", "🎁 Rewards", f"🛒 Cart ({len(st.session_state.cart)})"])

with tab1:
    st.markdown("### Browse Menu")
    
    # Large Nav Pills for Accessibility
    category_list = list(menu_data.keys())
    selected_category = st.pills(
        "Menu Categories", 
        category_list, 
        default="Lunch Specials (11am-3pm)", 
        label_visibility="collapsed"
    )
    
    st.divider()

    if selected_category:
        for item in menu_data[selected_category]:
            col1, col2 = st.columns([3, 1], vertical_alignment="center")
            
            with col1:
                st.markdown(f"<div class='item-name'>{item['name']}</div>", unsafe_allow_html=True)
                st.caption(item['desc'])
                st.markdown(f"<div class='price-text'>${item['price']:.2f}</div>", unsafe_allow_html=True)
            
            with col2:
                if st.button("➕ Add", key=f"add_{item['name']}"):
                    st.session_state.cart.append(item)
                    st.toast(f"Added {item['name']}! 🌮", icon="✅")
            st.divider()

with tab2:
    st.header("Poblano Status 🌶️")
    st.progress(0.5, text="500 pts until next tier (Habanero!)")
    
    st.markdown("### Claim Missing Points")
    st.info("Upload your phone order receipt below.")
    
    if st.button("📸 Tap to Scan Receipt"):
        st.session_state.show_camera = True
        
    if st.session_state.show_camera:
        picture = st.camera_input("Line up your receipt here")
        if picture:
            st.success("Points will be added shortly!")
            st.session_state.show_camera = False

with tab3:
    st.header("Your Order")
    if not st.session_state.cart:
        st.warning("Your cart is empty.")
    else:
        total = sum(item['price'] for item in st.session_state.cart)
        for i, item in enumerate(st.session_state.cart):
            col_i, col_x = st.columns([4, 1])
            col_i.markdown(f"- {item['name']} : **${item['price']:.2f}**")
            if col_x.button("🗑️", key=f"del_{i}"):
                st.session_state.cart.pop(i)
                st.rerun()
                
        st.divider()
        st.subheader(f"Total: ${total:.2f}")
        
        st.markdown("### Checkout Options")
        colA, colB = st.columns(2)
        with colA:
            if st.button("🏪 Pay at Pickup"):
                st.success(f"🎉 Order Confirmed! See you soon.")
                st.session_state.cart = []
                st.rerun() 
        with colB:
            if st.button("💳 Pay Now (Direct)"):
                st.info("Bypassing POS... Redirecting to Bank Bridge.")
