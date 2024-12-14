#!/bin/bash

echo "🌤️ Setting up Weather Forecasting ML Application..."

# Function to check Python version
check_python() {
    if command -v python3 &> /dev/null; then
        echo "✅ Python 3 detected"
        return 0
    else
        echo "❌ Python 3 is required but not installed."
        echo "Please install Python 3.8 or higher and try again."
        exit 1
    fi
}

# Function to create virtual environment
create_venv() {
    echo "📦 Creating virtual environment..."
    if [ -d "venv" ]; then
        echo "Virtual environment already exists, skipping creation."
    else
        python3 -m venv venv
    fi
    
    # Activate virtual environment based on OS
    if [ "$(uname)" == "Darwin" ] || [ "$(uname)" == "Linux" ]; then
        source venv/bin/activate
    elif [ "$(uname -s | cut -c 1-5)" == "MINGW" ] || [ "$(uname -s | cut -c 1-4)" == "MSYS" ]; then
        source venv/Scripts/activate
    else
        echo "❌ Unsupported operating system"
        exit 1
    fi
}

# Function to install dependencies
install_dependencies() {
    echo "📥 Installing required packages..."
    python3 -m pip install --upgrade pip
    if [ -f requirements.txt ]; then
        pip install -r requirements.txt
    else
        pip install streamlit pandas numpy scikit-learn plotly requests
        pip freeze > requirements.txt
        echo "✅ Generated requirements.txt"
    fi
}

# Function to setup environment file
setup_env() {
    if [ ! -f .env ]; then
        echo "🔑 Creating .env file..."
        echo "OPENWEATHERMAP_API_KEY=your_api_key_here" > .env
        echo "⚠️ Please update the .env file with your OpenWeatherMap API key"
    else
        echo "✅ .env file already exists"
    fi
}

# Main setup process
echo "🚀 Starting setup process..."
check_python
create_venv
install_dependencies
setup_env

echo "✨ Setup completed successfully!"
echo "
🎉 To run the application:
1. Activate the virtual environment:
   - On macOS/Linux: source venv/bin/activate
   - On Windows: .\\venv\\Scripts\\activate
2. Run the application:
   streamlit run main.py

⭐ Don't forget to update your OpenWeatherMap API key in the .env file!
"
