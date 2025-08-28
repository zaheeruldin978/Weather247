/**
 * Weather-247 - Professional Weather Insights
 * Main JavaScript functionality for weather application
 */

// Global weather utilities
const WeatherUtils = {
    // Format temperature with proper units
    formatTemperature: (temp, unit = 'C') => {
        if (temp === null || temp === undefined) return '--';
        return `${Math.round(temp)}°${unit}`;
    },

    // Format humidity percentage
    formatHumidity: (humidity) => {
        if (humidity === null || humidity === undefined) return '--';
        return `${humidity}%`;
    },

    // Format wind speed with units
    formatWindSpeed: (speed, unit = 'm/s') => {
        if (speed === null || speed === undefined) return '--';
        return `${speed} ${unit}`;
    },

    // Format pressure
    formatPressure: (pressure, unit = 'hPa') => {
        if (pressure === null || pressure === undefined) return '--';
        return `${pressure} ${unit}`;
    },

    // Get AQI level description
    getAQILevel: (aqi) => {
        if (aqi <= 50) return { level: 'Good', color: 'green', description: 'Air quality is satisfactory' };
        if (aqi <= 100) return { level: 'Moderate', color: 'yellow', description: 'Air quality is acceptable' };
        if (aqi <= 150) return { level: 'Unhealthy for Sensitive Groups', color: 'orange', description: 'Some pollutants may affect sensitive individuals' };
        if (aqi <= 200) return { level: 'Unhealthy', color: 'red', description: 'Everyone may begin to experience health effects' };
        if (aqi <= 300) return { level: 'Very Unhealthy', color: 'purple', description: 'Health warnings of emergency conditions' };
        return { level: 'Hazardous', color: 'maroon', description: 'Health alert: everyone may experience more serious health effects' };
    },

    // Get weather icon based on OpenWeather icon code
    getWeatherIcon: (iconCode) => {
        const iconMap = {
            '01d': '☀️', // clear sky day
            '01n': '🌙', // clear sky night
            '02d': '⛅', // few clouds day
            '02n': '☁️', // few clouds night
            '03d': '☁️', // scattered clouds
            '03n': '☁️', // scattered clouds
            '04d': '☁️', // broken clouds
            '04n': '☁️', // broken clouds
            '09d': '🌧️', // shower rain
            '09n': '🌧️', // shower rain
            '10d': '🌦️', // rain day
            '10n': '🌧️', // rain night
            '11d': '⛈️', // thunderstorm
            '11n': '⛈️', // thunderstorm
            '13d': '🌨️', // snow
            '13n': '🌨️', // snow
            '50d': '🌫️', // mist
            '50n': '🌫️', // mist
        };
        return iconMap[iconCode] || '🌤️';
    },

    // Get weather description
    getWeatherDescription: (description) => {
        return description.charAt(0).toUpperCase() + description.slice(1);
    },

    // Format timestamp
    formatTimestamp: (timestamp) => {
        if (!timestamp) return '--';
        const date = new Date(timestamp);
        return date.toLocaleString();
    },

    // Calculate wind direction
    getWindDirection: (degrees) => {
        const directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW'];
        const index = Math.round(degrees / 22.5) % 16;
        return directions[index];
    },

    // Convert Celsius to Fahrenheit
    celsiusToFahrenheit: (celsius) => {
        return (celsius * 9/5) + 32;
    },

    // Convert Fahrenheit to Celsius
    fahrenheitToCelsius: (fahrenheit) => {
        return (fahrenheit - 32) * 5/9;
    },

    // Convert m/s to mph
    msToMph: (ms) => {
        return ms * 2.237;
    },

    // Convert m/s to km/h
    msToKmh: (ms) => {
        return ms * 3.6;
    }
};

// Weather API service
const WeatherAPI = {
    baseURL: '/api',

    // Get current weather for a city
    async getCurrentWeather(city, country = null) {
        try {
            const params = new URLSearchParams({ city });
            if (country) params.append('country', country);
            
            const response = await fetch(`${this.baseURL}/current-weather/?${params}`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            
            return await response.json();
        } catch (error) {
            console.error('Error fetching current weather:', error);
            throw error;
        }
    },

    // Get weather forecast for a city
    async getForecast(city, days = 5) {
        try {
            const params = new URLSearchParams({ city, days });
            const response = await fetch(`${this.baseURL}/weather-forecast/?${params}`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            
            return await response.json();
        } catch (error) {
            console.error('Error fetching forecast:', error);
            throw error;
        }
    },

    // Get historical weather data
    async getHistoricalWeather(city, startDate, endDate) {
        try {
            const params = new URLSearchParams({ city });
            if (startDate) params.append('start_date', startDate);
            if (endDate) params.append('end_date', endDate);
            
            const response = await fetch(`${this.baseURL}/historical-weather/?${params}`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            
            return await response.json();
        } catch (error) {
            console.error('Error fetching historical weather:', error);
            throw error;
        }
    },

    // Get weather alerts for a city
    async getAlerts(city) {
        try {
            const params = new URLSearchParams({ city });
            const response = await fetch(`${this.baseURL}/weather-alerts/?${params}`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            
            return await response.json();
        } catch (error) {
            console.error('Error fetching alerts:', error);
            throw error;
        }
    },

    // Compare multiple cities
    async compareCities(cities) {
        try {
            const citiesStr = cities.join(',');
            const response = await fetch(`${this.baseURL}/compare-cities/?cities=${citiesStr}`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            
            return await response.json();
        } catch (error) {
            console.error('Error comparing cities:', error);
            throw error;
        }
    },

    // Get air quality data
    async getAirQuality(city, country = null) {
        try {
            const params = new URLSearchParams({ city });
            if (country) params.append('country', country);
            
            const response = await fetch(`${this.baseURL}/air-quality/?${params}`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            
            return await response.json();
        } catch (error) {
            console.error('Error fetching air quality:', error);
            throw error;
        }
    },

    // Search for cities
    async searchCity(query) {
        try {
            const response = await fetch(`${this.baseURL}/search-city/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query })
            });
            
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            
            return await response.json();
        } catch (error) {
            console.error('Error searching city:', error);
            throw error;
        }
    }
};

// Chart utilities
const ChartUtils = {
    // Create temperature chart
    createTemperatureChart(ctx, data, options = {}) {
        const defaultOptions = {
                responsive: true,
            maintainAspectRatio: false,
                plugins: {
                legend: { display: false },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: '#3b82f6',
                    borderWidth: 1
                    }
                },
                scales: {
                    y: {
                    beginAtZero: false,
                    grid: { color: 'rgba(0, 0, 0, 0.1)' },
                    ticks: { color: '#6b7280' }
                },
                x: {
                    grid: { color: 'rgba(0, 0, 0, 0.1)' },
                    ticks: { color: '#6b7280' }
                }
            },
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
            }
        };

        return new Chart(ctx, {
            type: 'line',
            data: data,
            options: { ...defaultOptions, ...options }
        });
    },

    // Create comparison chart
    createComparisonChart(ctx, data, options = {}) {
        const defaultOptions = {
                responsive: true,
            maintainAspectRatio: false,
                plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: '#3b82f6',
                    borderWidth: 1
                    }
                },
                scales: {
                    y: {
                    beginAtZero: false,
                    grid: { color: 'rgba(0, 0, 0, 0.1)' },
                    ticks: { color: '#6b7280' }
                },
                x: {
                    grid: { color: 'rgba(0, 0, 0, 0.1)' },
                    ticks: { color: '#6b7280' }
                }
            }
        };

        return new Chart(ctx, {
            type: 'bar',
            data: data,
            options: { ...defaultOptions, ...options }
        });
    },

    // Create gauge chart for AQI
    createAQIGauge(ctx, value, maxValue = 500) {
        const percentage = (value / maxValue) * 100;
        const angle = (percentage / 100) * Math.PI;
        
        ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
        
        const centerX = ctx.canvas.width / 2;
        const centerY = ctx.canvas.height / 2;
        const radius = Math.min(centerX, centerY) - 20;
        
        // Draw background arc
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, 0, Math.PI);
        ctx.strokeStyle = '#e5e7eb';
        ctx.lineWidth = 20;
        ctx.stroke();
        
        // Draw value arc
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, -Math.PI/2, -Math.PI/2 + angle);
        ctx.strokeStyle = this.getAQIColor(value);
        ctx.lineWidth = 20;
        ctx.stroke();
        
        // Draw value text
        ctx.fillStyle = '#1f2937';
        ctx.font = 'bold 24px Inter';
        ctx.textAlign = 'center';
        ctx.fillText(value.toString(), centerX, centerY + 10);
        
        // Draw label
        ctx.fillStyle = '#6b7280';
        ctx.font = '14px Inter';
        ctx.fillText('AQI', centerX, centerY + 40);
    },

    // Get AQI color
    getAQIColor(aqi) {
        if (aqi <= 50) return '#10b981';
        if (aqi <= 100) return '#f59e0b';
        if (aqi <= 150) return '#f97316';
        if (aqi <= 200) return '#ef4444';
        if (aqi <= 300) return '#8b5cf6';
        return '#7c2d12';
    }
};

// UI utilities
const UIUtils = {
    // Show loading spinner
    showLoading(element, text = 'Loading...') {
        element.innerHTML = `
            <div class="flex items-center justify-center p-8">
                <svg class="animate-spin h-8 w-8 text-blue-600 mr-3" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span class="text-gray-600">${text}</span>
            </div>
        `;
    },

    // Show error message
    showError(element, message) {
        element.innerHTML = `
            <div class="flex items-center justify-center p-8 text-red-600">
                <svg class="w-8 h-8 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
                </svg>
                <span>${message}</span>
            </div>
        `;
    },

    // Show success message
    showSuccess(element, message) {
        element.innerHTML = `
            <div class="flex items-center justify-center p-8 text-green-600">
                <svg class="w-8 h-8 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <span>${message}</span>
            </div>
        `;
    },

    // Create toast notification
    showToast(message, type = 'info', duration = 3000) {
        const toast = document.createElement('div');
        const colors = {
            info: 'bg-blue-500',
            success: 'bg-green-500',
            warning: 'bg-yellow-500',
            error: 'bg-red-500'
        };
        
        toast.className = `fixed top-4 right-4 ${colors[type]} text-white px-6 py-3 rounded-lg shadow-lg z-50 transform transition-all duration-300 translate-x-full`;
        toast.textContent = message;
        
        document.body.appendChild(toast);
        
        // Animate in
        setTimeout(() => toast.classList.remove('translate-x-full'), 100);
        
        // Auto remove
        setTimeout(() => {
            toast.classList.add('translate-x-full');
            setTimeout(() => document.body.removeChild(toast), 300);
        }, duration);
    },

    // Debounce function
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    // Throttle function
    throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
};

// Local storage utilities
const StorageUtils = {
    // Save to local storage
    save(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch (error) {
            console.error('Error saving to localStorage:', error);
        }
    },

    // Load from local storage
    load(key, defaultValue = null) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : defaultValue;
        } catch (error) {
            console.error('Error loading from localStorage:', error);
            return defaultValue;
        }
    },

    // Remove from local storage
    remove(key) {
        try {
            localStorage.removeItem(key);
        } catch (error) {
            console.error('Error removing from localStorage:', error);
        }
    },

    // Clear all local storage
    clear() {
        try {
            localStorage.clear();
        } catch (error) {
            console.error('Error clearing localStorage:', error);
        }
    }
};

// Weather data cache
const WeatherCache = {
    cache: new Map(),
    maxAge: 10 * 60 * 1000, // 10 minutes

    // Get cached weather data
    get(key) {
        const item = this.cache.get(key);
        if (!item) return null;
        
        if (Date.now() - item.timestamp > this.maxAge) {
            this.cache.delete(key);
            return null;
        }
        
        return item.data;
    },

    // Set cached weather data
    set(key, data) {
        this.cache.set(key, {
            data,
            timestamp: Date.now()
        });
    },

    // Clear expired cache
    clearExpired() {
        const now = Date.now();
        for (const [key, item] of this.cache.entries()) {
            if (now - item.timestamp > this.maxAge) {
                this.cache.delete(key);
            }
        }
    },

    // Clear all cache
    clear() {
        this.cache.clear();
    }
};

// Initialize weather application
document.addEventListener('DOMContentLoaded', function() {
    console.log('Weather-247 Application Initialized');
    
    // Clear expired cache every 5 minutes
    setInterval(() => WeatherCache.clearExpired(), 5 * 60 * 1000);
    
    // Initialize any global event listeners
    initializeGlobalListeners();
});

// Initialize global event listeners
function initializeGlobalListeners() {
    // Handle theme switching if implemented
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            document.documentElement.classList.toggle('dark');
            const isDark = document.documentElement.classList.contains('dark');
            StorageUtils.save('theme', isDark ? 'dark' : 'light');
        });
    }
    
    // Handle search functionality
    const searchInput = document.getElementById('city-search');
    if (searchInput) {
        const debouncedSearch = UIUtils.debounce(async (query) => {
            if (query.length < 2) return;
            
            try {
                const results = await WeatherAPI.searchCity(query);
                // Handle search results
                console.log('Search results:', results);
            } catch (error) {
                console.error('Search error:', error);
            }
        }, 300);
        
        searchInput.addEventListener('input', (e) => debouncedSearch(e.target.value));
    }
}

// Export utilities for global use
window.WeatherUtils = WeatherUtils;
window.WeatherAPI = WeatherAPI;
window.ChartUtils = ChartUtils;
window.UIUtils = UIUtils;
window.StorageUtils = StorageUtils;
window.WeatherCache = WeatherCache;

