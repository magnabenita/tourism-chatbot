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
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

bg_img_path = "Thanjai.jpg"
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
else:
    st.warning("Background image not found. Make sure 'Thanjai.jpg' is in the correct folder.")

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
            background-color: rgba(255, 255, 255, 0.9);
            z-index: 1000;
            padding: 1rem;
            text-align: center;
            font-size: 2vw;
            font-weight: bold;
            color: #6A1B9A;
            border-bottom: 2px solid #6A1B9A;
        }

        section[data-testid="stSidebar"] {
            background-color: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-right: 1px solid rgba(255, 255, 255, 0.2);
            color: #000 !important;
        }

        section[data-testid="stSidebar"] .block-container {
            background-color: transparent;
        }
            
        .chat-container {
            margin-top: 90px;
            margin-bottom: 150px;
            height: 60vh;
            overflow-y: auto;
            padding: 10px 20px 10px 10px;
        }

        .user-msg, .bot-msg {
            padding: 12px 18px;
            border-radius: 15px;
            max-width: 80%;
            margin-bottom: 12px;
            font-size: 1rem;
        }

        .user-msg {
            background-color: #E1F5FE;
            margin-left: auto;
            color: #0D47A1;
        }

        .bot-msg {
            background-color: #BA68C8;
            margin-right: auto;
            color: white;
        }

        .chat-input {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(255,255,255,0.9);
            padding: 10px 20px;
            z-index: 999;
        }

        textarea, .stButton>button {
            font-size: 16px !important;
        }

        @media (max-width: 768px) {
            .fixed-header {
                font-size: 5vw;
                padding: 0.8rem;
            }

            .chat-container {
                height: 55vh;
                padding: 10px;
            }

            .user-msg, .bot-msg {
                font-size: 0.9rem;
                max-width: 90%;
            }
        }
    </style>
""", unsafe_allow_html=True)

# ------------------------------
# Static Welcome Header (Fixed)
# ------------------------------
st.markdown("""
    <style>
        .fixed-header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background-color: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            z-index: 1000;
            padding: 1rem;
            text-align: center;
            font-size: 2.4vw;
            font-weight: bold;
            font-family: 'Apple Chancery', cursive;
            color: #d3d3d3;
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        }
    </style>
""", unsafe_allow_html=True)


st.markdown('<div class="fixed-header">🌄 Discover the Wonders of Tamil Nadu – Powered by AI</div>', unsafe_allow_html=True)

# ------------------------------
# Sidebar - Chat History Summary
# ------------------------------
with st.sidebar:
    st.title("🕘 Chat History")
    if st.button("🗑 Clear Chat History"):
        st.session_state.chat_history = []
    for i, item in enumerate(reversed(st.session_state.chat_history)):
        st.markdown(f"👨‍💬 {item['question'][:30]}...")

# ------------------------------
# Chat Display Section
# ------------------------------
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

if len(st.session_state.chat_history) == 0:
    st.markdown(
        '<div class="bot-msg">Hi there! 👋 Ask me about temples, places, festivals or anything in Tamil Nadu tourism.</div>',
        unsafe_allow_html=True
    )

for chat in st.session_state.chat_history:
    st.markdown(f'<div class="user-msg">{chat["question"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="bot-msg">{chat["answer"]}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------
# Fixed Chat Input using st.chat_input
# ------------------------------
query = st.chat_input("Type your message here...")

# ------------------------------
# Handle Submission
# ------------------------------
if query and query.strip():
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
elif query:
    st.warning("Please enter a message.")
