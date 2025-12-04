import pandas as pd
from simple_db import SimpleSupabase

db = SimpleSupabase()
df = pd.read_csv("linkedIn_export.csv")

rows = []
for _, r in df.iterrows():
    rows.append({
        "name": r["Full Name"],
        "current_company": r["Company"],
        "title": r["Job Title"],
        "location": r["Location"],
        "linkedin_url": r["LinkedIn URL"],
        "source": "linkedin_csv",
        "priority_score": 70,
    })

db.insert_talent(rows)
print(f"Inserted {len(rows)} LinkedIn rows")
