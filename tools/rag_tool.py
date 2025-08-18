from langchain.tools import Tool
import chromadb

from rag.retriever import RAGRetriever
from rag.vector_store import client as chroma_client

# Define a constant for the default knowledge base collection name
DEFAULT_COLLECTION_NAME = "intelli-core-kb"

def get_rag_tool() -> Tool:
    """
    Initializes and returns a RAG (Retrieval-Augmented Generation) tool.

    This tool is designed to answer questions based on a private knowledge base
    stored in a persistent ChromaDB collection. It checks if the collection
    exists and contains documents. If not, the tool's description will indicate
    that the knowledge base is not ready.
    """
    try:
        # 1. Get the persistent ChromaDB collection
        collection = chroma_client.get_collection(name=DEFAULT_COLLECTION_NAME)
        
        # 2. Check if the collection has documents
        if collection.count() == 0:
            # If the collection is empty, return a tool with a message.
            return Tool(
                name="Private Knowledge Base",
                func=lambda q: "The knowledge base is empty. Please load documents first.",
                description="The knowledge base is currently empty. This tool is not available.",
            )
            
        # 3. Instantiate the RAGRetriever
        retriever = RAGRetriever(collection)
        
        # 4. Create the LangChain Tool
        tool = Tool(
            name="Private Knowledge Base",
            func=retriever.answer_query,
            description="""
            Useful for when you need to answer questions about your private documents.
            Use this tool to find information within the internal knowledge base.
            Input should be a clear, specific question about the documents' content.
            """,
        )
        return tool

    except ValueError:
        # This exception is often raised by ChromaDB if the collection does not exist.
        return Tool(
            name="Private Knowledge Base",
            func=lambda q: "The knowledge base has not been initialized.",
            description="The knowledge base is not available. Please run the ingestion script.",
        )

# Instantiate the tool
rag_tool = get_rag_tool()

if __name__ == '__main__':
    # To test this tool, you first need to populate the "intelli-core-kb" collection.
    # You can do this by running a separate ingestion script.
    # For now, this example will likely show the "not initialized" message.
    
    print(f"Tool Name: {rag_tool.name}")
    print(f"Tool Description: {rag_tool.description}")
    
    query = "What is the core idea behind the Intelli-Core project?"
    result = rag_tool.run(query)
    
    print(f"\nQuery: '{query}'")
    print(f"Result: {result}")
