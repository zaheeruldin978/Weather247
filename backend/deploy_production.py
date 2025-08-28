#!/usr/bin/env python3
"""
Weather-247 Production Deployment Script
========================================

This script automates the production deployment process for Weather-247.
Run this script on your production server to deploy the application.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"\n🔄 {description}...")
    print(f"Running: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Error: {e.stderr}")
        return False

def check_prerequisites():
    """Check if all prerequisites are installed"""
    print("🔍 Checking prerequisites...")
    
    prerequisites = [
        ('python3', 'Python 3.8+'),
        ('pip3', 'Pip package manager'),
        ('postgres', 'PostgreSQL database'),
        ('redis-server', 'Redis server'),
        ('nginx', 'Nginx web server'),
    ]
    
    missing = []
    for cmd, name in prerequisites:
        if shutil.which(cmd) is None:
            missing.append(name)
    
    if missing:
        print(f"❌ Missing prerequisites: {', '.join(missing)}")
        print("Please install them before running this script.")
        return False
    
    print("✅ All prerequisites are installed")
    return True

def setup_environment():
    """Set up production environment"""
    print("\n🔧 Setting up production environment...")
    
    # Create logs directory
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    print("✅ Logs directory created")
    
    # Create media directory
    media_dir = Path("media")
    media_dir.mkdir(exist_ok=True)
    print("✅ Media directory created")
    
    # Set proper permissions
    os.chmod(logs_dir, 0o755)
    os.chmod(media_dir, 0o755)
    print("✅ Directory permissions set")
    
    return True

def install_dependencies():
    """Install production dependencies"""
    print("\n📦 Installing production dependencies...")
    
    if not run_command("pip3 install -r requirements.production.txt", "Installing Python packages"):
        return False
    
    return True

def setup_database():
    """Set up production database"""
    print("\n🗄️ Setting up production database...")
    
    # Create database user and database
    db_commands = [
        "sudo -u postgres createuser --interactive weather247_user",
        "sudo -u postgres createdb weather247_prod",
        "sudo -u postgres psql -c \"ALTER USER weather247_user WITH PASSWORD 'your-secure-password';\"",
        "sudo -u postgres psql -c \"GRANT ALL PRIVILEGES ON DATABASE weather247_prod TO weather247_user;\"",
    ]
    
    for cmd in db_commands:
        if not run_command(cmd, f"Database setup: {cmd}"):
            print("⚠️ Database setup command failed, you may need to run it manually")
    
    return True

def run_migrations():
    """Run database migrations"""
    print("\n🔄 Running database migrations...")
    
    if not run_command("python3 manage.py migrate", "Running migrations"):
        return False
    
    return True

def collect_static():
    """Collect static files"""
    print("\n📁 Collecting static files...")
    
    if not run_command("python3 manage.py collectstatic --noinput", "Collecting static files"):
        return False
    
    return True

def create_superuser():
    """Create superuser account"""
    print("\n👤 Creating superuser account...")
    
    print("Please create a superuser account:")
    if not run_command("python3 manage.py createsuperuser", "Creating superuser"):
        print("⚠️ Superuser creation failed, you can create it manually later")
    
    return True

def setup_services():
    """Set up system services"""
    print("\n🔧 Setting up system services...")
    
    # Create systemd service files
    gunicorn_service = """[Unit]
Description=Weather-247 Gunicorn
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/project
ExecStart=/usr/local/bin/gunicorn --workers 3 --bind unix:/tmp/weather247.sock weather247.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
"""
    
    celery_service = """[Unit]
Description=Weather-247 Celery
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/project
ExecStart=/usr/local/bin/celery -A weather247 worker --loglevel=info
Restart=always

[Install]
WantedBy=multi-user.target
"""
    
    # Write service files
    with open("/etc/systemd/system/weather247-gunicorn.service", "w") as f:
        f.write(gunicorn_service)
    
    with open("/etc/systemd/system/weather247-celery.service", "w") as f:
        f.write(celery_service)
    
    print("✅ Systemd service files created")
    
    # Reload systemd and enable services
    run_command("sudo systemctl daemon-reload", "Reloading systemd")
    run_command("sudo systemctl enable weather247-gunicorn", "Enabling Gunicorn service")
    run_command("sudo systemctl enable weather247-celery", "Enabling Celery service")
    
    return True

def configure_nginx():
    """Configure Nginx"""
    print("\n🌐 Configuring Nginx...")
    
    nginx_config = """server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    location / {
        proxy_pass http://unix:/tmp/weather247.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static/ {
        alias /path/to/your/project/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        alias /path/to/your/project/media/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
"""
    
    with open("/etc/nginx/sites-available/weather247", "w") as f:
        f.write(nginx_config)
    
    # Enable site and restart nginx
    run_command("sudo ln -s /etc/nginx/sites-available/weather247 /etc/nginx/sites-enabled/", "Enabling Nginx site")
    run_command("sudo nginx -t", "Testing Nginx configuration")
    run_command("sudo systemctl restart nginx", "Restarting Nginx")
    
    return True

def start_services():
    """Start all services"""
    print("\n🚀 Starting services...")
    
    services = [
        ("weather247-gunicorn", "Gunicorn web server"),
        ("weather247-celery", "Celery worker"),
        ("redis-server", "Redis server"),
        ("postgresql", "PostgreSQL database"),
    ]
    
    for service, description in services:
        run_command(f"sudo systemctl start {service}", f"Starting {description}")
    
    return True

def health_check():
    """Perform health check"""
    print("\n🏥 Performing health check...")
    
    # Wait a moment for services to start
    import time
    time.sleep(5)
    
    # Check if services are running
    services = [
        ("weather247-gunicorn", "Gunicorn"),
        ("weather247-celery", "Celery"),
        ("redis-server", "Redis"),
        ("postgresql", "PostgreSQL"),
    ]
    
    all_healthy = True
    for service, name in services:
        result = subprocess.run(f"sudo systemctl is-active {service}", shell=True, capture_output=True, text=True)
        if result.stdout.strip() == "active":
            print(f"✅ {name} is running")
        else:
            print(f"❌ {name} is not running")
            all_healthy = False
    
    return all_healthy

def main():
    """Main deployment function"""
    print("🚀 Weather-247 Production Deployment")
    print("=" * 50)
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites check failed. Please install missing components.")
        sys.exit(1)
    
    # Setup environment
    if not setup_environment():
        print("\n❌ Environment setup failed.")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Dependency installation failed.")
        sys.exit(1)
    
    # Setup database
    setup_database()
    
    # Run migrations
    if not run_migrations():
        print("\n❌ Database migration failed.")
        sys.exit(1)
    
    # Collect static files
    if not collect_static():
        print("\n❌ Static file collection failed.")
        sys.exit(1)
    
    # Create superuser
    create_superuser()
    
    # Setup services
    setup_services()
    
    # Configure Nginx
    configure_nginx()
    
    # Start services
    start_services()
    
    # Health check
    if health_check():
        print("\n🎉 Deployment completed successfully!")
        print("\nYour Weather-247 application is now running in production!")
        print("Access it at: http://yourdomain.com")
        print("\nNext steps:")
        print("1. Update your domain name in Nginx configuration")
        print("2. Set up SSL certificate with Let's Encrypt")
        print("3. Configure monitoring and alerts")
        print("4. Set up automated backups")
    else:
        print("\n⚠️ Deployment completed with some issues.")
        print("Please check the service status manually.")

if __name__ == "__main__":
    main()
