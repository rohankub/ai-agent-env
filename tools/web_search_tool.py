import requests
import os
from typing import Any, Type
from langchain.tools import BaseTool
from pydantic import BaseModel
from tools.base_models import WebSearchInput

class WebSearchTool(BaseTool):
    """Tool for performing web searches."""
    name: str = "web_search"
    description: str = "Search the web for information"
    args_schema: Type[BaseModel] = WebSearchInput
    
    def _run(self, query: str) -> str:
        """Run a web search for the query."""
        try:
            # Get API key and search engine ID from environment variables
            api_key = os.environ.get("GOOGLE_API_KEY")
            search_engine_id = os.environ.get("GOOGLE_CSE_ID")
            
            # Check if API credentials are available
            if not api_key or not search_engine_id:
                return (
                    "Web search could not be performed because API credentials are missing. "
                    "Please set GOOGLE_API_KEY and GOOGLE_CSE_ID environment variables."
                )
            
            # Build the search URL
            url = f"https://www.googleapis.com/customsearch/v1"
            params = {
                "key": api_key,
                "cx": search_engine_id,
                "q": query,
                "num": 5  # Number of results to return
            }
            
            # Make the request
            response = requests.get(url, params=params)
            search_results = response.json()
            
            # Check if the request was successful
            if "error" in search_results:
                error_message = search_results["error"]["message"]
                return f"Error performing web search: {error_message}"
            
            # Format the results
            formatted_results = "Web Search Results:\n\n"
            
            if "items" in search_results:
                for i, item in enumerate(search_results["items"], 1):
                    title = item.get("title", "No title")
                    link = item.get("link", "No link")
                    snippet = item.get("snippet", "No description")
                    
                    formatted_results += f"{i}. {title}\n"
                    formatted_results += f"   URL: {link}\n"
                    formatted_results += f"   Description: {snippet}\n\n"
            else:
                formatted_results += "No results found for this query."
            
            return formatted_results
            
        except Exception as e:
            return f"Error performing web search: {str(e)}"
    
    def _arun(self, query: str) -> Any:
        """Run a web search for the query asynchronously."""
        # For async implementation
        raise NotImplementedError("WebSearchTool does not support async") 