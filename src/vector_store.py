import chromadb


def store_embeddings(chunks, embeddings):

    client = chromadb.PersistentClient(
        path="./chroma_db"
    )

    collection = client.get_or_create_collection(
        name="claude_exam_guide"
    )

    collection.add(
        ids=[str(i) for i in range(len(chunks))],
        documents=[
            chunk.page_content
            for chunk in chunks
        ],
        embeddings=embeddings
    )

    return collection