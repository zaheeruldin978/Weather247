from django.contrib import admin
from .models import (
    City, 
    WeatherData, 
    WeatherForecast, 
    HistoricalWeather, 
    UserPreference, 
    WeatherAlert, 
    UserAlertSubscription
)

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'latitude', 'longitude', 'timezone')
    list_filter = ('country', 'timezone')
    search_fields = ('name', 'country')
    ordering = ('name', 'country')
    list_per_page = 25

@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ('city', 'temperature', 'feels_like', 'humidity', 'pressure', 'wind_speed', 'description', 'timestamp')
    list_filter = ('city__country', 'description', 'timestamp')
    search_fields = ('city__name', 'city__country')
    ordering = ('-timestamp', 'city__name')
    list_per_page = 25
    date_hierarchy = 'timestamp'
    
    fieldsets = (
        ('City Information', {
            'fields': ('city',)
        }),
        ('Weather Conditions', {
            'fields': ('temperature', 'feels_like', 'description', 'icon')
        }),
        ('Atmospheric Data', {
            'fields': ('humidity', 'pressure', 'wind_speed', 'wind_direction', 'visibility', 'aqi')
        }),
        ('Timing', {
            'fields': ('timestamp',)
        }),
    )

@admin.register(WeatherForecast)
class WeatherForecastAdmin(admin.ModelAdmin):
    list_display = ('city', 'forecast_time', 'temperature', 'humidity', 'pressure', 'wind_speed', 'description')
    list_filter = ('city__country', 'description', 'forecast_time')
    search_fields = ('city__name', 'city__country')
    ordering = ('forecast_time', 'city__name')
    list_per_page = 25
    date_hierarchy = 'forecast_time'
    
    fieldsets = (
        ('City Information', {
            'fields': ('city',)
        }),
        ('Forecast Details', {
            'fields': ('forecast_time', 'temperature', 'humidity', 'pressure', 'wind_speed', 'description', 'icon')
        }),
        ('Timing', {
            'fields': ('created_at',)
        }),
    )

@admin.register(HistoricalWeather)
class HistoricalWeatherAdmin(admin.ModelAdmin):
    list_display = ('city', 'date', 'max_temperature', 'min_temperature', 'avg_temperature', 'avg_humidity', 'precipitation')
    list_filter = ('city__country', 'date')
    search_fields = ('city__name', 'city__country')
    ordering = ('-date', 'city__name')
    list_per_page = 25
    date_hierarchy = 'date'
    
    fieldsets = (
        ('City Information', {
            'fields': ('city',)
        }),
        ('Temperature Data', {
            'fields': ('date', 'max_temperature', 'min_temperature', 'avg_temperature')
        }),
        ('Atmospheric Data', {
            'fields': ('avg_humidity', 'avg_pressure', 'precipitation')
        }),
    )

@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'default_city', 'temperature_unit', 'wind_speed_unit', 'pressure_unit', 'email_alerts', 'sms_alerts')
    list_filter = ('temperature_unit', 'wind_speed_unit', 'pressure_unit', 'email_alerts', 'sms_alerts')
    search_fields = ('user__username', 'user__email', 'default_city__name')
    ordering = ('user__username',)
    list_per_page = 25

@admin.register(WeatherAlert)
class WeatherAlertAdmin(admin.ModelAdmin):
    list_display = ('city', 'alert_type', 'severity', 'title', 'start_time', 'end_time', 'is_active')
    list_filter = ('alert_type', 'severity', 'is_active', 'city__country', 'start_time')
    search_fields = ('city__name', 'city__country', 'title', 'description')
    ordering = ('-start_time', 'city__name')
    list_per_page = 25
    date_hierarchy = 'start_time'
    
    fieldsets = (
        ('City Information', {
            'fields': ('city',)
        }),
        ('Alert Details', {
            'fields': ('alert_type', 'severity', 'title', 'description')
        }),
        ('Timing', {
            'fields': ('start_time', 'end_time', 'is_active')
        }),
    )

@admin.register(UserAlertSubscription)
class UserAlertSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'alert_types', 'email_enabled', 'sms_enabled', 'created_at')
    list_filter = ('email_enabled', 'sms_enabled', 'city__country', 'created_at')
    search_fields = ('user__username', 'user__email', 'city__name', 'city__country')
    ordering = ('-created_at', 'user__username')
    list_per_page = 25

# Customize the admin site
admin.site.site_header = "Weather-247 Administration"
admin.site.site_title = "Weather-247 Admin"
admin.site.index_title = "Welcome to Weather-247 Database Management"
