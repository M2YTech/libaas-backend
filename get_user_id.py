import os
import json
from supabase import create_client
from pathlib import Path

env_path = Path(r"c:\Users\Lenovo\Desktop\Libaas AI Backend\backend\.env")

env_vars = {}
with open(env_path, 'r', encoding='utf-8') as f:
    for line in f:
        if '=' in line and not line.startswith('#'):
            key, val = line.strip().split('=', 1)
            env_vars[key] = val

url = env_vars.get("SUPABASE_URL")
key = env_vars.get("SUPABASE_SERVICE_ROLE_KEY") or env_vars.get("SUPABASE_KEY")

print(f"Parsed URL: {url}")
print(f"Parsed Key length: {len(key) if key else 0}")

if not url or not key:
    print("Error: Missing SUPABASE_URL or SUPABASE_KEY")
    exit(1)

supabase = create_client(url, key)

def get_a_user():
    try:
        res = supabase.table("users").select("id, name, email").limit(1).execute()
        if res.data:
            print("Found User:", json.dumps(res.data[0], indent=2))
        else:
            print("No users found.")
    except Exception as e:
        print(f"Database error: {e}")

if __name__ == "__main__":
    get_a_user()
