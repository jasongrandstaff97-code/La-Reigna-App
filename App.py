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
if 'points_to_use' not in st.session_state:
    st.session_state.points_to_use = 0

def add_to_cart(item):
    st.session_state.cart.append(item)
    st.toast(f"Added {item['name']} to cart!")

def remove_from_cart(index):
    st.session_state.cart.pop(index)

def get_user_tier(lifetime_pts):
    if lifetime_pts >= 2500:
        return {"name": "Habanero", "icon": "🔥", "css": "tier-habanero", "base_multiplier": 15, "next_tier_req": None}
    elif lifetime_pts >= 1000:
        return {"name": "Jalapeño", "icon": "🌶️", "css": "tier-jalapeno", "base_multiplier": 12, "next_tier_req": 2500}
    else:
        return {"name": "Poblano", "icon": "🫑", "css": "tier-poblano", "base_multiplier": 10, "next_tier_req": 1000}

# ==========================================
# 4. APP HEADER & GLOBAL VARIABLES
# ==========================================
st.title("La Reina Margaritas")
st.caption("📍 1511 W State Highway J, Ozark, MO 65721")

# Call to order button using the tel: protocol
st.link_button("📞 Call to Order: (417) 598-6327", "tel:+14175986327", use_container_width=True)

subtotal = sum(item['price'] for item in st.session_state.cart)
cart_count = len(st.session_state.cart)

# ==========================================
# 5. THE MAIN TAB NAVIGATION
# ==========================================
tab_menu, tab_rewards, tab_cart = st.tabs([f"🍔 Menu", "🎁 Rewards", f"🛒 Cart ({cart_count})"])

# ------------------------------------------
# TAB 1: MENU
# ------------------------------------------
with tab_menu:
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
        table_number = st.text_input("Enter Table Number:", placeholder="e.g., 12", max_chars=3)
    
    st.divider()

    categories = list(MENU.keys())
    selected_category = st.selectbox("Browse Menu", categories)
    st.subheader(selected_category)

    for item in MENU[selected_category]:
        with st.container():
            col_text, col_btn = st.columns([4, 1])
            with col_text:
                st.markdown(f"<div class='item-title'>{item['name']}</div>", unsafe_allow_html=True)
                if item['promo']:
                    st.markdown(f"<div class='promo-tag'>🏷️ {item['promo']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='item-desc'>{item['desc']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='item-price'>${item['price']:.2f}</div>", unsafe_allow_html=True)
            with col_btn:
                st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
                if st.button("➕ Add", key=f"add_{item['id']}", use_container_width=True):
                    add_to_cart(item)
                    st.rerun() 
            st.markdown("<hr style='margin: 10px 0; opacity: 0.2;'>", unsafe_allow_html=True)

# ------------------------------------------
# TAB 2: REWARDS & SCANNING
# ------------------------------------------
with tab_rewards:
    st.header("Your Rewards")
    current_tier = get_user_tier(st.session_state.lifetime_points)
    
    st.markdown(f"<div class='{current_tier['css']}'>{current_tier['icon']} {current_tier['name']} Status</div>", unsafe_allow_html=True)
    
    if current_tier['next_tier_req']:
        pts_needed = current_tier['next_tier_req'] - st.session_state.lifetime_points
        st.progress(st.session_state.lifetime_points / current_tier['next_tier_req'])
        st.caption(f"Only {pts_needed} pts until next tier!")
    else:
        st.caption("You have reached the maximum rewards tier!")

    with st.expander("ℹ️ How Rewards Work"):
        st.markdown("""
        **Every 100 points = $1 off your order.**
        Level up your pepper tier based on your lifetime points to earn faster!
        * 🫑 **Poblano (0 - 999 pts):** 10 pts per $1 spent.
        * 🌶️ **Jalapeño (1,000 - 2,499 pts):** 12 pts per $1 spent.
        * 🔥 **Habanero (2,500+ pts):** 15 pts per $1 spent.
        📅 **Double Points Days:** Dine with us on Wednesdays and Sundays for double points!
        """)

    st.divider()
    
    st.subheader("📸 Claim Missing Points")
    st.write("Ordered over the phone or forgot to scan? Upload your receipt below.")
    
    receipt_img = st.camera_input("Take a photo of your receipt")
    
    if receipt_img:
        with st.spinner("Analyzing receipt barcode and total..."):
            time.sleep(2)
            
        if 'receipt_scanned' not in st.session_state:
            st.success("Valid receipt found! Added 150 points to your account.")
            st.session_state.user_points += 150
            st.session_state.lifetime_points += 150
            st.session_state.receipt_scanned = True
            time.sleep(1.5)
            st.rerun()

    with st.expander("Receipt too blurry? Enter manually"):
        with st.form("manual_receipt"):
            receipt_code = st.text_input("12-Digit Receipt Code", max_chars=12, placeholder="e.g., 123456789012")
            if st.form_submit_button("Claim Points", use_container_width=True):
                if len(receipt_code) == 12:
                    st.success(f"Code verified! Points added.")
                else:
                    st.error("Please enter a valid 12-digit code.")

    st.divider()
    st.subheader("Redeem Points")
    st.write(f"**Spendable Balance:** {st.session_state.user_points} pts")
    
    if subtotal == 0:
        st.info("Add items to your cart to redeem points for a discount.")
        st.session_state.points_to_use = 0
    else:
        max_redeemable = min(st.session_state.user_points // 100, int(subtotal)) * 100
        if max_redeemable > 0:
            st.session_state.points_to_use = st.slider("Slide to apply discount ($1 off per 100 pts)", 0, max_redeemable, step=100)
            if st.session_state.points_to_use > 0:
                st.success(f"Applying ${st.session_state.points_to_use / 100:.2f} discount to your cart!")
        else:
            st.warning("Not enough points to apply a discount, or subtotal is too low.")

# ------------------------------------------
# TAB 3: CART & CHECKOUT
# ------------------------------------------
with tab_cart:
    st.header("Order Summary")
    
    if st.session_state.order_type == "Dine In":
        display_table = f" (Table {table_number})" if table_number else " (Pending Table #)"
        st.caption(f"**Order Type:** Dine In{display_table}")
    else:
        st.caption("**Order Type:** Carry Out")
        
    st.divider()

    if not st.session_state.cart:
        st.info("Your cart is empty. Head to the Menu tab to add items!")
    else:
        for i, item in enumerate(st.session_state.cart):
            col_name, col_price, col_del = st.columns([3, 1, 1])
            col_name.write(item['name'])
            col_price.write(f"${item['price']:.2f}")
            if col_del.button("❌", key=f"del_{i}"):
                remove_from_cart(i)
                st.rerun()
                
        st.divider()
        
        discount = st.session_state.points_to_use / 100
        tax = (subtotal - discount) * 0.0825
        final_total = subtotal - discount + tax
        
        today = datetime.now().weekday()
        is_double_points = today in [2, 6]
        points_multiplier = current_tier['base_multiplier'] * 2 if is_double_points else current_tier['base_multiplier']
        earned_points = int((subtotal - discount) * points_multiplier)
        
        if is_double_points:
            st.success(f"🔥 **Double Points Day!** You will earn **{earned_points} pts** on this order!")
        else:
            st.info(f"You will earn **{earned_points} pts** on this order.")
        
        st.write(f"**Subtotal:** ${subtotal:.2f}")
        if discount > 0:
            st.write(f"**Rewards Discount:** -${discount:.2f}")
        st.write(f"**Tax (8.25%):** ${tax:.2f}")
        st.subheader(f"Total: ${final_total:.2f}")
        
        st.divider()
        st.subheader("Payment")
        
        if st.button(" Pay with Apple Pay", type="primary", use_container_width=True):
            st.success("Processing Apple Pay...")
        if st.button("Pay with Google Pay", use_container_width=True):
            st.success("Processing Google Pay...")
            
        with st.expander("💳 Credit / Debit Card"):
            with st.form("cc_form"):
                st.text_input("Card Number", placeholder="0000 0000 0000 0000", max_chars=19)
                col_exp, col_cvv = st.columns(2)
                col_exp.text_input("Exp Date", placeholder="MM/YY", max_chars=5)
                col_cvv.text_input("CVV", placeholder="123", max_chars=4)
                st.text_input("Zip Code", placeholder="65721", max_chars=5)
                
                submit_disabled = False
                if st.session_state.order_type == "Dine In" and not table_number:
                    submit_disabled = True
                    st.error("⚠️ Please enter a Table Number on the Menu tab before checking out.")
                
                if st.form_submit_button("Submit Order", type="primary", use_container_width=True, disabled=submit_disabled):
                    
                    # Pure app logic for order completion
                    st.session_state.user_points -= st.session_state.points_to_use
                    st.session_state.user_points += earned_points
                    st.session_state.lifetime_points += earned_points
                    
                    st.session_state.cart = []
                    st.session_state.points_to_use = 0
                    
                    st.success(f"Order Placed Successfully! You earned {earned_points} points.")
                    st.rerun()
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
if 'points_to_use' not in st.session_state:
    st.session_state.points_to_use = 0

def add_to_cart(item):
    st.session_state.cart.append(item)
    st.toast(f"Added {item['name']} to cart!")

def remove_from_cart(index):
    st.session_state.cart.pop(index)

def get_user_tier(lifetime_pts):
    if lifetime_pts >= 2500:
        return {"name": "Habanero", "icon": "🔥", "css": "tier-habanero", "base_multiplier": 15, "next_tier_req": None}
    elif lifetime_pts >= 1000:
        return {"name": "Jalapeño", "icon": "🌶️", "css": "tier-jalapeno", "base_multiplier": 12, "next_tier_req": 2500}
    else:
        return {"name": "Poblano", "icon": "🫑", "css": "tier-poblano", "base_multiplier": 10, "next_tier_req": 1000}

# ==========================================
# 4. APP HEADER & GLOBAL VARIABLES
# ==========================================
st.title("La Reina Margaritas")
st.caption("📍 1511 W State Highway J, Ozark, MO 65721")

# Call to order button using the tel: protocol
st.link_button("📞 Call to Order: (417) 598-6327", "tel:+14175986327", use_container_width=True)

subtotal = sum(item['price'] for item in st.session_state.cart)
cart_count = len(st.session_state.cart)

# ==========================================
# 5. THE MAIN TAB NAVIGATION
# ==========================================
tab_menu, tab_rewards, tab_cart = st.tabs([f"🍔 Menu", "🎁 Rewards", f"🛒 Cart ({cart_count})"])

# ------------------------------------------
# TAB 1: MENU
# ------------------------------------------
with tab_menu:
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
        table_number = st.text_input("Enter Table Number:", placeholder="e.g., 12", max_chars=3)
    
    st.divider()

    categories = list(MENU.keys())
    selected_category = st.selectbox("Browse Menu", categories)
    st.subheader(selected_category)

    for item in MENU[selected_category]:
        with st.container():
            col_text, col_btn = st.columns([4, 1])
            with col_text:
                st.markdown(f"<div class='item-title'>{item['name']}</div>", unsafe_allow_html=True)
                if item['promo']:
                    st.markdown(f"<div class='promo-tag'>🏷️ {item['promo']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='item-desc'>{item['desc']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='item-price'>${item['price']:.2f}</div>", unsafe_allow_html=True)
            with col_btn:
                st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
                if st.button("➕ Add", key=f"add_{item['id']}", use_container_width=True):
                    add_to_cart(item)
                    st.rerun() 
            st.markdown("<hr style='margin: 10px 0; opacity: 0.2;'>", unsafe_allow_html=True)

# ------------------------------------------
# TAB 2: REWARDS & SCANNING
# ------------------------------------------
with tab_rewards:
    st.header("Your Rewards")
    current_tier = get_user_tier(st.session_state.lifetime_points)
    
    st.markdown(f"<div class='{current_tier['css']}'>{current_tier['icon']} {current_tier['name']} Status</div>", unsafe_allow_html=True)
    
    if current_tier['next_tier_req']:
        pts_needed = current_tier['next_tier_req'] - st.session_state.lifetime_points
        st.progress(st.session_state.lifetime_points / current_tier['next_tier_req'])
        st.caption(f"Only {pts_needed} pts until next tier!")
    else:
        st.caption("You have reached the maximum rewards tier!")

    with st.expander("ℹ️ How Rewards Work"):
        st.markdown("""
        **Every 100 points = $1 off your order.**
        Level up your pepper tier based on your lifetime points to earn faster!
        * 🫑 **Poblano (0 - 999 pts):** 10 pts per $1 spent.
        * 🌶️ **Jalapeño (1,000 - 2,499 pts):** 12 pts per $1 spent.
        * 🔥 **Habanero (2,500+ pts):** 15 pts per $1 spent.
        📅 **Double Points Days:** Dine with us on Wednesdays and Sundays for double points!
        """)

    st.divider()
    
    st.subheader("📸 Claim Missing Points")
    st.write("Ordered over the phone or forgot to scan? Upload your receipt below.")
    
    receipt_img = st.camera_input("Take a photo of your receipt")
    
    if receipt_img:
        with st.spinner("Analyzing receipt barcode and total..."):
            time.sleep(2)
            
        if 'receipt_scanned' not in st.session_state:
            st.success("Valid receipt found! Added 150 points to your account.")
            st.session_state.user_points += 150
            st.session_state.lifetime_points += 150
            st.session_state.receipt_scanned = True
            time.sleep(1.5)
            st.rerun()

    with st.expander("Receipt too blurry? Enter manually"):
        with st.form("manual_receipt"):
            receipt_code = st.text_input("12-Digit Receipt Code", max_chars=12, placeholder="e.g., 123456789012")
            if st.form_submit_button("Claim Points", use_container_width=True):
                if len(receipt_code) == 12:
                    st.success(f"Code verified! Points added.")
                else:
                    st.error("Please enter a valid 12-digit code.")

    st.divider()
    st.subheader("Redeem Points")
    st.write(f"**Spendable Balance:** {st.session_state.user_points} pts")
    
    if subtotal == 0:
        st.info("Add items to your cart to redeem points for a discount.")
        st.session_state.points_to_use = 0
    else:
        max_redeemable = min(st.session_state.user_points // 100, int(subtotal)) * 100
        if max_redeemable > 0:
            st.session_state.points_to_use = st.slider("Slide to apply discount ($1 off per 100 pts)", 0, max_redeemable, step=100)
            if st.session_state.points_to_use > 0:
                st.success(f"Applying ${st.session_state.points_to_use / 100:.2f} discount to your cart!")
        else:
            st.warning("Not enough points to apply a discount, or subtotal is too low.")

# ------------------------------------------
# TAB 3: CART & CHECKOUT
# ------------------------------------------
with tab_cart:
    st.header("Order Summary")
    
    if st.session_state.order_type == "Dine In":
        display_table = f" (Table {table_number})" if table_number else " (Pending Table #)"
        st.caption(f"**Order Type:** Dine In{display_table}")
    else:
        st.caption("**Order Type:** Carry Out")
        
    st.divider()

    if not st.session_state.cart:
        st.info("Your cart is empty. Head to the Menu tab to add items!")
    else:
        for i, item in enumerate(st.session_state.cart):
            col_name, col_price, col_del = st.columns([3, 1, 1])
            col_name.write(item['name'])
            col_price.write(f"${item['price']:.2f}")
            if col_del.button("❌", key=f"del_{i}"):
                remove_from_cart(i)
                st.rerun()
                
        st.divider()
        
        discount = st.session_state.points_to_use / 100
        tax = (subtotal - discount) * 0.0825
        final_total = subtotal - discount + tax
        
        today = datetime.now().weekday()
        is_double_points = today in [2, 6]
        points_multiplier = current_tier['base_multiplier'] * 2 if is_double_points else current_tier['base_multiplier']
        earned_points = int((subtotal - discount) * points_multiplier)
        
        if is_double_points:
            st.success(f"🔥 **Double Points Day!** You will earn **{earned_points} pts** on this order!")
        else:
            st.info(f"You will earn **{earned_points} pts** on this order.")
        
        st.write(f"**Subtotal:** ${subtotal:.2f}")
        if discount > 0:
            st.write(f"**Rewards Discount:** -${discount:.2f}")
        st.write(f"**Tax (8.25%):** ${tax:.2f}")
        st.subheader(f"Total: ${final_total:.2f}")
        
        st.divider()
        st.subheader("Payment")
        
        if st.button(" Pay with Apple Pay", type="primary", use_container_width=True):
            st.success("Processing Apple Pay...")
        if st.button("Pay with Google Pay", use_container_width=True):
            st.success("Processing Google Pay...")
            
        with st.expander("💳 Credit / Debit Card"):
            with st.form("cc_form"):
                st.text_input("Card Number", placeholder="0000 0000 0000 0000", max_chars=19)
                col_exp, col_cvv = st.columns(2)
                col_exp.text_input("Exp Date", placeholder="MM/YY", max_chars=5)
                col_cvv.text_input("CVV", placeholder="123", max_chars=4)
                st.text_input("Zip Code", placeholder="65721", max_chars=5)
                
                submit_disabled = False
                if st.session_state.order_type == "Dine In" and not table_number:
                    submit_disabled = True
                    st.error("⚠️ Please enter a Table Number on the Menu tab before checking out.")
                
                if st.form_submit_button("Submit Order", type="primary", use_container_width=True, disabled=submit_disabled):
                    
                    # Pure app logic for order completion
                    st.session_state.user_points -= st.session_state.points_to_use
                    st.session_state.user_points += earned_points
                    st.session_state.lifetime_points += earned_points
                    
                    st.session_state.cart = []
                    st.session_state.points_to_use = 0
                    
                    st.success(f"Order Placed Successfully! You earned {earned_points} points.")
                    st.rerun()
    
