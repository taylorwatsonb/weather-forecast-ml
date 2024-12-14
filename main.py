import streamlit as st
import pandas as pd
from utils.data_processor import WeatherDataProcessor
from utils.ml_models import WeatherPredictor
from utils.visualizations import WeatherVisualizer
from utils.weather_api import WeatherAPI

# Page configuration
st.set_page_config(
    page_title="Weather Forecast ML",
    page_icon="🌤️",
    layout="wide"
)

# Initialize session state
if 'data_processor' not in st.session_state:
    st.session_state.data_processor = WeatherDataProcessor()
if 'predictor' not in st.session_state:
    st.session_state.predictor = WeatherPredictor()
if 'visualizer' not in st.session_state:
    st.session_state.visualizer = WeatherVisualizer()
if 'weather_api' not in st.session_state:
    st.session_state.weather_api = WeatherAPI()

# Add city selection to session state
if 'selected_city' not in st.session_state:
    st.session_state.selected_city = "San Francisco"

# App title and description
st.title("🌤️ Taylor's Weather Forecasting with ML")
st.markdown("""
This application uses machine learning to analyze and predict weather patterns.
Upload your weather data or use sample data to explore the predictions.
""")

# Sidebar
with st.sidebar:
    st.header("Data Input")
    data_option = st.radio(
        "Choose data source:",
        ("Upload Data", "Use Sample Data")
    )
    
    if data_option == "Upload Data":
        uploaded_file = st.file_uploader(
            "Upload CSV file",
            type=['csv'],
            help="Upload a CSV file with columns: date, temperature, humidity, pressure"
        )
        if uploaded_file is not None:
            df, message = st.session_state.data_processor.process_uploaded_data(uploaded_file)
            if df is not None:
                st.success(message)
            else:
                st.error(message)
    else:
        if st.button("Generate Sample Data"):
            with st.spinner("Generating sample weather data..."):
                df = st.session_state.data_processor.generate_sample_data()
                st.success("✨ Sample data generated! Scroll down to see the analysis.")
                st.balloons()

# Real-time Weather Section
st.header("🌡️ Real-time Weather")
col1, col2 = st.columns([1, 2])

with col1:
    st.session_state.selected_city = st.text_input("City", value=st.session_state.selected_city)
    if st.button("Update Weather"):
        with st.spinner("Fetching weather data..."):
            current_weather = st.session_state.weather_api.get_current_weather(st.session_state.selected_city)
            forecast = st.session_state.weather_api.get_forecast(st.session_state.selected_city)
            
            if current_weather == "API_INACTIVE":
                st.warning("The weather API key is still being activated. This usually takes 2-4 hours after registration. Please try again later.")
            elif current_weather is None:
                st.error(f"Could not find weather data for '{st.session_state.selected_city}'. Please enter a valid city name (e.g., 'Austin' instead of 'Texas').")
            else:
                st.session_state.current_weather = current_weather
                st.session_state.forecast = forecast

with col2:
    if 'current_weather' in st.session_state and st.session_state.current_weather:
        weather = st.session_state.current_weather
        st.markdown(f"""
        ### Current Conditions in {st.session_state.selected_city}
        - Temperature: {weather['temperature']}°C (Feels like: {weather['feels_like']}°C)
        - Conditions: {weather['description']}
        - Humidity: {weather['humidity']}%
        - Wind Speed: {weather['wind_speed']} m/s
        - Last Updated: {weather['timestamp']}
        """)

if 'forecast' in st.session_state and st.session_state.forecast:
    st.subheader("📅 5-Day Forecast")
    forecast_cols = st.columns(5)
    for idx, forecast in enumerate(st.session_state.forecast[:5]):
        with forecast_cols[idx]:
            st.markdown(f"""
                #### {forecast['timestamp'].strftime("%A")}
                ##### {forecast['timestamp'].strftime("%b %d")}
                **{forecast['temperature']}°C**
                {forecast['description']}
                
                💧 Humidity: {forecast['humidity']}%  
                💨 Wind: {forecast['wind_speed']} m/s
            """)
            # Add a separator between days
            if idx < 4:  # Don't add after the last column
                st.markdown("---")

# Historical Data Analysis
st.header("📊 Historical Data Analysis")
if st.session_state.data_processor.data is not None:
    # Data Overview
    st.header("Data Overview")
    col1, col2 = st.columns(2)
    
    with col1:
        st.dataframe(st.session_state.data_processor.data.head())
    
    with col2:
        st.plotly_chart(
            st.session_state.visualizer.plot_correlation_matrix(
                st.session_state.data_processor.data
            ),
            use_container_width=True
        )

    # Temperature Trend
    st.header("Temperature Trend")
    st.plotly_chart(
        st.session_state.visualizer.plot_temperature_trend(
            st.session_state.data_processor.data
        ),
        use_container_width=True
    )

    # ML Model Training and Prediction
    st.header("ML Model Analysis")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Model Configuration")
        model_option = st.selectbox(
            "Select ML Model",
            ["Linear Regression", "Random Forest", "XGBoost"],
            help="Choose the machine learning model for weather prediction"
        )
    with col2:
        st.subheader("Training")
        train_button = st.button("Train Model")
    
    if train_button:
        X, y = st.session_state.data_processor.prepare_ml_data()
        if X is not None and y is not None:
            with st.spinner(f'🤖 Training {model_option} model... This may take a moment.'):
                results = st.session_state.predictor.train_model(X, y, model_option)
            
            if results:
                st.success(f"✅ {model_option} model trained successfully!")
                
                # Model Performance Metrics
                st.subheader("📊 Model Performance")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Root Mean Square Error (RMSE)", 
                             f"{results['rmse']:.2f}",
                             help="Lower RMSE indicates better predictions")
                with col2:
                    st.metric("R² Score", 
                             f"{results['r2']:.2f}",
                             help="Higher R² indicates better fit (max: 1.0)")
                
                # Predictions Plot
                st.subheader("Model Predictions vs Actual Values")
                st.plotly_chart(
                    st.session_state.visualizer.plot_prediction_results(
                        results['test_actual'],
                        results['test_predictions'],
                        results['test_features'].index
                    ),
                    use_container_width=True
                )
                
                # Feature Importance Plot
                if results['feature_importance'] is not None:
                    st.subheader("Feature Importance Analysis")
                    st.plotly_chart(
                        st.session_state.visualizer.plot_feature_importance(
                            results['feature_importance']
                        ),
                        use_container_width=True
                    )
            else:
                st.error("Error training the model")
        else:
            st.error("Error preparing data for training")

else:
    st.info("Please upload data or generate sample data to begin analysis")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Built with Streamlit • Data Science • Machine Learning</p>
</div>
""", unsafe_allow_html=True)
