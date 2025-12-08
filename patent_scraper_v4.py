"""
Patent Intelligence Scraper V4 - Google Patents Public Data
Works with Python 3.14, no external patent libraries needed
Uses Google Patents Public Datasets
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import time

load_dotenv()

# Supabase setup
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Patent search queries
PATENT_SEARCHES = [
    "blended wing body aircraft",
    "BWB cargo aircraft",
    "flying wing design",
    "cargo aircraft door system",
    "fuel efficient wide body",
    "composite aircraft fuselage",
]

# Companies to monitor
TARGET_ASSIGNEES = [
    "Boeing",
    "Airbus",
    "Lockheed",
    "Northrop",
    "Aurora",
    "JetZero"
]

def search_google_patents(query, max_results=10):
    """
    Scrape Google Patents search results
    """
    print(f"Searching Google Patents for: {query}")
    
    try:
        # Google Patents search URL
        base_url = "https://patents.google.com/"
        search_url = f"{base_url}?q={query.replace(' ', '+')}&oq={query.replace(' ', '+')}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(search_url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        patents = []
        
        # Find patent result articles
        results = soup.find_all('search-result-item', limit=max_results)
        
        for result in results:
            try:
                # Extract patent number
                patent_num_elem = result.find('span', {'itemprop': 'publicationNumber'})
                if not patent_num_elem:
                    continue
                patent_number = patent_num_elem.text.strip()
                
                # Extract title
                title_elem = result.find('span', {'itemprop': 'title'})
                title = title_elem.text.strip() if title_elem else "Unknown Title"
                
                # Extract assignee
                assignee_elem = result.find('span', {'itemprop': 'assigneeOriginal'})
                assignee = assignee_elem.text.strip() if assignee_elem else "Unknown"
                
                # Extract date
                date_elem = result.find('time', {'itemprop': 'publicationDate'})
                pub_date = date_elem.get('datetime') if date_elem else None
                
                # Check if from target company
                is_target = any(target.lower() in assignee.lower() for target in TARGET_ASSIGNEES)
                
                patent = {
                    'patent_number': patent_number,
                    'title': title[:500],
                    'assignee': assignee,
                    'filing_date': pub_date,
                    'publication_date': pub_date,
                    'abstract': f"Patent for {query}",
                    'url': f"https://patents.google.com/patent/{patent_number}",
                    'technology_area': categorize_technology(title, query),
                    'competitive_threat': assess_threat(title, assignee, is_target),
                }
                
                patents.append(patent)
                
            except Exception as e:
                print(f"Error parsing patent: {str(e)}")
                continue
        
        return patents
    
    except Exception as e:
        print(f"Error searching patents for '{query}': {str(e)}")
        return []

def categorize_technology(title, query):
    """Categorize patent by technology area"""
    text = (title + " " + query).lower()
    
    if any(term in text for term in ['blended wing', 'bwb', 'flying wing']):
        return "BWB Design"
    elif 'cargo' in text and 'door' in text:
        return "Cargo Systems"
    elif any(term in text for term in ['composite', 'material', 'structure']):
        return "Materials/Structures"
    elif any(term in text for term in ['propulsion', 'engine', 'thrust']):
        return "Propulsion"
    elif any(term in text for term in ['fuel', 'efficiency', 'consumption']):
        return "Fuel Efficiency"
    else:
        return "General Aerospace"

def assess_threat(title, assignee, is_target_company):
    """Assess competitive threat level"""
    title_lower = title.lower()
    
    # HIGH threat: BWB patents from major competitors
    if is_target_company:
        if any(term in title_lower for term in ['blended wing', 'bwb', 'flying wing']):
            return "HIGH"
        elif 'cargo' in title_lower:
            return "HIGH"
        return "MEDIUM"
    
    return "LOW"

def save_patents_to_supabase(patents):
    """Save patents to Supabase"""
    saved_count = 0
    
    for patent in patents:
        try:
            result = supabase.table('patents').upsert(
                patent,
                on_conflict='patent_number'
            ).execute()
            saved_count += 1
        except Exception as e:
            print(f"Error saving patent {patent['patent_number']}: {str(e)}")
    
    print(f"Saved {saved_count}/{len(patents)} patents to database")
    return saved_count

def run_patent_scraper():
    """Main function to run patent scraper"""
    print("="*60)
    print("  NATILUS PATENT INTELLIGENCE V4")
    print("  Google Patents Web Scraper")
    print("  Python 3.14 Compatible")
    print("="*60)
    print()
    
    all_patents = []
    
    for query in PATENT_SEARCHES:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print(f"{'='*60}")
        
        patents = search_google_patents(query, max_results=10)
        all_patents.extend(patents)
        
        print(f"Found {len(patents)} patents")
        time.sleep(2)  # Be respectful to Google
    
    # Remove duplicates by patent_number
    unique_patents = {p['patent_number']: p for p in all_patents if p.get('patent_number')}.values()
    unique_patents = list(unique_patents)
    
    print(f"\n{'='*60}")
    print(f"Total unique patents: {len(unique_patents)}")
    print(f"{'='*60}")
    
    if unique_patents:
        save_patents_to_supabase(unique_patents)
        
        # Show high-threat patents
        high_threat = [p for p in unique_patents if p['competitive_threat'] == 'HIGH']
        if high_threat:
            print(f"\n🚨 HIGH THREAT PATENTS: {len(high_threat)}")
            for p in high_threat[:5]:
                print(f"  - {p['title'][:60]}... ({p['assignee']})")
    else:
        print("\n⚠️  No patents found. Google Patents may have changed their HTML structure.")

if __name__ == "__main__":
    run_patent_scraper()
