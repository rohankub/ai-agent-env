import traceback
from agent.core import create_agent
from refiners import pre_refine_query
from query_evaluator import evaluate_query

def process_query(question):
    """
    Process a question with query evaluation, appropriate pre-refinement, and get references if needed.
    
    Args:
        question: The original user question
    """
    try:
        # Step 1: Evaluate the query to determine temperature and whether references are needed
        print("\nEvaluating query type...")
        evaluation = evaluate_query(question)
        temperature = evaluation["temperature"]
        query_type = evaluation["query_type"]
        requires_references = evaluation["requires_references"]
        
        print(f"Query type: {query_type}")
        print(f"Temperature: {temperature}")
        print(f"Requires references: {requires_references}")
        
        # Display reference warning if present
        if "reference_warning" in evaluation and evaluation["reference_warning"]:
            print(f"\nWARNING: {evaluation['reference_warning']}")
        
        # Store the original question
        original_question = question
        
        # Step 2: Pre-refine the query based on its type and temperature
        print("\nPre-refining the query...")
        refined_question = pre_refine_query(question, query_type, temperature)
        print(f"Original question: {question}")
        print(f"Refined question: {refined_question}")
        
        # Step 3: Create an agent with the appropriate temperature
        agent = create_agent(temperature)
        
        # Step 4: Get the response from the agent with instructions for comprehensive answers
        print("\nGenerating response...")
        response = get_comprehensive_response(agent, refined_question)
        
        # Step 5: Get references if required
        references = ""
        references_from_refs = ""
        if requires_references:
            print("\nFetching references...")
            references_result = agent.invoke({"input": f"Find detailed, authoritative references about: {refined_question}"})
            references = references_result["output"]
            
            # Process references and enhance response if needed
            references_from_refs, additional_info = process_references(references, response)
            
            # Combine the response with additional info if available
            if additional_info:
                response = f"{response}\n{additional_info}"
        
        # Return the results
        return {
            "original_question": original_question,
            "refined_question": refined_question,
            "response": response,
            "references": references_from_refs,
            "query_evaluation": evaluation
        }
    except Exception as e:
        print(f"Error in process_query: {str(e)}")
        print(traceback.format_exc())
        # Return a basic response in case of error
        return {
            "original_question": question,
            "refined_question": question,
            "response": f"I encountered an error while processing your query. Please try again or rephrase your question. Error: {str(e)}",
            "references": "",
            "query_evaluation": {"query_type": "balanced", "temperature": 0.5, "requires_references": False, "reasoning": "Default due to error"}
        }

def get_comprehensive_response(agent, refined_question):
    """
    Get a comprehensive response from the agent.
    
    Args:
        agent: The initialized agent
        refined_question: The refined question to ask
    """
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
    response = agent.invoke({"input": response_prompt})["output"]
    return response

def process_references(references, response):
    """
    Process references and extract useful information.
    
    Args:
        references: The references text
        response: The current response
    
    Returns:
        tuple: (references_from_refs, additional_info)
    """
    # Extract the summary from references if available
    summary_from_refs = ""
    if "SUMMARY" in references:
        parts = references.split("SUMMARY")
        if len(parts) > 1:
            summary_parts = parts[1].split("REFERENCES")
            if len(summary_parts) > 0:
                summary_from_refs = summary_parts[0].strip()
    
    # Extract the references from the response
    references_from_refs = ""
    if "REFERENCES" in references:
        parts = references.split("REFERENCES")
        if len(parts) > 1:
            references_from_refs = parts[1].strip()
    
    # Prepare additional info if summary is available and not already in response
    additional_info = ""
    if summary_from_refs and summary_from_refs not in response:
        additional_info = f"\n\n## Additional Information\n{summary_from_refs}"
    
    return references_from_refs, additional_info 