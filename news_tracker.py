# news_tracker.py
import requests
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

class NewsTracker:
    def __init__(self):
        self.api_key = os.getenv('NEWSAPI_KEY')
        self.supabase = create_client(
            os.getenv('SUPABASE_URL'),
            os.getenv('SUPABASE_KEY')
        )
    
    def get_competitor_news(self):
        """Track competitor news using NewsAPI"""
        print("📰 Fetching competitor news...")
        
        if not self.api_key:
            print("⚠️ No NewsAPI key found. Get one free at newsapi.org")
            return []
        
        url = "https://newsapi.org/v2/everything"
        
        # Companies to track
        companies = [
            ('JetZero', 'HIGH'),
            ('Archer Aviation', 'MEDIUM'),
            ('Joby Aviation', 'MEDIUM'),
            ('Boeing BWB', 'HIGH'),
            ('Spirit AeroSystems', 'HIGH')
        ]
        
        all_news = []
        
        for company, importance in companies:
            params = {
                'q': company,
                'apiKey': self.api_key,
                'language': 'en',
                'sortBy': 'publishedAt',
                'from': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
                'pageSize': 10
            }
            
            try:
                response = requests.get(url, params=params)
                
                if response.status_code == 200:
                    articles = response.json().get('articles', [])
                    
                    for article in articles[:3]:  # Top 3 per company
                        # Analyze the headline for important keywords
                        headline = article['title'].lower()
                        
                        impact = importance
                        if any(word in headline for word in ['patent', 'funding', 'contract', 'hire', 'ceo']):
                            impact = 'HIGH'
                        
                        all_news.append({
                            'company': company,
                            'news_type': 'News',
                            'details': article['title'][:200],
                            'impact_on_natilus': f"{impact} - {article['source']['name']}",
                            'date_detected': article['publishedAt']
                        })
                    
                    print(f"✅ Found {len(articles)} articles about {company}")
                    
                elif response.status_code == 429:
                    print("⚠️ NewsAPI rate limit reached")
                    break
                    
            except Exception as e:
                print(f"❌ Error fetching news for {company}: {e}")
        
        return all_news
    
    def get_aviation_week_headlines(self):
        """Scrape Aviation Week for industry news"""
        print("📰 Checking Aviation Week...")
        
        url = "https://aviationweek.com/defense-space"
        
        try:
            response = requests.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            if response.status_code == 200:
                # Look for BWB mentions
                if 'blended wing' in response.text.lower() or 'bwb' in response.text.lower():
                    return [{
                        'company': 'Industry',
                        'news_type': 'Industry News',
                        'details': 'New BWB developments mentioned on Aviation Week',
                        'impact_on_natilus': 'MEDIUM - Industry momentum building'
                    }]
        except Exception as e:
            print(f"⚠️ Could not access Aviation Week: {e}")
        
        return []
    
    def save_to_database(self, news):
        """Save news to database"""
        if news:
            try:
                for article in news:
                    self.supabase.table('competitor_news').insert(article).execute()
                print(f"💾 Saved {len(news)} news items")
            except Exception as e:
                print(f"❌ Database error: {e}")
    
    def run(self):
        """Run news tracking"""
        all_news = []
        
        # Get news from NewsAPI
        all_news.extend(self.get_competitor_news())
        
        # Check Aviation Week
        all_news.extend(self.get_aviation_week_headlines())
        
        # Save to database
        self.save_to_database(all_news)
        
        return all_news

if __name__ == "__main__":
    # First, make sure you have your NewsAPI key in .env
    if not os.getenv('NEWSAPI_KEY'):
        print("⚠️ Please add NEWSAPI_KEY to your .env file")
        print("Get one free at: https://newsapi.org")
    else:
        tracker = NewsTracker()
        news = tracker.run()
        print(f"\n📰 Total news items tracked: {len(news)}")