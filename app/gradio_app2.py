# ======================================================
#                gradio_app.py
#         UI for RAG + Agent Chatbot
# ======================================================

import gradio as gr
from rag_agent import answer_question, agent_with_search, conversation_history


def chat_fn(user_input, history):
    rag = answer_question(user_input)
    final, source = agent_with_search(user_input, rag)

    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": f"**[{source}]**\n\n{final}"})

    return history, ""


with gr.Blocks(title="ChainMind Chatbot") as demo:
    gr.Markdown("<h1 style='text-align:center; color:#4B0082;'>ChainMind</h1>"
                "<p style='text-align:center; color:#aaa;'>SYSTEM ONLINE</p>")

    chat = gr.Chatbot(label="", height=400, elem_classes="chat-box")
    msg = gr.Textbox(label="Ask a question...")
    clear = gr.Button("Clear")

    msg.submit(chat_fn, [msg, chat], [chat, msg])
    clear.click(lambda: ([], ""), None, [chat, msg])

demo.launch(share=True)

# ======================================================
# with gr.Blocks(title="ChainMind Chatbot") as demo:
#     gr.Markdown("<h1 style='text-align:center; color:#4B0082;'>ChainMind</h1>"
#                 "<p style='text-align:center; color:#aaa;'>SYSTEM ONLINE</p>")
#     with gr.Column(scale=1, elem_id="chat_container"):
#         chat = gr.Chatbot(label="", height=400, elem_classes="chat-box")
#         msg = gr.Textbox(placeholder="Type your question...", lines=2, elem_classes="input-box")
#         submit = gr.Button("Send", elem_classes="submit-btn")
#         state = gr.State([])

#     msg.submit(chat_fn, [msg, state], [chat, msg, state])
#     submit.click(chat_fn, [msg, state], [chat, msg, state])

# # Launch with CSS + JS
# demo.launch(css=custom_css, head=custom_js, share=True)