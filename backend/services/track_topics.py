import os
import json
from datetime import datetime, date
from backend import bluesky_data  # your analysis file

# Supabase client
try:
    from supabase import Client, create_client
except Exception:
    Client = None
    create_client = None

# Topics to track
TOPICS = ["python", "ai", "bluesky"]

# Supabase credentials from env vars
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Supabase credentials not set.")

if create_client is None:
    raise RuntimeError("Supabase package not installed. Add `supabase` to requirements.txt.")

supabase: "Client" = create_client(SUPABASE_URL, SUPABASE_KEY)


def save_to_supabase(positive: float, negative: float, neutral: float):
    """Insert or update sentiment data into public.table."""
    today = date.today().isoformat()
    try:
        supabase.table("table").upsert(
            {
                "id": today,
                "positive_sentiment": positive,
                "negative_sentiment": negative,
                "neutral_sentiment": neutral
            },
            on_conflict="id"
        ).execute()
        print(f"Saved sentiments for {today}: +{positive}, -{negative}, 0{neutral}")
    except Exception as e:
        print(f"Supabase insert error: {e}")


def main():
    os.makedirs("data", exist_ok=True)
    timestamp = datetime.utcnow().isoformat()

    for topic in TOPICS:
        # Analyze topic
        result = bluesky_data.analyze_topic(topic, limit_per_platform=25, top_n=5)

        # Save locally
        filename = f"data/{topic.replace(' ', '_')}_{timestamp}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"Saved local file: {filename}")

        # Extract sentiment values
        positive = result.get("positive_sentiment", 0.0)
        negative = result.get("negative_sentiment", 0.0)
        neutral = result.get("neutral_sentiment", 0.0)

        # Save to Supabase table
        save_to_supabase(positive, negative, neutral)


if __name__ == "__main__":
    main()