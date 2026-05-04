import streamlit as st
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as components
import sys
import os

# ==========================================
# 1. SYSTEM BRIDGE
# Add parent directory to path so it can talk to the database_engine
# ==========================================
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database_engine import SystemConfig, get_sales_data, bump_kitchen_ticket

st.set_page_config(
    page_title="La Reina KDS",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. HIGH-CONTRAST CSS ENGINE
# ==========================================
def inject_kds_styles():
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
        
        .stApp {{ 
            background-color: {SystemConfig.BG_COLOR}; 
            color: #FFFFFF; 
            font-family: 'JetBrains Mono', monospace; 
        }}
        
        /* The Physical Ticket Card */
        .kds-ticket {{
            background-color: #1a1a1a;
            border-top: 5px solid {SystemConfig.PRIMARY_COLOR};
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}
        
        .kds-header {{
            font-size: 26px; 
            font-weight: 900; 
            color: #FFF;
            border-bottom: 2px dashed #444; 
            padding-bottom: 10px;
            margin-bottom: 15px; 
            display: flex; 
            justify-content: space-between;
        }}
        
        .kds-item {{ 
            font-size: 22px; 
            font-weight: bold; 
            color: {SystemConfig.ACCENT_COLOR}; 
            margin-bottom: 10px; 
            padding-left: 10px; 
            border-left: 4px solid #444; 
        }}
        
        /* The Digital Bump Button */
        .bump-btn>button {{
            background-color: #333 !important; 
            border: 2px solid #555 !important;
            color: #FFF !important; 
            font-size: 20px !important;
            height: 65px !important; 
            margin-top: 20px !important; 
            width: 100%;
            transition: 0.2s; 
            font-weight: bold !important; 
            border-radius: 8px !important;
            letter-spacing: 2px;
        }}
        
        .bump-btn>button:hover {{ 
            background-color: {SystemConfig.ACCENT_COLOR} !important; 
            color: #000 !important; 
            border-color: {SystemConfig.ACCENT_COLOR} !important; 
            box-shadow: 0 0 15px rgba(127, 255, 0, 0.4) !important;
        }}
        
        /* Hide Streamlit Junk */
        header {{visibility: hidden;}} 
        footer {{visibility: hidden;}} 
        #MainMenu {{visibility: hidden;}}
        </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. CORE KITCHEN RENDER ENGINE
# ==========================================
def render_kds():
    inject_kds_styles()
    
    # --- HARDWARE LISTENER INJECTION ---
    # Listens for the physical Spacebar (Keycode 32) and clicks the oldest ticket
    hardware_js = """
    <script>
    const doc = window.parent.document;
    doc.addEventListener('keydown', function(e) {
        if (e.keyCode === 32) { 
            e.preventDefault(); // Stop the screen from jumping down
            const buttons = doc.querySelectorAll('button');
            for (let i = 0; i < buttons.length; i++) {
                if (buttons[i].innerText.includes("BUMP TICKET")) {
                    buttons[i].click();
                    break; // Only clear one ticket at a time
                }
            }
        }
    });
    </script>
    """
    components.html(hardware_js, height=0, width=0)
    # -----------------------------------
    
    # KDS Header
    st.markdown(f"<h1 style='color:{SystemConfig.ACCENT_COLOR}; font-size: 40px; font-weight: 900; margin-top: -30px; letter-spacing: 2px;'>LA REINA // ACTIVE QUEUE</h1>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color: #333; margin-top: 0px;'>", unsafe_allow_html=True)
    
    # -----------------------------------
    # DATABASE SWEEP (Looks for PENDING tickets)
    # -----------------------------------
    sales_data = get_sales_data()
    active_tickets = [order for order in sales_data if order.get("status") == "PENDING"]

    if not active_tickets:
        st.markdown(f"<h2 style='text-align: center; color: #444; margin-top: 150px; font-size: 50px;'>NO ACTIVE ORDERS<br>KITCHEN IS CLEAR</h2>", unsafe_allow_html=True)
    else:
        # Create a dynamic 4-column grid across the TV/Monitor
        cols = st.columns(4)
        for idx, ticket in enumerate(active_tickets):
            with cols[idx % 4]:
                st.markdown("<div class='kds-ticket'>", unsafe_allow_html=True)
                
                # Format time (e.g., 18:45)
                time_only = ticket['timestamp'].split()[1][:5]
                
                # Visual Routing: Gold for Dine-In, Red for To-Go
                order_type_color = SystemConfig.PRIMARY_COLOR if "DINE-IN" in ticket['type'] else "#FF4B4B"
                border_color = order_type_color
                
                # Ticket Header HTML
                st.markdown(f"""
                    <div style="border-top: 5px solid {border_color}; margin: -20px -20px 15px -20px; border-radius: 8px 8px 0 0;"></div>
                    <div class="kds-header">
                        <span>#{ticket['order_id']}</span>
                        <span>{time_only}</span>
                    </div>
                    <div style="color: {order_type_color}; font-weight: bold; font-size: 22px; margin-bottom: 20px; letter-spacing: 1px;">
                        {ticket['type']}
                    </div>
                """, unsafe_allow_html=True)
                
                # Render the food items
                st.markdown("<div>", unsafe_allow_html=True)
                for item in ticket['items']:
                    st.markdown(f"<div class='kds-item'>{item}</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                # The execution button
                st.markdown("<div class='bump-btn'>", unsafe_allow_html=True)
                if st.button("BUMP TICKET", key=f"bump_{ticket['order_id']}"):
                    bump_kitchen_ticket(ticket['order_id'])
                    st.rerun()
                st.markdown("</div></div>", unsafe_allow_html=True)

    # -----------------------------------
    # THE PULSE: Refreshes the screen every 3000ms (3 seconds)
    # -----------------------------------
    st_autorefresh(interval=3000, key="kds_sync") 

if __name__ == "__main__":
    render_kds()
