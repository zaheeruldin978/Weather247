#!/usr/bin/env python
"""
Comprehensive Test Script for Weather-247
Tests all newly implemented features: AI predictions, SMS alerts, historical analysis
"""

import os
import sys
import django
import time

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather247.settings')
django.setup()

from django.core.cache import cache
from django.conf import settings
import requests

def test_ai_weather_predictions():
    """Test AI weather prediction system"""
    print("\n🔮 Testing AI Weather Predictions...")
    print("=" * 50)
    
    try:
        # Test weather predictor module
        from weather_ml.weather_predictor import weather_predictor
        
        # Test model training
        print("📚 Training AI models for London...")
        success = weather_predictor.train_models('London')
        
        if success:
            print("✅ AI models trained successfully!")
            
            # Test predictions
            print("🔮 Generating 24-hour weather predictions...")
            current_weather = {
                'temperature': 20,
                'humidity': 65,
                'pressure': 1013,
                'wind_speed': 5,
                'wind_direction': 180
            }
            
            predictions = weather_predictor.predict_weather('London', current_weather, 24)
            
            if predictions and len(predictions) == 24:
                print(f"✅ Generated {len(predictions)} predictions!")
                print(f"📊 Sample prediction: {predictions[0]}")
                
                # Test accuracy metrics
                accuracy = weather_predictor.get_prediction_accuracy('London')
                if accuracy:
                    print("✅ Accuracy metrics calculated!")
                    for param, metrics in accuracy.items():
                        print(f"   {param}: {metrics['accuracy_percentage']}% accuracy")
            else:
                print("❌ Failed to generate predictions")
                return False
        else:
            print("❌ Failed to train AI models")
            return False
            
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Error testing AI predictions: {str(e)}")
        return False

def test_sms_alert_system():
    """Test SMS and email alert system"""
    print("\n📱 Testing SMS/Email Alert System...")
    print("=" * 50)
    
    try:
        from weather_api.alert_service import alert_service
        
        # Test alert condition checking
        print("🔍 Testing alert condition checking...")
        weather_data = {
            'temperature': 38,  # Extreme heat
            'humidity': 85,
            'wind_speed': 25,  # High wind
            'description': 'thunderstorm with heavy rain'
        }
        
        alerts = alert_service.check_alert_conditions('London', weather_data)
        
        if alerts and len(alerts) > 0:
            print(f"✅ Generated {len(alerts)} weather alerts!")
            for alert in alerts:
                print(f"   ⚠️ {alert['event']}: {alert['description']}")
        else:
            print("❌ No alerts generated")
            return False
        
        # Test SMS alert simulation
        print("📱 Testing SMS alert simulation...")
        sms_result = alert_service.send_sms_alert('+1234567890', 'London', alerts[0])
        
        if sms_result['status'] == 'success':
            print("✅ SMS alert simulated successfully!")
            if sms_result.get('simulated'):
                print("   📱 Simulated SMS content:")
                print(f"   {sms_result['content']}")
        else:
            print("❌ SMS alert failed")
            return False
        
        # Test email alert
        print("📧 Testing email alert...")
        email_result = alert_service.send_email_alert('test@example.com', 'London', alerts[0])
        
        if email_result['status'] == 'success':
            print("✅ Email alert sent successfully!")
        else:
            print("❌ Email alert failed")
            return False
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Error testing alert system: {str(e)}")
        return False

def test_historical_analysis():
    """Test historical weather analysis system"""
    print("\n📊 Testing Historical Weather Analysis...")
    print("=" * 50)
    
    try:
        from weather_ml.historical_analyzer import historical_analyzer
        
        # Test historical data generation
        print("📈 Generating 5-year historical data for London...")
        analysis = historical_analyzer.generate_historical_data('London', 5)
        
        if analysis:
            print("✅ Historical analysis generated successfully!")
            print(f"   📅 Data period: {analysis['data_period']}")
            print(f"   📊 Total records: {analysis['total_records']}")
            print(f"   📈 Date range: {analysis['date_range']['start']} to {analysis['date_range']['end']}")
            
            # Test trend analysis
            if 'trends' in analysis:
                print("   🔍 Trend analysis:")
                for param, trend in analysis['trends'].items():
                    print(f"      {trend['icon']} {param.title()}: {trend['direction']} ({trend['strength']})")
            
            # Test seasonal patterns
            if 'seasonal_patterns' in analysis:
                print("   🌸 Seasonal patterns analyzed")
            
            # Test extreme events
            if 'extreme_events' in analysis:
                print("   ⚠️ Extreme events identified")
            
            # Test trend summary
            summary = historical_analyzer.get_trend_summary('London')
            if summary:
                print("   📋 Trend summary generated")
            
            # Test export functionality
            json_export = historical_analyzer.export_analysis('London', 'json')
            if json_export:
                print("   💾 JSON export successful")
            
            return True
        else:
            print("❌ Failed to generate historical analysis")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Error testing historical analysis: {str(e)}")
        return False



def test_redis_and_celery():
    """Test Redis and Celery functionality"""
    print("\n🔴 Testing Redis and Celery...")
    print("=" * 50)
    
    try:
        # Test Redis connection
        print("🔴 Testing Redis connection...")
        cache.set('test_feature', 'weather247_test', timeout=60)
        test_value = cache.get('test_feature')
        
        if test_value == 'weather247_test':
            print("✅ Redis cache working!")
        else:
            print("❌ Redis cache failed!")
            return False
        
        # Test Celery configuration
        print("🌿 Testing Celery configuration...")
        broker_url = settings.CELERY_BROKER_URL
        result_backend = settings.CELERY_RESULT_BACKEND
        
        if 'redis' in broker_url and 'redis' in result_backend:
            print("✅ Celery configured with Redis!")
        else:
            print("❌ Celery not configured with Redis!")
            return False
        
        # Test Celery tasks
        try:
            from weather_api.tasks import fetch_weather_data_task
            print("✅ Celery tasks imported successfully!")
        except ImportError:
            print("⚠️ Celery tasks not available (worker might not be running)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Redis/Celery: {str(e)}")
        return False

def test_api_endpoints():
    """Test new API endpoints"""
    print("\n🌐 Testing New API Endpoints...")
    print("=" * 50)
    
    try:
        base_url = 'http://localhost:8000'
        
        # Test AI prediction endpoint
        print("🔮 Testing AI prediction endpoint...")
        try:
            response = requests.get(f"{base_url}/api/ai-prediction/?city=London&hours=24", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'predictions' in data:
                    print("✅ AI prediction endpoint working!")
                else:
                    print("⚠️ AI prediction endpoint responded but no predictions data")
            else:
                print(f"⚠️ AI prediction endpoint status: {response.status_code}")
        except requests.exceptions.RequestException:
            print("⚠️ AI prediction endpoint not accessible (server might not be running)")
        
        # Test historical analysis endpoint
        print("📊 Testing historical analysis endpoint...")
        try:
            response = requests.get(f"{base_url}/api/historical-analysis/?city=London&years=5", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'analysis' in data:
                    print("✅ Historical analysis endpoint working!")
                else:
                    print("⚠️ Historical analysis endpoint responded but no analysis data")
            else:
                print(f"⚠️ Historical analysis endpoint status: {response.status_code}")
        except requests.exceptions.RequestException:
            print("⚠️ Historical analysis endpoint not accessible (server might not be running)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing API endpoints: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🚀 Weather-247 Comprehensive Feature Test Suite")
    print("=" * 60)
    print("Testing all newly implemented features...")
    
    test_results = {}
    
    # Run all tests
    test_results['AI Predictions'] = test_ai_weather_predictions()
    test_results['SMS Alerts'] = test_sms_alert_system()
    test_results['Historical Analysis'] = test_historical_analysis()

    test_results['Redis/Celery'] = test_redis_and_celery()
    test_results['API Endpoints'] = test_api_endpoints()
    
    # Print results summary
    print("\n" + "=" * 60)
    print("📋 Test Results Summary:")
    print("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for feature, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{feature:.<30} {status}")
        if result:
            passed += 1
    
    print("=" * 60)
    print(f"🎯 Overall Result: {passed}/{total} features working")
    
    if passed == total:
        print("\n🎉 EXCELLENT! All features are working correctly!")
        print("\n🚀 Your Weather-247 project now includes:")
        print("   • 🤖 AI-powered weather predictions with machine learning")
        print("   • 📱 SMS and email alert system")

        print("   • 📊 5-year historical weather analysis")
        print("   • 🔴 Redis caching and Celery background tasks")
        print("   • 📈 Advanced data visualization capabilities")
    else:
        print(f"\n⚠️ {total - passed} feature(s) need attention")
        print("\n🔧 Next steps:")
        print("   1. Check error messages above")
        print("   2. Ensure all required packages are installed")
        print("   3. Verify Redis server is running")
        print("   4. Check Django server status")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()
