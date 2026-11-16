import chromadb


def retrieve_documents(query_embedding, n_results=5):

    client = chromadb.PersistentClient(
        path="./chroma_db"
    )

    collection = client.get_collection(
        name="claude_exam_guide"
    )

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    return results