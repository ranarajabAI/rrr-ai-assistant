
import os
import streamlit as st

from ai_engine import generate_response
from document_processor import prepare_document, search_documents

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="RRR AI Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# SESSION STATE
# ==================================================

defaults = {
    "messages": [],
    "documents": [],
    "active_page": "Chat",
    "pending_prompt": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ==================================================
# LOGO CONFIGURATION
# ==================================================

LOGO_FILE = "rrr_brain_logo.png"

def display_logo(width=150):

    if os.path.exists(LOGO_FILE):
        st.image(LOGO_FILE, width=width)
    else:
        st.markdown(
            f"<div style='font-size:{width//2}px;text-align:center;'>🧠</div>",
            unsafe_allow_html=True
        )

# ==================================================
# THEME
# ==================================================

st.markdown("""
<style>

.stApp {
    background: #07111F;
    color: #EAF6FF;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D1B2E, #06101D);
    border-right: 1px solid #164E73;
}

[data-testid="stSidebar"] * {
    color: #EAF6FF;
}

.block-container {
    max-width: 1400px;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

h1, h2, h3 {
    color: #EAF6FF !important;
}

.stButton > button {
    background: #10243B;
    color: #EAF6FF;
    border: 1px solid #087EAA;
    border-radius: 12px;
    min-height: 42px;
}

.stButton > button:hover {
    background: #087EAA;
    color: white;
    border: 1px solid #00E5FF;
}

[data-testid="stChatMessage"] {
    background: #10243B;
    border: 1px solid #164E73;
    border-radius: 16px;
}

[data-testid="stChatInput"] {
    border: 1px solid #00BCD4;
    border-radius: 16px;
}

hr {
    border-color: #164E73;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    display_logo(180)

    st.markdown("## RRR AI")
    st.caption("AI Innovation • Smart Assistance")

    st.divider()

    if st.button("➕ New Chat", use_container_width=True):

        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.session_state.active_page = "Chat"

        st.rerun()

    st.divider()

    st.markdown("### Navigation")

    if st.button("💬 Chat", use_container_width=True):
        st.session_state.active_page = "Chat"
        st.rerun()

    if st.button("📜 History", use_container_width=True):
        st.session_state.active_page = "History"
        st.rerun()

    if st.button("ℹ️ About", use_container_width=True):
        st.session_state.active_page = "About"
        st.rerun()

    if st.button("⚙️ Settings", use_container_width=True):
        st.session_state.active_page = "Settings"
        st.rerun()

    st.divider()

    st.markdown("### 📁 Documents")

    uploaded_files = st.file_uploader(
        "Upload PDF, DOCX or TXT",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True
    )

    if st.button("📚 Process Documents", use_container_width=True):

        if uploaded_files:

            all_chunks = []

            with st.spinner("Reading your documents..."):

                for uploaded_file in uploaded_files:

                    chunks = prepare_document(uploaded_file)
                    all_chunks.extend(chunks)

            st.session_state.documents = all_chunks

            st.success("Documents processed successfully!")

        else:

            st.warning("Please upload files first.")

    st.metric(
        "Document Sections",
        len(st.session_state.documents)
    )

    if st.button("🗑️ Clear Documents", use_container_width=True):

        st.session_state.documents = []
        st.rerun()

    st.divider()

    st.caption("RRR AI Innovation Lab")

# ==================================================
# MAIN HEADER
# ==================================================

logo_col, title_col = st.columns([1, 5])

with logo_col:

    display_logo(160)

with title_col:

    with st.container(border=True):

        st.title("RRR AI Assistant")

        st.markdown(
            "**AI Innovation • Smart Assistance**"
        )

# ==================================================
# QUICK ACTIONS
# ==================================================

if st.session_state.active_page == "Chat":

    st.markdown("### ✨ Quick Actions")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        if st.button("💬 Smart Chat", use_container_width=True):
            st.session_state.pending_prompt = (
                "Help me explore what you can do."
            )

    with col2:

        if st.button("📄 Document AI", use_container_width=True):
            st.session_state.pending_prompt = (
                "Help me understand a document."
            )

    with col3:

        if st.button("💻 Help with Code", use_container_width=True):
            st.session_state.pending_prompt = (
                "Help me write or understand code."
            )

    with col4:

        if st.button("🌟 Explain a Topic", use_container_width=True):
            st.session_state.pending_prompt = (
                "Explain an interesting topic."
            )

# ==================================================
# WELCOME PANEL
# ==================================================

if (
    st.session_state.active_page == "Chat"
    and not st.session_state.messages
):

    with st.container(border=True):

        st.subheader("✨ Welcome to RRR AI Assistant!")

        st.write(
            "Ask questions, explore ideas, upload documents "
            "and use your AI assistant."
        )

        st.caption("Start a conversation below.")

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            if st.button("✨ Explain a topic", use_container_width=True):
                st.session_state.pending_prompt = (
                    "Explain an interesting topic."
                )

        with col2:

            if st.button("📚 Help me study", use_container_width=True):
                st.session_state.pending_prompt = (
                    "Help me study a topic."
                )

        col3, col4 = st.columns(2)

        with col3:

            if st.button("💻 Help me code", use_container_width=True):
                st.session_state.pending_prompt = (
                    "Help me with programming."
                )

        with col4:

            if st.button("💡 Generate ideas", use_container_width=True):
                st.session_state.pending_prompt = (
                    "Give me creative project ideas."
                )

# ==================================================
# HISTORY
# ==================================================

if st.session_state.active_page == "History":

    st.subheader("📜 Conversation History")

    if st.session_state.messages:

        for message in st.session_state.messages:

            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    else:

        st.info("No conversation history in this session.")

# ==================================================
# ABOUT
# ==================================================

elif st.session_state.active_page == "About":

    st.subheader("ℹ️ About RRR AI Assistant")

    st.markdown("""
    ## RRR AI Assistant

    An AI assistant from RRR AI Innovation Lab.

    ### Features

    - Generative AI conversations
    - Document assistance
    - Learning and explanations
    - Programming assistance
    - AI innovation

    ### Technologies

    - Python
    - Streamlit
    - Document processing
    - Generative AI
    """)

# ==================================================
# SETTINGS
# ==================================================

elif st.session_state.active_page == "Settings":

    st.subheader("⚙️ Settings")

    st.markdown("""
    ### Application Settings

    - Application: RRR AI Assistant
    - Theme: Dark navy and cyan
    - Documents: PDF, DOCX, TXT
    - AI engine: ai_engine.py
    """)

    if st.button("Clear Chat History"):

        st.session_state.messages = []
        st.rerun()

# ==================================================
# CHAT
# ==================================================

if st.session_state.active_page == "Chat":

    # DISPLAY PREVIOUS MESSAGES

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # CHAT INPUT

    prompt = st.chat_input("Ask RRR AI Assistant anything...")

    # QUICK ACTION

    if st.session_state.pending_prompt:

        prompt = st.session_state.pending_prompt
        st.session_state.pending_prompt = None

    # RESPONSE GENERATION

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

        st.rerun()

# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption("RRR AI Assistant • AI Innovation Lab")
