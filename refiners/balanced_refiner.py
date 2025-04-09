import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

def create_balanced_refiner_agent(temperature=0.5):
    """
    Create a refiner agent for balanced queries that have both factual and creative elements.
    
    Args:
        temperature: The temperature to use for the language model
    """
    # Initialize the language model with moderate temperature
    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=temperature,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create a prompt template for the balanced refiner
    balanced_refiner_prompt = ChatPromptTemplate.from_template("""
    You are a query enhancement specialist. Your job is to transform user questions into well-structured, 
    informative queries that will yield comprehensive and engaging responses.
    
    Original question: {question}
    
    Please enhance this question by:
    
    1. COMPREHENSIVE COVERAGE: Request thorough information
       - Ask for a detailed, multi-paragraph response that covers all important aspects
       - Request specific details, examples, and context
       - For products or technologies, ask about features, specifications, history, comparisons, and user experiences
       - For places, ask about history, culture, geography, attractions, and interesting facts
       - For people, ask about biography, achievements, impact, and legacy
    
    2. SCOPE: Define a broad but manageable scope
       - For general topics, request coverage of multiple dimensions (historical, practical, cultural, etc.)
       - For current events or products, ask for both factual information and analysis
       - Request both mainstream information and interesting lesser-known facts
    
    3. ENGAGEMENT: Encourage an informative yet engaging response
       - Ask for interesting facts, statistics, or notable aspects
       - Request real-world examples or applications
       - For general knowledge topics, ask for authoritative sources without requiring academic references
    
    Return ONLY the enhanced question without any explanations or additional text.
    Make the question sound natural and conversational, not like a list of requirements.
    """)
    
    return llm, balanced_refiner_prompt 