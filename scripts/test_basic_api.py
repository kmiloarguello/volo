#!/usr/bin/env python3
"""
Simple API test to verify endpoints are working before running architecture tests
"""

import requests
import json
import os

API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000')

def test_api_health():
    """Test the health endpoint"""
    print("🔍 Testing API health...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            print("✅ API is healthy")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_basic_endpoints():
    """Test basic CRUD endpoints"""
    print("\n🔍 Testing basic endpoints...")
    
    # Test regions endpoint
    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/regions/")
        if response.status_code == 200:
            print("✅ Regions endpoint working")
            regions = response.json()
            print(f"   Found {len(regions)} existing regions")
        else:
            print(f"❌ Regions endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Regions endpoint error: {e}")
    
    # Test volunteers endpoint  
    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/volunteers/")
        if response.status_code == 200:
            print("✅ Volunteers endpoint working")
            data = response.json()
            print(f"   Found {data.get('total', 0)} existing volunteers")
        else:
            print(f"❌ Volunteers endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Volunteers endpoint error: {e}")

def test_create_region():
    """Test creating a region"""
    print("\n🔍 Testing region creation...")
    
    region_data = {
        "name": f"Test Region API {hash(abs(hash('test'))) % 10000}"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/api/v1/regions/", json=region_data)
        if response.status_code in [200, 201]:
            region = response.json()
            print("✅ Region created successfully")
            print(f"   ID: {region['id']}")
            print(f"   Name: {region['name']}")
            return region
        else:
            print(f"❌ Region creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Region creation error: {e}")
        return None

def main():
    """Main test function"""
    print("🚀 Running basic API tests...")
    print("=" * 50)
    
    # Test health
    if not test_api_health():
        print("❌ API is not healthy, stopping tests")
        return
    
    # Test endpoints
    test_basic_endpoints()
    
    # Test creation
    region = test_create_region()
    
    print("\n" + "=" * 50)
    if region:
        print("🎉 Basic API tests completed successfully!")
        print("✅ Ready to run architecture tests")
    else:
        print("⚠️ Some basic tests failed")
        print("⚠️ Check API before running architecture tests")

if __name__ == "__main__":
    main()