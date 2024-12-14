#!/bin/bash

echo "Setting up Weather Forecasting ML Application..."

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed. Please install Python 3 and try again."
    exit 1
fi

# Create and activate virtual environment (optional)
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null

# Install required packages
echo "Installing required packages..."
pip install --upgrade pip
pip install -r requirements.txt 2>/dev/null || pip install streamlit pandas numpy scikit-learn plotly requests

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    echo "OPENWEATHERMAP_API_KEY=your_api_key_here" > .env
    echo "Please update the .env file with your OpenWeatherMap API key"
fi

echo "Setup completed! You can now run the application using:"
echo "streamlit run main.py"

# Reminder about API key
echo -e "\nIMPORTANT: Make sure to set your OpenWeatherMap API key in the .env file"
