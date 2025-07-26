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
# Background Image Styling
# ------------------------------
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

bg_img_path = "Thanjai.jpg"
base64_img = get_base64_image(bg_img_path)

if base64_img:
    st.markdown(f"""
        <style>
            .stApp {{
                background-image: linear-gradient(to bottom, rgba(255,255,255,0.2), rgba(255,255,255,0.3)),
                                  url("data:image/jpg;base64,{base64_img}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                font-family: 'Segoe UI', sans-serif;
                color: #333;
            }}
        </style>
    """, unsafe_allow_html=True)

# ------------------------------
# Custom CSS for Layout
# ------------------------------
st.markdown("""
    <style>
        .fixed-header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: linear-gradient(90deg, #6A1B9A, #AB47BC);
            color: white;
            z-index: 1000;
            padding: 1rem;
            text-align: center;
            font-size: 2.2vw;
            font-weight: 600;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        .chat-container {
            margin-top: 100px;
            margin-bottom: 130px;
            height: 60vh;
            overflow-y: auto;
            padding: 0 25px;
        }

        .user-msg, .bot-msg {
            padding: 14px 20px;
            border-radius: 20px;
            max-width: 80%;
            margin-bottom: 16px;
            font-size: 1.05rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .user-msg {
            background-color: #DCE775;
            margin-left: auto;
            color: #33691E;
        }

        .bot-msg {
            background-color: #9575CD;
            margin-right: auto;
            color: white;
        }

        .chat-input {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(255,255,255,0.95);
            padding: 12px 25px;
            z-index: 999;
            box-shadow: 0 -2px 5px rgba(0,0,0,0.1);
        }

        textarea, .stButton>button {
            font-size: 16px !important;
            border-radius: 10px !important;
        }

        @media (max-width: 768px) {
            .fixed-header {
                font-size: 5vw;
                padding: 1rem 0.5rem;
            }
            .chat-container {
                height: 55vh;
                padding: 0 15px;
            }
            .user-msg, .bot-msg {
                font-size: 0.95rem;
                max-width: 90%;
            }
        }
    </style>
""", unsafe_allow_html=True)

# ------------------------------
# Static Welcome Header (Fixed)
# ------------------------------
st.markdown('<div class="fixed-header">🌄 Discover the Wonders of Tamil Nadu – Powered by AI</div>', unsafe_allow_html=True)

# ------------------------------
# Sidebar - Chat History Summary
# ------------------------------
with st.sidebar:
    st.title("🕘 Chat History")
    if st.button("🗑 Clear Chat History"):
        st.session_state.chat_history = []
    for item in reversed(st.session_state.chat_history):
        st.markdown(f"🗨 {item['question'][:30]}...")

# ------------------------------
# Chat Display Section
# ------------------------------
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

if not st.session_state.chat_history:
    st.markdown(
        '<div class="bot-msg">Hi there! 👋 Ask me about temples, places, festivals or anything in Tamil Nadu tourism.</div>',
        unsafe_allow_html=True
    )

for chat in st.session_state.chat_history:
    st.markdown(f'<div class="user-msg">{chat["question"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="bot-msg">{chat["answer"]}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------
# Chat Input Handler
# ------------------------------
query = st.chat_input("Type your message here...")

if query and query.strip():
    lang = detect_language(query.strip())

    try:
        response = requests.post("http://127.0.0.1:8000/query", json={"query": query.strip(), "lang": lang})
        if response.status_code == 200:
            answer = response.json().get("answer", "Sorry, I couldn't find an answer.")
        else:
            answer = "⚠️ Backend error. Please try again later."
    except Exception as e:
        answer = f"🚫 Connection error: {e}"

    st.session_state.chat_history.append({"question": query, "answer": answer})
    st.rerun()
elif query:
    st.warning("Please enter a message.")

# ------------------------------
# Footer
# ------------------------------
st.markdown("""
    <hr>
    <div style="text-align:center; font-size:14px; background:#f9f9f9; padding:15px; border-radius:12px; margin-top:20px;">
        <p><strong>Note:</strong> This is a prototype version of the Tamil Nadu Tourism AI Assistant. It may produce incomplete or incorrect responses.</p>
        <p><em>Try asking:</em> “Top temples in Madurai” | “Where to go for Pongal celebration?”</p>
        <p><strong>Created by:</strong> Magna, Vasundhara, Anu, Aarmitha, Keerthi, Adhvaitha</p>
    </div>
""", unsafe_allow_html=True)
