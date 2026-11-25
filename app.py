
import streamlit as st

from ai_engine import generate_response
from document_processor import prepare_document, search_documents

# ==================================================
# PAGE CONFIGURATION
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
    border-radius: 12px;
    background: #10243B;
    color: #EAF6FF;
    border: 1px solid #087EAA;
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
# SIDEBAR
# ==================================================

with st.sidebar:

    try:
        st.image("rrr_logo_808x808_edited.jpg", width=180)
    except Exception:
        st.markdown("# 🧠 RRR AI")

    st.markdown("## RRR AI")
    st.caption("AI Innovation • Smart Assistance")

    st.divider()

    if st.button("➕ New Chat", use_container_width=True):

        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.session_state.active_page = "Chat"

        st.rerun()

    st.divider()

    # NAVIGATION

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

    # DOCUMENTS

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

            st.success("Documents processed!")

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
# TOP HEADER
# ==================================================

st.markdown("""
<div style="
    background: linear-gradient(120deg, #0D1B2E, #003F5C, #087EAA);
    border: 1px solid #00BCD4;
    border-radius: 22px;
    padding: 35px 20px;
    text-align: center;
    box-shadow: 0 0 25px rgba(0,188,212,0.12);
">

    <h1 style="
        font-size: 42px;
        color: white;
        margin-bottom: 8px;
    ">
        RRR <span style="color:#00E5FF;">AI Assistant</span>
    </h1>

    <p style="
        font-size: 18px;
        color: #C8E9FF;
    ">
        AI Innovation • Smart Assistance
    </p>

</div>
""", unsafe_allow_html=True)

st.write("")

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

    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #10243B, #071B30);
        border: 1px solid #087EAA;
        border-radius: 20px;
        padding: 28px;
        margin-top: 20px;
    ">

        <h2 style="color:#00E5FF;">
            Welcome to RRR AI Assistant!
        </h2>

        <p style="font-size:17px;color:#D7EFFF;">
            Ask questions, explore ideas, upload documents
            and use your AI assistant.
        </p>

        <p style="color:#9DC8E5;">
            Start a conversation below.
        </p>

    </div>
    """, unsafe_allow_html=True)

    st.write("")

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

        for i, message in enumerate(st.session_state.messages):

            role = message["role"].capitalize()

            st.markdown(
                f"**{role}:** {message['content']}"
            )

            st.divider()

    else:

        st.info("No conversation history in this session yet.")

# ==================================================
# ABOUT PAGE
# ==================================================

elif st.session_state.active_page == "About":

    st.subheader("ℹ️ About RRR AI Assistant")

    st.markdown("""
    **RRR AI Assistant** is an AI assistant project
    developed as part of RRR AI Innovation Lab.

    ### Project goals

    - AI-powered conversations
    - Document assistance
    - Learning and explanations
    - Programming assistance
    - AI innovation and experimentation

    ### Technology

    - Python
    - Streamlit
    - Document processing
    - Generative AI integration (planned)

    """)

# ==================================================
# SETTINGS PAGE
# ==================================================

elif st.session_state.active_page == "Settings":

    st.subheader("⚙️ Settings")

    st.markdown("""
    ### RRR AI Assistant Settings

    **Application:** RRR AI Assistant

    **Interface:** Dark futuristic theme

    **Document formats:** PDF, DOCX, TXT

    **AI provider:** Not yet connected to a
    generative model in this version.
    """)

    if st.button("Clear Chat History"):

        st.session_state.messages = []
        st.rerun()

# ==================================================
# CHAT PAGE
# ==================================================

if st.session_state.active_page == "Chat":

    # DISPLAY MESSAGES

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    # CHAT INPUT

    prompt = st.chat_input(
        "Ask RRR AI Assistant anything..."
    )

    # QUICK ACTION PROMPT

    if st.session_state.pending_prompt:

        prompt = st.session_state.pending_prompt

        st.session_state.pending_prompt = None

    # PROCESS PROMPT

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

st.markdown("""
<div style="
    text-align:center;
    padding:20px;
    color:#5E8BAA;
">
    RRR AI Assistant • AI Innovation Lab
</div>
""", unsafe_allow_html=True)
