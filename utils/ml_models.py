from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

class WeatherPredictor:
    def __init__(self):
        self.model = LinearRegression()
        self.is_trained = False

    def train_model(self, X, y):
        """Train the linear regression model"""
        try:
            # Split the data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Train the model
            self.model.fit(X_train, y_train)
            
            # Make predictions on test set
            y_pred = self.model.predict(X_test)
            
            # Calculate metrics
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            r2 = r2_score(y_test, y_pred)
            
            self.is_trained = True
            
            return {
                'rmse': rmse,
                'r2': r2,
                'test_predictions': y_pred,
                'test_actual': y_test,
                'test_features': X_test
            }
        except Exception as e:
            return None

    def predict(self, features):
        """Make predictions using trained model"""
        if not self.is_trained:
            return None
            
        try:
            predictions = self.model.predict(features)
            return predictions
        except Exception as e:
            return None
