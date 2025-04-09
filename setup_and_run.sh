#!/bin/bash

# Set the virtual environment name
VENV_NAME="ai-agent-env"

# Check if virtual environment already exists
if [ ! -d "$VENV_NAME" ]; then
    echo "Creating virtual environment..."
    python -m venv $VENV_NAME
fi

# Activate the virtual environment
source $VENV_NAME/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies with correct package names
echo "Installing required packages..."
pip install --upgrade langchain langchain-community openai requests python-dotenv streamlit

# Run the Streamlit app
echo "Starting Streamlit app..."
streamlit run streamlit_app.py

# Deactivate the virtual environment when done
deactivate
