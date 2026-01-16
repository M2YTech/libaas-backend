"""
Authentication utility functions.
"""

import bcrypt
import uuid
from datetime import datetime

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password: Plain text password
    
    Returns:
        Hashed password string
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password to compare against
    
    Returns:
        True if password matches, False otherwise
    """
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )

def generate_unique_filename(original_filename: str, user_email: str) -> str:
    """
    Generate a unique filename for image storage.
    
    Args:
        original_filename: Original name of the uploaded file
        user_email: User's email for uniqueness
    
    Returns:
        Unique filename string
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    extension = original_filename.split('.')[-1] if '.' in original_filename else 'jpg'
    safe_email = user_email.replace('@', '_').replace('.', '_')
    return f"{safe_email}_{timestamp}_{unique_id}.{extension}"

def validate_image_type(content_type: str) -> bool:
    """
    Validate if the file is an acceptable image type.
    
    Args:
        content_type: MIME type of the file
    
    Returns:
        True if valid image type, False otherwise
    """
    valid_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
    return content_type in valid_types













