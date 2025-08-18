from typing import List
from langchain.agents import AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import BaseTool

from agent.base_agent import create_intelli_agent
from core.model_provider import llm
from tools.rag_tool import rag_tool
from tools.search_tool import search_tool

# --- Agent Prompts ---

RESEARCHER_PROMPT_TEMPLATE = """
You are a master researcher. Your goal is to gather information on a given topic.
You must use your available tools to find the most relevant and up-to-date information.
Provide a concise and comprehensive summary of your findings.

You have access to the following tools:
{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I have gathered enough information.
Final Answer: A comprehensive summary of my findings.

Begin!

Question: {input}
Thought:{agent_scratchpad}
"""

WRITER_PROMPT_TEMPLATE = """
You are a professional writer. Your task is to take the provided research findings
and write a clear, concise, and well-structured report.
Do not add any information that is not present in the research findings.
Your final output should be only the report, without any extra commentary.

Research Findings:
---
{research_findings}
---

Based on the findings, write a report on the topic: {topic}
"""

# --- Agent Creation ---

def create_researcher_agent() -> AgentExecutor:
    """
    Creates an agent specialized in research tasks.
    It is equipped with search and knowledge base tools.
    """
    tools: List[BaseTool] = [search_tool, rag_tool]
    prompt = PromptTemplate.from_template(RESEARCHER_PROMPT_TEMPLATE)
    
    agent = create_intelli_agent(llm, tools, prompt)
    
    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
    )
    return executor

def create_writer_agent() -> "Runnable":
    """
    Creates a "writer" agent, which is a simple LLM chain.
    It takes research findings and a topic, and writes a report.
    It has no tools and operates non-interactively.
    """
    prompt = PromptTemplate.from_template(WRITER_PROMPT_TEMPLATE)
    
    # This "agent" is a simple chain, not an executor, as it has no tools.
    writer_chain = prompt | llm
    
    return writer_chain

if __name__ == '__main__':
    # --- Example Usage ---
    
    # 1. Create the researcher agent and run it
    print("--- Testing Researcher Agent ---")
    researcher = create_researcher_agent()
    topic = "the future of AI agents"
    research_result = researcher.invoke({"input": topic})
    print("\n--- Research Findings ---")
    print(research_result['output'])
    
    # 2. Create the writer agent and run it
    print("\n--- Testing Writer Agent ---")
    writer = create_writer_agent()
    report = writer.invoke({
        "research_findings": research_result['output'],
        "topic": topic
    })
    print("\n--- Final Report ---")
    # The writer output is a Generation object, we need to access the text
    print(report.content)
