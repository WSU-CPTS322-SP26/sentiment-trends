from datetime import datetime
import json
import os

from backend.apis import bluesky    # bluesky.py is in backend/apis/
from backend.services import sentiment  # assume sentiment.analyze_text(text) returns VADER scores

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

if __name__ == "__main__":
    main()