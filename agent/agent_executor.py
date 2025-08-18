from typing import List
from langchain.agents import AgentExecutor
from langchain_core.tools import BaseTool

from core.model_provider import llm
from tools.calculator_tool import calculator_tool
from tools.rag_tool import rag_tool
from tools.search_tool import search_tool
from .base_agent import create_intelli_agent

def get_agent_executor() -> AgentExecutor:
    """
    Initializes and returns the main AgentExecutor.

    This function gathers all the available tools, creates the agent's core logic
    using the factory function, and then wraps it in an AgentExecutor, which is
    responsible for running the agent's "thought-action" loop.
    """
    # 1. Gather all the tools into a list
    tools: List[BaseTool] = [calculator_tool, rag_tool, search_tool]
    
    # 2. Create the agent's core logic
    agent = create_intelli_agent(llm=llm, tools=tools)
    
    # 3. Create the agent executor
    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,  # Set to True to see the agent's thought process
        handle_parsing_errors=True, # Handle cases where the LLM output is not perfect
    )
    
    return executor

# Instantiate the main executor
agent_executor = get_agent_executor()

if __name__ == '__main__':
    # --- Example Usage ---
    print("Agent Executor is ready. You can now ask questions.")

    # Example 1: A question that should use the calculator
    # query1 = "What is the result of 3.14 * (5^2)?"
    # print(f"\n--- Running query: '{query1}' ---")
    # response1 = agent_executor.invoke({"input": query1})
    # print("\n--- Final Answer ---")
    # print(response1["output"])

    # Example 2: A question that should use the search tool
    # query2 = "What is the current weather in New York City?"
    # print(f"\n--- Running query: '{query2}' ---")
    # response2 = agent_executor.invoke({"input": query2})
    # print("\n--- Final Answer ---")
    # print(response2["output"])

    # Example 3: A question for the RAG tool (assuming the KB is populated)
    # To test this, you need to run an ingestion script first.
    query3 = "What is the main goal of the Intelli-Core project?"
    print(f"\n--- Running query: '{query3}' ---")
    response3 = agent_executor.invoke({"input": query3})
    print("\n--- Final Answer ---")
    print(response3["output"])
