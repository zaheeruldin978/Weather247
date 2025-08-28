import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Tuple, Optional
import json
import os

logger = logging.getLogger(__name__)

class HistoricalWeatherAnalyzer:
    """Analyze historical weather data and generate trends"""
    
    def __init__(self):
        self.analysis_cache = {}
        self.trend_indicators = {
            'temperature': {'warming': '🌡️', 'cooling': '❄️', 'stable': '🌤️'},
            'humidity': {'increasing': '💧', 'decreasing': '🏜️', 'stable': '🌊'},
            'precipitation': {'increasing': '🌧️', 'decreasing': '☀️', 'stable': '⛅'},
            'wind_speed': {'increasing': '💨', 'decreasing': '🍃', 'stable': '🌬️'}
        }
    
    def generate_historical_data(self, city_name: str, years: int = 5) -> Dict:
        """Generate comprehensive historical weather data for analysis"""
        logger.info(f"Generating {years}-year historical data for {city_name}")
        
        try:
            # City-specific climate patterns
            climate_patterns = self._get_city_climate_patterns(city_name)
            
            # Generate data for each year
            all_data = []
            current_date = datetime.now()
            
            for year in range(current_date.year - years, current_date.year + 1):
                year_data = self._generate_year_data(year, climate_patterns)
                all_data.extend(year_data)
            
            # Convert to DataFrame for analysis
            df = pd.DataFrame(all_data)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            
            # Perform trend analysis
            trends = self._analyze_trends(df)
            seasonal_patterns = self._analyze_seasonal_patterns(df)
            extreme_events = self._identify_extreme_events(df)
            
            historical_analysis = {
                'city': city_name,
                'data_period': f"{years} years",
                'total_records': len(df),
                'date_range': {
                    'start': df['date'].min().strftime('%Y-%m-%d'),
                    'end': df['date'].max().strftime('%Y-%m-%d')
                },
                'trends': trends,
                'seasonal_patterns': seasonal_patterns,
                'extreme_events': extreme_events,
                'climate_summary': self._generate_climate_summary(df),
                'monthly_averages': self._calculate_monthly_averages(df),
                'yearly_averages': self._calculate_yearly_averages(df)
            }
            
            # Cache the analysis
            self.analysis_cache[city_name] = historical_analysis
            
            logger.info(f"✅ Generated historical analysis for {city_name}")
            return historical_analysis
            
        except Exception as e:
            logger.error(f"❌ Error generating historical data for {city_name}: {str(e)}")
            return None
    
    def _get_city_climate_patterns(self, city_name: str) -> Dict:
        """Get city-specific climate patterns"""
        patterns = {
            'London': {
                'temp_range': (2, 25), 'temp_variation': 8,
                'humidity_range': (65, 85), 'humidity_variation': 10,
                'rainy_days': 0.4, 'wind_avg': 6, 'wind_variation': 3
            },
            'New York': {
                'temp_range': (-8, 32), 'temp_variation': 12,
                'humidity_range': (55, 75), 'humidity_variation': 15,
                'rainy_days': 0.35, 'wind_avg': 8, 'wind_variation': 4
            },
            'Tokyo': {
                'temp_range': (2, 30), 'temp_variation': 10,
                'humidity_range': (60, 80), 'humidity_variation': 12,
                'rainy_days': 0.45, 'wind_avg': 5, 'wind_variation': 2
            },
            'Miami': {
                'temp_range': (15, 35), 'temp_variation': 6,
                'humidity_range': (70, 90), 'humidity_variation': 8,
                'rainy_days': 0.5, 'wind_avg': 7, 'wind_variation': 3
            },
            'Gujranwala': {
                'temp_range': (8, 42), 'temp_variation': 15,
                'humidity_range': (40, 80), 'humidity_variation': 20,
                'rainy_days': 0.3, 'wind_avg': 4, 'wind_variation': 2
            },
            'Lahore': {
                'temp_range': (5, 45), 'temp_variation': 18,
                'humidity_range': (35, 75), 'humidity_variation': 18,
                'rainy_days': 0.25, 'wind_avg': 5, 'wind_variation': 2
            }
        }
        
        return patterns.get(city_name, patterns['London'])
    
    def _generate_year_data(self, year: int, climate_patterns: Dict) -> List[Dict]:
        """Generate weather data for a specific year"""
        data = []
        start_date = datetime(year, 1, 1)
        
        for day in range(365):
            current_date = start_date + timedelta(days=day)
            
            # Generate realistic weather data with seasonal variations
            weather_data = self._generate_daily_weather(current_date, climate_patterns)
            
            data.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'year': year,
                'month': current_date.month,
                'day_of_year': day + 1,
                'temperature': weather_data['temperature'],
                'humidity': weather_data['humidity'],
                'pressure': weather_data['pressure'],
                'wind_speed': weather_data['wind_speed'],
                'precipitation': weather_data['precipitation'],
                'description': weather_data['description']
            })
        
        return data
    
    def _generate_daily_weather(self, date: datetime, patterns: Dict) -> Dict:
        """Generate realistic daily weather data"""
        # Seasonal temperature variation
        seasonal_temp = np.sin(2 * np.pi * (date.timetuple().tm_yday - 172) / 365)
        
        # Base temperature with seasonal variation
        base_temp = np.mean(patterns['temp_range']) + patterns['temp_variation'] * seasonal_temp
        
        # Add daily random variation
        daily_temp = base_temp + np.random.normal(0, 2)
        
        # Generate other parameters
        humidity = np.random.normal(np.mean(patterns['humidity_range']), patterns['humidity_variation'])
        humidity = np.clip(humidity, 20, 100)
        
        pressure = 1013 + np.random.normal(0, 15)
        pressure = np.clip(pressure, 950, 1080)
        
        wind_speed = np.random.normal(patterns['wind_avg'], patterns['wind_variation'])
        wind_speed = np.clip(wind_speed, 0, 30)
        
        # Precipitation based on rainy days probability
        precipitation = 0
        if np.random.random() < patterns['rainy_days']:
            precipitation = np.random.exponential(5)  # Exponential distribution for rain
        
        # Weather description
        description = self._get_weather_description(daily_temp, humidity, precipitation, wind_speed)
        
        return {
            'temperature': round(daily_temp, 1),
            'humidity': round(humidity, 1),
            'pressure': round(pressure, 1),
            'wind_speed': round(wind_speed, 1),
            'precipitation': round(precipitation, 1),
            'description': description
        }
    
    def _get_weather_description(self, temp: float, humidity: float, precip: float, wind: float) -> str:
        """Generate weather description based on conditions"""
        descriptions = []
        
        # Temperature description
        if temp < 0:
            descriptions.append('freezing')
        elif temp < 10:
            descriptions.append('cold')
        elif temp < 20:
            descriptions.append('cool')
        elif temp < 25:
            descriptions.append('mild')
        elif temp < 30:
            descriptions.append('warm')
        else:
            descriptions.append('hot')
        
        # Humidity description
        if humidity > 80:
            descriptions.append('humid')
        elif humidity < 40:
            descriptions.append('dry')
        
        # Precipitation description
        if precip > 10:
            descriptions.append('heavy rain')
        elif precip > 5:
            descriptions.append('moderate rain')
        elif precip > 1:
            descriptions.append('light rain')
        elif precip > 0:
            descriptions.append('drizzle')
        
        # Wind description
        if wind > 20:
            descriptions.append('very windy')
        elif wind > 10:
            descriptions.append('windy')
        elif wind > 5:
            descriptions.append('breezy')
        
        return ', '.join(descriptions) if descriptions else 'clear'
    
    def _analyze_trends(self, df: pd.DataFrame) -> Dict:
        """Analyze long-term weather trends"""
        trends = {}
        
        for column in ['temperature', 'humidity', 'pressure', 'wind_speed', 'precipitation']:
            if column in df.columns:
                # Calculate trend using linear regression
                x = np.arange(len(df))
                y = df[column].values
                
                # Remove NaN values
                mask = ~np.isnan(y)
                if np.sum(mask) > 10:  # Need at least 10 data points
                    x_clean = x[mask]
                    y_clean = y[mask]
                    
                    # Linear regression
                    coeffs = np.polyfit(x_clean, y_clean, 1)
                    slope = coeffs[0]
                    
                    # Calculate trend direction and magnitude
                    trend_info = self._classify_trend(column, slope, y_clean)
                    trends[column] = trend_info
        
        return trends
    
    def _classify_trend(self, parameter: str, slope: float, values: np.ndarray) -> Dict:
        """Classify trend direction and significance"""
        # Normalize slope by data range for fair comparison
        data_range = np.max(values) - np.min(values)
        normalized_slope = slope / data_range if data_range > 0 else 0
        
        # Determine trend direction
        if abs(normalized_slope) < 0.001:
            direction = 'stable'
            icon = self.trend_indicators.get(parameter, {}).get('stable', '➡️')
        elif normalized_slope > 0:
            direction = 'increasing'
            icon = self.trend_indicators.get(parameter, {}).get('increasing', '📈')
        else:
            direction = 'decreasing'
            icon = self.trend_indicators.get(parameter, {}).get('decreasing', '📉')
        
        # Calculate trend strength
        trend_strength = abs(normalized_slope)
        if trend_strength < 0.001:
            strength = 'minimal'
        elif trend_strength < 0.005:
            strength = 'weak'
        elif trend_strength < 0.01:
            strength = 'moderate'
        elif trend_strength < 0.02:
            strength = 'strong'
        else:
            strength = 'very strong'
        
        return {
            'direction': direction,
            'slope': round(slope, 6),
            'normalized_slope': round(normalized_slope, 6),
            'strength': strength,
            'icon': icon,
            'description': f"{parameter.title()} is {direction} with {strength} trend"
        }
    
    def _analyze_seasonal_patterns(self, df: pd.DataFrame) -> Dict:
        """Analyze seasonal weather patterns"""
        seasonal = {}
        
        for column in ['temperature', 'humidity', 'pressure', 'wind_speed', 'precipitation']:
            if column in df.columns:
                monthly_avg = df.groupby(df['date'].dt.month)[column].mean()
                seasonal[column] = {
                    'monthly_averages': monthly_avg.round(2).to_dict(),
                    'seasonal_range': {
                        'min': round(monthly_avg.min(), 2),
                        'max': round(monthly_avg.max(), 2),
                        'variation': round(monthly_avg.max() - monthly_avg.min(), 2)
                    }
                }
        
        return seasonal
    
    def _identify_extreme_events(self, df: pd.DataFrame) -> Dict:
        """Identify extreme weather events"""
        extreme_events = {}
        
        for column in ['temperature', 'humidity', 'pressure', 'wind_speed', 'precipitation']:
            if column in df.columns:
                values = df[column].dropna()
                if len(values) > 0:
                    q1 = values.quantile(0.25)
                    q3 = values.quantile(0.75)
                    iqr = q3 - q1
                    
                    # Define outliers as beyond 1.5 * IQR
                    lower_bound = q1 - 1.5 * iqr
                    upper_bound = q3 + 1.5 * iqr
                    
                    outliers = values[(values < lower_bound) | (values > upper_bound)]
                    
                    extreme_events[column] = {
                        'outlier_count': len(outliers),
                        'outlier_percentage': round(len(outliers) / len(values) * 100, 2),
                        'extreme_values': outliers.round(2).tolist()[:10],  # Top 10 extreme values
                        'statistics': {
                            'min': round(values.min(), 2),
                            'max': round(values.max(), 2),
                            'mean': round(values.mean(), 2),
                            'std': round(values.std(), 2)
                        }
                    }
        
        return extreme_events
    
    def _generate_climate_summary(self, df: pd.DataFrame) -> Dict:
        """Generate overall climate summary"""
        summary = {}
        
        for column in ['temperature', 'humidity', 'pressure', 'wind_speed', 'precipitation']:
            if column in df.columns:
                values = df[column].dropna()
                if len(values) > 0:
                    summary[column] = {
                        'overall_mean': round(values.mean(), 2),
                        'overall_std': round(values.std(), 2),
                        'min_recorded': round(values.min(), 2),
                        'max_recorded': round(values.max(), 2),
                        'data_completeness': round(len(values) / len(df) * 100, 1)
                    }
        
        return summary
    
    def _calculate_monthly_averages(self, df: pd.DataFrame) -> Dict:
        """Calculate monthly averages for all parameters"""
        monthly_data = {}
        
        for column in ['temperature', 'humidity', 'pressure', 'wind_speed', 'precipitation']:
            if column in df.columns:
                monthly_avg = df.groupby([df['date'].dt.year, df['date'].dt.month])[column].mean()
                # Convert tuple keys to strings
                monthly_dict = {}
                for (year, month), value in monthly_avg.items():
                    key = f"{year}-{month:02d}"
                    monthly_dict[key] = round(value, 2)
                monthly_data[column] = monthly_dict
        
        return monthly_data
    
    def _calculate_yearly_averages(self, df: pd.DataFrame) -> Dict:
        """Calculate yearly averages for all parameters"""
        yearly_data = {}
        
        for column in ['temperature', 'humidity', 'pressure', 'wind_speed', 'precipitation']:
            if column in df.columns:
                yearly_avg = df.groupby(df['date'].dt.year)[column].mean()
                # Convert year keys to strings
                yearly_dict = {}
                for year, value in yearly_avg.items():
                    yearly_dict[str(year)] = round(value, 2)
                yearly_data[column] = yearly_dict
        
        return yearly_data
    
    def get_trend_summary(self, city_name: str) -> str:
        """Get a human-readable trend summary"""
        if city_name not in self.analysis_cache:
            return "No analysis available. Please generate historical data first."
        
        analysis = self.analysis_cache[city_name]
        trends = analysis['trends']
        
        summary_parts = [f"🌍 **{city_name} Climate Trends** (5 years)"]
        
        for param, trend in trends.items():
            icon = trend['icon']
            direction = trend['direction']
            strength = trend['strength']
            summary_parts.append(f"{icon} **{param.title()}**: {direction} ({strength} trend)")
        
        return "\n".join(summary_parts)
    
    def export_analysis(self, city_name: str, format: str = 'json') -> str:
        """Export analysis results"""
        if city_name not in self.analysis_cache:
            return None
        
        analysis = self.analysis_cache[city_name]
        
        if format.lower() == 'json':
            return json.dumps(analysis, indent=2, default=str)
        elif format.lower() == 'csv':
            # Convert to CSV format
            df = pd.DataFrame(analysis['monthly_averages'])
            return df.to_csv()
        else:
            return str(analysis)

# Global instance
historical_analyzer = HistoricalWeatherAnalyzer()
