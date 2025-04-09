import os
import traceback
from agent.processor import process_query

def main():
    """
    Main function to run the agent from the command line.
    """
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in environment variables.")
        print("Please set your OpenAI API key in the .env file.")
        return
        
    print("AI Agent initialized. Type 'exit' to quit.")
    print("Example commands:")
    print("- 'What's the weather in New York?'")
    print("- 'Search for information about artificial intelligence'")
    print("- 'Tell me about quantum computing with references'")
    print("- 'Write a creative story about a robot learning to paint'")
    print("- Add 'show details' to see references and query evaluation")
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() == "exit":
            print("Exiting AI agent. Goodbye!")
            break
        
        try:
            print(f"\nProcessing query...")
            
            result = process_query(user_input)
            
            # Display results
            print("\n=== ORIGINAL QUESTION ===")
            print(result["original_question"])
            
            print("\n=== REFINED QUESTION ===")
            print(result["refined_question"])
            
            print("\n=== RESPONSE ===")
            print(result["response"])
            
            # Only show details if explicitly requested
            if "show details" in user_input.lower():
                print("\n=== QUERY EVALUATION ===")
                print(f"Type: {result['query_evaluation']['query_type']}")
                print(f"Temperature: {result['query_evaluation']['temperature']}")
                print(f"Requires references: {result['query_evaluation']['requires_references']}")
                print(f"Reasoning: {result['query_evaluation']['reasoning']}")
                
                if result["references"]:
                    print("\n=== REFERENCES ===")
                    print(result["references"])
                
        except Exception as e:
            print(f"Error in main: {str(e)}")
            print(traceback.format_exc())
            print("\nI encountered an error while processing your query. Please try again or rephrase your question.")

if __name__ == "__main__":
    main() 