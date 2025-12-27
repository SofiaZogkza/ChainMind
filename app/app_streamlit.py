import streamlit as st
import sys
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Make src folder importable
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

# Import backend logic
from chainmind.memory import ConversationMemory
from chainmind.rag import answer_question
from chainmind.agent import agent_with_search


# =========================================================
# SESSION STATE INITIALIZATION
# =========================================================
if "memory" not in st.session_state:
    st.session_state.memory = ConversationMemory()

if "history" not in st.session_state:
    st.session_state.history = []

if "clear_input" not in st.session_state:
    st.session_state.clear_input = False

if "pending_message" not in st.session_state:
    st.session_state.pending_message = None

# Clear the input box on next rerun
if st.session_state.clear_input:
    st.session_state.input_box = ""
    st.session_state.clear_input = False


# =========================================================
# STREAMLIT PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="ChainMind Chatbot",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# =========================================================
# CUSTOM NEON CSS
# =========================================================
st.markdown(
    """
<style>

body {
    background-color: #0b0b0f;
    color: #e6e6e6;
}

/* Title */
h1 {
    text-align: center;
    font-size: 3rem;
    background: linear-gradient(90deg, #b57bff, #9a5bff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* USER BUBBLE - RIGHT */
.user-bubble-wrapper {
    display: flex;
    justify-content: flex-end;
    margin: 10px 0;
}
.user-bubble {
    background: linear-gradient(135deg, #8c52ff, #6a00ff);
    padding: 14px 18px;
    border-radius: 14px;
    max-width: 70%;
    color: white;
    font-size: 15px;
    box-shadow: 0 0 18px rgba(140, 82, 255, 0.7);
}

/* BOT BUBBLE - LEFT */
.bot-bubble-wrapper {
    display: flex;
    justify-content: flex-start;
    margin: 10px 0;
}
.bot-bubble {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.2);
    padding: 14px 18px;
    border-radius: 14px;
    max-width: 70%;
    font-size: 15px;
    backdrop-filter: blur(6px);
    box-shadow: 0 0 18px rgba(0, 200, 255, 0.4);
}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# TITLE
# =========================================================
st.title("🤖 ChainMind Chatbot")
st.subheader("Blockchain Game Development Assistant")


# =========================================================
# STREAMING GENERATOR
# =========================================================
def stream_output(text):
    """Yield the response word-by-word."""
    for word in text.split():
        yield word + " "
        time.sleep(0.03)  # speed of streaming


# =========================================================
# CHAT LOGIC WITH STREAMING
# =========================================================
def chat_fn(user_input):
    placeholder = st.empty()

    rag = answer_question(user_input, st.session_state.memory)
    final, source = agent_with_search(user_input, rag, st.session_state.memory)

    full_message = f"[{source}] {final}"
    streamed_text = ""

    for chunk in stream_output(full_message):
        streamed_text += chunk
        placeholder.markdown(
            f"""
            <div class="bot-bubble-wrapper">
                <div class="bot-bubble">🤖 {streamed_text}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.session_state.history.append(("assistant", full_message))


# =========================================================
# PROCESS ENTER KEY SUBMISSION
# =========================================================
if st.session_state.pending_message:
    msg = st.session_state.pending_message
    st.session_state.pending_message = None

    # append user message FIRST
    st.session_state.history.append(("user", msg))

    st.session_state.clear_input = True
    chat_fn(msg)

# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================
for role, msg in st.session_state.history:
    if role == "user":
        st.markdown(
            f"""
            <div class="user-bubble-wrapper">
                <div class="user-bubble">🧑‍💻 {msg}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div class="bot-bubble-wrapper">
                <div class="bot-bubble">🤖 {msg}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# INPUT BOX
# =========================================================
user_input = st.text_input(
    "Ask a question about blockchain game development:",
    key="input_box",
    on_change=lambda: st.session_state.update(
        {"pending_message": st.session_state.input_box}
    )
)


# =========================================================
# BUTTONS (SIDE BY SIDE)
# =========================================================
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("Send"):
        if user_input.strip():
            st.session_state.pending_message = user_input
            st.session_state.clear_input = True
            st.rerun()

with col2:
    if st.button("Clear"):
        st.session_state.history = []
        st.session_state.clear_input = True
        st.rerun()
