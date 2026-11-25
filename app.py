
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
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>
.stApp {
    background-color: #07111F;
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
    border-radius: 12px;
    background: #10243B;
    color: #EAF6FF;
    border: 1px solid #087EAA;
    min-height: 42px;
    transition: 0.2s;
}

.stButton > button:hover {
    background: #087EAA;
    border: 1px solid #00E5FF;
    color: white;
}

[data-testid="stChatMessage"] {
    background: #10243B;
    border: 1px solid #164E73;
    border-radius: 16px;
    padding: 12px;
    margin-bottom: 12px;
}

[data-testid="stChatInput"] {
    border: 1px solid #00BCD4;
    border-radius: 16px;
}

[data-testid="stMetric"] {
    background: #10243B;
    border: 1px solid #164E73;
    border-radius: 12px;
    padding: 12px;
}

hr {
    border-color: #164E73;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# LOGO FUNCTION
# ==================================================

LOGO_FILE = "rrr_brain_logo.png"

def show_logo(width):
    try:
        st.image(LOGO_FILE, width=width)
    except Exception:
        st.markdown("## 🧠 RRR AI")
        st.caption("Upload rrr_brain_logo.png to GitHub")

# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    show_logo(180)

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
# MAIN HEADER WITH BRAIN LOGO
# ==================================================

header_logo, header_text = st.columns([1, 4])

with header_logo:
    show_logo(150)

with header_text:

    st.markdown("")

    st.title("RRR AI Assistant")

    st.markdown(
        "<span style='color:#00E5FF;'>"
        "AI Innovation • Smart Assistance"
        "</span>",
        unsafe_allow_html=True
    )

st.divider()

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
                "Explain an interesting topic to me."
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

            if st.button(
                "✨ Explain a topic",
                use_container_width=True
            ):
                st.session_state.pending_prompt = (
                    "Explain an interesting topic."
                )

        with col2:

            if st.button(
                "📚 Help me study",
                use_container_width=True
            ):
                st.session_state.pending_prompt = (
                    "Help me study a topic."
                )

        col3, col4 = st.columns(2)

        with col3:

            if st.button(
                "💻 Help me code",
                use_container_width=True
            ):
                st.session_state.pending_prompt = (
                    "Help me with programming."
                )

        with col4:

            if st.button(
                "💡 Generate ideas",
                use_container_width=True
            ):
                st.session_state.pending_prompt = (
                    "Give me creative project ideas."
                )

# ==================================================
# HISTORY PAGE
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
# ABOUT PAGE
# ==================================================

elif st.session_state.active_page == "About":

    st.subheader("ℹ️ About RRR AI Assistant")

    st.markdown("""
    ## RRR AI Assistant

    An AI assistant project from RRR AI Innovation Lab.

    ### Project goals

    - AI-powered conversations
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
# SETTINGS PAGE
# ==================================================

elif st.session_state.active_page == "Settings":

    st.subheader("⚙️ Settings")

    st.markdown("""
    ### Application Settings

    - **Application:** RRR AI Assistant
    - **Interface:** Dark navy and cyan theme
    - **Documents:** PDF, DOCX, TXT
    - **AI engine:** ai_engine.py
    """)

    if st.button("Clear Chat History"):

        st.session_state.messages = []
        st.rerun()

# ==================================================
# CHAT PAGE
# ==================================================

if st.session_state.active_page == "Chat":

    # DISPLAY CHAT HISTORY

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # CHAT INPUT

    prompt = st.chat_input(
        "Ask RRR AI Assistant anything..."
    )

    # QUICK ACTION PROMPTS

    if st.session_state.pending_prompt:

        prompt = st.session_state.pending_prompt
        st.session_state.pending_prompt = None

    # GENERATE RESPONSE

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
