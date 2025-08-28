import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
import os
from datetime import datetime, timedelta
import random


class WeatherPredictor:
    """Main class for weather prediction using machine learning"""
    
    def __init__(self):
        self.temperature_model = None
        self.humidity_model = None
        self.precipitation_model = None
        self.wind_model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def generate_training_data(self, city, days=365):
        """Generate synthetic training data for demonstration"""
        data = []
        base_date = datetime.now() - timedelta(days=days)
        
        for i in range(days):
            date = base_date + timedelta(days=i)
            
            # Seasonal patterns
            day_of_year = date.timetuple().tm_yday
            season_factor = np.sin(2 * np.pi * day_of_year / 365)
            
            # Base temperature with seasonal variation
            base_temp = 15 + 10 * season_factor
            temperature = base_temp + random.uniform(-5, 5)
            
            # Humidity inversely related to temperature
            humidity = max(30, min(90, 80 - temperature * 1.5 + random.uniform(-10, 10)))
            
            # Pressure with some variation
            pressure = 1013 + random.uniform(-20, 20)
            
            # Wind speed
            wind_speed = random.uniform(0, 15)
            
            # Precipitation (more likely in certain conditions)
            precipitation = 0
            if humidity > 70 and random.random() < 0.3:
                precipitation = random.uniform(0, 50)
            
            data.append({
                'date': date,
                'day_of_year': day_of_year,
                'month': date.month,
                'hour': 12,  # Midday for simplicity
                'temperature': temperature,
                'humidity': humidity,
                'pressure': pressure,
                'wind_speed': wind_speed,
                'precipitation': precipitation,
                'season_factor': season_factor
            })
        
        return pd.DataFrame(data)
    
    def prepare_features(self, df):
        """Prepare features for machine learning"""
        features = df[['day_of_year', 'month', 'hour', 'season_factor']].copy()
        
        # Add lagged features (previous day's weather)
        features['temp_lag1'] = df['temperature'].shift(1)
        features['humidity_lag1'] = df['humidity'].shift(1)
        features['pressure_lag1'] = df['pressure'].shift(1)
        features['wind_lag1'] = df['wind_speed'].shift(1)
        
        # Add rolling averages
        features['temp_avg_7d'] = df['temperature'].rolling(7).mean()
        features['humidity_avg_7d'] = df['humidity'].rolling(7).mean()
        features['pressure_avg_7d'] = df['pressure'].rolling(7).mean()
        
        # Remove NaN values
        features = features.dropna()
        
        return features
    
    def train_models(self, city='London'):
        """Train all weather prediction models"""
        print(f"Training weather prediction models for {city}...")
        
        # Generate training data
        df = self.generate_training_data(city)
        features = self.prepare_features(df)
        
        # Prepare targets
        temp_target = df['temperature'].iloc[features.index]
        humidity_target = df['humidity'].iloc[features.index]
        precipitation_target = df['precipitation'].iloc[features.index]
        wind_target = df['wind_speed'].iloc[features.index]
        
        # Scale features
        features_scaled = self.scaler.fit_transform(features)
        
        # Train temperature model
        self.temperature_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.temperature_model.fit(features_scaled, temp_target)
        
        # Train humidity model
        self.humidity_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.humidity_model.fit(features_scaled, humidity_target)
        
        # Train precipitation model
        self.precipitation_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.precipitation_model.fit(features_scaled, precipitation_target)
        
        # Train wind model
        self.wind_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.wind_model.fit(features_scaled, wind_target)
        
        self.is_trained = True
        
        # Calculate and print model performance
        self._evaluate_models(features_scaled, temp_target, humidity_target, precipitation_target, wind_target)
        
        print("Model training completed!")
    
    def _evaluate_models(self, X, temp_y, humidity_y, precip_y, wind_y):
        """Evaluate model performance"""
        models = {
            'Temperature': (self.temperature_model, temp_y),
            'Humidity': (self.humidity_model, humidity_y),
            'Precipitation': (self.precipitation_model, precip_y),
            'Wind': (self.wind_model, wind_y)
        }
        
        print("\nModel Performance:")
        print("-" * 50)
        
        for name, (model, y_true) in models.items():
            y_pred = model.predict(X)
            mse = mean_squared_error(y_true, y_pred)
            mae = mean_absolute_error(y_true, y_pred)
            r2 = r2_score(y_true, y_pred)
            
            print(f"{name}:")
            print(f"  MSE: {mse:.4f}")
            print(f"  MAE: {mae:.4f}")
            print(f"  R²: {r2:.4f}")
            print()
    
    def predict_weather(self, city, hours_ahead=24):
        """Predict weather for the next N hours"""
        if not self.is_trained:
            raise ValueError("Models must be trained before making predictions")
        
        predictions = []
        current_time = datetime.now()
        
        for i in range(hours_ahead):
            future_time = current_time + timedelta(hours=i)
            day_of_year = future_time.timetuple().tm_yday
            season_factor = np.sin(2 * np.pi * day_of_year / 365)
            
            # Create feature vector
            features = np.array([[
                day_of_year,
                future_time.month,
                future_time.hour,
                season_factor,
                # Use current values as lagged features (in real app, these would be actual historical data)
                20.0,  # temp_lag1
                65.0,  # humidity_lag1
                1013.0,  # pressure_lag1
                5.0,  # wind_lag1
                20.0,  # temp_avg_7d
                65.0,  # humidity_avg_7d
                1013.0,  # pressure_avg_7d
            ]])
            
            # Scale features
            features_scaled = self.scaler.transform(features)
            
            # Make predictions
            temp_pred = self.temperature_model.predict(features_scaled)[0]
            humidity_pred = self.humidity_model.predict(features_scaled)[0]
            precip_pred = self.precipitation_model.predict(features_scaled)[0]
            wind_pred = self.wind_model.predict(features_scaled)[0]
            
            # Ensure predictions are within reasonable bounds
            temp_pred = max(-20, min(50, temp_pred))
            humidity_pred = max(0, min(100, humidity_pred))
            precip_pred = max(0, precip_pred)
            wind_pred = max(0, min(30, wind_pred))
            
            predictions.append({
                'time': future_time.isoformat(),
                'temperature': round(temp_pred, 1),
                'humidity': round(humidity_pred),
                'pressure': round(1013 + random.uniform(-10, 10)),
                'wind_speed': round(wind_pred, 1),
                'precipitation': round(precip_pred, 1),
                'description': self._get_weather_description(temp_pred, humidity_pred, precip_pred),
                'icon': self._get_weather_icon(temp_pred, humidity_pred, precip_pred)
            })
        
        return {
            'city': city,
            'predictions': predictions,
            'model_confidence': 0.85,
            'generated_at': current_time.isoformat()
        }
    
    def _get_weather_description(self, temp, humidity, precip):
        """Get weather description based on predictions"""
        if precip > 10:
            return "Heavy Rain"
        elif precip > 5:
            return "Light Rain"
        elif temp > 25:
            return "Hot"
        elif temp > 15:
            return "Warm"
        elif temp > 5:
            return "Cool"
        else:
            return "Cold"
    
    def _get_weather_icon(self, temp, humidity, precip):
        """Get weather icon based on predictions"""
        if precip > 5:
            return "09d"
        elif temp > 25:
            return "01d"
        elif temp > 15:
            return "02d"
        else:
            return "03d"
    
    def save_models(self, filepath):
        """Save trained models to disk"""
        if not self.is_trained:
            raise ValueError("Models must be trained before saving")
        
        os.makedirs(filepath, exist_ok=True)
        
        joblib.dump(self.temperature_model, os.path.join(filepath, 'temperature_model.pkl'))
        joblib.dump(self.humidity_model, os.path.join(filepath, 'humidity_model.pkl'))
        joblib.dump(self.precipitation_model, os.path.join(filepath, 'precipitation_model.pkl'))
        joblib.dump(self.wind_model, os.path.join(filepath, 'wind_model.pkl'))
        joblib.dump(self.scaler, os.path.join(filepath, 'scaler.pkl'))
        
        print(f"Models saved to {filepath}")
    
    def load_models(self, filepath):
        """Load trained models from disk"""
        try:
            self.temperature_model = joblib.load(os.path.join(filepath, 'temperature_model.pkl'))
            self.humidity_model = joblib.load(os.path.join(filepath, 'humidity_model.pkl'))
            self.precipitation_model = joblib.load(os.path.join(filepath, 'precipitation_model.pkl'))
            self.wind_model = joblib.load(os.path.join(filepath, 'wind_model.pkl'))
            self.scaler = joblib.load(os.path.join(filepath, 'scaler.pkl'))
            
            self.is_trained = True
            print(f"Models loaded from {filepath}")
        except FileNotFoundError:
            print("Model files not found. Please train models first.")


# Global instance for easy access
weather_predictor = WeatherPredictor()


def train_weather_models(city='London'):
    """Function to train weather prediction models"""
    weather_predictor.train_models(city)
    return weather_predictor


def get_weather_prediction(city, hours=24):
    """Function to get weather predictions"""
    if not weather_predictor.is_trained:
        weather_predictor.train_models(city)
    
    return weather_predictor.predict_weather(city, hours)
