import streamlit as st
from streamlit_pills import pills
import time
import base64

# ==========================================
# 1. GLOBAL SYSTEM CONFIGURATION (The OS DNA)
# ==========================================
SYSTEM_CONFIG = {
    "version": "2.1.0-PRO",
    "branding": {
        "name": "La Reina Margaritas",
        "primary": "#D4AF37",    # Gold
        "secondary": "#4CBB17",  # Poblano Green
        "bg_dark": "#0A0A0A",    # Deepest Black
        "card_bg": "#161616",    # Subtle gray-black
        "text": "#FFFFFF",
        "logo_url": "https://raw.githubusercontent.com/jason-grandstaff/logo-repo/main/la_reina_logo.png"
    },
    "audio": {
        "order_ping": "https://www.soundjay.com/buttons/beep-01a.mp3" # Placeholder
    }
}

# ==========================================
# 2. DATA INFRASTRUCTURE (The Master Inventory)
# ==========================================
# In V3, this moves to Supabase. For now, it's a robust object.
MENU_DATABASE = {
    "Tacos": [
        {"id": "t1", "name": "Street Taco", "desc": "Cilantro, onion, lime", "price": 3.50, "image": "🌮"},
        {"id": "t2", "name": "Al Pastor", "desc": "Marinated pork, pineapple", "price": 4.00, "image": "🍍"},
        {"id": "t3", "name": "Barbacoa", "desc": "Slow-braised beef", "price": 4.50, "image": "🥩"}
    ],
    "Entrees": [
        {"id": "e1", "name": "Enchiladas Verdes", "desc": "Three chicken enchiladas", "price": 14.00, "image": "🥘"},
        {"id": "e2", "name": "Burrito Grande", "desc": "Rice, beans, protein, cheese", "price": 12.00, "image": "🌯"},
        {"id": "e3", "name": "Fajita Platter", "desc": "Sizzling peppers & onions", "price": 18.00, "image": "🔥"}
    ],
    "Appetizers": [
        {"id": "a1", "name": "Guacamole & Chips", "desc": "Fresh made daily", "price": 8.00, "image": "🥑"},
        {"id": "a2", "name": "Queso Fundido", "desc": "Melted cheese with chorizo", "price": 9.00, "image": "🧀"}
    ],
    "Drinks": [
        {"id": "d1", "name": "House Margarita", "desc": "Gold tequila, fresh lime", "price": 9.00, "image": "🍹"},
        {"id": "d2", "name": "Paloma", "desc": "Grapefruit soda, lime, tequila", "price": 10.00, "image": "🍊"},
        {"id": "d3", "name": "Agua Fresca", "desc": "Seasonal fresh fruit water", "price": 4.00, "image": "🥤"}
    ]
}

# ==========================================
# 3. ADVANCED STYLING ENGINE (The Behavioral UX)
# ==========================================
def apply_enterprise_styles():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {{
        background-color: {SYSTEM_CONFIG['branding']['bg_dark']};
        color: {SYSTEM_CONFIG['branding']['text']};
        font-family: 'Inter', sans-serif;
    }}
    
    /* The Mega-Pill Card */
    .menu-card {{
        background-color: {SYSTEM_CONFIG['branding']['card_bg']};
        border: 1px solid #333;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 16px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }}
    .menu-card:hover {{
        border-color: {SYSTEM_CONFIG['branding']['primary']};
        transform: translateY(-2px);
    }}
    
    /* Status Bars */
    .poblano-header {{
        background: linear-gradient(90deg, {SYSTEM_CONFIG['branding']['secondary']} 0%, #2e7d32 100%);
        color: white;
        padding: 10px;
        text-align: center;
        border-radius: 8px;
        font-weight: 800;
        letter-spacing: 1px;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }}
    
    /* Buttons */
    .stButton>button {{
        background-color: {SYSTEM_CONFIG['branding']['primary']};
        color: black !important;
        border-radius: 12px;
        border: none;
        font-weight: bold;
        height: 3em;
        width: 100%;
    }}
    
    /* KDS Specific Styles */
    .kds-ticket {{
        background-color: #f5f5f5;
        color: #111;
        padding: 15px;
        border-left: 10px solid {SYSTEM_CONFIG['branding']['secondary']};
        border-radius: 5px;
        margin-bottom: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 4. SYSTEM UTILITIES (The Backend Logic)
# ==========================================
class LaReinaOS:
    @staticmethod
    def init_state():
        if 'view' not in st.session_state: st.session_state.view = "Customer"
        if 'cart' not in st.session_state: st.session_state.cart = []
        if 'orders' not in st.session_state: st.session_state.orders = []
        if 'user_phone' not in st.session_state: st.session_state.user_phone = None
        if 'points' not in st.session_state: st.session_state.points = 0

    @staticmethod
    def play_sound():
        # JavaScript Audio Injection
        sound_html = f"""
            <audio autoplay>
                <source src="{SYSTEM_CONFIG['audio']['order_ping']}" type="audio/mp3">
            </audio>
        """
        st.components.v1.html(sound_html, height=0)

    @staticmethod
    def add_to_cart(item):
        st.session_state.cart.append(item)
        st.toast(f"✅ Added {item['name']} to order!")

# ==========================================
# 5. UI MODULES (The Component Library)
# ==========================================

def render_customer_view():
    st.image(SYSTEM_CONFIG['branding']['logo_url'], width=220)
    st.markdown('<div class="poblano-header">KITCHEN ONLINE • SELECT ITEMS</div>', unsafe_allow_html=True)

    # Navigation Pills
    categories = list(MENU_DATABASE.keys()) + ["Rewards 👑"]
    active_tab = pills("Menu", categories, index=0, label_visibility="collapsed")

    st.write("---")

    if "Rewards" in active_tab:
        render_rewards_center()
    else:
        # Dual Column Layout for Menu
        items = MENU_DATABASE.get(active_tab, [])
        for i in range(0, len(items), 2):
            cols = st.columns(2)
            for idx, col in enumerate(cols):
                if i + idx < len(items):
                    item = items[i+idx]
                    with col:
                        st.markdown(f"""
                        <div class="menu-card">
                            <span style="font-size: 2rem;">{item['image']}</span>
                            <h3 style="margin: 10px 0;">{item['name']}</h3>
                            <p style="color: #888; font-size: 0.9rem;">{item['desc']}</p>
                            <h2 style="color: {SYSTEM_CONFIG['branding']['primary']};">${item['price']:.2f}</h2>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button(f"Add {item['name']}", key=item['id']):
                            LaReinaOS.add_to_cart(item)

def render_rewards_center():
    st.title("Loyalty & Rewards")
    col1, col2 = st.columns([2,1])
    
    with col1:
        st.markdown("""
        ### Why Join the Kingdom?
        * **1 Point** for every $1 spent.
        * **Free Taco** at 50 points.
        * **Birthday Surprise** every year.
        """)
        
        phone = st.text_input("Enter Phone Number", value=st.session_state.user_phone if st.session_state.user_phone else "")
        if st.button("Link Account"):
            if len(phone) >= 10:
                st.session_state.user_phone = phone
                st.success("Welcome back! Your points are being tracked.")
                st.balloons()
            else:
                st.error("Please enter a valid 10-digit mobile number.")
    
    with col2:
        if st.session_state.user_phone:
            st.metric("Your Points", f"{st.session_state.points} PTS")
            st.progress(st.session_state.points / 50 if st.session_state.points < 50 else 1.0)
            st.caption("Next Reward: 50 Points")

def render_kds_view():
    st.markdown(f"<h1 style='color:{SYSTEM_CONFIG['branding']['secondary']}'>Kitchen Display System</h1>", unsafe_allow_html=True)
    st.write("---")
    
    if not st.session_state.orders:
        st.info("Waiting for new orders... 🔥")
    
    # Grid for KDS Tickets
    cols = st.columns(3)
    for idx, order in enumerate(st.session_state.orders):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="kds-ticket">
                <h4>ORDER #{order['id']}</h4>
                <hr>
                {'<br>'.join([f"• {i['name']}" for i in order['items']])}
                <hr>
                <strong>TIME: {order['time']}</strong>
            </div>
            """, unsafe_allow_html=True)
            if st.button("BUMP", key=f"bump_{idx}"):
                st.session_state.orders.pop(idx)
                st.rerun()

def render_sidebar():
    with st.sidebar:
        st.title("System Control")
        st.session_state.view = st.radio("Access Level", ["Customer", "Kitchen (KDS)", "Admin"])
        
        st.write("---")
        if st.session_state.view == "Customer":
            st.subheader("🛒 Current Cart")
            if not st.session_state.cart:
                st.write("Your cart is empty.")
            else:
                for item in st.session_state.cart:
                    st.write(f"• {item['name']} (${item['price']})")
                
                total = sum([i['price'] for i in st.session_state.cart])
                st.markdown(f"### Total: ${total:.2f}")
                
                if st.button("🚀 PLACE ORDER"):
                    new_order = {
                        "id": len(st.session_state.orders) + 101,
                        "items": st.session_state.cart,
                        "time": time.strftime("%H:%M:%S")
                    }
                    st.session_state.orders.append(new_order)
                    st.session_state.points += int(total)
                    st.session_state.cart = []
                    LaReinaOS.play_sound()
                    st.success("Order sent to kitchen!")

# ==========================================
# 6. MAIN EXECUTION (The Bootloader)
# ==========================================
def main():
    LaReinaOS.init_state()
    apply_enterprise_styles()
    render_sidebar()

    if st.session_state.view == "Customer":
        render_customer_view()
    elif st.session_state.view == "Kitchen (KDS)":
        render_kds_view()
    else:
        st.title("Admin Dashboard")
        st.write("Detailed analytics and inventory management coming soon.")

if __name__ == "__main__":
    main()
