from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import pandas as pd

class WeatherPredictor:
    def __init__(self):
        self.models = {
            'Linear Regression': LinearRegression(),
            'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
            'XGBoost': GradientBoostingRegressor(n_estimators=100, random_state=42)
        }
        self.current_model = None
        self.current_model_name = None
        self.feature_importance = None
        self.is_trained = False

    def train_model(self, X, y, model_name='Linear Regression'):
        """Train the selected model"""
        try:
            # Split the data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Select and train the model
            self.current_model = self.models[model_name]
            self.current_model_name = model_name
            self.current_model.fit(X_train, y_train)
            
            # Make predictions on test set
            y_pred = self.current_model.predict(X_test)
            
            # Calculate metrics
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            r2 = r2_score(y_test, y_pred)
            
            # Calculate feature importance
            if model_name in ['Random Forest', 'XGBoost']:
                self.feature_importance = pd.DataFrame({
                    'feature': X.columns,
                    'importance': self.current_model.feature_importances_
                }).sort_values('importance', ascending=False)
            elif model_name == 'Linear Regression':
                self.feature_importance = pd.DataFrame({
                    'feature': X.columns,
                    'importance': np.abs(self.current_model.coef_)
                }).sort_values('importance', ascending=False)
            
            self.is_trained = True
            
            return {
                'rmse': rmse,
                'r2': r2,
                'test_predictions': y_pred,
                'test_actual': y_test,
                'test_features': X_test,
                'feature_importance': self.feature_importance
            }
        except Exception as e:
            print(f"Error in training: {str(e)}")
            return None

    def predict(self, features):
        """Make predictions using trained model"""
        if not self.is_trained or self.current_model is None:
            return None
            
        try:
            predictions = self.current_model.predict(features)
            return predictions
        except Exception as e:
            print(f"Error in prediction: {str(e)}")
            return None

    def get_feature_importance(self):
        """Return feature importance for the current model"""
        return self.feature_importance if self.is_trained else None
