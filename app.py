
import streamlit as st
import json

st.title("🛍️ Product Info Chat Assistant")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("Ask about the product...")

# Load product data
with open("products.json") as f:
    products = json.load(f)

def get_answer(user_input):
    user_input_lower = user_input.lower()
    for product in products:
        response_parts = []
        for key, value in product.items():
            if key != "product_id" and user_input_lower in value.lower():
                response_parts.append(f"{key.capitalize()}: {value}")
        if response_parts:
            return f"Here is what I found for {product['name']}:" + "\n".join(response_parts)
    return "Sorry, I couldn’t find that information."

if user_input:
    answer = get_answer(user_input)
    st.session_state.chat_history.append((user_input, answer))

for q, a in st.session_state.chat_history:
    st.chat_message("user").write(q)
    st.chat_message("assistant").write(a)
