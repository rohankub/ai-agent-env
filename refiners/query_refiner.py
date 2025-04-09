from refiners.scientific_refiner import create_scientific_refiner_agent
from refiners.creative_refiner import create_creative_refiner_agent
from refiners.balanced_refiner import create_balanced_refiner_agent

def pre_refine_query(question, query_type="balanced", temperature=0.3):
    """
    Use the appropriate refiner agent to improve a query before getting any responses.
    
    Args:
        question: The original user question
        query_type: The type of query ("scientific", "balanced", or "creative")
        temperature: The temperature to use for the language model
    """
    # Select the appropriate refiner based on query type
    if query_type == "scientific":
        llm, refiner_prompt = create_scientific_refiner_agent(temperature)
    elif query_type == "creative":
        llm, refiner_prompt = create_creative_refiner_agent(temperature)
    else:  # balanced or default
        llm, refiner_prompt = create_balanced_refiner_agent(temperature)
    
    # Format the prompt with just the question
    formatted_prompt = refiner_prompt.format(
        question=question
    )
    
    # Get the refined query
    refined_query = llm.invoke(formatted_prompt)
    
    return refined_query.content