from typing import List
from langchain.tools import BaseTool
from tools.weather_tool import WeatherTool
from tools.web_search_tool import WebSearchTool
from tools.reference_tool import ReferenceTool

def get_custom_tools() -> List[BaseTool]:
    """Return a list of custom tools."""
    return [
        WeatherTool(),
        WebSearchTool(),
        ReferenceTool(),
    ] 