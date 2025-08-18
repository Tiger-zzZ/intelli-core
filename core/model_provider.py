from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from .config import OPENAI_API_KEY, DEFAULT_LLM_MODEL, DEFAULT_EMBEDDING_MODEL

def get_llm(model_name: str = DEFAULT_LLM_MODEL):
    """
    Initializes and returns a ChatOpenAI instance.

    Args:
        model_name (str): The name of the OpenAI model to use.

    Returns:
        A configured ChatOpenAI instance.
    
    Raises:
        ValueError: If OPENAI_API_KEY is not set.
    """
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY not found in .env file. Please set it.")
    
    model = ChatOpenAI(
        model_name=model_name,
        openai_api_key=OPENAI_API_KEY,
        temperature=0, # Set for predictable outputs
    )
    return model

def get_embedding_model(model_name: str = DEFAULT_EMBEDDING_MODEL):
    """
    Initializes and returns an OpenAIEmbeddings instance.

    Args:
        model_name (str): The name of the OpenAI embedding model to use.

    Returns:
        A configured OpenAIEmbeddings instance.

    Raises:
        ValueError: If OPENAI_API_KEY is not set.
    """
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY not found in .env file. Please set it.")
        
    embedding_model = OpenAIEmbeddings(
        model=model_name,
        openai_api_key=OPENAI_API_KEY
    )
    return embedding_model

# Instantiate the models for easy import elsewhere
try:
    llm = get_llm()
    embedding_model = get_embedding_model()
except ValueError as e:
    print(f"Could not initialize models: {e}")
    llm = None
    embedding_model = None


# --- Example Usage ---
if __name__ == '__main__':
    if not llm or not embedding_model:
        print("Skipping example because models could not be initialized.")
    else:
        try:
            # 1. Test the LLM
            print(f"--- Testing LLM ({llm.model_name}) ---")
            response = llm.invoke("Tell me a short joke about AI.")
            print("LLM Response:")
            print(response.content)
            
            print("\n" + "-"*20 + "\n")
            
            # 2. Test the Embedding Model
            print(f"--- Testing Embedding Model ({embedding_model.model}) ---")
            sample_text = "This is a test sentence."
            embedding_vector = embedding_model.embed_query(sample_text)
            
            print(f"Embedding for: '{sample_text}'")
            print(f"Vector (first 5 dimensions): {embedding_vector[:5]}")
            print(f"Total dimensions: {len(embedding_vector)}")

        except Exception as e:
            print(f"An error occurred during the example run: {e}")