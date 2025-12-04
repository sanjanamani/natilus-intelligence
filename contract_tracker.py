# contract_tracker.py
import requests
import json
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

class ContractTracker:
    def __init__(self):
        self.supabase = create_client(
            os.getenv('SUPABASE_URL'),
            os.getenv('SUPABASE_KEY')
        )
    
    def get_federal_contracts(self):
        """Track aerospace contracts from USASpending.gov"""
        print("💰 Fetching federal contracts...")
        
        url = "https://api.usaspending.gov/api/v2/search/spending_by_award/"
        
        # Search for recent aerospace contracts
        payload = {
            "filters": {
                "keywords": ["aircraft", "aerospace", "UAV", "blended wing"],
                "time_period": [{
                    "start_date": (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d"),
                    "end_date": datetime.now().strftime("%Y-%m-%d")
                }],
                "award_type_codes": ["A", "B", "C", "D"],  # Contract types
                "award_amounts": [{
                    "lower_bound": 1000000,  # Only $1M+ contracts
                    "upper_bound": 999999999
                }]
            },
            "limit": 50,
            "page": 1
        }
        
        try:
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                contracts = data.get('results', [])
                
                contract_insights = []
                
                for contract in contracts:
                    recipient = contract.get('recipient_name', '')
                    
                    # Check if it's a competitor
                    if any(company in recipient for company in ['JetZero', 'Boeing', 'Lockheed', 'Northrop']):
                        contract_insights.append({
                            'company': recipient,
                            'news_type': 'Federal Contract',
                            'details': f"${contract.get('award_amount', 0):,.0f} - {contract.get('description', 'Classified')[:100]}",
                            'impact_on_natilus': 'HIGH - Competitor funding',
                            'date_detected': contract.get('action_date', '')
                        })
                
                print(f"✅ Found {len(contract_insights)} relevant contracts")
                return contract_insights
            else:
                print(f"❌ USASpending API error: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Error fetching contracts: {e}")
            return []
    
    def save_to_database(self, contracts):
        """Save contract intelligence to database"""
        if contracts:
            try:
                for contract in contracts:
                    self.supabase.table('competitor_moves').insert(contract).execute()
                print(f"💾 Saved {len(contracts)} contract insights")
            except Exception as e:
                print(f"❌ Database error: {e}")
    
    def run(self):
        """Run contract tracking"""
        contracts = self.get_federal_contracts()
        self.save_to_database(contracts)
        return contracts

if __name__ == "__main__":
    tracker = ContractTracker()
    contracts = tracker.run()
    print(f"\n💰 Total contracts tracked: {len(contracts)}")