
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
st.caption("RRR AI Innovation Lab | Version 2")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "documents" not in st.session_state:
    st.session_state.documents = []

# New chat
if st.sidebar.button("➕ New Chat"):
    st.session_state.messages = []
    st.rerun()

st.sidebar.header("📁 Upload Documents")

uploaded_files = st.sidebar.file_uploader(
    "Choose your files",
    type=["pdf", "docx", "txt", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)

documents = []

if uploaded_files:
    for file in uploaded_files:
        filename = file.name.lower()

        try:
            if filename.endswith(".pdf"):
                reader = PdfReader(file)
                content = "\n".join(
                    page.extract_text() or ""
                    for page in reader.pages
                )

            elif filename.endswith(".docx"):
                doc = Document(file)
                content = "\n".join(
                    p.text for p in doc.paragraphs
                )

            elif filename.endswith(".txt"):
                content = file.getvalue().decode(
                    "utf-8", errors="ignore"
                )

            elif filename.endswith((".png", ".jpg", ".jpeg")):
                picture = Image.open(file)
                st.sidebar.image(
                    picture,
                    caption=file.name,
                    use_container_width=True
                )
                continue

            else:
                continue

            if content.strip():
                documents.append({
                    "name": file.name,
                    "text": content
                })

        except Exception as error:
            st.sidebar.error(
                f"Error reading {file.name}: {error}"
            )

st.session_state.documents = documents

if documents:
    st.sidebar.success(
        f"{len(documents)} document(s) loaded"
    )

def make_paragraphs(text):
    paragraphs = re.split(r"\n\s*\n|\n", text)
    return [
        p.strip()
        for p in paragraphs
        if len(p.strip()) > 30
    ]

def search_documents(question, documents):
    stopwords = {
        "the", "is", "are", "was", "were", "what",
        "why", "how", "when", "where", "who",
        "explain", "describe", "tell", "me", "about",
        "give", "please", "and", "for", "with",
        "from", "this", "that", "complete", "details",
        "detailed", "information"
    }

    keywords = [
        word.lower()
        for word in re.findall(r"\w+", question)
        if len(word) > 2 and word.lower() not in stopwords
    ]

    if not keywords:
        return "Please ask a more specific question."

    matches = []

    for document in documents:
        paragraphs = make_paragraphs(document["text"])

        for paragraph in paragraphs:
            lower = paragraph.lower()

            score = sum(
                lower.count(word) for word in keywords
            )

            if score > 0:
                matches.append({
                    "score": score,
                    "source": document["name"],
                    "text": paragraph
                })

    matches.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    if not matches:
        return (
            "I couldn't find relevant information "
            "in your uploaded documents. Try using "
            "different keywords or uploading another file."
        )

    # Remove duplicate passages
    unique_matches = []
    seen = set()

    for item in matches:
        key = item["text"].lower()

        if key not in seen:
            seen.add(key)
            unique_matches.append(item)

    answer = "## Detailed information from your documents\n\n"

    for number, item in enumerate(unique_matches[:8], 1):
        answer += (
            f"### Section {number}\n"
            f"**Source:** {item['source']}\n\n"
            f"{item['text']}\n\n"
            "---\n\n"
        )

    answer += (
        "*These are relevant passages retrieved from "
        "your documents. They are not AI-generated "
        "explanations.*"
    )

    return answer

# Display conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Ask questions
question = st.chat_input(
    "Ask anything about your uploaded documents..."
)

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        if st.session_state.documents:
            answer = search_documents(
                question,
                st.session_state.documents
            )
        else:
            answer = (
                "Welcome to RRR AI Assistant! "
                "Please upload a PDF, Word or TXT document "
                "so I can search its contents. General AI "
                "chat will be added after we connect an "
                "eligible AI model."
            )

        st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

st.sidebar.divider()
st.sidebar.caption("Built with Streamlit")
st.sidebar.caption("RRR AI Innovation Lab")
    
