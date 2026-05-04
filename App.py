import streamlit as st
from streamlit_pills import pills
import pandas as pd
import time
import datetime
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as components

# ==========================================
# 1. GLOBAL SYSTEM CONFIGURATION
# ==========================================
class SystemConfig:
    RESTAURANT_NAME = "La Reina"
    VERSION = "2.0.4-PRO"
    PRIMARY_COLOR = "#FFD700"  # Gold
    ACCENT_COLOR = "#7FFF00"   # Poblano Green
    BG_COLOR = "#000000"       # Deep Black
    LOGO_PATH = "logo.png"     # Case-sensitive file name
    REFRESH_RATE = 5000        # 5 Seconds for live order syncing

st.set_page_config(
    page_title=f"{SystemConfig.RESTAURANT_NAME} OS",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. ADVANCED CSS ENGINE (Industrial UX)
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

        /* Header & Logo Container */
        .header-container {{
            display: flex;
            justify-content: center;
            padding: 20px 0;
            border-bottom: 1px solid #222;
        }}

        /* The "Poblano" Status Bar */
        .status-engine {{
            background: linear-gradient(90deg, #111, #222);
            border: 2px solid {SystemConfig.ACCENT_COLOR};
            color: {SystemConfig.ACCENT_COLOR};
            padding: 12px;
            text-align: center;
            font-weight: 700;
            border-radius: 8px;
            margin: 20px 0;
            text-transform: uppercase;
            letter-spacing: 3px;
            box-shadow: 0 0 15px rgba(127, 255, 0, 0.2);
        }}

        /* Enterprise Menu Cards */
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
        }}

        .menu-card:hover {{
            border-color: {SystemConfig.PRIMARY_COLOR};
            transform: translateY(-5px);
        }}

        .item-title {{
            color: {SystemConfig.PRIMARY_COLOR};
            font-size: 26px;
            font-weight: 800;
            margin-bottom: 5px;
        }}

        .item-meta {{
            color: #888;
            font-size: 14px;
            line-height: 1.4;
        }}

        .price-tag {{
            color: {SystemConfig.PRIMARY_COLOR};
            font-size: 22px;
            font-weight: 700;
            margin-top: 15px;
        }}

        /* Hardware Button Simulation */
        .stButton>button {{
            width: 100%;
            background-color: transparent !important;
            border: 2px solid #444 !important;
            color: white !important;
            height: 50px !important;
            border-radius: 8px !important;
            transition: 0.2s;
        }}

        .stButton>button:hover {{
            border-color: {SystemConfig.PRIMARY_COLOR} !important;
            color: {SystemConfig.PRIMARY_COLOR} !important;
            background: rgba(255, 215, 0, 0.1) !important;
        }}

        /* Hide Streamlit Junk */
        header {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        #MainMenu {{visibility: hidden;}}
        </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. STATE & DATA MANAGEMENT
# ==========================================
def initialize_session():
    if 'orders' not in st.session_state:
        st.session_state.orders = []
    if 'metrics' not in st.session_state:
        st.session_state.metrics = {"avg_prep_time": 0, "total_today": 0}
    if 'last_update' not in st.session_state:
        st.session_state.last_update = datetime.datetime.now()

def load_master_menu():
    # Structured as an enterprise JSON object for future database migration
    return {
        "Tacos": [
            {"id": "T1", "name": "Street Taco", "desc": "Cilantro, onion, lime, choice of protein", "price": 3.50},
            {"id": "T2", "name": "Al Pastor", "desc": "Marinated pork, pineapple, spicy salsa", "price": 4.00},
            {"id": "T3", "name": "Barbacoa", "desc": "Slow-braised beef, tender & rich", "price": 4.50},
            {"id": "T4", "name": "Carnitas", "desc": "Crispy shredded pork, pickled red onions", "price": 4.00}
        ],
        "Entrees": [
            {"id": "E1", "name": "Enchiladas", "desc": "Three corn tortillas, salsa verde, queso fresco", "price": 12.00},
            {"id": "E2", "name": "Burrito Grande", "desc": "Rice, beans, protein, smothered in queso", "price": 13.50}
        ],
        "Drinks": [
            {"id": "D1", "name": "House Margarita", "desc": "Gold tequila, lime, agave", "price": 9.00},
            {"id": "D2", "name": "Paloma", "desc": "Grapefruit soda, tequila, salt rim", "price": 10.00}
        ],
        "Rewards 👑": []
    }

# ==========================================
# 4. HARDWARE INTEGRATION: Audio & Key-Listening
# ==========================================
def inject_hardware_listeners():
    # Audio Alert & Spacebar Listener
    hardware_js = """
    <script>
    const doc = window.parent.document;
    const audio = new Audio('https://www.soundjay.com/buttons/beep-01a.mp3');
    
    doc.addEventListener('keydown', function(e) {
        if (e.keyCode === 32) { // Spacebar (Physical Bump Bar)
            window.parent.postMessage({type: 'BUMP_ORDER'}, '*');
        }
    });
    </script>
    """
    components.html(hardware_js, height=0)

# ==========================================
# 5. CORE UI LAYOUT
# ==========================================
def main():
    initialize_session()
    inject_custom_styles()
    inject_hardware_listeners()
    
    # 5a. Global Logo Injection (Centering logic)
    _, logo_col, _ = st.columns([1, 2, 1])
    with logo_col:
        try:
            st.image(SystemConfig.LOGO_PATH, use_container_width=True)
        except:
            st.markdown(f"<h1 style='text-align:center; color:{SystemConfig.PRIMARY_COLOR};'>LA REINA</h1>", unsafe_allow_html=True)

    # 5b. The Industrial Status Bar
    st.markdown(f"""
        <div class="status-engine">
            STATUS: POBLANO 🫑 | VERSION {SystemConfig.VERSION} | ENGINE LIVE
        </div>
    """, unsafe_allow_html=True)

    # 5c. Multi-Category Navigation
    menu = load_master_menu()
    selected_category = pills("", list(menu.keys()), index=0, 
                              active_format="bold",
                              colors={"active": "#FF4B4B", "inactive": "#222"})

    # 5d. Grid Engine (Dynamic Column Logic)
    if selected_category:
        items = menu[selected_category]
        if not items:
            st.info("Rewards Portal initializing. Connect your La Reina membership card to continue.")
        else:
            cols = st.columns(2)
            for idx, item in enumerate(items):
                with cols[idx % 2]:
                    # The Menu Card Component
                    st.markdown(f"""
                        <div class="menu-card">
                            <div>
                                <div class="item-title">{item['name']}</div>
                                <div class="item-meta">{item['desc']}</div>
                            </div>
                            <div class="price-tag">${item['price']:.2f}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Action Logic
                    if st.button(f"SELECT {item['id']}", key=f"btn_{item['id']}"):
                        st.toast(f"Adding {item['name']} to order...")

    # 5e. Real-Time Logic (The "Sync" Engine)
    st_autorefresh(interval=SystemConfig.REFRESH_RATE, key="sync_engine")

if __name__ == "__main__":
    main()
