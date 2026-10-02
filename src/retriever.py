from src.knowledge_base import get_collection


def search_knowledge(query, top_k=3):
    """
    Search the customer-support knowledge base
    for information relevant to the user's query.
    """

    if not query or not query.strip():
        return []

    collection = get_collection()

    results = collection.query(
        query_texts=[query.strip()],
        n_results=top_k
    )

    documents = results.get("documents", [[]])[0]

    return documents


if __name__ == "__main__":
    query = input("Enter a support question: ")

    results = search_knowledge(query)

    print("\nRelevant Knowledge:\n")

    for i, document in enumerate(results, start=1):
        print(f"--- Result {i} ---")
        print(document)
        print()