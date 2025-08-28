from django.urls import path
from . import views

app_name = 'weather_dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('compare/', views.compare_cities, name='compare_cities'),
    path('forecast/', views.forecast, name='forecast'),
    path('alerts/', views.alerts, name='alerts'),
    path('route/', views.route_planning, name='route_planning'),

    path('profile/', views.user_profile, name='user_profile'),
    path('settings/', views.user_settings, name='user_settings'),
    
    # Health Check Endpoints
    path('health/', views.health_check, name='health_check'),
    path('status/', views.system_status, name='system_status'),
]
