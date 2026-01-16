"""
Run script for the FastAPI server.
Execute this file to start the backend server.
"""
import os
import sys

# Ensure we're in the correct directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
sys.path.insert(0, script_dir)

# Load environment variables from .env file
from dotenv import load_dotenv
env_path = os.path.join(script_dir, ".env")
load_dotenv(env_path)

if __name__ == "__main__":
    import uvicorn
    # Disable reload to avoid subprocess issues with environment variables
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)

