#!/usr/bin/env python
"""
PostgreSQL Setup Script for Weather-247
This script helps set up PostgreSQL database and migrate data from SQLite.
"""

import os
import sys
import subprocess
import psycopg2
from psycopg2 import sql

def check_postgresql_installed():
    """Check if PostgreSQL is installed and accessible"""
    try:
        # Try to connect to PostgreSQL
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            user="postgres",
            password="124421weather247",
            database="postgres"
        )
        conn.close()
        print("✅ PostgreSQL is accessible!")
        return True
    except psycopg2.OperationalError as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        return False
    except ImportError:
        print("❌ psycopg2 not installed. Run: pip install psycopg2-binary")
        return False

def create_database():
    """Create the weather247_db database"""
    try:
        # Connect to default postgres database
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            user="postgres",
            password="124421weather247",
            database="postgres"
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'weather247_db'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier("weather247_db")))
            print("✅ Database 'weather247_db' created successfully!")
        else:
            print("✅ Database 'weather247_db' already exists!")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False

def setup_postgresql():
    """Main setup function"""
    print("🚀 Setting up PostgreSQL for Weather-247...")
    print("=" * 50)
    
    # Check if PostgreSQL is accessible
    if not check_postgresql_installed():
        print("\n📋 To install PostgreSQL on Windows:")
        print("1. Download from: https://www.postgresql.org/download/windows/")
        print("2. Install with default settings")
        print("3. Remember the password you set for 'postgres' user")
        print("4. Update the password in settings.py if different")
        return False
    
    # Create database
    if not create_database():
        return False
    
    print("\n✅ PostgreSQL setup completed!")
    print("\n📋 Next steps:")
    print("1. Run: python manage.py makemigrations")
    print("2. Run: python manage.py migrate")
    print("3. Run: python populate_database.py")
    print("\n🔗 Your database will now use PostgreSQL instead of SQLite!")
    
    return True

if __name__ == '__main__':
    setup_postgresql()

