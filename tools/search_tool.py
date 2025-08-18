from langchain.tools import Tool
from langchain_community.utilities import GoogleSearchAPIWrapper

from core.config import settings

def get_search_tool() -> Tool:
    """
    Initializes and returns a Tool object for performing Google searches.

    This function sets up a GoogleSearchAPIWrapper and configures it as a Tool.
    The tool is named "Google Search" and is described as being useful for
    searching the internet for current events or information not available in
    the local knowledge base. The underlying API requires the GOOGLE_API_KEY
    and GOOGLE_CSE_ID environment variables to be set.
    """
    # Ensure the required environment variables are set
    if not settings.GOOGLE_API_KEY or not settings.GOOGLE_CSE_ID:
        raise ValueError(
            "Missing GOOGLE_API_KEY or GOOGLE_CSE_ID environment variables."
        )

    search = GoogleSearchAPIWrapper()
    
    tool = Tool(
        name="Google Search",
        description="""
        A wrapper around Google Search.
        Useful for when you need to answer questions about current events.
        Use this tool to find information on the internet.
        Input should be a search query.
        """,
        func=search.run,
    )
    return tool

# Instantiate the tool
try:
    search_tool = get_search_tool()
except ValueError as e:
    print(f"Could not instantiate search_tool: {e}")
    # Create a placeholder or dummy tool if the API keys are not set
    search_tool = Tool(
        name="Google Search",
        description="Search tool is not configured. Please set GOOGLE_API_KEY and GOOGLE_CSE_ID.",
        func=lambda x: "Search tool is not configured."
    )


if __name__ == '__main__':
    # Example usage of the search tool
    if "not configured" in search_tool.description:
        print("Search tool is not configured. Skipping example.")
    else:
        query = "What is the latest news on AI agents?"
        result = search_tool.run(query)
        print(f"Query: {query}")
        print(f"Result: {result}")
