import os
from dotenv import load_dotenv
from supabase import create_client
from datetime import datetime, date
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from atproto import Client
import uuid
import requests
from pytrends.request import TrendReq
import time
import httpx
from bluesky_topics import get_search_topics, fetch_timeline, create_session


def retry_request(func, *args, retries=3, delay=2, **kwargs):
    for attempt in range(retries):
        try:
            return func(*args, **kwargs)
        except httpx.ReadTimeout:
            print(f"Read timeout on attempt {attempt + 1}/{retries}...")
        except Exception as e:
            print(f"Request failed on attempt {attempt + 1}/{retries}: {e}")

        if attempt < retries - 1:
            time.sleep(delay)

    return None


load_dotenv()


#First)   get trending topics
#Second)  load # of posts for each trending topic
#Third)   run sentiment analysis on each post
#Fourth)  store sentiment data and topic in supabase


#topics should have many categories
#
#examples: currencies, celebs, companies or stocks



#trending topics(hard coded)
#trending_topics = ["Meta","Tesla","Instagram","AI","Ford"]






bluesky_handle = os.getenv("BLUESKY_HANDLE")
bluesky_password = os.getenv("BLUESKY_APP_PASSWORD")
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_KEY")

MAX_POSTS = 200
PAGE_SIZE = 50


client = Client()
client.login(bluesky_handle, bluesky_password)


sia = SentimentIntensityAnalyzer()


supabase = create_client(supabase_url, supabase_key)


#1) read feed
#2) extract topics




session = create_session()


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


trending_topics = get_search_topics(all_posts)



today = date.today().isoformat()



for topic in trending_topics:
    results = retry_request(
    client.app.bsky.feed.search_posts,
    {"q": topic, "limit": 10}
)
    if results is None:
        print(f"Skipping topic '{topic}' due to repeated timeout.")
        continue

    time.sleep(1)

    for post in results.posts:
        print(post.record.text)
        scores = sia.polarity_scores(post.record.text)
        negative = scores['neg']
        neutral = scores['neu']
        positive = scores['pos']
        compound = scores['compound']


        row_id = str(uuid.uuid4())

        supabase.table("data").upsert(
            {
                "id": row_id,
                "pos": positive,
                "neu": neutral,
                "neg": negative,
                "topic": topic,
                "compound": compound
            },
            on_conflict="id"
        ).execute()