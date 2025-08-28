# Weather-247 Frontend

This directory contains the frontend templates and static assets for the Weather-247 application.

## Structure

- `templates/` - Django HTML templates
  - `base.html` - Base template with common layout and styling
  - `weather_dashboard/` - Weather dashboard specific templates
    - `home.html` - Landing page
    - `dashboard.html` - Main dashboard
    - `compare.html` - City comparison
    - `forecast.html` - AI weather forecast
    - `alerts.html` - Weather alerts
    - `route.html` - Route planning
    - `profile.html` - User profile

## Technologies Used

- **Bootstrap 5** - CSS framework for responsive design
- **Bootstrap Icons** - Icon library
- **Chart.js** - Interactive charts and graphs
- **Plotly.js** - Advanced data visualization
- **Leaflet.js** - Interactive maps
- **Custom CSS** - Modern styling and animations

## Features

- Responsive design that works on all devices
- Interactive weather charts and graphs
- Real-time data updates
- Modern UI with smooth animations
- User-friendly navigation
- Beautiful weather icons and visualizations

## Running the Frontend

The frontend is served by the Django backend. To run the complete application:

1. Navigate to the backend directory
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Start the server: `python manage.py runserver`
5. Open your browser and go to `http://127.0.0.1:8000`



