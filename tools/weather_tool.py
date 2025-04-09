from typing import Any, Type
from langchain.tools import BaseTool
from pydantic import BaseModel
from tools.base_models import WeatherInput

class WeatherTool(BaseTool):
    """Tool for getting weather information."""
    name: str = "get_weather"
    description: str = "Get the current weather in a given location"
    args_schema: Type[BaseModel] = WeatherInput
    
    def _run(self, location: str) -> str:
        """Get the weather in a location."""
        # This is a placeholder. In a real implementation, you would call a weather API
        return f"The weather in {location} is currently sunny and 72 degrees Fahrenheit."
    
    def _arun(self, location: str) -> Any:
        """Get the weather in a location asynchronously."""
        # For async implementation
        raise NotImplementedError("WeatherTool does not support async") 