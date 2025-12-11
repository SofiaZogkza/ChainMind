# ChainMind Roadmap

This roadmap outlines the planned features, improvements, and long-term vision for ChainMind, the multimodal AI tutor that learns from YouTube videos and answers questions using Retrieval-Augmented Generation, conversational memory, and agent reasoning.

### 📌 Phase 1 — Foundation (Completed)

Establish the core pipeline and minimal viable product.

#### ✅ Data Extraction & Processing

- Extract YouTube transcripts using VTT parsing
- Clean and normalize text
- Chunk transcripts for embeddings
- Generate metadata (title, start/end times)

#### ✅ Vector Database (Pinecone)

- Store embeddings
- Set up a performant retriever (k=3)
- Build RAG pipeline

#### ✅ Base Chatbot Engine

- RAG → Memory → Agent → Fallback chain
- Gradio chat interface
- Basic system prompts

---

### 📌 Phase 2 — Improvements & Stability (Current Focus)
#### 🔧 1. Codebase Refactoring

Move notebook logic into a clean src/chainmind/ module

Create reusable components:

( eg. retriever.py, rag_engine.py, agent.py, memory.py, utils/ )

Add type hints & error handling

#### 📘 2. Documentation

Improve README.md
Add Tutorials ("Add a new Youtube video"...)

#### 🧪 3. Testing & Quality

- Add unit tests for the RAG chain
- Add integration tests for the agen
- Introduce linting (ruff, flake8, black)

#### 🎨 4. UI / UX Enhancements

- Better Gradio layout. Maybe proper UI.
- Add video selector or dataset info
- Add response categories (RAG / Memory / Agent / Fallback indicator)

---

### 📌  Phase 3 — Multimodal Upgrade

#### 1. Audio & Video Features

- Integrate Whisper for audio transcription
- Add image frames or video thumbnails to context
- Allow users to upload custom videos

#### 2. Visual Retrieval

- Extract keyframes and embed with CLIP
- Support multimodal RAG (text + image)

#### 3. Timeline Navigation

- “Jump to moment in video” links
- Display timestamps in answers

---

### 📌 Phase 4 — AI Agent Evolution

#### 1. Smarter Reasoning

Add tool for:
- Code execution (Python REPL)
- Web search w/ ranking
- Wallet or blockchain API queries (optional future)

#### 2. Retrieval Optimization

- Multi-query retrieval
- Re-ranking model (ColBERT / Cohere reranker)

#### 3. Memory System V2

- Long-term memory store
- Automatic summarization
- Topic clustering

----

# ☁️ Phase 5 — Deployment & Production

#### 📦 1. Packaging

Publish Python package:
pip install chainmind

Add PyPI readme + metadata

#### 🐳 2. Docker Support

- Dockerfile + docker-compose for:
- App
- Pinecone proxy (optional)

#### 🌍 3. Cloud Deployment

Deploy on:
- AWS Lambda + API Gateway
- HuggingFace Spaces

#### 📊 4. Monitoring

- Logging, tracing, and retrieval analytics
- Evaluation dashboard

---

# 🤝 Phase 6 — Community Features

#### 👥 Contributions

- Add “good first issues”
- Add templates:
    - Bug report
    - Feature request
    - Pull request template

#### 📖 Documentation Website

- Use MkDocs or Docusaurus

- Host via GitHub Pages

#### 🔌 Plugin Ecosystem

- Allow custom tools for the agent

- Allow custom embedding models

- Allow custom vector DB backends

---
---
---

##  📌  Hallucination Detection & Evaluation

### 🎯 Goals  
Improve answer reliability by ensuring the chatbot’s responses are grounded in retrieved video context, reducing unsupported claims and inconsistencies.

---

### 📌 Planned Features

#### **1. Post-Answer Faithfulness Check**
Implement a verification step after each response:
- LLM compares the answer with the retrieved context  
- Labels output as: **supported**, **partially supported**, or **unsupported**  
- If “unsupported”:  
  - Retry retrieval  
  - Or return “I don’t have enough information to answer this.”

---

#### **2. Multi-Query Retrieval**
Improve recall by generating multiple versions of the user question:
- Create 3–5 reformulated queries  
- Retrieve results for each  
- Merge and deduplicate context before passing to the RAG model  

This reduces context gaps and improves answer grounding.

---

#### **3. Reranking Layer**
Introduce a reranking step for retrieved documents:
- Use cross-encoder or reranking models such as:  
  - Cohere Reranker  
  - SentenceTransformer Cross-Encoder  
  - BGE Reranker  
- Select only the top, most relevant chunks as final RAG context  

This significantly reduces hallucinations caused by weak retrieval.

---

#### **4. Deterministic RAG Testing & Benchmarking**
Create an offline evaluation workflow to measure hallucination frequency:
- Build a fixed set of test questions  
- Compare output across multiple runs  
- Detect inconsistent answers or unsupported claims  
- Store results in `evaluation/results/`  

This helps track improvements over time and evaluate model versions.

---

#### **5. Confidence Score in UI (Optional)**
Display the model’s confidence based on context verification:
- **High confidence** → fully supported  
- **Medium confidence** → partially supported  
- **Low confidence** → unsupported (possible hallucination)  

This increases transparency and user trust.

---

### ⭐ Expected Impact
- Higher factual accuracy  
- More stable and predictable answers  
- Reduced hallucinations from both RAG and the agent  
- Better debugging capability  
- Foundation for future improvements like feedback loops, reinforcement learning, or model fine-tuning  
