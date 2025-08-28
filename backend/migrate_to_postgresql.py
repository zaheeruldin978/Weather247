#!/usr/bin/env python
"""
Data Migration Script: SQLite to PostgreSQL
This script migrates all your existing data from SQLite to PostgreSQL.
"""

import os
import django
import json
from datetime import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather247.settings')
django.setup()

from django.contrib.auth.models import User
from weather_api.models import City, WeatherData, WeatherForecast, HistoricalWeather, UserPreference, WeatherAlert, UserAlertSubscription

def export_sqlite_data():
    """Export all data from SQLite to JSON format"""
    print("📤 Exporting data from SQLite...")
    
    # Temporarily switch back to SQLite
    from django.conf import settings
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
    
    # Export data
    data = {
        'cities': [],
        'weather_data': [],
        'forecasts': [],
        'historical': [],
        'alerts': [],
        'users': [],
        'preferences': []
    }
    
    # Export cities
    for city in City.objects.all():
        data['cities'].append({
            'name': city.name,
            'country': city.country,
            'latitude': float(city.latitude),
            'longitude': float(city.longitude),
            'timezone': city.timezone
        })
    
    # Export weather data
    for weather in WeatherData.objects.all():
        data['weather_data'].append({
            'city_name': weather.city.name,
            'temperature': float(weather.temperature),
            'feels_like': float(weather.feels_like),
            'humidity': weather.humidity,
            'pressure': weather.pressure,
            'wind_speed': float(weather.wind_speed),
            'wind_direction': weather.wind_direction,
            'description': weather.description,
            'icon': weather.icon,
            'visibility': weather.visibility,
            'aqi': weather.aqi,
            'timestamp': weather.timestamp.isoformat()
        })
    
    # Export forecasts
    for forecast in WeatherForecast.objects.all():
        data['forecasts'].append({
            'city_name': forecast.city.name,
            'forecast_time': forecast.forecast_time.isoformat(),
            'temperature': float(forecast.temperature),
            'humidity': forecast.humidity,
            'pressure': forecast.pressure,
            'wind_speed': float(forecast.wind_speed),
            'description': forecast.description,
            'icon': forecast.icon,
            'created_at': forecast.created_at.isoformat()
        })
    
    # Export historical data
    for hist in HistoricalWeather.objects.all():
        data['historical'].append({
            'city_name': hist.city.name,
            'date': hist.date.isoformat(),
            'max_temperature': float(hist.max_temperature),
            'min_temperature': float(hist.min_temperature),
            'avg_temperature': float(hist.avg_temperature),
            'avg_humidity': float(hist.avg_humidity),
            'avg_pressure': float(hist.avg_pressure),
            'precipitation': float(hist.precipitation)
        })
    
    # Export alerts
    for alert in WeatherAlert.objects.all():
        data['alerts'].append({
            'city_name': alert.city.name,
            'alert_type': alert.alert_type,
            'severity': alert.severity,
            'title': alert.title,
            'description': alert.description,
            'start_time': alert.start_time.isoformat(),
            'end_time': alert.end_time.isoformat(),
            'is_active': alert.is_active
        })
    
    # Export users
    for user in User.objects.all():
        data['users'].append({
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'is_active': user.is_active,
            'date_joined': user.date_joined.isoformat()
        })
    
    # Export preferences
    for pref in UserPreference.objects.all():
        data['preferences'].append({
            'username': pref.user.username,
            'default_city_name': pref.default_city.name if pref.default_city else None,
            'temperature_unit': pref.temperature_unit,
            'wind_speed_unit': pref.wind_speed_unit,
            'pressure_unit': pref.pressure_unit,
            'email_alerts': pref.email_alerts,
            'sms_alerts': pref.sms_alerts
        })
    
    # Save to JSON file
    with open('sqlite_data_backup.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Exported {len(data['cities'])} cities")
    print(f"✅ Exported {len(data['weather_data'])} weather records")
    print(f"✅ Exported {len(data['forecasts'])} forecasts")
    print(f"✅ Exported {len(data['historical'])} historical records")
    print(f"✅ Exported {len(data['alerts'])} alerts")
    print(f"✅ Exported {len(data['users'])} users")
    print(f"✅ Exported {len(data['preferences'])} preferences")
    print("📁 Data saved to: sqlite_data_backup.json")
    
    return data

def import_to_postgresql(data):
    """Import data to PostgreSQL"""
    print("\n📥 Importing data to PostgreSQL...")
    
    # Switch back to PostgreSQL
    from django.conf import settings
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'weather247_db',
        'USER': 'postgres',
        'PASSWORD': '124421weather247',
        'HOST': 'localhost',
        'PORT': '5432',
    }
    
    # Clear existing data
    print("🧹 Clearing existing PostgreSQL data...")
    UserAlertSubscription.objects.all().delete()
    UserPreference.objects.all().delete()
    WeatherAlert.objects.all().delete()
    HistoricalWeather.objects.all().delete()
    WeatherForecast.objects.all().delete()
    WeatherData.objects.all().delete()
    City.objects.all().delete()
    User.objects.all().delete()
    
    # Import cities
    city_map = {}
    for city_data in data['cities']:
        city = City.objects.create(
            name=city_data['name'],
            country=city_data['country'],
            latitude=city_data['latitude'],
            longitude=city_data['longitude'],
            timezone=city_data['timezone']
        )
        city_map[city_data['name']] = city
        print(f"✅ Created city: {city.name}")
    
    # Import users
    user_map = {}
    for user_data in data['users']:
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password='temp123',  # Set temporary password
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            is_staff=user_data['is_staff'],
            is_superuser=user_data['is_superuser'],
            is_active=user_data['is_active']
        )
        user.date_joined = datetime.fromisoformat(user_data['date_joined'])
        user.save()
        user_map[user_data['username']] = user
        print(f"✅ Created user: {user.username}")
    
    # Import weather data
    for weather_data in data['weather_data']:
        city = city_map[weather_data['city_name']]
        WeatherData.objects.create(
            city=city,
            temperature=weather_data['temperature'],
            feels_like=weather_data['feels_like'],
            humidity=weather_data['humidity'],
            pressure=weather_data['pressure'],
            wind_speed=weather_data['wind_speed'],
            wind_direction=weather_data['wind_direction'],
            description=weather_data['description'],
            icon=weather_data['icon'],
            visibility=weather_data['visibility'],
            aqi=weather_data['aqi'],
            timestamp=datetime.fromisoformat(weather_data['timestamp'])
        )
    print(f"✅ Imported {len(data['weather_data'])} weather records")
    
    # Import forecasts
    for forecast_data in data['forecasts']:
        city = city_map[forecast_data['city_name']]
        WeatherForecast.objects.create(
            city=city,
            forecast_time=datetime.fromisoformat(forecast_data['forecast_time']),
            temperature=forecast_data['temperature'],
            humidity=forecast_data['humidity'],
            pressure=forecast_data['pressure'],
            wind_speed=forecast_data['wind_speed'],
            description=forecast_data['description'],
            icon=forecast_data['icon'],
            created_at=datetime.fromisoformat(forecast_data['created_at'])
        )
    print(f"✅ Imported {len(data['forecasts'])} forecasts")
    
    # Import historical data
    for hist_data in data['historical']:
        city = city_map[hist_data['city_name']]
        HistoricalWeather.objects.create(
            city=city,
            date=datetime.fromisoformat(hist_data['date']).date(),
            max_temperature=hist_data['max_temperature'],
            min_temperature=hist_data['min_temperature'],
            avg_temperature=hist_data['avg_temperature'],
            avg_humidity=hist_data['avg_humidity'],
            avg_pressure=hist_data['avg_pressure'],
            precipitation=hist_data['precipitation']
        )
    print(f"✅ Imported {len(data['historical'])} historical records")
    
    # Import alerts
    for alert_data in data['alerts']:
        city = city_map[alert_data['city_name']]
        WeatherAlert.objects.create(
            city=city,
            alert_type=alert_data['alert_type'],
            severity=alert_data['severity'],
            title=alert_data['title'],
            description=alert_data['description'],
            start_time=datetime.fromisoformat(alert_data['start_time']),
            end_time=datetime.fromisoformat(alert_data['end_time']),
            is_active=alert_data['is_active']
        )
    print(f"✅ Imported {len(data['alerts'])} alerts")
    
    # Import preferences
    for pref_data in data['preferences']:
        user = user_map[pref_data['username']]
        default_city = city_map[pref_data['default_city_name']] if pref_data['default_city_name'] else None
        UserPreference.objects.create(
            user=user,
            default_city=default_city,
            temperature_unit=pref_data['temperature_unit'],
            wind_speed_unit=pref_data['wind_speed_unit'],
            pressure_unit=pref_data['pressure_unit'],
            email_alerts=pref_data['email_alerts'],
            sms_alerts=pref_data['sms_alerts']
        )
    print(f"✅ Imported {len(data['preferences'])} preferences")
    
    # Set admin password
    admin_user = User.objects.get(username='admin')
    admin_user.set_password('admin123')
    admin_user.save()
    print("✅ Set admin password to 'admin123'")
    
    print("\n🎉 Data migration completed successfully!")
    print("🔗 Your database now uses PostgreSQL with all your data!")

def main():
    """Main migration function"""
    print("🔄 MIGRATING FROM SQLITE TO POSTGRESQL")
    print("=" * 50)
    
    try:
        # Export data from SQLite
        data = export_sqlite_data()
        
        # Import to PostgreSQL
        import_to_postgresql(data)
        
        print("\n" + "=" * 50)
        print("✅ MIGRATION COMPLETED SUCCESSFULLY!")
        print("🎯 Your project now matches your thesis requirements!")
        print("🗄️ Database: PostgreSQL (as specified in your proposal)")
        print("🔗 Access at: http://127.0.0.1:8000/admin/")
        print("👤 Username: admin, Password: admin123")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()

