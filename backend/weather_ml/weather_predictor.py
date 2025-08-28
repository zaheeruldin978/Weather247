import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os
import logging
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)

class WeatherPredictor:
    """Advanced weather prediction using machine learning"""
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.feature_names = [
            'temperature', 'humidity', 'pressure', 'wind_speed', 'wind_direction',
            'hour', 'day_of_year', 'month', 'is_weekend', 'is_night'
        ]
        self.target_variables = ['temperature', 'humidity', 'pressure', 'wind_speed']
        self.model_path = 'weather_ml/saved_models/'
        
        # Create models directory if it doesn't exist
        os.makedirs(self.model_path, exist_ok=True)
        
        # Initialize models
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize machine learning models for each weather parameter"""
        for target in self.target_variables:
            # Random Forest for temperature and wind speed
            if target in ['temperature', 'wind_speed']:
                self.models[target] = RandomForestRegressor(
                    n_estimators=100,
                    max_depth=10,
                    random_state=42,
                    n_jobs=-1
                )
            # Gradient Boosting for humidity and pressure
            else:
                self.models[target] = GradientBoostingRegressor(
                    n_estimators=100,
                    max_depth=6,
                    random_state=42,
                    learning_rate=0.1
                )
            
            self.scalers[target] = StandardScaler()
    
    def _extract_features(self, weather_data, timestamp):
        """Extract features from weather data and timestamp"""
        dt = datetime.fromtimestamp(timestamp)
        
        features = [
            weather_data.get('temperature', 20),
            weather_data.get('humidity', 50),
            weather_data.get('pressure', 1013),
            weather_data.get('wind_speed', 5),
            weather_data.get('wind_direction', 180),
            dt.hour,
            dt.timetuple().tm_yday,
            dt.month,
            1 if dt.weekday() >= 5 else 0,  # is_weekend
            1 if 22 <= dt.hour or dt.hour <= 6 else 0  # is_night
        ]
        
        return np.array(features).reshape(1, -1)
    
    def _generate_synthetic_training_data(self, city_name):
        """Generate synthetic training data based on city characteristics"""
        logger.info(f"Generating synthetic training data for {city_name}")
        
        # City-specific weather patterns
        city_patterns = {
            'London': {'temp_range': (5, 25), 'humidity_range': (60, 85), 'rainy_days': 0.4},
            'New York': {'temp_range': (-10, 35), 'humidity_range': (50, 80), 'rainy_days': 0.35},
            'Tokyo': {'temp_range': (0, 30), 'humidity_range': (55, 85), 'rainy_days': 0.45},
            'Miami': {'temp_range': (15, 35), 'humidity_range': (70, 90), 'rainy_days': 0.5},
            'Gujranwala': {'temp_range': (10, 40), 'humidity_range': (40, 80), 'rainy_days': 0.3},
            'Lahore': {'temp_range': (8, 42), 'humidity_range': (35, 75), 'rainy_days': 0.25}
        }
        
        pattern = city_patterns.get(city_name, city_patterns['London'])
        
        # Generate 1000 synthetic data points
        n_samples = 1000
        data = []
        
        for i in range(n_samples):
            # Generate random timestamp within last year
            timestamp = datetime.now() - timedelta(days=np.random.randint(0, 365))
            dt = timestamp.timetuple()
            
            # Generate weather parameters with realistic patterns
            base_temp = np.random.uniform(pattern['temp_range'][0], pattern['temp_range'][1])
            
            # Add seasonal variation
            seasonal_temp = base_temp + 10 * np.sin(2 * np.pi * dt.tm_yday / 365)
            
            # Add daily variation
            daily_temp = seasonal_temp + 5 * np.sin(2 * np.pi * dt.tm_hour / 24)
            
            # Generate other parameters
            humidity = np.random.uniform(pattern['humidity_range'][0], pattern['humidity_range'][1])
            pressure = 1013 + np.random.uniform(-20, 20)
            wind_speed = np.random.uniform(0, 15)
            wind_direction = np.random.uniform(0, 360)
            
            # Add some correlation between parameters
            if np.random.random() < pattern['rainy_days']:
                humidity += 10
                pressure -= 10
                wind_speed += 5
            
            features = [
                daily_temp, humidity, pressure, wind_speed, wind_direction,
                dt.tm_hour, dt.tm_yday, dt.tm_mon,
                1 if dt.tm_wday >= 5 else 0,
                1 if 22 <= dt.tm_hour or dt.tm_hour <= 6 else 0
            ]
            
            data.append(features)
        
        return np.array(data)
    
    def train_models(self, city_name):
        """Train machine learning models for a specific city"""
        logger.info(f"Training weather prediction models for {city_name}")
        
        try:
            # Generate synthetic training data
            X = self._generate_synthetic_training_data(city_name)
            
            # Train models for each target variable
            for target in self.target_variables:
                logger.info(f"Training {target} prediction model...")
                
                # Use the corresponding feature as target (excluding it from features)
                target_idx = self.feature_names.index(target)
                y = X[:, target_idx]
                X_features = np.delete(X, target_idx, axis=1)
                
                # Split data
                X_train, X_test, y_train, y_test = train_test_split(
                    X_features, y, test_size=0.2, random_state=42
                )
                
                # Scale features
                X_train_scaled = self.scalers[target].fit_transform(X_train)
                X_test_scaled = self.scalers[target].transform(X_test)
                
                # Train model
                self.models[target].fit(X_train_scaled, y_train)
                
                # Evaluate model
                y_pred = self.models[target].predict(X_test_scaled)
                mae = mean_absolute_error(y_test, y_pred)
                r2 = r2_score(y_test, y_pred)
                
                logger.info(f"✅ {target} model trained - MAE: {mae:.2f}, R²: {r2:.3f}")
                
                # Save model
                model_file = f"{self.model_path}{city_name}_{target}_model.pkl"
                scaler_file = f"{self.model_path}{city_name}_{target}_scaler.pkl"
                
                joblib.dump(self.models[target], model_file)
                joblib.dump(self.scalers[target], scaler_file)
                
                logger.info(f"✅ Model saved to {model_file}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error training models for {city_name}: {str(e)}")
            return False
    
    def predict_weather(self, city_name, current_weather, hours_ahead=24):
        """Predict weather for the next N hours"""
        logger.info(f"Predicting weather for {city_name} - {hours_ahead} hours ahead")
        
        try:
            predictions = []
            current_time = datetime.now()
            
            for hour in range(1, hours_ahead + 1):
                # Calculate future timestamp
                future_time = current_time + timedelta(hours=hour)
                timestamp = future_time.timestamp()
                
                # Extract features
                features = self._extract_features(current_weather, timestamp)
                
                # Make predictions for each weather parameter
                hour_prediction = {'timestamp': timestamp, 'datetime': future_time.isoformat()}
                
                for target in self.target_variables:
                    target_idx = self.feature_names.index(target)
                    X_features = np.delete(features, target_idx, axis=1)
                    
                    # Scale features
                    X_scaled = self.scalers[target].transform(X_features)
                    
                    # Make prediction
                    prediction = self.models[target].predict(X_scaled)[0]
                    
                    # Add realistic constraints
                    if target == 'temperature':
                        prediction = np.clip(prediction, -40, 50)
                    elif target == 'humidity':
                        prediction = np.clip(prediction, 0, 100)
                    elif target == 'pressure':
                        prediction = np.clip(prediction, 900, 1100)
                    elif target == 'wind_speed':
                        prediction = np.clip(prediction, 0, 50)
                    
                    hour_prediction[target] = round(prediction, 1)
                
                # Add weather description based on conditions
                hour_prediction['description'] = self._get_weather_description(hour_prediction)
                
                predictions.append(hour_prediction)
            
            logger.info(f"✅ Generated {len(predictions)} weather predictions for {city_name}")
            return predictions
            
        except Exception as e:
            logger.error(f"❌ Error predicting weather for {city_name}: {str(e)}")
            return None
    
    def _get_weather_description(self, weather_data):
        """Generate weather description based on predicted conditions"""
        temp = weather_data.get('temperature', 20)
        humidity = weather_data.get('humidity', 50)
        wind_speed = weather_data.get('wind_speed', 5)
        
        # Temperature-based description
        if temp < 0:
            temp_desc = "freezing"
        elif temp < 10:
            temp_desc = "cold"
        elif temp < 20:
            temp_desc = "cool"
        elif temp < 25:
            temp_desc = "mild"
        elif temp < 30:
            temp_desc = "warm"
        else:
            temp_desc = "hot"
        
        # Humidity-based description
        if humidity > 80:
            humidity_desc = "humid"
        elif humidity > 60:
            humidity_desc = "moderately humid"
        else:
            humidity_desc = "dry"
        
        # Wind-based description
        if wind_speed > 20:
            wind_desc = "very windy"
        elif wind_speed > 10:
            wind_desc = "windy"
        elif wind_speed > 5:
            wind_desc = "breezy"
        else:
            wind_desc = "calm"
        
        return f"{temp_desc}, {humidity_desc}, {wind_desc}"
    
    def get_prediction_accuracy(self, city_name):
        """Get prediction accuracy metrics for a city"""
        try:
            # Load test data
            X = self._generate_synthetic_training_data(city_name)
            
            accuracy_metrics = {}
            
            for target in self.target_variables:
                target_idx = self.feature_names.index(target)
                y_true = X[:, target_idx]
                X_features = np.delete(X, target_idx, axis=1)
                
                # Scale features
                X_scaled = self.scalers[target].transform(X_features)
                
                # Make predictions
                y_pred = self.models[target].predict(X_scaled)
                
                # Calculate metrics
                mae = mean_absolute_error(y_true, y_pred)
                mse = mean_squared_error(y_true, y_pred)
                rmse = np.sqrt(mse)
                r2 = r2_score(y_true, y_pred)
                
                accuracy_metrics[target] = {
                    'mae': round(mae, 2),
                    'rmse': round(rmse, 2),
                    'r2': round(r2, 3),
                    'accuracy_percentage': round((1 - mae / np.mean(np.abs(y_true))) * 100, 1)
                }
            
            return accuracy_metrics
            
        except Exception as e:
            logger.error(f"❌ Error calculating accuracy for {city_name}: {str(e)}")
            return None

# Global instance
weather_predictor = WeatherPredictor()
