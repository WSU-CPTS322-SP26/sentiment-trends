from datetime import datetime
import json
import os
from backend import bluesky_data  # analysis file
from backend.services import sentiment  # sentiment processing

# Optional: Supabase client (keep import optional so the script can still run)
try:
    from supabase import Client, create_client  # type: ignore[import-untyped]
except Exception:  # pragma: no cover
    Client = None  # type: ignore[assignment]
    create_client = None  # type: ignore[assignment]

# Topics to track
TOPICS = ["python", "ai", "bluesky"]

# Load credentials (env vars override config.py)
try:
    from backend import config
except ImportError:
    config = None




BLUESKY_HANDLE = os.environ.get("BLUESKY_HANDLE")
BLUESKY_APP_PASSWORD = os.environ.get("BLUESKY_APP_PASSWORD")
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")

# Initialize Supabase client if credentials exist
supabase: "Client | None" = None
if SUPABASE_URL and SUPABASE_KEY:
    if create_client is None:
        raise RuntimeError(
            "Supabase credentials are set, but the `supabase` package isn't installed. "
            "Add `supabase` to backend/requirements.txt."
        )
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("Supabase client initialized successfully")
else:
    print("Supabase URL or KEY not set. Skipping database inserts.")

def save_to_supabase(topic: str, data: dict):
    """Insert analyzed topic data into Supabase (table: 'topics')."""
    if supabase is None:
        print(f"Supabase client not configured. Skipping insert for topic: {topic}")
        return
    try:
        response = supabase.table("topics").insert({
            "topic": topic,
            "timestamp": datetime.utcnow().isoformat(),
            "data": json.dumps(data)
        }).execute()
        print(f"Inserted topic '{topic}' into Supabase: {response}")
    except Exception as e:
        print(f"Supabase insert error for topic '{topic}': {e}")

def main():
    os.makedirs("data", exist_ok=True)  # make sure folder exists
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")

    for topic in TOPICS:
        # Analyze topic
        result = bluesky_data.analyze_topic(topic, limit_per_platform=25, top_n=5)

        # Save locally
        filename = f"data/{topic.replace(' ', '_')}_{timestamp}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"Saved {filename}")

        # Send to Supabase for this topic
        save_to_supabase(topic, result)

if __name__ == "__main__":
    main()