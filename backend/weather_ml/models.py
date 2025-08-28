from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class WeatherModel(models.Model):
    """Model for storing trained weather prediction models"""
    MODEL_TYPES = [
        ('temperature', 'Temperature Prediction'),
        ('humidity', 'Humidity Prediction'),
        ('precipitation', 'Precipitation Prediction'),
        ('wind', 'Wind Speed Prediction'),
    ]
    
    name = models.CharField(max_length=100)
    model_type = models.CharField(max_length=20, choices=MODEL_TYPES)
    version = models.CharField(max_length=20)
    accuracy = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    model_file = models.FileField(upload_to='ml_models/', null=True, blank=True)
    parameters = models.JSONField(default=dict)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['name', 'version']
    
    def __str__(self):
        return f"{self.name} v{self.version} ({self.model_type})"


class WeatherPrediction(models.Model):
    """Model for storing weather predictions"""
    city = models.CharField(max_length=100)
    model = models.ForeignKey(WeatherModel, on_delete=models.CASCADE)
    prediction_time = models.DateTimeField()
    temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    humidity = models.IntegerField(null=True, blank=True)
    pressure = models.IntegerField(null=True, blank=True)
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    precipitation = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    confidence = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-prediction_time']
    
    def __str__(self):
        return f"{self.city} - {self.prediction_time}"


class ModelTrainingLog(models.Model):
    """Model for storing ML model training logs"""
    model = models.ForeignKey(WeatherModel, on_delete=models.CASCADE)
    training_start = models.DateTimeField()
    training_end = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], default='running')
    accuracy = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    loss = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    epochs = models.IntegerField(null=True, blank=True)
    training_data_size = models.IntegerField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-training_start']
    
    def __str__(self):
        return f"{self.model.name} - {self.training_start}"


class PredictionAccuracy(models.Model):
    """Model for tracking prediction accuracy over time"""
    model = models.ForeignKey(WeatherModel, on_delete=models.CASCADE)
    prediction = models.ForeignKey(WeatherPrediction, on_delete=models.CASCADE)
    actual_temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    actual_humidity = models.IntegerField(null=True, blank=True)
    actual_pressure = models.IntegerField(null=True, blank=True)
    actual_wind_speed = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    actual_precipitation = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    temperature_error = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    humidity_error = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    pressure_error = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    wind_error = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    precipitation_error = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    recorded_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-recorded_at']
    
    def __str__(self):
        return f"{self.model.name} - {self.prediction.city} - {self.recorded_at}"
