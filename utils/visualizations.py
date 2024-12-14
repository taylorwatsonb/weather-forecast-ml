import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

class WeatherVisualizer:
    @staticmethod
    def plot_temperature_trend(df):
        """Plot historical temperature trend with confidence intervals"""
        fig = go.Figure()

        # Add temperature line
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['temperature'],
            name='Temperature',
            line=dict(color='rgb(31, 119, 180)'),
        ))

        # Calculate rolling mean and std
        rolling_mean = df['temperature'].rolling(window=7).mean()
        rolling_std = df['temperature'].rolling(window=7).std()

        # Add confidence intervals
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=rolling_mean + 2*rolling_std,
            fill=None,
            mode='lines',
            line_color='rgba(31, 119, 180, 0)',
            showlegend=False,
        ))

        fig.add_trace(go.Scatter(
            x=df['date'],
            y=rolling_mean - 2*rolling_std,
            fill='tonexty',
            mode='lines',
            line_color='rgba(31, 119, 180, 0)',
            name='95% Confidence Interval',
            fillcolor='rgba(31, 119, 180, 0.2)',
        ))

        fig.update_layout(
            title='Temperature Trend with Confidence Intervals',
            xaxis_title='Date',
            yaxis_title='Temperature (°C)',
            hovermode='x unified'
        )
        return fig

    @staticmethod
    def plot_correlation_matrix(df):
        """Plot enhanced correlation matrix of weather parameters"""
        correlation = df[['temperature', 'humidity', 'pressure']].corr()
        
        fig = px.imshow(
            correlation,
            labels=dict(color="Correlation"),
            title="Weather Parameter Correlations",
            color_continuous_scale='RdBu_r',
            aspect='auto'
        )
        
        # Add correlation values as text
        for i in range(len(correlation.index)):
            for j in range(len(correlation.columns)):
                fig.add_annotation(
                    x=i,
                    y=j,
                    text=f"{correlation.iloc[i, j]:.2f}",
                    showarrow=False,
                    font=dict(color='black' if abs(correlation.iloc[i, j]) < 0.7 else 'white')
                )
        
        fig.update_layout(
            width=600,
            height=500
        )
        return fig

    @staticmethod
    def plot_prediction_results(actual, predicted, dates):
        """Plot actual vs predicted temperatures with confidence intervals"""
        fig = go.Figure()
        
        # Calculate prediction intervals (mock data for demonstration)
        confidence = 0.1 * np.std(predicted) * np.random.randn(len(predicted))
        
        # Add actual values
        fig.add_trace(go.Scatter(
            x=dates,
            y=actual,
            name='Actual',
            mode='lines+markers',
            line=dict(color='blue')
        ))
        
        # Add predicted values with confidence intervals
        fig.add_trace(go.Scatter(
            x=dates,
            y=predicted + 2*confidence,
            mode='lines',
            line=dict(width=0),
            showlegend=False
        ))
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=predicted - 2*confidence,
            mode='lines',
            line=dict(width=0),
            fillcolor='rgba(255, 0, 0, 0.2)',
            fill='tonexty',
            name='95% Confidence Interval'
        ))
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=predicted,
            name='Predicted',
            mode='lines+markers',
            line=dict(color='red')
        ))
        
        fig.update_layout(
            title='Model Predictions vs Actual Values',
            xaxis_title='Date',
            yaxis_title='Temperature (°C)',
            legend_title='Legend',
            hovermode='x unified'
        )
        
        return fig

    @staticmethod
    def plot_feature_importance(feature_importance_df):
        """Plot enhanced feature importance analysis with detailed metrics"""
        # Calculate relative importance percentage
        total_importance = feature_importance_df['importance'].sum()
        feature_importance_df['importance_pct'] = (feature_importance_df['importance'] / total_importance * 100).round(2)
        
        # Create the bar plot with enhanced styling
        fig = go.Figure()
        
        # Add bars with gradient colors
        fig.add_trace(go.Bar(
            x=feature_importance_df['importance'],
            y=feature_importance_df['feature'],
            orientation='h',
            marker=dict(
                color=feature_importance_df['importance'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title='Importance Score')
            ),
            text=feature_importance_df['importance_pct'].apply(lambda x: f'{x:.1f}%'),
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>' +
                         'Importance Score: %{x:.4f}<br>' +
                         'Relative Importance: %{text}<br>' +
                         '<extra></extra>'
        ))
        
        # Update layout with enhanced styling
        fig.update_layout(
            title={
                'text': 'Feature Importance Analysis',
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(size=20)
            },
            xaxis_title='Importance Score',
            yaxis_title='Feature',
            yaxis={'categoryorder': 'total ascending'},
            plot_bgcolor='white',
            hoverlabel=dict(bgcolor='white'),
            margin=dict(l=20, r=20, t=60, b=20),
            height=400
        )
        
        # Add grid lines
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        
        return fig
