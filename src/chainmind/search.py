import os
from serpapi import GoogleSearch


def internet_search(query):
    params = {"q": query, "api_key": os.getenv("SERPAPI_KEY")}
    result = GoogleSearch(params).get_dict()

    if "organic_results" in result:
        return "\n".join([r.get("snippet", "") for r in result["organic_results"][:3]])

    return "No results found."
