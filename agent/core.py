import os
from dotenv import load_dotenv
from langchain.agents import AgentType, initialize_agent
from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from tools import get_custom_tools

# Load environment variables
load_dotenv()

def create_agent(temperature=0.2):
    """
    Create and initialize a LangChain agent with OpenAI.
    
    Args:
        temperature: The temperature to use for the language model
    """
    # Initialize the language model with a reasonable token limit
    # 4000 tokens is approximately 3000 words, which is a good balance
    # between comprehensiveness and practical limitations
    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=temperature,
        max_tokens=4000,  # Reasonable token limit for comprehensive responses
        request_timeout=180,  # 3 minute timeout for API requests
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Get custom tools
    tools = get_custom_tools()
    
    # Set up memory for the agent
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    # Initialize the agent
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory,
        verbose=True
    )
    
    return agent 