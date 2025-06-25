
import streamlit as st
import json

st.title("🛍️ Product Info Chat Assistant")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("Ask about the product...")

# Load product data
try:
    with open("products.json") as f:
        products = json.load(f)
except Exception as e:
    st.error("❌ Failed to load product data. Check if 'products.json' exists.")
    st.stop()

def get_answer(user_input):
    user_input_lower = user_input.lower()
    
    for product in products:
        if user_input_lower in product["name"].lower():
            # Build full spec response
            response_lines = [f"Here is what I found for {product['name']}:"]
            for key, value in product.items():
                if key != "product_id" and key != "name":
                    response_lines.append(f"{key.capitalize()}: {value}")
            return "\n".join(response_lines)

    return "Sorry, I couldn't find that information."

if user_input:
    answer = get_answer(user_input)
    st.session_state.chat_history.append((user_input, answer))

for q, a in st.session_state.chat_history:
    st.chat_message("user").write(q)
    st.chat_message("assistant").write(a)
