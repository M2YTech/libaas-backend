import os
from pathlib import Path

env_path = Path(r"c:\Users\Lenovo\Desktop\Libaas AI Backend\backend\.env")

with open(env_path, 'rb') as f:
    content = f.read()
    print(f"File content (bytes): {content[:50]}")

with open(env_path, 'r', encoding='utf-8-sig') as f:
    for line in f:
        print(f"Line: {line.strip()}")
        if '=' in line:
            k, v = line.strip().split('=', 1)
            print(f"Key: '{k}', Val: '{v}'")
