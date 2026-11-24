
import streamlit as st
import re
from pypdf import PdfReader
from docx import Document
from PIL import Image

st.set_page_config(
    page_title="RRR AI Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 RRR AI Assistant")
st.caption("Your document-based assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "document_text" not in st.session_state:
    st.session_state.document_text = ""

if st.sidebar.button("➕ New Chat"):
    st.session_state.messages = []
    st.rerun()

st.sidebar.header("📁 Upload Files")

files = st.sidebar.file_uploader(
    "Upload PDF, DOCX, TXT or image",
    type=["pdf", "docx", "txt", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)

all_text = []

if files:
    for file in files:
        name = file.name.lower()

        try:
            if name.endswith(".pdf"):
                reader = PdfReader(file)
                text = "\n".join(
                    page.extract_text() or ""
                    for page in reader.pages
                )
                all_text.append(text)

            elif name.endswith(".docx"):
                doc = Document(file)
                text = "\n".join(
                    paragraph.text
                    for paragraph in doc.paragraphs
                )
                all_text.append(text)

            elif name.endswith(".txt"):
                all_text.append(
                    file.getvalue().decode("utf-8", errors="ignore")
                )

            elif name.endswith((".png", ".jpg", ".jpeg")):
                image = Image.open(file)
                st.sidebar.image(
                    image,
                    caption=file.name,
                    use_container_width=True
                )

        except Exception as error:
            st.sidebar.error(f"Could not read {file.name}: {error}")

    st.session_state.document_text = "\n".join(all_text)

if st.session_state.document_text:
    st.success("Document text loaded successfully!")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask a question about your document...")

def search_document(question, document):
    sentences = re.split(r'(?<=[.!?])\s+|\n+', document)

    keywords = [
        word.lower()
        for word in re.findall(r'\w+', question)
        if len(word) > 2
    ]

    results = []

    for sentence in sentences:
        sentence_lower = sentence.lower()
        score = sum(
            1 for word in keywords
            if word in sentence_lower
        )

        if score > 0:
            results.append((score, sentence.strip()))

    results.sort(key=lambda item: item[0], reverse=True)

    if not results:
        return "I could not find a matching answer in your uploaded document."

    answer = "\n\n".join(
        sentence for score, sentence in results[:5]
    )

    return "Here are the most relevant passages:\n\n" + answer

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    if st.session_state.document_text.strip():
        answer = search_document(
            question,
            st.session_state.document_text
        )
    else:
        answer = (
            "Please upload a PDF, DOCX or TXT document first. "
            "I can search its text to find relevant passages."
        )

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    with st.chat_message("assistant"):
        st.markdown(answer)

st.sidebar.divider()
st.sidebar.caption("RRR AI Innovation Lab")
