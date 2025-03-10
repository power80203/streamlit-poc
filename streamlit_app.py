import streamlit as st
from openai import OpenAI

# Set page configuration
st.set_page_config(page_title="Chatbot Dashboard", layout="wide")


# Sidebar with three options
st.sidebar.title("📊 功能選單")
st.sidebar.page_link("交通壅塞", "#", label="Page 1")
st.sidebar.page_link("人流分析", "#", label="Page 2", disabled=True)
st.sidebar.page_link("路線改善", "#", label="Page 3", disabled=True)


# Display login info at the top right
st.markdown("<div style='text-align: right; font-size: 18px; font-weight: bold;'>🔑 使用者：admin</div>", unsafe_allow_html=True)

# Title for chat area
st.title("💬 交通壅塞對話助手")

# Initialize session state for chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input (always available)
prompt = st.chat_input("請輸入訊息...")

# Ask user for their OpenAI API key
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    pass
    #st.info("請輸入 OpenAI API key 才能啟用 AI 回應功能。", icon="🗝️")
else:
    # Create an OpenAI client
    client = OpenAI(api_key=openai_api_key)
    
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