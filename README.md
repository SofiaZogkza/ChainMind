# ChainMind
A self-training AI Tutornthat digests Web3 videos and becomes a blockchain oracle.

ChainMind is a conversational AI Agent focused on **blockchain game development**. It uses a **RAG (Retrieval-Augmented Generation) pipeline** to answer questions based on video transcripts or documents stored in Pinecone, and provides a sleek, interactive UI via Gradio.


## Features

- Answer blockchain game development questions using RAG
- Uses Pinecone for vector search
- Embeddings via OpenAI (text-embedding-3-small)
- Chat interface built with Gradio (modern chat UI with dark theme)
- Maintains conversation memory across chat
- Agent chooses between RAG, memory, and internet search (SerpAPI) based on logic

---

## 🔧 Setup Instructions

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

### 5. Offline Pipeline
Run the `notebooks/main_phase_1_data.ipynb` (✔ loads youtube videos - ✔ cleans )
Run the `notebooks/main_phase_2_rag.ipynb`(✔ Chunks - Embeds - Upsert to Pinecone ✔ Produces rag_dataset.json)
Run the `notebooks/main_phase_3_QA.ipynb` (✔ Tests RAG pipeline ✔ Tests agent logic ✔ Verifies follow-up memory behavior)

### 6. Run the Chatbot

Option 1 - Gradio:

`python app/gradio_app2.py`

The app will open locally at http://127.0.0.1:7860

You will also get a public shareable link via Gradio

Option 2 Streamlit:

`venv/bin/python -m streamlit run app/app_streamlit.py`

The app will load automatically locally in `http://localhost:8502/`

---

## Technical Details

- **Vector Store:** Pinecone stores text chunks as vectors for semantic retrieval
- **Embeddings:** OpenAI `text-embedding-3-small`
- **LLM:** ChatOpenAI `GPT-3.5-turbo` for natural language responses
- **Agent** Agent `gpt-4o-mini`
- **Tools** SerpAPI live Google results
- **Prompting:** Uses `ChatPromptTemplate` with retrieved context and conversation history
- **Memory** Custom | 5 last QA entries stored as conversational context
- **Frontend:** Gradio Blocks
  - Chatbot component for conversations
  - Custom CSS for dark theme and floating blobs
  - JavaScript for dynamic background and key handling (Enter/Shift+Enter)

---

## Architectural Diagram



<img src="assets/diagram.png" width="600" />



---
---

## 📌 Next Steps (Future Enhancements for v2)

- Add multimodal support (images - video frames - audio)

- Improve memory architecture (vector-based memory)

- Add guardrails & hallucination detection

- Deploy on AWS/GCP with HTTPS + scaling

- Improve UI styling (animations, themes, branding)

- Add user authentication for personalized history

- 👉 **See the full roadmap here:** [ROADMAP.md](./ROADMAP.md)
