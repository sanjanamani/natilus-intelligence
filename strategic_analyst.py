"""
AI Strategic Analyst - Anthropic Claude API
Analyzes all collected intelligence and generates strategic insights for Natilus
"""

import anthropic
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from datetime import datetime
import json

load_dotenv()

# Supabase setup
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def fetch_all_intelligence():
    """Fetch all intelligence data from Supabase"""
    print("📊 Fetching all intelligence data...")
    
    data = {
        'jobs': [],
        'patents': [],
        'suppliers': [],
        'news': [],
        'talent': []
    }
    
    try:
        # Fetch competitor jobs
        jobs_result = supabase.table('competitor_jobs').select("*").limit(50).execute()
        data['jobs'] = jobs_result.data if jobs_result.data else []
        
        # Fetch patents
        patents_result = supabase.table('patents').select("*").limit(50).execute()
        data['patents'] = patents_result.data if patents_result.data else []
        
        # Fetch supplier data
        suppliers_result = supabase.table('supplier_monitoring').select("*").execute()
        data['suppliers'] = suppliers_result.data if suppliers_result.data else []
        
        # Fetch news
        news_result = supabase.table('intelligence_feed').select("*").limit(100).execute()
        data['news'] = news_result.data if news_result.data else []
        
        # Fetch talent
        talent_result = supabase.table('talent_leads').select("*").limit(50).execute()
        data['talent'] = talent_result.data if talent_result.data else []
        
        print(f"✅ Fetched: {len(data['jobs'])} jobs, {len(data['patents'])} patents, "
              f"{len(data['suppliers'])} suppliers, {len(data['news'])} news, {len(data['talent'])} talent")
        
        return data
    
    except Exception as e:
        print(f"❌ Error fetching intelligence: {str(e)}")
        return data

def analyze_with_claude(intelligence_data):
    """Use Claude to analyze intelligence and generate strategic insights"""
    print("\n🤖 Analyzing with Claude AI...")
    
    # Prepare context for Claude
    context = f"""You are a strategic intelligence analyst for Natilus, a company building blended wing body (BWB) cargo aircraft. 

Analyze the following intelligence data and provide strategic insights:

COMPETITOR JOBS ({len(intelligence_data['jobs'])} postings):
{json.dumps(intelligence_data['jobs'][:20], indent=2)}

PATENTS ({len(intelligence_data['patents'])} filings):
{json.dumps(intelligence_data['patents'][:20], indent=2)}

SUPPLIER HEALTH ({len(intelligence_data['suppliers'])} monitored):
{json.dumps(intelligence_data['suppliers'], indent=2)}

NEWS ARTICLES ({len(intelligence_data['news'])} articles):
{json.dumps(intelligence_data['news'][:30], indent=2)}

TALENT LEADS ({len(intelligence_data['talent'])} candidates):
{json.dumps(intelligence_data['talent'][:20], indent=2)}

Provide a strategic analysis in JSON format with these sections:
{{
  "executive_summary": "2-3 sentence overview of most critical findings",
  "critical_threats": [
    {{
      "threat": "description",
      "impact": "high/medium/low",
      "recommendation": "what Natilus should do",
      "urgency": "immediate/this_week/this_month"
    }}
  ],
  "opportunities": [
    {{
      "opportunity": "description",
      "value": "high/medium/low",
      "action": "what to do",
      "timeline": "when to act"
    }}
  ],
  "competitor_movements": [
    {{
      "company": "name",
      "activity": "what they're doing",
      "strategic_meaning": "what it means for Natilus",
      "response": "how to respond"
    }}
  ],
  "talent_recommendations": [
    {{
      "priority": "critical/high/medium",
      "who": "person or profile type",
      "why": "reason to hire",
      "deadline": "when to contact"
    }}
  ],
  "supply_chain_risks": [
    {{
      "supplier": "name",
      "risk_level": "critical/high/medium/low",
      "issue": "what's wrong",
      "mitigation": "what to do"
    }}
  ],
  "strategic_priorities": [
    "Priority 1 for this week",
    "Priority 2 for this week",
    "Priority 3 for this week"
  ]
}}

Focus on:
1. What competitor moves matter most to Natilus's BWB cargo strategy?
2. What patents threaten Natilus's IP position?
3. Which suppliers pose immediate risks?
4. What talent should be contacted urgently?
5. What strategic pivots or accelerations are needed?

Be specific, actionable, and prioritize by urgency."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            messages=[
                {"role": "user", "content": context}
            ]
        )
        
        # Extract JSON from response
        response_text = message.content[0].text
        
        # Try to parse JSON from response
        # Claude might wrap it in markdown code blocks
        if "```json" in response_text:
            json_str = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            json_str = response_text.split("```")[1].split("```")[0].strip()
        else:
            json_str = response_text
        
        analysis = json.loads(json_str)
        
        return analysis
    
    except Exception as e:
        print(f"❌ Error analyzing with Claude: {str(e)}")
        return {
            "executive_summary": "Error generating analysis",
            "critical_threats": [],
            "opportunities": [],
            "competitor_movements": [],
            "talent_recommendations": [],
            "supply_chain_risks": [],
            "strategic_priorities": []
        }

def save_analysis_to_supabase(analysis):
    """Save strategic analysis to Supabase"""
    print("\n💾 Saving analysis to database...")
    
    try:
        analysis_record = {
            'analysis_date': datetime.now().isoformat(),
            'executive_summary': analysis.get('executive_summary', ''),
            'critical_threats': json.dumps(analysis.get('critical_threats', [])),
            'opportunities': json.dumps(analysis.get('opportunities', [])),
            'competitor_movements': json.dumps(analysis.get('competitor_movements', [])),
            'talent_recommendations': json.dumps(analysis.get('talent_recommendations', [])),
            'supply_chain_risks': json.dumps(analysis.get('supply_chain_risks', [])),
            'strategic_priorities': json.dumps(analysis.get('strategic_priorities', []))
        }
        
        # Try to create strategic_analysis table if it doesn't exist
        result = supabase.table('strategic_analysis').insert(analysis_record).execute()
        
        print("✅ Analysis saved to database")
        return True
    
    except Exception as e:
        print(f"⚠️  Could not save to database: {str(e)}")
        print("Note: You may need to add the strategic_analysis table to your schema")
        return False

def print_analysis(analysis):
    """Pretty print the strategic analysis"""
    print("\n" + "="*70)
    print("🎯 STRATEGIC INTELLIGENCE ANALYSIS")
    print("="*70)
    
    print(f"\n📋 EXECUTIVE SUMMARY:")
    print(f"   {analysis.get('executive_summary', 'No summary available')}")
    
    if analysis.get('critical_threats'):
        print(f"\n🚨 CRITICAL THREATS ({len(analysis['critical_threats'])}):")
        for threat in analysis['critical_threats']:
            print(f"\n   ⚠️  {threat.get('threat', 'Unknown threat')}")
            print(f"      Impact: {threat.get('impact', 'unknown')}")
            print(f"      Recommendation: {threat.get('recommendation', 'No recommendation')}")
            print(f"      Urgency: {threat.get('urgency', 'unknown')}")
    
    if analysis.get('opportunities'):
        print(f"\n💡 OPPORTUNITIES ({len(analysis['opportunities'])}):")
        for opp in analysis['opportunities']:
            print(f"\n   ✨ {opp.get('opportunity', 'Unknown opportunity')}")
            print(f"      Value: {opp.get('value', 'unknown')}")
            print(f"      Action: {opp.get('action', 'No action specified')}")
    
    if analysis.get('competitor_movements'):
        print(f"\n🎯 COMPETITOR MOVEMENTS ({len(analysis['competitor_movements'])}):")
        for comp in analysis['competitor_movements']:
            print(f"\n   🏢 {comp.get('company', 'Unknown company')}")
            print(f"      Activity: {comp.get('activity', 'No activity')}")
            print(f"      Meaning: {comp.get('strategic_meaning', 'Unknown')}")
            print(f"      Response: {comp.get('response', 'No response')}")
    
    if analysis.get('strategic_priorities'):
        print(f"\n📌 TOP PRIORITIES FOR THIS WEEK:")
        for i, priority in enumerate(analysis['strategic_priorities'], 1):
            print(f"   {i}. {priority}")
    
    print("\n" + "="*70)

def run_strategic_analyst():
    """Main function to run strategic analysis"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║         NATILUS AI STRATEGIC ANALYST                     ║
    ║              Powered by Claude Sonnet 4                  ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    if not ANTHROPIC_API_KEY or ANTHROPIC_API_KEY == "your_anthropic_key":
        print("❌ ERROR: ANTHROPIC_API_KEY not set in .env")
        print("Get free key at: https://console.anthropic.com")
        return
    
    # Fetch all intelligence
    intelligence_data = fetch_all_intelligence()
    
    # Check if we have any data
    total_items = (len(intelligence_data['jobs']) + len(intelligence_data['patents']) + 
                  len(intelligence_data['suppliers']) + len(intelligence_data['news']) + 
                  len(intelligence_data['talent']))
    
    if total_items == 0:
        print("⚠️  No intelligence data found. Run the scrapers first!")
        return
    
    # Analyze with Claude
    analysis = analyze_with_claude(intelligence_data)
    
    # Print analysis
    print_analysis(analysis)
    
    # Save to database
    save_analysis_to_supabase(analysis)
    
    print("\n✅ Strategic analysis complete!")

if __name__ == "__main__":
    run_strategic_analyst()
