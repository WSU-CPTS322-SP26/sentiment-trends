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



results = client.app.bsky.feed.search_posts(
    {
        "q": "Ford Motor Company",
        "limit": 10
    }
)

for post in results.posts:
    print(post.record.text)
    print(sia.polarity_scores(post.record.text))
for post in results.posts:
    print(post.record.text)








supabase = create_client(supabase_url, supabase_key)






positive = 0
negative = 0
neutral = 0

row_id = str(uuid.uuid4())

today = date.today().isoformat()
supabase.table("data").upsert(
    {
        "id": row_id,
        "pos": positive,
        "neu": neutral,
        "neg": negative,
        "topic": "the topic!"
    },
    on_conflict="id"
).execute()
