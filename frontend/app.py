import streamlit as st
import requests
import re
import os
import base64

# ------------------------------
# Function: Detect Tamil or English
# ------------------------------
def detect_language(text):
    tamil_pattern = r'[\u0B80-\u0BFF]'
    return "ta" if re.search(tamil_pattern, text) else "en"

# ------------------------------
# Session State Init
# ------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ------------------------------
# Page Configuration
# ------------------------------
st.set_page_config(page_title="🧘 Tourism Chatbot", layout="wide")

# ------------------------------
# Encode background image as base64
# ------------------------------
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

bg_img_path = "Thanjai.jpg"  # Put this image in the same directory
if os.path.exists(bg_img_path):
    base64_img = get_base64_image(bg_img_path)
    st.markdown(f"""
        <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{base64_img}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }}
        </style>
    """, unsafe_allow_html=True)

# ------------------------------
# Sidebar - Chat History Summary
# ------------------------------
with st.sidebar:
    st.title("🕘 Chat History")
    if st.button("🗑 Clear Chat History"):
        st.session_state.chat_history = []
    for i, item in enumerate(reversed(st.session_state.chat_history)):
        st.markdown(f"🗨 {item['question'][:30]}...")

# ------------------------------
# Custom CSS for Chat Styling
# ------------------------------
st.markdown("""
    <style>
        .user-msg {
            background-color: #f1f1f1;
            padding: 10px 15px;
            border-radius: 15px;
            max-width: 70%;
            margin-left: auto;
            margin-bottom: 10px;
            color: black;
        }
        .bot-msg {
            background-color: #7e57c2;
            padding: 10px 15px;
            border-radius: 15px;
            max-width: 70%;
            margin-right: auto;
            margin-bottom: 10px;
            color: white;
        }
        .chat-container {
            height: 500px;
            overflow-y: auto;
            padding: 10px 20px 10px 0px;
        }
    </style>
""", unsafe_allow_html=True)

# ------------------------------
# Chat Display Section
# ------------------------------
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for chat in st.session_state.chat_history:
    st.markdown(f'<div class="user-msg">{chat["question"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="bot-msg">{chat["answer"]}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------
# Styled Input Field at Bottom
# ------------------------------
with st.form("chat_input_form", clear_on_submit=True):
    query = st.text_area("Type your message here...", key="custom_input", label_visibility="collapsed")
    send_clicked = st.form_submit_button("Send", use_container_width=True)

# ------------------------------
# Handle Submission
# ------------------------------
if send_clicked and query.strip():
    lang = detect_language(query)
    try:
        response = requests.post("http://127.0.0.1:8000/query", json={"query": query.strip(), "lang": lang})
        if response.status_code == 200:
            answer = response.json().get("answer", "Sorry, I couldn't find an answer.")
        else:
            answer = "Backend error."
    except Exception as e:
        answer = f"Connection error: {e}"

    st.session_state.chat_history.append({"question": query, "answer": answer})
    st.rerun()
elif send_clicked:
    st.warning("Please enter a message.")