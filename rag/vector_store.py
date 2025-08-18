import chromadb
from typing import List, Dict, Union
from core.model_provider import embedding_model

# Define Document type
Document = Dict[str, Union[str, Dict]]

# Initialize ChromaDB client
# Using persistent storage
client = chromadb.PersistentClient(path="chroma_db")

def create_vector_store(documents: List[Document], collection_name: str = "default_collection") -> chromadb.Collection:
    """
    Creates a vector store, vectorizes the documents, and stores them.

    Args:
        documents (List[Document]): A list of document chunks to process.
        collection_name (str): The name of the collection to create in ChromaDB.

    Returns:
        chromadb.Collection: The created or retrieved collection object.
    """
    if not embedding_model:
        raise RuntimeError("Embedding model is not available. Check your OPENAI_API_KEY.")

    # Get or create a collection
    collection = client.get_or_create_collection(name=collection_name)

    # Prepare data for the collection
    ids = [f"doc_{i}" for i in range(len(documents))]
    contents = [doc["page_content"] for doc in documents]
    metadatas = [doc["metadata"] for doc in documents]

    # Use the OpenAIEmbeddings model to create embeddings in batches
    print(f"Creating embeddings for {len(contents)} documents...")
    embeddings = embedding_model.embed_documents(contents)
    print("Embeddings created successfully.")

    # Add data to the collection
    collection.add(
        embeddings=embeddings,
        documents=contents,
        metadatas=metadatas,
        ids=ids
    )
    
    return collection

def search_vector_store(query: str, collection: chromadb.Collection, n_results: int = 3) -> List[Document]:
    """
    Performs a similarity search in the vector store.

    Args:
        query (str): The user's query string.
        collection (chromadb.Collection): The collection to search in.
        n_results (int): The number of results to return.

    Returns:
        List[Document]: A list of documents containing the search results.
    """
    if not embedding_model:
        raise RuntimeError("Embedding model is not available. Check your OPENAI_API_KEY.")

    # Vectorize the query text
    query_embedding = embedding_model.embed_query(query)

    # Perform the query in the collection
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    # Format the results into a list of Documents
    retrieved_docs = []
    if results and results['documents']:
        for i, doc_content in enumerate(results['documents'][0]):
            retrieved_docs.append({
                "page_content": doc_content,
                "metadata": results['metadatas'][0][i]
            })
            
    return retrieved_docs

# --- Example Usage ---
if __name__ == '__main__':
    if not embedding_model:
        print("\nSkipping vector store example because embedding model could not be initialized.")
    else:
        # 1. Prepare sample document chunks
        sample_chunks = [
            {"page_content": "Artificial intelligence (AI) is intelligence demonstrated by machines.", "metadata": {"source": "wiki/ai", "chunk": 1}},
            {"page_content": "Machine learning (ML) is a field of study in artificial intelligence.", "metadata": {"source": "wiki/ml", "chunk": 1}},
            {"page_content": "A neural network is a network or circuit of biological neurons, or, in a modern sense, an artificial neural network, composed of artificial neurons or nodes.", "metadata": {"source": "wiki/nn", "chunk": 1}},
            {"page_content": "Deep learning is part of a broader family of machine learning methods based on artificial neural networks.", "metadata": {"source": "wiki/dl", "chunk": 1}}
        ]

        # 2. Create the vector store
        print("\n--- Creating vector store ---")
        collection_name = "ai_concepts_openai"
        # Clean up any old collection that might exist
        if collection_name in [c.name for c in client.list_collections()]:
            client.delete_collection(name=collection_name)
            print(f"Deleted existing collection: {collection_name}")
            
        collection = create_vector_store(sample_chunks, collection_name=collection_name)
        print(f"Vector store created. Collection '{collection.name}' contains {collection.count()} items.")

        # 3. Perform a search
        print("\n--- Performing similarity search ---")
        query = "What is deep learning?"
        search_results = search_vector_store(query, collection)

        print(f"\nQuery: '{query}'")
        print("Search results:")
        for doc in search_results:
            print(f"  - Content: '{doc['page_content']}'")
            print(f"    Metadata: {doc['metadata']}")