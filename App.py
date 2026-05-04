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
    LOGO_PATH = "la_reina_dark.png"  # Hardwired for your specific asset
    REFRESH_RATE = 5000        # 5 Seconds for live order syncing

st.set_page_config(
    page_title=f"{SystemConfig.RESTAURANT_NAME} OS",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. ADVANCED CSS ENGINE (Bulletproof Styling)
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

        /* The Minimalist "Poblano" Status Bar */
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
            font-weight: bold !important;
        }}

        .stButton>button:hover {{
            border-color: {SystemConfig.PRIMARY_COLOR} !important;
            color: {SystemConfig.PRIMARY_COLOR} !important;
            background: rgba(255, 215, 0, 0.1) !important;
        }}

        /* PILLS OVERRIDE: Fixing the TypeError from the library */
        div[data-testid="stMarkdownContainer"] p {{
            font-weight: bold;
            font-size: 16px;
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

def load_master_menu():
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
# 4. HARDWARE INTEGRATION (Spacebar Listener)
# ==========================================
def inject_hardware_listeners():
    hardware_js = """
    <script>
    const doc = window.parent.document;
    doc.addEventListener('keydown', function(e) {
        if (e.keyCode === 32) { // Spacebar Detection
            console.log("HARDWARE BUMP DETECTED");
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
    
    # 5a. Global Logo Injection
    _, logo_col, _ = st.columns([1, 2, 1])
    with logo_col:
        try:
            st.image(SystemConfig.LOGO_PATH, use_container_width=True)
        except:
            # Fallback if the logo ever gets deleted or renamed
            st.markdown(f"<h1 style='text-align:center; color:{SystemConfig.PRIMARY_COLOR};'>{SystemConfig.RESTAURANT_NAME}</h1>", unsafe_allow_html=True)

    # 5b. The Minimalist Status Bar
    st.markdown(f"""
        <div class="status-engine">
            STATUS: POBLANO 🫑
        </div>
    """, unsafe_allow_html=True)

    # 5c. Multi-Category Navigation
    menu = load_master_menu()
    selected_category = pills("Navigation", list(menu.keys()), index=0)

    # 5d. Grid Engine
    if selected_category:
        items = menu[selected_category]
        if not items:
            st.info("Rewards Engine Offline. Awaiting Database Link.")
        else:
            cols = st.columns(2)
            for idx, item in enumerate(items):
                with cols[idx % 2]:
                    # Build Card
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
                    if st.button(f"FIRE {item['id']}", key=f"btn_{item['id']}"):
                        st.toast(f"{item['name']} sent to kitchen array.")

    # 5e. Real-Time Refresh Loop
    st_autorefresh(interval=SystemConfig.REFRESH_RATE, key="sync_engine")

if __name__ == "__main__":
    main()
