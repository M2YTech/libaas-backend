
import os
import asyncio
import json
from groq import AsyncGroq
from dotenv import load_dotenv

load_dotenv()

async def test_groq():
    api_key = os.getenv("GROQ_API_KEY")
    print(f"API Key: {api_key[:10]}...")
    
    client = AsyncGroq(api_key=api_key)
    
    try:
        response = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": "Return a JSON object with a 'test' key and 'ok' value. Respond with ONLY JSON."}
            ],
            temperature=0,
        )
        content = response.choices[0].message.content
        print(f"Raw Content: '{content}'")
        
        data = json.loads(content)
        print(f"Parsed Data: {data}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_groq())
