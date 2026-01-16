import sys
import io

# Force UTF-8 encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from gradio_client import Client

try:
    print("Inspecting levihsu/OOTDiffusion API...")
    client = Client("levihsu/OOTDiffusion")
    client.view_api()
except Exception as e:
    print(f"Error: {e}")
