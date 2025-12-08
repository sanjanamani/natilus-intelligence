"""
Job Scraper V2 - REAL CAREER PAGES
Scrapes actual company career pages for competitor intelligence
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import time
import re

load_dotenv()

# Supabase setup
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Company career pages to scrape
COMPANY_CAREER_PAGES = {
    "JetZero": {
        "url": "https://jobs.lever.co/jetzero",
        "type": "lever"
    },
    "Boom Supersonic": {
        "url": "https://boards.greenhouse.io/boomsupersonic",
        "type": "greenhouse"
    },
    "Boeing": {
        "url": "https://jobs.boeing.com/search-jobs",
        "type": "custom"
    },
    "Airbus": {
        "url": "https://ag.wd3.myworkdayjobs.com/Airbus",
        "type": "workday"
    }
}

def scrape_lever_jobs(company_name, url):
    """Scrape Lever-hosted career pages (JetZero uses this)"""
    print(f"Scraping Lever jobs for {company_name}...")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        jobs = []
        
        # Lever uses <div class="posting"> for each job
        job_postings = soup.find_all('div', class_='posting')
        
        for posting in job_postings[:20]:  # Limit to 20 most recent
            try:
                # Extract title
                title_elem = posting.find('h5')
                if not title_elem:
                    continue
                title = title_elem.text.strip()
                
                # Extract location
                location_elem = posting.find('span', class_='sort-by-location')
                location = location_elem.text.strip() if location_elem else "Remote"
                
                # Extract URL
                link_elem = posting.find('a', class_='posting-title')
                job_url = link_elem['href'] if link_elem and 'href' in link_elem.attrs else url
                
                # Generate unique job ID
                job_id = f"{company_name.lower().replace(' ', '-')}-{hash(title + location) % 100000}"
                
                job = {
                    'job_id': job_id,
                    'company': company_name,
                    'title': title,
                    'location': location,
                    'description': f"{title} - {location}",
                    'posted_date': datetime.now().isoformat(),
                    'url': job_url,
                    'strategic_signal': categorize_job(title),
                    'priority': assess_priority(title, company_name)
                }
                
                jobs.append(job)
                
            except Exception as e:
                print(f"Error parsing job posting: {str(e)}")
                continue
        
        return jobs
    
    except Exception as e:
        print(f"Error scraping Lever jobs for {company_name}: {str(e)}")
        return []

def scrape_greenhouse_jobs(company_name, url):
    """Scrape Greenhouse-hosted career pages (Boom uses this)"""
    print(f"Scraping Greenhouse jobs for {company_name}...")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        jobs = []
        
        # Greenhouse uses <div class="opening"> for each job
        job_postings = soup.find_all('div', class_='opening')
        
        for posting in job_postings[:20]:
            try:
                # Extract title
                title_elem = posting.find('a')
                if not title_elem:
                    continue
                title = title_elem.text.strip()
                
                # Extract location
                location_elem = posting.find('span', class_='location')
                location = location_elem.text.strip() if location_elem else "Remote"
                
                # Extract URL
                job_url = title_elem['href'] if 'href' in title_elem.attrs else url
                if not job_url.startswith('http'):
                    job_url = f"https://boards.greenhouse.io{job_url}"
                
                job_id = f"{company_name.lower().replace(' ', '-')}-{hash(title + location) % 100000}"
                
                job = {
                    'job_id': job_id,
                    'company': company_name,
                    'title': title,
                    'location': location,
                    'description': f"{title} - {location}",
                    'posted_date': datetime.now().isoformat(),
                    'url': job_url,
                    'strategic_signal': categorize_job(title),
                    'priority': assess_priority(title, company_name)
                }
                
                jobs.append(job)
                
            except Exception as e:
                print(f"Error parsing job posting: {str(e)}")
                continue
        
        return jobs
    
    except Exception as e:
        print(f"Error scraping Greenhouse jobs for {company_name}: {str(e)}")
        return []

def scrape_generic_jobs(company_name, url):
    """Generic scraper for other career pages"""
    print(f"Attempting generic scrape for {company_name}...")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        jobs = []
        
        # Look for common job listing patterns
        # Try to find links with job-related keywords
        job_links = soup.find_all('a', href=True)
        
        for link in job_links[:20]:
            href = link.get('href', '')
            text = link.text.strip()
            
            # Filter for likely job postings
            if len(text) > 10 and any(keyword in text.lower() for keyword in 
                ['engineer', 'manager', 'director', 'specialist', 'analyst', 'designer']):
                
                job_id = f"{company_name.lower().replace(' ', '-')}-{hash(text) % 100000}"
                
                job = {
                    'job_id': job_id,
                    'company': company_name,
                    'title': text[:200],
                    'location': "Unknown",
                    'description': text,
                    'posted_date': datetime.now().isoformat(),
                    'url': href if href.startswith('http') else url,
                    'strategic_signal': categorize_job(text),
                    'priority': assess_priority(text, company_name)
                }
                
                jobs.append(job)
        
        return jobs
    
    except Exception as e:
        print(f"Error in generic scrape for {company_name}: {str(e)}")
        return []

def categorize_job(job_title):
    """Determine strategic signal from job title"""
    title_lower = job_title.lower()
    
    if any(word in title_lower for word in ['manufacturing', 'production', 'factory', 'plant', 'assembly']):
        return "Manufacturing Scale-up"
    elif any(word in title_lower for word in ['engineer', 'design', 'architect', 'technical', 'software']):
        return "Engineering Expansion"
    elif any(word in title_lower for word in ['certification', 'regulatory', 'compliance', 'faa', 'quality']):
        return "Certification Push"
    elif any(word in title_lower for word in ['supply chain', 'procurement', 'logistics', 'sourcing']):
        return "Supply Chain Build"
    elif any(word in title_lower for word in ['sales', 'business development', 'commercial', 'account']):
        return "Go-to-Market Prep"
    elif any(word in title_lower for word in ['finance', 'accounting', 'controller', 'cfo']):
        return "Financial Scaling"
    else:
        return "General Hiring"

def assess_priority(job_title, company):
    """Assess priority based on job and company"""
    title_lower = job_title.lower()
    
    # Critical roles that indicate major moves
    critical_roles = ['vp', 'vice president', 'director', 'head of', 'chief', 'lead engineer', 'principal']
    high_value_roles = ['certification', 'faa', 'composite', 'aerodynamics', 'propulsion', 'manufacturing']
    
    if any(role in title_lower for role in critical_roles):
        return "HIGH"
    elif any(role in title_lower for role in high_value_roles):
        return "HIGH"
    elif company in ["JetZero", "Boom Supersonic"]:  # Direct competitors
        return "MEDIUM"
    else:
        return "LOW"

def save_jobs_to_supabase(jobs):
    """Save jobs to Supabase"""
    saved_count = 0
    
    for job in jobs:
        try:
            result = supabase.table('competitor_jobs').upsert(
                job,
                on_conflict='job_id'
            ).execute()
            saved_count += 1
        except Exception as e:
            print(f"Error saving job {job['job_id']}: {str(e)}")
    
    print(f"Saved {saved_count}/{len(jobs)} jobs to database")
    return saved_count

def run_job_scraper():
    """Main function to run the job scraper"""
    print("="*60)
    print("  NATILUS JOB INTELLIGENCE V2")
    print("  Real Career Page Scraper")
    print("="*60)
    print()
    
    all_jobs = []
    
    for company, config in COMPANY_CAREER_PAGES.items():
        print(f"\n{'='*60}")
        print(f"Scraping: {company}")
        print(f"{'='*60}")
        
        jobs = []
        
        if config['type'] == 'lever':
            jobs = scrape_lever_jobs(company, config['url'])
        elif config['type'] == 'greenhouse':
            jobs = scrape_greenhouse_jobs(company, config['url'])
        else:
            jobs = scrape_generic_jobs(company, config['url'])
        
        all_jobs.extend(jobs)
        print(f"Found {len(jobs)} jobs")
        
        time.sleep(2)  # Be respectful to servers
    
    print(f"\n{'='*60}")
    print(f"Total jobs collected: {len(all_jobs)}")
    print(f"{'='*60}")
    
    if all_jobs:
        save_jobs_to_supabase(all_jobs)
        
        # Show high-priority jobs
        high_priority = [j for j in all_jobs if j['priority'] == 'HIGH']
        if high_priority:
            print(f"\n🎯 HIGH PRIORITY JOBS: {len(high_priority)}")
            for j in high_priority[:5]:
                print(f"  - {j['title'][:50]}... ({j['company']})")

if __name__ == "__main__":
    run_job_scraper()
