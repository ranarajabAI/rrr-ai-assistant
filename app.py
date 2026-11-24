
import streamlit as st

from ai_engine import generate_response
from document_processor import (
    prepare_document,
    search_documents
)

st.set_page_config(
    page_title="RRR AI Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 RRR AI Assistant")
st.caption("Your personal AI assistant")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "documents" not in st.session_state:
    st.session_state.documents = []

# Sidebar
with st.sidebar:
    st.title("Settings")

    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.subheader("📁 Upload Files")

    uploaded_files = st.file_uploader(
        "Upload PDF, DOCX or TXT",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True
    )

    if st.button("Process Uploaded Files"):
        if uploaded_files:
            new_documents = []

            with st.spinner("Reading your files..."):
                for file in uploaded_files:
                    chunks = prepare_document(file)
                    new_documents.extend(chunks)

            st.session_state.documents = new_documents

            st.success(
                f"Processed {len(uploaded_files)} file(s)."
            )
        else:
            st.warning("Please upload a file first.")

    st.write(
        f"Document sections: {len(st.session_state.documents)}"
    )

    st.divider()
    st.caption("RRR AI Assistant | Built with Streamlit")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Ask RRR AI Assistant anything...")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

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

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
        
