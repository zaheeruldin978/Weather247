#!/usr/bin/env python
"""
Database Population Script for Weather-247
This script populates the database with comprehensive weather data for demonstration purposes.
Run this script to create a complete database with realistic weather information.
"""

import os
import sys
import django
from datetime import datetime, timedelta
import random
from decimal import Decimal

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather247.settings')
django.setup()

from django.contrib.auth.models import User
from weather_api.models import City, WeatherData, WeatherForecast, HistoricalWeather, UserPreference, WeatherAlert, UserAlertSubscription
from django.utils import timezone

def create_superuser():
    """Create a superuser if it doesn't exist"""
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@weather247.com', 'admin123')
        print("✅ Superuser 'admin' created with password 'admin123'")
    else:
        print("✅ Superuser 'admin' already exists")

def create_cities():
    """Create comprehensive city data"""
    cities_data = [
        # Major Pakistani Cities
        {'name': 'Karachi', 'country': 'Pakistan', 'lat': 24.8607, 'lon': 67.0011, 'timezone': 'Asia/Karachi'},
        {'name': 'Lahore', 'country': 'Pakistan', 'lat': 31.5204, 'lon': 74.3587, 'timezone': 'Asia/Karachi'},
        {'name': 'Islamabad', 'country': 'Pakistan', 'lat': 33.6844, 'lon': 73.0479, 'timezone': 'Asia/Karachi'},
        {'name': 'Faisalabad', 'country': 'Pakistan', 'lat': 31.4167, 'lon': 73.0892, 'timezone': 'Asia/Karachi'},
        {'name': 'Rawalpindi', 'country': 'Pakistan', 'lat': 33.6007, 'lon': 73.0679, 'timezone': 'Asia/Karachi'},
        {'name': 'Multan', 'country': 'Pakistan', 'lat': 30.1575, 'lon': 71.5249, 'timezone': 'Asia/Karachi'},
        {'name': 'Gujranwala', 'country': 'Pakistan', 'lat': 32.1877, 'lon': 74.1945, 'timezone': 'Asia/Karachi'},
        {'name': 'Peshawar', 'country': 'Pakistan', 'lat': 34.0080, 'lon': 71.5785, 'timezone': 'Asia/Karachi'},
        {'name': 'Quetta', 'country': 'Pakistan', 'lat': 30.1798, 'lon': 66.9750, 'timezone': 'Asia/Karachi'},
        {'name': 'Sialkot', 'country': 'Pakistan', 'lat': 32.4924, 'lon': 74.5313, 'timezone': 'Asia/Karachi'},
        
        # Major International Cities
        {'name': 'London', 'country': 'United Kingdom', 'lat': 51.5074, 'lon': -0.1278, 'timezone': 'Europe/London'},
        {'name': 'New York', 'country': 'United States', 'lat': 40.7128, 'lon': -74.0060, 'timezone': 'America/New_York'},
        {'name': 'Tokyo', 'country': 'Japan', 'lat': 35.6762, 'lon': 139.6503, 'timezone': 'Asia/Tokyo'},
        {'name': 'Paris', 'country': 'France', 'lat': 48.8566, 'lon': 2.3522, 'timezone': 'Europe/Paris'},
        {'name': 'Berlin', 'country': 'Germany', 'lat': 52.5200, 'lon': 13.4050, 'timezone': 'Europe/Berlin'},
        {'name': 'Moscow', 'country': 'Russia', 'lat': 55.7558, 'lon': 37.6176, 'timezone': 'Europe/Moscow'},
        {'name': 'Dubai', 'country': 'UAE', 'lat': 25.2048, 'lon': 55.2708, 'timezone': 'Asia/Dubai'},
        {'name': 'Mumbai', 'country': 'India', 'lat': 19.0760, 'lon': 72.8777, 'timezone': 'Asia/Kolkata'},
        {'name': 'Sydney', 'country': 'Australia', 'lat': -33.8688, 'lon': 151.2093, 'timezone': 'Australia/Sydney'},
        {'name': 'Toronto', 'country': 'Canada', 'lat': 43.6532, 'lon': -79.3832, 'timezone': 'America/Toronto'},
        {'name': 'Singapore', 'country': 'Singapore', 'lat': 1.3521, 'lon': 103.8198, 'timezone': 'Asia/Singapore'},
        {'name': 'Hong Kong', 'country': 'China', 'lat': 22.3193, 'lon': 114.1694, 'timezone': 'Asia/Hong_Kong'},
        {'name': 'Seoul', 'country': 'South Korea', 'lat': 37.5665, 'lon': 126.9780, 'timezone': 'Asia/Seoul'},
        {'name': 'Bangkok', 'country': 'Thailand', 'lat': 13.7563, 'lon': 100.5018, 'timezone': 'Asia/Bangkok'},
        {'name': 'Cairo', 'country': 'Egypt', 'lat': 30.0444, 'lon': 31.2357, 'timezone': 'Africa/Cairo'},
        {'name': 'Rio de Janeiro', 'country': 'Brazil', 'lat': -22.9068, 'lon': -43.1729, 'timezone': 'America/Sao_Paulo'},
        {'name': 'Mexico City', 'country': 'Mexico', 'lat': 19.4326, 'lon': -99.1332, 'timezone': 'America/Mexico_City'},
        {'name': 'Istanbul', 'country': 'Turkey', 'lat': 41.0082, 'lon': 28.9784, 'timezone': 'Europe/Istanbul'},
        {'name': 'Madrid', 'country': 'Spain', 'lat': 40.4168, 'lon': -3.7038, 'timezone': 'Europe/Madrid'},
        {'name': 'Rome', 'country': 'Italy', 'lat': 41.9028, 'lon': 12.4964, 'timezone': 'Europe/Rome'},
        {'name': 'Amsterdam', 'country': 'Netherlands', 'lat': 52.3676, 'lon': 4.9041, 'timezone': 'Europe/Amsterdam'},
    ]
    
    cities = []
    for city_data in cities_data:
        city, created = City.objects.get_or_create(
            name=city_data['name'],
            country=city_data['country'],
            defaults={
                'latitude': city_data['lat'],
                'longitude': city_data['lon'],
                'timezone': city_data['timezone']
            }
        )
        cities.append(city)
        if created:
            print(f"✅ Created city: {city.name}, {city.country}")
        else:
            print(f"✅ City exists: {city.name}, {city.country}")
    
    return cities

def create_weather_data(cities):
    """Create current weather data for all cities"""
    weather_conditions = [
        {'desc': 'clear sky', 'icon': '01d', 'temp_range': (15, 35)},
        {'desc': 'few clouds', 'icon': '02d', 'temp_range': (12, 32)},
        {'desc': 'scattered clouds', 'icon': '03d', 'temp_range': (10, 30)},
        {'desc': 'broken clouds', 'icon': '04d', 'temp_range': (8, 28)},
        {'desc': 'shower rain', 'icon': '09d', 'temp_range': (5, 25)},
        {'desc': 'rain', 'icon': '10d', 'temp_range': (3, 22)},
        {'desc': 'thunderstorm', 'icon': '11d', 'temp_range': (2, 20)},
        {'desc': 'snow', 'icon': '13d', 'temp_range': (-5, 5)},
        {'desc': 'mist', 'icon': '50d', 'temp_range': (8, 25)},
    ]
    
    for city in cities:
        # Generate realistic weather based on city location
        if city.country == 'Pakistan':
            # Pakistan cities - warmer climate
            base_temp = random.randint(25, 40)
            humidity_range = (30, 80)
        elif city.country in ['Canada', 'Russia']:
            # Cold climate cities
            base_temp = random.randint(-10, 15)
            humidity_range = (40, 90)
        elif city.country in ['UAE', 'India', 'Thailand', 'Egypt']:
            # Hot climate cities
            base_temp = random.randint(30, 45)
            humidity_range = (50, 90)
        else:
            # Temperate climate cities
            base_temp = random.randint(10, 30)
            humidity_range = (40, 85)
        
        condition = random.choice(weather_conditions)
        temp = base_temp + random.randint(-5, 5)
        feels_like = temp + random.randint(-3, 3)
        humidity = random.randint(*humidity_range)
        pressure = random.randint(1000, 1020)
        wind_speed = random.uniform(0.5, 15.0)
        wind_direction = random.randint(0, 360)
        visibility = random.randint(5000, 10000)
        aqi = random.randint(20, 80)
        
        # Create or update weather data
        weather_data, created = WeatherData.objects.get_or_create(
            city=city,
            defaults={
                'temperature': temp,
                'feels_like': feels_like,
                'humidity': humidity,
                'pressure': pressure,
                'wind_speed': wind_speed,
                'wind_direction': wind_direction,
                'description': condition['desc'],
                'icon': condition['icon'],
                'visibility': visibility,
                'aqi': aqi,
                'timestamp': timezone.now()
            }
        )
        
        if created:
            print(f"✅ Created weather data for {city.name}: {temp}°C, {condition['desc']}")
        else:
            # Update existing data
            weather_data.temperature = temp
            weather_data.feels_like = feels_like
            weather_data.humidity = humidity
            weather_data.pressure = pressure
            weather_data.wind_speed = wind_speed
            weather_data.wind_direction = wind_direction
            weather_data.description = condition['desc']
            weather_data.icon = condition['icon']
            weather_data.visibility = visibility
            weather_data.aqi = aqi
            weather_data.timestamp = timezone.now()
            weather_data.save()
            print(f"✅ Updated weather data for {city.name}: {temp}°C, {condition['desc']}")

def create_weather_forecasts(cities):
    """Create weather forecast data for the next 5 days"""
    for city in cities:
        base_temp = random.randint(15, 30)
        
        for day in range(5):
            forecast_date = timezone.now() + timedelta(days=day)
            
            for hour in range(0, 24, 3):  # Every 3 hours
                forecast_time = forecast_date.replace(hour=hour, minute=0, second=0, microsecond=0)
                
                # Generate realistic hourly temperatures
                if hour in [0, 3, 21]:  # Night hours
                    temp = base_temp - random.randint(5, 15)
                elif hour in [12, 15, 18]:  # Day hours
                    temp = base_temp + random.randint(5, 15)
                else:
                    temp = base_temp + random.randint(-3, 8)
                
                humidity = random.randint(40, 90)
                pressure = random.randint(1000, 1020)
                wind_speed = random.uniform(0.5, 20.0)
                
                conditions = ['clear sky', 'few clouds', 'scattered clouds', 'broken clouds', 'shower rain', 'rain']
                description = random.choice(conditions)
                icon = '01d' if 'clear' in description else '02d' if 'few' in description else '03d' if 'scattered' in description else '04d' if 'broken' in description else '09d' if 'shower' in description else '10d'
                
                WeatherForecast.objects.get_or_create(
                    city=city,
                    forecast_time=forecast_time,
                    defaults={
                        'temperature': temp,
                        'humidity': humidity,
                        'pressure': pressure,
                        'wind_speed': wind_speed,
                        'description': description,
                        'icon': icon,
                        'created_at': timezone.now()
                    }
                )
        
        print(f"✅ Created 5-day forecast for {city.name}")

def create_historical_weather(cities):
    """Create historical weather data for the past 30 days"""
    for city in cities:
        base_temp = random.randint(15, 30)
        
        for day in range(30):
            date = timezone.now().date() - timedelta(days=day)
            
            max_temp = base_temp + random.randint(5, 15)
            min_temp = base_temp - random.randint(5, 15)
            avg_temp = (max_temp + min_temp) / 2
            avg_humidity = random.randint(40, 90)
            avg_pressure = random.randint(1000, 1020)
            precipitation = random.uniform(0, 20) if random.random() < 0.3 else 0  # 30% chance of rain
            
            HistoricalWeather.objects.get_or_create(
                city=city,
                date=date,
                defaults={
                    'max_temperature': max_temp,
                    'min_temperature': min_temp,
                    'avg_temperature': avg_temp,
                    'avg_humidity': avg_humidity,
                    'avg_pressure': avg_pressure,
                    'precipitation': precipitation
                }
            )
        
        print(f"✅ Created 30-day historical data for {city.name}")

def create_weather_alerts(cities):
    """Create some weather alerts for demonstration"""
    alert_types = [
        ('storm', 'Storm Warning', 'Severe thunderstorms expected with heavy rainfall'),
        ('heat', 'Heat Advisory', 'Extreme heat conditions, stay hydrated'),
        ('cold', 'Cold Warning', 'Freezing temperatures expected'),
        ('flood', 'Flood Warning', 'Heavy rainfall may cause flooding'),
        ('air_quality', 'Air Quality Alert', 'Poor air quality, limit outdoor activities'),
    ]
    
    for city in cities:
        if random.random() < 0.3:  # 30% chance of having alerts
            alert_type, title, description = random.choice(alert_types)
            severity = random.choice(['low', 'medium', 'high'])
            
            start_time = timezone.now() + timedelta(hours=random.randint(1, 24))
            end_time = start_time + timedelta(hours=random.randint(2, 12))
            
            WeatherAlert.objects.create(
                city=city,
                alert_type=alert_type,
                severity=severity,
                title=title,
                description=description,
                start_time=start_time,
                end_time=end_time,
                is_active=True
            )
            
            print(f"✅ Created {severity} alert for {city.name}: {title}")

def create_user_preferences():
    """Create user preferences for existing users"""
    users = User.objects.all()
    cities = City.objects.all()
    
    for user in users:
        if not UserPreference.objects.filter(user=user).exists():
            UserPreference.objects.create(
                user=user,
                default_city=random.choice(cities),
                temperature_unit='C',
                wind_speed_unit='m/s',
                pressure_unit='hPa',
                email_alerts=True,
                sms_alerts=False
            )
            print(f"✅ Created preferences for user: {user.username}")

def create_sample_users():
    """Create some sample users for demonstration"""
    sample_users = [
        {'username': 'weather_user1', 'email': 'user1@weather247.com', 'password': 'user123'},
        {'username': 'weather_user2', 'email': 'user2@weather247.com', 'password': 'user123'},
        {'username': 'student', 'email': 'student@weather247.com', 'password': 'student123'},
        {'username': 'demo_user', 'email': 'demo@weather247.com', 'password': 'demo123'},
    ]
    
    for user_data in sample_users:
        if not User.objects.filter(username=user_data['username']).exists():
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password']
            )
            print(f"✅ Created user: {user.username} with password: {user_data['password']}")

def main():
    """Main function to populate the database"""
    print("🚀 Starting database population...")
    print("=" * 50)
    
    try:
        # Create superuser
        create_superuser()
        print()
        
        # Create sample users
        create_sample_users()
        print()
        
        # Create cities
        print("🌍 Creating cities...")
        cities = create_cities()
        print()
        
        # Create weather data
        print("🌤️ Creating current weather data...")
        create_weather_data(cities)
        print()
        
        # Create forecasts
        print("📅 Creating weather forecasts...")
        create_weather_forecasts(cities)
        print()
        
        # Create historical data
        print("📊 Creating historical weather data...")
        create_historical_weather(cities)
        print()
        
        # Create alerts
        print("⚠️ Creating weather alerts...")
        create_weather_alerts(cities)
        print()
        
        # Create user preferences
        print("👤 Creating user preferences...")
        create_user_preferences()
        print()
        
        print("=" * 50)
        print("🎉 Database population completed successfully!")
        print()
        print("📋 Summary of created data:")
        print(f"   • Cities: {City.objects.count()}")
        print(f"   • Weather Data: {WeatherData.objects.count()}")
        print(f"   • Forecasts: {WeatherForecast.objects.count()}")
        print(f"   • Historical Data: {HistoricalWeather.objects.count()}")
        print(f"   • Weather Alerts: {WeatherAlert.objects.count()}")
        print(f"   • Users: {User.objects.count()}")
        print(f"   • User Preferences: {UserPreference.objects.count()}")
        print()
        print("🔗 Access your database at:")
        print("   • Django Admin: http://127.0.0.1:8000/admin/")
        print("   • Username: admin")
        print("   • Password: admin123")
        print()
        print("📁 Database file location:")
        print("   • backend/db.sqlite3")
        
    except Exception as e:
        print(f"❌ Error during database population: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
