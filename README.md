# ChainMind
A self-training AI that digests Web3 videos and becomes a blockchain oracle.

ChainMind is a conversational AI Agent focused on **blockchain game development**. It uses a **RAG (Retrieval-Augmented Generation) pipeline** to answer questions based on video transcripts or documents stored in Pinecone, and provides a sleek, interactive UI via Gradio.


## Features

- Answer blockchain game development questions using RAG
- Uses Pinecone for vector search
- Embeddings via OpenAI (text-embedding-3-small)
- Chat interface built with Gradio (modern chat UI with dark theme)
- Maintains conversation memory across chat

---

## Installation

Follow these steps to set up and run ChainMind locally:

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/ChainMind.git
cd ChainMind
```
### 2. Create a virtual environment and activate it
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
`pip install -r requirements.txt`

### 4. Add your API keys
Create a `.env` file in the project root with the variables mentioned in `.env.example`

### 5. Run the chatbot
`python app/gradio_app.py`

The app will open locally at http://127.0.0.1:7860

You will also get a public shareable link via Gradio

---

## Technical Details

- **Vector Store:** Pinecone stores text chunks as vectors for semantic retrieval
- **Embeddings:** OpenAI `text-embedding-3-small`
- **LLM:** ChatOpenAI GPT-3.5-turbo for natural language responses
- **Prompting:** Uses `ChatPromptTemplate` with retrieved context and conversation history
- **Frontend:** Gradio Blocks
  - Chatbot component for conversations
  - Custom CSS for dark theme and floating blobs
  - JavaScript for dynamic background and key handling (Enter/Shift+Enter)
