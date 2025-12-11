# src/chainmind/retriever.py
import os
from openai import OpenAI
from pinecone import Pinecone

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("youtube-chunks")


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
