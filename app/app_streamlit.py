import streamlit as st
import sys
import os
from dotenv import load_dotenv

load_dotenv()

# Add src folder to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from chainmind.memory import ConversationMemory
from chainmind.rag import answer_question
from chainmind.agent import agent_with_search


# ---------------------------------------------------------
# INITIALIZE SESSION STATE
# ---------------------------------------------------------
if "memory" not in st.session_state:
    st.session_state.memory = ConversationMemory()

if "history" not in st.session_state:
    st.session_state.history = []

# Flags for input clearing + pending messages
if "clear_input" not in st.session_state:
    st.session_state.clear_input = False

if "pending_message" not in st.session_state:
    st.session_state.pending_message = None


# If we flagged the input to clear, clear BEFORE rendering widget:
if st.session_state.clear_input:
    st.session_state.input_box = ""
    st.session_state.clear_input = False


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="ChainMind Chatbot",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------
# CUSTOM CSS (NEON THEME)
# ---------------------------------------------------------
st.markdown(
    """
<style>

body {
    background-color: #0b0b0f;
    color: #e6e6e6;
}

/* TITLE */
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

# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------
st.title("🤖 ChainMind Chatbot")
st.subheader("Blockchain Game Development Assistant")


# ---------------------------------------------------------
# PROCESS MESSAGE
# ---------------------------------------------------------
def chat_fn(user_input):
    rag = answer_question(user_input, st.session_state.memory)
    final, source = agent_with_search(user_input, rag, st.session_state.memory)

    st.session_state.history.append(("user", user_input))
    st.session_state.history.append(("assistant", f"[{source}] {final}"))


# If Enter was pressed (pending_message exists)
if st.session_state.pending_message:
    chat_fn(st.session_state.pending_message)
    st.session_state.pending_message = None
    st.session_state.clear_input = True
    st.rerun()


# ---------------------------------------------------------
# DISPLAY CHAT HISTORY
# ---------------------------------------------------------
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


# ---------------------------------------------------------
# INPUT BOX
# ---------------------------------------------------------
user_input = st.text_input(
    "Ask a question about blockchain game development:",
    key="input_box",
    on_change=lambda: st.session_state.update(
        {"pending_message": st.session_state.input_box}
    )
)

# ---------------------------------------------------------
# BUTTONS (aligned horizontally)
# ---------------------------------------------------------
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
