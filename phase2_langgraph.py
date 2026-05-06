from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_core.tools import tool
import json
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# -------------------------
# LLM
# -------------------------
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.7,
    api_key=os.getenv("GROQ_API_KEY")
)

# -------------------------
# STATE
# -------------------------
class BotState(TypedDict):
    bot_id: str
    persona: str
    topic: str
    search_results: str
    post_content: str


# -------------------------
# MOCK SEARCH TOOL
# -------------------------
@tool
def mock_searxng_search(query: str):
    """
    Mock search tool that returns fake recent headlines
    based on user query keywords.
    """

    query = query.lower()

    if "crypto" in query:
        return "Bitcoin hits new all-time high amid ETF approvals."

    elif "ai" in query:
        return "OpenAI launches powerful coding model."

    elif "market" in query:
        return "Federal Reserve hints at rate cuts."

    elif "elon" in query:
        return "Elon Musk announces new SpaceX mission."

    return "No recent news found."


# -------------------------
# NODE 1: Decide Search Topic
# -------------------------
def decide_search(state):
    prompt = f"""
    You are a social media bot with this persona:

    {state['persona']}

    Choose ONLY a topic related to this persona.

    Examples:
    - AI
    - Crypto
    - Elon Musk
    - Automation

    Return ONLY the topic name.
    """

    topic = llm.invoke(prompt).content.strip()

    return {
        "topic": topic
    }


# -------------------------
# NODE 2: Web Search
# -------------------------
def web_search(state):
    results = mock_searxng_search.invoke(
        state["topic"]
    )

    return {
        "search_results": results
    }


# -------------------------
# NODE 3: Draft Post
# -------------------------
def draft_post(state):
    prompt = f"""
    Persona:
    {state['persona']}

    Topic:
    {state['topic']}

    Search Results:
    {state['search_results']}

    Generate a highly opinionated post under 280 characters.

    Return ONLY valid JSON in this exact format:

    {{
        "bot_id": "{state['bot_id']}",
        "topic": "...",
        "post_content": "..."
    }}
    """

    response = llm.invoke(prompt).content

    print("\nRaw LLM Response:")
    print(response)

    try:
        parsed_response = json.loads(response)
        return parsed_response

    except:
        return {
            "bot_id": state["bot_id"],
            "topic": state["topic"],
            "post_content": response
        }


# -------------------------
# BUILD GRAPH
# -------------------------
builder = StateGraph(BotState)

builder.add_node("decide_search", decide_search)
builder.add_node("web_search", web_search)
builder.add_node("draft_post", draft_post)

builder.set_entry_point("decide_search")

builder.add_edge("decide_search", "web_search")
builder.add_edge("web_search", "draft_post")
builder.add_edge("draft_post", END)

graph = builder.compile()


# -------------------------
# RUN GRAPH
# -------------------------
if __name__ == "__main__":
    result = graph.invoke({
        "bot_id": "bot_a",
        "persona": "I believe AI, crypto, automation, Elon Musk, and technology will solve human problems."
    })

    print("\nFinal Output:")
    print(json.dumps(result, indent=4))