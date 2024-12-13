import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class WeatherVisualizer:
    @staticmethod
    def plot_temperature_trend(df):
        """Plot historical temperature trend"""
        fig = px.line(
            df,
            x='date',
            y='temperature',
            title='Temperature Over Time',
            labels={'temperature': 'Temperature (°C)', 'date': 'Date'}
        )
        return fig

    @staticmethod
    def plot_correlation_matrix(df):
        """Plot correlation matrix of weather parameters"""
        correlation = df[['temperature', 'humidity', 'pressure']].corr()
        
        fig = px.imshow(
            correlation,
            labels=dict(color="Correlation"),
            title="Parameter Correlation Matrix"
        )
        return fig

    @staticmethod
    def plot_prediction_results(actual, predicted, dates):
        """Plot actual vs predicted temperatures"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=actual,
            name='Actual',
            mode='lines+markers'
        ))
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=predicted,
            name='Predicted',
            mode='lines+markers'
        ))
        
        fig.update_layout(
            title='Actual vs Predicted Temperature',
            xaxis_title='Date',
            yaxis_title='Temperature (°C)',
            legend_title='Legend'
        )
        
        return fig
