#!/bin/bash

echo "Setting up Weather Forecasting ML Application..."

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed. Please install Python 3 and try again."
    exit 1
fi

# Install required packages
echo "Installing required packages..."
pip install streamlit pandas numpy scikit-learn plotly requests

echo "Setup completed! You can now run the application using:"
echo "streamlit run main.py"
