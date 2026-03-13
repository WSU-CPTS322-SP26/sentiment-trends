from datetime import datetime
import json
import os

from backend.apis import bluesky_data, bluesky
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer  # type: ignore[import-untyped]

# Optional Supabase import
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

# Initialize VADER analyzer
analyzer = SentimentIntensityAnalyzer()

def save_to_supabase(topic: str, compound_score: float, post_text: str):
    """Insert compound sentiment score into Supabase table `topic_sentiment_data`."""
    if supabase is None:
        print(f"Supabase client not configured. Skipping insert for topic: {topic}")
        return
    try:
        supabase.table("topic_sentiment_data").insert({
            "topic": topic,
            "timestamp": datetime.utcnow().isoformat(),
            "compound": compound_score,
            "post_text": post_text[:1000]  # optional: limit text length
        }).execute()
        print(f"Inserted topic '{topic}' into Supabase with compound={compound_score}")
    except Exception as e:
        print(f"Supabase insert error for topic '{topic}': {e}")

def analyze_topic_posts(keyword: str):
    """Search posts via Bluesky API and calculate compound sentiment per post."""
    posts_result = bluesky.search_posts(keyword, limit=50, sort="top")
    posts = posts_result.get("posts", []) if isinstance(posts_result, dict) else []
    if not posts:
        return []

    results = []
    for post in posts:
        text = post.get("text", "").strip()
        if not text:
            continue
        scores = analyzer.polarity_scores(text)
        compound = scores.get("compound")
        results.append({"text": text, "compound": compound})
    return results

def main():
    os.makedirs("data", exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")

    for topic, keyword in TOPICS.items():
        analyzed_posts = analyze_topic_posts(keyword)

        if not analyzed_posts:
            print(f"No posts found for topic '{topic}'")
            continue

        # Save local JSON backup
        filename = f"data/{topic.replace(' ', '_')}_{timestamp}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(analyzed_posts, f, ensure_ascii=False, indent=2)
        print(f"Saved {filename}")

        # Insert each post's sentiment into Supabase
        for post_data in analyzed_posts:
            compound_score = post_data["compound"]
            post_text = post_data["text"]
            save_to_supabase(topic, compound_score, post_text)

if __name__ == "__main__":
    main()