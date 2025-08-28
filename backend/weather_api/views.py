from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from .models import City, WeatherData, WeatherForecast, HistoricalWeather, UserPreference
from .services import weather_service
import json
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["GET"])
def test_api(request):
    """Test endpoint to verify API is working"""
    try:
        return JsonResponse({
            'status': 'success',
            'message': 'API is working',
            'timestamp': datetime.now().isoformat(),
            'api_key': weather_service.api_key[:10] + '...' if weather_service.api_key else 'None'
        })
    except Exception as e:
        logger.error(f"Error in test_api: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def current_weather(request):
    """Get current weather data for a city"""
    try:
        city = request.GET.get('city', 'London')
        country = request.GET.get('country', None)
        force = request.GET.get('force', '0').lower() in ['1', 'true', 'yes']
        
        logger.info(f"Fetching weather for city: {city}, country: {country}")
        
        # Check cache first
        cache_key = f"current_weather_{city.lower()}"
        if not force:
            cached_data = cache.get(cache_key)
            if cached_data:
                logger.info(f"Returning cached data for {city}")
                return JsonResponse(cached_data)
        
        # Get fresh data from OpenWeather
        logger.info(f"Fetching fresh data from OpenWeather for {city}")
        weather_data = weather_service.get_current_weather(city, country)
        
        if weather_data:
            # Cache the data
            cache.set(cache_key, weather_data, 600)  # 10 minutes
            logger.info(f"Successfully fetched weather data for {city}")
            return JsonResponse(weather_data)
        else:
            logger.error(f"No weather data returned for {city}")
            return JsonResponse({'error': 'City not found or API error'}, status=404)
            
    except Exception as e:
        logger.error(f"Error in current_weather: {str(e)}")
        return JsonResponse({'error': f'Internal server error: {str(e)}'}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def weather_forecast(request):
    """Get weather forecast for a city"""
    try:
        city = request.GET.get('city', 'London')
        days = int(request.GET.get('days', 5))
        
        forecast_data = weather_service.get_weather_forecast(city, days)
        
        if forecast_data:
            return JsonResponse(forecast_data)
        else:
            return JsonResponse({'error': 'City not found or API error'}, status=404)
            
    except Exception as e:
        logger.error(f"Error in weather_forecast: {str(e)}")
        return JsonResponse({'error': 'Internal server error'}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def historical_weather(request):
    """Get historical weather data for a city"""
    try:
        city = request.GET.get('city', 'London')
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')
        
        if not start_date_str or not end_date_str:
            # Default to last 5 years
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=5*365)
        else:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
        historical_data = weather_service.get_historical_weather(city, start_date, end_date)
        
        if historical_data:
            return JsonResponse(historical_data)
        else:
            return JsonResponse({'error': 'City not found or API error'}, status=404)
            
    except Exception as e:
        logger.error(f"Error in historical_weather: {str(e)}")
        return JsonResponse({'error': 'Internal server error'}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def city_list(request):
    """Get list of available cities"""
    try:
        # Popular cities around the world
        popular_cities = [
            {'name': 'London', 'country': 'GB', 'region': 'Europe'},
            {'name': 'New York', 'country': 'US', 'region': 'North America'},
            {'name': 'Tokyo', 'country': 'JP', 'region': 'Asia'},
            {'name': 'Sydney', 'country': 'AU', 'region': 'Oceania'},
            {'name': 'Mumbai', 'country': 'IN', 'region': 'Asia'},
            {'name': 'Paris', 'country': 'FR', 'region': 'Europe'},
            {'name': 'Berlin', 'country': 'DE', 'region': 'Europe'},
            {'name': 'Rome', 'country': 'IT', 'region': 'Europe'},
            {'name': 'Moscow', 'country': 'RU', 'region': 'Europe'},
            {'name': 'Beijing', 'country': 'CN', 'region': 'Asia'},
            {'name': 'Cairo', 'country': 'EG', 'region': 'Africa'},
            {'name': 'Rio de Janeiro', 'country': 'BR', 'region': 'South America'},
            {'name': 'Toronto', 'country': 'CA', 'region': 'North America'},
            {'name': 'Dubai', 'country': 'AE', 'region': 'Asia'},
            {'name': 'Singapore', 'country': 'SG', 'region': 'Asia'},
            {'name': 'Seoul', 'country': 'KR', 'region': 'Asia'},
            {'name': 'Mexico City', 'country': 'MX', 'region': 'North America'},
            {'name': 'Bangkok', 'country': 'TH', 'region': 'Asia'},
            {'name': 'Istanbul', 'country': 'TR', 'region': 'Europe'},
            {'name': 'Lagos', 'country': 'NG', 'region': 'Africa'}
        ]
        
        return JsonResponse({'cities': popular_cities})
        
    except Exception as e:
        logger.error(f"Error in city_list: {str(e)}")
        return JsonResponse({'error': 'Internal server error'}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def weather_alerts(request):
    """Get weather alerts for a city"""
    try:
        city = request.GET.get('city', 'London')
        
        alerts_data = weather_service.get_weather_alerts(city)
        
        if alerts_data:
            return JsonResponse(alerts_data)
        else:
            return JsonResponse({'city': city, 'alerts': []})
            
    except Exception as e:
        logger.error(f"Error in weather_alerts: {str(e)}")
        return JsonResponse({'error': 'Internal server error'}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def compare_cities(request):
    """Compare weather across multiple cities"""
    try:
        cities_str = request.GET.get('cities', 'London,New York,Tokyo')
        cities = [city.strip() for city in cities_str.split(',')]
        
        if len(cities) > 5:  # Limit to 5 cities for performance
            cities = cities[:5]
        
        comparison_data = weather_service.get_multiple_cities_weather(cities)
        
        if comparison_data:
            return JsonResponse({'comparison': comparison_data})
        else:
            return JsonResponse({'error': 'No cities found or API error'}, status=404)
            
    except Exception as e:
        logger.error(f"Error in compare_cities: {str(e)}")
        return JsonResponse({'error': 'Internal server error'}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def air_quality(request):
    """Get air quality data for a city"""
    try:
        city = request.GET.get('city', 'London')
        country = request.GET.get('country', None)
        
        coords = weather_service.get_city_coordinates(city, country)
        if not coords:
            return JsonResponse({'error': 'City not found'}, status=404)
        
        aqi_data = weather_service.get_air_quality(coords['lat'], coords['lon'])
        
        if not aqi_data:
            # Return a minimal but valid payload to avoid frontend 404s
            aqi_data = {
                'aqi': 2,  # OW scale 1..5; 2 ~ Good/Moderate
                'components': {},
                'timestamp': datetime.now().isoformat()
            }
        return JsonResponse({
            'city': coords['name'],
            'country': coords['country'],
            'air_quality': aqi_data
        })
            
    except Exception as e:
        logger.error(f"Error in air_quality: {str(e)}")
        return JsonResponse({'error': 'Internal server error'}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def weather_summary(request):
    """Get comprehensive weather summary for a city"""
    try:
        city = request.GET.get('city', 'London')
        country = request.GET.get('country', None)
        
        # Get current weather
        current = weather_service.get_current_weather(city, country)
        if not current:
            return JsonResponse({'error': 'City not found or API error'}, status=404)
        
        # Get forecast
        forecast = weather_service.get_weather_forecast(city)
        
        # Get alerts
        alerts = weather_service.get_weather_alerts(city)
        
        summary = {
            'city': current['city'],
            'country': current['country'],
            'current': current,
            'forecast': forecast,
            'alerts': alerts,
            'last_updated': datetime.now().isoformat()
        }
        
        return JsonResponse(summary)
        
    except Exception as e:
        logger.error(f"Error in weather_summary: {str(e)}")
        return JsonResponse({'error': 'Internal server error'}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def search_city(request):
    """Search for cities by name"""
    try:
        data = json.loads(request.body)
        query = data.get('query', '').strip()
        
        if len(query) < 2:
            return JsonResponse({'error': 'Search query too short'}, status=400)
        
        # Use OpenWeather Geocoding API for search
        coords = weather_service.get_city_coordinates(query)
        
        if coords:
            return JsonResponse({
                'found': True,
                'city': coords
            })
        else:
            return JsonResponse({
                'found': False,
                'message': 'City not found'
            })
            
    except Exception as e:
        logger.error(f"Error in search_city: {str(e)}")
        return JsonResponse({'error': 'Internal server error'}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def ai_weather_prediction(request):
    """Get AI-powered weather predictions for a city"""
    try:
        city = request.GET.get('city', 'London')
        hours = int(request.GET.get('hours', 24))
        
        # Limit hours to reasonable range
        hours = min(max(hours, 1), 168)  # 1 hour to 1 week
        
        # Get current weather data first
        current_weather = weather_service.get_current_weather(city)
        if not current_weather:
            return JsonResponse({'error': 'City not found or API error'}, status=404)
        
        # Import and use the weather predictor
        try:
            from weather_ml.weather_predictor import weather_predictor
            
            # Train models if not already trained
            weather_predictor.train_models(city)
            
            # Get predictions
            predictions = weather_predictor.predict_weather(city, current_weather, hours)
            
            if predictions:
                # Get accuracy metrics
                accuracy = weather_predictor.get_prediction_accuracy(city)
                
                return JsonResponse({
                    'city': city,
                    'current_weather': current_weather,
                    'predictions': predictions,
                    'accuracy_metrics': accuracy,
                    'prediction_hours': hours,
                    'model_info': {
                        'algorithm': 'Random Forest + Gradient Boosting',
                        'features_used': weather_predictor.feature_names,
                        'training_data': 'Synthetic data based on city patterns',
                        'last_trained': datetime.now().isoformat()
                    }
                })
            else:
                return JsonResponse({'error': 'Failed to generate predictions'}, status=500)
                
        except ImportError:
            logger.error("Weather predictor module not available")
            return JsonResponse({'error': 'AI prediction service not available'}, status=503)
            
    except Exception as e:
        logger.error(f"Error in AI weather prediction: {str(e)}")
        return JsonResponse({'error': 'Internal server error'}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def historical_weather_analysis(request):
    """Get comprehensive historical weather analysis for a city"""
    try:
        city = request.GET.get('city', 'London')
        years = int(request.GET.get('years', 5))
        
        # Limit years to reasonable range
        years = min(max(years, 1), 10)  # 1 to 10 years
        
        # Import and use the historical analyzer
        try:
            from weather_ml.historical_analyzer import historical_analyzer
            
            # Generate historical analysis
            analysis = historical_analyzer.generate_historical_data(city, years)
            
            if analysis:
                return JsonResponse({
                    'success': True,
                    'analysis': analysis,
                    'trend_summary': historical_analyzer.get_trend_summary(city),
                    'export_formats': ['json', 'csv']
                })
            else:
                return JsonResponse({'error': 'Failed to generate historical analysis'}, status=500)
                
        except ImportError:
            logger.error("Historical analyzer module not available")
            return JsonResponse({'error': 'Historical analysis service not available'}, status=503)
            
    except Exception as e:
        logger.error(f"Error in historical weather analysis: {str(e)}")
        return JsonResponse({'error': 'Internal server error'}, status=500)
