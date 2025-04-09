import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

def create_creative_refiner_agent(temperature=0.7):
    """
    Create a refiner agent specifically for creative/artistic queries.
    
    Args:
        temperature: The temperature to use for the language model
    """
    # Initialize the language model with higher temperature for creativity
    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=temperature,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create a prompt template for the creative refiner
    creative_refiner_prompt = ChatPromptTemplate.from_template("""
    You are a creative query enhancer. Your job is to transform user questions into richer, more inspiring prompts
    that will yield imaginative, engaging, and thoughtful responses.
    
    Original question: {question}
    
    Please enhance this question by:
    
    1. DEPTH: Add elements that encourage deeper exploration
       - Suggest considering multiple perspectives or interpretations
       - Invite exploration of nuance, complexity, or creative tensions
       - Request rich, detailed descriptions and vivid imagery
    
    2. INSPIRATION: Add elements that spark creativity
       - Suggest interesting angles, metaphors, or connections
       - Encourage thinking outside conventional boundaries
       - Request emotional depth and sensory details
    
    3. CONTEXT: Add helpful creative context when relevant
       - Suggest considering historical, cultural, or artistic influences
       - Invite exploration of emotional or experiential dimensions
       - Request a fully developed narrative or concept
    
    4. CLARITY: Ensure the creative direction is clear while allowing freedom
       - Maintain the core intent of the original question
       - Provide enough structure for guidance without constraining creativity
       - Request a substantial, detailed response
    
    Return ONLY the enhanced question without any explanations or additional text.
    Make the question sound natural and conversational, not like a list of requirements.
    """)
    
    return llm, creative_refiner_prompt 