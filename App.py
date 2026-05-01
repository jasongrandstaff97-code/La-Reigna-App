import streamlit as st
from datetime import datetime
import time

# ==========================================
# 1. PAGE CONFIGURATION & CUSTOM CSS
# ==========================================
st.set_page_config(page_title="La Reina Margaritas", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .item-card { border: 1px solid #e6e6e6; border-radius: 10px; padding: 15px; margin-bottom: 15px; background-color: white; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    .item-title { font-size: 18px; font-weight: bold; margin-bottom: 5px; color: #111; }
    .item-desc { font-size: 14px; color: #666; margin-bottom: 10px; line-height: 1.4; }
    .item-price { font-size: 16px; font-weight: bold; color: #333; }
    .promo-tag { color: #d92128; font-size: 12px; font-weight: bold; margin-bottom: 5px; display: inline-block; }
    .tier-poblano { color: #2e7d32; font-weight: bold; font-size: 18px; }
    .tier-jalapeno { color: #f57f17; font-weight: bold; font-size: 18px; }
    .tier-habanero { color: #c62828; font-weight: bold; font-size: 18px; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
    .stTabs [data-baseweb="tab"] { height: 50px; font-size: 16px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. FULL MENU DATABASE
# ==========================================
MENU = {
    "Most Ordered": [
        {"id": 1, "name": "Street Corn", "price": 5.75, "desc": "2 for $5.75.", "promo": "Buy 1, get 1 free", "img": None},
        {"id": 2, "name": "Tamale de Elote Trufado", "price": 7.00, "desc": "Sweet corn tamale, queso fresco, truffle oil.", "promo": "Buy 1, get 1 free", "img": None},
        {"id": 3, "name": "Famoso Queso Casero", "price": 8.00, "desc": "Our delicious house-made queso, made with a hint of spice.", "promo": None, "img": None},
        {"id": 4, "name": "Street Tacos Asada", "price": 14.75, "desc": "Three asada or grilled chicken tacos, garnished.", "promo": None, "img": None},
        {"id": 5, "name": "Carnita Tacos", "price": 14.00, "desc": "Three slow-cooked pork tacos, lightly fried.", "promo": None, "img": None},
        {"id": 6, "name": "Mexican Enchiladas", "price": 14.75, "desc": "Three enchiladas - one cheese, one shredded chicken, one ground beef.", "promo": None, "img": None},
        {"id": 7, "name": "Reina Style Enchiladas", "price": 16.00, "desc": "Texas-style enchiladas, filled with shredded chicken, topped with melted cheese.", "promo": None, "img": None},
        {"id": 8, "name": "Jamaica", "price": 8.50, "desc": "Refreshing Hibiscus Tea, a Classic Caribbean Beverage.", "promo": "Buy 1, get 1 free", "img": None},
        {"id": 9, "name": "Esquites De La Casa", "price": 8.00, "desc": "Charred corn kernels, epazote aioli, chile ash, lime dust.", "promo": "Buy 1, get 1 free", "img": None},
        {"id": 10, "name": "Sopa De Tortilla", "price": 12.00, "desc": "Chipotle chicken broth with shredded chicken, topped with crispy tortilla chips.", "promo": "Buy 1, get 1 free", "img": None}
    ],
    "Antojitos & Botanas": [
        {"id": 11, "name": "Stuffed Avocados", "price": 13.00, "desc": "Two fresh avocados filled with cheese, jalapeño, and chorizo. Deep-fried.", "promo": None, "img": None},
        {"id": 12, "name": "Top Shelf Guacamole", "price": 9.00, "desc": "Fresh flavor avocado dip, lime juice, garlic, onion.", "promo": None, "img": None},
        {"id": 13, "name": "Tres Cheese Tostadas", "price": 9.00, "desc": "Three crisp corn tortillas layered with refried beans, a blend of three melted cheeses.", "promo": None, "img": None},
        {"id": 14, "name": "Esquites De La Casa", "price": 8.00, "desc": "Charred corn kernels, epazote aioli, chile ash, lime dust.", "promo": None, "img": None},
        {"id": 15, "name": "Tamale de Elote Trufado", "price": 14.00, "desc": "Sweet corn tamale, queso fresco, truffle oil.", "promo": "Buy 1, get 1 free (2 for $7.00)", "img": None},
        {"id": 16, "name": "Empanadas", "price": 9.00, "desc": "Two golden, flaky pastries filled with tender, slow-cooked shredded beef.", "promo": None, "img": None},
        {"id": 17, "name": "Fried Calamari", "price": 14.00, "desc": "Lightly breaded calamari rings, fried until golden.", "promo": "Buy 1, get 1 free", "img": None},
        {"id": 18, "name": "Chilaquiles De La Casa", "price": 12.00, "desc": "Baked chips covered in our house-made mole, garnished with sour cream.", "promo": None, "img": None},
        {"id": 19, "name": "Empanadas De Flor De Calabaza", "price": 14.00, "desc": "Two empanadas filled with queso and flor de calabaza.", "promo": "Buy 1, get 1 free", "img": None},
        {"id": 20, "name": "Flautas", "price": 10.00, "desc": "Three rolled, deep-fried taquitos filled with shredded chicken.", "promo": None, "img": None},
        {"id": 21, "name": "Agua Chile De Camarón", "price": 14.00, "desc": "Jumbo butterfly cut shrimp, cooked and marinated.", "promo": None, "img": None}
    ],
    "Ensaladas y Sopas": [
        {"id": 22, "name": "Blackened Chicken Taco Salad", "price": 14.00, "desc": "Crisp lettuce, topped with blackened chicken, fire-roasted corn, black beans.", "promo": "Buy 1, get 1 free", "img": None},
        {"id": 23, "name": "El Rey Bowl", "price": 15.00, "desc": "Sautéed shrimp, mixed greens, cucumber, corn, avocado.", "promo": "Buy 1, get 1 free", "img": None},
        {"id": 24, "name": "Sopa De Tortilla", "price": 12.00, "desc": "Chipotle chicken broth with shredded chicken.", "promo": None, "img": None},
        {"id": 25, "name": "Ensalada Royal", "price": 10.00, "desc": "Spring mix, grape tomato, jicama, goat cheese, raspberry vinaigrette.", "promo": "Buy 1, get 1 free", "img": None}
    ],
    "Platos Fuertes / Main": [
        {"id": 26, "name": "Reina Style Enchiladas", "price": 16.00, "desc": "Texas-style enchiladas, filled with shredded chicken.", "promo": None, "img": None},
        {"id": 27, "name": "Mexican Enchiladas", "price": 14.75, "desc": "Three enchiladas - one cheese, one shredded chicken, one ground beef.", "promo": None, "img": None},
        {"id": 28, "name": "Salsa Verde Carnitas", "price": 16.00, "desc": "Tender pork chunks cooked in a special house-made green sauce.", "promo": None, "img": None},
        {"id": 29, "name": "Chile Relleno", "price": 14.75, "desc": "Roasted poblano pepper stuffed with cheese or seasoned meat.", "promo": None, "img": None},
        {"id": 30, "name": "Rey Birria Nachos", "price": 18.00, "desc": "Grande birria nachos topped with our special queso sauce.", "promo": "Buy 1, get 1 free", "img": None},
        {"id": 31, "name": "Tampiquena Real", "price": 23.75, "desc": "Tender 10 oz beef skirt cooked to perfection.", "promo": None, "img": None},
        {"id": 32, "name": "Birria Torta", "price": 16.00, "desc": "A hearty sandwich made with tender, slow-cooked birria beef.", "promo": None, "img": None},
        {"id": 33, "name": "Pollo Pibil", "price": 16.00, "desc": "Citrus and achiote marinated chicken, slow-cooked in banana leaves.", "promo": None, "img": None},
        {"id": 34, "name": "Mole Poblano", "price": 16.75, "desc": "Slow-cooked chicken smothered in a rich mole sauce.", "promo": "Buy 1, get 1 free", "img": None},
        {"id": 35, "name": "Barbacoa Plate", "price": 16.00, "desc": "Slow-cooked shredded beef, simmered in our traditional spices.", "promo": None, "img": None},
        {"id": 36, "name": "Burrito Mexicano", "price": 16.00, "desc": "Large tortilla filled with chicken fajita, sautéed onion, red bell pepper.", "promo": "Buy 1, get 1 free", "img": None},
        {"id": 37, "name": "Ribeye Tacos", "price": 24.00, "desc": "Three ribeye tacos, garnished with cilantro, onion, fire-roasted salsa.", "promo": None, "img": None},
        {"id": 38, "name": "Milanesa Empanizada", "price": 16.00, "desc": "Crispy, golden breaded chicken or beef cutlet.", "promo": None, "img": None},
        {"id": 39, "name": "Puffy Tacos", "price": 15.00, "desc": "Three deep-fried tortilla shells filled with beans, birria.", "promo": "Buy 1, get 1 free", "img": None},
        {"id": 40, "name": "Tamale Plate", "price": 14.00, "desc": "Two tamales, choice of pork or chicken.", "promo": None, "img": None}
    ],
    "À La Parrilla": [
        {"id": 41, "name": "Sizzling Fajitas", "price": 18.75, "desc": "Tender chicken or steak fajitas, marinated and grilled.", "promo": None, "img": None},
        {"id": 42, "name": "Pollo A La Plancha", "price": 16.75, "desc": "Tender, marinated chicken grilled on a plancha.", "promo": None, "img": None},
        {"id": 43, "name": "Fajita Alambre", "price": 17.75, "desc": "Grilled beef or chicken with sautéed onions, bell peppers, crispy bacon.", "promo": None, "img": None},
        {"id": 44, "name": "El Real Molcajete", "price": 19.00, "desc": "Sizzling molcajete with your choice of protein.", "promo": "Buy 1, get 1 free", "img": None}
    ],
    "Parrillada Nortena": [
        {"id": 45, "name": "Recommended For 2 People", "price": 39.00, "desc": "Beef skirt steak, chicken a la plancha, house chorizo, salchicha.", "promo": None, "img": None},
        {"id": 46, "name": "Recommended For 4 People", "price": 59.00, "desc": "Beef skirt steak, chicken a la plancha, house chorizo, salchicha.", "promo": None, "img": None}
    ],
    "Taqueria": [
        {"id": 47, "name": "Carnita Tacos", "price": 14.00, "desc": "Three slow-cooked pork tacos, lightly fried.", "promo": "Buy 1, get 1 free", "img": None},
        {"id": 48, "name": "Tacos Al Pastor", "price": 14.00, "desc": "Three marinated pork, cooked in aromatic spices.", "promo": None, "img": None},
        {"id": 49, "name": "Quesabirria", "price": 16.00, "desc": "Three corn tortillas filled with tender, slow-roasted beef.", "promo": None, "img": None},
        {"id": 50, "name": "Tacos De Pescado", "price": 15.75, "desc": "Three grilled tilapia, cabbage, pickled onion.", "promo": None, "img": None},
        {"id": 51, "name": "Keto Taco", "price": 14.00, "desc": "Three cheese tortillas, pastor, onion, cilantro.", "promo": "Buy 1, get 1 free", "img": None},
        {"id": 52, "name": "Lettuce-wrapped", "price": 12.75, "desc": "Three ground beef, lettuce, tomato, and shredded cheddar.", "promo": None, "img": None},
        {"id": 53, "name": "Tacos Vegetables", "price": 14.00, "desc": "Vegetarian. Three roasted vegetables, pico de gallo.", "promo": None, "img": None},
        {"id": 54, "name": "Tex-mex", "price": 13.00, "desc": "Three crispy tacos with crispy ground beef, lettuce.", "promo": None, "img": None},
        {"id": 55, "name": "Street Tacos Asada", "price": 14.75, "desc": "Three asada or grilled chicken tacos.", "promo": None, "img": None}
    ],
    "Platos Vegetarianos": [
        {"id": 56, "name": "Enchiladas De Espinaca", "price": 14.00, "desc": "Three rolled tortillas filled with sautéed spinach.", "promo": "Buy 1, get 1 free", "img": None},
        {"id": 57, "name": "Tacos De Nopal Asado", "price": 14.00, "desc": "Three grilled cactus tacos, marinated in a special house-made sauce.", "promo": None, "img": None},
        {"id": 58, "name": "Tacos Dorados De Papa", "price": 14.00, "desc": "Three crispy corn tortillas fried until golden, filled with seasoned potatoes.", "promo": None, "img": None},
        {"id": 59, "name": "Roasted Chile Rellenos", "price": 15.75, "desc": "Poblano pepper filled with squash, mushrooms, red bell pepper.", "promo": "Buy 1, get 1 free", "img": None},
        {"id": 60, "name": "Veggie Fajitas", "price": 16.00, "desc": "Grilled mixed-season veggies. Served in a sizzling skillet.", "promo": None, "img": None},
        {"id": 61, "name": "Vegetables Al Vapor", "price": 14.00, "desc": "Oven-cooked mixed veggies. Served with white rice.", "promo": "Buy 1, get 1 free", "img": None},
        {"id": 62, "name": "La Reina Special", "price": 13.75, "desc": "Roasted veggies on a bed of white rice topped with cheese sauce.", "promo": None, "img": None}
    ],
    "Acompanamientos / Sides": [
        {"id": 63, "name": "Roasted Potatoes", "price": 5.00, "desc": "Perfectly roasted potatoes, seasoned with rosemary.", "promo": "Buy 1, get 1 free", "img": None},
        {"id": 64, "name": "House Rice", "price": 3.00, "desc": "Seasoned rice typically includes minced garlic, onions.", "promo": None, "img": None},
        {"id": 65, "name": "Roasted Carrot", "price": 4.75, "desc": "Roasted carrots with a hint of Mexican spices.", "promo": None, "img": None},
        {"id": 66, "name": "Borracho Beans", "price": 4.00, "desc": "Slow-cooked pinto beans prepared with bacon.", "promo": None, "img": None},
        {"id": 67, "name": "Vegetarian Black Beans", "price": 3.00, "desc": "Vegetarian black beans.", "promo": None, "img": None},
        {"id": 68, "name": "Refried Beans", "price": 3.00, "desc": "Creamy, mashed beans, lightly seasoned.", "promo": None, "img": None},
        {"id": 69, "name": "House Salad", "price": 4.75, "desc": "Fresh mix of greens, with an assortment of vegetables.", "promo": None, "img": None},
        {"id": 70, "name": "Roasted Broccoli", "price": 4.75, "desc": "Roasted broccoli includes olive oil, garlic.", "promo": None, "img": None},
        {"id": 71, "name": "French Fries", "price": 4.00, "desc": "Crispy golden strips of deliciousness.", "promo": None, "img": None},
        {"id": 72, "name": "Street Corn", "price": 5.75, "desc": "2 for $5.75.", "promo": "Buy 1, get 1 free", "img": None},
        {"id": 73, "name": "White Vegetarian Rice", "price": 3.00, "desc": "Vegetarian white rice.", "promo": None, "img": None}
    ],
    "Desserts": [
        {"id": 74, "name": "Flan", "price": 7.00, "desc": "Smooth, caramel-topped custard.", "promo": "Buy 1, get 1 free", "img": None},
        {"id": 75, "name": "Chocolate Dubai Cake", "price": 8.99, "desc": "Typically includes a combination of traditional Mexican desserts.", "promo": None, "img": None},
        {"id": 76, "name": "Tres Leches", "price": 7.00, "desc": "Velvety three-milk cake, soaked and sweetened.", "promo": None, "img": None},
        {"id": 77, "name": "Churros De La Casa (2)", "price": 6.00, "desc": "Two fried churros typically rolled in cinnamon and sugar.", "promo": None, "img": None}
    ],
    "Kids' Meals": [
        {"id": 78, "name": "Chicken Tenders", "price": 8.00, "desc": "Three chicken tenders, fried until golden.", "promo": "Buy 1, get 1 free", "img": None},
        {"id": 79, "name": "Bean & Cheese Burrito", "price": 7.00, "desc": "Burrito filled with beans and cheese, topped with cheese sauce.", "promo": None, "img": None},
        {"id": 80, "name": "Mini Bean & Cheese Chimi", "price": 7.00, "desc": "Chimichanga filled with beans and cheese.", "promo": None, "img": None},
        {"id": 81, "name": "Kids' Strawberry Smoothie", "price": 3.99, "desc": "Creamy smoothie with strawberry.", "promo": "Buy 1, get 1 free", "img": None},
        {"id": 82, "name": "Kids Pina Colada Smoothie", "price": 3.99, "desc": "Pineapple, coconut cream, and typically includes banana.", "promo": None, "img": None},
        {"id": 83, "name": "Cheese Enchilada", "price": 7.00, "desc": "Rolled soft corn tortilla filled with cheese.", "promo": "Buy 1, get 1 free", "img": None},
        {"id": 84, "name": "Taco Plate", "price": 6.00, "desc": "Crispy ground beef topped with lettuce, tomato.", "promo": None, "img": None},
        {"id": 85, "name": "Quesadilla Plate", "price": 7.00, "desc": "Melted cheese quesadilla.", "promo": None, "img": None}
    ],
    "Non-Alcoholic Beverages": [
        {"id": 86, "name": "Mexican Coca-cola", "price": 4.00, "desc": "The same great taste made with only pure cane sugar.", "promo": "Buy 1, get 1 free", "img": None},
        {"id": 87, "name": "House-made Punch", "price": 5.00, "desc": "A blend of assorted fresh fruits.", "promo": None, "img": None},
        {"id": 88, "name": "Lemonade / Tropicana Lemonade", "price": 3.25, "desc": "Refreshing citrus drink.", "promo": "Buy 1, get 1 free", "img": None},
        {"id": 89, "name": "Flavored Lemonade", "price": 3.95, "desc": "Freshly squeezed lemon juice combined with sweetened water.", "promo": None, "img": None},
        {"id": 90, "name": "Tea / Coffee / Sparkling Water", "price": 3.00, "desc": "Choice of tea, coffee, or sparkling water.", "promo": "Buy 1, get 1 free", "img": None},
        {"id": 91, "name": "Flavored Tea", "price": 3.95, "desc": "Flavored tea typically includes a blend of black or green tea.", "promo": None, "img": None},
        {"id": 92, "name": "Jarritos (Punch)", "price": 4.99, "desc": "A Mexican soda with a fruity punch flavor.", "promo": "Buy 1, get 1 free", "img": None},
        {"id": 93, "name": "Jarritos (Lime)", "price": 4.99, "desc": "Lime-flavored Mexican soda.", "promo": None, "img": None},
        {"id": 94, "name": "Jarritos (Pineapple)", "price": 4.99, "desc": "Pineapple-flavored soda.", "promo": None, "img": None},
        {"id": 95, "name": "Jarritos (Mandarin)", "price": 4.99, "desc": "Mexican mandarin-flavored soda.", "promo": None, "img": None},
        {"id": 96, "name": "Pepsi / Pepsi Zero / Orange Crush", "price": 3.25, "desc": "Choice of popular sodas.", "promo": None, "img": None}
    ],
    "Aguas Frescas (32 Oz)": [
        {"id": 97, "name": "Jamaica", "price": 8.50, "desc": "Refreshing Hibiscus Tea, a Classic Caribbean Beverage.", "promo": "Buy 1, get 1 free", "img": None},
        {"id": 98, "name": "Sandia", "price": 8.50, "desc": "Refreshing watermelon drink.", "promo": None, "img": None},
        {"id": 99, "name": "Strawberry", "price": 8.50, "desc": "Fresh strawberry water.", "promo": None, "img": None},
        {"id": 100, "name": "Pineapple", "price": 8.50, "desc": "Fresh pineapple water.", "promo": None, "img": None},
        {"id": 101, "name": "Horchata", "price": 8.50, "desc": "Sweet and refreshing Mexican drink (rice and cinnamon).", "promo": "Buy 1, get 1 free", "img": None},
        {"id": 102, "name": "Tamarindo", "price": 8.50, "desc": "Sweet and tart tamarind beverage.", "promo": None, "img": None}
        
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
            
