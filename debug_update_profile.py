import requests
import json

def test_update_profile():
    # Use local URL if running locally, otherwise use Railway URL
    # URL = "http://localhost:8000/auth/update-profile"
    URL = "https://web-production-9463.up.railway.app/auth/update-profile"
    
    # Use a real user ID from your database for testing
    # From the logs, I saw "Found 6 users". I'll use a dummy ID first to see the 404 behavior.
    
    test_user_id = "550e8400-e29b-41d4-a716-446655440000" # Dummy UUID
    
    data = {
        "user_id": test_user_id,
        "name": "Test User Improved",
        "gender": "male",
        "country": "Pakistan",
        "height": "175",
        "body_shape": "athletic",
        "skin_tone": "tan"
    }
    
    print(f"🚀 Testing Profile Update at {URL}...")
    try:
        response = requests.post(URL, data=data)
        print(f"Status Code: {response.status_code}")
        try:
            print("Response JSON:")
            print(json.dumps(response.json(), indent=2))
        except:
            print("Response Text:", response.text)
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    test_update_profile()
