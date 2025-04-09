# Experiment with AI Agents

# AI Query Refinement and Response System

This project implements an intelligent query processing system that refines user queries, evaluates their type, and provides appropriate responses with optional references. The system uses LangChain, OpenAI's GPT models, and custom tools to deliver high-quality, contextually appropriate answers.

## Features

- **Query Refinement**: Automatically expands and improves user queries based on their type
- **Query Type Detection**: Classifies queries as scientific, balanced, or creative
- **Dynamic Temperature Adjustment**: Sets appropriate temperature for each query type
- **Reference Integration**: Provides academic references for factual queries when available
- **Custom Tools**: Includes tools for weather information, web searches, and academic references
- **Query History**: Maintains a record of all queries and responses
- **User-friendly Interface**: Streamlit web interface for easy interaction
- **Extensible Architecture**: Modular design for adding new tools and refiners

## How It Works

1. **Query Input**: User submits a simple query
2. **Query Evaluation**: System evaluates the query type (scientific, balanced, creative)
3. **Query Refinement**: Query is expanded and improved based on its type
4. **Temperature Setting**: Appropriate temperature is set based on query type
5. **Tool Selection**: Relevant tools are selected based on query content
6. **Response Generation**: Comprehensive response is generated
7. **Reference Addition**: References are added for scientific/factual queries if available
8. **History Storage**: Query and response are stored in history

## Query Types

The system classifies queries into three types:

1. **Scientific/Factual (Temperature 0.1-0.3)**
   - Requires precise, factual information
   - Involves technical, academic, or scientific topics
   - Example: "Explain quantum entanglement"

2. **Balanced (Temperature 0.4-0.6)**
   - Combines factual information with some interpretation
   - General knowledge, history, places, people, everyday topics
   - Example: "Tell me about New York City"

3. **Creative (Temperature 0.7-0.9)**
   - Requires imagination, storytelling, or artistic expression
   - Involves creative writing, hypotheticals, or subjective content
   - Example: "Write a poem about autumn"

## Setup

1. Clone this repository
2. Make sure you have Python 3.8+ installed
3. Install dependencies:
   ```
   pip install langchain langchain_community openai requests python-dotenv streamlit
   ```
4. Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Setting Up Google Custom Search API (for Web Search and References)

To enable the web search functionality and improve reference retrieval:

1. **Create a Google Cloud Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Make sure billing is enabled for your project

2. **Enable the Custom Search API**:
   - Go to [API Library](https://console.cloud.google.com/apis/library)
   - Search for "Custom Search API"
   - Click "Enable"

3. **Create API Credentials**:
   - Go to [Credentials](https://console.cloud.google.com/apis/credentials)
   - Click "Create Credentials" and select "API Key"
   - Copy your API key

4. **Set Up a Programmable Search Engine**:
   - Go to [Programmable Search Engine](https://programmablesearchengine.google.com/)
   - Click "Add" to create a new search engine
   - Choose to search the entire web
   - Get your Search Engine ID (cx)

5. **Update Your .env File**:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   GOOGLE_CSE_ID=your_custom_search_engine_id_here
   ```

## Usage

### Running the Web Interface

Run the Streamlit web interface:

```
streamlit run streamlit_app.py
```

This will open a web interface where you can:
- Enter queries in the input box
- View responses with optional references
- Access query history
- Adjust settings

### Running from Command Line

Run the agent directly from the command line:

```
python agent/cli.py
```

### Example Queries

Try these example queries to see how the system works:

#### Scientific Queries (with references)
- "Explain how black holes form"
- "What is quantum computing?"
- "How do vaccines work?"
- "Tell me about pulsars with references"

#### Balanced Queries
- "What's the weather in New York?"
- "Tell me about Leonardo da Vinci"
- "How is the movie Top Gun: Maverick?"
- "Describe the history of coffee"

#### Creative Queries
- "Write a poem about autumn"
- "Create a story about a robot discovering emotions"
- "Imagine life in the year 3000"

## Project Structure

The project follows a modular structure:

```
.
├── agent/                  # Agent-related functionality
│   ├── __init__.py         # Exports main functions
│   ├── core.py             # Core agent creation
│   ├── processor.py        # Query processing logic
│   ├── query_processor.py  # Streamlit-specific query processing
│   └── cli.py              # Command-line interface
├── tools/                  # Tool implementations
│   ├── __init__.py         # Exports get_custom_tools
│   ├── base_models.py      # Input models for tools
│   ├── weather_tool.py     # Weather tool implementation
│   ├── web_search_tool.py  # Web search tool implementation
│   └── reference_tool.py   # Reference tool implementation
├── refiners/               # Query refinement functionality
│   ├── __init__.py         # Exports refiner functions
│   ├── base_refiner.py     # Base refiner functionality
│   ├── scientific_refiner.py # Scientific query refiner
│   ├── creative_refiner.py # Creative query refiner
│   ├── balanced_refiner.py # Balanced query refiner
│   └── query_refiner.py    # Query refinement orchestration
├── history/                # Directory for storing query history
│   └── query_history.json  # JSON file storing all queries and responses
├── settings/               # Directory for storing application settings
├── streamlit_app.py        # Main Streamlit application
├── utils.py                # Utility functions
├── styles.py               # UI styles
├── pages.py                # Page rendering
├── sidebar.py              # Sidebar rendering
├── ui_components.py        # UI components
└── query_evaluator.py      # Query evaluation logic
```

## How Query Refinement Works

The system uses specialized refiners for each query type:

1. **Scientific Refiner**: Expands queries to include requests for detailed explanations, technical details, and references to authoritative sources.

2. **Balanced Refiner**: Enhances queries to request comprehensive information with a mix of facts and context, while maintaining a balanced perspective.

3. **Creative Refiner**: Transforms queries to encourage imaginative, original, and expressive responses.

## Query History Format

Query history is stored in JSON format with the following structure:

```json
{
  "original_question": "How is the movie Mission impossible 4?",
  "refined_question": "Can you provide a detailed overview of the movie \"Mission: Impossible - Ghost Protocol\"?...",
  "response": "I can't provide a detailed overview of 'Mission: Impossible - Ghost Protocol' due to limitations...",
  "query_evaluation": {
    "temperature": 0.4,
    "requires_references": false,
    "query_type": "balanced",
    "reasoning": "The query asks for an evaluation of a movie, which involves a mix of factual information..."
  },
  "references": "",
  "timestamp": "2025-03-09T21:43:44.708953"
}
```

## Extending the System

### Adding New Tools

To add new tools:

1. Create a new tool file in the `tools` directory
2. Implement the tool following the pattern in existing tools
3. Add your tool to the `get_custom_tools()` function in `tools/__init__.py`

### Adding New Refiners

To add new refiners:

1. Create a new refiner file in the `refiners` directory
2. Implement the refiner following the pattern in existing refiners
3. Add your refiner to the appropriate functions in `refiners/__init__.py`

## Troubleshooting

### References Not Working
- Ensure you've set up the Google Custom Search API correctly
- Check that your API key and Search Engine ID are correctly set in the `.env` file
- Verify that you have billing enabled for your Google Cloud project

### Temperature Not Adjusting Correctly
- Check the query evaluator logic in `query_evaluator.py`
- Ensure the query type is being correctly identified

### Query Refinement Issues
- Check the appropriate refiner in the `refiners` directory
- Ensure the refiner is correctly registered in `refiners/__init__.py`

## License

MIT 
