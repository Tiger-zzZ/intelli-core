from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from core.model_provider import llm

# --- Task Decomposition Prompt ---

DECOMPOSER_PROMPT_TEMPLATE = """
You are a task analysis assistant. Your role is to extract the core research topic
from a user's request. The user might ask for a complex task involving multiple steps,
like research and writing. You should only identify the main subject of the research.

For example:
User Request: "Can you research the impact of climate change on polar bears and then write a short summary?"
Core Topic: "the impact of climate change on polar bears"

User Request: "Tell me everything you can find about the history of the Roman Empire."
Core Topic: "the history of the Roman Empire"

User Request: "write a report about the latest advancements in quantum computing"
Core Topic: "the latest advancements in quantum computing"

Now, analyze the following user request and extract the core research topic.
Your output should ONLY be the topic itself, with no preamble or explanation.

User Request: "{user_request}"
Core Topic:
"""

# --- Task Decomposition Chain ---

def get_task_decomposer() -> "Runnable":
    """
    Creates and returns a simple chain for decomposing a user request into a core topic.
    """
    prompt = PromptTemplate.from_template(DECOMPOSER_PROMPT_TEMPLATE)
    
    # The chain consists of the prompt, the LLM, and a string output parser.
    decomposer_chain = prompt | llm | StrOutputParser()
    
    return decomposer_chain

# Instantiate the decomposer
task_decomposer = get_task_decomposer()

if __name__ == '__main__':
    # --- Example Usage ---
    print("--- Testing Task Decomposer ---")
    
    request1 = "Please research the benefits of a four-day work week and then write a report for management."
    topic1 = task_decomposer.invoke({"user_request": request1})
    
    print(f"User Request: '{request1}'")
    print(f"Extracted Topic: '{topic1}'")
    
    print("\n" + "-"*20 + "\n")
    
    request2 = "I need a detailed analysis of the current state of the global economy."
    topic2 = task_decomposer.invoke({"user_request": request2})
    
    print(f"User Request: '{request2}'")
    print(f"Extracted Topic: '{topic2}'")
