#!/usr/bin/env python
"""
Production Startup Script for Weather-247
Checks all services and starts them properly
"""
import os
import sys
import subprocess
import time
from pathlib import Path

def check_service(service_name, check_command):
    """Check if a service is running"""
    try:
        result = subprocess.run(check_command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {service_name} is running")
            return True
        else:
            print(f"❌ {service_name} is not running")
            return False
    except Exception as e:
        print(f"❌ Error checking {service_name}: {e}")
        return False

def start_service(service_name, start_command):
    """Start a service"""
    try:
        print(f"🚀 Starting {service_name}...")
        subprocess.run(start_command, shell=True, check=True)
        print(f"✅ {service_name} started successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start {service_name}: {e}")
        return False

def check_database():
    """Check database connection"""
    try:
        import psycopg2
        from django.conf import settings
        
        # Get database settings
        db_settings = settings.DATABASES['default']
        
        # Try to connect
        conn = psycopg2.connect(
            host=db_settings['HOST'],
            port=db_settings['PORT'],
            database=db_settings['NAME'],
            user=db_settings['USER'],
            password=db_settings['PASSWORD']
        )
        conn.close()
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def check_redis():
    """Check Redis connection"""
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        print("✅ Redis connection successful")
        return True
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
        return False

def main():
    """Main startup function"""
    print("🚀 Weather-247 Production Startup")
    print("=" * 50)
    
    # Check current directory
    if not Path("manage.py").exists():
        print("❌ Please run this script from the backend directory")
        sys.exit(1)
    
    # Check Python environment
    print(f"🐍 Python version: {sys.version}")
    print(f"📁 Working directory: {os.getcwd()}")
    
    # Check environment file
    if not Path(".env").exists():
        print("⚠️  .env file not found. Creating from config.env...")
        if Path("config.env").exists():
            os.system("copy config.env .env")
            print("✅ .env file created from config.env")
        else:
            print("❌ config.env file not found. Please create .env file manually.")
    
    # Check services
    services_status = {}
    
    print("\n🔍 Checking Services...")
    print("-" * 30)
    
    # Check PostgreSQL
    services_status['postgresql'] = check_service(
        'PostgreSQL', 
        'pg_isready -h localhost -p 5432'
    )
    
    # Check Redis
    services_status['redis'] = check_service(
        'Redis', 
        'redis-cli ping'
    )
    
    # Check database connection
    services_status['database'] = check_database()
    
    # Check Redis connection
    services_status['redis_connection'] = check_redis()
    
    # Summary
    print("\n📊 Service Status Summary")
    print("-" * 30)
    for service, status in services_status.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {service}")
    
    # Start missing services
    if not services_status['postgresql']:
        print("\n🚀 Starting PostgreSQL...")
        start_service('PostgreSQL', 'net start postgresql-x64-15')
    
    if not services_status['redis']:
        print("\n🚀 Starting Redis...")
        start_service('Redis', 'net start Redis')
    
    # Final check
    print("\n🔍 Final Service Check...")
    print("-" * 30)
    
    time.sleep(2)  # Wait for services to start
    
    final_status = {}
    final_status['postgresql'] = check_service(
        'PostgreSQL', 
        'pg_isready -h localhost -p 5432'
    )
    final_status['redis'] = check_service(
        'Redis', 
        'redis-cli ping'
    )
    final_status['database'] = check_database()
    final_status['redis_connection'] = check_redis()
    
    # Final summary
    print("\n🎯 Final Status")
    print("-" * 30)
    all_working = all(final_status.values())
    
    for service, status in final_status.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {service}")
    
    if all_working:
        print("\n🎉 All services are running! You can now:")
        print("1. Start Django server: python manage.py runserver")
        print("2. Start Celery worker: celery -A weather247 worker --loglevel=info")
        print("3. Visit your application in the browser")
    else:
        print("\n⚠️  Some services are not working. Please check the errors above.")
        print("You may need to:")
        print("1. Install missing services")
        print("2. Check configuration files")
        print("3. Verify network settings")
    
    print("\n📚 Next Steps:")
            print("1. Configure SMS service credentials in .env file (optional)")
    print("2. Test SMS functionality")
    print("3. Run comprehensive tests: python test_all_features.py")
    print("4. Start production services")

if __name__ == '__main__':
    main()
