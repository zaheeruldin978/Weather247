import os
import logging
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from datetime import datetime, timedelta
import requests

logger = logging.getLogger(__name__)

class AlertService:
    """Service for sending weather alerts via SMS and email"""
    
    def __init__(self):
                self.sms_account_sid = getattr(settings, 'SMS_ACCOUNT_SID', '')
        self.sms_auth_token = getattr(settings, 'SMS_AUTH_TOKEN', '')
        self.sms_phone_number = getattr(settings, 'SMS_PHONE_NUMBER', '')

        # Check if SMS is configured
        self.sms_available = all([
            self.sms_account_sid,
            self.sms_auth_token,
            self.sms_phone_number
        ])

        if not self.sms_available:
            logger.warning("⚠️ SMS not configured - SMS alerts will be simulated")
    
    def send_sms_alert(self, phone_number, city, alert_data):
        """Send SMS alert using SMS service"""
        try:
            if not self.sms_available:
                return self._simulate_sms_alert(phone_number, city, alert_data)
            
            # Prepare SMS message
            message = self._format_sms_message(city, alert_data)
            
            # Send via SMS service (placeholder for future implementation)
            logger.info(f"📱 SMS service not implemented yet - simulating SMS to {phone_number}")
            
            return {
                'status': 'success',
                'message': 'SMS alert sent successfully (simulated)',
                'sms_message_id': 'simulated'
            }
                
        except Exception as e:
            logger.error(f"❌ Error sending SMS alert: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _simulate_sms_alert(self, phone_number, city, alert_data):
        """Simulate SMS alert for development/testing"""
        message = self._format_sms_message(city, alert_data)
        
        logger.info(f"📱 SIMULATED SMS to {phone_number}: {message}")
        
        return {
            'status': 'success',
            'message': 'SMS alert simulated successfully',
            'simulated': True,
            'content': message
        }
    
    def send_email_alert(self, email, city, alert_data):
        """Send email alert"""
        try:
            # Prepare email content
            subject = f"Weather Alert for {city} - {alert_data.get('event', 'Weather Warning')}"
            
            # Create HTML email template
            html_message = render_to_string('weather_alerts/email_alert.html', {
                'city': city,
                'alert': alert_data,
                'timestamp': datetime.now(),
                'unsubscribe_url': f"{settings.SITE_URL}/unsubscribe/{email}" if hasattr(settings, 'SITE_URL') else '#'
            })
            
            # Send email
            send_mail(
                subject=subject,
                message=self._format_email_text(city, alert_data),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                html_message=html_message,
                fail_silently=False
            )
            
            logger.info(f"✅ Email alert sent to {email} for {city}")
            return {
                'status': 'success',
                'message': 'Email alert sent successfully'
            }
            
        except Exception as e:
            logger.error(f"❌ Error sending email alert: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _format_sms_message(self, city, alert_data):
        """Format SMS message content"""
        event = alert_data.get('event', 'Weather Alert')
        description = alert_data.get('description', 'No description available')
        
        # Format start and end times
        start_time = alert_data.get('start')
        end_time = alert_data.get('end')
        
        if start_time and end_time:
            start_dt = datetime.fromtimestamp(start_time)
            end_dt = datetime.fromtimestamp(end_time)
            time_info = f"From {start_dt.strftime('%H:%M')} to {end_dt.strftime('%H:%M')}"
        else:
            time_info = "Time information unavailable"
        
        message = f"🌤️ WEATHER ALERT - {city}\n"
        message += f"⚠️ {event}\n"
        message += f"📝 {description}\n"
        message += f"⏰ {time_info}\n"
        message += f"🔔 Weather-247"
        
        return message
    
    def _format_email_text(self, city, alert_data):
        """Format plain text email content"""
        event = alert_data.get('event', 'Weather Alert')
        description = alert_data.get('description', 'No description available')
        
        text = f"Weather Alert for {city}\n"
        text += f"Event: {event}\n"
        text += f"Description: {description}\n"
        text += f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        text += f"\nStay safe and check Weather-247 for updates."
        
        return text
    
    def check_alert_conditions(self, city, weather_data):
        """Check if weather conditions warrant alerts"""
        alerts = []
        
        try:
            temperature = weather_data.get('temperature', 20)
            humidity = weather_data.get('humidity', 50)
            wind_speed = weather_data.get('wind_speed', 5)
            description = weather_data.get('description', '').lower()
            
            # Temperature alerts
            if temperature > 35:
                alerts.append({
                    'event': 'Extreme Heat Warning',
                    'description': f'Temperature is {temperature}°C - extreme heat conditions',
                    'severity': 'high',
                    'start': datetime.now().timestamp(),
                    'end': (datetime.now() + timedelta(hours=6)).timestamp()
                })
            elif temperature < -10:
                alerts.append({
                    'event': 'Extreme Cold Warning',
                    'description': f'Temperature is {temperature}°C - extreme cold conditions',
                    'severity': 'high',
                    'start': datetime.now().timestamp(),
                    'end': (datetime.now() + timedelta(hours=6)).timestamp()
                })
            
            # Humidity alerts
            if humidity > 90:
                alerts.append({
                    'event': 'High Humidity Alert',
                    'description': f'Humidity is {humidity}% - very humid conditions',
                    'severity': 'medium',
                    'start': datetime.now().timestamp(),
                    'end': (datetime.now() + timedelta(hours=4)).timestamp()
                })
            
            # Wind alerts
            if wind_speed > 25:
                alerts.append({
                    'event': 'High Wind Warning',
                    'description': f'Wind speed is {wind_speed} m/s - dangerous wind conditions',
                    'severity': 'high',
                    'start': datetime.now().timestamp(),
                    'end': (datetime.now() + timedelta(hours=3)).timestamp()
                })
            elif wind_speed > 15:
                alerts.append({
                    'event': 'Wind Advisory',
                    'description': f'Wind speed is {wind_speed} m/s - strong winds expected',
                    'severity': 'medium',
                    'start': datetime.now().timestamp(),
                    'end': (datetime.now() + timedelta(hours=4)).timestamp()
                })
            
            # Weather condition alerts
            if any(word in description for word in ['thunderstorm', 'storm']):
                alerts.append({
                    'event': 'Thunderstorm Warning',
                    'description': f'Thunderstorm conditions: {description}',
                    'severity': 'high',
                    'start': datetime.now().timestamp(),
                    'end': (datetime.now() + timedelta(hours=2)).timestamp()
                })
            
            if any(word in description for word in ['heavy rain', 'torrential']):
                alerts.append({
                    'event': 'Heavy Rain Warning',
                    'description': f'Heavy rainfall: {description}',
                    'severity': 'medium',
                    'start': datetime.now().timestamp(),
                    'end': (datetime.now() + timedelta(hours=3)).timestamp()
                })
            
            if any(word in description for word in ['snow', 'blizzard']):
                alerts.append({
                    'event': 'Winter Weather Warning',
                    'description': f'Winter conditions: {description}',
                    'severity': 'medium',
                    'start': datetime.now().timestamp(),
                    'end': (datetime.now() + timedelta(hours=4)).timestamp()
                })
            
            logger.info(f"✅ Generated {len(alerts)} alerts for {city}")
            return alerts
            
        except Exception as e:
            logger.error(f"❌ Error checking alert conditions for {city}: {str(e)}")
            return []
    
    def send_bulk_alerts(self, city, alert_data, subscribers):
        """Send alerts to multiple subscribers"""
        results = {
            'sms_sent': 0,
            'sms_failed': 0,
            'email_sent': 0,
            'email_failed': 0,
            'total_subscribers': len(subscribers)
        }
        
        for subscriber in subscribers:
            try:
                # Send SMS if enabled
                if subscriber.get('sms_enabled') and subscriber.get('phone_number'):
                    sms_result = self.send_sms_alert(
                        subscriber['phone_number'],
                        city,
                        alert_data
                    )
                    
                    if sms_result['status'] == 'success':
                        results['sms_sent'] += 1
                    else:
                        results['sms_failed'] += 1
                
                # Send email if enabled
                if subscriber.get('email_enabled') and subscriber.get('email'):
                    email_result = self.send_email_alert(
                        subscriber['email'],
                        city,
                        alert_data
                    )
                    
                    if email_result['status'] == 'success':
                        results['email_sent'] += 1
                    else:
                        results['email_failed'] += 1
                        
            except Exception as e:
                logger.error(f"❌ Error sending alert to subscriber: {str(e)}")
                results['sms_failed'] += 1
                results['email_failed'] += 1
        
        logger.info(f"📊 Bulk alert results for {city}: {results}")
        return results

# Global instance
alert_service = AlertService()
