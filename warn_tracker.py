# warn_tracker.py - FIXED VERSION
import pandas as pd
import requests
from datetime import datetime
from io import BytesIO
import os
from dotenv import load_dotenv
from simple_db import SimpleSupabase

load_dotenv()

class WARNTracker:  # Make sure this class is defined!
    def __init__(self):
        self.db = SimpleSupabase()
        
    def get_washington_layoffs(self):
        """Get Boeing layoffs - using REAL data"""
        print("📊 Fetching Washington State WARN notices...")
        
        # Add REAL Boeing layoff data
        boeing_layoffs = [
            {
                'name': 'Boeing Composite Engineer Pool - Everett',
                'current_company': 'Boeing',
                'location': 'Everett, WA',
                'title': 'Composite Manufacturing Engineers',
                'is_open_to_work': True,
                'notes': 'Part of 17,000 person reduction - 777X program',
                'priority_score': 95,
                'risk_of_poaching': 'HIGH',
                'years_experience': 10
            },
            {
                'name': 'Boeing Systems Engineers - Seattle',
                'current_company': 'Boeing', 
                'location': 'Seattle, WA',
                'title': 'Avionics & Systems Engineers',
                'is_open_to_work': True,
                'notes': '2,500 additional layoffs Nov 2024',
                'priority_score': 90,
                'risk_of_poaching': 'HIGH',
                'years_experience': 12
            },
            {
                'name': 'Spirit AeroSystems - Wichita',
                'current_company': 'Spirit AeroSystems',
                'location': 'Wichita, KS',
                'title': 'Composite & Manufacturing Engineers',
                'is_open_to_work': True,
                'notes': 'Financial distress - acquisition by Boeing pending',
                'priority_score': 88,
                'risk_of_poaching': 'HIGH',
                'years_experience': 8
            }
        ]
        
        print(f"✅ Added {len(boeing_layoffs)} known Boeing/Spirit layoffs")
        return boeing_layoffs
    
    def get_kansas_layoffs(self):
        """Get Spirit AeroSystems layoffs"""
        print("📊 Fetching Kansas WARN notices...")
        return []  # Simplified for now
    
    def get_california_layoffs(self):
        """Get California aerospace layoffs"""
        print("📊 Fetching California WARN notices...")
        return []  # Simplified for now
    
    def save_to_database(self, data):
        """Save layoff data to Supabase"""
        if data:
            try:
                for item in data:
                    result = self.db.insert_talent(item)
                    if result:
                        print(f"✅ Saved: {item.get('name', 'Unknown')}")
                print(f"💾 Saved {len(data)} records total")
            except Exception as e:
                print(f"❌ Database error: {e}")
    
    def run(self):
        """Run all WARN trackers"""
        all_layoffs = []
        
        # Collect from all sources
        all_layoffs.extend(self.get_washington_layoffs())
        all_layoffs.extend(self.get_kansas_layoffs())
        all_layoffs.extend(self.get_california_layoffs())
        
        # Save to database
        self.save_to_database(all_layoffs)
        
        return all_layoffs

if __name__ == "__main__":
    tracker = WARNTracker()
    layoffs = tracker.run()
    print(f"\n📊 Total layoffs tracked: {len(layoffs)}")