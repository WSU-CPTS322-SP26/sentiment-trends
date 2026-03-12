from datetime import datetime
import json
import os

from backend import bluesky_data
from backend.services import sentiment  # noqa: F401 (import kept if used elsewhere)

# Optional Supabase import so the script can still run without it
try:
    from supabase import create_client
except Exception:
    create_client = None

# Topics to track
TOPICS = ["python", "ai", "bluesky"]

# Load credentials from environment
BLUESKY_HANDLE = os.getenv("BLUESKY_HANDLE")
BLUESKY_APP_PASSWORD = os.getenv("BLUESKY_APP_PASSWORD")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

# Initialize Supabase client
supabase = None
if SUPABASE_URL and SUPABASE_SERVICE_KEY:
    if create_client is None:
        raise RuntimeError(
            "Supabase credentials found but `supabase` package is not installed."
        )
    supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    print("Supabase client initialized successfully")
else:
    print("Supabase URL or SERVICE KEY not set. Skipping database inserts.")


def save_to_supabase(topic: str, compound_score: float):
    """Insert analyzed topic data into Supabase (table: topic_sentiment_data)."""
    if supabase is None:
        print(f"Supabase client not configured. Skipping insert for topic: {topic}")
        return

    try:
        response = (
            supabase.table("topic_sentiment_data")
            .insert(
                {
                    "topic": topic,
                    "timestamp": datetime.utcnow().isoformat(),
                    "compound": compound_score,
                }
            )
            .execute()
        )
        print(f"Inserted topic '{topic}' into Supabase")
    except Exception as e:
        print(f"Supabase insert error for topic '{topic}': {e}")


def main():
    """Main pipeline for analyzing topics and storing results."""
    os.makedirs("data", exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")

    for topic in TOPICS:
        # Run analysis
        result = bluesky_data.analyze_topic(
            topic,
            limit_per_platform=25,
            top_n=5,
        )

        # Save local JSON backup
        filename = f"data/{topic.replace(' ', '_')}_{timestamp}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"Saved {filename}")

        # Extract compound score (assumes `result` has a key like 'compound')
        compound_score = result.get("compound")
        if compound_score is None:
            print(f"No compound score found for topic '{topic}', skipping Supabase insert.")
        else:
            # Insert numeric compound score into Supabase
            save_to_supabase(topic, compound_score)


if __name__ == "__main__":
    main()