# ======================================================
#                    APP.PY - FULL APP
#           REAL RAG + MEMORY + AGENT + SEARCH
# ======================================================

import os
import json
from dotenv import load_dotenv

# ==============================
# Load .env
# ==============================
load_dotenv()

from openai import OpenAI
from pinecone import Pinecone
from serpapi import GoogleSearch
import gradio as gr

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ==============================
# Pinecone
# ==============================
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("youtube-chunks")

# ==============================
# MEMORY
# ==============================
conversation_history = []


# ======================================================
# RAG FUNCTIONS
# ======================================================
def retrieve_from_pinecone(query, k=3):
    query_embedding = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    ).data[0].embedding

    results = index.query(
        vector=query_embedding,
        top_k=k,
        include_metadata=True
    )

    contexts = [m.metadata["text_chunk"] for m in results.matches]
    return "\n\n".join(contexts)


def answer_question(query):
    """REAL RAG (same as notebook)"""
    context = retrieve_from_pinecone(query)

    # Build memory text
    memory_text = ""
    for turn in conversation_history[-5:]:
        memory_text += f"USER: {turn['question']}\nASSISTANT: {turn['answer']}\n\n"

    prompt = f"""
You are a helpful assistant answering questions about YouTube videos.

You have TWO sources:

1) Conversation Memory (for conversational continuity ONLY)
{memory_text}

2) Video Context (for factual information — ALWAYS use this for answering questions)
{context}

QUESTION: {query}

If the answer is not in the context but is in the conversation memory, use the memory.
If it is in neither, say: "The video does not explain this clearly."
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    answer = response.choices[0].message.content

    # Save memory
    conversation_history.append({"question": query, "answer": answer})

    return answer


# ======================================================
# INTERNET SEARCH TOOL
# ======================================================
def internet_search(query):
    params = {"q": query, "api_key": os.getenv("SERPAPI_KEY")}
    result = GoogleSearch(params).get_dict()

    if "organic_results" in result:
        return "\n".join([r.get("snippet", "") for r in result["organic_results"][:3]])

    return "No results found."


# ======================================================
# AGENT (same logic as notebook)
# ======================================================
def agent_with_search(query, rag_answer):
    global conversation_history

    # Build memory text again (agent also needs it)
    memory_text = ""
    for turn in conversation_history[-5:]:
        memory_text += f"USER: {turn['question']}\nASSISTANT: {turn['answer']}\n\n"

    # FOLLOW-UP DETECTION
    followups = [
        "give me an example", "another example",
        "previous", "what was the previous",
        "again", "repeat", "continue",
        "elaborate", "what did you say before"
    ]

    if any(f in query.lower() for f in followups):
        if conversation_history:
            last_answer = conversation_history[-1]["answer"]
            conversation_history.append({"question": query, "answer": last_answer})
            return last_answer, "MEMORY"

    # USE RAG IF RAG KNOWS
    if rag_answer.strip() != "The video does not explain this clearly.":
        return rag_answer, "RAG"

    # OTHERWISE USE INTERNET SEARCH AGENT
    tools = [{
        "type": "function",
        "function": {
            "name": "internet_search",
            "description": "Search online.",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"]
            }
        }
    }]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
             "content": "If RAG does not know answer, call internet_search and rewrite results."},
            {"role": "assistant", "content": f"MEMORY:\n{memory_text}"},
            {"role": "user", "content": query}
        ],
        tools=tools,
        tool_choice="auto"
    )

    msg = response.choices[0].message

    if msg.tool_calls:
        args = json.loads(msg.tool_calls[0].function.arguments)
        term = args.get("query", query)

        raw = internet_search(term)

        refined = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Rewrite search results into a clean answer."},
                {"role": "assistant", "content": raw},
                {"role": "user", "content": query}
            ]
        )

        final = refined.choices[0].message.content
        return final, "AGENT"

    return rag_answer, "FALLBACK"