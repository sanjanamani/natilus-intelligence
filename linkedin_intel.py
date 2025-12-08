"""
LinkedIn Intelligence V2 - Serper API
Find aerospace talent and track competitor employee movements
"""

import requests
from datetime import datetime, timedelta
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import time

load_dotenv()

# Supabase setup
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Search queries for talent
TALENT_SEARCHES = [
    'site:linkedin.com "aerospace engineer" "open to work"',
    'site:linkedin.com "aircraft designer" Boeing',
    'site:linkedin.com "composite engineer" Airbus',
    'site:linkedin.com "aerodynamics engineer" "seeking opportunities"',
    'site:linkedin.com "FAA certification specialist"',
    'site:linkedin.com "manufacturing engineer" Spirit AeroSystems',
    'site:linkedin.com "propulsion engineer" "blended wing"'
]

# Target companies for talent poaching
TARGET_COMPANIES = [
    "Boeing",
    "Airbus",
    "Lockheed Martin",
    "Northrop Grumman",
    "Spirit AeroSystems",
    "SpaceX",
    "Blue Origin"
]

def search_linkedin(query):
    """Search LinkedIn using Serper Google Search API"""
    url = "https://google.serper.dev/search"
    
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    
    payload = {
        'q': query,
        'num': 10
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        data = response.json()
        
        return data.get('organic', [])
    
    except Exception as e:
        print(f"Error searching for '{query}': {str(e)}")
        return []

def extract_talent_info(result):
    """Extract talent information from search result"""
    title = result.get('title', '')
    snippet = result.get('snippet', '')
    link = result.get('link', '')
    
    # Extract name (usually first part of title before '-' or '|')
    name = title.split(' - ')[0].split(' | ')[0].strip()
    
    # Extract current company and title from snippet
    current_title = "Unknown"
    current_company = "Unknown"
    
    # Try to parse from snippet
    for company in TARGET_COMPANIES:
        if company in snippet or company in title:
            current_company = company
            break
    
    # Extract title keywords
    title_keywords = ['engineer', 'manager', 'director', 'specialist', 'architect', 'designer']
    for keyword in title_keywords:
        if keyword.lower() in snippet.lower():
            # Try to extract full title around the keyword
            words = snippet.split()
            for i, word in enumerate(words):
                if keyword.lower() in word.lower():
                    # Get surrounding context
                    start = max(0, i-2)
                    end = min(len(words), i+3)
                    current_title = ' '.join(words[start:end])
                    break
            break
    
    # Check for "open to work" signals
    open_to_work = any(phrase in snippet.lower() for phrase in 
                      ['open to work', 'seeking opportunities', 'looking for', 'available'])
    
    # Extract skills from snippet
    skills = []
    skill_keywords = ['aerospace', 'composite', 'CAD', 'CATIA', 'CFD', 'FEA', 'Python', 'C++']
    for skill in skill_keywords:
        if skill.lower() in snippet.lower():
            skills.append(skill)
    
    # Assess priority
    priority = assess_talent_priority(current_title, current_company, open_to_work)
    
    return {
        'name': name,
        'current_company': current_company,
        'current_title': current_title,
        'linkedin_url': link,
        'location': "Unknown",  # Would need to scrape profile for this
        'skills': skills,
        'open_to_work': open_to_work,
        'priority': priority,
        'notes': snippet[:200],
        'discovered_at': datetime.now().isoformat(),
        'action_deadline': (datetime.now() + timedelta(days=7)).date().isoformat()
    }

def assess_talent_priority(title, company, open_to_work):
    """Assess talent priority"""
    score = 0
    
    title_lower = title.lower()
    
    # Experience level
    if any(word in title_lower for word in ['senior', 'principal', 'lead', 'staff']):
        score += 3
    elif any(word in title_lower for word in ['director', 'vp', 'chief']):
        score += 4
    
    # From target company
    if company in TARGET_COMPANIES:
        score += 2
    
    # Open to work
    if open_to_work:
        score += 3
    
    # Critical skills
    if any(skill in title_lower for skill in ['composite', 'aerodynamics', 'certification', 'bwb']):
        score += 2
    
    if score >= 6:
        return "CRITICAL"
    elif score >= 4:
        return "HIGH"
    elif score >= 2:
        return "MEDIUM"
    else:
        return "LOW"

def save_talents_to_supabase(talents):
    """Save talent leads to Supabase"""
    saved_count = 0
    
    for talent in talents:
        try:
            result = supabase.table('talent_leads').upsert(
                talent,
                on_conflict='linkedin_url'
            ).execute()
            saved_count += 1
        except Exception as e:
            print(f"Error saving talent {talent['name']}: {str(e)}")
    
    print(f"Saved {saved_count}/{len(talents)} talent leads to database")
    return saved_count

def run_linkedin_intel():
    """Main function to discover talent on LinkedIn"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║         NATILUS LINKEDIN INTELLIGENCE V2                 ║
    ║              Serper API Talent Discovery                 ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    if not SERPER_API_KEY or SERPER_API_KEY == "your_serper_key":
        print("❌ ERROR: SERPER_API_KEY not set in .env")
        print("Get free key at: https://serper.dev")
        return
    
    all_talents = []
    
    for query in TALENT_SEARCHES:
        print(f"\n{'='*60}")
        print(f"Searching: {query}")
        print(f"{'='*60}")
        
        results = search_linkedin(query)
        
        for result in results:
            talent = extract_talent_info(result)
            all_talents.append(talent)
        
        print(f"Found {len(results)} potential candidates")
        time.sleep(1)  # Be respectful to API
    
    # Remove duplicates by LinkedIn URL
    unique_talents = {t['linkedin_url']: t for t in all_talents}.values()
    unique_talents = list(unique_talents)
    
    print(f"\n{'='*60}")
    print(f"Total unique candidates: {len(unique_talents)}")
    print(f"{'='*60}")
    
    if unique_talents:
        save_talents_to_supabase(unique_talents)
        
        # Show high-priority candidates
        high_priority = [t for t in unique_talents if t['priority'] in ['CRITICAL', 'HIGH']]
        if high_priority:
            print(f"\n🎯 HIGH PRIORITY CANDIDATES: {len(high_priority)}")
            for t in high_priority[:5]:
                print(f"  - {t['name']}")
                print(f"    Company: {t['current_company']}")
                print(f"    Title: {t['current_title']}")
                print(f"    Open to Work: {t['open_to_work']}")
                print(f"    Priority: {t['priority']}")
                print()

if __name__ == "__main__":
    run_linkedin_intel()
