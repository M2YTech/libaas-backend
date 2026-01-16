"""
GPT-4o-mini based image analysis for fashion insights.
Replaces the heavy local CLIP model with lightweight API calls.
"""

from typing import Dict, Any, List
import base64
from openai import OpenAI
import os

def get_openai_client():
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_image(image_bytes: bytes) -> Dict[str, Any]:
    """
    Analyze an image using GPT-4o-mini Vision capabilities.
    
    Args:
        image_bytes: Raw bytes of the image file
    
    Returns:
        Dictionary containing fashion insights (top_label, confidence, etc.)
    """
    try:
        client = get_openai_client()
        
        # Convert image to base64
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        
        print("[AI] Analyzing profile image with GPT-4o-mini...", flush=True)
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a fashion AI. Analyze the person's clothing style in this photo. Predict their preferred fashion style from these categories: ['Casual', 'Formal', 'Traditional (Desi)', 'Modern', 'Streetwear', 'Bohemian', 'Minimalist']. Return a JSON object with: 'top_label', 'top_confidence' (0.0-1.0), and 'all_predictions' (list of other likely styles with scores)."
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Analyze this person's fashion style."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                                "detail": "low"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300,
            response_format={"type": "json_object"}
        )
        
        # Parse result
        import json
        result_text = response.choices[0].message.content
        result_json = json.loads(result_text)
        
        # Normalize keys to match old CLIP interface
        return {
            "top_label": result_json.get("top_label", "unknown"),
            "top_confidence": result_json.get("top_confidence", 0.0),
            "all_predictions": result_json.get("all_predictions", []),
            "source": "gpt-4o-mini"
        }
        
    except Exception as e:
        print(f"[ERROR] GPT-4o-mini analysis failed: {e}")
        return {
            "top_label": "unknown",
            "top_confidence": 0.0,
            "all_predictions": [],
            "error": str(e)
        }
