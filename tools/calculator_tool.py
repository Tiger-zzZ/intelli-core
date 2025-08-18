from langchain.chains import LLMMathChain
from langchain.tools import Tool

from core.model_provider import llm

def get_calculator_tool() -> Tool:
    """
    Initializes and returns a Tool object that uses an LLMMathChain to perform calculations.

    The LLMMathChain is configured with a language model (llm) and set to be verbose.
    The returned Tool is configured with a name, the chain's run method, and a description
    that informs the agent how to use the tool for mathematical questions.
    """
    llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)
    
    tool = Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="""
        Useful for when you need to answer questions about math.
        Use this tool for any mathematical questions, calculations, or evaluations.
        """,
    )
    return tool

# Instantiate the tool
calculator_tool = get_calculator_tool()

if __name__ == '__main__':
    # Example usage of the calculator tool
    question = "What is 2 + 2?"
    result = calculator_tool.run(question)
    print(f"Question: {question}")
    print(f"Result: {result}")

    question = "what is 3 * (4 + 5)?"
    result = calculator_tool.run(question)
    print(f"Question: {question}")
    print(f"Result: {result}")
