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
    page_title=f"{SystemConfig.RESTAURANT_NAME} Rewards",
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
            text-transform: uppercase;
        }}

        .stButton>button:hover {{
            border-color: {SystemConfig.PRIMARY_COLOR} !important;
            color: {SystemConfig.PRIMARY_COLOR} !important;
            background: rgba(255, 215, 0, 0.1) !important;
        }}

        /* Login Input Styling */
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

        /* Tier Box Styling */
        .tier-box {{
            background: #111;
            border: 1px solid #333;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            height: 100%;
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
# 3. STATE, TIER LOGIC & DATABASE
# ==========================================
def initialize_session():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'phone_number' not in st.session_state:
        st.session_state.phone_number = ""
    # REWARDS START AT ZERO
    if 'reward_points' not in st.session_state:
        st.session_state.reward_points = 0 

def get_tier_info(pts):
    """The Dynamic Gamification Engine"""
    if pts < 100:
        return "POBLANO 🫑", 100, "JALAPEÑO 🌶️"
    elif pts < 300:
        return "JALAPEÑO 🌶️", 300, "HABANERO 🔥"
    else:
        return "HABANERO 🔥", 1000, "EL REY 👑" # Max theoretical tier

def load_master_menu():
    return {
        "Lunch Specials": [
            {"id": "L1", "name": "Speedy Gonzales", "desc": "One taco, one enchilada, choice of rice or beans.", "price": 7.99},
            {"id": "L2", "name": "Lunch Fajitas", "desc": "Steak or Chicken, peppers, onions, rice, beans, tortillas.", "price": 10.50},
            {"id": "L3", "name": "ACP (Arroz Con Pollo)", "desc": "Grilled chicken over rice, smothered in white queso.", "price": 9.99},
        ],
        "Appetizers": [
            {"id": "A1", "name": "Queso Blanco", "desc": "Creamy melted white cheese dip with jalapeño hints.", "price": 5.99},
            {"id": "A2", "name": "Fresh Guacamole", "desc": "Avocado, lime, cilantro, tomatoes, onions. Made daily.", "price": 7.50},
            {"id": "A3", "name": "Nachos Supremos", "desc": "Beef, chicken, beans, queso, lettuce, sour cream, tomatoes.", "price": 11.99},
        ],
        "Tacos": [
            {"id": "T1", "name": "Street Taco (Asada)", "desc": "Steak, cilantro, onion, lime on corn tortillas.", "price": 3.50},
            {"id": "T2", "name": "Al Pastor", "desc": "Marinated pork, pineapple, cilantro, onion.", "price": 3.75},
            {"id": "T3", "name": "Quesa-Birria", "desc": "Braised beef with melted cheese, cilantro, side of consommé.", "price": 4.50},
        ],
        "Entrees": [
            {"id": "E1", "name": "Burrito California", "desc": "Massive burrito: steak, fries, cheese, guac, sour cream inside.", "price": 14.50},
            {"id": "E2", "name": "Enchiladas Suizas", "desc": "Three chicken enchiladas, salsa verde, cheese, cilantro.", "price": 12.99},
            {"id": "E3", "name": "Carne Asada", "desc": "Thinly sliced grilled steak, grilled onions, rice, beans, guac salad.", "price": 17.50},
        ],
        "Drinks": [
            {"id": "D1", "name": "La Reina House Rita", "desc": "Classic gold tequila, fresh lime, agave. Rocks or Frozen.", "price": 8.99},
            {"id": "D2", "name": "Top Shelf Margarita", "desc": "Patrón Silver, Grand Marnier, fresh lime.", "price": 13.00},
            {"id": "D3", "name": "Spicy Mango Rita", "desc": "Tequila, mango purée, fresh jalapeño, Tajín rim.", "price": 10.50},
        ],
        "Rewards 👑": []
    }

# ==========================================
# 4. SCREENS (Login & Main OS)
# ==========================================
def render_login_screen():
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 2, 1])
    
    with col:
        try:
            st.image(SystemConfig.LOGO_PATH, use_container_width=True)
        except:
            st.markdown(f"<h1 style='text-align:center; color:{SystemConfig.PRIMARY_COLOR};'>{SystemConfig.RESTAURANT_NAME}</h1>", unsafe_allow_html=True)
        
        st.markdown(f"<h4 style='text-align:center; color:#888; margin-bottom: 20px;'>ENTER PHONE NUMBER TO UNLOCK</h4>", unsafe_allow_html=True)
        
        # Frictionless Gate: Removed Button
        phone_input = st.text_input("PHONE", placeholder="10-DIGIT NUMBER", label_visibility="collapsed", max_chars=10)
        st.markdown("<p style='text-align:center; color:#555; font-size:12px;'>Press ENTER to authenticate</p>", unsafe_allow_html=True)
        
        if phone_input:
            cleaned_phone = ''.join(filter(str.isdigit, phone_input))
            if len(cleaned_phone) >= 10: 
                st.session_state.authenticated = True
                st.session_state.phone_number = cleaned_phone
                st.rerun() 
            else:
                st.error("Access Denied. 10-digit sequence required.")

def render_main_os():
    _, logo_col, _ = st.columns([1, 2, 1])
    with logo_col:
        try:
            st.image(SystemConfig.LOGO_PATH, use_container_width=True)
        except:
            st.markdown(f"<h1 style='text-align:center; color:{SystemConfig.PRIMARY_COLOR};'>{SystemConfig.RESTAURANT_NAME}</h1>", unsafe_allow_html=True)

    # Dynamic Tier Math
    pts = st.session_state.reward_points
    current_tier, target, next_tier = get_tier_info(pts)
    progress_percentage = min(int((pts / target) * 100), 100)
    pts_away = target - pts

    # Customer-Facing Status Bar
    st.markdown(f"""
        <div class="status-engine">
            <div class="status-header">
                <span style="color: {SystemConfig.PRIMARY_COLOR};">TIER: {current_tier}</span>
                <span>MEMBER: {st.session_state.phone_number}</span>
            </div>
            <div style="width: 100%; background-color: #222; height: 12px; border-radius: 6px; margin-bottom: 5px; overflow: hidden; border: 1px solid #333;">
                <div style="width: {progress_percentage}%; background-color: {SystemConfig.PRIMARY_COLOR}; height: 100%; box-shadow: 0 0 10px {SystemConfig.PRIMARY_COLOR}; border-radius: 6px;"></div>
            </div>
            <div style="text-align: right; color: #888; font-size: 12px; font-weight: bold;">
                {pts} / {target} PTS — <span style="color: {SystemConfig.PRIMARY_COLOR};">{pts_away} PTS AWAY FROM {next_tier}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    menu = load_master_menu()
    selected_category = pills("Navigation", list(menu.keys()), index=0)

    # ==========================================
    # REWARDS PORTAL (Receipt Scanner & Overview)
    # ==========================================
    if selected_category == "Rewards 👑":
        st.markdown(f"<h2 style='color: {SystemConfig.PRIMARY_COLOR}; text-align: center;'>LA REINA LOYALTY TIERS</h2>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Tier Visuals
        t1, t2, t3 = st.columns(3)
        with t1:
            st.markdown("""
            <div class="tier-box">
                <h3 style="color:#7FFF00;">POBLANO 🫑</h3>
                <p style="color:#888;">0 - 100 Points</p>
                <p>• Free Birthday Dessert<br>• Access to Secret Menu<br>• $5 Off Next Visit</p>
            </div>
            """, unsafe_allow_html=True)
        with t2:
            st.markdown("""
            <div class="tier-box" style="border-color: #FFA500;">
                <h3 style="color:#FFA500;">JALAPEÑO 🌶️</h3>
                <p style="color:#888;">100 - 300 Points</p>
                <p>• Free Queso or Guac<br>• Priority Seating<br>• 2x Points on Tuesdays</p>
            </div>
            """, unsafe_allow_html=True)
        with t3:
            st.markdown("""
            <div class="tier-box" style="border-color: #FF4500;">
                <h3 style="color:#FF4500;">HABANERO 🔥</h3>
                <p style="color:#888;">300+ Points</p>
                <p>• Free Entree Every 10 Visits<br>• VIP Tasting Events<br>• Exclusive Merch</p>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<hr style='border-color: #333;'>", unsafe_allow_html=True)
        
        # Receipt Scanner Integration
        st.markdown("<h3 style='text-align: center;'>📸 SCAN RECEIPT FOR POINTS</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #888;'>Align your receipt barcode or QR code in the frame below.</p>", unsafe_allow_html=True)
        
        receipt_img = st.camera_input("Scan Receipt", label_visibility="collapsed")
        
        if receipt_img:
            # Simulated Processing Time & Point Award
            st.success("Receipt successfully scanned! Processing transaction...")
            st.session_state.reward_points += 45 # Mock point boost
            st.balloons() # Gamification reward
            st.rerun()

    # ==========================================
    # MENU ENGINE
    # ==========================================
    elif selected_category:
        items = menu[selected_category]
        if not items:
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
                    
                    # Renamed from FIRE to ADD + Item Name
                    if st.button(f"+ ADD {item['name']}", key=f"btn_{item['id']}"):
                        st.session_state.reward_points += int(float(item['price']))
                        st.toast(f"Added {item['name']} to your tray! Earned points.")
                        st.rerun() 

# ==========================================
# 5. ROUTER
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
