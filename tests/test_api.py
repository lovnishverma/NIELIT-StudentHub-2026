import os
import requests
import sys
import json

# Retrieve the URL from the environment (same secret we used for deploy)
API_URL = os.environ.get("APP_SHEET_URL")

if not API_URL:
    print("Error: APP_SHEET_URL is missing.")
    sys.exit(1)

def test_endpoint():
    print(f"Testing API Connection...")
    
    # Test the 'getStats' action which is read-only and fast
    try:
        response = requests.get(f"{API_URL}?action=getStats", timeout=15, allow_redirects=True)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                print("API responded with success.")
                print(f"Stats received: {data.get('data')}")
                return True
            else:
                print(f"API Logic Error: {data}")
        else:
            print(f"HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"Connection Failed: {str(e)}")
        
    return False

if __name__ == "__main__":
    if test_endpoint():
        print("\n SMOKE TEST PASSED")
        sys.exit(0)
    else:
        print("\n TEST FAILED")
        sys.exit(1)
