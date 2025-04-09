import streamlit as st
from utils import clear_history, copy_to_clipboard
from ui_components import display_response, display_processing_indicator

def render_chat_page():
    """Render the main chat page"""
    # Display the response area
    with st.container():
        # Display results if available
        if st.session_state.query_result:
            # Clear the processing state once we have results
            st.session_state.is_processing = False
            display_response(st.session_state.query_result)
        
        # Show processing status if currently processing
        elif st.session_state.is_processing and st.session_state.current_query:
            display_processing_indicator()

def render_history_page():
    """Render the history page"""
    with st.container():
        st.title("📚 Query History")
        
        if not st.session_state.history:
            # Empty space if no history
            pass
        else:
            # Add clear history button
            if st.button("Clear History"):
                clear_history()
            
            # Display history items
            for i, item in enumerate(st.session_state.history):
                with st.expander(f"Query: {item['original_question']}", expanded=False):
                    st.markdown(f"**Timestamp:** {item['timestamp']}")
                    st.markdown(f"**Refined Question:** {item['refined_question']}")
                    st.markdown("**Response:**")
                    st.markdown(item['response'])
                    
                    # Copy button for response
                    copy_to_clipboard(item['response'], "Copy Response")

def render_settings_page():
    """Render the settings page"""
    with st.container():
        st.title("⚙️ Settings")
        
        st.subheader("Display Settings")
        st.markdown("Customize the appearance and behavior of the AI Agent Interface.")
        
        # Settings are handled in the sidebar
        
        st.subheader("About")
        st.markdown("""
        **AI Agent Interface**
        
        Version: 1.0.0
        
        This application uses LangChain and OpenAI to provide intelligent responses to your questions.
        The system evaluates your query type, refines your question, and generates comprehensive responses.
        
        Built with ❤️ using Python, LangChain, and Streamlit.
        """) 