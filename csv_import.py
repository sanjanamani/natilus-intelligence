# csv_import.py - import manual talent into Supabase
import csv
from pathlib import Path
from simple_db import SimpleSupabase

CSV_PATH = Path("data") / "aerospace_talent_manual.csv"


def load_manual_talent():
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"CSV not found at {CSV_PATH}. Create it first.")

    rows = []
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
    # Expected headers:
    # name,current_company,previous_company,title,location,years_experience,
    # linkedin_url,skills,is_open_to_work,notes,priority_score,source_tag

        for raw in reader:
            # normalize booleans and ints
            is_open = str(raw.get("is_open_to_work", "")).strip().lower() in ("true", "1", "yes", "y")
            years = raw.get("years_experience")
            years = int(years) if years not in (None, "", " ") else None

            priority = raw.get("priority_score")
            priority = int(priority) if priority not in (None, "", " ") else None

            row = {
                "name": raw.get("name"),
                "current_company": raw.get("current_company") or None,
                "previous_company": raw.get("previous_company") or None,
                "title": raw.get("title") or None,
                "location": raw.get("location") or None,
                "years_experience": years,
                "linkedin_url": raw.get("linkedin_url") or None,
                "skills": raw.get("skills") or None,
                "is_open_to_work": is_open,
                "layoff_date": None,  # leave null
                "risk_of_poaching": None,
                "competitor_interest": None,
                "notes": raw.get("notes") or None,
                "priority_score": priority,
                "github_login": None,
                "github_url": None,
                "source_tag": raw.get("source_tag") or "manual_linkedin",
            }
            rows.append(row)
    return rows


def main():
    print(f"📥 Importing manual talent from {CSV_PATH} ...")
    db = SimpleSupabase()

    rows = load_manual_talent()
    if not rows:
        print("⚠️ No rows found in CSV. Did you add any people?")
        return

    inserted = db.insert_talent(rows)
    print(f"✅ Imported {len(inserted)} manual talent profiles into aerospace_talent")


if __name__ == "__main__":
    main()
