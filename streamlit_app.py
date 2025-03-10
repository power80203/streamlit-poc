import streamlit as st
from openai import OpenAI

# Set page configuration
st.set_page_config(page_title="Chatbot Dashboard", layout="wide")


# Apply dark theme styling
st.markdown(
    """
    <style>
    body {
        background-color: #121212;
        color: white;
    }
    .stApp {
        background-color: #121212;
        color: white;
    }
    .stSidebar {
        background-color: #1E1E1E;
        color: white;
    }
    .stChatMessage {
        background-color: #1E1E1E;
        color: white;
        border-radius: 10px;
        padding: 10px;
        margin: 5px;
    }
    .stTextInput > div > div > input {
        background-color: #333;
        color: white;
        border: 1px solid white;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Sidebar with three options
st.sidebar.title("📊 功能選單")
page = st.sidebar.radio("選擇功能", ["交通壅塞", "人流分析", "路線改善"])

# 顯示當前頁面標題
st.title(f"💬 {page} 對話助手")

# Display login info at the top right
st.markdown("<div style='text-align: right; font-size: 18px; font-weight: bold;'>🔑 使用者：admin</div>", unsafe_allow_html=True)

# 初始化 session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# 顯示對話
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input (always available)
prompt = st.chat_input("請輸入訊息...")

if "openai_api_key" in st.session_state and st.session_state.openai_api_key:
    # Create an OpenAI client
    client = OpenAI(api_key=st.session_state.openai_api_key)
    
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        )

        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})