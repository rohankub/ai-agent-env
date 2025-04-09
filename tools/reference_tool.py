from typing import Any, Type
from langchain.tools import BaseTool
from pydantic import BaseModel
from tools.base_models import ReferenceInput
from tools.web_search_tool import WebSearchTool

class ReferenceTool(BaseTool):
    """Tool for retrieving references on a topic."""
    name: str = "get_references"
    description: str = "Get academic or reliable references on a specific topic"
    args_schema: Type[BaseModel] = ReferenceInput
    
    def _run(self, topic: str) -> str:
        """Get references for a topic."""
        # First, try to get references from web search
        try:
            web_search_tool = WebSearchTool()
            
            # First search for academic sources
            academic_query = f"academic papers research articles {topic}"
            academic_results = web_search_tool._run(academic_query)
            
            # Then search for Wikipedia and other public resources
            wiki_query = f"wikipedia {topic} site:en.wikipedia.org"
            wiki_results = web_search_tool._run(wiki_query)
            
            # Check if we got valid search results from either query
            if ("Web Search Results:" in academic_results and "Error performing web search" not in academic_results) or \
               ("Web Search Results:" in wiki_results and "Error performing web search" not in wiki_results):
                
                # Format the web search results as references
                formatted_refs = "REFERENCES FROM WEB SEARCH\n\n"
                
                # Add academic results if available
                if "Web Search Results:" in academic_results and "Error performing web search" not in academic_results:
                    formatted_refs += "Academic Sources:\n"
                    formatted_refs += academic_results.split("Web Search Results:")[1].strip() + "\n\n"
                
                # Add Wikipedia and public resources if available
                if "Web Search Results:" in wiki_results and "Error performing web search" not in wiki_results:
                    formatted_refs += "Public Resources:\n"
                    formatted_refs += wiki_results.split("Web Search Results:")[1].strip()
                
                return formatted_refs
            else:
                # If web search failed, provide a helpful message
                error_message = ""
                if "Error performing web search" in academic_results:
                    error_message = academic_results.split("Error performing web search:")[1].strip()
                
                return self._generate_reference_limitation_notice(topic, error_message)
        except Exception as e:
            # If there's an error with web search, provide a helpful error message
            return self._generate_reference_limitation_notice(topic, str(e))
    
    def _generate_reference_limitation_notice(self, topic: str, error_message: str = "") -> str:
        """Generate a helpful notice about reference limitations."""
        disclaimer = f"""
IMPORTANT NOTICE: REFERENCE LIMITATION

I couldn't find specific references for "{topic}" through web search. {error_message}

To get accurate and up-to-date references, please consider:

1. Using academic search engines like:
   - Google Scholar (scholar.google.com)
   - PubMed (pubmed.ncbi.nlm.nih.gov) for medical/biological topics
   - IEEE Xplore (ieeexplore.ieee.org) for engineering/computer science
   - ACM Digital Library (dl.acm.org) for computer science
   - arXiv (arxiv.org) for preprints in physics, math, computer science

2. Checking Wikipedia and other public resources:
   - Wikipedia (en.wikipedia.org)
   - Encyclopedia Britannica (britannica.com)
   - National Geographic (nationalgeographic.com)

NOTE ON WEB SEARCH: The web search feature requires valid Google API credentials. To enable this feature:
1. Create a Google Cloud project at https://console.cloud.google.com/
2. Enable the Custom Search API
3. Create API credentials at https://console.cloud.google.com/apis/credentials
4. Set up a Programmable Search Engine at https://programmablesearchengine.google.com/
5. Update your .env file with the API key and search engine ID

I can still provide information on this topic based on my training, but I cannot generate specific citations without access to current databases or functioning web search.
"""
        return disclaimer
    
    def _arun(self, topic: str) -> Any:
        """Get references for a topic asynchronously."""
        # For async implementation
        raise NotImplementedError("ReferenceTool does not support async") 