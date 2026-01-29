"""
Authentication routes for signup and login.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import Optional
import json

from app.core.database import create_user, get_user_by_email, upload_image_to_storage
from app.schemas import SignupResponse, LoginRequest, LoginResponse, ClipInsights
from app.components.auth.utils import hash_password, verify_password, generate_unique_filename, validate_image_type
from app.components.ai.clip_insights import analyze_image

router = APIRouter()

@router.post("/signup", response_model=SignupResponse)
async def signup(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    gender: str = Form(...),
    height: Optional[str] = Form(None),
    country: Optional[str] = Form(None),
    body_shape: Optional[str] = Form(None),
    skin_tone: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None)
):
    """
    Register a new user with profile details and optional image.
    
    The image is analyzed using CLIP model to generate AI insights
    that will help with outfit recommendations later.
    """
    try:
        # 1. Validate input
        if len(password) < 6:
            raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
        
        if gender not in ['male', 'female', 'other']:
            raise HTTPException(status_code=400, detail="Gender must be 'male', 'female', or 'other'")
        
        # 2. Check if user already exists
        existing_user = await get_user_by_email(email)
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this email already exists")
        
        # 3. Hash password
        password_hash = hash_password(password)
        
        # 4. Process image if provided
        image_url = None
        clip_insights_data = None
        
        if image:
            # Validate image type
            if not validate_image_type(image.content_type):
                raise HTTPException(
                    status_code=400, 
                    detail="Invalid image type. Allowed: JPEG, PNG, GIF, WebP"
                )
            
            # Read image bytes
            image_bytes = await image.read()
            
            # Generate unique filename
            filename = generate_unique_filename(image.filename, email)
            
            # Upload to Supabase Storage
            image_url = await upload_image_to_storage(
                file_bytes=image_bytes,
                filename=filename,
                content_type=image.content_type
            )
            
            # 5. Generate AI insights using CLIP
            clip_insights_data = analyze_image(image_bytes)
        
        # 6. Create user in database
        user_data = {
            "name": name,
            "email": email,
            "password_hash": password_hash,
            "gender": gender,
            "height": height,
            "country": country,
            "body_shape": body_shape,
            "skin_tone": skin_tone,
            "image_url": image_url,
            "clip_insights": clip_insights_data
        }
        
        created_user = await create_user(user_data)
        
        if not created_user:
            raise HTTPException(status_code=500, detail="Failed to create user")
        
        # 7. Return response
        response_data = {
            "message": "Signup successful",
            "user_id": created_user["id"],
            "clip_insights": clip_insights_data
        }
        
        return JSONResponse(content=response_data, status_code=201)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Signup error: {e}")
        raise HTTPException(status_code=500, detail=f"Signup failed: {str(e)}")

@router.post("/login", response_model=LoginResponse)
async def login(credentials: LoginRequest):
    """
    Authenticate user with email and password.
    """
    print(f"Login attempt for: {credentials.email}")
    try:
        # Get user by email
        print("Fetching user from DB...")
        user = await get_user_by_email(credentials.email)
        print(f"User fetch result: {user is not None}")
        
        if not user:
            print("User not found")
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Verify password
        print("Verifying password...")
        is_valid = verify_password(credentials.password, user["password_hash"])
        print(f"Password valid: {is_valid}")
        
        if not is_valid:
            print("Invalid password")
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        print("Login successful, returning response")
        return {
            "message": "Login successful",
            "user_id": user["id"],
            "name": user["name"],
            "email": user["email"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {e}")
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

@router.get("/profile/{user_id}")
async def get_profile(user_id: str):
    """
    Get user profile by ID with personalized fashion recommendations.
    """
    from app.core.database import get_user_by_id
    from app.components.ai.fashion_recommendations import generate_recommendations
    
    try:
        user = await get_user_by_id(user_id)
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Generate personalized recommendations
        recommendations = generate_recommendations(
            gender=user.get("gender"),
            body_shape=user.get("body_shape"),
            skin_tone=user.get("skin_tone"),
            height=user.get("height"),
            country=user.get("country")
        )
        
        # Remove sensitive data
        user.pop("password_hash", None)
        
        # Add recommendations to response
        user["recommendations"] = recommendations
        
        # Populate style_insights from persisted storage if available
        if "clip_insights" in user and user["clip_insights"] and "persisted_style_insights" in user["clip_insights"]:
            user["style_insights"] = user["clip_insights"]["persisted_style_insights"]
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Profile fetch error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch profile: {str(e)}")


@router.post("/update-profile")
async def update_profile(
    user_id: str = Form(...),
    name: Optional[str] = Form(None),
    gender: Optional[str] = Form(None),
    country: Optional[str] = Form(None),
    height: Optional[str] = Form(None),
    body_shape: Optional[str] = Form(None),
    skin_tone: Optional[str] = Form(None)
):
    """
    Update user profile details.
    """
    from app.core.database import get_user_by_id, get_supabase_client
    supabase = get_supabase_client()
    
    print(f"[DEBUG] Update request for user_id: {user_id}")
    
    try:
        if not user_id or user_id in ["null", "undefined"]:
            raise HTTPException(status_code=400, detail="Invalid user_id provided")

        # Validate user exists
        user = await get_user_by_id(user_id)
        if not user:
            print(f"[ERROR] User not found for ID: {user_id}")
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
        
        # Build update dictionary
        updates = {}
        if name: updates["name"] = name
        if gender: updates["gender"] = gender
        if country: updates["country"] = country
        if height: updates["height"] = height
        if body_shape: updates["body_shape"] = body_shape
        if skin_tone: updates["skin_tone"] = skin_tone
        
        if not updates:
            print("[INFO] No changes to update")
            return {"message": "No changes to update"}
            
        print(f"[DEBUG] Updating user {user_id} with: {updates}")
        
        # Update user record in database
        supabase = get_supabase_client()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database client not initialized")
        response = supabase.table("users").update(updates).eq("id", user_id).execute()
        
        if not response.data:
            print(f"[ERROR] No data returned after update for user {user_id}")
            raise HTTPException(status_code=500, detail="Database update failed - no record was modified")

        print(f"[SUCCESS] Profile updated for user {user_id}")
        
        return JSONResponse(content={
            "success": True,
            "message": "Profile updated successfully",
            "data": response.data[0]
        })
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Profile update error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to update profile: {str(e)}")


@router.post("/update-profile-photo")
async def update_profile_photo(
    user_id: str = Form(...),
    file: UploadFile = File(...)
):
    """
    Update user's profile photo.
    
    Args:
        user_id: User's UUID
        file: New profile image file
    
    Returns:
        JSON response with new image URL
    """
    from app.core.database import get_user_by_id, get_supabase_client
    supabase = get_supabase_client()
    from app.components.auth.utils import generate_unique_filename, validate_image_type
    
    try:
        # Validate user exists
        user = await get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Validate image type
        if not validate_image_type(file.content_type):
            raise HTTPException(
                status_code=400,
                detail="Invalid image type. Allowed: JPEG, PNG, GIF, WebP"
            )
        
        # Read image bytes
        image_bytes = await file.read()
        
        # Validate file size (max 5MB)
        if len(image_bytes) > 5 * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail="Image size must be less than 5MB"
            )
        
        # Generate unique filename
        filename = generate_unique_filename(file.filename, user["email"])
        
        # Upload to Supabase Storage
        image_url = await upload_image_to_storage(
            file_bytes=image_bytes,
            filename=filename,
            content_type=file.content_type
        )
        
        # Update user record in database
        response = supabase.table("users").update({
            "image_url": image_url
        }).eq("id", user_id).execute()
        
        return JSONResponse(content={
            "success": True,
            "message": "Profile photo updated successfully",
            "image_url": image_url
        })
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Profile photo update error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to update profile photo: {str(e)}")


@router.get("/style-insights/{user_id}")
async def get_style_insights(user_id: str):
    """
    Generate AI-powered style insights for a user using Groq.
    
    Args:
        user_id: User UUID
    
    Returns:
        JSON response with personalized style recommendations
    """
    from app.core.database import get_user_by_id
    from app.components.ai.style_insights import generate_style_insights
    
    try:
        print(f"[STYLE_INSIGHTS] Generating insights for user {user_id}")
        
        # Get user profile
        user_profile = await get_user_by_id(user_id)
        if not user_profile:
            raise HTTPException(status_code=404, detail="User not found")
        
        print(f"[STYLE_INSIGHTS] User: {user_profile.get('name')}, Country: {user_profile.get('country')}, Gender: {user_profile.get('gender')}", flush=True)
        
        # Generate insights using Groq
        result = await generate_style_insights(user_profile)
        
        if result["success"]:
            print(f"[SUCCESS] Style insights generated for user {user_id}")
            
            # Save insights to database for persistence
            try:
                from app.core.database import get_supabase_client, get_user_by_id
                supabase = get_supabase_client()
                if supabase:
                    # Fetch current user to preserve existing clip_insights
                    user_data = await get_user_by_id(user_id)
                    current_clip_insights = user_data.get("clip_insights") or {}
                    
                    # Store style insights inside clip_insights as a sub-field
                    # This avoids needing a schema change for a new column
                    current_clip_insights["persisted_style_insights"] = result["insights"]
                    
                    supabase.table("users").update({
                        "clip_insights": current_clip_insights
                    }).eq("id", user_id).execute()
                    
                    print(f"[DATABASE] Saved style insights into clip_insights for user {user_id}")
            except Exception as db_err:
                print(f"[DATABASE_ERROR] Failed to save style insights: {db_err}")
                
            return JSONResponse(content={
                "success": True,
                "insights": result["insights"]
            })
        else:
            error_msg = result.get('error', 'Unknown error')
            print(f"[ERROR] Failed to generate insights: {error_msg}")
            return JSONResponse(
                content={
                    "success": False,
                    "message": f"Failed to generate style insights: {error_msg}",
                    "insights": result["insights"]  # Return fallback insights
                },
                status_code=500
            )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Style insights error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to generate style insights: {str(e)}")
