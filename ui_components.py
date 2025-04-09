import streamlit as st
from utils import copy_to_clipboard
import os

def input_area(process_and_clear):
    """Render the input area with text input and submit button"""
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_area(
            "User input",
            placeholder="Ask a question...",
            height=100,
            label_visibility="collapsed",
            key="user_input",
            on_change=process_and_clear
        )
    with col2:
        st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
        submit_button = st.button(
            "Submit",
            type="primary",
            use_container_width=True,
            on_click=process_and_clear
        )
    st.markdown('</div>', unsafe_allow_html=True)

def display_response(result):
    """Display the query response with tabs"""
    st.markdown('<div class="question-container">', unsafe_allow_html=True)
    st.markdown('<div class="question-label">Question:</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="question-text">{result["original_question"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Check if references are required but API keys are not available
    eval_data = result['query_evaluation']
    if eval_data.get('requires_references', False):
        google_api_key = os.environ.get("GOOGLE_API_KEY")
        google_cse_id = os.environ.get("GOOGLE_CSE_ID")
        
        if (not google_api_key or google_api_key == "YOUR_GOOGLE_API_KEY_HERE" or 
            not google_cse_id or google_cse_id == "YOUR_CUSTOM_SEARCH_ENGINE_ID_HERE"):
            st.warning("References were requested but are currently unavailable. The reference feature requires Google API credentials to be configured.")
    
    # Display reference warning if present
    if 'reference_warning' in eval_data:
        st.info(eval_data['reference_warning'])
    
    # Create tabs
    tab_labels = ["Response"]
    if st.session_state.show_details:
        tab_labels.append("Query Details")
        if result["references"]:
            tab_labels.append("References")
    
    tabs = st.tabs(tab_labels)
    
    # Response tab
    with tabs[0]:
        st.markdown(result["response"], unsafe_allow_html=False)
        copy_to_clipboard(result['response'], "Copy Response")
        
        # Feedback buttons
        col1, col2, col3 = st.columns([1, 1, 5])
        with col1:
            if st.button("👍 Helpful", key="helpful_button_response", use_container_width=True):
                st.success("Thank you for your feedback!")
                st.session_state.current_feedback = True
        with col2:
            if st.button("👎 Not Helpful", key="not_helpful_button_response", use_container_width=True):
                st.error("We'll try to improve!")
                st.session_state.current_feedback = False
    
    # Query Details tab
    if st.session_state.show_details and len(tabs) > 1:
        with tabs[1]:
            st.markdown('<div class="response-header">Query Evaluation</div>', unsafe_allow_html=True)
            eval_html = f"""
            <div class='evaluation'>
                <strong>Type:</strong> {eval_data['query_type']}<br>
                <strong>Temperature:</strong> {eval_data['temperature']}<br>
                <strong>Requires References:</strong> {eval_data['requires_references']}<br>
                <strong>Reasoning:</strong> {eval_data['reasoning']}
            </div>
            """
            st.markdown(eval_html, unsafe_allow_html=True)
            
            st.markdown('<div class="response-header">Processing Details</div>', unsafe_allow_html=True)
            st.markdown(f"""
            - **Original Question**: {result['original_question']}
            - **Refined Question**: {result['refined_question']}
            - **Query Type**: {eval_data['query_type']}
            - **Temperature**: {eval_data['temperature']}
            """)
    
    # References tab
    if st.session_state.show_details and result["references"] and len(tabs) > 2:
        with tabs[2]:
            st.markdown('<div class="response-header">References</div>', unsafe_allow_html=True)
            st.markdown(f"<div class='references'>{result['references']}</div>", unsafe_allow_html=True)

def display_processing_indicator():
    """Display the processing indicator"""
    with st.container():
        st.markdown('<div class="processing-indicator">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 3])
        with col1:
            st.spinner()
        with col2:
            if 'current_query' in st.session_state and st.session_state.current_query:
                st.markdown(f"<div style='padding: 10px 0;'>Processing query: <strong>{st.session_state.current_query}</strong></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='padding: 10px 0;'>Processing your query...</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True) 