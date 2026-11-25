
import streamlit as st
from pypdf import PdfReader
from docx import Document
from PIL import Image
import io

st.set_page_config(
    page_title="RRR AI Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 RRR AI Assistant")
st.caption("Your intelligent assistant workspace")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "documents" not in st.session_state:
    st.session_state.documents = ""

# New chat
if st.button("➕ New Chat"):
    st.session_state.messages = []
    st.rerun()

# Upload section
st.subheader("📁 Upload Files")

uploaded_files = st.file_uploader(
    "Upload PDF, DOCX, TXT or images",
    type=["pdf", "docx", "txt", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)

def extract_text(file):
    text = ""

    try:
        if file.name.lower().endswith(".pdf"):
            reader = PdfReader(file)
            text = "\n".join(
                page.extract_text() or ""
                for page in reader.pages
            )

        elif file.name.lower().endswith(".docx"):
            doc = Document(file)
            text = "\n".join(
                paragraph.text for paragraph in doc.paragraphs
            )

        elif file.name.lower().endswith(".txt"):
            text = file.read().decode("utf-8", errors="ignore")

    except Exception as e:
        st.error(f"Could not read {file.name}: {e}")

    return text

if uploaded_files:
    collected_text = []

    for file in uploaded_files:
        if file.name.lower().endswith(
            (".pdf", ".docx", ".txt")
        ):
            extracted = extract_text(file)
            if extracted:
                collected_text.append(
                    f"\n--- {file.name} ---\n{extracted}"
                )

        elif file.name.lower().endswith(
            (".png", ".jpg", ".jpeg")
        ):
            try:
                image = Image.open(file)
                st.image(image, caption=file.name)
            except Exception:
                st.warning(f"Could not display {file.name}")

    st.session_state.documents = "\n".join(collected_text)

    if st.session_state.documents:
        st.success("Document text loaded.")

# Chat display
st.subheader("💬 Chat")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Ask RRR AI Assistant...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = (
            "The AI engine is not connected yet. "
            "Your message has been received by RRR AI Assistant. "
            "A permitted hosted generative AI connection is required "
            "to generate real AI answers."
        )

        st.markdown(response)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )
