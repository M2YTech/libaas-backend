import os
from pathlib import Path
from supabase import create_client, Client
from dotenv import load_dotenv
import time
import asyncio

# Load .env from the backend directory
backend_dir = Path(__file__).resolve().parent.parent.parent
env_path = backend_dir / ".env"
load_dotenv(env_path)

# supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
_supabase_client = None

def get_supabase_client() -> Client:
    """Get or initialize Supabase client instance."""
    global _supabase_client
    if _supabase_client is None:
        url = os.getenv("SUPABASE_URL", "https://qsvvjrlmcguanqnewayh.supabase.co")
        key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY")
        if not key:
            print("⚠️ Warning: SUPABASE_KEY is missing. Database operations will fail.")
            # We don't raise here to allow the app to boot/build even without keys
            return None 
        _supabase_client = create_client(url, key)
    return _supabase_client

async def upload_image_to_storage(file_bytes: bytes, filename: str, content_type: str) -> str:
    """
    Upload image to Supabase Storage and return public URL with retry logic.
    
    Args:
        file_bytes: Image file bytes
        filename: Unique filename for storage
        content_type: MIME type of the file
    
    Returns:
        Public URL of the uploaded image
    """
    max_retries = 3
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            # Upload to Supabase Storage
            supabase = get_supabase_client()
            if not supabase:
                raise ValueError("Supabase client not initialized")
            response = supabase.storage.from_("profile_images").upload(
                path=filename,
                file=file_bytes,
                file_options={"content-type": content_type}
            )
            
            # Get public URL
            supabase = get_supabase_client()
            public_url = supabase.storage.from_("profile_images").get_public_url(filename)
            
            if attempt > 0:
                print(f"✅ Upload succeeded on retry {attempt}")
            
            return public_url
            
        except Exception as e:
            error_msg = str(e)
            print(f"Upload attempt {attempt + 1}/{max_retries} failed: {error_msg}")
            
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                print(f"❌ All upload attempts failed for {filename}")
                raise e

async def create_user(user_data: dict) -> dict:
    """
    Create a new user in the users table.
    
    Args:
        user_data: Dictionary containing user information
    
    Returns:
        Created user record
    """
    try:
        supabase = get_supabase_client()
        if not supabase:
            raise ValueError("Supabase client not initialized")
        response = supabase.table("users").insert(user_data).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error creating user: {e}")
        raise e

async def get_user_by_email(email: str) -> dict | None:
    """
    Get user by email address.
    
    Args:
        email: User's email address
    
    Returns:
        User record or None if not found
    """
    try:
        supabase = get_supabase_client()
        if not supabase:
            return None
        response = supabase.table("users").select("*").eq("email", email).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error fetching user: {e}")
        raise e

async def get_user_by_id(user_id: str) -> dict | None:
    """
    Get user by ID.
    
    Args:
        user_id: User's UUID
    
    Returns:
        User record or None if not found
    """
    try:
        supabase = get_supabase_client()
        if not supabase:
            return None
        response = supabase.table("users").select("*").eq("id", user_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error fetching user: {e}")
        raise e

# ====================================
# Wardrobe Database Operations
# ====================================

async def upload_wardrobe_image(file_bytes: bytes, filename: str, content_type: str) -> str:
    """
    Upload wardrobe item image to Supabase Storage with retry logic.
    
    Args:
        file_bytes: Image file bytes
        filename: Unique filename for storage
        content_type: MIME type of the file
    
    Returns:
        Public URL of the uploaded image
    """
    max_retries = 3
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            # Upload to Supabase Storage (wardrobe_images bucket)
            supabase = get_supabase_client()
            if not supabase:
                raise ValueError("Supabase client not initialized")
            response = supabase.storage.from_("wardrobe_images").upload(
                path=filename,
                file=file_bytes,
                file_options={"content-type": content_type}
            )
            
            # Get public URL
            public_url = supabase.storage.from_("wardrobe_images").get_public_url(filename)
            
            if attempt > 0:
                print(f"✅ Upload succeeded on retry {attempt}")
            
            return public_url
            
        except Exception as e:
            error_msg = str(e)
            print(f"Upload attempt {attempt + 1}/{max_retries} failed: {error_msg}")
            
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                print(f"❌ All upload attempts failed for {filename}")
                raise e

async def upload_tryon_image(file_bytes: bytes, filename: str, content_type: str = "image/jpeg") -> str:
    """
    Upload virtual try-on image to Supabase Storage with retry logic.
    
    Args:
        file_bytes: Image file bytes
        filename: Unique filename for storage
        content_type: MIME type of the file
    
    Returns:
        Public URL of the uploaded image
    """
    max_retries = 3
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            # Upload to Supabase Storage (tryon_images bucket)
            response = supabase.storage.from_("tryon_images").upload(
                path=filename,
                file=file_bytes,
                file_options={"content-type": content_type}
            )
            
            # Get public URL
            public_url = supabase.storage.from_("tryon_images").get_public_url(filename)
            
            if attempt > 0:
                print(f"✅ Try-on image upload succeeded on retry {attempt}")
            
            return public_url
            
        except Exception as e:
            error_msg = str(e)
            print(f"Try-on upload attempt {attempt + 1}/{max_retries} failed: {error_msg}")
            
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                print(f"❌ All try-on upload attempts failed for {filename}")
                raise e


async def create_wardrobe_item(item_data: dict) -> dict:
    """
    Create a new wardrobe item in the database.
    
    Args:
        item_data: Dictionary containing wardrobe item information
    
    Returns:
        Created wardrobe item record
    """
    try:
        supabase = get_supabase_client()
        if not supabase:
            raise ValueError("Supabase client not initialized")
        response = supabase.table("wardrobe_items").insert(item_data).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error creating wardrobe item: {e}")
        raise e

async def get_user_wardrobe(user_id: str) -> list:
    """
    Get all wardrobe items for a user.
    
    Args:
        user_id: User's UUID
    
    Returns:
        List of wardrobe items
    """
    try:
        response = supabase.table("wardrobe_items").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching wardrobe: {e}")
        raise e

async def delete_wardrobe_item(item_id: str, user_id: str) -> bool:
    """
    Delete a wardrobe item.
    
    Args:
        item_id: Item's UUID
        user_id: User's UUID (for verification)
    
    Returns:
        True if deleted successfully
    """
    try:
        response = supabase.table("wardrobe_items").delete().eq("id", item_id).eq("user_id", user_id).execute()
        return True
    except Exception as e:
        print(f"Error deleting wardrobe item: {e}")
        raise e

async def update_wardrobe_item(item_id: str, user_id: str, updates: dict) -> dict:
    """
    Update a wardrobe item.
    
    Args:
        item_id: Item's UUID
        user_id: User's UUID (for verification)
        updates: Dictionary of fields to update
    
    Returns:
        Updated wardrobe item
    """
    try:
        supabase = get_supabase_client()
        if not supabase:
            return None
        response = supabase.table("wardrobe_items").update(updates).eq("id", item_id).eq("user_id", user_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error updating wardrobe item: {e}")
        raise e

