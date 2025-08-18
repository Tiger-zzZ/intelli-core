from typing import List
from langchain.agents import create_react_agent
from langchain_core.language_models import BaseLanguageModel
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import BaseTool

from .prompt_template import REACT_PROMPT_TEMPLATE

def create_intelli_agent(
    llm: BaseLanguageModel,
    tools: List[BaseTool],
) -> "Runnable":
    """
    Creates a ReAct agent using the provided language model, tools, and prompt template.

    This function acts as a factory for our agent. It pulls the prompt template,
    formats it with the available tools, and then uses LangChain's `create_react_agent`
    to construct the core agent logic (a Runnable).

    Args:
        llm (BaseLanguageModel): The language model that will power the agent.
        tools (List[BaseTool]): A list of tools the agent can use.

    Returns:
        Runnable: The core agent logic, ready to be wrapped by an AgentExecutor.
    """
    # Create the prompt template from our defined string
    prompt = PromptTemplate.from_template(REACT_PROMPT_TEMPLATE)
    
    # Use LangChain's factory function to create the agent's core logic
    agent = create_react_agent(llm, tools, prompt)
    
    return agent
