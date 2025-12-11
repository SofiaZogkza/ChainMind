import os
import json
from openai import OpenAI
from chainmind.search import internet_search

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def agent_with_search(query, rag_answer, memory):
    memory_text = memory.last_n_text()

    followups = [
        "give me an example", "another example",
        "previous", "what was the previous",
        "again", "repeat", "continue",
        "elaborate", "what did you say before"
    ]

    # FOLLOW-UP DETECTION
    if any(f in query.lower() for f in followups):
        last = memory.last_answer()
        if last:
            memory.add(query, last)
            return last, "MEMORY"

    # RAG WORKED
    if rag_answer.strip() != "The video does not explain this clearly.":
        return rag_answer, "RAG"

    # TOOL CALL
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
