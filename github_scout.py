# github_scout.py
import requests
import time
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

class GitHubScout:
    def __init__(self):
        self.supabase = create_client(
            os.getenv('SUPABASE_URL'),
            os.getenv('SUPABASE_KEY')
        )
        # GitHub API allows 60 requests/hour without auth
        self.headers = {
            'Accept': 'application/vnd.github.v3+json'
        }
    
    def find_aerospace_engineers(self):
        """Find engineers with aerospace experience on GitHub"""
        print("👨‍💻 Searching GitHub for aerospace engineers...")
        
        base_url = "https://api.github.com/search/users"
        
        # Search queries targeting aerospace engineers
        queries = [
            "Boeing location:Seattle aerospace",
            "Spirit AeroSystems",
            "composite materials aircraft",
            "UAV autopilot",
            "flight dynamics",
            "CFD aerospace"
        ]
        
        all_talent = []
        
        for query in queries:
            params = {
                'q': query,
                'sort': 'followers',
                'per_page': 5  # Keep it small to avoid rate limits
            }
            
            try:
                response = requests.get(base_url, params=params, headers=self.headers)
                
                if response.status_code == 200:
                    users = response.json().get('items', [])
                    
                    for user in users:
                        # Get detailed profile
                        time.sleep(1)  # Be nice to GitHub's API
                        profile_response = requests.get(user['url'], headers=self.headers)
                        
                        if profile_response.status_code == 200:
                            profile = profile_response.json()
                            
                            # Check if they're hireable or recently updated
                            if profile.get('hireable') or profile.get('bio'):
                                talent = {
                                    'name': profile.get('name', user['login']),
                                    'current_company': profile.get('company', 'Unknown'),
                                    'location': profile.get('location', 'Unknown'),
                                    'title': f"Engineer ({profile.get('bio', 'Aerospace')[:50]})" if profile.get('bio') else 'Software Engineer',
                                    'linkedin_url': profile['html_url'],
                                    'is_open_to_work': profile.get('hireable', False),
                                    'skills': f"GitHub: {profile.get('public_repos', 0)} repos, {profile.get('followers', 0)} followers",
                                    'priority_score': min(50 + profile.get('followers', 0), 95),
                                    'notes': f"GitHub profile - {profile.get('bio', '')[:100]}"
                                }
                                
                                all_talent.append(talent)
                                print(f"✅ Found: {talent['name']} at {talent['current_company']}")
                
                elif response.status_code == 403:
                    print("⚠️ GitHub API rate limit reached. Wait 1 hour.")
                    break
                    
            except Exception as e:
                print(f"❌ Error searching GitHub: {e}")
            
            time.sleep(2)  # Pause between searches
        
        return all_talent
    
    def save_to_database(self, talent):
        """Save GitHub talent to database"""
        if talent:
            try:
                for person in talent:
                    # Use upsert to avoid duplicates
                    self.supabase.table('aerospace_talent').upsert(
                        person,
                        on_conflict='name'
                    ).execute()
                print(f"💾 Saved {len(talent)} GitHub profiles")
            except Exception as e:
                print(f"❌ Database error: {e}")
    
    def run(self):
        """Run GitHub talent search"""
        talent = self.find_aerospace_engineers()
        self.save_to_database(talent)
        return talent

if __name__ == "__main__":
    scout = GitHubScout()
    talent = scout.run()
    print(f"\n👨‍💻 Total GitHub talent found: {len(talent)}")