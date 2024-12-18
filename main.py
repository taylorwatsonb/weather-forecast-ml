# Standard library imports
import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Try importing required packages
try:
    from dotenv import load_dotenv
    logger.debug("Successfully imported dotenv")
    import streamlit as st
    logger.debug("Successfully imported streamlit")
    import pandas as pd
    logger.debug("Successfully imported pandas")
    
    # Load environment variables
    load_dotenv()
    logger.debug("Environment variables loaded")
except ImportError as e:
    print(f"Error importing required packages: {str(e)}")
    sys.exit(1)

def run_app(st, WeatherDataProcessor, WeatherPredictor, WeatherVisualizer, WeatherAPI):
    # Page configuration
    st.set_page_config(
        page_title="Weather Forecast ML",
        page_icon="🌤️",
        layout="wide"
    )

    # Verify environment variables
    if not os.getenv('OPENWEATHERMAP_API_KEY'):
        st.error("OpenWeatherMap API key is missing. Please add it to your .env file.")
        st.info("You can get an API key from: https://openweathermap.org/api")
        return

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
    st.title("🌤️ Weather Forecasting with ML")
    st.markdown("""
    This application combines real-time weather data with machine learning to provide accurate weather predictions.
    Upload your own weather data or use our sample dataset to train ML models and visualize weather patterns.
    """)

    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Current Weather", "Data Analysis", "ML Model Training"])

    if page == "Current Weather":
        st.header("🌡️ Current Weather")
        city = st.text_input("Enter City Name", value=st.session_state.selected_city)
        
        if st.button("Get Weather"):
            weather_data = st.session_state.weather_api.get_current_weather(city)
            if weather_data == "API_INACTIVE":
                st.warning("Weather API key is not active yet. Please wait a few minutes and try again.")
            elif weather_data:
                st.session_state.selected_city = city
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Temperature", f"{weather_data['temperature']}°C")
                    st.metric("Humidity", f"{weather_data['humidity']}%")
                with col2:
                    st.metric("Pressure", f"{weather_data['pressure']} hPa")
                    st.metric("Wind Speed", f"{weather_data['wind_speed']} m/s")
                
                st.subheader("5-Day Forecast")
                forecast_data = st.session_state.weather_api.get_forecast(city)
                if forecast_data:
                    for forecast in forecast_data:
                        st.write(f"Date: {forecast['timestamp'].strftime('%Y-%m-%d')}")
                        st.write(f"Temperature: {forecast['temperature']}°C")
                        st.write(f"Description: {forecast['description']}")
                        st.write("---")
            else:
                st.error("Error fetching weather data. Please check the city name and try again.")

    elif page == "Data Analysis":
        st.header("📊 Data Analysis")
        
        col1, col2 = st.columns(2)
        with col1:
            uploaded_file = st.file_uploader("Upload Weather Data (CSV)", type=['csv'])
        with col2:
            if st.button("Generate Sample Data"):
                st.session_state.data_processor.generate_sample_data()
                st.success("Sample data generated successfully!")

        if uploaded_file is not None:
            data, message = st.session_state.data_processor.process_uploaded_data(uploaded_file)
            if data is not None:
                st.success(message)
            else:
                st.error(message)

        if st.session_state.data_processor.data is not None:
            st.subheader("Data Visualization")
            
            fig1 = st.session_state.visualizer.plot_temperature_trend(st.session_state.data_processor.data)
            st.plotly_chart(fig1, use_container_width=True)
            
            fig2 = st.session_state.visualizer.plot_correlation_matrix(st.session_state.data_processor.data)
            st.plotly_chart(fig2, use_container_width=True)

    elif page == "ML Model Training":
        st.header("🤖 ML Model Training")
        
        if st.session_state.data_processor.data is not None:
            model_type = st.selectbox(
                "Select Model",
                ["Linear Regression", "Random Forest", "XGBoost"]
            )
            
            if st.button("Train Model"):
                X, y = st.session_state.data_processor.prepare_ml_data()
                if X is not None and y is not None:
                    with st.spinner("Training model..."):
                        results = st.session_state.predictor.train_model(X, y, model_type)
                        if results:
                            st.success("Model trained successfully!")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("RMSE", f"{results['rmse']:.2f}")
                                st.metric("R² Score", f"{results['r2']:.2f}")
                            with col2:
                                st.metric("CV RMSE (mean)", f"{results['cv_rmse_mean']:.2f}")
                                st.metric("CV RMSE (std)", f"{results['cv_rmse_std']:.2f}")
                            
                            if 'feature_importance' in results:
                                st.subheader("Feature Importance Analysis")
                                fig = st.session_state.visualizer.plot_feature_importance(
                                    results['feature_importance']
                                )
                                st.plotly_chart(fig, use_container_width=True)
                            
                            st.subheader("Predictions vs Actual Values")
                            fig = st.session_state.visualizer.plot_prediction_results(
                                results['test_actual'],
                                results['test_predictions'],
                                results['test_features'].index
                            )
                            st.plotly_chart(
                                fig,
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

def main():
    try:
        import streamlit as st
        import pandas as pd
        from utils.data_processor import WeatherDataProcessor
        from utils.ml_models import WeatherPredictor
        from utils.visualizations import WeatherVisualizer
        from utils.weather_api import WeatherAPI
        
        # Initialize the app
        run_app(st, WeatherDataProcessor, WeatherPredictor, WeatherVisualizer, WeatherAPI)
    except ImportError as e:
        st.error(f"Error importing required packages: {str(e)}")
        st.info("Please ensure all required packages are installed correctly.")
        return

if __name__ == "__main__":
    try:
        port = int(os.getenv('PORT', 5000))
        main()
    except Exception as e:
        logger.error(f"Application failed to start: {str(e)}")
        sys.exit(1)
