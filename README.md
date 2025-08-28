# 🌤️ Weather247 - Advanced Weather Forecasting System

A comprehensive weather forecasting and alert system built with Django, featuring machine learning predictions, real-time alerts, and a modern responsive frontend.

## 🚀 Features

### Backend (Django)
- **User Management**: Registration, authentication, and profile management
- **Weather API Integration**: OpenWeatherMap API integration for real-time data
- **Machine Learning**: Predictive models for temperature, humidity, pressure, and wind speed
- **Alert System**: Automated weather alerts via email and SMS
- **Database**: PostgreSQL support with SQLite fallback
- **Production Ready**: Redis caching, Celery tasks, and comprehensive testing

### Frontend (HTML/CSS/JavaScript)
- **Responsive Design**: Modern UI with Tailwind CSS
- **Interactive Dashboard**: Real-time weather data visualization
- **User Interface**: Clean, professional design with weather icons
- **Mobile Friendly**: Optimized for all device sizes

## 🛠️ Technology Stack

- **Backend**: Django 4.2+, Python 3.8+
- **Database**: PostgreSQL (production), SQLite (development)
- **Cache**: Redis
- **Task Queue**: Celery
- **Frontend**: HTML5, CSS3, JavaScript, Tailwind CSS
- **ML**: Scikit-learn, Pandas, NumPy
- **Deployment**: Gunicorn, Nginx

## 📁 Project Structure

```
weather247/
├── backend/                 # Django backend application
│   ├── weather247/         # Main Django project
│   ├── user_management/    # User authentication & profiles
│   ├── weather_api/        # Weather data & API services
│   ├── weather_dashboard/  # Dashboard views & URLs
│   ├── weather_ml/         # Machine learning models
│   └── static/             # Static files (CSS, JS, images)
├── frontend/               # Frontend templates & assets
│   ├── templates/          # HTML templates
│   ├── icons/             # Weather icons
│   └── logo.png           # Project logo
└── documentation/          # Project documentation (separate)
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL (optional, SQLite for development)
- Redis (optional for development)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/zaheeruldin978/weather-247.git
   cd weather-247
   ```

2. **Setup backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Environment configuration**
   ```bash
   cp env_example.txt .env
   # Edit .env with your configuration
   ```

4. **Database setup**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **Run the application**
   ```bash
   python manage.py runserver
   ```

## 🔧 Configuration

### Environment Variables
- `DEBUG`: Set to False for production
- `SECRET_KEY`: Django secret key
- `DATABASE_URL`: Database connection string
- `OPENWEATHER_API_KEY`: OpenWeatherMap API key
- `REDIS_URL`: Redis connection (optional)

### Database
- **Development**: SQLite (default)
- **Production**: PostgreSQL with connection pooling

## 📊 API Endpoints

- `/api/weather/current/` - Current weather data
- `/api/weather/forecast/` - Weather forecasts
- `/api/alerts/` - Weather alerts
- `/api/users/` - User management
- `/health/` - System health check
- `/status/` - System status

## 🤖 Machine Learning Features

- **Temperature Prediction**: 24-hour temperature forecasting
- **Humidity Models**: Humidity level predictions
- **Pressure Analysis**: Atmospheric pressure forecasting
- **Wind Speed**: Wind velocity predictions
- **Model Training**: Automated model retraining scripts

## 🧪 Testing

```bash
# Run all tests
python test_all_features.py

# Production testing
python test_production.py

# Specific test categories
python -m pytest backend/tests/
```

## 🚀 Deployment

### Production Setup
```bash
python deploy_production.py
```

### Manual Deployment
1. Set production environment variables
2. Install production requirements
3. Configure database and Redis
4. Setup Gunicorn and Nginx
5. Configure SSL certificates

## 📈 Performance Features

- **Caching**: Redis-based caching for weather data
- **Database Optimization**: Connection pooling and indexing
- **Static Files**: CDN-ready static file serving
- **API Rate Limiting**: Request throttling and monitoring

## 🔒 Security Features

- **HTTPS**: SSL/TLS encryption
- **Security Headers**: HSTS, XSS protection, CSRF
- **Authentication**: Secure user authentication
- **Input Validation**: Comprehensive data validation
- **SQL Injection Protection**: Parameterized queries

## 📱 Mobile & Responsive

- **Mobile First**: Responsive design for all devices
- **Touch Friendly**: Optimized for mobile interactions
- **Progressive Web App**: PWA capabilities
- **Cross Browser**: Compatible with all modern browsers

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Team

### **Project Lead & Backend Developer**
**Muhammad Zaheer Uddin**
- GitHub: [@zaheeruldin978](https://github.com/zaheeruldin978)
- Role: Backend Development, Django, Machine Learning, Database Design
- Project: Final Year Project - Weather247

### **Frontend Developer**
**Waqas Ahmad**
- GitHub: [@waqasbutt689](https://github.com/waqasbutt689)
- Role: Frontend Development, UI/UX Design, Responsive Templates
- Contribution: Complete frontend implementation, Tailwind CSS, JavaScript

## 🙏 Acknowledgments

- OpenWeatherMap for weather data API
- Django community for the excellent framework
- Tailwind CSS for the beautiful UI components
- Scikit-learn for machine learning capabilities

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Contact: zaheeruldin978@gmail.com

---

**Weather247** - Making weather forecasting accessible and intelligent! 🌤️✨

*Built with ❤️ by Muhammad Zaheer Ul Din Babar & Waqas Ahmad*
