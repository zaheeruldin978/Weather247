from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
import requests
import json
from datetime import datetime, timedelta
from django.utils import timezone
import time
import platform
import django

def home(request):
    """Home page with weather overview"""
    context = {
        'title': 'Weather-247 - Real-time Weather Insights',
        'description': 'Get real-time, historical, and predictive weather insights through our interactive web platform.'
    }
    return render(request, 'weather_dashboard/home.html', context)

@login_required
def dashboard(request):
    """Main weather dashboard"""
    # Default cities for demonstration
    default_cities = ['London', 'New York', 'Tokyo', 'Sydney', 'Mumbai']
    
    context = {
        'title': 'Weather Dashboard',
        'cities': default_cities,
        'user': request.user,
    }
    return render(request, 'weather_dashboard/dashboard.html', context)

@login_required
def compare_cities(request):
    """City comparison page"""
    context = {
        'title': 'Compare Cities',
        'cities': ['London', 'New York', 'Tokyo', 'Sydney', 'Mumbai', 'Paris', 'Berlin', 'Rome'],
    }
    return render(request, 'weather_dashboard/compare.html', context)

@login_required
def forecast(request):
    """Weather forecast page with AI predictions"""
    context = {
        'title': '24-Hour Weather Forecast',
        'cities': ['London', 'New York', 'Tokyo', 'Sydney', 'Mumbai'],
    }
    return render(request, 'weather_dashboard/forecast.html', context)

@login_required
def alerts(request):
    """Weather alerts page"""
    context = {
        'title': 'Weather Alerts',
        'alerts': [
            {'type': 'Storm Warning', 'city': 'Miami', 'severity': 'High', 'time': '2 hours ago'},
            {'type': 'Heat Advisory', 'city': 'Phoenix', 'severity': 'Medium', 'time': '4 hours ago'},
        ]
    }
    return render(request, 'weather_dashboard/alerts.html', context)

@login_required
def route_planning(request):
    """Route planning with weather-aware suggestions"""
    context = {
        'title': 'Route Planning',
    }
    return render(request, 'weather_dashboard/route.html', context)

@login_required
def user_profile(request):
    """User profile and preferences"""
    context = {
        'title': 'User Profile',
        'user': request.user,
    }
    return render(request, 'weather_dashboard/profile.html', context)

@login_required
def user_settings(request):
    """User settings and preferences"""
    context = {
        'title': 'User Settings',
        'user': request.user,
    }
    return render(request, 'weather_dashboard/settings.html', context)



def get_weather_data(request):
    """API endpoint to get weather data for a city"""
    city = request.GET.get('city', 'London')
    
    # Mock weather data for demonstration
    weather_data = {
        'city': city,
        'temperature': 22,
        'feels_like': 24,
        'humidity': 65,
        'pressure': 1013,
        'description': 'Partly cloudy',
        'icon': '02d',
        'wind_speed': 5.2,
        'visibility': 10000,
        'aqi': 45,
        'timestamp': datetime.now().isoformat(),
    }
    
    return JsonResponse(weather_data)

def get_forecast_data(request):
    """API endpoint to get forecast data"""
    city = request.GET.get('city', 'London')
    
    # Mock forecast data
    forecast_data = {
        'city': city,
        'forecast': []
    }
    
    for i in range(24):
        forecast_data['forecast'].append({
            'time': (datetime.now() + timedelta(hours=i)).isoformat(),
            'temperature': 20 + (i % 10),
            'humidity': 60 + (i % 20),
            'description': 'Partly cloudy',
            'icon': '02d',
        })
    
    return JsonResponse(forecast_data)

def health_check(request):
    """Health check endpoint for monitoring"""
    from django.db import connection
    from django.core.cache import cache
    from django.conf import settings
    
    health_status = {
        'status': 'healthy',
        'timestamp': timezone.now().isoformat(),
        'version': '1.0.0',
        'checks': {}
    }
    
    # Database health check
    try:
        connection.ensure_connection()
        health_status['checks']['database'] = {'status': 'healthy', 'message': 'Connected'}
    except Exception as e:
        health_status['checks']['database'] = {'status': 'unhealthy', 'message': str(e)}
        health_status['status'] = 'unhealthy'
    
    # Cache health check
    try:
        cache.set('health_check', 'ok', timeout=10)
        cache_value = cache.get('health_check')
        if cache_value == 'ok':
            health_status['checks']['cache'] = {'status': 'healthy', 'message': 'Working'}
        else:
            health_status['checks']['cache'] = {'status': 'unhealthy', 'message': 'Cache not working'}
            health_status['status'] = 'unhealthy'
    except Exception as e:
        health_status['checks']['cache'] = {'status': 'unhealthy', 'message': str(e)}
        health_status['status'] = 'unhealthy'
    
    # Redis health check (only if Redis is configured)
    try:
        if 'redis' in str(settings.CACHES['default']['BACKEND']):
            import redis
            redis_client = redis.Redis.from_url(settings.CACHES['default']['LOCATION'])
            redis_client.ping()
            health_status['checks']['redis'] = {'status': 'healthy', 'message': 'Connected'}
        else:
            health_status['checks']['redis'] = {'status': 'not_configured', 'message': 'Using local memory cache'}
    except Exception as e:
        health_status['checks']['redis'] = {'status': 'unhealthy', 'message': str(e)}
        health_status['status'] = 'unhealthy'
    
    status_code = 200 if health_status['status'] == 'healthy' else 503
    return JsonResponse(health_status, status=status_code)

def system_status(request):
    """System status and metrics endpoint"""
    from django.db import connection
    from django.core.cache import cache
    from django.conf import settings
    import os
    
    # Database metrics
    db_stats = {}
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            db_stats['version'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT count(*) FROM information_schema.tables;")
            db_stats['table_count'] = cursor.fetchone()[0]
    except Exception as e:
        db_stats['error'] = str(e)
    
    # System metrics (simplified for development)
    system_stats = {
        'cpu_percent': 'N/A (development mode)',
        'memory_percent': 'N/A (development mode)',
        'disk_percent': 'N/A (development mode)',
        'uptime': 'N/A (development mode)',
    }
    
    # Application metrics
    app_stats = {
        'django_version': django.get_version(),
        'python_version': platform.python_version(),
        'installed_apps_count': len(settings.INSTALLED_APPS),
        'middleware_count': len(settings.MIDDLEWARE),
    }
    
    status_data = {
        'database': db_stats,
        'system': system_stats,
        'application': app_stats,
        'timestamp': timezone.now().isoformat(),
    }
    
    return JsonResponse(status_data)
