#!/usr/bin/env python
"""
Redis Demo Script for Weather-247
This script demonstrates Redis caching and Celery tasks
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather247.settings')
django.setup()

from django.core.cache import cache
from weather_api.tasks import fetch_weather_data_task, fetch_weather_alerts_task
import time

def demo_redis_caching():
    """Demonstrate Redis caching for weather data"""
    print("🌤️ Redis Weather Caching Demo")
    print("=" * 50)
    
    # Demo 1: Cache weather data
    print("\n1️⃣ Caching Weather Data...")
    
    # Simulate weather data
    weather_data = {
        'city': 'London',
        'temperature': 22.5,
        'condition': 'partly cloudy',
        'humidity': 65,
        'timestamp': time.time()
    }
    
    # Cache the data
    cache_key = f"weather_{weather_data['city'].lower()}"
    cache.set(cache_key, weather_data, timeout=300)  # 5 minutes
    print(f"✅ Cached weather data for {weather_data['city']}")
    
    # Retrieve from cache
    cached_data = cache.get(cache_key)
    if cached_data:
        print(f"✅ Retrieved from cache: {cached_data['temperature']}°C, {cached_data['condition']}")
    else:
        print("❌ Cache miss!")
    
    # Demo 2: Cache weather alerts
    print("\n2️⃣ Caching Weather Alerts...")
    
    alerts_data = {
        'city': 'London',
        'alerts': [
            {
                'event': 'Heavy Rain Warning',
                'description': 'Persistent rainfall expected',
                'start': int(time.time()),
                'end': int(time.time() + 3600)
            }
        ]
    }
    
    alerts_key = f"alerts_{alerts_data['city'].lower()}"
    cache.set(alerts_key, alerts_data, timeout=1800)  # 30 minutes
    print(f"✅ Cached alerts data for {alerts_data['city']}")
    
    # Demo 3: Cache performance comparison
    print("\n3️⃣ Cache Performance Test...")
    
    # Test cache hit performance
    start_time = time.time()
    for _ in range(100):
        cache.get(cache_key)
    cache_time = time.time() - start_time
    
    print(f"✅ 100 cache reads in {cache_time:.4f} seconds")
    print(f"✅ Average: {cache_time/100:.6f} seconds per read")
    
    # Demo 4: Cache expiration
    print("\n4️⃣ Cache Expiration Test...")
    
    # Set a short-lived cache entry
    cache.set('temp_test', 'will_expire_soon', timeout=2)
    print("✅ Set temporary cache entry (2 seconds)")
    
    # Check immediately
    immediate = cache.get('temp_test')
    print(f"✅ Immediate check: {immediate}")
    
    # Wait for expiration
    print("⏳ Waiting 3 seconds for expiration...")
    time.sleep(3)
    
    # Check after expiration
    expired = cache.get('temp_test')
    print(f"✅ After expiration: {expired}")
    
    # Demo 5: Celery task demonstration
    print("\n5️⃣ Celery Task Demo...")
    
    try:
        # This will be queued in Redis and processed by Celery worker
        print("🔄 Queuing weather data fetch task for London...")
        task = fetch_weather_data_task.delay('London')
        print(f"✅ Task queued with ID: {task.id}")
        
        print("🔄 Queuing weather alerts fetch task for London...")
        alerts_task = fetch_weather_alerts_task.delay('London')
        print(f"✅ Alerts task queued with ID: {alerts_task.id}")
        
        print("\n💡 Check your Celery worker terminal to see task execution!")
        
    except Exception as e:
        print(f"⚠️ Celery task error (worker might not be running): {str(e)}")
    
    # Demo 6: Cache statistics
    print("\n6️⃣ Cache Statistics...")
    
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        info = r.info()
        
        print(f"📊 Redis Version: {info.get('redis_version', 'Unknown')}")
        print(f"📊 Memory Used: {info.get('used_memory_human', 'Unknown')}")
        print(f"📊 Total Keys: {info.get('db0', {}).get('keys', 'Unknown')}")
        print(f"📊 Connected Clients: {info.get('connected_clients', 'Unknown')}")
        
    except Exception as e:
        print(f"⚠️ Could not get Redis stats: {str(e)}")
    
    # Cleanup
    print("\n🧹 Cleaning up demo data...")
    cache.delete(cache_key)
    cache.delete(alerts_key)
    cache.delete('temp_test')
    print("✅ Demo data cleaned up")
    
    print("\n" + "=" * 50)
    print("🎉 Redis Demo Completed Successfully!")
    print("\n🚀 Your Weather-247 project is now using Redis for:")
    print("   • Fast weather data caching")
    print("   • Background task processing")
    print("   • Session storage")
    print("   • Performance optimization")

if __name__ == '__main__':
    demo_redis_caching()
