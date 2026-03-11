from datetime import datetime
import json
from backend import bluesky_data  # your analysis file
import os

TOPICS = ["python", "ai", "bluesky"]

def main():
    os.makedirs("data", exist_ok=True)  # make sure folder exists
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    
    for topic in TOPICS:
        result = bluesky_data.analyze_topic(topic, limit_per_platform=25, top_n=5)
        filename = f"data/{topic.replace(' ', '_')}_{timestamp}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"Saved {filename}")

if __name__ == "__main__":
    main()