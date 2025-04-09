import streamlit as st
import os
from styles import inject_styles
from utils import initialize_session_state, process_and_clear
from ui_components import input_area
from sidebar import render_sidebar
from pages import render_chat_page, render_history_page, render_settings_page
from agent.query_processor import process_query

# Increase Streamlit's server timeout (needs to be set before the app starts)
os.environ['STREAMLIT_SERVER_MAX_UPLOAD_SIZE'] = '200'  # 200 MB
os.environ['STREAMLIT_SERVER_TIMEOUT'] = '300'  # 300 seconds (5 minutes)

# Set page configuration
st.set_page_config(
    page_title="AI Agent Interface",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize styles and session state
inject_styles()
initialize_session_state()

# Input area at the top
input_area(process_and_clear)

# Render the sidebar
render_sidebar()

# Main content area based on selected page
if st.session_state.page == "History":
    render_history_page()
elif st.session_state.page == "Settings":
    render_settings_page()
else:  # Chat page (default)
    render_chat_page()

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<div class='footer-text'>Powered by LangChain and OpenAI</div>", unsafe_allow_html=True)

# Process the query if in processing state
if st.session_state.is_processing and st.session_state.current_query:
    process_query()