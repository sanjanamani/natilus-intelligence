# test_connection.py
import os
from dotenv import load_dotenv

load_dotenv()

# Just print your credentials (remove this after testing!)
print("URL:", os.getenv('SUPABASE_URL'))
print("KEY exists:", bool(os.getenv('SUPABASE_KEY')))

# Test basic HTTP request to Supabase
import requests

url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')

response = requests.get(
    f"{url}/rest/v1/aerospace_talent?select=*&limit=1",
    headers={
        'apikey': key,
        'Authorization': f'Bearer {key}'
    }
)

print(f"Status: {response.status_code}")
print(f"Response: {response.text[:200]}")