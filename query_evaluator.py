import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

def create_evaluator():
    """
    Create a query evaluator that determines the appropriate temperature based on query type.
    """
    # Initialize the language model with low temperature for consistent evaluation
    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=0.1,  # Low temperature for consistent evaluation
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create a prompt template for the evaluator
    evaluator_prompt = ChatPromptTemplate.from_template("""
    You are a query evaluator that determines the appropriate temperature setting for an AI model based on the type of query.
    
    Query: {query}
    
    Analyze this query carefully and determine:
    
    1. SCIENTIFIC/FACTUAL QUERIES (Temperature 0.1-0.3):
       - Requires precise, factual information
       - Involves technical, academic, or scientific topics
       - Examples: "Explain quantum entanglement", "How do vaccines work?", "What causes black holes to form?"
    
    2. BALANCED QUERIES (Temperature 0.4-0.6):
       - Combines factual information with some interpretation
       - General knowledge, history, places, people, everyday topics
       - Examples: "Tell me about New York City", "Who was Leonardo da Vinci?", "Describe the history of coffee"
    
    3. CREATIVE QUERIES (Temperature 0.7-0.9):
       - Requires imagination, storytelling, or artistic expression
       - Involves creative writing, hypotheticals, or subjective content
       - Examples: "Write a poem about autumn", "Create a story about a robot", "Imagine life in the year 3000"
    
    Also determine if the query explicitly or implicitly requires references to authoritative sources.
    
    Return ONLY a JSON object with the following structure:
    {{
      "temperature": [float between 0.1 and 0.9],
      "requires_references": [true/false],
      "query_type": ["scientific", "balanced", or "creative"],
      "reasoning": [brief explanation for your decision]
    }}
    """)
    
    return llm, evaluator_prompt

def evaluate_query(query):
    """
    Evaluate a query and determine the appropriate temperature and whether references are required.
    
    Args:
        query: The user's query
        
    Returns:
        dict: A dictionary containing temperature, requires_references, query_type, and reasoning
    """
    llm, evaluator_prompt = create_evaluator()
    
    # Format the prompt with the query
    formatted_prompt = evaluator_prompt.format(
        query=query
    )
    
    # Get the evaluation
    evaluation = llm.invoke(formatted_prompt)
    
    # Parse the JSON response
    import json
    try:
        result = json.loads(evaluation.content)
        # Ensure temperature is within bounds
        result["temperature"] = max(0.1, min(0.9, result["temperature"]))
        
        # Override requires_references if "with references" is explicitly mentioned
        if "with references" in query.lower():
            result["requires_references"] = True
            
        # Add a warning if references are requested
        if result["requires_references"]:
            # Check if Google API credentials are available
            google_api_key = os.environ.get("GOOGLE_API_KEY")
            google_cse_id = os.environ.get("GOOGLE_CSE_ID")
            
            if (not google_api_key or google_api_key == "YOUR_GOOGLE_API_KEY_HERE" or 
                not google_cse_id or google_cse_id == "YOUR_CUSTOM_SEARCH_ENGINE_ID_HERE"):
                result["reference_warning"] = "Note: The reference feature requires Google API credentials which are currently not configured. References will not be available until these credentials are set up."
            else:
                # Check if the query is about one of our pre-defined topics
                predefined_topics = ["pulsars", "quantum computing", "artificial intelligence", "black hole"]
                query_lower = query.lower()
                has_predefined_topic = any(topic in query_lower for topic in predefined_topics)
                
                if not has_predefined_topic:
                    result["reference_warning"] = "Note: The system can only provide verified references for a limited set of topics. For other topics, it will suggest using academic search engines instead."
            
        return result
    except json.JSONDecodeError:
        # Fallback if JSON parsing fails
        reference_warning = None
        requires_references = "with references" in query.lower()
        
        if requires_references:
            # Check if Google API credentials are available
            google_api_key = os.environ.get("GOOGLE_API_KEY")
            google_cse_id = os.environ.get("GOOGLE_CSE_ID")
            
            if (not google_api_key or google_api_key == "YOUR_GOOGLE_API_KEY_HERE" or 
                not google_cse_id or google_cse_id == "YOUR_CUSTOM_SEARCH_ENGINE_ID_HERE"):
                reference_warning = "Note: The reference feature requires Google API credentials which are currently not configured. References will not be available until these credentials are set up."
            else:
                reference_warning = "Note: The system can only provide verified references for a limited set of topics. For other topics, it will suggest using academic search engines instead."
            
        return {
            "temperature": 0.5,  # Default to balanced
            "requires_references": requires_references,
            "query_type": "balanced",
            "reasoning": "Failed to parse evaluation, using default values.",
            "reference_warning": reference_warning
        } 