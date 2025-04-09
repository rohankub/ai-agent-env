import os
import shutil
import subprocess
import argparse

def create_requirements_file():
    """Create a requirements.txt file for deployment"""
    requirements = [
        "streamlit>=1.22.0",
        "langchain>=0.0.267",
        "langchain-community>=0.0.10",
        "openai>=0.27.0",
        "python-dotenv>=1.0.0",
        "requests>=2.28.0"
    ]
    
    with open("requirements.txt", "w") as f:
        f.write("\n".join(requirements))
    
    print("✅ Created requirements.txt")

def create_readme():
    """Create a README.md file for the repository"""
    readme_content = """# AI Agent Interface

An intelligent AI agent that evaluates query types, refines questions, and provides comprehensive responses.

## Features

- **Query Evaluation**: Automatically determines if your query is scientific, balanced, or creative
- **Question Refinement**: Transforms simple questions into comprehensive queries
- **Structured Responses**: Provides well-organized responses with headings and bullet points
- **Reference Support**: Includes references for factual queries
- **History Tracking**: Saves your previous queries and responses
- **Feedback System**: Rate responses to help improve the system
- **Dark Mode**: Toggle between light and dark themes

## How to Use

1. Enter your question in the text area at the bottom of the screen
2. Click "Submit" to get a response
3. View your response at the top of the page
4. Optionally provide feedback with the 👍 or 👎 buttons
5. Access your query history from the History page
6. Customize settings from the Settings page

## Deployment

This application can be deployed to Streamlit Cloud:

1. Fork this repository
2. Connect your Streamlit Cloud account to your GitHub account
3. Deploy the app from the Streamlit Cloud dashboard
4. Set the required environment variables (OPENAI_API_KEY)

## Local Development

To run this application locally:

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Environment Variables

The following environment variables are required:

- `OPENAI_API_KEY`: Your OpenAI API key

## License

MIT
"""
    
    with open("README.md", "w") as f:
        f.write(readme_content)
    
    print("✅ Created README.md")

def create_gitignore():
    """Create a .gitignore file"""
    gitignore_content = """# Environment variables
.env

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/
ai-agent-env/

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
"""
    
    with open(".gitignore", "w") as f:
        f.write(gitignore_content)
    
    print("✅ Created .gitignore")

def create_streamlit_config():
    """Create a streamlit config file"""
    os.makedirs(".streamlit", exist_ok=True)
    
    config_content = """[theme]
primaryColor = "#3b82f6"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
maxUploadSize = 200
timeout = 300
"""
    
    with open(".streamlit/config.toml", "w") as f:
        f.write(config_content)
    
    print("✅ Created .streamlit/config.toml")

def prepare_for_deployment(args):
    """Prepare the project for deployment"""
    print("Preparing project for deployment...")
    
    # Create necessary files
    create_requirements_file()
    create_readme()
    create_gitignore()
    create_streamlit_config()
    
    # Initialize git repository if requested
    if args.git:
        try:
            subprocess.run(["git", "init"], check=True)
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)
            print("✅ Initialized git repository")
        except subprocess.CalledProcessError:
            print("❌ Failed to initialize git repository")
    
    print("\nDeployment preparation complete!")
    print("\nTo deploy to Streamlit Cloud:")
    print("1. Push this repository to GitHub")
    print("2. Connect your Streamlit Cloud account to your GitHub account")
    print("3. Deploy the app from the Streamlit Cloud dashboard")
    print("4. Set the required environment variables (OPENAI_API_KEY)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prepare the AI Agent Interface for deployment")
    parser.add_argument("--git", action="store_true", help="Initialize a git repository")
    args = parser.parse_args()
    
    prepare_for_deployment(args) 