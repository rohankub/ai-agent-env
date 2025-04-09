import streamlit as st

def inject_styles():
    st.markdown("""
    <style>
    /* Base styles */
    .main { padding: 1rem; }
    
    /* Remove white bars in dark mode */
    .stApp {
        background-color: #0e1117;
    }
    
    /* Remove white horizontal bars */
    [data-testid="stAppViewContainer"] > div:first-child {
        border: none;
        background-color: transparent;
    }
    
    [data-testid="stHeader"] {
        background-color: transparent;
        border-bottom: none;
    }
    
    [data-testid="stToolbar"] {
        display: none;
    }
    
    [data-testid="stDecoration"] {
        display: none;
    }
    
    /* Remove white horizontal bars at the top and bottom */
    [data-testid="stAppViewContainer"] > div:first-child,
    [data-testid="stAppViewContainer"] > div:last-child {
        border: none !important;
        background-color: transparent !important;
    }
    
    /* Ensure consistent dark background */
    .dark-mode [data-testid="stAppViewContainer"],
    .dark-mode [data-testid="stHeader"],
    .dark-mode [data-testid="stSidebar"],
    .dark-mode [data-testid="stAppViewContainer"] > div {
        background-color: #1f2937 !important;
        border: none !important;
    }
    
    .input-container {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 20px;
        border: 1px solid #e5e7eb;
    }
    
    .input-prompt {
        font-size: 1rem;
        color: #4b5563;
        margin-bottom: 10px;
    }
    
    .stButton > button {
        background-color: #f94144;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    .stButton > button:hover {
        background-color: #e71d36;
    }
    
    .question-container {
        display: flex;
        margin-bottom: 0.5rem;
        background-color: #f9fafb;
        border-radius: 8px;
        padding: 8px;
        border: 1px solid #e5e7eb;
    }
    
    .question-label {
        font-weight: bold;
        min-width: 80px;
        color: #4b5563;
    }
    
    .question-text { flex-grow: 1; }
    
    .temp-badge {
        display: inline-block;
        background-color: #e0e7ff;
        color: #3730a3;
        font-size: 0.8rem;
        padding: 2px 8px;
        border-radius: 12px;
        margin-left: 8px;
        font-weight: 500;
    }
    
    .processing-indicator {
        background-color: #f9fafb;
        border-radius: 8px;
        padding: 16px;
        margin: 20px 0;
        border: 1px solid #e5e7eb;
        color: #4b5563;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .intermediate-content {
        color: #6b7280;
        font-style: italic;
        margin-bottom: 1rem;
        padding: 0.5rem;
        border-left: 3px solid #d1d5db;
    }
    
    .copy-btn-container {
        display: flex;
        justify-content: flex-end;
        margin-top: 0.5rem;
    }
    
    .copy-btn {
        background-color: #f3f4f6;
        border: 1px solid #d1d5db;
        border-radius: 4px;
        padding: 0.25rem 0.5rem;
        font-size: 0.8rem;
        cursor: pointer;
        color: #4b5563;
    }
    
    .copy-btn:hover {
        background-color: #e5e7eb;
    }
    
    /* Dark mode styles */
    .dark-mode {
        background-color: #1f2937;
        color: #f3f4f6;
    }
    
    .dark-mode .input-container {
        background-color: #374151;
        border-color: #4b5563;
    }
    
    .dark-mode .question-container {
        background-color: #374151;
        border-color: #4b5563;
    }
    
    .dark-mode .processing-indicator {
        background-color: #374151;
        border-color: #4b5563;
        color: #e5e7eb;
    }
    
    .dark-mode .copy-btn {
        background-color: #374151;
        border-color: #4b5563;
        color: #e5e7eb;
    }
    
    .dark-mode .temp-badge {
        background-color: #1e3a8a;
        color: #bfdbfe;
    }
    
    /* Additional dark mode fixes for Streamlit elements */
    .dark-mode .stTextInput > div > div {
        background-color: #374151;
        color: #f3f4f6;
        border-color: #4b5563;
    }
    
    .dark-mode .stTextArea > div > div {
        background-color: #374151;
        color: #f3f4f6;
        border-color: #4b5563;
    }
    
    .dark-mode .stTabs [data-baseweb="tab-list"] {
        background-color: #1f2937;
        border-color: #4b5563;
    }
    
    .dark-mode .stTabs [data-baseweb="tab"] {
        color: #f3f4f6;
    }
    
    .dark-mode .stTabs [aria-selected="true"] {
        background-color: #374151;
        color: #f3f4f6;
    }
    
    /* Remove any remaining white bars */
    .dark-mode [data-testid="stVerticalBlock"] {
        background-color: #1f2937;
        border: none;
    }
    
    /* Remove fixed positioning */
    .fixed-top, .fixed-bottom {
        position: static !important;
        box-shadow: none !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
        display: block !important;
    }
    
    /* Properly style Markdown headings */
    h1 {
        font-size: 1.8em;
        margin-top: 1em;
        margin-bottom: 0.5em;
        color: #1e3a8a;
        font-weight: 600;
    }
    
    h2 {
        font-size: 1.5em;
        margin-top: 0.8em;
        margin-bottom: 0.4em;
        color: #1e3a8a;
        font-weight: 600;
    }
    
    h3 {
        font-size: 1.2em;
        margin-top: 0.6em;
        margin-bottom: 0.3em;
        color: #2563eb;
        font-weight: 600;
    }
    
    /* Style for code blocks */
    pre {
        background-color: #f1f5f9;
        padding: 0.7em;
        border-radius: 4px;
        overflow-x: auto;
        margin-bottom: 1em;
    }
    
    code {
        background-color: #f1f5f9;
        padding: 2px 4px;
        border-radius: 4px;
        font-family: monospace;
    }
    
    /* Hide streamlit footer */
    footer {
        display: none !important;
    }
    
    /* Divider style */
    hr {
        margin: 1.5rem 0;
        border: 0;
        border-top: 1px solid #e5e7eb;
    }
    
    /* Footer text */
    .footer-text {
        color: #6b7280;
        font-size: 0.9rem;
        text-align: center;
        margin-top: 2rem;
    }
    
    /* Remove info messages styling */
    .stAlert {
        border: none !important;
        background-color: transparent !important;
    }
    
    /* Clean up the interface */
    .clean-interface {
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    
    /* Hide default Streamlit elements */
    .stDeployButton, [data-testid="stDecoration"] {
        display: none !important;
    }
    
    /* Processing indicator */
    .processing-indicator {
        background-color: #f9fafb;
        border-radius: 8px;
        padding: 16px;
        margin: 20px 0;
        border: 1px solid #e5e7eb;
        color: #4b5563;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .processing-indicator .stSpinner {
        margin-right: 10px;
    }
    
    /* Loader animation */
    .loader {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(0, 0, 0, 0.1);
        border-radius: 50%;
        border-top-color: #3b82f6;
        animation: spin 1s ease-in-out infinite;
        margin-left: 10px;
        vertical-align: middle;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Dark mode loader */
    .dark-mode .loader {
        border-color: rgba(255, 255, 255, 0.1);
        border-top-color: #60a5fa;
    }
    
    /* Dark mode styles */
    .dark-mode h1, .dark-mode h2 {
        color: #93c5fd;
    }
    
    .dark-mode h3 {
        color: #60a5fa;
    }
    
    .dark-mode pre, .dark-mode code {
        background-color: #1f2937;
    }
    
    .dark-mode .copy-btn:hover {
        background-color: #4b5563;
    }
    
    .dark-mode .footer-text {
        color: #9ca3af;
    }
    
    .dark-mode hr {
        border-top-color: #4b5563;
    }
    
    /* Example question chips */
    .example-chips {
        margin-top: 10px;
    }
    
    .example-chips button {
        background-color: #f3f4f6 !important;
        color: #4b5563 !important;
        border: 1px solid #e5e7eb !important;
        font-size: 0.8rem !important;
        padding: 0.25rem 0.5rem !important;
        height: auto !important;
        min-height: 0 !important;
    }
    
    .example-chips button:hover {
        background-color: #e5e7eb !important;
        border-color: #d1d5db !important;
    }
    
    .dark-mode .example-chips button {
        background-color: #374151 !important;
        color: #e5e7eb !important;
        border-color: #4b5563 !important;
    }
    
    .dark-mode .example-chips button:hover {
        background-color: #4b5563 !important;
        border-color: #6b7280 !important;
    }
    
    /* Feedback button styling */
    .feedback-button {
        width: 100%;
        height: 45px;
        text-align: center;
        border-radius: 5px;
        background-color: #f63366;
        color: white;
        border: none;
        cursor: pointer;
    }
    
    /* Feedback buttons styling */
    .stButton > button {
        width: 100%;
        height: 45px;
        border-radius: 5px;
        font-weight: 500;
    }
    
    /* Make sure the text in the Not Helpful button is properly centered */
    div[data-testid="column"] > div > div > div > div > div > button {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    </style>
    
    <script>
    function copyToClipboard(text) {
        navigator.clipboard.writeText(text);
        alert('Copied to clipboard!');
    }

    // Function to toggle dark mode
    function toggleDarkMode(isDark) {
        if (isDark) {
            document.body.classList.add('dark-mode');
        } else {
            document.body.classList.remove('dark-mode');
        }
    }
    </script>
    """, unsafe_allow_html=True) 