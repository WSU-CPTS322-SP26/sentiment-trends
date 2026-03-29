import os
from dotenv import load_dotenv
from supabase import create_client
from datetime import datetime, date
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from atproto import Client
import uuid
import requests
from pytrends.request import TrendReq

from bluesky_topics import get_search_topics


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




client = Client()
client.login(bluesky_handle, bluesky_password)


sia = SentimentIntensityAnalyzer()


supabase = create_client(supabase_url, supabase_key)


#1) read feed
#2) extract topics

source_results = client.app.bsky.feed.search_posts({
    "q": "*",
    "limit": 25
})


source_posts = source_results.posts
trending_topics = get_search_topics()



today = date.today().isoformat()



for topic in trending_topics:
    results = client.app.bsky.feed.search_posts({
        "q": topic,
        "limit": 10
    })


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