# track_topics.py
import json
import os
from datetime import datetime
from backend import bluesky_data  # your existing analysis/processing file
from backend.services import sentiment     # sentiment is in backend/services/


# Optional: Supabase client
from supabase import create_client, Client  # make sure supabase-py is in requirements

# Topics to track
TOPICS = ["python", "ai", "bluesky"]

# Load credentials (env vars override config.py)
try:
    from backend import config
except ImportError:
    config = None

BLUESKY_HANDLE = os.environ.get("BLUESKY_HANDLE") or (getattr(config, "BLUESKY_HANDLE", None))
BLUESKY_APP_PASSWORD = os.environ.get("BLUESKY_APP_PASSWORD") or (getattr(config, "BLUESKY_APP_PASSWORD", None))
BLUESKY_SESSION_STRING = os.environ.get("BLUESKY_SESSION_STRING") or (getattr(config, "BLUESKY_SESSION_STRING", None))
SUPABASE_URL = os.environ.get("SUPABASE_URL") or (getattr(config, "SUPABASE_URL", None))
SUPABASE_KEY = os.environ.get("SUPABASE_KEY") or (getattr(config, "SUPABASE_KEY", None))

# Initialize Supabase client if credentials exist
supabase: Client | None = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_to_supabase(topic: str, data: dict):
    """Insert analyzed topic data into Supabase (table: 'topics')."""
    if supabase is None:
        print("Supabase client not configured. Skipping DB insert.")
        return
    try:
        # Customize your table/columns as needed
        response = supabase.table("topics").insert({
            "topic": topic,
            "timestamp": datetime.utcnow().isoformat(),
            "data": json.dumps(data)
        }).execute()
        print(f"Inserted into Supabase: {response}")
    except Exception as e:
        print(f"Supabase insert error: {e}")

def main():
    timestamp = datetime.utcnow().isoformat()

    # Ensure local data folder exists
    os.makedirs("data", exist_ok=True)

    for topic in TOPICS:
        print(f"Processing topic: {topic}")
        result = bluesky_data.analyze_topic(topic, limit_per_platform=25, top_n=5)

        # Save results locally
        filename = f"data/{topic.replace(' ', '_')}_{timestamp}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"Saved local file: {filename}")

        # Save results to Supabase
        save_to_supabase(topic, result)

if __name__ == "__main__":
    main()