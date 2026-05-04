import streamlit as st
from streamlit_pills import pills
import time
import base64

# ==============================================================================
# 1. CORE SYSTEM ARCHITECTURE (The Scaling Engine)
# ==============================================================================
# This dictionary is the "Source of Truth." Every key here becomes a Pill Tab.
MENU_DATABASE = {
    "Tacos": [
        {"name": "Street Taco", "desc": "Cilantro, onion, lime, choice of protein", "price": 3.50, "feat": "Popular"},
        {"name": "Al Pastor", "desc": "Marinated pork, pineapple, spicy salsa", "price": 4.00, "feat": "Classic"},
        {"name": "Barbacoa", "desc": "Slow-braised beef, tender & rich", "price": 4.50, "feat": ""},
        {"name": "Carnitas", "desc": "Crispy shredded pork, pickled red onions", "price": 4.00, "feat": ""}
    ],
    "Entrees": [
        {"name": "Enchiladas Verdes", "desc": "3 chicken enchiladas, salsa verde, queso fresco", "price": 14.00, "feat": "Best Seller"},
        {"name": "Burrito Grande", "desc": "Rice, beans, protein, smothered in house queso", "price": 12.00, "feat": ""},
        {"name": "Fajita Platter", "desc": "Sizzling steak or chicken, peppers, onions", "price": 18.00, "feat": ""},
        {"name": "Chimichanga", "desc": "Deep-fried burrito, cheese sauce, pico de gallo", "price": 13.50, "feat": ""}
    ],
    "Appetizers": [
        {"name": "Guacamole & Chips", "desc": "Hand-smashed daily with fresh lime", "price": 8.00, "feat": ""},
        {"name": "Queso Fundido", "desc": "Melted cheese blend with spicy chorizo", "price": 9.00, "feat": "Chef's Pick"},
        {"name": "Street Corn", "desc": "Elote with cotija, tajin, and lime crema", "price": 6.00, "feat": ""},
        {"name": "Nachos Supremos", "desc": "Queso, jalapeños, beans, pico, sour cream", "price": 11.00, "feat": ""}
    ],
    "Drinks": [
        {"name": "House Margarita", "desc": "Gold tequila, fresh lime, organic agave", "price": 9.00, "feat": "Signature"},
        {"name": "Paloma", "desc": "Grapefruit, lime, tequila, soda splash", "price": 10.00, "feat": ""},
        {"name": "Agua Fresca", "desc": "Watermelon, Pineapple, or Horchata", "price": 4.00, "feat": ""},
        {"name": "Jarritos", "desc": "Mexican soda: Mango, Lime, or Mandarina", "price": 3.00, "feat": ""}
    ],
    "Desserts": [
        {"name": "Churros", "desc": "Cinnamon sugar with Mexican chocolate dip", "price": 7.00, "feat": ""},
        {"name": "Tres Leches", "desc": "Classic soaked sponge cake with cream", "price": 8.00, "feat": ""},
        {"name": "Flan", "desc": "Traditional caramel custard", "price": 6.00, "feat": ""}
    ]
}

# ==============================================================================
# 2. BRANDING & BEHAVIORAL UI (The Moat)
# ==============================================================================
st.set_page_config(page_title="La Reina OS", layout="wide")

def apply_branding():
    st.markdown(f"""
        <style>
        /* Dark Mode Ergonomics */
        .stApp {{
            background-color: #000000;
            color: #FFFFFF;
        }}
        
        /* The Poblano Pulse - Operational Status */
        .status-header {{
            background-color: #4CBB17;
            color: black;
            padding: 10px;
            text-align: center;
            font-weight: 900;
            border-radius: 4px;
            margin-bottom: 20px;
            letter-spacing: 2px;
            box-shadow: 0px 4px 10px rgba(76,187,23,0.3);
        }}

        /* Mega-Pill Menu Cards */
        .menu-item {{
            background-color: #111111;
            border: 1px solid #333;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            transition: border 0.3s;
        }}
        .menu-item:hover {{
            border-color: #D4AF37;
        }}
        
        .item-name {{
            color: #D4AF37;
            font-size: 1.5rem;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .price-text {{
            color: #D4AF37;
            font-family: 'monospace';
            font-size: 1.3rem;
            font-weight: bold;
        }}
        
        /* Pills Customization */
        .stPills {{
            padding: 10px 0px;
        }}
        </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. SYSTEM UTILITIES
# ==============================================================================
class OSBrain:
    @staticmethod
    def initialize():
        if 'cart' not in st.session_state: st.session_state.cart = []
        if 'phone' not in st.session_state: st.session_state.phone = None
        if 'points' not in st.session_state: st.session_state.points = 0
        if 'order_history' not in st.session_state: st.session_state.order_history = []

    @staticmethod
    def add_item(item):
        st.session_state.cart.append(item)
        st.toast(f"Added {item['name']}! 🌮")

# ==============================================================================
# 4. MODULAR UI COMPONENTS
# ==============================================================================

def render_header():
    # DIRECT LOGO LOGIC
    # Replace this URL with your raw GitHub logo link or local path
    LOGO_URL = "https://raw.githubusercontent.com/jason-grandstaff/logo-repo/main/logo.png"
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            st.image(LOGO_URL, width=350)
        except:
            st.markdown("<h1 style='text-align:center; color:#D4AF37; font-size:4rem;'>LA REINA</h1>", unsafe_allow_html=True)
            st.markdown("<p style='text-align:center; margin-top:-20px;'>AUTHENTIC MEXICAN KITCHEN & CANTINA</p>", unsafe_allow_html=True)
    
    st.markdown('<div class="status-header">STATUS: POBLANO 🫑 LIVE ENGINE</div>', unsafe_allow_html=True)

def render_rewards_center():
    st.markdown("## 👑 The Kingdom Rewards")
    st.write("Enter your number to track points and unlock free items.")
    
    c1, c2 = st.columns(2)
    with c1:
        num = st.text_input("Mobile Number", placeholder="417-XXX-XXXX", 
                            value=st.session_state.phone if st.session_state.phone else "")
        if st.button("Sync Account", use_container_width=True):
            st.session_state.phone = num
            st.success("Account Synced.")
            st.balloons()
    
    with c2:
        if st.session_state.phone:
            st.metric("Your Points", f"{st.session_state.points} PTS")
            st.progress(min(st.session_state.points / 100, 1.0))
            st.caption("100 Points = 1 Free Specialty Margarita")

def render_menu_engine(category):
    items = MENU_DATABASE.get(category, [])
    
    # Render 2 items per row for professional "Grid" feel
    for i in range(0, len(items), 2):
        row = st.columns(2)
        for idx, col in enumerate(row):
            if i + idx < len(items):
                item = items[i+idx]
                with col:
                    st.markdown(f"""
                        <div class="menu-item">
                            <div class="item-name">{item['name']}</div>
                            <div style="color:#888; margin-bottom:10px;">{item['desc']}</div>
                            <div class="price-text">${item['price']:.2f}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"Add {item['name']}", key=f"btn_{item['name']}"):
                        OSBrain.add_item(item)

# ==============================================================================
# 5. MAIN EXECUTION (The Bootloader)
# ==============================================================================
def main():
    OSBrain.initialize()
    apply_branding()
    
    # Sidebar: The "Command Center"
    with st.sidebar:
        st.title("🛒 Your Order")
        if not st.session_state.cart:
            st.write("Cart is empty.")
        else:
            for i in st.session_state.cart:
                st.write(f"• {i['name']} (${i['price']:.2f})")
            
            total = sum(item['price'] for item in st.session_state.cart)
            st.markdown(f"### Total: **${total:.2f}**")
            
            if st.button("PLACE ORDER 🚀", use_container_width=True):
                st.session_state.points += int(total)
                st.session_state.cart = []
                st.success("Sent to Kitchen!")

    # Main Screen Logic
    render_header()
    
    # DYNAMIC PILL GENERATION
    # This automatically includes EVERY key in MENU_DATABASE
    pill_options = list(MENU_DATABASE.keys()) + ["Rewards 👑"]
    selected_tab = pills("", pill_options, index=0, label_visibility="collapsed")
    
    st.write("---")
    
    if "Rewards" in selected_tab:
        render_rewards_center()
    else:
        render_menu_engine(selected_tab)

if __name__ == "__main__":
    main()
