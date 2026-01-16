"""
Wardrobe API Routes
Handle wardrobe item upload, categorization, listing, and management.
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional, Dict
import uuid
from datetime import datetime
import tempfile
import os

from app.core.database import (
    create_wardrobe_item,
    get_user_wardrobe,
    delete_wardrobe_item,
    update_wardrobe_item,
    upload_wardrobe_image,
    upload_tryon_image
)
from app.components.ai.outfit_generator import generate_outfit_recommendations

router = APIRouter()

# Auto-categorization disabled for slim deployment


@router.post("/upload")
async def upload_wardrobe_item(
    user_id: str = Form(...),
    file: UploadFile = File(...)
):
    """
    Upload a wardrobe item (Simple storage, no AI classification).
    """
    try:
        # 1. Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # 2. Read file
        file_bytes = await file.read()
        
        # 3. Generate unique filename
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
        unique_filename = f"{user_id}/{uuid.uuid4()}.{file_extension}"
        
        # 4. Upload image to Supabase Storage
        image_url = await upload_wardrobe_image(
            file_bytes,
            unique_filename,
            file.content_type
        )
        
        # 5. Create wardrobe item record (Default/Empty tags)
        item_data = {
            "user_id": user_id,
            "name": "New Item",
            "description": "Uploaded item",
            "image_url": image_url,
            "category": "Uncategorized", 
            "sub_category": "item",
            "color": "unknown",
            "style": "casual",
            "pattern": "plain",
            "tags": ["uploaded"],
            "auto_categorized": False
        }
        
        created_item = await create_wardrobe_item(item_data)
        
        if not created_item:
            raise HTTPException(status_code=500, detail="Failed to create wardrobe item")
        
        return JSONResponse(
            content={
                "success": True,
                "item": created_item,
                "message": "Item uploaded successfully!"
            },
            status_code=201
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error uploading wardrobe item: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.get("/items/{user_id}")
async def get_wardrobe_items(user_id: str):
    """
    Get all wardrobe items for a user.
    """
    try:
        items = await get_user_wardrobe(user_id)
        
        return {
            "success": True,
            "count": len(items),
            "items": items
        }
    
    except Exception as e:
        print(f"Error fetching wardrobe: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch wardrobe: {str(e)}")


@router.delete("/items/{item_id}")
async def delete_wardrobe_item_endpoint(item_id: str, user_id: str):
    """
    Delete a wardrobe item.
    """
    try:
        success = await delete_wardrobe_item(item_id, user_id)
        
        if success:
            return {
                "success": True,
                "message": "Item deleted successfully"
            }
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error deleting wardrobe item: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete item: {str(e)}")


@router.patch("/items/{item_id}")
async def update_wardrobe_item_endpoint(
    item_id: str,
    user_id: str = Form(...),
    name: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    tags: Optional[str] = Form(None)  # Comma-separated
):
    """
    Update a wardrobe item.
    """
    try:
        updates = {}
        
        if name:
            updates["name"] = name
        if category:
            updates["category"] = category
        if tags:
            updates["tags"] = tags.split(",")
        
        updates["updated_at"] = datetime.now().isoformat()
        
        updated_item = await update_wardrobe_item(item_id, user_id, updates)
        
        if not updated_item:
            raise HTTPException(status_code=404, detail="Item not found")
        
        return {
            "success": True,
            "item": updated_item,
            "message": "Item updated successfully"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating wardrobe item: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update item: {str(e)}")


@router.post("/recategorize/{user_id}")
async def recategorize_all_items(user_id: str):
    """
    Recategorization not available in slim deployment.
    """
    return {
        "success": False,
        "message": "AI Auto-categorization is disabled in this deployment."
    }


def _generate_outfit_description(outfit: Dict, event_type: str, user_profile: Optional[Dict]) -> str:
    """Generate a personalized description for an outfit"""
    items = outfit.get("items", [])
    primary_color = (outfit.get("primary_color") or "").title()
    style = (outfit.get("style") or "").title()
    
    # Get body shape and skin tone if available
    body_shape = (user_profile.get("body_shape") or "").title() if user_profile else ""
    skin_tone = (user_profile.get("skin_tone") or "").title() if user_profile else ""
    
    # Build description
    description_parts = []
    
    # Event context
    event_descriptions = {
        "wedding": "Perfect for a wedding celebration",
        "mehndi": "Vibrant and festive for a mehndi ceremony",
        "cultural": "Elegantly traditional for a cultural event",
        "office": "Professional and polished for the workplace",
        "casual": "Comfortable and stylish for everyday wear",
        "party": "Eye-catching and fun for a party",
        "formal": "Sophisticated and elegant for a formal occasion"
    }
    
    description_parts.append(event_descriptions.get(event_type.lower(), "Perfect for any occasion"))
    
    # Personalization based on user profile
    if body_shape:
        description_parts.append(f"This ensemble flatters your {body_shape} silhouette")
    
    if skin_tone and primary_color:
        description_parts.append(f"featuring {primary_color} tones that complement your {skin_tone} complexion")
    elif primary_color:
        description_parts.append(f"featuring beautiful {primary_color} tones")
    
    # Style mention
    if style:
        description_parts.append(f"The {style} style adds the perfect finishing touch")
    
    return ". ".join(description_parts) + "."


@router.post("/generate-looks")
async def generate_outfit_looks(
    user_id: str = Form(...),
    event_type: str = Form("casual"),
    num_looks: int = Form(5)
):
    """
    Virtual Try-On is temporarily unavailable in slim deployment.
    """
    return JSONResponse({
        "success": False,
        "message": "AI Virtual Try-On is coming soon (Disabled for optimization)."
    })


@router.post("/generate-outfit-recommendations")
async def generate_outfit_recommendations_endpoint(
    user_id: str = Form(...),
    event_type: str = Form(...),
    event_venue: str = Form(...),
    event_time: str = Form(...),
    weather: str = Form(...),
    theme: str = Form(...),
    num_looks: int = Form(3)
):
    """
    Generate AI-powered outfit recommendations using GPT-4o-mini
    
    Args:
        user_id: User UUID
        event_type: Type of event (wedding, party, office, etc.)
        event_venue: Venue description (garden, hotel, etc.)
        event_time: Time of day (morning, afternoon, evening, night)
        weather: Weather/season (hot, warm, cool, cold, rainy)
        theme: Style theme (desi, formal, elite, casual, etc.)
        num_looks: Number of outfit recommendations (3, 5, or 7)
    
    Returns:
        JSON response with outfit recommendations
    """
    try:
        print(f"[OUTFIT_REC] Generating {num_looks} recommendations for user {user_id}", flush=True)
        print(f"[EVENT] Type: {event_type}, Venue: {event_venue}, Time: {event_time}", flush=True)
        print(f"[STYLE] Weather: {weather}, Theme: {theme}", flush=True)
        
        # Get user profile from database
        # Get user profile from database
        try:
            from app.core.database import get_user_by_id
            user_profile = await get_user_by_id(user_id)
        except Exception as e:
            print(f"[ERROR] Database fetch failed: {e}")
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")
        
        if not user_profile:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Ensure country is present (defaults to None in DB if not set)
        if "country" not in user_profile or not user_profile["country"]:
             pass
        
        print(f"[USER] Gender: {user_profile.get('gender')}, Body Shape: {user_profile.get('body_shape')}, Country: {user_profile.get('country')}", flush=True)
        
        # Generate outfit recommendations using GPT-4o-mini
        try:
            recommendations = await generate_outfit_recommendations(
                user_profile=user_profile,
                event_type=event_type,
                event_venue=event_venue,
                event_time=event_time,
                weather=weather,
                theme=theme,
                num_looks=num_looks
            )
        except Exception as e:
            print(f"[ERROR] AI generation failed: {e}")
            raise HTTPException(status_code=500, detail=f"AI Service Error: {str(e)}")
        
        print(f"[SUCCESS] Generated {len(recommendations)} outfit recommendations", flush=True)
        
        return JSONResponse(content={
            "success": True,
            "recommendations": recommendations,
            "event_details": {
                "type": event_type,
                "venue": event_venue,
                "time": event_time,
                "weather": weather,
                "theme": theme
            }
        })
        
    except Exception as e:
        print(f"[ERROR] Failed to generate outfit recommendations: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

