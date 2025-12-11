import gradio as gr
from rag_agent import answer_question, agent_with_search, conversation_history


# ---------------------------------------------------------
# CHAT FUNCTION
# ---------------------------------------------------------
def chat_fn(user_input, history):
    rag = answer_question(user_input)
    final, source = agent_with_search(user_input, rag)

    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant",
                    "content": f"<div class='tag'>[{source}]</div><br>{final}"})

    return history, ""


# ---------------------------------------------------------
# CUSTOM CSS (FULL CYBER NEON THEME)
# ---------------------------------------------------------
custom_css = """
/* GLOBAL ------------------------------------------------------ */
body, .gradio-container {
    background: #0b0b0f !important;
    color: #e6e6e6 !important;
    font-family: 'Inter', sans-serif;
}

/* BRAND TITLE ------------------------------------------------- */
#title h1 {
    font-size: 3rem;
    text-align: center;
    font-weight: 800;
    background: linear-gradient(90deg, #b57bff, #9a5bff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: -10px;
}

#subtitle p {
    text-align: center;
    color: #9a9a9a;
    margin-bottom: 30px;
}

/* FLOATING BLOBS --------------------------------------------- */
.blob {
    position: fixed;
    width: 450px;
    height: 450px;
    filter: blur(140px);
    border-radius: 50%;
    opacity: 0.45;
    z-index: -1;
    animation: float 22s infinite ease-in-out;
}

#blob1 { background: #7f00ff; top: 10%; left: 60%; }
#blob2 { background: #ff0095; top: 50%; left: 10%; animation-duration: 28s; }
#blob3 { background: #00eaff; top: 70%; left: 70%; animation-duration: 34s; }

@keyframes float {
    0%   { transform: translate(0, 0) scale(1); }
    50%  { transform: translate(40px, -30px) scale(1.1); }
    100% { transform: translate(0, 0) scale(1); }
}

/* CHATBOT CONTAINER ------------------------------------------ */
.gr-chatbot {
    background: rgba(255,255,255,0.03) !important;
    border-radius: 14px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
}

/* CHAT BUBBLES ------------------------------------------------ */
.message.user .message-content {
    background: #6d28d9 !important;
    color: white !important;
    border-radius: 12px !important;
    padding: 10px 14px !important;
    font-size: 15px !important;
}

.message.bot .message-content {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 12px !important;
    padding: 12px !important;
    backdrop-filter: blur(6px);
    font-size: 15px !important;
}

.tag {
    display: inline-block;
    padding: 2px 8px;
    background: #b57bff;
    color: #0b0b0f;
    border-radius: 6px;
    font-size: 11px;
    font-weight: bold;
}

/* INPUT BOX --------------------------------------------------- */
#input-box textarea {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    color: white !important;
    border-radius: 10px !important;
}

/* BUTTONS ----------------------------------------------------- */
button {
    background: linear-gradient(90deg, #9a5bff, #b57bff) !important;
    color: white !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    border: none !important;
    padding: 10px !important;
}

button:hover {
    opacity: 0.9;
}
"""


# ---------------------------------------------------------
# CUSTOM JS (ADD FLOATING BLOBS)
# ---------------------------------------------------------
custom_js = """
<script>
window.onload = () => {
    const blob1 = document.createElement('div');
    const blob2 = document.createElement('div');
    const blob3 = document.createElement('div');
    blob1.className = 'blob'; blob1.id = 'blob1';
    blob2.className = 'blob'; blob2.id = 'blob2';
    blob3.className = 'blob'; blob3.id = 'blob3';
    document.body.appendChild(blob1);
    document.body.appendChild(blob2);
    document.body.appendChild(blob3);
};
</script>
"""


# ---------------------------------------------------------
# BUILD THE UI
# ---------------------------------------------------------
with gr.Blocks(title="ChainMind Chatbot") as demo:

    gr.HTML("<div id='title'><h1>ChainMind</h1></div>")
    gr.HTML("<div id='subtitle'><p>SYSTEM ONLINE</p></div>")

    chat = gr.Chatbot(height=450)

    msg = gr.Textbox(
        label="",
        placeholder="Ask a question about blockchain game development...",
        elem_id="input-box"
    )

    with gr.Row():
        send_btn = gr.Button("Send")
        clear_btn = gr.Button("Clear")

    msg.submit(chat_fn, inputs=[msg, chat], outputs=[chat, msg])
    send_btn.click(chat_fn, inputs=[msg, chat], outputs=[chat, msg])
    clear_btn.click(lambda: ([], ""), None, [chat, msg])


# ---------------------------------------------------------
# LAUNCH (IMPORTANT: CSS/JS GO HERE)
# ---------------------------------------------------------
demo.launch(css=custom_css, head=custom_js, share=True)
