from abc import ABC, abstractmethod

class BaseTool(ABC):
    """
    The base class for all tools.
    """
    name: str
    description: str

    @abstractmethod
    def run(self, query: str) -> str:
        """
        Run the tool.
        """
        pass
