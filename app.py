
import streamlit as st
import json

st.title("🛍️ Product Info Chat Assistant")

# Load product data safely
try:
    with open("products.json") as f:
        products = json.load(f)
    st.success("✅ Product data loaded successfully.")
except Exception as e:
    st.error(f"❌ Failed to load product data: {e}")
    st.stop()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Helper function to display product specs
def format_product_details(product):
    lines = []
    for key, value in product.items():
        if key not in ["product_id", "name"]:
            lines.append(f"{key.replace('_', ' ').capitalize()}: {value}")
    return "\n".join(lines)

# Main logic to handle user queries
def get_answer(user_input):
    user_input_lower = user_input.lower()
    exact_matches = []
    partial_matches = []

    for product in products:
        name_lower = product["name"].lower()
        if user_input_lower in name_lower:
            exact_matches.append(product)
        elif any(word in name_lower for word in user_input_lower.split()):
            partial_matches.append(product)

    if exact_matches:
        product = exact_matches[0]
        response_lines = [f"Here is what I found for {product['name']}:", ""]
        response_lines += format_product_details(product).split("\n")
        return response_lines

    elif partial_matches:
        response_lines = ["Here are the results that may match what you're looking for:", ""]
        for product in partial_matches:
            response_lines.append(f"🔹 {product['name']}")
            response_lines += format_product_details(product).split("\n")
            response_lines.append("")
        return response_lines

    return ["Sorry, I couldn't find that information."]

# Handle user input and display chat
user_input = st.chat_input("Ask about the product...")

if user_input:
    answer_lines = get_answer(user_input)
    st.session_state.chat_history.append((user_input, answer_lines))

for q, a_lines in st.session_state.chat_history:
    st.chat_message("user").write(q)
    st.chat_message("assistant").write("\n".join(a_lines))
