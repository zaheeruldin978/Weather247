from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django import forms


class UserProfileForm(forms.ModelForm):
    """Form for user profile updates"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


@login_required
def profile(request):
    """User profile page"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user_management:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    context = {
        'form': form,
        'user': request.user,
    }
    return render(request, 'user_management/profile.html', context)


@login_required
def preferences(request):
    """User preferences page"""
    # Mock preferences data
    preferences = {
        'default_city': 'London',
        'temperature_unit': 'C',
        'wind_speed_unit': 'm/s',
        'pressure_unit': 'hPa',
        'email_alerts': True,
        'sms_alerts': False,
    }
    
    if request.method == 'POST':
        # Handle preferences update
        preferences['default_city'] = request.POST.get('default_city', 'London')
        preferences['temperature_unit'] = request.POST.get('temperature_unit', 'C')
        preferences['wind_speed_unit'] = request.POST.get('wind_speed_unit', 'm/s')
        preferences['pressure_unit'] = request.POST.get('pressure_unit', 'hPa')
        preferences['email_alerts'] = request.POST.get('email_alerts') == 'on'
        preferences['sms_alerts'] = request.POST.get('sms_alerts') == 'on'
        
        messages.success(request, 'Preferences updated successfully!')
        return redirect('user_management:preferences')
    
    context = {
        'preferences': preferences,
        'cities': ['London', 'New York', 'Tokyo', 'Sydney', 'Mumbai', 'Paris', 'Berlin', 'Rome'],
    }
    return render(request, 'user_management/preferences.html', context)


@login_required
def alert_settings(request):
    """Weather alert settings page"""
    # Mock alert subscriptions
    alert_subscriptions = [
        {
            'city': 'London',
            'alert_types': ['storm', 'heat', 'air_quality'],
            'email_enabled': True,
            'sms_enabled': False,
        },
        {
            'city': 'New York',
            'alert_types': ['storm', 'cold'],
            'email_enabled': True,
            'sms_enabled': True,
        }
    ]
    
    if request.method == 'POST':
        # Handle alert settings update
        messages.success(request, 'Alert settings updated successfully!')
        return redirect('user_management:alert_settings')
    
    context = {
        'alert_subscriptions': alert_subscriptions,
        'cities': ['London', 'New York', 'Tokyo', 'Sydney', 'Mumbai', 'Paris', 'Berlin', 'Rome'],
        'alert_types': [
            ('storm', 'Storm Warning'),
            ('heat', 'Heat Advisory'),
            ('cold', 'Cold Warning'),
            ('flood', 'Flood Warning'),
            ('air_quality', 'Air Quality Alert'),
        ]
    }
    return render(request, 'user_management/alert_settings.html', context)


@login_required
@require_POST
def update_preferences(request):
    """AJAX endpoint for updating user preferences"""
    try:
        # Handle preference updates
        response_data = {
            'success': True,
            'message': 'Preferences updated successfully!'
        }
    except Exception as e:
        response_data = {
            'success': False,
            'message': str(e)
        }
    
    return JsonResponse(response_data)
