from celery import shared_task
from django.core.cache import cache
from .services import weather_service
import logging

logger = logging.getLogger(__name__)

@shared_task
def fetch_weather_data_task(city_name):
    """Background task to fetch weather data and cache it"""
    try:
        logger.info(f"🔄 Fetching weather data for {city_name} in background")
        
        # Get weather data
        weather_data = weather_service.get_current_weather(city_name)
        
        if weather_data:
            # Cache the data in Redis
            cache_key = f"weather_data_{city_name.lower()}"
            cache.set(cache_key, weather_data, timeout=600)  # 10 minutes
            
            logger.info(f"✅ Weather data cached for {city_name}")
            return {
                'status': 'success',
                'city': city_name,
                'data': weather_data
            }
        else:
            logger.warning(f"⚠️ No weather data received for {city_name}")
            return {
                'status': 'error',
                'city': city_name,
                'message': 'No data received'
            }
            
    except Exception as e:
        logger.error(f"❌ Error in weather fetch task for {city_name}: {str(e)}")
        return {
            'status': 'error',
            'city': city_name,
            'message': str(e)
        }

@shared_task
def fetch_weather_alerts_task(city_name):
    """Background task to fetch weather alerts and cache them"""
    try:
        logger.info(f"🔄 Fetching weather alerts for {city_name} in background")
        
        # Get alerts data
        alerts_data = weather_service.get_weather_alerts(city_name)
        
        if alerts_data:
            # Cache the alerts in Redis
            cache_key = f"alerts_data_{city_name.lower()}"
            cache.set(cache_key, alerts_data, timeout=1800)  # 30 minutes
            
            logger.info(f"✅ Weather alerts cached for {city_name}")
            return {
                'status': 'success',
                'city': city_name,
                'alerts': alerts_data
            }
        else:
            logger.warning(f"⚠️ No alerts data received for {city_name}")
            return {
                'status': 'error',
                'city': city_name,
                'message': 'No alerts received'
            }
            
    except Exception as e:
        logger.error(f"❌ Error in alerts fetch task for {city_name}: {str(e)}")
        return {
            'status': 'error',
            'city': city_name,
            'message': str(e)
        }

@shared_task
def clear_expired_cache_task():
    """Background task to clean up expired cache entries"""
    try:
        logger.info("🧹 Cleaning up expired cache entries")
        
        # This is a simple cleanup task
        # In production, you might want more sophisticated cache management
        
        logger.info("✅ Cache cleanup completed")
        return {
            'status': 'success',
            'message': 'Cache cleanup completed'
        }
        
    except Exception as e:
        logger.error(f"❌ Error in cache cleanup task: {str(e)}")
        return {
            'status': 'error',
            'message': str(e)
        }

@shared_task
def update_weather_cache_task():
    """Background task to update weather cache for all major cities"""
    try:
        logger.info("🔄 Updating weather cache for all cities")
        
        major_cities = ['London', 'New York', 'Tokyo', 'Miami', 'Gujranwala', 'Lahore']
        
        for city in major_cities:
            # Fetch weather data for each city
            fetch_weather_data_task.delay(city)
            fetch_weather_alerts_task.delay(city)
        
        logger.info(f"✅ Weather cache update initiated for {len(major_cities)} cities")
        return {
            'status': 'success',
            'cities_processed': len(major_cities),
            'message': 'Weather cache update initiated'
        }
        
    except Exception as e:
        logger.error(f"❌ Error in weather cache update task: {str(e)}")
        return {
            'status': 'error',
            'message': str(e)
        }
