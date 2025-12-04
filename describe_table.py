# describe_table.py
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    raise RuntimeError("Supabase environment variables missing")

supabase: Client = create_client(url, key)

TABLE = "competitor_news"

print(f"🔍 Fetching schema for table: {TABLE}")

# Query the schema
result = supabase.table("competitor_news").select("*").limit(1).execute()

print("\n📌 Columns detected in competitor_news:")

if hasattr(result, "data") and len(result.data) > 0:
    # If table has rows, print keys of the first row
    for col in result.data[0].keys():
        print(" -", col)
else:
    # If the table is empty, we must query Postgres system catalog
    print("⚠️ Table is empty; querying PostgreSQL catalog...")

    query = """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'competitor_news'
        ORDER BY ordinal_position;
    """

    pg_result = supabase.rpc("execute_raw", {"query": query}).execute()

    if hasattr(pg_result, "data"):
        for row in pg_result.data:
            print(" -", row["column_name"])
    else:
        print("❌ Could not read schema. Check permissions.")
