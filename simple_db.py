# simple_db.py - unified Supabase helper for local + Streamlit Cloud

import os
import json
from typing import Any, Dict, List, Union

import requests
from dotenv import load_dotenv

try:
    import streamlit as st  # type: ignore
except ImportError:
    st = None


class SimpleSupabase:
    def __init__(self) -> None:
        # Load .env for local runs
        load_dotenv()

        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")

        # Fallback to st.secrets when running on Streamlit Cloud
        if (not url or not key) and st is not None:
            try:
                secrets = st.secrets
                url = url or secrets.get("SUPABASE_URL")
                key = key or secrets.get("SUPABASE_KEY")
            except Exception:
                pass

        if not url or not key:
            raise RuntimeError(
                "Supabase URL or KEY not set. "
                "Set SUPABASE_URL and SUPABASE_KEY in .env (local) "
                "OR in Streamlit secrets (cloud)."
            )

        self.url = url.rstrip("/")
        self.key = key
        self.headers = {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation",
        }

    # ---------- Generic helpers ----------

    def insert_rows(
        self, table: str, rows: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Low-level insert with basic error handling."""
        resp = requests.post(
            f"{self.url}/rest/v1/{table}",
            headers=self.headers,
            data=json.dumps(rows),
        )
        if not resp.ok:
            raise RuntimeError(
                f"Supabase insert error {resp.status_code}: {resp.text}"
            )
        try:
            return resp.json()
        except Exception:
            return []

    def fetch_table(
        self, table: str, limit: int = 200
    ) -> List[Dict[str, Any]]:
        resp = requests.get(
            f"{self.url}/rest/v1/{table}?select=*&limit={limit}",
            headers=self.headers,
        )
        if not resp.ok:
            raise RuntimeError(
                f"Supabase fetch error {resp.status_code}: {resp.text}"
            )
        try:
            return resp.json()
        except Exception:
            return []

    # ---------- Domain-specific helpers ----------

    def insert_talent(
        self, talent: Union[Dict[str, Any], List[Dict[str, Any]]]
    ) -> List[Dict[str, Any]]:
        """Insert into aerospace_talent. Only send columns that really exist."""
        if isinstance(talent, dict):
            rows = [talent]
        else:
            rows = talent

        # These are safe, schema-based columns you actually have
        allowed_cols = {
            "name",
            "current_company",
            "previous_company",
            "title",
            "location",
            "years_experience",
            "linkedin_url",
            "is_open_to_work",
            "priority_score",
            "skills",
            "notes",
            "risk_of_poaching",
        }

        cleaned: List[Dict[str, Any]] = []
        for row in rows:
            cleaned.append({k: v for k, v in row.items() if k in allowed_cols})

        if not cleaned:
            return []
        return self.insert_rows("aerospace_talent", cleaned)

    def insert_competitor_news(
        self, news: Union[Dict[str, Any], List[Dict[str, Any]]]
    ) -> List[Dict[str, Any]]:
        """Insert into competitor_news, matching its actual schema:
           id, company, news_type, details, impact_on_natilus, date_detected
        """
        if isinstance(news, dict):
            rows = [news]
        else:
            rows = news

        allowed_cols = {
            "company",
            "news_type",
            "details",
            "impact_on_natilus",
            "date_detected",
        }

        cleaned: List[Dict[str, Any]] = []
        for row in rows:
            cleaned.append({k: v for k, v in row.items() if k in allowed_cols})

        if not cleaned:
            return []
        return self.insert_rows("competitor_news", cleaned)

    def insert_supply_chain(
        self, items: Union[Dict[str, Any], List[Dict[str, Any]]]
    ) -> List[Dict[str, Any]]:
        """Insert into supply_chain_opportunities (whatever schema you defined there)."""
        if isinstance(items, dict):
            rows = [items]
        else:
            rows = items

        return self.insert_rows("supply_chain_opportunities", rows)
