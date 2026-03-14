import json
from datetime import datetime
from backend import bluesky_data  # your analysis file

TOPICS = ["python", "ai", "bluesky"]  # topics to track

def main():
    timestamp = datetime.utcnow().isoformat()
    for topic in TOPICS:
        result = bluesky_data.analyze_topic(topic, limit_per_platform=25, top_n=5)
        # Save results locally as JSON (or you can push to a DB)
        filename = f"data/{topic.replace(' ', '_')}_{timestamp}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"Saved {filename}")

if __name__ == "__main__":
    main()