# 🌤️ Taylor's Weather Forecasting with ML

An advanced weather forecasting application that combines real-time weather data with machine learning capabilities. This project features an interactive interface for model training, weather data visualization, and intelligent weather predictions.

## ✨ Features

- **Real-time Weather Data**: Get current weather conditions for any city
- **5-Day Weather Forecast**: View detailed weather predictions for the next 5 days
- **Machine Learning Models**:
  - Random Forest
  - XGBoost
  - Linear Regression
- **Interactive Data Visualization**:
  - Temperature trends with confidence intervals
  - Feature importance analysis
  - Correlation matrices
- **Model Performance Metrics**:
  - RMSE (Root Mean Square Error)
  - Cross-validation scores
  - R² Score

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- OpenWeatherMap API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/weather-forecast-ml.git
cd weather-forecast-ml
```

2. Install required packages:
```bash
pip install streamlit pandas numpy scikit-learn plotly requests
```

3. Set up your environment variables:
Create a `.env` file in the root directory and add your OpenWeatherMap API key:
```
OPENWEATHERMAP_API_KEY=your_api_key_here
```

### Running the Application

Start the application by running:
```bash
streamlit run main.py
```

The application will be available at `http://localhost:5000`

## 📊 Features in Detail

### Weather Data
- Real-time weather information
- Historical weather data analysis
- Interactive temperature trend visualization
- Weather parameter correlation analysis

### Machine Learning Capabilities
- Multiple ML model options
- Cross-validation for robust evaluation
- Feature importance analysis
- Interactive model performance visualization

### Data Visualization
- Temperature trends with confidence intervals
- Correlation matrices
- Feature importance plots
- Actual vs Predicted comparisons

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check [issues page](https://github.com/yourusername/weather-forecast-ml/issues).

## 👥 Authors

- Initial work - [Your Name]

## 🙏 Acknowledgments

- OpenWeatherMap API for weather data
- Streamlit for the web interface
- Scikit-learn for machine learning capabilities
