import streamlit as st
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path

def save_to_history(item):
    """Save a query and response to history."""
    # Add timestamp
    item['timestamp'] = datetime.now().isoformat()
    
    # Add to session state
    if 'history' not in st.session_state:
        st.session_state.history = []
    
    st.session_state.history.append(item)
    
    # Save to file
    history_dir = Path("history")
    history_dir.mkdir(exist_ok=True)
    
    history_file = history_dir / "query_history.json"
    
    try:
        if history_file.exists():
            with open(history_file, "r") as f:
                history = json.load(f)
        else:
            history = []
        
        history.append(item)
        
        with open(history_file, "w") as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        st.error(f"Error saving history: {str(e)}")

def clear_history():
    """Clear the query history"""
    st.session_state.history = []
    st.success("History cleared!")

def copy_to_clipboard(text, button_text="Copy"):
    """Create a button to copy text to clipboard"""
    button_id = hashlib.md5(text.encode()).hexdigest()[:10]
    
    js_code = f"""
    <script>
    function copyToClipboard_{button_id}() {{
        const text = {json.dumps(text)};
        navigator.clipboard.writeText(text)
            .then(() => console.log('Copied to clipboard'))
            .catch(err => console.error('Failed to copy: ', err));
    }}
    </script>
    """
    
    button_html = f"""
    <div class="copy-btn-container">
        <button class="copy-btn" onclick="copyToClipboard_{button_id}()">
            {button_text} 📋
        </button>
    </div>
    """
    
    st.markdown(js_code + button_html, unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables if they don't exist."""
    if 'page' not in st.session_state:
        st.session_state.page = "Chat"
    
    if 'is_processing' not in st.session_state:
        st.session_state.is_processing = False
    
    if 'current_query' not in st.session_state:
        st.session_state.current_query = None
    
    if 'query_result' not in st.session_state:
        st.session_state.query_result = None
    
    if 'history' not in st.session_state:
        st.session_state.history = load_history()
    
    if 'settings' not in st.session_state:
        st.session_state.settings = load_settings()
        
    # UI state variables
    if 'show_processing' not in st.session_state:
        st.session_state.show_processing = False
        
    if 'show_details' not in st.session_state:
        st.session_state.show_details = True
        
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False
        
    if 'example_selected' not in st.session_state:
        st.session_state.example_selected = None
        
    if 'current_feedback' not in st.session_state:
        st.session_state.current_feedback = None
        
    if 'feedback' not in st.session_state:
        st.session_state.feedback = {}

def process_and_clear():
    """Process the query and clear the input."""
    if 'user_input' in st.session_state and st.session_state.user_input:
        query = st.session_state.user_input
        st.session_state.is_processing = True
        st.session_state.current_query = query
        st.session_state.user_input = ""
        # Clear the previous query result
        st.session_state.query_result = None

def load_history():
    """Load query history from file."""
    history_dir = Path("history")
    history_file = history_dir / "query_history.json"
    
    if history_file.exists():
        try:
            with open(history_file, "r") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error loading history: {str(e)}")
    
    return []

def load_settings():
    """Load settings from file."""
    settings_dir = Path("settings")
    settings_file = settings_dir / "app_settings.json"
    
    default_settings = {
        "theme": "light",
        "api_key": os.environ.get("OPENAI_API_KEY", ""),
        "model": "gpt-4o-mini",
        "max_tokens": 4000
    }
    
    if settings_file.exists():
        try:
            with open(settings_file, "r") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error loading settings: {str(e)}")
    
    return default_settings

def save_settings(settings):
    """Save settings to file."""
    settings_dir = Path("settings")
    settings_dir.mkdir(exist_ok=True)
    
    settings_file = settings_dir / "app_settings.json"
    
    try:
        with open(settings_file, "w") as f:
            json.dump(settings, f, indent=2)
        
        # Update session state
        st.session_state.settings = settings
        
        # Update environment variable for API key
        if "api_key" in settings and settings["api_key"]:
            os.environ["OPENAI_API_KEY"] = settings["api_key"]
            
        return True
    except Exception as e:
        st.error(f"Error saving settings: {str(e)}")
        return False 