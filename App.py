import streamlit as st
import random 

# 1. PAGE CONFIG & BRANDING
st.set_page_config(page_title="La Reina Margaritas", page_icon="👑", layout="centered")

# 2. CUSTOM CSS: La Reina's Sage Green & Gold
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #556B2F; 
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: bold;
        padding: 10px 24px;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #435425; 
        color: #F8E231; 
    }
    h1, h2, h3 { 
        color: #556B2F; 
        font-family: 'Georgia', serif; 
    }
    </style>
""", unsafe_allow_html=True)

# 3. STATE MANAGEMENT
if "cart" not in st.session_state:
    st.session_state.cart = []
if "show_camera" not in st.session_state:
    st.session_state.show_camera = False

# 4. FULL MENU DATABASE
menu_data = {
    "Lunch Specials (11am-3pm)": [
        {"name": "Lunch Fajitas", "price": 13.75, "desc": "Sizzling Steak or Chicken, grilled onions & peppers. With rice, beans & tortillas."},
        {"name": "Fajita Chimichanga", "price": 12.75, "desc": "Steak & Chicken deep-fried burrito smothered in queso sauce. With rice & beans."},
        {"name": "Sopes (3)", "price": 13.75, "desc": "Three traditional sopes with your choice of toppings."},
        {"name": "Rey Nachos", "price": 14.00, "desc": "Loaded nachos topped with tender Birria meat."},
        {"name": "Specialty Burritos", "price": 11.75, "desc": "Choice of protein, shredded chicken, veggies, smothered in queso."},
        {"name": "Ribeye Tacos", "price": 16.99, "desc": "Two tacos, salsa cruda, street corn & rice."},
        {"name": "El Rey Bowl", "price": 12.75, "desc": "Choice of Shrimp, Asada, Chicken Fajita, Ground Beef, Tinga, or Veggies."},
        {"name": "Burrito Style Enchilada", "price": 13.00, "desc": "Ground beef with special sauces."},
        {"name": "El Real Molcajete", "price": 16.75, "desc": "Sizzling molcajete, choice of protein."},
        {"name": "Enchiladas de Espinaca", "price": 13.25, "desc": "Spinach enchiladas served w/ rice & beans (Vegetarian)."}
    ],
    "Antojitos & Botanas": [
        {"name": "Famoso Queso Casero", "price": 8.00, "desc": "Our delicious house-made queso with a hint of spice."},
        {"name": "Tamale de Elote Trufado", "price": 7.00, "desc": "Sweet corn tamale, queso fresco, truffle oil."},
        {"name": "Esquites de la Casa", "price": 8.00, "desc": "Charred corn kernels, epazote aioli, chile ash, lime dust, queso fresco."},
        {"name": "Stuffed Avocados", "price": 14.00, "desc": "Two fresh avocados filled with cheese, jalapeño, and chorizo. Lightly battered and deep-fried."},
        {"name": "Chilaquiles de la Casa", "price": 12.00, "desc": "Baked chips covered in our house-made mole, garnished with sour cream drizzle."},
        {"name": "Table Side Cart Special", "price": 17.00, "desc": "Appetizer trio made table side. Our famous queso flameado, fresh guacamole, and roasted salsa."}
    ],
    "Taqueria / Tacos": [
        {"name": "Street Tacos", "price": 14.75, "desc": "Three asada or grilled chicken tacos, garnished with onions, cilantro, and salsa verde."},
        {"name": "Tex-Mex", "price": 13.00, "desc": "Three crispy tacos with ground beef, lettuce, tomato, sour cream, guacamole drizzle, and queso fresco."},
        {"name": "Carnita Tacos", "price": 14.00, "desc": "Three slow-cooked pork tacos, lightly fried for extra flavor."},
        {"name": "Quesabirria", "price": 16.00, "desc": "Three corn tortillas filled with tender, slow-roasted beef, and melted cheese. Served with savory consommé."},
        {"name": "Tacos de Pescado", "price": 15.75, "desc": "Three grilled tilapia, cabbage, pickled onion, pico de gallo, and creamy chipotle sauce."},
        {"name": "Keto Taco", "price": 14.00, "desc": "Three cheese tortillas, pastor, onion, cilantro, and salsa verde."}
    ],
    "Platos Fuertes / Entrees": [
        {"name": "Tamale Plate", "price": 14.00, "desc": "Two tamales, choice of pork or chicken, topped with chile con carne and melted cheese."},
        {"name": "Rey Birria Nachos", "price": 16.00, "desc": "Crispy nachos topped with birria, house-made queso, signature corona sauce, and guacamole."},
        {"name": "Reina Style Enchiladas", "price": 16.00, "desc": "Three Texas-style enchiladas, filled with shredded chicken, topped with melted cheese and sour cream sauce."},
        {"name": "Ribeye Tacos (Dinner)", "price": 24.00, "desc": "Three ribeye tacos, garnished with cilantro, onion, salsa cruda. Served with street corn and Mexican rice."},
        {"name": "Mole Poblano", "price": 16.75, "desc": "Slow-cooked chicken smothered in a rich mole sauce made with roasted chiles, chocolate, nuts, and aromatic spices."},
        {"name": "Barbacoa Plate", "price": 16.00, "desc": "Slow-cooked shredded beef, simmered in our traditional spices. Served with salsa verde, rice, beans, and tortillas."}
    ],
    "Sizzling Platters & Seafood": [
        {"name": "El Real Molcajete", "price": 19.00, "desc": "Sizzling molcajete with your choice of protein over a smoking medley of pepper and onion."},
        {"name": "Sizzling Fajitas", "price": 18.75, "desc": "Tender chicken or steak fajitas, marinated and grilled over an open flame."},
        {"name": "Parrillada Nortena (For 2)", "price": 39.00, "desc": "Mixed grill: Beef Skirt Steak, Chicken a la Plancha, House Chorizo, Salchicha, Chiles Toreados. Served with tortillas and sides."},
        {"name": "Caldo de Mariscos", "price": 18.75, "desc": "Traditional Mexican seafood soup prepared with shrimp, fish, and crab simmered in a rich tomato and chile broth."},
        {"name": "Camarones a la Diabla", "price": 16.00, "desc": "Succulent shrimp simmered in a bold blend of dried chiles, garlic, and spices."}
    ],
    "Vegetarian": [
        {"name": "La Reina Special", "price": 13.75, "desc": "Roasted veggies on a bed of white rice and topped with cheese sauce and our signature Corona sauce."},
        {"name": "Roasted Chile Rellenos", "price": 15.75, "desc": "Poblano pepper filled with squash, mushrooms, red bell pepper, and queso fresco. Topped with roasted red salsa."},
        {"name": "Veggie Fajitas", "price": 16.00, "desc": "Grilled seasonal veggies, served in a sizzling skillet with lettuce, pico, shredded cheddar cheese, sour cream, and guacamole."}
    ],
    "Drinks & Desserts": [
        {"name": "Aguas Frescas (32 oz)", "price": 7.50, "desc": "Horchata, Jamaica, Sandia, Tamarindo, Strawberry, or Pineapple."},
        {"name": "House Margarita (Happy Hour)", "price": 6.75, "desc": "Classic house-made margarita."},
        {"name": "Churros de la Casa", "price": 6.00, "desc": "Traditional warm churros."},
        {"name": "Tres Leches", "price": 7.00, "desc": "Classic Mexican three-milk cake."},
        {"name": "Dulce Banana Mousse", "price": 10.00, "desc": "Rich, sweet banana mousse dessert."}
    ]
}
# 5. HEADER & LOGO
try:
    st.image("logo.png", use_container_width=True) 
except:
    st.markdown("<h1 style='text-align: center;'>👑 La Reina Margaritas</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>AUTHENTIC MEXICAN KITCHEN & CANTINA</p>", unsafe_allow_html=True)

# 6. MAIN TABS SETUP
tab1, tab2, tab3 = st.tabs(["🍽️ Menu", "🎁 Rewards", f"🛒 Cart ({len(st.session_state.cart)})"])

# --- TAB 1: MENU UI ---
with tab1:
    st.markdown("### Browse Menu")
    
    category_list = list(menu_data.keys())
    selected_category = st.pills("Select Category", category_list, default="Lunch Specials (11am-3pm)")
    
    st.divider()

    if selected_category:
        for item in menu_data[selected_category]:
            col1, col2 = st.columns([3, 1], vertical_alignment="center")
            
            with col1:
                st.markdown(f"**{item['name']}**")
                st.caption(item['desc'])
                st.markdown(f"**${item['price']:.2f}**")
            
            with col2:
                if st.button("➕ Add", key=item['name']):
                    st.session_state.cart.append(item)
                    st.toast(f"Added {item['name']} to your cart! 🌮", icon="✅")
            st.divider()
            # --- TAB 2: REWARDS UI ---
with tab2:
    st.header("Poblano Status 🌶️")
    st.progress(0.5, text="500 pts until next tier (Habanero!)")
    
    st.markdown("### Claim Missing Points")
    st.info("Ordered over the phone? Upload your receipt below.")
    
    if st.button("📸 Tap to Scan Receipt"):
        st.session_state.show_camera = True
        
    if st.session_state.show_camera:
        picture = st.camera_input("Line up your receipt here")
        if picture:
            st.success("Receipt scanned successfully! Points will be added shortly.")
            st.toast("50 Points Added!", icon="🔥")
            st.session_state.show_camera = False

# --- TAB 3: CART & CHECKOUT UI ---
with tab3:
    st.header("Your Order")
    if len(st.session_state.cart) == 0:
        st.warning("Your cart is empty. Head to the Menu tab to add items!")
    else:
        total = 0
        for item in st.session_state.cart:
            st.markdown(f"- {item['name']} : **${item['price']:.2f}**")
            total += item['price']
            
        st.divider()
        st.subheader(f"Total: ${total:.2f}")
        
        st.markdown("### How would you like to pay?")
        
        colA, colB = st.columns(2)
        with colA:
            if st.button("🏪 Pay at Pickup"):
                order_num = random.randint(1000, 9999)
                st.success(f"🎉 Order #{order_num} confirmed! We will have it ready for you. You can pay however you prefer upon arrival.")
                st.session_state.cart = []
                st.rerun() 
                
        with colB:
            if st.button("💳 Pay Now in App"):
                st.info("Redirecting to secure card payment...")
                
