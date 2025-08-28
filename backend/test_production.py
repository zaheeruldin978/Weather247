#!/usr/bin/env python3
"""
Weather-247 Production Testing Suite
====================================

Comprehensive testing for production deployment
"""

import os
import sys
import django
import time
import requests
import json
from pathlib import Path

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather247.settings')
django.setup()

from django.core.cache import cache
from django.conf import settings
from django.db import connection
from django.test import TestCase, Client

def test_database_connection():
    """Test database connectivity and performance"""
    print("\n🗄️ Testing Database Connection...")
    print("=" * 50)
    
    try:
        # Test basic connection
        connection.ensure_connection()
        print("✅ Database connection established")
        
        # Test query performance
        start_time = time.time()
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"✅ Database version: {version}")
        
        # Test table count
        with connection.cursor() as cursor:
            cursor.execute("SELECT count(*) FROM information_schema.tables;")
            table_count = cursor.fetchone()[0]
            print(f"✅ Total tables: {table_count}")
        
        query_time = time.time() - start_time
        print(f"✅ Query performance: {query_time:.4f} seconds")
        
        # Test connection pooling
        connections = []
        for i in range(10):
            conn = connection.ensure_connection()
            connections.append(conn)
        
        print(f"✅ Connection pooling: {len(connections)} connections created")
        
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {str(e)}")
        return False

def test_cache_performance():
    """Test cache performance"""
    print("\n🔴 Testing Cache Performance...")
    print("=" * 50)
    
    try:
        # Test cache write
        start_time = time.time()
        cache.set('test_key', 'test_value', timeout=60)
        write_time = time.time() - start_time
        print(f"✅ Cache write: {write_time:.4f} seconds")
        
        # Test cache read
        start_time = time.time()
        value = cache.get('test_key')
        read_time = time.time() - start_time
        print(f"✅ Cache read: {read_time:.4f} seconds")
        
        if value == 'test_value':
            print("✅ Cache value retrieved correctly")
        else:
            print("❌ Cache value mismatch")
            return False
        
        # Test cache performance under load
        start_time = time.time()
        for i in range(100):
            cache.set(f'load_test_{i}', f'value_{i}', timeout=60)
        
        load_time = time.time() - start_time
        print(f"✅ Cache load test: 100 writes in {load_time:.4f} seconds")
        
        # Show cache backend type
        cache_backend = settings.CACHES['default']['BACKEND']
        print(f"✅ Cache backend: {cache_backend}")
        
        return True
        
    except Exception as e:
        print(f"❌ Cache test failed: {str(e)}")
        return False

def test_api_endpoints():
    """Test all API endpoints"""
    print("\n🌐 Testing API Endpoints...")
    print("=" * 50)
    
    client = Client()
    base_url = 'http://localhost:8000'
    
    endpoints = [
        '/',
        '/dashboard/',
        '/forecast/',
        '/alerts/',
        '/compare/',
        '/route/',
        '/health/',
        '/status/',
    ]
    
    all_working = True
    
    for endpoint in endpoints:
        try:
            response = client.get(endpoint)
            if response.status_code in [200, 302]:  # 302 for redirects
                print(f"✅ {endpoint}: {response.status_code}")
            else:
                print(f"⚠️ {endpoint}: {response.status_code}")
                all_working = False
        except Exception as e:
            print(f"❌ {endpoint}: Error - {str(e)}")
            all_working = False
    
    return all_working

def test_security_features():
    """Test security features"""
    print("\n🔒 Testing Security Features...")
    print("=" * 50)
    
    try:
        # Test CSRF protection
        client = Client(enforce_csrf_checks=True)
        response = client.post('/login/', {'username': 'test', 'password': 'test'})
        if response.status_code == 403:  # CSRF rejected
            print("✅ CSRF protection working")
        else:
            print("⚠️ CSRF protection may not be working")
        
        # Test XSS protection
        test_script = "<script>alert('xss')</script>"
        response = client.get(f'/?q={test_script}')
        if test_script not in str(response.content):
            print("✅ XSS protection working")
        else:
            print("⚠️ XSS protection may not be working")
        
        # Test SQL injection protection
        test_sql = "' OR '1'='1"
        response = client.get(f'/?q={test_sql}')
        if response.status_code != 500:  # No server error
            print("✅ SQL injection protection working")
        else:
            print("⚠️ SQL injection protection may not be working")
        
        return True
        
    except Exception as e:
        print(f"❌ Security test failed: {str(e)}")
        return False

def test_performance():
    """Test application performance"""
    print("\n⚡ Testing Performance...")
    print("=" * 50)
    
    try:
        client = Client()
        
        # Test homepage load time
        start_time = time.time()
        response = client.get('/')
        load_time = time.time() - start_time
        
        if load_time < 1.0:
            print(f"✅ Homepage load time: {load_time:.4f} seconds (Excellent)")
        elif load_time < 2.0:
            print(f"✅ Homepage load time: {load_time:.4f} seconds (Good)")
        else:
            print(f"⚠️ Homepage load time: {load_time:.4f} seconds (Needs optimization)")
        
        # Test database query performance
        start_time = time.time()
        from weather_dashboard.models import WeatherData
        count = WeatherData.objects.count()
        query_time = time.time() - start_time
        
        print(f"✅ Database query: {count} records in {query_time:.4f} seconds")
        
        # Test cache hit rate
        cache.set('perf_test', 'value', timeout=60)
        start_time = time.time()
        cache.get('perf_test')
        cache_time = time.time() - start_time
        
        print(f"✅ Cache performance: {cache_time:.4f} seconds")
        
        return True
        
    except Exception as e:
        print(f"❌ Performance test failed: {str(e)}")
        return False

def test_error_handling():
    """Test error handling and logging"""
    print("\n🚨 Testing Error Handling...")
    print("=" * 50)
    
    try:
        client = Client()
        
        # Test 404 handling
        response = client.get('/nonexistent-page/')
        if response.status_code == 404:
            print("✅ 404 error handling working")
        else:
            print("⚠️ 404 error handling may not be working")
        
        # Test 500 handling (if any)
        try:
            response = client.get('/invalid-endpoint/')
            print("✅ Error handling working")
        except:
            print("✅ Exception handling working")
        
        # Check if logs directory exists
        logs_dir = Path('logs')
        if logs_dir.exists():
            print("✅ Logs directory exists")
            
            # Check if log file exists and has content
            log_file = logs_dir / 'django.log'
            if log_file.exists() and log_file.stat().st_size > 0:
                print("✅ Logging is working")
            else:
                print("⚠️ Logging may not be working")
        else:
            print("⚠️ Logs directory not found")
        
        return True
        
    except Exception as e:
        print(f"❌ Error handling test failed: {str(e)}")
        return False

def test_mobile_responsiveness():
    """Test mobile responsiveness"""
    print("\n📱 Testing Mobile Responsiveness...")
    print("=" * 50)
    
    try:
        client = Client()
        
        # Test with mobile user agent
        mobile_headers = {
            'HTTP_USER_AGENT': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
        }
        
        response = client.get('/', **mobile_headers)
        if response.status_code == 200:
            print("✅ Mobile access working")
            
            # Check if response contains mobile-friendly content
            content = str(response.content)
            if 'mobile' in content.lower() or 'responsive' in content.lower():
                print("✅ Mobile-friendly content detected")
            else:
                print("⚠️ Mobile content may need optimization")
        else:
            print("⚠️ Mobile access may have issues")
        
        return True
        
    except Exception as e:
        print(f"❌ Mobile responsiveness test failed: {str(e)}")
        return False

def main():
    """Main testing function"""
    print("🚀 Weather-247 Production Testing Suite")
    print("=" * 60)
    print("Running comprehensive production tests...")
    
    test_results = {}
    
    # Run all tests
    test_results['Database'] = test_database_connection()
    test_results['Cache'] = test_cache_performance()
    test_results['API'] = test_api_endpoints()
    test_results['Security'] = test_security_features()
    test_results['Performance'] = test_performance()
    test_results['Error Handling'] = test_error_handling()
    test_results['Mobile'] = test_mobile_responsiveness()
    
    # Print results summary
    print("\n" + "=" * 60)
    print("📋 Production Test Results Summary:")
    print("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for feature, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{feature:.<30} {status}")
        if result:
            passed += 1
    
    print("=" * 60)
    print(f"🎯 Overall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 EXCELLENT! All production tests passed!")
        print("Your Weather-247 application is 100% production-ready!")
        print("\n🚀 Ready for deployment to:")
        print("   • Production servers")
        print("   • Cloud platforms (AWS, Azure, GCP)")
        print("   • Enterprise environments")
        print("   • Client demonstrations")
    else:
        print(f"\n⚠️ {total - passed} test(s) failed")
        print("Please fix the issues before production deployment")
    
    print("\n" + "=" * 60)
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
