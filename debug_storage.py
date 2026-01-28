import os
from supabase import create_client

# Manual parse of .env to handle any encoding issues
env_vars = {}
try:
    with open(".env", "r", encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                env_vars[k.strip()] = v.strip()
except Exception as e:
    print(f"Error reading .env: {e}")

url = env_vars.get("SUPABASE_URL")
# Prefer service role key for storage operations
key = env_vars.get("SUPABASE_SERVICE_ROLE_KEY") or env_vars.get("SUPABASE_KEY")

print(f"--- Supabase Debugger ---")
print(f"URL: {url}")
print(f"Using Key (first 20 chars): {key[:20] if key else 'None'}")

if not url or not key:
    print("Error: Missing SUPABASE_URL or KEY in .env")
    exit(1)

try:
    supabase = create_client(url, key)
    
    # 1. Test Connection
    print("\n[1/3] Testing Connection...")
    res = supabase.table("users").select("count", count="exact").limit(1).execute()
    print(f"Success! Status code: 200. Found {res.count} users.")

    # 2. Check Storage Buckets
    print("\n[2/3] Checking Storage Buckets...")
    try:
        buckets = supabase.storage.list_buckets()
        bucket_names = [b.name for b in buckets]
        print(f"Existing buckets: {bucket_names}")
        
        required = ["profile_images", "wardrobe_images", "tryon_images"]
        for b in required:
            if b in bucket_names:
                print(f"Bucket '{b}': Found")
            else:
                print(f"Bucket '{b}': MISSING")
    except Exception as e:
        print(f"Failed to list buckets: {e}")
        print("NOTE: Listing buckets usually requires the 'service_role' key.")

    # 3. Test Upload
    print("\n[3/3] Testing Upload to 'profile_images'...")
    try:
        test_file = b"debug test"
        supabase.storage.from_("profile_images").upload(
            path="debug_test.txt",
            file=test_file,
            file_options={"upsert": "true", "content-type": "text/plain"}
        )
        print("Upload test: SUCCESS!")
        supabase.storage.from_("profile_images").remove(["debug_test.txt"])
    except Exception as e:
        print(f"Upload test: FAILED")
        print(f"Error: {e}")

except Exception as e:
    print(f"\nFATAL ERROR: {e}")
