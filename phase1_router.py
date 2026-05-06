import chromadb
from sentence_transformers import SentenceTransformer
import numpy as np

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize Chroma client
client = chromadb.Client()
collection = client.create_collection("bot_personas")


bot_personas = {
    "bot_a": """
    I strongly believe artificial intelligence, crypto, Elon Musk,
    automation, robotics, startups, and space exploration will solve
    human problems. I am highly optimistic about technology.
    """,

    "bot_b": """
    I believe tech monopolies, billionaires, surveillance capitalism,
    AI companies, and social media platforms are harming society.
    I care about privacy, ethics, and nature.
    """,

    "bot_c": """
    I focus on stock markets, trading algorithms, investing,
    interest rates, profits, finance, economics, and ROI.
    """
}


# Store persona embeddings
for bot_id, persona in bot_personas.items():
    embedding = model.encode(persona).tolist()

    collection.add(
        ids=[bot_id],
        embeddings=[embedding],
        documents=[persona]
    )


def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)

    return np.dot(vec1, vec2) / (
        np.linalg.norm(vec1) * np.linalg.norm(vec2)
    )


def route_post_to_bots(post_content, threshold=0.20):
    post_embedding = model.encode(post_content).tolist()

    results = collection.get(
        include=["embeddings", "documents"]
    )

    matched_bots = []

    for i, bot_id in enumerate(results["ids"]):
        bot_embedding = results["embeddings"][i]

        similarity = cosine_similarity(
            post_embedding,
            bot_embedding
        )

        print(f"{bot_id} similarity: {round(similarity,3)}")

        if similarity > threshold:
            matched_bots.append({
                "bot_id": bot_id,
                "similarity": round(similarity, 3)
            })

    return matched_bots


if __name__ == "__main__":
    post = "AI automation and Elon Musk are transforming the future of humanity."

    matches = route_post_to_bots(post)

    print("\nMatched Bots:")
    print(matches)