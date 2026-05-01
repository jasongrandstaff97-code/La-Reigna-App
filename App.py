import streamlit as st
from datetime import datetime

# ==========================================
# 1. PAGE CONFIGURATION & CUSTOM CSS
# ==========================================
st.set_page_config(page_title="La Reina Margaritas | Order", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .item-card { border: 1px solid #e6e6e6; border-radius: 10px; padding: 15px; margin-bottom: 15px; background-color: white; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    .item-title { font-size: 18px; font-weight: bold; margin-bottom: 5px; }
    .item-desc { font-size: 14px; color: #666; margin-bottom: 10px; }
    .item-price { font-size: 16px; font-weight: bold; color: #333; }
    .promo-tag { color: #d92128; font-size: 12px; font-weight: bold; }
    .tier-poblano { color: #2e7d32; font-weight: bold; }
    .tier-jalapeno { color: #f57f17; font-weight: bold; }
    .tier-habanero { color: #c62828; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. MENU DATABASE
# ==========================================
MENU = {
    "Most Ordered": [
        {"id": 1, "name": "Street Corn", "price": 5.75, "desc": "2 for $5.75.", "promo": "Buy 1, get 1 free", "img": "🌽"},
        {"id": 2, "name": "Tamale de Elote Trufado", "price": 7.00, "desc": "Sweet corn tamale, queso fresco, truffle oil.", "promo": "Buy 1, get 1 free", "img": "🫔"},
        {"id": 3, "name": "Street Tacos Asada", "price": 14.75, "desc": "Three asada or grilled chicken tacos, garnished.", "promo": None, "img": "🌮"},
        {"id": 4, "name": "Carnita Tacos", "price": 14.00, "desc": "Three slow-cooked pork tacos, lightly fried.", "promo": None, "img": "🌮"}
    ],
    "Antojitos & Botanas": [
        {"id": 5, "name": "Stuffed Avocados", "price": 13.00, "desc": "Two fresh avocados filled with cheese, jalapeño, and chorizo.", "promo": None, "img": "🥑"},
        {"id": 6, "name": "Top Shelf Guacamole", "price": 9.00, "desc": "Fresh flavor avocado dip, lime juice, garlic, onion.", "promo": None, "img": "🥣"},
        {"id": 7, "name": "Esquites De La Casa", "price": 8.00, "desc": "Charred corn kernels, epazote aioli, chile ash.", "promo": "Buy 1, get 1 free", "img": "🌽"}
    ],
    "Aguas Frescas (32 Oz)": [
        {"id": 8, "name": "Jamaica", "price": 8.50, "desc": "Refreshing Hibiscus Tea, a Classic Caribbean Beverage.", "promo": None, "img": "🥤"},
        {"id": 9, "name": "Horchata", "price": 8.50, "desc": "Sweet and refreshing Mexican drink (rice and cinnamon).", "promo": None, "img": "🥤"}
    ]
}

# ==========================================
# 3. SESSION STATE (Cart & Gamified Rewards)
# ==========================================
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'order_type' not in st.session_state:
    st.session_state.order_type = "Carry Out"
if 'user_points' not in st.session_state:
    st.session_state.user_points = 500  # Spendable currency
if 'lifetime_points' not in st.session_state:
    st.session_state.lifetime_points = 500  # Tally for Tier Status

def add_to_cart(item):
    st.session_state.cart.append(item)
    st.toast(f"Added {item['name']} to cart!")

def remove_from_cart(index):
    st.session_state.cart.pop(index)

# TIER LOGIC HELPER FUNCTION
def get_user_tier(lifetime_pts):
    if lifetime_pts >= 2500:
        return {"name": "Habanero", "icon": "🔥", "css": "tier-habanero", "base_multiplier": 15, "next_tier_req": None}
    elif lifetime_pts >= 1000:
        return {"name": "Jalapeño", "icon": "🌶️", "css": "tier-jalapeno", "base_multiplier": 12, "next_tier_req": 2500}
    else:
        return {"name": "Poblano", "icon": "🫑", "css": "tier-poblano", "base_multiplier": 10, "next_tier_req": 1000}

# ==========================================
# 4. APP HEADER & DINING OPTIONS
# ==========================================
st.title("La Reina Margaritas")
st.caption("★ 4.5 (10+) • Mexican • 1511 W State Highway J, Ozark, MO 65721")

col1, col2 = st.columns(2)
with col1:
    if st.button("🥡 Carry Out", type="primary" if st.session_state.order_type == "Carry Out" else "secondary", use_container_width=True):
        st.session_state.order_type = "Carry Out"
        st.rerun()
with col2:
    if st.button("🍽️ Dine In", type="primary" if st.session_state.order_type == "Dine In" else "secondary", use_container_width=True):
        st.session_state.order_type = "Dine In"
        st.rerun()

table_number = None
if st.session_state.order_type == "Dine In":
    table_number = st.text_input("Enter your Table Number:", placeholder="e.g., 12", max_chars=3)

st.divider()

# ==========================================
# 5. MAIN MENU DISPLAY
# ==========================================
categories = list(MENU.keys())
selected_category = st.radio("Categories", categories, horizontal=True, label_visibility="collapsed")

st.subheader(selected_category)

for item in MENU[selected_category]:
    with st.container():
        col_text, col_img = st.columns([3, 1])
        with col_text:
            st.markdown(f"<div class='item-title'>{item['name']}</div>", unsafe_allow_html=True)
            if item['promo']:
                st.markdown(f"<div class='promo-tag'>🏷️ {item['promo']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='item-desc'>{item['desc']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='item-price'>${item['price']:.2f}</div>", unsafe_allow_html=True)
        with col_img:
            st.write(f"<h1 style='text-align:center;'>{item['img']}</h1>", unsafe_allow_html=True)
            if st.button("➕ Add", key=f"add_{item['id']}", use_container_width=True):
                add_to_cart(item)
        st.markdown("<hr style='margin: 10px 0; opacity: 0.2;'>", unsafe_allow_html=True)

# ==========================================
# 6. CART & CHECKOUT SIDEBAR
# ==========================================
st.sidebar.header("🛒 Your Order")

if st.session_state.order_type == "Dine In":
    display_table = f" (Table {table_number})" if table_number else " (Pending Table #)"
    st.sidebar.caption(f"**Order Type:** Dine In{display_table}")
else:
    st.sidebar.caption("**Order Type:** Carry Out")
    
st.sidebar.divider()

if not st.session_state.cart:
    st.sidebar.info("Your cart is empty.")
else:
    subtotal = sum(item['price'] for item in st.session_state.cart)
    for i, item in enumerate(st.session_state.cart):
        col_name, col_price, col_del = st.sidebar.columns([3, 1, 1])
        col_name.write(item['name'])
        col_price.write(f"${item['price']:.2f}")
        if col_del.button("❌", key=f"del_{i}"):
            remove_from_cart(i)
            st.rerun()
            
    st.sidebar.divider()
    
    # --- GAMIFIED REWARDS LOGIC ---
    current_tier = get_user_tier(st.session_state.lifetime_points)
    
    st.sidebar.subheader("🎁 La Reina Rewards")
    
    # Display Tier Status and Progress
    st.sidebar.markdown(f"Status: <span class='{current_tier['css']}'>{current_tier['icon']} {current_tier['name']} Status</span>", unsafe_allow_html=True)
    if current_tier['next_tier_req']:
        pts_needed = current_tier['next_tier_req'] - st.session_state.lifetime_points
        st.sidebar.progress(st.session_state.lifetime_points / current_tier['next_tier_req'])
        st.sidebar.caption(f"Only {pts_needed} pts until next tier!")
    else:
        st.sidebar.caption("You are at the maximum rewards tier!")

    st.sidebar.write(f"**Spendable Balance:** {st.session_state.user_points} pts")
    
    # Redemption Slider
    max_redeemable = min(st.session_state.user_points // 100, int(subtotal)) * 100
    discount = 0
    points_to_use = 0
    if max_redeemable > 0:
        points_to_use = st.sidebar.slider("Redeem points ($1 off per 100 pts)", 0, max_redeemable, step=100)
        discount = points_to_use / 100
        if discount > 0:
            st.sidebar.success(f"Applying ${discount:.2f} reward discount!")

    # Calculate Earnings based on Tier & Day
    today = datetime.now().weekday()
    is_double_points = today in [2, 6]
    points_multiplier = current_tier['base_multiplier'] * 2 if is_double_points else current_tier['base_multiplier']
    
    earned_points = int((subtotal - discount) * points_multiplier)
    
    if is_double_points:
        st.sidebar.warning(f"🔥 **Double Points Day!** As a {current_tier['name']}, you earn {earned_points} pts!")
    else:
        st.sidebar.info(f"As a {current_tier['name']}, you will earn {earned_points} pts.")
        
    st.sidebar.divider()
    
    # --- TOTALS ---
    tax = (subtotal - discount) * 0.0825
    final_total = subtotal - discount + tax
    
    st.sidebar.write(f"**Subtotal:** ${subtotal:.2f}")
    if discount > 0:
        st.sidebar.write(f"**Discount:** -${discount:.2f}")
    st.sidebar.write(f"**Tax:** ${tax:.2f}")
    st.sidebar.subheader(f"Total: ${final_total:.2f}")
    
    st.sidebar.divider()
    st.sidebar.subheader("Payment Method")
    
    if st.sidebar.button(" Pay with Apple Pay", type="primary", use_container_width=True):
        st.sidebar.success("Processing Apple Pay...")
    if st.sidebar.button("Pay with Google Pay", use_container_width=True):
        st.sidebar.success("Processing Google Pay...")
        
    with st.sidebar.expander("💳 Credit / Debit Card"):
        with st.form("cc_form"):
            st.text_input("Card Number", placeholder="0000 0000 0000 0000", max_chars=19)
            col_exp, col_cvv = st.columns(2)
            col_exp.text_input("Exp Date", placeholder="MM/YY", max_chars=5)
            col_cvv.text_input("CVV", placeholder="123", max_chars=4)
            st.text_input("Zip Code", placeholder="65721", max_chars=5)
            
            submit_disabled = st.session_state.order_type == "Dine In" and not table_number
            
            if st.form_submit_button("Submit Order", type="primary", use_container_width=True, disabled=submit_disabled):
                # Update BOTH points banks
                st.session_state.user_points -= points_to_use
                st.session_state.user_points += earned_points
                st.session_state.lifetime_points += earned_points
                
                st.success(f"Order Placed! You earned {earned_points} points.")
                st.session_state.cart = []
                st.rerun()
              
