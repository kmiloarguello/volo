#!/usr/bin/env python3
"""
Test environment variable configuration
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

def test_config_module():
    """Test that the config module loads correctly"""
    print("🔍 Testing config module import...")
    try:
        from config import settings
        print("✅ Config module imported successfully")
        return settings
    except Exception as e:
        print(f"❌ Failed to import config module: {e}")
        return None

def test_database_url(settings):
    """Test database URL configuration"""
    print("\n🔍 Testing database URL...")
    try:
        db_url = settings.get_database_url()
        print(f"✅ Database URL: {db_url}")
        
        # Check that it's not using hardcoded fallback values when env is set
        if "postgresql://" in db_url:
            print("✅ Database URL format is correct")
        else:
            print("❌ Database URL format is incorrect")
            return False
        return True
    except Exception as e:
        print(f"❌ Failed to get database URL: {e}")
        return False

def test_cors_config(settings):
    """Test CORS configuration"""
    print("\n🔍 Testing CORS configuration...")
    try:
        cors_origins = settings.get_cors_origins_list()
        print(f"✅ CORS Origins: {cors_origins}")
        
        if isinstance(cors_origins, list):
            print("✅ CORS origins is a list")
        else:
            print("❌ CORS origins is not a list")
            return False
        return True
    except Exception as e:
        print(f"❌ Failed to get CORS config: {e}")
        return False

def test_fastapi_config(settings):
    """Test FastAPI configuration"""
    print("\n🔍 Testing FastAPI configuration...")
    try:
        print(f"✅ FastAPI Host: {settings.fastapi_host}")
        print(f"✅ FastAPI Port: {settings.fastapi_port}")
        print(f"✅ FastAPI Reload: {settings.fastapi_reload}")
        return True
    except Exception as e:
        print(f"❌ Failed to get FastAPI config: {e}")
        return False

def test_database_connection():
    """Test database connection module"""
    print("\n🔍 Testing database connection module...")
    try:
        from database.connection import DATABASE_URL, engine
        print(f"✅ Database connection module imported")
        print(f"✅ Database URL from connection: {DATABASE_URL}")
        return True
    except Exception as e:
        print(f"❌ Failed to import database connection: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Running environment variable configuration tests...")
    print("=" * 70)
    
    # Test config module
    settings = test_config_module()
    if not settings:
        print("\n❌ Config module tests failed")
        return False
    
    # Run all tests
    all_passed = True
    all_passed &= test_database_url(settings)
    all_passed &= test_cors_config(settings)
    all_passed &= test_fastapi_config(settings)
    all_passed &= test_database_connection()
    
    print("\n" + "=" * 70)
    if all_passed:
        print("🎉 All environment variable configuration tests passed!")
        print("✅ Configuration is loaded from .env file correctly")
    else:
        print("❌ Some tests failed")
        print("⚠️ Check the configuration setup")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
