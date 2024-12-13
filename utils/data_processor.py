import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class WeatherDataProcessor:
    def __init__(self):
        self.data = None

    def process_uploaded_data(self, file):
        """Process uploaded CSV file containing weather data"""
        try:
            df = pd.read_csv(file)
            required_columns = ['date', 'temperature', 'humidity', 'pressure']
            
            # Ensure required columns exist
            if not all(col in df.columns for col in required_columns):
                return None, "Missing required columns"

            # Convert date to datetime
            df['date'] = pd.to_datetime(df['date'])
            
            # Sort by date
            df = df.sort_values('date')
            
            # Handle missing values
            df = df.interpolate(method='linear')
            
            self.data = df
            return df, "Data processed successfully"
        except Exception as e:
            return None, f"Error processing file: {str(e)}"

    def generate_sample_data(self):
        """Generate sample weather data for demonstration"""
        dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
        
        # Generate synthetic weather data
        np.random.seed(42)
        temperature = np.random.normal(25, 5, len(dates))
        humidity = np.random.normal(60, 10, len(dates))
        pressure = np.random.normal(1013, 5, len(dates))
        
        df = pd.DataFrame({
            'date': dates,
            'temperature': temperature,
            'humidity': humidity,
            'pressure': pressure
        })
        
        self.data = df
        return df

    def prepare_ml_data(self):
        """Prepare data for ML model"""
        if self.data is None:
            return None, None
            
        df = self.data.copy()
        
        # Create features
        df['day_of_year'] = df['date'].dt.dayofyear
        df['month'] = df['date'].dt.month
        
        # Prepare X (features) and y (target)
        X = df[['day_of_year', 'month', 'humidity', 'pressure']]
        y = df['temperature']
        
        return X, y
