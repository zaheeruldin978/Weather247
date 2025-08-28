#!/usr/bin/env python
"""
Redis Connection Test Script
This script tests Redis connectivity and basic operations
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
from django.conf import settings
import redis

def test_redis_connection():
    """Test basic Redis connection"""
    print("🔍 Testing Redis Connection...")
    
    try:
        # Test Django cache (Redis)
        cache.set('test_key', 'test_value', timeout=60)
        test_value = cache.get('test_key')
        
        if test_value == 'test_value':
            print("✅ Django Redis cache is working!")
        else:
            print("❌ Django Redis cache failed!")
            return False
            
        # Test direct Redis connection
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.set('direct_test', 'direct_value')
        direct_value = r.get('direct_test')
        
        if direct_value.decode() == 'direct_value':
            print("✅ Direct Redis connection is working!")
        else:
            print("❌ Direct Redis connection failed!")
            return False
            
        # Test Redis info
        info = r.info()
        print(f"📊 Redis Version: {info.get('redis_version', 'Unknown')}")
        print(f"📊 Redis Memory: {info.get('used_memory_human', 'Unknown')}")
        print(f"📊 Redis Keys: {info.get('db0', {}).get('keys', 'Unknown')}")
        
        # Clean up test keys
        cache.delete('test_key')
        r.delete('direct_test')
        
        return True
        
    except Exception as e:
        print(f"❌ Redis connection error: {str(e)}")
        return False

def test_celery_config():
    """Test Celery configuration"""
    print("\n🔍 Testing Celery Configuration...")
    
    try:
        broker_url = settings.CELERY_BROKER_URL
        result_backend = settings.CELERY_RESULT_BACKEND
        
        print(f"✅ Celery Broker URL: {broker_url}")
        print(f"✅ Celery Result Backend: {result_backend}")
        
        if 'redis' in broker_url and 'redis' in result_backend:
            print("✅ Celery is configured to use Redis!")
            return True
        else:
            print("❌ Celery is not configured to use Redis!")
            return False
            
    except Exception as e:
        print(f"❌ Celery configuration error: {str(e)}")
        return False

def test_cache_operations():
    """Test cache operations"""
    print("\n🔍 Testing Cache Operations...")
    
    try:
        # Test setting cache
        cache.set('weather_london', {'temp': 20, 'condition': 'sunny'}, timeout=300)
        print("✅ Cache set operation successful")
        
        # Test getting cache
        weather_data = cache.get('weather_london')
        if weather_data and weather_data.get('temp') == 20:
            print("✅ Cache get operation successful")
        else:
            print("❌ Cache get operation failed")
            return False
            
        # Test cache expiration
        cache.set('expire_test', 'will_expire', timeout=1)
        import time
        time.sleep(2)
        expired_value = cache.get('expire_test')
        if expired_value is None:
            print("✅ Cache expiration working correctly")
        else:
            print("❌ Cache expiration not working")
            return False
            
        # Clean up
        cache.delete('weather_london')
        
        return True
        
    except Exception as e:
        print(f"❌ Cache operations error: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🚀 Redis and Celery Test Suite")
    print("=" * 40)
    
    # Test Redis connection
    redis_ok = test_redis_connection()
    
    # Test Celery configuration
    celery_ok = test_celery_config()
    
    # Test cache operations
    cache_ok = test_cache_operations()
    
    print("\n" + "=" * 40)
    print("📋 Test Results Summary:")
    print(f"Redis Connection: {'✅ PASS' if redis_ok else '❌ FAIL'}")
    print(f"Celery Config: {'✅ PASS' if celery_ok else '❌ FAIL'}")
    print(f"Cache Operations: {'✅ PASS' if cache_ok else '❌ FAIL'}")
    
    if all([redis_ok, celery_ok, cache_ok]):
        print("\n🎉 All tests passed! Redis and Celery are working correctly.")
        print("\n🚀 Next steps:")
        print("1. Start Celery worker: celery -A weather247 worker --loglevel=info")
        print("2. Start Celery beat: celery -A weather247 beat --loglevel=info")
        print("3. Your Django app will now use Redis for caching and background tasks!")
    else:
        print("\n❌ Some tests failed. Please check the error messages above.")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure Redis server is running")
        print("2. Check Redis connection settings")
        print("3. Verify Celery configuration")

if __name__ == '__main__':
    main()
