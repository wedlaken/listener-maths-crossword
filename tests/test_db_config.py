#!/usr/bin/env python3
"""
Test database configuration
"""

import os
from app import app, db

def test_database_config():
    """Test the database configuration"""
    
    print("🧪 TESTING DATABASE CONFIGURATION")
    print("=" * 40)
    
    # Check current database URL
    database_url = app.config['SQLALCHEMY_DATABASE_URI']
    print(f"Database URL: {database_url}")
    
    # Test database connection
    try:
        with app.app_context():
            # Test if we can connect
            with db.engine.connect() as conn:
                result = conn.execute("SELECT 1")
                print("✅ Database connection successful!")
                
                # Test if tables exist
                result = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = [row[0] for row in result]
                print(f"✅ Tables found: {tables}")
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")

if __name__ == "__main__":
    test_database_config() 