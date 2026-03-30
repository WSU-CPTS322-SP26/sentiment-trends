import os
import time
import re
import requests
from dotenv import load_dotenv
from collections import Counter

load_dotenv()

BLUESKY_HANDLE = os.getenv("BLUESKY_HANDLE")
BLUESKY_APP_PASSWORD = os.getenv("BLUESKY_APP_PASSWORD")

CREATE_SESSION_URL = "https://bsky.social/xrpc/com.atproto.server.createSession"
TIMELINE_URL = "https://bsky.social/xrpc/app.bsky.feed.getTimeline"

MAX_POSTS = 200
PAGE_SIZE = 50

STOPWORDS = {
    "the", "and", "for", "with", "from", "that", "this", "you", "are", "was", "but",
    "not", "all", "our", "can", "have", "has", "your", "they", "his", "her", "its",
    "on", "in", "at", "of", "is", "as", "to", "now", "be", "by", "it", "an", "or",
    "if", "we", "he", "she", "them", "their", "my", "me", "so", "just", "about",
    "what", "when", "who", "how", "why", "after", "before", "into", "over", "under",
    "up", "down", "out", "off", "more", "less", "than", "then", "also", "still",
    "will", "would", "could", "should", "been", "being", "do", "does", "did"
}


def create_session():
    payload = {
        "identifier": BLUESKY_HANDLE,
        "password": BLUESKY_APP_PASSWORD
    }

    resp = requests.post(CREATE_SESSION_URL, json=payload, timeout=10)

    if resp.status_code != 200:
        print("Login failed:", resp.status_code, resp.text)
        return None

    return resp.json()


def fetch_timeline(access_jwt, limit=50, cursor=None):
    headers = {
        "Authorization": f"Bearer {access_jwt}"
    }

    params = {
        "limit": limit
    }

    if cursor:
        params["cursor"] = cursor

    resp = requests.get(TIMELINE_URL, headers=headers, params=params, timeout=10)

    if resp.status_code != 200:
        print("Timeline fetch failed:", resp.status_code, resp.text)
        return None

    return resp.json()


def extract_hashtags(text):
    return re.findall(r"#\w+", text.lower())


def extract_cashtags(text):
    return re.findall(r"\$[A-Z]{1,5}\b", text)


def extract_uppercase_tickers(text):
    # catches things like NVDA, TSLA, AI, AMD
    candidates = re.findall(r"\b[A-Z]{2,5}\b", text)
    # filter obvious junk abbreviations if needed
    blacklist = {"THE", "AND", "FOR", "YOU", "ARE", "BUT", "NOT", "ALL", "CAN", "NOW"}
    return [c for c in candidates if c not in blacklist]


def extract_single_words(text):
    words = re.findall(r"\b[a-zA-Z]{2,20}\b", text.lower())
    return [w for w in words if w not in STOPWORDS]


def extract_bigrams(text):
    words = extract_single_words(text)
    return [f"{words[i]} {words[i+1]}" for i in range(len(words) - 1)]


def get_top_single_word_topics(posts, top_n=8, min_count=2):
    counter = Counter()

    for item in posts:
        try:
            text = item.get("post", {}).get("record", {}).get("text", "")
            if not text:
                continue

            words = extract_single_words(text)
            counter.update(words)

        except Exception:
            continue

    return [word for word, count in counter.most_common(top_n) if count >= min_count]


def get_top_bigram_topics(posts, top_n=8, min_count=2):
    counter = Counter()

    for item in posts:
        try:
            text = item.get("post", {}).get("record", {}).get("text", "")
            if not text:
                continue

            bigrams = extract_bigrams(text)
            counter.update(bigrams)

        except Exception:
            continue

    return [phrase for phrase, count in counter.most_common(top_n) if count >= min_count]



def get_search_topics(posts, single_top_n=5, bigram_top_n=5):
    single_topics = get_top_single_word_topics(posts, top_n=single_top_n)
    bigram_topics = get_top_bigram_topics(posts, top_n=bigram_top_n)

    topics = single_topics + bigram_topics



    seen = set()
    deduped = []
    for t in topics:
        if t not in seen:
            deduped.append(t)
            seen.add(t)

    return deduped


def main():
    session = create_session()
    if not session:
        return

    access_jwt = session["accessJwt"]

    all_posts = []
    cursor = None

    while True:
        data = fetch_timeline(access_jwt, limit=PAGE_SIZE, cursor=cursor)
        if not data:
            break

        posts = data.get("feed", [])
        all_posts.extend(posts)

        cursor = data.get("cursor")
        print(f"Fetched {len(posts)} posts, next cursor: {cursor}")

        if not cursor or len(all_posts) >= MAX_POSTS:
            break

        time.sleep(1)

    print(f"\nTotal posts fetched: {len(all_posts)}\n")

    hashtag_counter = Counter()
    cashtag_counter = Counter()
    ticker_counter = Counter()
    word_counter = Counter()
    bigram_counter = Counter()

    for item in all_posts:
        try:
            post = item.get("post", {})
            author = post.get("author", {}).get("handle", "unknown")
            text = post.get("record", {}).get("text", "")

            if not text:
                continue

            hashtags = extract_hashtags(text)
            cashtags = extract_cashtags(text)
            tickers = extract_uppercase_tickers(text)
            single_words = extract_single_words(text)
            bigrams = extract_bigrams(text)

            hashtag_counter.update(hashtags)
            cashtag_counter.update(cashtags)
            ticker_counter.update(tickers)
            word_counter.update(single_words)
            bigram_counter.update(bigrams)

            print(f"{author}: {text}")
            if hashtags:
                print("  hashtags:", hashtags)
            if cashtags:
                print("  cashtags:", cashtags)
            if tickers:
                print("  tickers:", tickers)
            print()

        except Exception as e:
            print("Error processing post:", e)

    print("\n==============================")
    print("TOP HASHTAGS")
    print("==============================")
    for tag, count in hashtag_counter.most_common(15):
        print(f"{tag}: {count}")

    print("\n==============================")
    print("TOP STOCK CASHTAGS")
    print("==============================")
    for tag, count in cashtag_counter.most_common(15):
        print(f"{tag}: {count}")

    print("\n==============================")
    print("TOP UPPERCASE TICKERS / TERMS")
    print("==============================")
    for ticker, count in ticker_counter.most_common(15):
        print(f"{ticker}: {count}")

    print("\n==============================")
    print("TOP SINGLE-WORD TOPICS")
    print("==============================")
    for word, count in word_counter.most_common(20):
        print(f"{word}: {count}")

    print("\n==============================")
    print("TOP TWO-WORD TOPICS")
    print("==============================")
    for phrase, count in bigram_counter.most_common(20):
        print(f"{phrase}: {count}")


if __name__ == "__main__":
    main()
