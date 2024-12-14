import os
import requests
from datetime import datetime

class WeatherAPI:
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHERMAP_API_KEY')
        self.base_url = "http://api.openweathermap.org/data/2.5"

    def get_current_weather(self, city="San Francisco", country="US"):
        """Fetch current weather data for a given city"""
        try:
            response = requests.get(
                f"{self.base_url}/weather",
                params={
                    'q': f"{city},{country}",
                    'appid': self.api_key,
                    'units': 'metric'
                }
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                'temperature': round(data['main']['temp'], 1),
                'feels_like': round(data['main']['feels_like'], 1),
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'description': data['weather'][0]['description'].capitalize(),
                'icon': data['weather'][0]['icon'],
                'wind_speed': data['wind']['speed'],
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            print(f"Error fetching weather data: {str(e)}")
            return None

    def get_forecast(self, city="San Francisco", country="US"):
        """Fetch 5-day weather forecast data"""
        try:
            response = requests.get(
                f"{self.base_url}/forecast",
                params={
                    'q': f"{city},{country}",
                    'appid': self.api_key,
                    'units': 'metric'
                }
            )
            response.raise_for_status()
            data = response.json()
            
            forecasts = []
            for item in data['list']:
                forecasts.append({
                    'timestamp': datetime.fromtimestamp(item['dt']),
                    'temperature': round(item['main']['temp'], 1),
                    'description': item['weather'][0]['description'].capitalize(),
                    'icon': item['weather'][0]['icon']
                })
            
            return forecasts
        except Exception as e:
            print(f"Error fetching forecast data: {str(e)}")
            return None
