from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class City(models.Model):
    """Model for storing city information"""
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    timezone = models.CharField(max_length=50, default='UTC')
    
    class Meta:
        verbose_name_plural = 'Cities'
        unique_together = ['name', 'country']
    
    def __str__(self):
        return f"{self.name}, {self.country}"


class WeatherData(models.Model):
    """Model for storing current weather data"""
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    feels_like = models.DecimalField(max_digits=5, decimal_places=2)
    humidity = models.IntegerField()
    pressure = models.IntegerField()
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2)
    wind_direction = models.IntegerField()
    description = models.CharField(max_length=200)
    icon = models.CharField(max_length=10)
    visibility = models.IntegerField()
    aqi = models.IntegerField()
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.city.name} - {self.temperature}°C at {self.timestamp}"


class WeatherForecast(models.Model):
    """Model for storing weather forecast data"""
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    forecast_time = models.DateTimeField()
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    humidity = models.IntegerField()
    pressure = models.IntegerField()
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.CharField(max_length=200)
    icon = models.CharField(max_length=10)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['forecast_time']
    
    def __str__(self):
        return f"{self.city.name} - {self.forecast_time}"


class HistoricalWeather(models.Model):
    """Model for storing historical weather data"""
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    date = models.DateField()
    max_temperature = models.DecimalField(max_digits=5, decimal_places=2)
    min_temperature = models.DecimalField(max_digits=5, decimal_places=2)
    avg_temperature = models.DecimalField(max_digits=5, decimal_places=2)
    avg_humidity = models.DecimalField(max_digits=5, decimal_places=2)
    avg_pressure = models.DecimalField(max_digits=7, decimal_places=2)
    precipitation = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    class Meta:
        ordering = ['-date']
        unique_together = ['city', 'date']
    
    def __str__(self):
        return f"{self.city.name} - {self.date}"


class UserPreference(models.Model):
    """Model for storing user preferences"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    temperature_unit = models.CharField(max_length=1, choices=[('C', 'Celsius'), ('F', 'Fahrenheit')], default='C')
    wind_speed_unit = models.CharField(max_length=4, choices=[('m/s', 'm/s'), ('mph', 'mph'), ('km/h', 'km/h')], default='m/s')
    pressure_unit = models.CharField(max_length=4, choices=[('hPa', 'hPa'), ('inHg', 'inHg')], default='hPa')
    email_alerts = models.BooleanField(default=True)
    sms_alerts = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return f"Preferences for {self.user.email}"


class WeatherAlert(models.Model):
    """Model for storing weather alerts"""
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('extreme', 'Extreme'),
    ]
    
    ALERT_TYPES = [
        ('storm', 'Storm Warning'),
        ('heat', 'Heat Advisory'),
        ('cold', 'Cold Warning'),
        ('flood', 'Flood Warning'),
        ('air_quality', 'Air Quality Alert'),
        ('other', 'Other'),
    ]
    
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.city.name} - {self.title}"


class UserAlertSubscription(models.Model):
    """Model for storing user alert subscriptions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    alert_types = models.JSONField(default=list)  # List of alert types to subscribe to
    email_enabled = models.BooleanField(default=True)
    sms_enabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['user', 'city']
    
    def __str__(self):
        return f"{self.user.email} - {self.city.name}"
