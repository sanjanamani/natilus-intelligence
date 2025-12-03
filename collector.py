# collector.py
import json
import random
from datetime import datetime, timedelta
from supabase import create_client, Client
import time

# Load your Supabase credentials
SUPABASE_URL = "https://npvpsovgkxxulcrxnmju.supabase.co"  # Replace with your URL
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5wdnBzb3Zna3h4dWxjcnhubWp1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQ3MTI2NDQsImV4cCI6MjA4MDI4ODY0NH0.YGtLYWdIXZtbgWMDHCdG2kpiOgyT-hhg7H_a1TtUQFw"  # Replace with your key

# Initialize Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def generate_mock_talent():
    """Generate realistic talent data"""
    
    first_names = ["James", "Maria", "Robert", "Jennifer", "Michael", "Linda", "David", "Patricia", "Richard", "Barbara"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
    companies = ["Boeing", "Spirit AeroSystems", "Textron", "Lockheed Martin", "Northrop Grumman"]
    titles = ["Senior Composite Engineer", "Manufacturing Engineer", "Flight Test Engineer", 
              "Certification Specialist", "Aerodynamics Engineer", "Quality Engineer",
              "Structural Engineer", "Systems Engineer"]
    locations = ["Seattle, WA", "Wichita, KS", "Everett, WA", "Fort Worth, TX", "Los Angeles, CA"]
    skills_list = [
        "Carbon fiber composites, 787 program, Autoclave processing",
        "FAA Part 23/25, Certification, Compliance",
        "Manufacturing optimization, Lean, Six Sigma",
        "Flight testing, Data analysis, Instrumentation",
        "Aerodynamics, CFD, Wind tunnel testing",
        "Quality control, AS9100, Root cause analysis"
    ]
    
    talent = []
    for i in range(20):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        talent.append({
            "name": name,
            "current_company": random.choice(companies),
            "title": random.choice(titles),
            "location": random.choice(locations),
            "years_experience": random.randint(5, 20),
            "skills": random.choice(skills_list),
            "is_open_to_work": random.choice([True, True, False]),  # 66% open
            "priority_score": random.randint(70, 95),
            "risk_of_poaching": random.choice(["HIGH", "MEDIUM", "LOW"]),
            "linkedin_url": f"linkedin.com/in/{name.lower().replace(' ', '-')}",
            "layoff_date": (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d')
        })
    
    return talent

def add_talent_to_database():
    """Add talent to Supabase"""
    print("🚀 Adding talent to database...")
    
    talent = generate_mock_talent()
    
    # Insert to Supabase
    try:
        result = supabase.table('aerospace_talent').insert(talent).execute()
        print(f"✅ Added {len(talent)} talent profiles")
    except Exception as e:
        print(f"❌ Error: {e}")

def add_competitor_intelligence():
    """Add competitor moves"""
    print("📊 Adding competitor intelligence...")
    
    moves = [
        {
            "company": "JetZero",
            "news_type": "Patent Filing",
            "details": "Filed 3 new BWB control system patents",
            "impact_on_natilus": "HIGH - Advanced control systems critical for BWB"
        },
        {
            "company": "Archer",
            "news_type": "Facility Expansion",
            "details": "Opening 350,000 sqft facility in Georgia",
            "impact_on_natilus": "LOW - Different market segment"
        }
    ]
    
    try:
        result = supabase.table('competitor_moves').insert(moves).execute()
        print(f"✅ Added {len(moves)} competitor updates")
    except Exception as e:
        print(f"❌ Error: {e}")

def add_supply_chain_alerts():
    """Add supply chain risk updates"""
    print("🏭 Adding supply chain updates...")
    
    risks = [
        {
            "supplier": "Toray Industries",
            "risk_level": "LOW",
            "issue": "Expanding US production capacity",
            "alternative_suppliers": "Hexcel, SGL Carbon"
        }
    ]
    
    try:
        result = supabase.table('supply_chain_risks').insert(risks).execute()
        print(f"✅ Added {len(risks)} supply chain updates")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════╗
    ║   NATILUS INTELLIGENCE DATA COLLECTOR    ║
    ╚══════════════════════════════════════════╝
    """)
    
    # Run all collectors
    add_talent_to_database()
    add_competitor_intelligence()
    add_supply_chain_alerts()
    
    print("\n✅ Data collection complete!")
    print("📊 Check your Supabase dashboard to verify data")