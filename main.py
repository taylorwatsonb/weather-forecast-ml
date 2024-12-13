import streamlit as st
import pandas as pd
from utils.data_processor import WeatherDataProcessor
from utils.ml_models import WeatherPredictor
from utils.visualizations import WeatherVisualizer

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
            df = st.session_state.data_processor.generate_sample_data()
            st.success("Sample data generated!")

# Main content
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
    
    # Model Selection
    model_option = st.selectbox(
        "Select ML Model",
        ["Linear Regression", "Random Forest", "XGBoost"],
        help="Choose the machine learning model for weather prediction"
    )
    
    if st.button("Train Model"):
        X, y = st.session_state.data_processor.prepare_ml_data()
        if X is not None and y is not None:
            with st.spinner(f'Training {model_option} model...'):
                results = st.session_state.predictor.train_model(X, y, model_option)
            
            if results:
                # Model Performance Metrics
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Root Mean Square Error", f"{results['rmse']:.2f}")
                with col2:
                    st.metric("R² Score", f"{results['r2']:.2f}")
                
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
