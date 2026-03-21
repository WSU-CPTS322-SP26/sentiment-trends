import os
from dotenv import load_dotenv
from supabase import create_client
from datetime import datetime, date
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from atproto import Client
import uuid

#First)   get trending topics
#Second)  load 20 posts for each trending topic
#Third)   run sentiment analysis on each post
#Fourth)  store sentiment data and topic in supabase db




load_dotenv()



bluesky_handle = os.getenv("BLUESKY_HANDLE")
bluesky_password = os.getenv("BLUESKY_APP_PASSWORD")
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_KEY")

client = Client()
client.login(bluesky_handle, bluesky_password)


sia = SentimentIntensityAnalyzer()


supabase = create_client(supabase_url, supabase_key)




results = client.app.bsky.feed.search_posts(
    {
        "q": "Tesla",
        "limit": 10
    }
)

for post in results.posts:
    print(post.record.text)
    scores = sia.polarity_scores(post.record.text)
    negative = scores['neg']
    neutral = scores['neu']
    positive = scores['pos']
    compound = scores['compound']


    row_id = str(uuid.uuid4())

    today = date.today().isoformat()
    supabase.table("data").upsert(
        {
            "id": row_id,
            "pos": positive,
            "neu": neutral,
            "neg": negative,
            "topic": "the topic!",
            "compound": compound
        },
        on_conflict="id"
    ).execute()