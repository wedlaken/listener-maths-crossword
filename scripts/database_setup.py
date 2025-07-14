#!/usr/bin/env python3
"""
Database configuration helper for development vs production
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def setup_database_config():
    """Setup database configuration based on environment"""
    
    print("🔧 DATABASE CONFIGURATION SETUP")
    print("=" * 50)
    
    # Check current environment
    environment = os.environ.get('FLASK_ENV', 'development')
    print(f"Current environment: {environment}")
    
    if environment == 'production':
        # Production: Use PostgreSQL from environment variable
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            print("❌ ERROR: DATABASE_URL environment variable not set for production")
            print("Please set DATABASE_URL to your PostgreSQL connection string")
            return None
        
        print(f"✅ Using PostgreSQL: {database_url}")
        return database_url
    
    else:
        # Development: Use SQLite
        database_url = 'sqlite:///crossword_solver.db'
        print(f"✅ Using SQLite: {database_url}")
        print("📁 Database file: instance/crossword_solver.db")
        return database_url

def create_app_with_database():
    """Create Flask app with appropriate database configuration"""
    
    app = Flask(__name__)
    
    # Get database URL
    database_url = setup_database_config()
    if not database_url:
        return None
    
    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    db = SQLAlchemy(app)
    
    return app, db

def show_database_options():
    """Show different database options for the project"""
    
    print("\n📋 DATABASE OPTIONS FOR YOUR PROJECT")
    print("=" * 50)
    
    print("\n1️⃣  LOCAL DEVELOPMENT (Current)")
    print("   Database: SQLite")
    print("   Location: instance/crossword_solver.db")
    print("   Pros: Simple, no setup, works offline")
    print("   Cons: Separate per machine, no sharing")
    print("   Command: python app.py")
    
    print("\n2️⃣  SHARED DEVELOPMENT (Recommended)")
    print("   Database: PostgreSQL on Railway/Supabase")
    print("   Cost: Free tier")
    print("   Pros: Shared between machines, real production-like")
    print("   Cons: Requires internet, slight setup")
    print("   Command: FLASK_ENV=production python app.py")
    
    print("\n3️⃣  PRODUCTION DEPLOYMENT")
    print("   Database: PostgreSQL on Heroku/Railway")
    print("   Cost: $5-10/month")
    print("   Pros: Full production environment")
    print("   Cons: Requires payment, more complex")
    
    print("\n🚀 QUICK SETUP FOR SHARED DEVELOPMENT:")
    print("1. Sign up for Railway (railway.app) - Free")
    print("2. Create PostgreSQL database")
    print("3. Copy connection string")
    print("4. Set environment variable: export DATABASE_URL='your_connection_string'")
    print("5. Run: FLASK_ENV=production python app.py")

if __name__ == "__main__":
    show_database_options() 