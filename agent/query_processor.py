import streamlit as st
import os
from query_evaluator import evaluate_query
from refiners import pre_refine_query
from agent.core import create_agent
from utils import save_to_history
from tools.reference_tool import ReferenceTool

def process_query():
    """Process the current query and update the session state with results"""
    if not st.session_state.is_processing or not st.session_state.current_query:
        return
    
    try:
        # Clear any existing query result
        st.session_state.query_result = None
        
        # Use the stored query
        current_query = st.session_state.current_query
        
        # Create a single placeholder for the final result
        result_placeholder = st.empty()
        
        # Get query evaluation
        evaluation = evaluate_query(current_query)
        
        # Get refined query
        refined_question = pre_refine_query(current_query, evaluation["query_type"], evaluation["temperature"])
        
        # Get the agent with appropriate temperature
        agent = create_agent(evaluation["temperature"])
        
        # Create the response prompt
        response_prompt = f"""
{refined_question}

Please provide a comprehensive, detailed response with the following characteristics:
1. Structure your response with clear headings and subheadings using markdown formatting (e.g., ## Main Features, ### Camera System)
2. Include at least 4-5 paragraphs of detailed information
3. Use bullet points for listing features or specifications
4. Include specific details, examples, and comparisons where relevant
5. Cover all major aspects of the topic thoroughly
6. If discussing a product or technology, include information about:
   - Key features and specifications
   - Comparisons with previous versions or competitors
   - User experiences and reviews
   - Market impact and significance
   - Future prospects or developments

Your response should be well-organized, informative, and engaging.
"""
        # Get the response
        response_result = agent.invoke({"input": response_prompt})
        response = response_result["output"]
        
        # Update result placeholder with final response
        result_placeholder.markdown(response, unsafe_allow_html=False)
        
        # Get references if required
        references = ""
        references_from_refs = ""
        if evaluation["requires_references"]:
            # Check if Google API credentials are available
            google_api_key = os.environ.get("GOOGLE_API_KEY")
            google_cse_id = os.environ.get("GOOGLE_CSE_ID")
            
            if (not google_api_key or google_api_key == "YOUR_GOOGLE_API_KEY_HERE" or 
                not google_cse_id or google_cse_id == "YOUR_CUSTOM_SEARCH_ENGINE_ID_HERE"):
                # API keys are not available, show a message
                references_from_refs = """
## References Unavailable

The reference feature requires Google API credentials which are currently not configured.

To enable references, please:
1. Create a Google Cloud project at https://console.cloud.google.com/
2. Enable the Custom Search API
3. Create API credentials at https://console.cloud.google.com/apis/credentials
4. Set up a Programmable Search Engine at https://programmablesearchengine.google.com/
5. Update your .env file with the API key and search engine ID

Once these credentials are configured, the reference feature will be automatically activated.
"""
            else:
                # API keys are available, try to get references
                try:
                    # Try to get references directly using the ReferenceTool
                    reference_tool = ReferenceTool()
                    references = reference_tool._run(refined_question)
                    
                    # Extract the references from the response
                    if "REFERENCES FROM WEB SEARCH" in references:
                        parts = references.split("REFERENCES FROM WEB SEARCH")
                        if len(parts) > 1:
                            references_from_refs = parts[1].strip()
                    elif "REFERENCES" in references:
                        parts = references.split("REFERENCES")
                        if len(parts) > 1:
                            references_from_refs = parts[1].strip()
                    elif "IMPORTANT NOTICE: REFERENCE LIMITATION" in references:
                        # If we couldn't get references, include the notice
                        references_from_refs = references
                except Exception as e:
                    # If there's an error getting references, show a message
                    references_from_refs = f"""
## Error Retrieving References

There was an error retrieving references: {str(e)}

Please check your Google API credentials and try again.
"""
        
        # Create the result dictionary
        result = {
            "original_question": current_query,
            "refined_question": refined_question,
            "response": response,
            "references": references_from_refs,
            "query_evaluation": evaluation
        }
        
        # Save to session state
        st.session_state.query_result = result
        
        # Save to history
        history_item = {
            'original_question': result['original_question'],
            'refined_question': result['refined_question'],
            'response': result['response'],
            'query_evaluation': result['query_evaluation'],
            'references': result['references']
        }
        save_to_history(history_item)
        
        # Clear the processing state
        st.session_state.is_processing = False
        
        # Clear the current query
        st.session_state.current_query = None
        
        # Force a rerun to update the UI
        st.rerun()
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        # Clear the processing state even if there's an error
        st.session_state.is_processing = False
        # Clear the current query
        st.session_state.current_query = None 