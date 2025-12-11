# src/chainmind/rag.py

from openai import OpenAI
import os
from chainmind.retriever import retrieve_from_pinecone

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def answer_question(query, memory):
    """Your original answer_question logic, unchanged."""
    context = retrieve_from_pinecone(query)

    memory_text = memory.last_n_text()

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

    memory.add(query, answer)
    return answer
