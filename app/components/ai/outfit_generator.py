"""
AI-Powered Outfit Generator Service
Uses Groq (Llama 3.3 70B) to generate detailed outfit recommendations
"""
import os
import json
from typing import List, Dict, Optional
from groq import AsyncGroq

# Initialize Groq client (will be None if API key not set)
api_key = os.getenv("GROQ_API_KEY")
client = AsyncGroq(api_key=api_key) if api_key else None


async def generate_outfit_recommendations(
    user_profile: Dict,
    event_type: str,
    event_venue: str,
    event_time: str,
    weather: str,
    theme: str,
    num_looks: int = 3,
    wardrobe_items: List[Dict] = []
) -> List[Dict]:
    """
    Generate outfit recommendations using Groq (Llama 3.3 70B)
    
    Args:
        user_profile: User profile data (body_shape, skin_tone, gender, etc.)
        event_type: Type of event (wedding, party, office, etc.)
        event_venue: Venue type (garden, hotel, restaurant, etc.)
        event_time: Time of day (morning, afternoon, evening, night)
        weather: Weather/season (hot, warm, cool, cold, rainy)
        theme: Style theme (desi, formal, elite, casual, traditional, modern, fusion)
        num_looks: Number of outfit recommendations to generate (3, 5, or 7)
        wardrobe_items: User's wardrobe inventory for matching
    
    Returns:
        List of outfit recommendation dictionaries
    """
    
    # Check if Groq client is available
    if client is None:
        raise Exception("Groq API key not configured. Please add GROQ_API_KEY to your .env file.")
    
    # Build the prompt (GPT generates outfit requirements only, no wardrobe matching)
    prompt = build_outfit_prompt(
        user_profile=user_profile,
        event_type=event_type,
        event_venue=event_venue,
        event_time=event_time,
        weather=weather,
        theme=theme,
        num_looks=num_looks
    )
    
    # Debug: Check API Key format
    masked_key = f"{api_key[:8]}...{api_key[-4:]}" if api_key else "None"
    print(f"[DEBUG] Using Groq API Key: {masked_key}", flush=True)
    if not api_key.startswith("gsk_"):
        print("[WARNING] API Key does not start with 'gsk_'. Check for quotes or whitespace.", flush=True)
    
    try:
        print(f"[OUTFIT_GEN] Generating {num_looks} outfit recommendations for {event_type}...", flush=True)
        
        response = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert personalized fashion stylist with deep knowledge of global and South Asian fashion, cultural dress codes, and modern styling. You provide detailed, practical outfit recommendations that are strictly tailored to the user's specific body shape, skin tone, height, and country context. IMPORTANT: Always return the response in valid JSON format."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=3000,
            stream=False
        )
        
        # Parse the response
        content = response.choices[0].message.content
        recommendations_data = json.loads(content)
        
        print(f"[SUCCESS] Generated {len(recommendations_data.get('outfits', []))} outfit recommendations", flush=True)
        
        # Structure the response (No backend matching)
        outfits = []
        for idx, outfit in enumerate(recommendations_data.get("outfits", []), 1):
            sections = {}
            
            # Process each section
            for section_name in ["top", "layer", "bottom", "footwear", "accessories"]:
                if section_name in outfit and outfit[section_name]:
                    data = outfit[section_name]
                    
                    # Handle accessories (list format)
                    if section_name == "accessories":
                        sections[section_name] = {"items": data.get("items", [])}
                        continue
                        
                    # Handle main sections
                    processed_section = {
                        "item": data.get("item", ""),
                        "details": data.get("details", [])
                    }
                    
                    # No wardrobe matching
                    # processed_section["wardrobe_match"] = None
                    
                    sections[section_name] = processed_section

            processed_outfit = {
                "title": outfit.get("title", f"Look {idx}"),
                "sections": sections
            }
            
            outfits.append({
                "id": idx,
                "title": outfit.get("title", f"Look {idx}"),
                "description": outfit.get("description", ""),
                "sections": sections,
                "full_text_prompt": build_image_prompt(processed_outfit, user_profile)
            })
        
        return outfits
        
    except Exception as e:
        print(f"[ERROR] Failed to generate outfit recommendations: {type(e).__name__}: {e}", flush=True)
        import traceback
        traceback.print_exc()
        raise e


def build_outfit_prompt(
    user_profile: Dict,
    event_type: str,
    event_venue: str,
    event_time: str,
    weather: str,
    theme: str,
    num_looks: int
) -> str:
    """Build the Groq prompt for outfit generation (requirements only)"""
    
    # Extract user profile data
    gender = user_profile.get("gender", "male")
    body_shape = user_profile.get("body_shape", "")
    skin_tone = user_profile.get("skin_tone", "")
    height = user_profile.get("height", "")
    country = user_profile.get("country", "")
    
    prompt = f"""
    You are an expert fashion stylist AI.
    
    TASK:
    Generate {num_looks} complete outfit recommendations for a {gender} based in {country or "Pakistan"}.
    The outfits should be culturally appropriate for {country or "Pakistan"}, stylish, and suitable for the event.
    
    CRITICAL: YOU MUST CUSTOMIZE THE LOOKS FOR THIS USER:
    - Gender: {gender}
    - Body Shape: {body_shape or "Not specified"} (Recommend cuts/fits that flatter this shape)
    - Skin Tone: {skin_tone or "Not specified"} (Recommend colors that complement this tone)
    - Height: {height or "Not specified"} (Recommend styles that suit this height)
    - Country/Culture: {country or "Pakistan"} (Ensure cultural appropriateness)

    EVENT CONTEXT:
    - Event Type: {event_type}
    - Venue: {event_venue}
    - Time of Day: {event_time}
    - Weather: {weather}
    - Theme: {theme}

    OUTPUT INSTRUCTIONS:
    - Provide specific advice on WHY this outfit works for their body shape/skin tone in the description.
    - Be specific about fabrics (e.g., "Silk", "Cotton", "Jamawar").
    - Be specific about colors (e.g., "Navy Blue" instead of just "Blue").

    OUTPUT FORMAT (STRICT JSON):
    {{
      "outfits": [
        {{
          "title": "Outfit Title",
          "description": "Description explaining why this works for a {body_shape} {gender} with {skin_tone} skin in {country}.",
          "top": {{
            "item": "Name/Description of item",
            "details": ["detail1", "detail2"],
            "category": "top",
            "color": "specific color",
            "fabric": "specific fabric",
            "style": "specific style"
          }},
          "layer": {{
            "item": "Waistcoat or Shawl description (optional)",
            "details": ["..."],
            "category": "layer",
            "color": "...",
            "fabric": "...",
            "style": "..."
          }},
          "bottom": {{
            "item": "Trousers/Shalwar description",
            "details": ["..."],
            "category": "bottom",
            "color": "...",
            "fabric": "...",
            "style": "..."
          }},
          "footwear": {{
            "item": "Shoe description",
            "details": ["..."],
            "category": "footwear",
            "color": "...",
            "fabric": "...",
            "style": "..."
          }},
          "accessories": {{
            "items": ["Watch", "Cufflinks"]
          }}
        }}
      ]
    }}
    """
    
    return prompt


def build_image_prompt(outfit: Dict, user_profile: Dict) -> str:
    """
    Build a detailed text prompt for image generation from outfit recommendation
    This will be used later with nano-banana or similar image generation model
    """
    
    gender = user_profile.get("gender", "male")
    body_shape = user_profile.get("body_shape", "")
    skin_tone = user_profile.get("skin_tone", "")
    country = user_profile.get("country", "Pakistan")
    
    # Extract outfit details
    title = outfit.get("title", "")
    sections = outfit.get("sections", {})
    
    # Build detailed description
    prompt_parts = []
    
    # Start with person description
    person_desc = f"A well-groomed {country} {gender}"
    if body_shape:
        person_desc += f" with {body_shape} build"
    if skin_tone:
        person_desc += f" and {skin_tone} skin tone"
    
    prompt_parts.append(person_desc)
    
    # Add outfit details
    if "top" in sections:
        top = sections["top"]
        top_desc = f"wearing {top.get('item', '')}"
        if top.get('details'):
            top_desc += f" ({', '.join(top['details'])})"
        prompt_parts.append(top_desc)
    
    if "layer" in sections:
        layer = sections["layer"]
        layer_desc = f"with {layer.get('item', '')}"
        if layer.get('details'):
            layer_desc += f" ({', '.join(layer['details'])})"
        prompt_parts.append(layer_desc)
    
    if "bottom" in sections:
        bottom = sections["bottom"]
        bottom_desc = f"paired with {bottom.get('item', '')}"
        if bottom.get('details'):
            bottom_desc += f" ({', '.join(bottom['details'])})"
        prompt_parts.append(bottom_desc)
    
    if "footwear" in sections:
        footwear = sections["footwear"]
        footwear_desc = f"wearing {footwear.get('item', '')}"
        if footwear.get('details'):
            footwear_desc += f" ({', '.join(footwear['details'])})"
        prompt_parts.append(footwear_desc)

    if "accessories" in sections:
        accessories = sections["accessories"]
        if accessories.get("items"):
            acc_desc = f"accessorized with {', '.join(accessories['items'])}"
            prompt_parts.append(acc_desc)
    
    # Add styling context
    prompt_parts.append(f"cultural {country} fashion, full body shot, professional photography, natural lighting, clean background")
    
    full_prompt = ", ".join(prompt_parts)
    
    return full_prompt
