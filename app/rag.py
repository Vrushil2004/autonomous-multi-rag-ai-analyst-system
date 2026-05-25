from pathlib import Path
from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from app.utils import clean_text

# =========================================================
# Vector Store Configuration
# =========================================================

VECTOR_DB_PATH = "data/processed/faiss_index"

Path(VECTOR_DB_PATH).mkdir(parents=True, exist_ok=True)

# =========================================================
# Embedding Model Configuration
# =========================================================

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# =========================================================
# Text Splitter Configuration
# =========================================================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150,
    separators=["\n\n", "\n", ".", " ", ""],
)

# =========================================================
# Document Processing Pipeline
# =========================================================

def process_document(file_path: str) -> None:
    """
    Process enterprise documents and store
    embeddings into FAISS vector database.

    Steps:
    1. Load document
    2. Clean text
    3. Chunk text
    4. Generate embeddings
    5. Save FAISS index
    """

    # -----------------------------------------------------
    # Step 1: Load PDF
    # -----------------------------------------------------

    loader = PyPDFLoader(file_path)
    documents = loader.load()

    # -----------------------------------------------------
    # Step 2: Clean document text
    # -----------------------------------------------------

    for document in documents:
        document.page_content = clean_text(
            document.page_content
        )

    # -----------------------------------------------------
    # Step 3: Split documents into chunks
    # -----------------------------------------------------

    chunks = text_splitter.split_documents(documents)

    # -----------------------------------------------------
    # Step 4: Create FAISS vector store
    # -----------------------------------------------------

    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embedding_model,
    )

    # -----------------------------------------------------
    # Step 5: Save FAISS index locally
    # -----------------------------------------------------

    vector_store.save_local(VECTOR_DB_PATH)


# =========================================================
# Vector Store Loader
# =========================================================

def load_vector_store() -> FAISS:
    """
    Load FAISS vector database from disk.
    """

    vector_store = FAISS.load_local(
        VECTOR_DB_PATH,
        embeddings=embedding_model,
        allow_dangerous_deserialization=True,
    )

    return vector_store


# =========================================================
# Semantic Retrieval Pipeline
# =========================================================

def retrieve_context(
    query: str,
    top_k: int = 3,
) -> str:
    """
    Retrieve semantically relevant document chunks.

    Args:
        query: User query
        top_k: Number of retrieved chunks

    Returns:
        Combined retrieved context
    """

    # -----------------------------------------------------
    # Load Vector Store
    # -----------------------------------------------------

    vector_store = load_vector_store()

    # -----------------------------------------------------
    # Similarity Search
    # -----------------------------------------------------

    retrieved_documents = vector_store.similarity_search(
        query=query,
        k=top_k,
    )

    # -----------------------------------------------------
    # Combine Retrieved Context
    # -----------------------------------------------------

    combined_context = "\n\n".join(
        [
            document.page_content
            for document in retrieved_documents
        ]
    )

    return combined_context


# =========================================================
# Multi-Query Retrieval
# =========================================================

def retrieve_multiple_contexts(
    queries: List[str],
    top_k: int = 2,
) -> List[str]:
    """
    Retrieve contexts for multiple
    planner-generated subqueries.
    """

    contexts = []

    for query in queries:

        context = retrieve_context(
            query=query,
            top_k=top_k,
        )

        contexts.append(context)

    return contexts