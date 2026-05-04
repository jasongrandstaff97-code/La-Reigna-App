import streamlit as st
from streamlit_pills import pills
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as components

# ==========================================
# 1. GLOBAL SYSTEM CONFIGURATION
# ==========================================
class SystemConfig:
    RESTAURANT_NAME = "La Reina"
    PRIMARY_COLOR = "#FFD700"  # Gold
    ACCENT_COLOR = "#7FFF00"   # Poblano Green
    BG_COLOR = "#000000"       # Deep Black
    LOGO_PATH = "la_reina_dark.png" 
    REFRESH_RATE = 5000        # Live sync interval

st.set_page_config(
    page_title=f"{SystemConfig.RESTAURANT_NAME} OS",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. ADVANCED CSS ENGINE
# ==========================================
def inject_custom_styles():
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');

        .stApp {{
            background-color: {SystemConfig.BG_COLOR};
            color: #FFFFFF;
            font-family: 'JetBrains Mono', monospace;
        }}

        .status-engine {{
            background: linear-gradient(90deg, #111, #222);
            border: 2px solid {SystemConfig.ACCENT_COLOR};
            padding: 15px 20px;
            border-radius: 8px;
            margin: 20px 0;
            box-shadow: 0 0 15px rgba(127, 255, 0, 0.15);
        }}
        
        .status-header {{
            display: flex;
            justify-content: space-between;
            color: {SystemConfig.ACCENT_COLOR};
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 10px;
            font-size: 14px;
        }}

        .menu-card {{
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(10px);
            border: 1px solid #333;
            border-radius: 12px;
            padding: 25px;
            transition: all 0.3s ease;
            height: 220px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            margin-bottom: 15px;
        }}

        .menu-card:hover {{
            border-color: {SystemConfig.PRIMARY_COLOR};
            transform: translateY(-5px);
        }}

        .item-title {{
            color: {SystemConfig.PRIMARY_COLOR};
            font-size: 24px;
            font-weight: 800;
            margin-bottom: 5px;
            line-height: 1.2;
        }}

        .item-meta {{
            color: #888;
            font-size: 13px;
            line-height: 1.4;
        }}

        .price-tag {{
            color: {SystemConfig.PRIMARY_COLOR};
            font-size: 22px;
            font-weight: 700;
            margin-top: 15px;
        }}

        .stButton>button {{
            width: 100%;
            background-color: transparent !important;
            border: 2px solid #444 !important;
            color: white !important;
            height: 50px !important;
            border-radius: 8px !important;
            transition: 0.2s;
            font-weight: bold !important;
        }}

        .stButton>button:hover {{
            border-color: {SystemConfig.PRIMARY_COLOR} !important;
            color: {SystemConfig.PRIMARY_COLOR} !important;
            background: rgba(255, 215, 0, 0.1) !important;
        }}

        .stTextInput>div>div>input {{
            background-color: #111 !important;
            color: {SystemConfig.PRIMARY_COLOR} !important;
            border: 2px solid #333 !important;
            border-radius: 8px !important;
            font-size: 24px !important;
            text-align: center !important;
            height: 60px !important;
            letter-spacing: 2px;
        }}
        
        .stTextInput>div>div>input:focus {{
            border-color: {SystemConfig.ACCENT_COLOR} !important;
            box-shadow: 0 0 10px rgba(127, 255, 0, 0.3) !important;
        }}

        div[data-testid="stMarkdownContainer"] p {{
            font-weight: bold;
            font-size: 16px;
        }}

        header {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        #MainMenu {{visibility: hidden;}}
        </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. STATE & FULL DATABASE LOAD
# ==========================================
def initialize_session():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'phone_number' not in st.session_state:
        st.session_state.phone_number = ""
    if 'reward_points' not in st.session_state:
        st.session_state.reward_points = 65 
    if 'tier_target' not in st.session_state:
        st.session_state.tier_target = 100   
    if 'next_tier_name' not in st.session_state:
        st.session_state.next_tier_name = "REYES VIP TIER"

def load_master_menu():
    """The fully populated Data Engine."""
    return {
        "Lunch Specials": [
            {"id": "L1", "name": "Speedy Gonzales", "desc": "One taco, one enchilada, choice of rice or beans.", "price": 7.99},
            {"id": "L2", "name": "Lunch Fajitas", "desc": "Steak or Chicken, peppers, onions, rice, beans, tortillas.", "price": 10.50},
            {"id": "L3", "name": "ACP (Arroz Con Pollo)", "desc": "Grilled chicken over rice, smothered in white queso.", "price": 9.99},
            {"id": "L4", "name": "Lunch Chimichanga", "desc": "Fried burrito topped with queso, served with rice and crema salad.", "price": 9.50},
            {"id": "L5", "name": "Huevos Rancheros", "desc": "Two fried eggs, ranchero sauce, rice, beans, tortillas.", "price": 8.50}
        ],
        "Appetizers": [
            {"id": "A1", "name": "Queso Blanco", "desc": "Creamy melted white cheese dip with jalapeño hints.", "price": 5.99},
            {"id": "A2", "name": "Fresh Guacamole", "desc": "Avocado, lime, cilantro, tomatoes, onions. Made daily.", "price": 7.50},
            {"id": "A3", "name": "Nachos Supremos", "desc": "Beef, chicken, beans, queso, lettuce, sour cream, tomatoes.", "price": 11.99},
            {"id": "A4", "name": "Chorizo Dip", "desc": "Mexican sausage mixed with our signature white queso.", "price": 8.50}
        ],
        "Tacos": [
            {"id": "T1", "name": "Street Taco (Asada)", "desc": "Steak, cilantro, onion, lime on corn tortillas.", "price": 3.50},
            {"id": "T2", "name": "Al Pastor", "desc": "Marinated pork, pineapple, cilantro, onion.", "price": 3.75},
            {"id": "T3", "name": "Quesa-Birria", "desc": "Braised beef with melted cheese, cilantro, onion, side of consommé.", "price": 4.50},
            {"id": "T4", "name": "Carnitas", "desc": "Crispy slow-roasted pork, pickled red onions.", "price": 3.50},
            {"id": "T5", "name": "Baja Fish Taco", "desc": "Crispy fish, chipotle slaw, avocado on flour tortillas.", "price": 4.00}
        ],
        "Fajitas": [
            {"id": "F1", "name": "Steak Fajitas", "desc": "Sizzling steak, bell peppers, onions. Includes rice, beans, salad.", "price": 16.99},
            {"id": "F2", "name": "Chicken Fajitas", "desc": "Sizzling grilled chicken breast, bell peppers, onions.", "price": 15.99},
            {"id": "F3", "name": "Texas Fajitas", "desc": "The Trio: Steak, Chicken, and Shrimp.", "price": 18.99},
            {"id": "F4", "name": "Veggie Fajitas", "desc": "Grilled mushrooms, zucchini, peppers, onions, tomatoes.", "price": 13.99}
        ],
        "Entrees": [
            {"id": "E1", "name": "Burrito California", "desc": "Massive burrito: steak, fries, cheese, guac, sour cream inside.", "price": 14.50},
            {"id": "E2", "name": "Enchiladas Suizas", "desc": "Three chicken enchiladas, salsa verde, cheese, cilantro.", "price": 12.99},
            {"id": "E3", "name": "Carne Asada", "desc": "Thinly sliced grilled steak, grilled onions, rice, beans, guac salad.", "price": 17.50},
            {"id": "E4", "name": "Pollo Loco", "desc": "Grilled chicken breast topped with spinach and queso.", "price": 14.99},
            {"id": "E5", "name": "Carnitas Dinner", "desc": "Traditional slow-cooked pork chunks, rice, beans, tortillas.", "price": 15.50}
        ],
        "Drinks": [
            {"id": "D1", "name": "La Reina House Rita", "desc": "Classic gold tequila, fresh lime, agave. Rocks or Frozen.", "price": 8.99},
            {"id": "D2", "name": "Top Shelf Margarita", "desc": "Patrón Silver, Grand Marnier, fresh lime.", "price": 13.00},
            {"id": "D3", "name": "Spicy Mango Rita", "desc": "Tequila, mango purée, fresh jalapeño, Tajín rim.", "price": 10.50},
            {"id": "D4", "name": "Paloma", "desc": "Grapefruit soda, silver tequila, fresh lime, salt rim.", "price": 9.50},
            {"id": "D5", "name": "Agua de Horchata", "desc": "Sweet rice milk with vanilla and cinnamon.", "price": 3.50},
            {"id": "D6", "name": "Modelo Especial", "desc": "Draft or Bottle. Serve chilled with a lime.", "price": 5.00}
        ],
        "Desserts": [
            {"id": "DS1", "name": "Churros", "desc": "Fried dough pastry dusted in cinnamon sugar, chocolate drizzle.", "price": 5.99},
            {"id": "DS2", "name": "Fried Ice Cream", "desc": "Vanilla ice cream in a crispy shell, whipped cream, honey.", "price": 6.50},
            {"id": "DS3", "name": "Flan", "desc": "Traditional Mexican baked caramel custard.", "price": 5.00}
        ],
        "Rewards 👑": []
    }

# ==========================================
# 4. HARDWARE INTEGRATION
# ==========================================
def inject_hardware_listeners():
    hardware_js = """
    <script>
    const doc = window.parent.document;
    doc.addEventListener('keydown', function(e) {
        if (e.keyCode === 32) { 
            console.log("HARDWARE BUMP DETECTED");
        }
    });
    </script>
    """
    components.html(hardware_js, height=0)

# ==========================================
# 5. SCREENS (Login & Main OS)
# ==========================================
def render_login_screen():
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 2, 1])
    
    with col:
        try:
            st.image(SystemConfig.LOGO_PATH, use_container_width=True)
        except:
            st.markdown(f"<h1 style='text-align:center; color:{SystemConfig.PRIMARY_COLOR};'>{SystemConfig.RESTAURANT_NAME}</h1>", unsafe_allow_html=True)
        
        st.markdown(f"<h4 style='text-align:center; color:#888; margin-bottom: 30px;'>ENTER PHONE NUMBER TO UNLOCK REWARDS</h4>", unsafe_allow_html=True)
        
        phone_input = st.text_input("PHONE", placeholder="(555) 555-5555", label_visibility="collapsed")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("UNLOCK SYSTEM"):
            if len(phone_input) >= 10: 
                st.session_state.authenticated = True
                st.session_state.phone_number = phone_input
                st.rerun() 
            else:
                st.error("Invalid sequence. Please enter a valid 10-digit number.")

def render_main_os():
    inject_hardware_listeners()
    
    _, logo_col, _ = st.columns([1, 2, 1])
    with logo_col:
        try:
            st.image(SystemConfig.LOGO_PATH, use_container_width=True)
        except:
            st.markdown(f"<h1 style='text-align:center; color:{SystemConfig.PRIMARY_COLOR};'>{SystemConfig.RESTAURANT_NAME}</h1>", unsafe_allow_html=True)

    pts = st.session_state.reward_points
    target = st.session_state.tier_target
    progress_percentage = min(int((pts / target) * 100), 100)
    pts_away = target - pts

    st.markdown(f"""
        <div class="status-engine">
            <div class="status-header">
                <span>STATUS: POBLANO 🫑</span>
                <span>MEMBER: {st.session_state.phone_number}</span>
            </div>
            <div style="width: 100%; background-color: #222; height: 12px; border-radius: 6px; margin-bottom: 5px; overflow: hidden; border: 1px solid #333;">
                <div style="width: {progress_percentage}%; background-color: {SystemConfig.PRIMARY_COLOR}; height: 100%; box-shadow: 0 0 10px {SystemConfig.PRIMARY_COLOR}; border-radius: 6px;"></div>
            </div>
            <div style="text-align: right; color: #888; font-size: 12px; font-weight: bold;">
                {pts} / {target} PTS — <span style="color: {SystemConfig.PRIMARY_COLOR};">{pts_away} PTS AWAY FROM {st.session_state.next_tier_name}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    menu = load_master_menu()
    selected_category = pills("Navigation", list(menu.keys()), index=0)

    if selected_category:
        items = menu[selected_category]
        if not items and selected_category == "Rewards 👑":
            st.success(f"Rewards Active! You are {pts_away} points away from your next free entree.")
        elif not items:
            st.info("Menu items loading...")
        else:
            cols = st.columns(2)
            for idx, item in enumerate(items):
                with cols[idx % 2]:
                    st.markdown(f"""
                        <div class="menu-card">
                            <div>
                                <div class="item-title">{item['name']}</div>
                                <div class="item-meta">{item['desc']}</div>
                            </div>
                            <div class="price-tag">${item['price']:.2f}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"FIRE {item['id']}", key=f"btn_{item['id']}"):
                        st.session_state.reward_points += int(float(item['price']))
                        st.toast(f"{item['name']} ordered! +{int(float(item['price']))} Points earned.")
                        st.rerun() 

    st_autorefresh(interval=SystemConfig.REFRESH_RATE, key="sync_engine")

# ==========================================
# 6. ROUTER
# ==========================================
def main():
    initialize_session()
    inject_custom_styles()
    
    if not st.session_state.authenticated:
        render_login_screen()
    else:
        render_main_os()

if __name__ == "__main__":
    main()
