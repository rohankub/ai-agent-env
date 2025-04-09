import os
from dotenv import load_dotenv
from agent.core import create_agent

def test_agent():
    """
    Test the AI agent with a simple query.
    """
    # Load environment variables
    load_dotenv()
    
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in environment variables.")
        print("Please set your OpenAI API key in the .env file.")
        return
    
    print("Initializing agent for testing...")
    agent = create_agent()
    
    # Test query
    test_query = "Hello, who are you?"
    
    print(f"\nTest Query: '{test_query}'")
    print("Agent Response:")
    
    try:
        response_result = agent.invoke({"input": test_query})
        response = response_result["output"]
        print(f"✅ Success! Agent responded with:\n{response}")
        print("\nBasic framework is working correctly!")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\nThere might be an issue with the agent setup.")

if __name__ == "__main__":
    test_agent() 