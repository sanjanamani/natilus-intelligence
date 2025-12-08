"""
News Intelligence Scraper - REAL DATA
Uses Google News RSS feeds to monitor aerospace industry
"""

import feedparser
from datetime import datetime
from supabase import create_client, Client
import os
import time
from textblob import TextBlob

# Supabase setup
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# News topics to monitor
NEWS_TOPICS = [
    "Natilus aircraft",
    "JetZero BWB",
    "Boom Supersonic",
    "Spirit AeroSystems bankruptcy",
    "Boeing blended wing body",
    "cargo aircraft innovation",
    "sustainable aviation fuel",
    "FAA aircraft certification",
    "aerospace manufacturing",
    "venture capital aerospace"
]

# Company/entity tracking
KEY_ENTITIES = [
    "Natilus", "JetZero", "Boom Supersonic", "Boeing", "Airbus",
    "Spirit AeroSystems", "Triumph Group", "FAA", "NASA",
    "Lux Capital", "Founders Fund", "Khosla Ventures"
]

def get_google_news_rss(topic, num_results=10):
    """
    Fetch news from Google News RSS
    URL: https://news.google.com/rss/search?q={topic}&hl=en-US&gl=US&ceid=US:en
    """
    base_url = "https://news.google.com/rss/search"
    
    # Encode topic
    encoded_topic = topic.replace(" ", "+")
    rss_url = f"{base_url}?q={encoded_topic}&hl=en-US&gl=US&ceid=US:en"
    
    print(f"Fetching news for: {topic}")
    
    try:
        feed = feedparser.parse(rss_url)
        articles = []
        
        for entry in feed.entries[:num_results]:
            # Parse published date
            pub_date = datetime(*entry.published_parsed[:6]) if hasattr(entry, 'published_parsed') else datetime.now()
            
            # Extract source from title (Google News format: "Article Title - Source")
            source = extract_source(entry.title)
            clean_title = entry.title.split(' - ')[0] if ' - ' in entry.title else entry.title
            
            article = {
                'source': source,
                'headline': clean_title,
                'summary': entry.get('summary', '')[:500],
                'url': entry.link,
                'published_date': pub_date.isoformat(),
                'category': categorize_news(clean_title + " " + entry.get('summary', '')),
                'entities': extract_entities(entry.title + " " + entry.get('summary', '')),
                'sentiment': analyze_sentiment(entry.title + " " + entry.get('summary', '')),
                'action_required': needs_action(clean_title + " " + entry.get('summary', ''))
            }
            articles.append(article)
        
        return articles
    
    except Exception as e:
        print(f"Error fetching news for '{topic}': {str(e)}")
        return []

def extract_source(title):
    """Extract source from Google News title format"""
    if ' - ' in title:
        return title.split(' - ')[-1]
    return "Unknown Source"

def categorize_news(text):
    """Categorize news article"""
    text_lower = text.lower()
    
    if any(comp in text_lower for comp in ['jetzero', 'boom', 'boeing', 'airbus', 'natilus']):
        return "COMPETITOR"
    elif any(word in text_lower for word in ['spirit aerosystems', 'triumph', 'supplier', 'supply chain']):
        return "SUPPLIER"
    elif any(word in text_lower for word in ['faa', 'certification', 'regulatory', 'compliance']):
        return "REGULATORY"
    elif any(word in text_lower for word in ['investment', 'funding', 'venture capital', 'series']):
        return "INVESTOR"
    else:
        return "INDUSTRY"

def extract_entities(text):
    """Extract relevant entities (companies/people) from text"""
    entities_found = []
    
    for entity in KEY_ENTITIES:
        if entity.lower() in text.lower():
            entities_found.append(entity)
    
    return entities_found

def analyze_sentiment(text):
    """Analyze sentiment using TextBlob (simple, no API needed)"""
    try:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        if polarity > 0.1:
            return "POSITIVE"
        elif polarity < -0.1:
            return "NEGATIVE"
        else:
            return "NEUTRAL"
    except:
        return "NEUTRAL"

def needs_action(text):
    """Determine if article requires immediate action"""
    text_lower = text.lower()
    
    # Action triggers
    action_keywords = [
        'bankruptcy', 'acquisition', 'raises', 'funding', 
        'certification approved', 'faa approval', 'contract awarded',
        'partnership', 'merger', 'closes', 'hires', 'ceo'
    ]
    
    return any(keyword in text_lower for keyword in action_keywords)

def save_news_to_supabase(articles):
    """Save news articles to Supabase"""
    saved_count = 0
    
    for article in articles:
        try:
            result = supabase.table('intelligence_feed').upsert(
                article,
                on_conflict='url'
            ).execute()
            saved_count += 1
        except Exception as e:
            print(f"Error saving article: {str(e)}")
    
    print(f"Saved {saved_count}/{len(articles)} articles to database")
    return saved_count

def run_news_scraper():
    """Main function to run news scraper"""
    print("="*60)
    print("  NATILUS NEWS INTELLIGENCE MONITOR")
    print("  Google News RSS Aggregator")
    print("="*60)
    print()
    
    all_articles = []
    
    for topic in NEWS_TOPICS:
        print(f"\n{'='*60}")
        print(f"Topic: {topic}")
        print(f"{'='*60}")
        
        articles = get_google_news_rss(topic, num_results=5)
        all_articles.extend(articles)
        
        print(f"Found {len(articles)} articles")
        time.sleep(1)  # Be respectful to Google's servers
    
    # Remove duplicates by URL
    unique_articles = {a['url']: a for a in all_articles}.values()
    unique_articles = list(unique_articles)
    
    print(f"\n{'='*60}")
    print(f"Total unique articles: {len(unique_articles)}")
    print(f"{'='*60}")
    
    if unique_articles:
        save_news_to_supabase(unique_articles)
        
        # Show action-required articles
        action_items = [a for a in unique_articles if a['action_required']]
        if action_items:
            print(f"\n⚡ ACTION REQUIRED: {len(action_items)} articles")
            for a in action_items[:5]:
                print(f"  - {a['headline'][:60]}... ({a['category']})")
        
        # Show competitor news
        competitor_news = [a for a in unique_articles if a['category'] == 'COMPETITOR']
        if competitor_news:
            print(f"\n🎯 COMPETITOR NEWS: {len(competitor_news)} articles")
            for a in competitor_news[:3]:
                entities_str = ", ".join(a['entities']) if a['entities'] else "N/A"
                print(f"  - {a['headline'][:50]}... [{entities_str}]")

if __name__ == "__main__":
    run_news_scraper()
