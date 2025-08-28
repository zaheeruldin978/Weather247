#!/usr/bin/env python
"""
Database Summary Script for Weather-247
This script shows a comprehensive summary of all data in your database.
"""

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather247.settings')
django.setup()

from django.contrib.auth.models import User
from weather_api.models import City, WeatherData, WeatherForecast, HistoricalWeather, UserPreference, WeatherAlert, UserAlertSubscription

def show_database_summary():
    """Show comprehensive database summary"""
    print("🌍 WEATHER-247 DATABASE SUMMARY")
    print("=" * 60)
    
    # Count all records
    print(f"📊 TOTAL RECORDS:")
    print(f"   • Cities: {City.objects.count()}")
    print(f"   • Current Weather Data: {WeatherData.objects.count()}")
    print(f"   • Weather Forecasts: {WeatherForecast.objects.count()}")
    print(f"   • Historical Weather: {HistoricalWeather.objects.count()}")
    print(f"   • Weather Alerts: {WeatherAlert.objects.count()}")
    print(f"   • Users: {User.objects.count()}")
    print(f"   • User Preferences: {UserPreference.objects.count()}")
    print(f"   • Alert Subscriptions: {UserAlertSubscription.objects.count()}")
    print()
    
    # Show cities by country
    print("🌍 CITIES BY COUNTRY:")
    cities_by_country = {}
    for city in City.objects.all():
        if city.country not in cities_by_country:
            cities_by_country[city.country] = []
        cities_by_country[city.country].append(city.name)
    
    for country, cities in cities_by_country.items():
        print(f"   • {country}: {', '.join(cities)}")
    print()
    
    # Show sample weather data
    print("🌤️ SAMPLE CURRENT WEATHER DATA:")
    for weather in WeatherData.objects.all()[:5]:  # Show first 5
        print(f"   • {weather.city.name}: {weather.temperature}°C, {weather.description}, Humidity: {weather.humidity}%")
    print()
    
    # Show active alerts
    print("⚠️ ACTIVE WEATHER ALERTS:")
    active_alerts = WeatherAlert.objects.filter(is_active=True)
    if active_alerts.exists():
        for alert in active_alerts:
            print(f"   • {alert.city.name}: {alert.title} ({alert.severity} severity)")
    else:
        print("   • No active alerts")
    print()
    
    # Show users
    print("👤 USERS:")
    for user in User.objects.all():
        print(f"   • {user.username} ({user.email}) - {'Staff' if user.is_staff else 'Regular User'}")
    print()
    
    print("=" * 60)
    print("🎯 ACCESS YOUR DATABASE AT: http://127.0.0.1:8000/admin/")
    print("   Username: admin")
    print("   Password: admin123")
    print("=" * 60)

if __name__ == '__main__':
    show_database_summary()
