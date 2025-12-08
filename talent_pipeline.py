"""
Enhanced Talent Pipeline Intelligence
LinkedIn + GitHub integration with hiring recommendations
"""

import requests
from datetime import datetime
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import time

load_dotenv()

# Supabase setup
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Optional: Serper API for LinkedIn search
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# Talent search queries with hiring context
TALENT_SEARCHES = [
    {
        "query": "aerospace engineer composite structures 'open to work'",
        "role": "Senior Composite Structures Engineer",
        "why_good_fit": "BWB aircraft requires advanced composite expertise for large-scale fuselage manufacturing",
        "priority": "CRITICAL",
        "department": "Engineering",
        "location": "San Diego, CA"
    },
    {
        "query": "aircraft manufacturing engineer Boeing Airbus",
        "role": "Manufacturing Engineer - Assembly",
        "why_good_fit": "Experience scaling aircraft production critical for Natilus manufacturing ramp-up",
        "priority": "HIGH",
        "department": "Manufacturing",
        "location": "San Diego, CA"
    },
    {
        "query": "FAA certification specialist cargo aircraft",
        "role": "Certification Manager",
        "why_good_fit": "FAA certification pathway for BWB cargo aircraft is complex, need experienced specialist",
        "priority": "CRITICAL",
        "department": "Regulatory",
        "location": "Remote OK"
    },
    {
        "query": "aerospace supply chain manager",
        "role": "Supply Chain Director",
        "why_good_fit": "Managing supplier relationships for composite materials and cargo systems",
        "priority": "HIGH",
        "department": "Operations",
        "location": "San Diego, CA"
    },
    {
        "query": "'cargo aircraft' 'door systems' engineer",
        "role": "Cargo Systems Engineer",
        "why_good_fit": "Specialized cargo loading/unloading systems are key differentiator for Natilus",
        "priority": "MEDIUM",
        "department": "Engineering",
        "location": "San Diego, CA"
    },
    {
        "query": "aerodynamics BWB 'blended wing body'",
        "role": "Aerodynamics Lead",
        "why_good_fit": "BWB aerodynamics is unique - need specialists with flying wing experience",
        "priority": "CRITICAL",
        "department": "Engineering",
        "location": "San Diego, CA"
    },
    {
        "query": "aircraft production manager Boom Spirit",
        "role": "Production Manager",
        "why_good_fit": "Scaling production from prototypes to serial manufacturing - startup aerospace experience ideal",
        "priority": "HIGH",
        "department": "Manufacturing",
        "location": "San Diego, CA"
    }
]

def search_linkedin_talent(query_obj):
    """Search LinkedIn via Serper API with hiring context"""
    if not SERPER_API_KEY:
        print("⚠️  SERPER_API_KEY not set - skipping LinkedIn search")
        return []
    
    try:
        url = "https://google.serper.dev/search"
        
        payload = {
            "q": f"{query_obj['query']} site:linkedin.com/in",
            "num": 10
        }
        
        headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        
        leads = []
        
        if 'organic' in data:
            for result in data['organic'][:10]:
                # Extract LinkedIn profile info
                name = result.get('title', '').split('|')[0].split('-')[0].strip()
                linkedin_url = result.get('link', '')
                snippet = result.get('snippet', '')
                
                # Score the candidate
                score = calculate_candidate_score(snippet, query_obj)
                
                lead = {
                    'name': name,
                    'linkedin_url': linkedin_url,
                    'current_role': extract_current_role(snippet),
                    'target_role': query_obj['role'],
                    'why_good_fit': query_obj['why_good_fit'],
                    'key_skills': extract_skills(snippet),
                    'priority': query_obj['priority'],
                    'score': score,
                    'department': query_obj['department'],
                    'preferred_location': query_obj['location'],
                    'outreach_notes': generate_outreach_notes(snippet, query_obj),
                    'discovered_date': datetime.now().isoformat()
                }
                
                leads.append(lead)
        
        return leads
    
    except Exception as e:
        print(f"Error searching LinkedIn: {str(e)}")
        return []

def calculate_candidate_score(snippet, query_obj):
    """Score candidate 0-100 based on relevance"""
    score = 0
    
    snippet_lower = snippet.lower()
    
    # Experience at target companies
    target_companies = ['boeing', 'airbus', 'lockheed', 'northrop', 'spirit', 'boom', 'jetzero']
    if any(company in snippet_lower for company in target_companies):
        score += 30
    
    # Relevant keywords
    relevant_keywords = ['composite', 'bwb', 'cargo', 'certification', 'manufacturing', 'aerospace']
    matches = sum(1 for keyword in relevant_keywords if keyword in snippet_lower)
    score += matches * 10
    
    # Open to work signal
    if 'open to' in snippet_lower or 'seeking' in snippet_lower:
        score += 20
    
    # Senior level
    if any(level in snippet_lower for level in ['senior', 'lead', 'principal', 'director', 'manager']):
        score += 10
    
    return min(score, 100)

def extract_current_role(snippet):
    """Extract current role from snippet"""
    # Simple extraction - could be enhanced
    lines = snippet.split('·')
    if len(lines) > 0:
        return lines[0].strip()
    return "Not specified"

def extract_skills(snippet):
    """Extract skills from snippet"""
    skill_keywords = [
        'composites', 'CAD', 'CATIA', 'manufacturing', 'FAA', 
        'certification', 'supply chain', 'program management',
        'aerodynamics', 'CFD', 'structural analysis'
    ]
    
    found_skills = [skill for skill in skill_keywords if skill.lower() in snippet.lower()]
    return ', '.join(found_skills) if found_skills else "See LinkedIn profile"

def generate_outreach_notes(snippet, query_obj):
    """Generate personalized outreach talking points"""
    notes = []
    
    # Mention their current company
    snippet_lower = snippet.lower()
    if 'boeing' in snippet_lower:
        notes.append("Boeing experience - familiar with commercial aircraft certification")
    if 'composite' in snippet_lower:
        notes.append("Composite structures background aligns with BWB fuselage design")
    if 'manufacturing' in snippet_lower:
        notes.append("Manufacturing experience critical for production scale-up")
    
    # Add role-specific notes
    notes.append(query_obj['why_good_fit'])
    
    return " | ".join(notes)

def save_leads_to_supabase(leads):
    """Save talent leads to database"""
    saved_count = 0
    
    for lead in leads:
        try:
            # Check if already exists
            existing = supabase.table('talent_leads').select('*').eq('linkedin_url', lead['linkedin_url']).execute()
            
            if existing.data:
                # Update
                supabase.table('talent_leads').update(lead).eq('linkedin_url', lead['linkedin_url']).execute()
            else:
                # Insert
                supabase.table('talent_leads').insert(lead).execute()
            
            saved_count += 1
        
        except Exception as e:
            print(f"Error saving lead {lead.get('name')}: {str(e)}")
    
    print(f"Saved {saved_count}/{len(leads)} leads to database")
    return saved_count

def run_talent_scraper():
    """Main function to run talent scraper"""
    print("="*60)
    print("  NATILUS TALENT PIPELINE INTELLIGENCE")
    print("  LinkedIn + Hiring Recommendations")
    print("="*60)
    print()
    
    if not SERPER_API_KEY:
        print("❌ SERPER_API_KEY not found in .env")
        print("Get free API key at: https://serper.dev")
        print("Add to .env: SERPER_API_KEY=your_key_here")
        return
    
    all_leads = []
    
    for search_obj in TALENT_SEARCHES:
        print(f"\n{'='*60}")
        print(f"Searching: {search_obj['role']}")
        print(f"Priority: {search_obj['priority']}")
        print(f"{'='*60}")
        
        leads = search_linkedin_talent(search_obj)
        all_leads.extend(leads)
        
        print(f"Found {len(leads)} candidates")
        
        # Show top candidate
        if leads:
            top = max(leads, key=lambda x: x['score'])
            print(f"\nTop Candidate: {top['name']} (Score: {top['score']}/100)")
            print(f"  Current Role: {top['current_role']}")
            print(f"  Why Good Fit: {top['why_good_fit']}")
        
        time.sleep(2)  # Rate limiting
    
    print(f"\n{'='*60}")
    print(f"Total candidates found: {len(all_leads)}")
    print(f"{'='*60}")
    
    if all_leads:
        save_leads_to_supabase(all_leads)
        
        # Show summary
        critical = [l for l in all_leads if l['priority'] == 'CRITICAL']
        high = [l for l in all_leads if l['priority'] == 'HIGH']
        
        print(f"\n🚨 CRITICAL PRIORITY: {len(critical)} candidates")
        print(f"⚠️  HIGH PRIORITY: {len(high)} candidates")
        
        print("\nTop 5 Candidates to Contact:")
        top_5 = sorted(all_leads, key=lambda x: x['score'], reverse=True)[:5]
        for i, lead in enumerate(top_5, 1):
            print(f"{i}. {lead['name']} - {lead['target_role']} (Score: {lead['score']}/100)")
            print(f"   LinkedIn: {lead['linkedin_url']}")

if __name__ == "__main__":
    run_talent_scraper()
