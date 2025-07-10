import streamlit as st

# ---- Menu and Pricing ----
menu = {
    'pizza': 350,
    'burger': 120,
    'momos': 50,
    'chowmein': 40,
    'maggi': 45,
    'veg-roll': 60
}

unit = {'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
        'six': 6, 'seven': 7, 'eight': 8, 'nine': 9}
tens = {'ten': 10, 'twenty': 20, 'thirty': 30, 'forty': 40, 'fifty': 50}
teens = {'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14,
         'fifteen': 15, 'sixteen': 16, 'seventeen': 17, 'eighteen': 18, 'nineteen': 19}

# ---- Session State Initialization ----
if 'bill' not in st.session_state:
    st.session_state.bill = {}

if 'total' not in st.session_state:
    st.session_state.total = 0

# ---- Utility Functions ----
def change_num(number):
    words = number.split()
    total = 0
    chunks = 0
    for word in words:
        if word in unit:
            chunks += unit[word]
        elif word in tens:
            chunks += tens[word]
        elif word in teens:
            chunks += teens[word]
    total += chunks
    return total

def menu_function():
    st.subheader("📋 Menu")
    for key, value in menu.items():
        st.write(f"👉 {key.title()} - ₹{value}")

def order_from_input(user_input):
    found_any = False
    for item in menu:
        if item in user_input:
            found_any = True
            quantity = 1
            words = user_input.split()
            for word in words:
                if word.isdigit():
                    quantity = int(word)
                elif word in unit or word in tens or word in teens:
                    quantity = change_num(word)
            if item in st.session_state.bill:
                st.session_state.bill[item] += quantity
            else:
                st.session_state.bill[item] = quantity
            st.success(f"Added {quantity} {item}(s) to your order.")
    if not found_any:
        st.warning("No valid items found in your input.")

def show_bill():
    st.subheader("🧾 Your Bill")
    total = 0
    for item, qty in st.session_state.bill.items():
        amount = menu[item] * qty
        st.write(f"**{item.title()}** × {qty} = ₹{amount}")
        total += amount
    st.session_state.total = total
    st.markdown(f"### 💰 Total: ₹{total}")

def remove_order(user_input):
    remove_words = ['remove', 'delete', 'lower']
    found = False
    for item in list(st.session_state.bill):
        for word in remove_words:
            if word in user_input and item in user_input:
                quantity = 0
                words = user_input.split()
                for w in words:
                    if w.isdigit():
                        quantity = int(w)
                        break
                    elif w in unit or w in tens or w in teens:
                        quantity = change_num(w)
                        break
                if quantity > 0:
                    if st.session_state.bill[item] > quantity:
                        st.session_state.bill[item] -= quantity
                        st.success(f"Removed {quantity} {item}(s). Remaining: {st.session_state.bill[item]}")
                    elif st.session_state.bill[item] == quantity:
                        st.session_state.bill.pop(item)
                        st.info(f"All {item}(s) removed from your order.")
                    else:
                        st.warning(f"You only have {st.session_state.bill[item]} {item}(s), can't remove {quantity}.")
                    found = True
                    break
                else:
                    st.session_state.bill.pop(item)
                    st.info(f"{item} has been removed from your order.")
                    found = True
                    break
        if found:
            break
    if not found:
        st.warning("Could not understand what to remove. Please try again.")

# ---- Streamlit Page Layout ----
st.title("🍽️ Welcome to Food Order Bot")
menu_function()
st.markdown("---")

user_input = st.text_input("What would you like to order? (e.g., 'two pizzas and 1 burger')")

if st.button("Place Order"):
    if user_input.strip():
        order_from_input(user_input.lower())
    else:
        st.warning("Please enter your order.")

if st.button("Show Bill"):
    if st.session_state.bill:
        show_bill()
    else:
        st.info("Your order bucket is empty.")

remove_input = st.text_input("Want to remove something? (e.g., 'remove 1 burger')")

if st.button("Remove Item"):
    if remove_input.strip():
        remove_order(remove_input.lower())
    else:
        st.warning("Please enter what you want to remove.")
