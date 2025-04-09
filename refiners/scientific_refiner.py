import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

def create_scientific_refiner_agent(temperature=0.1):
    """
    Create a refiner agent specifically for scientific/factual queries.
    
    Args:
        temperature: The temperature to use for the language model
    """
    # Initialize the language model with very low temperature for precision
    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=temperature,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create a prompt template for the scientific refiner
    scientific_refiner_prompt = ChatPromptTemplate.from_template("""
    You are an expert scientific query optimizer. Your job is to transform user questions into precise, 
    comprehensive queries that will yield accurate, well-referenced, and complete responses.
    
    Original question: {question}
    
    Please refine this question by:
    
    1. SPECIFICITY: Make it specific about exactly what scientific information is needed
       - Identify the core scientific subject and key aspects that need explanation
       - Specify the depth of information required (introductory, intermediate, advanced)
       - Include any particular scientific angles or perspectives of interest
       - Request comprehensive coverage with multiple aspects and examples
    
    2. CONTEXT & CONSTRAINTS: Add necessary scientific context
       - Specify any time periods, domains, or scientific fields relevant to the query
       - Include any specific applications or use cases of interest
       - Request historical context and current developments
    
    3. REFERENCE REQUIREMENTS: Request reliable scientific sources
       - Ask for peer-reviewed papers, academic journals, or authoritative references
       - Request specific types of references (historical, recent developments, meta-analyses)
       - Ask for a mix of foundational and cutting-edge references when appropriate
    
    4. STRUCTURE: Format the query to minimize ambiguity
       - Break complex scientific topics into clear sub-questions if needed
       - Use precise terminology appropriate to the scientific field
       - Request a thorough, multi-paragraph response with examples
    
    5. ANTI-HALLUCINATION: Include elements that discourage fabricated information
       - Request verification of key scientific claims
       - Ask for specific examples or data that can be verified
    
    Return ONLY the improved question without any explanations or additional text.
    Make the question sound natural and conversational, not like a list of requirements.
    """)
    
    return llm, scientific_refiner_prompt 