"""
AI Style Insights Generator
Uses Groq (Llama 3.3) to generate personalized style recommendations
"""

from groq import AsyncGroq
import os
import json
from typing import Dict, Optional

# Initialize Groq client
api_key = os.getenv("GROQ_API_KEY")
if api_key:
    # Sanitize key
    api_key = api_key.strip().replace('"', '').replace("'", "")

groq_client = AsyncGroq(api_key=api_key)

async def generate_style_insights(user_profile: Dict) -> Dict:
    """
    Generate personalized style insights using Groq AI
    
    Args:
        user_profile: User profile data including gender, body_shape, skin_tone, country, etc.
    
    Returns:
        Dictionary with style recommendations
    """
    
    # Extract user details
    gender = (user_profile.get("gender") or "Not specified").title()
    body_shape = (user_profile.get("body_shape") or "Not specified").title()
    skin_tone = (user_profile.get("skin_tone") or "Not specified").title()
    country = user_profile.get("country") or "Pakistan"
    height = user_profile.get("height") or "Not specified"
    
    # Build context
    context_parts = [
        f"Gender: {gender}",
        f"Body Shape: {body_shape}",
        f"Skin Tone: {skin_tone}",
        f"Location: {country}",
        f"Height: {height}"
    ]
    
    user_context = ", ".join(context_parts)
    print(f"[STYLE_INSIGHTS] Context: {user_context}", flush=True)
    
    # Create prompt
    prompt = f"""You are a professional fashion stylist and personal shopper. Generate personalized style insights for a user with the following profile:

{user_context}

Provide a comprehensive style analysis in JSON format with these sections:

1. "summary": A warm, personalized 2-3 sentence overview of their style potential
2. "color_palette": Array of 5-6 recommended colors that complement their features (just color names)
3. "style_recommendations": Array of 3-4 specific style tips tailored to their body shape and preferences
4. "wardrobe_essentials": Array of 5-6 must-have clothing items for their profile
5. "fashion_dos": Array of 3 fashion do's specific to their body type
6. "fashion_donts": Array of 3 fashion don'ts to avoid
7. "cultural_tips": If country is provided, 1-2 sentences on incorporating local fashion trends

Keep recommendations practical, positive, and culturally sensitive. Focus on empowering the user.

Return ONLY valid JSON, no markdown formatting."""

    try:
        # Call Groq API
        response = await groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert fashion stylist. Always respond with valid JSON only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        # Parse response
        content = response.choices[0].message.content.strip()
        
        # Remove markdown code blocks if present
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        insights = json.loads(content)
        
        return {
            "success": True,
            "insights": insights,
            "generated_at": user_profile.get("created_at", "")
        }
        
    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to parse Groq response as JSON: {e}")
        print(f"[DEBUG] Raw response: {content}")
        return {
            "success": False,
            "error": "Failed to generate insights",
            "insights": {
                "summary": "We're having trouble generating insights right now. Please try again later.",
                "color_palette": [],
                "style_recommendations": [],
                "wardrobe_essentials": [],
                "fashion_dos": [],
                "fashion_donts": [],
                "cultural_tips": ""
            }
        }
    except Exception as e:
        print(f"[ERROR] Groq API error: {e}")
        return {
            "success": False,
            "error": str(e),
            "insights": {
                "summary": "Unable to generate insights at this time.",
                "color_palette": [],
                "style_recommendations": [],
                "wardrobe_essentials": [],
                "fashion_dos": [],
                "fashion_donts": [],
                "cultural_tips": ""
            }
        }
