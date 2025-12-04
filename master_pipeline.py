# master_pipeline.py
import os
import sys
from datetime import datetime
import time
from dotenv import load_dotenv

# Import all our trackers
from warn_tracker import WARNTracker
from patent_tracker import PatentTracker
from news_tracker import NewsTracker
from github_scout import GithubScout
from contract_tracker import ContractTracker

load_dotenv()

class NatilusMasterPipeline:
    def __init__(self):
        print("""
        ╔══════════════════════════════════════════╗
        ║   NATILUS INTELLIGENCE PIPELINE v2.0     ║
        ║          Real-Time Data Collection        ║
        ╚══════════════════════════════════════════╝
        """)
        
        self.warn = WARNTracker()
        self.patents = PatentTracker()
        self.news = NewsTracker()
        self.github = GithubScout()
        self.contracts = ContractTracker()
        
    def run_full_intelligence(self):
        """Run all intelligence gathering"""
        start_time = datetime.now()
        print(f"\n🚀 Starting Intelligence Run: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)
        
        results = {
            'layoffs': [],
            'patents': [],
            'news': [],
            'github_talent': [],
            'contracts': []
        }
        
        # 1. WARN Layoffs
        print("\n📊 PHASE 1: Layoff Tracking")
        print("-" * 30)
        try:
            results['layoffs'] = self.warn.run()
        except Exception as e:
            print(f"❌ Layoff tracking failed: {e}")
        
        # 2. Patents
        print("\n📋 PHASE 2: Patent Intelligence")
        print("-" * 30)
        try:
            results['patents'] = self.patents.run()
        except Exception as e:
            print(f"❌ Patent tracking failed: {e}")
        
        # 3. News
        print("\n📰 PHASE 3: News Monitoring")
        print("-" * 30)
        try:
            results['news'] = self.news.run()
        except Exception as e:
            print(f"❌ News tracking failed: {e}")
        
        # 4. GitHub Talent
        print("\n👨‍💻 PHASE 4: GitHub Talent Scout")
        print("-" * 30)
        try:
            results['github_talent'] = self.github.run()
        except Exception as e:
            print(f"❌ GitHub scout failed: {e}")
        
        # 5. Federal Contracts
        print("\n💰 PHASE 5: Contract Intelligence")
        print("-" * 30)
        try:
            results['contracts'] = self.contracts.run()
        except Exception as e:
            print(f"❌ Contract tracking failed: {e}")
        
        # Generate summary
        print("\n" + "=" * 50)
        print("📊 INTELLIGENCE SUMMARY")
        print("=" * 50)
        
        total_items = sum(len(v) for v in results.values())
        
        print(f"✅ Layoffs tracked: {len(results['layoffs'])}")
        print(f"✅ Patents found: {len(results['patents'])}")
        print(f"✅ News items: {len(results['news'])}")
        print(f"✅ GitHub talent: {len(results['github_talent'])}")
        print(f"✅ Contracts: {len(results['contracts'])}")
        print(f"\n🎯 TOTAL INTELLIGENCE ITEMS: {total_items}")
        
        # Calculate runtime
        end_time = datetime.now()
        duration = (end_time - start_time).seconds
        print(f"⏱️ Runtime: {duration} seconds")
        
        # Generate insights
        self.generate_executive_insights(results)
        
        return results
    
    def generate_executive_insights(self, results):
        """Generate actionable insights for Nolan"""
        print("\n" + "=" * 50)
        print("🎯 EXECUTIVE INSIGHTS FOR NATILUS")
        print("=" * 50)
        
        # Urgent actions
        if len(results['layoffs']) > 10:
            print(f"\n🚨 URGENT: {len(results['layoffs'])} aerospace professionals available from layoffs")
            print("   ACTION: Schedule recruiting trip to Seattle/Wichita THIS WEEK")
        
        # Patent threats
        jetzero_patents = [p for p in results['patents'] if 'JetZero' in str(p.get('company', ''))]
        if jetzero_patents:
            print(f"\n⚠️ THREAT: JetZero filed {len(jetzero_patents)} new patents")
            print("   ACTION: Review for IP conflicts immediately")
        
        # Funding landscape
        big_contracts = [c for c in results['contracts'] if 'HIGH' in str(c.get('impact_on_natilus', ''))]
        if big_contracts:
            print(f"\n💰 COMPETITION: {len(big_contracts)} major contracts to competitors")
            print("   ACTION: Accelerate Series A to maintain momentum")
        
        # Talent opportunity
        if results['github_talent']:
            print(f"\n💎 OPPORTUNITY: {len(results['github_talent'])} engineers found on GitHub")
            print("   ACTION: Reach out before competitors do")
        
        print("\n" + "=" * 50)
        print("✅ Intelligence gathering complete!")
        print("Check your Streamlit dashboard for real-time updates.")

def main():
    """Run the pipeline"""
    pipeline = NatilusMasterPipeline()
    
    # Check for required API keys
    if not os.getenv('SUPABASE_URL'):
        print("❌ ERROR: Missing SUPABASE_URL in .env file")
        return
    
    if not os.getenv('NEWSAPI_KEY'):
        print("⚠️ WARNING: No NewsAPI key found. Get one free at newsapi.org")
        print("   News tracking will be limited.\n")
    
    # Run the full pipeline
    results = pipeline.run_full_intelligence()
    
    print("\n🔄 Pipeline will run every 6 hours in production")
    print("Press Ctrl+C to stop")
    
    # Continuous run (optional)
    # while True:
    #     time.sleep(21600)  # 6 hours
    #     results = pipeline.run_full_intelligence()

if __name__ == "__main__":
    main()