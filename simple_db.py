# simple_db.py - Direct Supabase API calls without the SDK
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

class SimpleSupabase:
    def __init__(self):
        self.url = os.getenv('SUPABASE_URL')
        self.key = os.getenv('SUPABASE_KEY')
        self.headers = {
            'apikey': self.key,
            'Authorization': f'Bearer {self.key}',
            'Content-Type': 'application/json',
            'Prefer': 'return=representation'
        }
    
    def insert_talent(self, data):
        """Insert data into aerospace_talent table"""
        response = requests.post(
            f"{self.url}/rest/v1/aerospace_talent",
            headers=self.headers,
            json=data
        )
        return response.json() if response.status_code == 201 else None
    
    def insert_competitor_moves(self, data):
        """Insert data into competitor_moves table"""
        response = requests.post(
            f"{self.url}/rest/v1/competitor_moves",
            headers=self.headers,
            json=data
        )
        return response.json() if response.status_code == 201 else None
    
    def get_all_talent(self):
        """Get all talent from database"""
        response = requests.get(
            f"{self.url}/rest/v1/aerospace_talent?select=*",
            headers=self.headers
        )
        return response.json() if response.status_code == 200 else []
    
    def get_competitor_moves(self):
        """Get all competitor moves"""
        response = requests.get(
            f"{self.url}/rest/v1/competitor_moves?select=*",
            headers=self.headers
        )
        return response.json() if response.status_code == 200 else []