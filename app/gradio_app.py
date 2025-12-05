import os
import gradio as gr

from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pinecone import Pinecone

# --- Load environment variables ---
from dotenv import load_dotenv
load_dotenv()

# --- Connect to Pinecone ---
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))

# --- Embeddings ---
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# --- Vectorstore ---
vectorstore = PineconeVectorStore(
    index=index,
    embedding=embeddings,
    text_key="text_chunk"
)

# --- LLM ---
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.2,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# --- Retriever ---
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# --- Prompt ---
template = """
You are a helpful assistant. Use the conversation history and the retrieved context
to answer the user's question.

Context:
{context}

Question:
{question}
If the answer is not in the context but is in the conversation memory, use the memory.
If it is in neither, say: "The video does not explain this clearly so I will explain it. An now write your explanation based on your knowledge."
Answer:
"""

prompt = ChatPromptTemplate.from_template(template)

# --- RAG chain ---
rag_chain = (
    {
        "context": retriever | RunnableLambda(
            lambda docs: "\n\n".join([doc.page_content for doc in docs])
        ),
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
)

# --- Chat function for Gradio ---
def answer_question(question):
    if question.strip() == "":
        return "Please enter a question."
    return rag_chain.invoke(question)

# --- Chat function using your RAG chain ---
# --- Custom CSS ---
custom_css = """
/* Animated background */
body, .gradio-container {
    margin: 0;
    padding: 0;
    height: 100%;
    background: #0d0d0d;
    overflow: hidden;
    position: relative;
}

/* Blob styles */
.blob {
    position: absolute;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle at 30% 30%, rgba(75,0,130,0.6), rgba(75,0,130,0.1));
    border-radius: 50%;
    animation: float 20s infinite ease-in-out;
    filter: blur(100px);
    opacity: 0.7;
}

/* Multiple blobs will move independently */
.blob:nth-child(2) {
    background: radial-gradient(circle at 30% 30%, rgba(255,0,128,0.6), rgba(255,0,128,0.1));
    width: 300px;
    height: 300px;
    animation-duration: 25s;
    top: 50%;
    left: 60%;
}
.blob:nth-child(3) {
    background: radial-gradient(circle at 30% 30%, rgba(0,255,255,0.5), rgba(0,255,255,0.1));
    width: 350px;
    height: 350px;
    animation-duration: 30s;
    top: 70%;
    left: 30%;
}

/* Float animation */
@keyframes float {
    0% { transform: translate(0, 0) scale(1); }
    50% { transform: translate(50px, -30px) scale(1.1); }
    100% { transform: translate(0, 0) scale(1); }
}

/* Chat container styling */
#chat_container { 
    background-color: rgba(26,26,26,0.9); 
    padding: 20px; 
    border-radius: 10px; 
    position: relative;
    z-index: 10;
}
.chat-box .message.user { 
    background-color: #333; color: white; border-radius: 15px; padding: 10px; margin: 5px 0;
}
.chat-box .message.assistant { 
    background-color: #2E2E2E; color: white; border-radius: 15px; padding: 10px; margin: 5px 0;
}
.input-box textarea { 
    border-radius: 8px; border: 1px solid #555; background-color: #222; color: white;
}
.submit-btn { 
    background-color: #4B0082; color: white; font-weight: bold; border-radius: 5px; padding: 8px 15px;
}
"""

# --- Custom JS ---
custom_js = """
<script>
// Press Enter to send message
document.addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        document.querySelector('button').click();
        e.preventDefault();
    }
});

// Add blob elements dynamically
for (let i = 0; i < 3; i++) {
    const blob = document.createElement('div');
    blob.className = 'blob';
    document.body.appendChild(blob);
}
</script>
"""

# --- Gradio Blocks layout ---
with gr.Blocks(title="ChainMind Chatbot") as demo:
    gr.Markdown("<h1 style='text-align:center; color:#4B0082;'>ChainMind</h1>"
                "<p style='text-align:center; color:#aaa;'>SYSTEM ONLINE</p>")
    with gr.Column(scale=1, elem_id="chat_container"):
        chat = gr.Chatbot(label="", height=400, elem_classes="chat-box")
        msg = gr.Textbox(placeholder="Type your question...", lines=2, elem_classes="input-box")
        submit = gr.Button("Send", elem_classes="submit-btn")
        state = gr.State([])

    msg.submit(chat_fn, [msg, state], [chat, msg, state])
    submit.click(chat_fn, [msg, state], [chat, msg, state])

# Launch with CSS + JS
demo.launch(css=custom_css, head=custom_js, share=True)

 gradio backup

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