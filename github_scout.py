# github_scout.py
import os
import time
from typing import Any, Dict, List, Optional

import requests

from simple_db import SimpleSupabase


GITHUB_API_URL = "https://api.github.com"


class GithubScout:
    def __init__(self) -> None:
        self.db = SimpleSupabase()
        self.token = os.getenv("GITHUB_TOKEN")

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/vnd.github+json",
                "User-Agent": "natilus-intelligence-github-scout",
            }
        )
        if self.token:
            self.session.headers["Authorization"] = f"Bearer {self.token}"

        # These are the signals you care about for Natilus
        self.search_queries: List[str] = [
            "Boeing aerodynamic engineer",
            "Spirit Aerosystems composite engineer",
            "Airbus aero structures",
            "electric aircraft aerospace engineer",
        ]

    def _search_users(self, query: str, per_page: int = 5) -> List[Dict[str, Any]]:
        print(f"🔍 Searching GitHub: {query}")
        params = {"q": query, "per_page": per_page}
        resp = self.session.get(f"{GITHUB_API_URL}/search/users", params=params, timeout=20)

        if resp.status_code == 403:
            print("⚠️ GitHub rate limit or auth issue. Set GITHUB_TOKEN to increase limits.")
            return []

        if not resp.ok:
            print(f"⚠️ GitHub search error {resp.status_code}: {resp.text}")
            return []

        data = resp.json()
        return data.get("items", [])

    def _fetch_user_details(self, login: str) -> Optional[Dict[str, Any]]:
        resp = self.session.get(f"{GITHUB_API_URL}/users/{login}", timeout=20)
        if not resp.ok:
            print(f"⚠️ Failed to fetch details for {login}: {resp.status_code}")
            return None
        return resp.json()

    def _build_talent_row(
        self, user: Dict[str, Any], details: Dict[str, Any], source_query: str
    ) -> Dict[str, Any]:
        name = details.get("name") or user.get("login")
        location = details.get("location") or ""
        company = details.get("company") or ""

        notes_parts = []
        if source_query:
            notes_parts.append(f"Found via GitHub search: '{source_query}'")
        if details.get("bio"):
            notes_parts.append(f"Bio: {details['bio'][:180]}")

        notes = " | ".join(notes_parts)

        return {
            "name": name,
            "current_company": company,
            "location": location,
            "github_login": user.get("login"),
            "github_url": user.get("html_url"),
            "notes": notes,
            "priority_score": 85,  # default; you can tune this later
            "is_open_to_work": True,  # you could infer from bio if you want
        }

    def run(self) -> List[Dict[str, Any]]:
        all_talent: List[Dict[str, Any]] = []

        for query in self.search_queries:
            users = self._search_users(query)
            for user in users:
                login = user.get("login")
                if not login:
                    continue

                details = self._fetch_user_details(login)
                if not details:
                    continue

                row = self._build_talent_row(user, details, query)
                print(f"✅ Found: {row['name']} at {row['current_company'] or 'Unknown'}")
                all_talent.append(row)

                # be gentle with the API
                time.sleep(0.4)

        # Save to Supabase
        saved = 0
        if all_talent:
            try:
                saved = self.db.insert_rows("aerospace_talent", all_talent)
                print(f"\n💾 Saved {saved} GitHub engineers to aerospace_talent")
            except Exception as e:
                print(f"\n⚠️ Could not save to Supabase: {e}")

        print(f"\n👨‍💻 Total GitHub talent found: {len(all_talent)}")
        return all_talent


if __name__ == "__main__":
    scout = GithubScout()
    scout.run()
