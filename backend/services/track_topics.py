<<<<<<< HEAD
# track_topics.py
import json
import os
from datetime import datetime
from backend import bluesky_data  # your existing analysis/processing file
from backend.services import sentiment     # sentiment is in backend/services/








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

BLUESKY_HANDLE = os.environ.get("BLUESKY_HANDLE") or (getattr(config, "BLUESKY_HANDLE", None))
BLUESKY_APP_PASSWORD = os.environ.get("BLUESKY_APP_PASSWORD") or (getattr(config, "BLUESKY_APP_PASSWORD", None))
BLUESKY_SESSION_STRING = os.environ.get("BLUESKY_SESSION_STRING") or (getattr(config, "BLUESKY_SESSION_STRING", None))
SUPABASE_URL = os.environ.get("SUPABASE_URL") or (getattr(config, "SUPABASE_URL", None))
SUPABASE_KEY = os.environ.get("SUPABASE_KEY") or (getattr(config, "SUPABASE_KEY", None))


supabase: "Client | None" = None
if SUPABASE_URL and SUPABASE_KEY:
    if create_client is None:
        raise RuntimeError(
            "Supabase credentials are set, but the `supabase` package isn't installed."
        )
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    
# Initialize Supabase client if credentials exist
supabase: "Client | None" = None
if SUPABASE_URL and SUPABASE_KEY:
    if create_client is None:
        raise RuntimeError(
            "Supabase credentials are set, but the `supabase` package isn't installed. "
            "Add `supabase` to backend/requirements.txt."
        )
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
=======
from datetime import datetime
import json
import os

from backend.apis import bluesky    # bluesky.py is in backend/apis/
from backend.services import sentiment  # assume sentiment.analyze_text(text) returns VADER scores
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer  # type: ignore[import-untyped]

from backend import bluesky_data        # bluesky_data.py is in backend/

try:
    from supabase import create_client
except Exception:
    create_client = None

# Topics to track and their search keywords
TOPICS = {
    "python": "python programming",
    "ai": "artificial intelligence",
    "bluesky": "bluesky social",
}

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
    """Insert compound sentiment score into Supabase table `topic_sentiment_data`."""
    if supabase is None:
        print(f"Supabase client not configured. Skipping insert for topic: {topic}")
        return
    try:
        supabase.table("topic_sentiment_data").insert({
            "topic": topic,
            "timestamp": datetime.utcnow().isoformat(),
            "compound": compound_score
        }).execute()
        print(f"Inserted topic '{topic}' into Supabase with compound={compound_score}")
    except Exception as e:
        print(f"Supabase insert error for topic '{topic}': {e}")

def analyze_topic_posts(keyword: str):
    """Search posts via Bluesky API and calculate compound sentiment."""
    posts_result = bluesky.search_posts(keyword, limit=50, sort="top")
    posts = posts_result.get("posts", []) if isinstance(posts_result, dict) else []
    if not posts:
        return None  # no posts found

    # Combine text from all posts to analyze
    combined_text = " ".join([p.get("text", "") for p in posts if p.get("text")])
    if not combined_text.strip():
        return None  # no text content

    # Run sentiment analysis
    scores = sentiment.analyze_text(combined_text)  # returns dict with 'compound'
    compound = scores.get("compound")
    return compound

def main():
    os.makedirs("data", exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")

    for topic, keyword in TOPICS.items():
        compound_score = analyze_topic_posts(keyword)

        # Save local JSON backup
        result_data = {"topic": topic, "keyword": keyword, "compound": compound_score}
        filename = f"data/{topic.replace(' ', '_')}_{timestamp}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)
        print(f"Saved {filename}")

        # Insert into Supabase if we have a compound score
        if compound_score is not None:
            save_to_supabase(topic, compound_score)
        else:
            print(f"No posts or compound score found for topic '{topic}', skipping Supabase insert.")
>>>>>>> 6d12b1b24ed914e31545cb84a9c687f4771f12aa

if __name__ == "__main__":
    main()