from pathlib import Path
import chromadb


# Project paths
KNOWLEDGE_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "knowledge_base.txt"
)

CHROMA_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "chroma"
)


def load_knowledge():
    """Load the customer-support knowledge base."""

    if not KNOWLEDGE_FILE.exists():
        raise FileNotFoundError(
            f"Knowledge base not found: {KNOWLEDGE_FILE}"
        )

    return KNOWLEDGE_FILE.read_text(
        encoding="utf-8"
    )


def create_chunks(text):
    """Split the knowledge base into meaningful sections."""

    sections = text.split("\n## ")

    chunks = []

    for i, section in enumerate(sections):
        section = section.strip()

        if not section:
            continue

        # Add the heading back for sections after the first one
        if i > 0:
            section = "## " + section

        chunks.append(section)

    return chunks


def get_collection():
    """Create or load the ChromaDB collection."""

    client = chromadb.PersistentClient(
        path=str(CHROMA_PATH)
    )

    collection = client.get_or_create_collection(
        name="customer_support_knowledge"
    )

    return collection


def build_knowledge_base():
    """Load, chunk, and store the knowledge base in ChromaDB."""

    text = load_knowledge()

    chunks = create_chunks(text)

    collection = get_collection()

    ids = [
        f"chunk_{i}"
        for i in range(len(chunks))
    ]

    collection.upsert(
        ids=ids,
        documents=chunks
    )

    return len(chunks)


if __name__ == "__main__":
    count = build_knowledge_base()

    print("Knowledge base created successfully.")
    print(f"Chunks stored: {count}")