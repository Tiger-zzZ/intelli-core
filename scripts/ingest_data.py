import os
import argparse
from pathlib import Path
import sys

# Add project root to sys.path to allow importing project modules
sys.path.append(str(Path(__file__).parent.parent))

from rag.document_loader import load_text_document
from rag.text_splitter import split_text_by_character
from rag.vector_store import create_vector_store, client as chroma_client
from tools.rag_tool import DEFAULT_COLLECTION_NAME

def main(file_path: str):
    """
    Main function to process a document and load it into the vector store.
    """
    print(f"--- Starting data ingestion for: {file_path} ---")
    
    # 1. Load the document
    print("1. Loading document...")
    try:
        doc = load_text_document(file_path)
        print(f"   - Successfully loaded '{doc['metadata']['source']}'")
    except Exception as e:
        print(f"   - Error loading document: {e}")
        return

    # 2. Split the text into chunks
    print("2. Splitting document into chunks...")
    try:
        chunks = split_text_by_character(doc, chunk_size=1000, chunk_overlap=200)
        print(f"   - Document split into {len(chunks)} chunks.")
    except Exception as e:
        print(f"   - Error splitting document: {e}")
        return

    # 3. Create or update the vector store
    print(f"3. Loading chunks into ChromaDB collection: '{DEFAULT_COLLECTION_NAME}'...")
    try:
        # Check if the collection already exists
        if DEFAULT_COLLECTION_NAME in [c.name for c in chroma_client.list_collections()]:
            print(f"   - Collection '{DEFAULT_COLLECTION_NAME}' already exists. Adding new documents.")
        else:
            print(f"   - Creating new collection: '{DEFAULT_COLLECTION_NAME}'")
            
        collection = create_vector_store(chunks, collection_name=DEFAULT_COLLECTION_NAME)
        print(f"   - Successfully loaded data. Collection now contains {collection.count()} items.")
    except Exception as e:
        print(f"   - Error creating vector store: {e}")
        return
        
    print("\n--- Ingestion complete! ---")
    print("The RAG tool is now ready to use this document.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load a document into the Intelli-Core knowledge base.")
    parser.add_argument("file_path", type=str, help="The path to the .txt file to ingest.")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file_path):
        print(f"Error: File not found at '{args.file_path}'")
    else:
        main(args.file_path)
