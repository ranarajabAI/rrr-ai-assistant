
import streamlit as st

st.set_page_config(
    page_title="RRR AI Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 RRR AI Assistant")
st.caption("Your personal AI assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Settings")
    if st.button("New Chat"):
        st.session_state.messages = []
        st.rerun()

    st.write("PDF, image and voice features coming soon.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("Ask me anything...")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    answer = (
        "Welcome to RRR AI Assistant! "
        "The AI connection will be added in the next step."
    )

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    with st.chat_message("assistant"):
        st.write(answer)
      
