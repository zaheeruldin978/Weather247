from django.urls import path
from . import views

app_name = 'user_management'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('preferences/', views.preferences, name='preferences'),
    path('alerts/', views.alert_settings, name='alert_settings'),
]
