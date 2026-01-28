import requests
import json

def test_live_update():
    # URL = "http://localhost:8000/auth/update-profile"
    URL = "https://web-production-9463.up.railway.app/auth/update-profile"
    
    # Using the real user ID found in earlier debug logs
    real_user_id = "41f66d47-33fb-41f3-9ae4-7ff59cabdb00"
    
    data = {
        "user_id": real_user_id,
        "name": "Hussein Debug Test",
        "gender": "male",
        "country": "Pakistan",
        "height": "5,8",
        "body_shape": "rectangle",
        "skin_tone": "fair"
    }
    
    print(f"Testing Profile Update at {URL}...")
    try:
        # Use data= for multipart/form-data (matching frontend FormData)
        response = requests.post(URL, data=data) 
        print(f"Status Code: {response.status_code}")
        print("Response JSON:")
        print(json.dumps(response.json(), indent=2))
            
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_live_update()
