
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://api.openai.com/v1/responses"
api_key = os.getenv("OPENAI_API_KEY")

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

payload = {
    "model": "gpt-5-nano",
    "input": "write a haiku about ai",
    "store": True
}

try:
    print(f"Sending request to {url}...")
    response = requests.post(url, headers=headers, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
