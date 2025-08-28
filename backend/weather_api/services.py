import requests
import json
from datetime import datetime, timedelta
from django.conf import settings
from django.core.cache import cache
from .models import City, WeatherData, WeatherForecast, HistoricalWeather
import logging

logger = logging.getLogger(__name__)

class OpenWeatherService:
    """Service class for OpenWeather API integration"""
    
    def __init__(self):
        self.api_key = getattr(settings, 'OPENWEATHER_API_KEY', '1526952d944b16b4107765039667b561')
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.geo_url = "http://api.openweathermap.org/geo/1.0"
        self.air_url = "http://api.openweathermap.org/data/2.8"
        
    def get_city_coordinates(self, city_name, country_code=None):
        """Get city coordinates from OpenWeather Geocoding API"""
        try:
            url = f"{self.geo_url}/direct"
            params = {
                'q': f"{city_name},{country_code}" if country_code else city_name,
                'limit': 1,
                'appid': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data:
                return {
                    'name': data[0]['name'],
                    'country': data[0]['country'],
                    'lat': data[0]['lat'],
                    'lon': data[0]['lon'],
                    'state': data[0].get('state', '')
                }
            return None
        except Exception as e:
            logger.error(f"Error getting coordinates for {city_name}: {str(e)}")
            return None
    
    def get_current_weather(self, city_name, country_code=None):
        """Get current weather data for a city"""
        try:
            logger.info(f"Getting weather for {city_name} (country: {country_code})")
            
            coords = self.get_city_coordinates(city_name, country_code)
            if not coords:
                logger.error(f"Could not get coordinates for {city_name}")
                return None
                
            logger.info(f"Got coordinates for {city_name}: {coords}")
            
            url = f"{self.base_url}/weather"
            params = {
                'lat': coords['lat'],
                'lon': coords['lon'],
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'en'
            }
            
            logger.info(f"Making request to OpenWeather API: {url}")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"OpenWeather API response received for {city_name}")
            
            # Get AQI data
            aqi_data = self.get_air_quality(coords['lat'], coords['lon'])
            
            weather_data = {
                'city': coords['name'],
                'country': coords['country'],
                'state': coords['state'],
                'coordinates': {'lat': coords['lat'], 'lon': coords['lon']},
                'temperature': round(data['main']['temp'], 1),
                'feels_like': round(data['main']['feels_like'], 1),
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': round(data['wind']['speed'], 1),
                'wind_direction': data['wind'].get('deg', 0),
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'visibility': data.get('visibility', 10000),
                'aqi': aqi_data.get('aqi', 50) if aqi_data else 50,
                'sunrise': data['sys']['sunrise'],  # Keep as Unix timestamp
                'sunset': data['sys']['sunset'],    # Keep as Unix timestamp
                'timestamp': datetime.now()
            }
            
            logger.info(f"Processed weather data for {city_name}: {weather_data}")
            
            # Cache the data for 10 minutes
            cache_key = f"current_weather_{city_name.lower()}"
            cache.set(cache_key, weather_data, 600)
            
            return weather_data
            
        except Exception as e:
            logger.error(f"Error getting current weather for {city_name}: {str(e)}")
            return None
    
    def get_air_quality(self, lat, lon):
        """Get air quality data using OpenWeather API v3.0"""
        try:
            # Use the correct API endpoint for air quality
            url = f"https://api.openweathermap.org/data/2.5/air_pollution"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key
            }
            
            logger.info(f"Fetching air quality data for coordinates: {lat}, {lon}")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get('list') and len(data['list']) > 0:
                aqi = data['list'][0]['main']['aqi']
                components = data['list'][0]['components']
                
                logger.info(f"Air quality data received: AQI {aqi}")
                return {
                    'aqi': aqi,
                    'components': components,
                    'timestamp': datetime.fromtimestamp(data['list'][0]['dt'])
                }
            else:
                logger.warning("No air quality data in response")
                return None
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error getting air quality: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error getting air quality: {str(e)}")
            return None
    
    def get_weather_forecast(self, city_name, days=5):
        """Get 5-day weather forecast with hourly data"""
        try:
            coords = self.get_city_coordinates(city_name)
            if not coords:
                return None
                
            url = f"{self.base_url}/forecast"
            params = {
                'lat': coords['lat'],
                'lon': coords['lon'],
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'en'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Get base forecasts (3-hour intervals)
            base_forecasts = []
            for item in data['list']:
                forecast = {
                    'datetime': datetime.fromtimestamp(item['dt']),
                    'temperature': round(item['main']['temp'], 1),
                    'feels_like': round(item['main']['feels_like'], 1),
                    'humidity': item['main']['humidity'],
                    'pressure': item['main']['pressure'],
                    'wind_speed': round(item['wind']['speed'], 1),
                    'description': item['weather'][0]['description'],
                    'icon': item['weather'][0]['icon'],
                    'pop': round(item['pop'] * 100, 1)  # Probability of precipitation
                }
                base_forecasts.append(forecast)
            
            # Generate hourly forecasts by interpolating between 3-hour intervals
            hourly_forecasts = []
            for i in range(len(base_forecasts) - 1):
                current = base_forecasts[i]
                next_forecast = base_forecasts[i + 1]
                
                # Add the current 3-hour forecast
                hourly_forecasts.append(current)
                
                # Generate intermediate hours (1 and 2 hours after current)
                for hour_offset in [1, 2]:
                    # Interpolate values for intermediate hours
                    progress = hour_offset / 3.0
                    
                    # Linear interpolation for numerical values
                    temp = current['temperature'] + (next_forecast['temperature'] - current['temperature']) * progress
                    feels_like = current['feels_like'] + (next_forecast['feels_like'] - current['feels_like']) * progress
                    humidity = round(current['humidity'] + (next_forecast['humidity'] - current['humidity']) * progress)
                    pressure = round(current['pressure'] + (next_forecast['pressure'] - current['pressure']) * progress)
                    wind_speed = current['wind_speed'] + (next_forecast['wind_speed'] - current['wind_speed']) * progress
                    
                    # Create intermediate datetime
                    intermediate_dt = current['datetime'] + timedelta(hours=hour_offset)
                    
                    # Interpolate rain probability (decrease as we move away from the base forecast)
                    rain_decay = 1.0 - (progress * 0.3)  # 30% reduction for intermediate hours
                    pop = round(current['pop'] * rain_decay, 1)
                    
                    intermediate_forecast = {
                        'datetime': intermediate_dt,
                        'temperature': round(temp, 1),
                        'feels_like': round(feels_like, 1),
                        'humidity': humidity,
                        'pressure': pressure,
                        'wind_speed': round(wind_speed, 1),
                        'description': current['description'],  # Keep same weather description
                        'icon': current['icon'],  # Keep same icon
                        'pop': pop
                    }
                    hourly_forecasts.append(intermediate_forecast)
            
            # Add the last forecast
            if base_forecasts:
                hourly_forecasts.append(base_forecasts[-1])
            
            return {
                'city': coords['name'],
                'country': coords['country'],
                'forecasts': hourly_forecasts
            }
            
        except Exception as e:
            logger.error(f"Error getting forecast for {city_name}: {str(e)}")
            return None
    
    def get_historical_weather(self, city_name, start_date, end_date):
        """Get historical weather data (requires OpenWeather One Call API 3.0)"""
        try:
            coords = self.get_city_coordinates(city_name)
            if not coords:
                return None
                
            # Note: Historical data requires One Call API 3.0 subscription
            # For now, we'll return mock data structure
            historical_data = []
            current_date = start_date
            
            while current_date <= end_date:
                # Mock historical data - replace with actual API call when subscription is available
                historical_data.append({
                    'date': current_date,
                    'max_temperature': round(20 + (current_date.day % 10), 1),
                    'min_temperature': round(10 + (current_date.day % 8), 1),
                    'avg_temperature': round(15 + (current_date.day % 9), 1),
                    'avg_humidity': 60 + (current_date.day % 20),
                    'avg_pressure': 1013 + (current_date.day % 10),
                    'precipitation': round((current_date.day % 7) * 0.5, 1)
                })
                current_date += timedelta(days=1)
            
            return {
                'city': coords['name'],
                'country': coords['country'],
                'historical_data': historical_data
            }
            
        except Exception as e:
            logger.error(f"Error getting historical weather for {city_name}: {str(e)}")
            return None
    
    def get_weather_alerts(self, city_name):
        """Get weather alerts for a city using OpenWeather API"""
        try:
            coords = self.get_city_coordinates(city_name)
            if not coords:
                logger.error(f"Could not get coordinates for {city_name}")
                return None
                
            # Try One Call API 2.5 first (includes alerts)
            url = f"https://api.openweathermap.org/data/2.5/onecall"
            params = {
                'lat': coords['lat'],
                'lon': coords['lon'],
                'exclude': 'current,minutely,hourly,daily',
                'appid': self.api_key,
                'units': 'metric'
            }
            
            logger.info(f"Fetching weather alerts for {city_name} at coordinates: {coords['lat']}, {coords['lon']}")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            alerts = data.get('alerts', [])
            
            logger.info(f"Weather alerts data received for {city_name}: {len(alerts)} alerts")
            return {
                'city': coords['name'],
                'country': coords['country'],
                'alerts': alerts
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error getting alerts for {city_name}: {str(e)}")
            # Try alternative approach - check if it's a subscription issue
            if "401" in str(e) or "403" in str(e):
                logger.warning(f"API subscription issue for {city_name}, returning mock data for testing")
                # Return city-specific mock alerts for testing purposes
                mock_alerts = self._get_mock_alerts_for_city(city_name)
                return {
                    'city': city_name,
                    'country': 'Unknown',
                    'alerts': mock_alerts
                }
            # Return empty alerts instead of None to avoid frontend errors
            return {
                'city': city_name,
                'country': 'Unknown',
                'alerts': []
            }
        except Exception as e:
            logger.error(f"Error getting alerts for {city_name}: {str(e)}")
            # Return empty alerts instead of None to avoid frontend errors
            return {
                'city': city_name,
                'country': 'Unknown',
                'alerts': []
            }
    
    def _get_mock_alerts_for_city(self, city_name):
        """Generate city-specific mock weather alerts for testing"""
        import random
        
        # City-specific alert patterns
        city_alerts = {
            'London': [
                {
                    'event': 'Heavy Rain Warning',
                    'description': 'Persistent rainfall expected with potential flooding in low-lying areas',
                    'start': int(datetime.now().timestamp()),
                    'end': int((datetime.now() + timedelta(hours=8)).timestamp()),
                    'tags': ['rain', 'flooding']
                }
            ],
            'New York': [
                {
                    'event': 'Heat Advisory',
                    'description': 'High temperatures and humidity creating dangerous heat index values',
                    'start': int(datetime.now().timestamp()),
                    'end': int((datetime.now() + timedelta(hours=12)).timestamp()),
                    'tags': ['heat', 'humidity']
                }
            ],
            'Tokyo': [
                {
                    'event': 'Typhoon Watch',
                    'description': 'Tropical storm approaching with heavy winds and rainfall expected',
                    'start': int(datetime.now().timestamp()),
                    'end': int((datetime.now() + timedelta(hours=24)).timestamp()),
                    'tags': ['typhoon', 'wind', 'rain']
                }
            ],
            'Miami': [
                {
                    'event': 'Tropical Storm Warning',
                    'description': 'Tropical storm conditions with heavy rainfall and strong winds',
                    'start': int(datetime.now().timestamp()),
                    'end': int((datetime.now() + timedelta(hours=18)).timestamp()),
                    'tags': ['tropical storm', 'rain', 'wind']
                }
            ],
            'Gujranwala': [
                {
                    'event': 'Dust Storm Alert',
                    'description': 'Dust storm conditions with reduced visibility and respiratory concerns',
                    'start': int(datetime.now().timestamp()),
                    'end': int((datetime.now() + timedelta(hours=6)).timestamp()),
                    'tags': ['dust storm', 'visibility']
                }
            ],
            'Lahore': [
                {
                    'event': 'Heat Wave Warning',
                    'description': 'Extreme heat conditions with temperatures exceeding 40°C',
                    'start': int(datetime.now().timestamp()),
                    'end': int((datetime.now() + timedelta(hours=10)).timestamp()),
                    'tags': ['heat wave', 'extreme temperature']
                }
            ]
        }
        
        # Return city-specific alerts if available, otherwise random alert
        if city_name in city_alerts:
            return city_alerts[city_name]
        
        # Generate random alert for other cities
        alert_types = [
            {
                'event': 'Weather Advisory',
                'description': 'Moderate weather conditions requiring attention',
                'tags': ['advisory']
            },
            {
                'event': 'Wind Warning',
                'description': 'Strong winds expected with potential for minor damage',
                'tags': ['wind']
            },
            {
                'event': 'Fog Alert',
                'description': 'Dense fog reducing visibility on roads and highways',
                'tags': ['fog', 'visibility']
            }
        ]
        
        random_alert = random.choice(alert_types)
        random_alert['start'] = int(datetime.now().timestamp())
        random_alert['end'] = int((datetime.now() + timedelta(hours=random.randint(4, 12))).timestamp())
        
        return [random_alert]

    def get_multiple_cities_weather(self, cities):
        """Get weather data for multiple cities simultaneously"""
        results = {}
        for city in cities:
            weather = self.get_current_weather(city)
            if weather:
                results[city] = weather
        return results

# Global instance
weather_service = OpenWeatherService()
