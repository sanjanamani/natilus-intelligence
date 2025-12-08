"""
Natilus Intelligence Platform
Master data collection script
"""

import os
import sys
import json
import pandas as pd
import subprocess
from datetime import datetime
from dotenv import load_dotenv

# Load environment
load_dotenv()

print("="*70)
print("")
print("  NATILUS INTELLIGENCE PLATFORM")
print("  Strategic Intelligence Collection")
print("")
print("="*70)
print()

# Verify environment
required_vars = ['SUPABASE_URL', 'SUPABASE_KEY']
missing = [var for var in required_vars if not os.getenv(var)]

if missing:
    print("❌ ERROR: Missing required environment variables:")
    for var in missing:
        print(f"   - {var}")
    print("\nPlease configure your .env file.")
    sys.exit(1)

print("✅ Environment configured\n")

# Create output directory
OUTPUT_DIR = "intelligence_reports"
os.makedirs(OUTPUT_DIR, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Run scrapers
scrapers = [
    ("news_scraper.py", "News Intelligence"),
    ("patent_scraper_v4.py", "Patent Intelligence"),
    ("job_scraper_v2.py", "Job Intelligence"),
]

print("🚀 Running Intelligence Collection...\n")

for script, name in scrapers:
    print(f"{'='*70}")
    print(f"Running: {name}")
    print(f"{'='*70}")
    
    try:
        # Run as subprocess to avoid encoding issues
        result = subprocess.run(
            [sys.executable, script],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode == 0:
            print(result.stdout)
            print(f"✅ {name} complete\n")
        else:
            print(result.stdout)
            print(result.stderr)
            print(f"⚠️  {name} had errors\n")
    
    except Exception as e:
        print(f"⚠️  {name} failed: {str(e)}\n")

# Export data from Supabase
print("\n" + "="*70)
print("📊 Exporting Data")
print("="*70)

try:
    from supabase import create_client
    
    supabase = create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_KEY")
    )
    
    tables = {
        'news': 'intelligence_feed',
        'jobs': 'competitor_jobs',
        'patents': 'patents',
        'talent': 'talent_leads',
        'suppliers': 'supplier_monitoring'
    }
    
    for name, table in tables.items():
        try:
            result = supabase.table(table).select("*").execute()
            data = result.data
            
            if data:
                # Export to JSON
                json_file = f"{OUTPUT_DIR}/{name}_{timestamp}.json"
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, default=str)
                
                # Export to CSV
                csv_file = f"{OUTPUT_DIR}/{name}_{timestamp}.csv"
                df = pd.DataFrame(data)
                df.to_csv(csv_file, index=False)
                
                # Export to Excel
                excel_file = f"{OUTPUT_DIR}/{name}_{timestamp}.xlsx"
                df.to_excel(excel_file, index=False)
                
                print(f"✅ Exported {len(data)} {name} records")
                print(f"   📄 JSON: {json_file}")
                print(f"   📊 CSV: {csv_file}")
                print(f"   📗 Excel: {excel_file}\n")
            else:
                print(f"⚠️  No {name} data found\n")
        
        except Exception as e:
            print(f"⚠️  Could not export {name}: {str(e)}\n")
    
    print("="*70)
    print("✅ COLLECTION COMPLETE")
    print("="*70)
    print(f"\n📂 Reports saved to: {os.path.abspath(OUTPUT_DIR)}/")
    print("\nYou can:")
    print("  • Open CSV files in Excel")
    print("  • Open JSON files in any text editor")
    print("  • View Excel files for formatted data")
    
except Exception as e:
    print(f"❌ Export failed: {str(e)}")

print("\n" + "="*70)
