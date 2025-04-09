from pydantic import BaseModel, Field

class WeatherInput(BaseModel):
    """Input for the weather tool."""
    location: str = Field(..., description="The city and state, e.g. San Francisco, CA")

class WebSearchInput(BaseModel):
    """Input for the web search tool."""
    query: str = Field(..., description="The search query")

class ReferenceInput(BaseModel):
    """Input for the reference retrieval tool."""
    topic: str = Field(..., description="The topic to find references for") 