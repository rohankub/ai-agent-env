from tools import get_custom_tools

def test_tools():
    """
    Test each custom tool individually.
    """
    print("Testing custom tools...")
    tools = get_custom_tools()
    
    # Test each tool
    for tool in tools:
        print(f"\nTesting tool: {tool.name}")
        print(f"Description: {tool.description}")
        
        try:
            # Test with sample input based on tool type
            if tool.name == "get_weather":
                result = tool.invoke("New York, NY")
                print(f"Sample input: 'New York, NY'")
            elif tool.name == "web_search":
                result = tool.invoke("artificial intelligence")
                print(f"Sample input: 'artificial intelligence'")
            else:
                print(f"Unknown tool type: {tool.name}, skipping test.")
                continue
                
            print(f"Result: {result}")
            print(f"✅ Tool '{tool.name}' is working correctly!")
        except Exception as e:
            print(f"❌ Error with tool '{tool.name}': {str(e)}")
            print(f"There might be an issue with this tool.")

if __name__ == "__main__":
    test_tools() 