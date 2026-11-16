from langchain_community.document_loaders import PyPDFLoader
from src.chunking import create_chunks
from src.embeddings import get_embedding_model
from src.vector_store import store_embeddings
from src.retrieval import retrieve_documents
from src.llm import get_llm

from prompts.qa_prompt import QA_PROMPT


def initialize_rag():
    loader = PyPDFLoader("data/sample.pdf")
    documents = loader.load()

    chunks = create_chunks(documents)

    embedding_model = get_embedding_model()

    embeddings = embedding_model.embed_documents(
        [chunk.page_content for chunk in chunks]
    )

    collection = store_embeddings(
        chunks,
        embeddings
    )

    return embedding_model, collection


def ask_question(question, embedding_model):

    query_embedding = embedding_model.embed_query(
        question
    )

    results = retrieve_documents(
        query_embedding
    )

    print("\n" + "=" * 80)
    print("TOP RETRIEVED CHUNKS")
    print("=" * 80)

    for i, chunk in enumerate(results["documents"][0], start=1):
        print(f"\n\n----- CHUNK {i} -----")
        print(chunk[:1000])  # First 1000 characters

    context = "\n\n".join(
        results["documents"][0]
    )

    llm = get_llm()

    prompt = QA_PROMPT.format(
        context=context,
        question=question
    )

    response = llm.invoke(prompt)

    return response.content