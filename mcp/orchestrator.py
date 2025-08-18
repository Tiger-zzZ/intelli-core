from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from mcp.agent_manager import create_researcher_agent, create_writer_agent
from mcp.task_decomposer import task_decomposer
from core.logger import log

from core.logger import log

# --- 1. Define the State for the Graph ---

class GraphState(TypedDict):
    """
    Represents the state of our multi-agent workflow.
    This state is passed between nodes in the graph.
    """
    user_request: str
    topic: str
    research_findings: str
    final_report: str

# --- 2. Define the Nodes for the Graph ---

def decompose_task_node(state: GraphState):
    """
    Node that decomposes the initial user request to extract the research topic.
    """
    log.info("--- Node: Decompose Task ---")
    request = state['user_request']
    
    log.info(f"Decomposing request: '{request}'")
    topic = task_decomposer.invoke({"user_request": request})
    log.info(f"Extracted Topic: '{topic}'")
    
    return {"topic": topic}

def research_node(state: GraphState):
    """
    Node that invokes the researcher agent to gather information on the topic.
    """
    log.info("--- Node: Research ---")
    topic = state['topic']
    
    log.info(f"Invoking researcher for topic: '{topic}'")
    researcher = create_researcher_agent()
    findings = researcher.invoke({"input": topic})
    log.info(f"Research complete. Findings length: {len(findings['output'])}")
    
    return {"research_findings": findings['output']}

def write_node(state: GraphState):
    """
    Node that invokes the writer agent to create a report from the research findings.
    """
    log.info("--- Node: Write ---")
    findings = state['research_findings']
    topic = state['topic']
    
    log.info(f"Invoking writer for topic: '{topic}'")
    writer = create_writer_agent()
    report = writer.invoke({"research_findings": findings, "topic": topic})
    log.info("Writing complete.")
    
    return {"final_report": report.content}

# --- 3. Define and Compile the Graph ---

def get_orchestrator():
    """
    Builds and compiles the LangGraph orchestrator.
    """
    workflow = StateGraph(GraphState)

    # Add the nodes
    workflow.add_node("decomposer", decompose_task_node)
    workflow.add_node("researcher", research_node)
    workflow.add_node("writer", write_node)

    # Set the entry and end points
    workflow.set_entry_point("decomposer")
    workflow.add_edge("writer", END)

    # Define the workflow sequence
    workflow.add_edge("decomposer", "researcher")
    workflow.add_edge("researcher", "writer")

    # Compile the graph into a runnable, with memory to persist state
    memory = MemorySaver()
    orchestrator = workflow.compile(checkpointer=memory)
    
    return orchestrator

# Instantiate the orchestrator
main_orchestrator = get_orchestrator()

if __name__ == '__main__':
    # --- Example Usage ---
    print("Orchestrator is ready.")
    
    user_request = "Write a short report on the main challenges and opportunities in the field of AI Agents."
    config = {"configurable": {"thread_id": "user-123"}} # Unique ID for the run
    
    # The .stream() method returns an iterator of the state at each step
    for step in main_orchestrator.stream({"user_request": user_request}, config=config):
        # The key is the name of the node that just ran
        node_name = list(step.keys())[0]
        print(f"\n--- Finished Step: {node_name} ---")
        print(f"State: {step[node_name]}")

    # Final state can be retrieved from the checkpointer if needed
    final_state = main_orchestrator.get_state(config)
    print("\n--- Final Report ---")
    print(final_state.values['final_report'])
