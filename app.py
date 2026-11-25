
import streamlit as st

from ai_engine import generate_response
from document_processor import (
    prepare_document,
    search_documents
)

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="RRR AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM THEME ----------------

st.markdown("""
<style>
.stApp {
    background-color: #0B1220;
    color: #F1F5F9;
}

[data-testid="stSidebar"] {
    background-color: #162338;
}

[data-testid="stSidebar"] * {
    color: #F1F5F9;
}

.main .block-container {
    padding-top: 2rem;
    max-width: 1100px;
}

h1, h2, h3 {
    color: #F1F5F9 !important;
}

.stChatInput textarea {
    color: #F1F5F9;
}

.stButton button {
    border-radius: 10px;
    border: 1px solid #0D9488;
    background-color: #162338;
    color: white;
}

.stButton button:hover {
    background-color: #0D9488;
    color: white;
    border: 1px solid #0D9488;
}

[data-testid="stChatMessage"] {
    border: 1px solid #263B55;
    border-radius: 15px;
    padding: 15px;
}

hr {
    border-color: #263B55;
}
</style>
""", unsafe_allow_html=True)

# ---------------- MAIN HEADER ----------------

st.markdown("""
<div style="
    padding: 25px 10px;
    border-radius: 18px;
    background: linear-gradient(135deg, #162338, #0D9488);
    text-align: center;
    margin-bottom: 20px;
">
    <h1 style="color:white;">
        RRR AI Assistant
    </h1>
    <p style="color:#E0F2FE;">
        AI Innovation • Smart Assistance
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "documents" not in st.session_state:
    st.session_state.documents = []

# ---------------- SIDEBAR ----------------

with st.sidebar:

    # LOGO
    st.image(
        "rrr_logo_808x808_edited.jpg",
        width=180
    )

    st.markdown("## RRR AI")
    st.caption("AI Innovation • Smart Assistance")

    st.divider()

    # NEW CHAT
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    # DOCUMENT UPLOAD
    st.subheader("📁 Documents")

    uploaded_files = st.file_uploader(
        "Upload your documents",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True
    )

    if st.button(
        "📚 Process Documents",
        use_container_width=True
    ):

        if uploaded_files:

            new_documents = []

            with st.spinner("Processing documents..."):

                for file in uploaded_files:

                    chunks = prepare_document(file)

                    new_documents.extend(chunks)

            st.session_state.documents = new_documents

            st.success(
                f"Processed {len(uploaded_files)} file(s)."
            )

        else:

            st.warning("Upload documents first.")

    # DOCUMENT COUNT
    st.metric(
        "Document Sections",
        len(st.session_state.documents)
    )

    # CLEAR DOCUMENTS
    if st.button(
        "🗑️ Clear Documents",
        use_container_width=True
    ):

        st.session_state.documents = []

        st.rerun()

    st.divider()

    st.caption("RRR AI Assistant | AI Innovation Lab")

# ---------------- DISPLAY CHAT HISTORY ----------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# ---------------- CHAT INPUT ----------------

prompt = st.chat_input(
    "Ask RRR AI Assistant anything..."
)

if prompt:

    # USER MESSAGE
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):

        st.markdown(prompt)

    # ASSISTANT RESPONSE
    with st.chat_message("assistant"):

        with st.spinner("Preparing response..."):

            relevant_sections = search_documents(
                prompt,
                st.session_state.documents
            )

            document_context = "\n\n".join(
                relevant_sections
            )

            response = generate_response(
                prompt,
                document_context
            )

            st.markdown(response)

    # SAVE RESPONSE
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
