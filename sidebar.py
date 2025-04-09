import streamlit as st

def render_sidebar():
    """Render the sidebar with all its components"""
    with st.sidebar:
        st.header("About this Agent")
        st.markdown("""
        This AI agent uses a sophisticated system to:
        
        1. **Evaluate** your query type (scientific, balanced, or creative)
        2. **Refine** your question to get better results
        3. **Generate** a comprehensive response
        4. **Provide** references when appropriate
        
        Try different types of questions to see how the agent adapts!
        """)
        
        # Query Types
        st.subheader("Query Types")
        st.markdown("""
        * **Scientific** (temperature 0.1-0.3):
          Technical, academic topics
        
        * **Balanced** (temperature 0.4-0.6):
          General knowledge, places, people
        
        * **Creative** (temperature 0.7-0.9):
          Stories, poems, creative content
        """)
        
        # Options section
        st.subheader("Options")
        show_processing = st.checkbox(
            "Show processing details",
            value=st.session_state.show_processing
        )
        st.session_state.show_processing = show_processing
        
        show_details = st.checkbox(
            "Show details (references & evaluation)",
            value=st.session_state.show_details
        )
        st.session_state.show_details = show_details
        
        dark_mode = st.checkbox(
            "Dark mode",
            value=st.session_state.dark_mode
        )
        if dark_mode != st.session_state.dark_mode:
            st.session_state.dark_mode = dark_mode
            st.rerun()
        
        # Warning about long-running queries
        st.warning("Note: Comprehensive responses may take up to 5 minutes to generate.")
        
        # Navigation
        st.subheader("Navigation")
        page = st.radio(
            "Go to",
            ["Chat", "History", "Settings"],
            index=["Chat", "History", "Settings"].index(st.session_state.page)
        )
        if page != st.session_state.page:
            st.session_state.page = page
            st.rerun() 