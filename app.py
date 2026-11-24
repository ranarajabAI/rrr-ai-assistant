
import streamlit as st
from pypdf import PdfReader
from docx import Document
from io import BytesIO

st.set_page_config(
    page_title="RRR AI Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 RRR AI Assistant")
st.caption("Your personal AI assistant")

with st.sidebar:
    st.header("Your Assistant")
    st.write("Upload documents, images or record your voice.")

    uploaded_file = st.file_uploader(
        "Upload a file",
        type=["pdf", "txt", "docx", "png", "jpg", "jpeg"]
    )

    if uploaded_file:
        file_name = uploaded_file.name
        st.success(f"Uploaded: {file_name}")

        if file_name.endswith(".pdf"):
            reader = PdfReader(uploaded_file)
            text = "\n".join(
                page.extract_text() or ""
                for page in reader.pages
            )
            st.text_area("PDF text", text, height=200)

        elif file_name.endswith(".txt"):
            text = uploaded_file.getvalue().decode(
                "utf-8", errors="replace"
            )
            st.text_area("File text", text, height=200)

        elif file_name.endswith(".docx"):
            doc = Document(uploaded_file)
            text = "\n".join(
                p.text for p in doc.paragraphs
            )
            st.text_area("Document text", text, height=200)

        elif file_name.lower().endswith(
            (".png", ".jpg", ".jpeg")
        ):
            st.image(uploaded_file, use_container_width=True)

    st.divider()
    st.subheader("Voice input")
    audio = st.audio_input("Record your voice")

    if audio:
        st.audio(audio)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("Ask RRR AI Assistant...")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    answer = (
        "Welcome! Your chatbot interface is working. "
        "The AI model connection will be added next."
    )

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    with st.chat_message("assistant"):
        st.write(answer)
        
