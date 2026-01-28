import asyncio
import os
import json
from dotenv import load_dotenv
from app.components.ai.outfit_generator import generate_outfit_recommendations

async def test_groq_generation():
    load_dotenv()
    
    # Check if GROQ_API_KEY is present
    if not os.getenv("GROQ_API_KEY"):
        print("❌ Error: GROQ_API_KEY not found in .env")
        return

    print("🚀 Testing Groq (Llama 3.3 70B) Outfit Generation...")
    
    user_profile = {
        "gender": "male",
        "body_shape": "athletic",
        "skin_tone": "medium-tan",
        "height": "180cm",
        "country": "Pakistan"
    }
    
    try:
        recommendations = await generate_outfit_recommendations(
            user_profile=user_profile,
            event_type="Wedding Reception",
            event_venue="Banquet Hall",
            event_time="Evening",
            weather="Cool",
            theme="Fusion",
            num_looks=2
        )
        
        print(f"\n✅ Success! Generated {len(recommendations)} outfits.")
        print(json.dumps(recommendations[0], indent=2))
        
    except Exception as e:
        print(f"\n❌ Generation failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_groq_generation())
