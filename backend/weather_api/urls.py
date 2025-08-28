from django.urls import path
from . import views

app_name = 'weather_api'

urlpatterns = [
    path('test/', views.test_api, name='test_api'),
    path('current-weather/', views.current_weather, name='current_weather'),
    path('weather-forecast/', views.weather_forecast, name='weather_forecast'),
    path('historical-weather/', views.historical_weather, name='historical_weather'),
    path('city-list/', views.city_list, name='city_list'),
    path('weather-alerts/', views.weather_alerts, name='weather_alerts'),
    path('ai-prediction/', views.ai_weather_prediction, name='ai_weather_prediction'),
    path('historical-analysis/', views.historical_weather_analysis, name='historical_weather_analysis'),
    path('compare-cities/', views.compare_cities, name='compare_cities'),
    path('air-quality/', views.air_quality, name='air_quality'),
    path('weather-summary/', views.weather_summary, name='weather_summary'),
    path('search-city/', views.search_city, name='search_city'),

]
