import os
import json
from supabase import create_client
from pathlib import Path

# Hardcoded for reliability during debug
url = "https://qsvvjrlmcguanqnewayh.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFzdnZqcmxtY2d1YW5xbmV3YXloIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NDkwMTUxMSwiZXhwIjoyMDgwNDc3NTExfQ.E09EiKATP3-N6edCnnM0LF0NwHgRordgOYydMDD0Zj4"

supabase = create_client(url, key)

def get_real_id():
    res = supabase.table("users").select("id").limit(1).execute()
    if res.data:
        return res.data[0]["id"]
    return None

def test_manual_update(user_id):
    print(f"Testing update for user: {user_id}")
    updates = {"name": "Debug Updated Name"}
    try:
        res = supabase.table("users").update(updates).eq("id", user_id).execute()
        print("Update result:", res.data)
    except Exception as e:
        print(f"Update failed: {e}")

if __name__ == "__main__":
    uid = get_real_id()
    if uid:
        test_manual_update(uid)
    else:
        print("No users found to test.")
