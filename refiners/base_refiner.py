import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

def create_refiner_agent(temperature=0.3):
    """
    Create a refiner agent that improves queries based on feedback.
    
    Args:
        temperature: The temperature to use for the language model
    """
    # Initialize the language model
    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=temperature,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create a prompt template for the refiner
    refiner_prompt = ChatPromptTemplate.from_template("""
    You are a query refiner that improves questions based on feedback.
    
    Original question: {question}
    Initial response: {response}
    Judge's evaluation: {evaluation}
    
    Your task is to create an improved version of the original question that addresses the issues identified by the judge.
    Focus on making the question more specific, clear, and designed to avoid the problems found in the initial response.
    
    Return ONLY the improved question without any explanations or additional text.
    """)
    
    return llm, refiner_prompt

def refine_query(question, response, evaluation):
    """
    Use the refiner agent to improve a query based on judge feedback.
    """
    llm, refiner_prompt = create_refiner_agent()
    
    # Format the prompt with the question, response, and evaluation
    formatted_prompt = refiner_prompt.format(
        question=question,
        response=response,
        evaluation=evaluation
    )
    
    # Get the refined query
    refined_query = llm.invoke(formatted_prompt)
    
    return refined_query.content 