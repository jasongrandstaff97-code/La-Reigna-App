import streamlit as st
from streamlit_autorefresh import st_autorefresh
import sys
import os

# Add parent directory to path so it can find the database_engine file
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database_engine import SystemConfig, get_sales_data, bump_kitchen_ticket

st.set_page_config(
    page_title="KDS Terminal",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def inject_kds_styles():
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
        .stApp {{ background-color: {SystemConfig.BG_COLOR}; color: #FFFFFF; font-family: 'JetBrains Mono', monospace; }}
        
        .kds-ticket {{
            background-color: #1a1a1a;
            border-top: 5px solid {SystemConfig.PRIMARY_COLOR};
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            height: 100%;
        }}
        .kds-header {{
            font-size: 24px; font-weight: 900; color: #FFF;
            border-bottom: 2px dashed #444; padding-bottom: 10px;
            margin-bottom: 10px; display: flex; justify-content: space-between;
        }}
        .kds-item {{ font-size: 20px; font-weight: bold; color: {SystemConfig.ACCENT_COLOR}; margin-bottom: 8px; padding-left: 10px; border-left: 3px solid #444; }}
        
        .bump-btn>button {{
            background-color: #333 !important; border-color: #555 !important;
            color: #FFF !important; font-size: 18px !important;
            height: 60px !important; margin-top: 15px !important; width: 100%;
            transition: 0.2s; font-weight: bold !important; border-radius: 8px !important;
        }}
        .bump-btn>button:hover {{ background-color: {SystemConfig.ACCENT_COLOR} !important; color: #000 !important; border-color: {SystemConfig.ACCENT_COLOR} !important; }}
        
        header {{visibility: hidden;}} footer {{visibility: hidden;}} #MainMenu {{visibility: hidden;}}
        </style>
    """, unsafe_allow_html=True)

def render_kds():
    inject_kds_styles()
    
    st.markdown(f"<h1 style='color:{SystemConfig.ACCENT_COLOR}; font-size: 36px; font-weight: 900; margin-top: -20px; letter-spacing: 2px;'>LA REINA // ACTIVE KITCHEN QUEUE</h1>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color: #333; margin-top: 0px;'>", unsafe_allow_html=True)
    
    sales_data = get_sales_data()
    active_tickets = [order for order in sales_data if order.get("status") == "PENDING"]

    if not active_tickets:
        st.markdown(f"<h2 style='text-align: center; color: #555; margin-top: 100px;'>NO ACTIVE ORDERS<br>KITCHEN IS CLEAR</h2>", unsafe_allow_html=True)
    else:
        cols = st.columns(4)
        for idx, ticket in enumerate(active_tickets):
            with cols[idx % 4]:
                st.markdown("<div class='kds-ticket'>", unsafe_allow_html=True)
                
                time_only = ticket['timestamp'].split()[1][:5]
                order_type_color = SystemConfig.PRIMARY_COLOR if "DINE-IN" in ticket['type'] else "#FF4B4B"
                
                st.markdown(f"""
                    <div class="kds-header">
                        <span>#{ticket['order_id']}</span>
                        <span>{time_only}</span>
                    </div>
                    <div style="color: {order_type_color}; font-weight: bold; font-size: 18px; margin-bottom: 15px; letter-spacing: 1px;">
                        {ticket['type']}
                    </div>
                """, unsafe_allow_html=True)
                
                for item in ticket['items']:
                    st.markdown(f"<div class='kds-item'>• {item}</div>", unsafe_allow_html=True)
                
                st.markdown("<div class='bump-btn'>", unsafe_allow_html=True)
                if st.button("BUMP TICKET", key=f"bump_{ticket['order_id']}"):
                    bump_kitchen_ticket(ticket['order_id'])
                    st.rerun()
                st.markdown("</div></div>", unsafe_allow_html=True)

    # Scans the shared database engine every 3 seconds for new orders
    st_autorefresh(interval=3000, key="kds_sync") 

if __name__ == "__main__":
    render_kds()
