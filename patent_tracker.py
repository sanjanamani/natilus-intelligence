# patent_tracker.py
import requests
import json
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

class PatentTracker:
    def __init__(self):
        self.supabase = create_client(
            os.getenv('SUPABASE_URL'),
            os.getenv('SUPABASE_KEY')
        )
        
    def search_uspto_patents(self):
        """Search for recent BWB and aerospace patents"""
        print("🔍 Searching USPTO for BWB patents...")
        
        # USPTO PatentsView API - completely free!
        base_url = "https://api.patentsview.org/patents/query"
        
        # Calculate date 30 days ago
        date_threshold = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        # Search query for BWB-related patents
        query = {
            "q": {
                "_and": [
                    {
                        "_or": [
                            {"_text_any": {"patent_title": "blended wing"}},
                            {"_text_any": {"patent_title": "BWB"}},
                            {"_text_any": {"patent_abstract": "blended wing body"}},
                            {"_text_any": {"patent_abstract": "distributed propulsion"}}
                        ]
                    },
                    {"_gte": {"patent_date": date_threshold}}
                ]
            },
            "f": ["patent_number", "patent_title", "patent_date", "assignee_organization", "patent_abstract"],
            "s": [{"patent_date": "desc"}],
            "o": {"per_page": 25}
        }
        
        try:
            response = requests.post(
                base_url,
                json=query,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                data = response.json()
                patents = data.get('patents', [])
                
                patent_insights = []
                for patent in patents:
                    # Check if it's from a competitor
                    assignee = patent.get('assignees', [{}])[0].get('assignee_organization', 'Unknown')
                    
                    if any(company in assignee for company in ['Boeing', 'JetZero', 'Airbus', 'Lockheed']):
                        impact = 'HIGH'
                    else:
                        impact = 'MEDIUM'
                    
                    patent_insights.append({
                        'company': assignee,
                        'news_type': 'Patent Filing',
                        'details': f"Patent: {patent.get('patent_title', 'Unknown')}",
                        'impact_on_natilus': f"{impact} - {patent.get('patent_number', '')}",
                        'date_detected': patent.get('patent_date', '')
                    })
                
                print(f"✅ Found {len(patent_insights)} relevant patents")
                return patent_insights
            else:
                print(f"❌ USPTO API error: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Error searching patents: {e}")
            return []
    
    def search_google_patents(self):
        """Alternative: Search Google Patents (no API needed)"""
        print("🔍 Searching Google Patents...")
        
        # We can scrape Google Patents search results
        search_terms = [
            "blended+wing+body+aircraft",
            "JetZero",
            "distributed+propulsion+cargo"
        ]
        
        patent_insights = []
        
        for term in search_terms:
            url = f"https://patents.google.com/?q={term}&oq={term}&sort=new"
            
            try:
                # For basic info, we can parse the URL
                # In production, you'd use BeautifulSoup here
                response = requests.get(url, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                })
                
                if response.status_code == 200 and 'JetZero' in response.text:
                    patent_insights.append({
                        'company': 'Competitor',
                        'news_type': 'Patent Activity',
                        'details': f'New patents found for: {term.replace("+", " ")}',
                        'impact_on_natilus': 'MEDIUM - Competitive landscape evolving'
                    })
                    
            except Exception as e:
                print(f"⚠️ Could not search Google Patents: {e}")
        
        return patent_insights
    
    def save_to_database(self, patents):
        """Save patent intelligence to database"""
        if patents:
            try:
                for patent in patents:
                    self.supabase.table('competitor_moves').insert(patent).execute()
                print(f"💾 Saved {len(patents)} patent insights")
            except Exception as e:
                print(f"❌ Database error: {e}")
    
    def run(self):
        """Run patent tracking"""
        all_patents = []
        
        # Try USPTO first
        all_patents.extend(self.search_uspto_patents())
        
        # Also check Google Patents
        all_patents.extend(self.search_google_patents())
        
        # Save to database
        self.save_to_database(all_patents)
        
        return all_patents

if __name__ == "__main__":
    tracker = PatentTracker()
    patents = tracker.run()
    print(f"\n📋 Total patents tracked: {len(patents)}")